---
rank: 12
slug: distributed_log
---

A distributed log is an append-only, replicated sequence of records that many services write and many more read; Apache Kafka is the reference design. The checkout service appends `{order 81723: paid}` to the topic `orders`; billing, search indexing and fraud scoring each read it independently, milliseconds or days later, and a service launched next month can replay the retained history. Three questions decide the design: how to make reads and writes cheap enough for gigabytes a second on ordinary disks, how to replicate so that an acknowledged record survives a broker failure without a majority vote on every write, and how consumers share a stream so that each record is processed once even when they crash.

### Requirements

Producers append records (key, value, headers, timestamp) to named topics and learn each record's offset. A topic is split into partitions, and records with the same key land in the same partition, in order; nothing is ordered across partitions. Consumers read a partition sequentially from any offset or from the first record after a timestamp. Any number of consumer groups read a topic independently; within a group the partitions are shared out so that each record goes to one member, and progress survives restarts as committed offsets. Topics keep records for a set time or size or, when compacted, the latest record per key, and producers can write to several partitions atomically.

Assume one cluster per region carrying a million records a second on average, twice that at peak, kept for seven days. A fully replicated write should take a few milliseconds at the median and under 50 ms at the 99th percentile, and a consumer that keeps up should see a record within about 100 ms. An acknowledged record must survive the loss of any broker or availability zone, and every partition must keep accepting writes with one broker down. Delivery is at least once, with exactly-once for pipelines that read and write the log. Schemas, stream processing and connectors are out of scope.

### Estimates

```text
ingest       1 M records/s × 1 KB after compression = 1 GB/s  (peak ×2: 2 GB/s)
batching     2 GB/s in 64 KB batches ≈ 31,000 produce batches/s at peak
replication  factor 3 → 3 GB/s of disk writes, 2 GB/s between brokers
fan-out      3 consumer groups read each record → 3 GB/s out (peak 6 GB/s)
retention    7 days × 1 GB/s ≈ 605 TB × 3 replicas ≈ 1.8 PB
brokers      1.8 PB / 30 TB of log per broker ≈ 60 brokers
per broker   peak in (2 + 4) GB/s / 60 = 100 MB/s, out (4 + 6) / 60 ≈ 170 MB/s
             ≈ 5% of a 25 Gb/s NIC; disks take 100 MB/s, all sequential
page cache   48 GB per broker / 100 MB/s of writes ≈ the newest 8 minutes
partitions   500 topics × 20 = 10,000 → 30,000 replicas ≈ 500 per broker
hot topic    200 MB/s peak / 5 MB/s per consumer = 40 partitions → create 64
group state  10,000 partitions × 3 groups = 30,000 offsets × ~100 B ≈ 3 MB
rebuild      30 TB / 500 MB/s (throttled) ≈ 17 hours to refill a lost broker
```

Three numbers shape the design. Storage, not bandwidth, sizes the cluster: a week of log needs sixty brokers' worth of disk while their network cards idle at 5%, and refilling a lost broker takes most of a day, the case for tiered storage. The page cache holds the newest minutes of every partition, so consumers that keep up never touch the disks. And all groups' progress together fits in 3 MB, because a position is one integer per partition rather than an acknowledgement per message; that is what lets one log feed any number of readers.

### API

```text
Metadata(topics) → brokers; per partition: leader, leader_epoch, replicas, isr

Produce(acks = 0 | 1 | all, timeout, [(topic, partition, batch)])
  batch: producer_id, producer_epoch, base_sequence, compressed records
         [(key, value, headers, timestamp)]
  → base_offset | NOT_LEADER_OR_FOLLOWER | NOT_ENOUGH_REPLICAS
    | OUT_OF_ORDER_SEQUENCE_NUMBER         (a duplicate batch is acked again)

Fetch(replica_id?, max_wait_ms, min_bytes, isolation_level,
      [(topic, partition, fetch_offset, current_leader_epoch)])
  → batches, high_watermark, last_stable_offset
    | OFFSET_OUT_OF_RANGE | FENCED_LEADER_EPOCH
ListOffsets(topic, partition, timestamp | earliest | latest) → offset

FindCoordinator(group_id | transactional_id) → broker
JoinGroup, SyncGroup, Heartbeat(group_id, member_id, generation)
  → assigned partitions | REBALANCE_IN_PROGRESS
OffsetCommit(group_id, generation, [(topic, partition, next_offset)])
  → ok | ILLEGAL_GENERATION                OffsetFetch(group_id) → offsets

InitProducerId(transactional_id) → producer_id, epoch  (fences older epochs)
AddPartitionsToTxn, AddOffsetsToTxn, TxnOffsetCommit, EndTxn(commit | abort)
```

Clients speak a binary protocol over long-lived TCP connections, pipelining requests matched by a correlation id. Any broker answers Metadata, so clients send Produce and Fetch straight to each partition's leader and refresh on NOT_LEADER_OR_FOLLOWER. Fetch is a long poll, held until `min_bytes` arrive or `max_wait_ms` passes, and followers replicate with the same request. The offset is the cursor, so nothing paginates and the broker tracks no reader positions beyond committed offsets; ListOffsets turns a timestamp into an offset. Produce is idempotent through the producer id and sequence in each batch. Clients authenticate with SASL or mutual TLS, and ACLs apply per topic.

### Data Model

```text
metadata log   __cluster_metadata: one partition, Raft-replicated on the
               controllers; every broker keeps an in-memory copy
  topic        name, topic_id → partition count, replication factor, configs
  partition    (topic, p) → replicas [1,2,3], leader 1, leader_epoch 7,
               isr [1,2,3]
partition log  directory orders-0/ on each broker that holds a replica
  segment      00000000000001048576.log        record batches, append-only
               00000000000001048576.index      relative offset → byte, sparse
               00000000000001048576.timeindex  timestamp → offset, sparse
               leader-epoch-checkpoint         epoch → its first offset
record batch   base_offset, length, partition_leader_epoch, crc, attributes,
               producer_id, producer_epoch, base_sequence, records[]
record         offset_delta, timestamp_delta, key, value, headers
__consumer_offsets   (group, topic, partition) → next offset to read;
                     compacted, 50 partitions by hash(group_id)
__transaction_state  transactional_id → producer_id, epoch, state,
                     partitions; compacted, 50 partitions by hash(id)
```

The log is the data model. Each replica is a directory of segments named by their first offset; only the active segment takes appends and closed ones never change, so retention, compaction and tiering work on whole files. Records stay in the producer's batches, whose header carries what idempotence checks (producer id, epoch, sequence) and what failover repair uses (the leader epoch). Cluster metadata is the opposite kind of data, small and strongly consistent, so it lives in a Raft-replicated log on the controllers; consensus is the subject of Chapter 39. Group and transaction state live in compacted internal topics: a commit is a record keyed by (group, topic, partition), and a group's coordinator is the leader of the partition its id hashes to.

### Architecture

```dot
rankdir=TB;
compound=true;
prod [label="producers\nhash(key) mod N", class=client];
c1   [label="consumer 1\ngroup billing", class=client];
c2   [label="consumer 2\ngroup billing", class=client];
subgraph cluster_b1 { label="broker 1"; style="rounded,dashed"; color="#9CA3AF";
  o0L  [label="orders-0\nleader", class=store];
  o1F1 [label="orders-1\nfollower", class=store];
}
subgraph cluster_b2 { label="broker 2"; style="rounded,dashed"; color="#9CA3AF";
  o1L  [label="orders-1\nleader", class=store];
  o0F1 [label="orders-0\nfollower", class=store];
}
subgraph cluster_b3 { label="broker 3"; style="rounded,dashed"; color="#9CA3AF";
  gc   [label="group coordinator\n__consumer_offsets", class=service];
  o0F2 [label="orders-0\nfollower", class=store];
  o1F2 [label="orders-1\nfollower", class=store];
}
ctrl [label="KRaft controllers\nRaft quorum of 3", class=service];
tier [label="object store\nclosed segments", class=store];
prod -> o0L [label=" key A"];
prod -> o1L [label=" key B"];
c1 -> o0L [label=" fetch"];
c2 -> o1L [label=" fetch"];
c1 -> gc [label=" commit"];
c2 -> gc;
o0L -> o0F1 [label=" replicate"];
o0L -> o0F2;
o1L -> o1F1;
o1L -> o1F2 [label=" replicate"];
o1F1 -> ctrl [ltail=cluster_b1, style=dashed, label=" heartbeat,\n metadata"];
o0F1 -> ctrl [ltail=cluster_b2, style=dashed];
o1F2 -> ctrl [ltail=cluster_b3, style=dashed];
o1F1 -> tier [ltail=cluster_b1, style=dashed, label=" tiering"];
{rank=same; prod; c1; c2}
{rank=same; ctrl; tier}
```

The figure shows one topic, orders, with two partitions of three replicas each on three brokers. On the write path, producers hash each key to choose a partition, so key A always goes to orders-0 and key B to orders-1, batch records per partition for a few milliseconds and send each compressed batch to the partition's leader. Broker 1, the leader of orders-0, appends the batch to its active segment in the page cache. The orders-0 followers on brokers 2 and 3, already waiting in a long-poll fetch, append it to their copies and report their new log end in their next fetch. Once every in-sync replica has the batch, the leader advances the high watermark and answers an acks=all producer. Partition orders-1 works the same way, led by broker 2 with followers on brokers 1 and 3.

Consumer 1 and consumer 2 form the group billing, and the group coordinator on broker 3 has assigned them orders-0 and orders-1; a partition has one owner per group, so a third consumer would sit idle. Each consumer fetches from its leader, from the committed offset up to the high watermark, and after processing commits the next offset to read to the coordinator, which appends it to `__consumer_offsets`. When a member joins, leaves or stops heartbeating, the coordinator rebalances the partitions and starts a new generation.

Every broker heartbeats to the KRaft controllers, a Raft quorum of three holding the metadata log of topics, assignments, leaders and ISRs, and fetches that log into its own metadata cache. When a broker goes silent, the active controller elects new leaders for its partitions from their ISRs and records the change. In the background, replicas roll their active segment at 1 GB, and with tiered storage leaders copy closed segments to an object store, as broker 1 does in the figure.

### Deep Dives

#### The log on disk: segments, sparse indexes and zero-copy

A conventional broker keeps per-consumer queues in a database and updates per-message state on every delivery and acknowledgement: small random writes that multiply with the consumers. One file per partition fixes the I/O pattern, but then old data cannot be deleted without rewriting the file, and reading from offset N becomes a scan.

Kafka writes each partition as a sequence of 1 GB segment files and appends only to the newest. Roughly every 4 KB of appended data it adds an 8-byte entry, a relative offset and a byte position, to the segment's offset index, so the index is at most 2 MB and stays memory-mapped. Finding an offset is a floor lookup among the segment base offsets, a binary search (#14) of at most 18 steps in that segment's index, and a short scan:

```text
orders-0/
  00000000000000000000.log  .index  .timeindex   offsets 0 … 1,048,575
  00000000000001048576.log  .index  .timeindex   offsets 1,048,576 … 2,097,151
  00000000000002097152.log  .index  .timeindex   active: appends go here
fetch offset 1,500,000
  → newest segment whose base offset ≤ 1,500,000:  00000000000001048576
  → binary search its .index (≤ 2 MB) for relative offset 451,424
  → step over a few batch headers to the batch holding it, then sendfile()
```

Speed comes from work avoided. The broker writes into the page cache and leaves flushing to the kernel, relying on replicas rather than fsync for durability, so consumers that keep up read from memory. Batches stay compressed from producer to disk to consumer, so the bytes on disk are the bytes a fetch returns, and sendfile copies them from the page cache to the socket without passing through the JVM. The cost is flexibility: the broker cannot filter records per consumer, TLS gives up zero-copy because it encrypts in user space, and one consumer replaying cold data pollutes the page cache for everyone.

Retention deletes whole segments, oldest first, once a segment's newest record is older than `retention.ms` or the partition exceeds `retention.bytes`. A partition is thus a circular queue (#110) on disk: the head advances with each append, the tail a segment at a time, and a consumer that lags past retention falls off the tail and resets as `auto.offset.reset` says. Compaction keeps the newest record per key instead. A cleaner loads the dirty part of the log into a fixed-size open-addressing hash table (#101) of 24-byte entries, a 16-byte MD5 of the key and an 8-byte offset, then recopies closed segments, dropping records that a later one with the same key supersedes. A tombstone, a null-valued record, deletes its key and is itself dropped after `delete.retention.ms`, a day by default. Offsets never change, so a compacted log has gaps.

#### Replication: in-sync replicas and the high watermark

Asynchronous replication, acknowledging after the leader's local write, loses acknowledged records whenever a leader dies before its followers catch up, which is the risk acks=1 takes. Waiting for every replica lets one slow machine stall the partition. A majority quorum, as in Raft or the quorums of Chapter 3, ignores the slowest replica but needs 2f + 1 copies to survive f failures: five copies of 605 TB to survive two.

Kafka keeps a dynamic set of in-sync replicas (ISR): the leader and the followers that have caught up to its log end within the last 30 seconds (`replica.lag.time.max.ms`). Followers pull with Fetch, which tells the leader how far each has got, and the high watermark is the smallest log end in the ISR. Records below it are committed, and consumers read only below it, so no consumer ever sees a record that a failover could take back:

```text
offset    0   1   2   3   4   5   6   7
broker 1  ●   ●   ●   ●   ●   ●   ●   ●   leader     log end 8
broker 2  ●   ●   ●   ●   ●   ●           follower   log end 6
broker 3  ●   ●   ●   ●   ●               follower   log end 5
                              ▲ high watermark 5 = lowest log end in the ISR
consumers read offsets 0 to 4; a batch at offset 7 sent with acks=all is
acknowledged once both followers have fetched past it
```

A lagging follower is dropped from the ISR rather than stalling writes, and rejoins once caught up. The leader changes the ISR only through the controller, whose metadata log is authoritative, and the controller elects new leaders only from the ISR, which holds every committed record. So f + 1 replicas survive f failures, and consensus is paid once, in the controller, not on every write. Producers choose what to wait for: acks=0 for nothing, acks=1 for the leader, acks=all for the whole ISR. Since the ISR can shrink to the leader alone, acks=all comes with `min.insync.replicas` = 2: writes continue with one of three brokers down, and below two in-sync replicas the leader refuses them with NOT_ENOUGH_REPLICAS.

Failover can leave the old leader holding records the rest of the ISR never received. Every batch carries the leader epoch it was written under, and a returning replica asks the leader where its last epoch ended and truncates the rest, so replicas never diverge. If the whole ISR is lost, the partition waits offline; unclean leader election, off by default, would promote a stale replica and give up committed records. The price is latency: acks=all waits for the slowest in-sync follower, and a sick but live one can stretch writes for up to 30 seconds before it is dropped.

#### Delivery guarantees: from at-least-once to exactly-once

A consumer's guarantee is set by when it commits. Committing before processing gives at-most-once, since a crash loses the records in between, and committing after gives at-least-once, since a crash replays them. Producers add duplicates when a write whose acknowledgement was lost is retried. Remembering every record id at the consumer would take unbounded state, so the log removes duplicates where they are made.

An idempotent producer gets a producer id and numbers its batches per partition. The leader remembers each producer's last five batches on each partition, acknowledges a repeat without writing it and rejects a gap with OUT_OF_ORDER_SEQUENCE_NUMBER; followers rebuild the same table from the batch headers, so a new leader still recognises a retry. Five is also the cap on requests in flight, which is how order survives retries, and current Kafka producers turn idempotence on by default.

A consume-transform-produce job must also commit its output and its input offsets together. A producer with a `transactional.id` finds its transaction coordinator, the leader of the `__transaction_state` partition the id hashes to, and InitProducerId bumps its epoch, fencing any zombie still using the old one. The coordinator records each partition the transaction touches, and the consumed offsets go to the group coordinator inside the same transaction. To commit, the coordinator logs a prepare record, writes a commit marker into every partition involved and then logs completion: a two-phase commit whose decision is durable once the prepare record is. Consumers set to read_committed read only up to the last stable offset, the start of the oldest open transaction, and skip aborted records.

Each transaction costs coordinator round trips and marker writes, so jobs commit every 100 ms or so rather than per record, and read_committed consumers see output that much later; a producer that hangs mid-transaction holds the last stable offset back until it times out. The guarantee also ends at Kafka's edge. An external database needs an idempotent write keyed by (topic, partition, offset), or the offset stored in the same database transaction, which is where Chapter 28 picks up.

### Scaling and Bottlenecks

The partition is the unit of scale, and its count is the decision hardest to undo: a topic's throughput and its consumers' parallelism are both capped by it, hence 64 partitions for the hot topic where 40 suffice today. Keys map to partitions by a murmur2 hash modulo the count, not by consistent hashing (#139), because Kafka puts the indirection one level down: partitions are fixed shards, like the fixed virtual nodes of a consistent-hashing ring, placed on brokers explicitly by the controller. Adding brokers moves whole partitions without changing any key's partition; adding partitions remaps many keys and breaks per-key order across the change, so partitions are sized for years and never removed. New brokers take load only when replicas are reassigned to them, a throttled copy that Cruise Control automates.

What breaks first is rarely the network. A consumer replaying last week reads cold segments, evicts the hot tail from the page cache and slows the tailing readers on the same brokers; quotas, fetching from a follower in the consumer's own zone and tiered storage contain it. A skewed key overloads one partition however many there are, and salting the key spreads it at the price of that key's order. Tiered storage is also the storage lever: keeping 12 hours locally cuts each broker's log from 30 TB to about 2 TB, so a lost broker refills in about an hour, and long retention moves to the object store of Chapter 33. Across regions, MirrorMaker 2 copies topics asynchronously and translates consumer offsets, which differ between clusters.

### Failure Modes

When a broker crashes, the controller fences it after its session timeout (9 seconds by default under KRaft), elects new leaders from the ISRs and bumps their epochs. Clients' requests fail, so they refresh metadata and retry; idempotence keeps producer retries safe, and consumers resume at the same offset, since the new leader holds everything below the high watermark. A returning broker truncates by leader epoch, catches up and rejoins the ISRs. One that never returns stays a missing replica until its partitions are reassigned: unlike the file system of Chapter 37, Kafka does not re-replicate on its own, and the 17-hour rebuild is that copy.

A leader cut off by a network partition can still take acks=1 writes that are later lost, but it cannot complete acks=all writes, since its followers have moved to the new leader and the controller rejects an ISR change from a stale epoch. A controller failure pauses only metadata changes, for the seconds the quorum takes to elect a new active controller. Because acknowledgements come from the page cache, a power cut that hits every replica at once can lose recent writes, so rack awareness places the three replicas in three zones.

A crashed consumer's partitions move to the survivors, which reprocess from the last commit. One stuck for longer than `max.poll.interval.ms`, five minutes by default, is evicted, and its late commits are rejected for carrying an old generation. A poison record is parked in a dead-letter topic after a few attempts instead of stalling its partition. Rolling restarts used to trigger stop-the-world rebalances; static membership lets a quickly restarted member keep its partitions, and cooperative rebalancing and the broker-driven protocol made generally available in Kafka 4.0 move only the partitions that must move.

### Trade-offs and Alternatives

The central trade is the ISR against a majority quorum: f + 1 copies instead of 2f + 1, paid for in tail latency and a dependence on the controller. Raft-per-partition systems such as Redpanda commit on a majority and never wait for stragglers, at 2f + 1 copies. A log is also not a queue. SQS and classic RabbitMQ queues acknowledge and redeliver individual messages and let any number of consumers share one queue, but they cannot replay history or feed many groups from one copy. Independent tasks belong on a queue, and Kafka's share groups (KIP-932) are bringing queue-style consumption into Kafka.

Ordering is a dial. One partition gives a total order at the throughput of one leader and one consumer; otherwise a consumer merges partitions by timestamp, a k-way merge (#20) that Kafka Streams runs inside each task with a priority queue of its input partitions keyed by head-record timestamp, and the result is only as good as the producers' clocks. Storage is the last dial. Pulsar separates stateless brokers from BookKeeper storage nodes so each scales alone, and object-storage-native designs such as WarpStream write straight to object storage, trading latency for no local disks and no cross-zone replication traffic.

### What Interviewers Probe

Expect six questions. How is order kept? Only within a partition: one key always maps to one partition, and idempotence preserves order across retries. What does acks=all promise? That every current in-sync replica has the record, which is why it comes with `min.insync.replicas` = 2. What happens when a leader dies? An ISR member, which has every committed record, takes over; consumers never saw past the high watermark, and producers retry idempotently. Why is it fast? Sequential appends of compressed batches, the page cache, sendfile and no per-message state. How many partitions? Peak throughput over one consumer's capacity, rounded up because adding partitions moves keys. Is exactly-once real? Inside Kafka, through idempotence, transactions and read_committed consumers; at the edges, only with idempotent sinks.

Strong candidates raise the rest unprompted: the high watermark as the line between written and committed, what the ISR gives up for cheaper durability, rebalance storms, hot keys, lag racing retention, and acknowledgement without fsync. Interviewers care less about configuration names than about whether the candidate can say which replicas hold an acknowledged record at every moment.

*Algorithms:* #110 Circular Queue · #14 Binary Search · #139 Consistent Hashing · #101 Hash Map with Open Addressing · #20 Merge K Sorted Arrays
