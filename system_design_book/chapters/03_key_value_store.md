---
rank: 3
slug: key_value_store
---

A distributed key-value store keeps an enormous number of small values, each addressed by a key, on hundreds of machines that fail as a matter of routine. A service calls `put("cart:8412", bytes)` and later `get("cart:8412")`, and the store answers in milliseconds even while a disk is dying or a link between zones is down. Amazon built Dynamo so that a shopping cart would take an item under exactly those conditions, and Cassandra and Riak adopted its design. Three questions decide it: how to spread keys so that adding a machine moves little data, how many replicas must answer before a request returns, and how replicas that missed writes, or accepted conflicting ones, come back into agreement.

### Requirements

A client creates a table, then puts, gets and deletes values by key. Keys are at most 1 KB and values at most 1 MB, with most records near 1 KB; larger objects belong in an object store (Chapter 33). Each request names a consistency level, ONE, QUORUM or ALL, trading speed against seeing the latest write, and each table declares how concurrent writes are settled: last-write-wins, or siblings that the application merges.

Assume 100 billion keys and, at peak, a million reads and half a million writes a second, each answered within 10 ms at the 99th percentile. Writes must be accepted while nodes are down and while the network is partitioned, because a rejected write is lost business and a briefly stale read is usually harmless. A write acknowledged at QUORUM survives the loss of any one machine or zone, and replicas that diverge converge without an operator. Range scans, secondary indexes, multi-key transactions and compare-and-set are out of scope; the last needs the consensus designs contrasted at the end.

### Estimates

```text
data         assume 10^11 keys × ~1 KB (key, value, version)  = 100 TB
replicas     × 3, one replica per zone                         = 300 TB
nodes        300 TB / ~1 TB of data per node (on 2 TB SSDs)   = 300 nodes
traffic      assume 1 M reads/s and 500,000 writes/s at peak
reads/node   1 M/s × 3 replicas asked / 300 nodes              = 10,000/s
writes/node  500,000/s × 3 replicas / 300 nodes                = 5,000/s
Bloom        10^9 keys per node × 10 bits                      = 1.25 GB, ~1% FP
outages      each node down ~1 day a year: 300 / 365           ≈ 1 down at once
hints        1 h outage: 5,000 writes/s × 3,600 s = 18 M writes ≈ 18 GB
rebuild      1 TB from one peer at 100 MB/s                    ≈ 2.8 hours
             1 TB from 100 peers in parallel, 10 GB each       ≈ 2 minutes
```

Storage, not traffic, sizes this cluster. Each node serves 10,000 replica reads and 5,000 replica writes a second, a light load for SSDs that leaves headroom for a failed neighbour's share, for compaction and for repair. Capping a node at a terabyte is deliberate: a dead node rebuilt by one neighbour takes hours, and by a hundred peers minutes, which is the case for virtual nodes. Bloom filters for every file fit in memory. And with 300 machines one is down at almost any moment, so the failure path is the normal path: an hour's outage leaves 18 GB of missed writes for the other nodes to hold.

### API

```text
CreateTable(name, n = 3, conflicts = LWW | SIBLINGS)

Get(table, key, consistency = ONE | QUORUM | ALL)
    OK                 {versions: [{value, clock}], context}   1 or more
    NOT_FOUND          no live version (a tombstone counts as none)
    UNAVAILABLE        fewer than R replicas reachable

Put(table, key, value, context, consistency)
    OK                 at least W replicas acknowledged
    UNAVAILABLE        fewer than W nodes alive: nothing was sent
    DEADLINE_EXCEEDED  sent, but fewer than W acks in time: it may still land
    INVALID_ARGUMENT   key over 1 KB or value over 1 MB

Delete(table, key, context, consistency)    writes a tombstone; same codes
```

The interface is Dynamo's. A get returns every version the store cannot order, plus an opaque context holding their clocks, and the next put passes the context back so the store knows which versions the new value replaces. The two write errors must be handled differently. UNAVAILABLE is clean: the coordinator knew too few nodes were alive and sent nothing. DEADLINE_EXCEEDED is not: the write reached some replicas, is never rolled back and may surface later through read repair or hinted handoff. That is why a put carries a whole value rather than an increment: a retried put is harmless, a retried increment double-counts. Services authenticate with mutual TLS and are authorised per table.

### Data Model

```text
table        name | n = 3 | default R and W | conflicts: LWW or SIBLINGS
record       key → [(value or tombstone, version)]
             version = timestamp (LWW) or vector clock [(node, counter)]
ring         token = 64-bit hash(key); each node owns 256 random tokens
             preference list(k) = first 3 distinct nodes clockwise of
             token(k), one per zone, then fallback nodes further round
node store   commit log → memtable (sorted, in RAM) → SSTables (immutable)
             SSTable = sorted data blocks + block index + Bloom filter
hints        (intended node, key, value, version), kept by the stand-in
merkle       one hash tree per key range the node replicates
membership   node, tokens, zone, heartbeat, status; gossiped to every node
```

Every request is a lookup by key, so the key is hashed to a 64-bit token and the ring, not an index, says where it lives. Each machine owns 256 tokens, its virtual nodes, and a key belongs to the first three distinct machines clockwise from its token, one in each zone. The ring is metadata, about 2 MB for 76,800 tokens; every node keeps a copy that gossip keeps current, so any node or token-aware client computes a preference list locally and no directory sits on the request path. A record is a list of versions: one timestamped entry under last-write-wins, or every version that no other version's vector clock supersedes under siblings. Records live in a log-structured merge tree, because the workload is write-heavy and a put never reads the old value. Hints and Merkle trees live beside the data on each node, one tree per key range.

### Architecture

```dot
rankdir=TB;
client [label="client service\ntoken-aware driver", class=client];
ring   [label="ring view\n(gossiped)", class=cache];
a [label="replica A\ncoordinator", class=store];
subgraph cluster_eng {
  label="storage engine on every node"; style="rounded,dashed"; color="#9CA3AF";
  log  [label="commit log", class=store];
  mem  [label="memtable", class=cache];
  sst  [label="SSTables\n+ Bloom filters", class=store];
  comp [label="compaction\nk-way merge", class=worker];
}
b [label="replica B", class=store];
c [label="replica C\n(down)", class=store];
d [label="node D\nstand-in", class=store];
repair [label="anti-entropy\nMerkle trees", class=worker];
client -> a [label=" put / get"];
ring -> client [style=dashed, label=" token map"];
ring -> a [style=dashed, label=" who is up"];
a -> log [label=" 1. append"];
a -> mem [label=" 2. insert"];
a -> b [label=" forward"];
a -> c [style=dotted, label=" timeout"];
a -> d [label=" write\n + hint"];
c -> d [dir=back, style=dashed, label=" hand off"];
mem -> sst [label=" flush"];
comp -> sst [dir=both, label=" merge"];
b -> repair [dir=back, style=dashed, label=" compare"];
c -> repair [dir=back, style=dashed];
{rank=same; ring; client}
{rank=same; log; mem; b; c; d}
{rank=same; sst; comp; repair}
```

The write path starts in the client service, whose driver holds the token map and sends a put straight to the key's first healthy replica, A, which coordinates it. Only a replica may coordinate a write, because in a sibling table the coordinator adds its own entry to the vector clock. A takes the preference list and every node's liveness from its ring view, appends the record to its commit log, inserts it into its memtable and forwards it to B and C in parallel; with W = 2 it answers OK once one of them acknowledges. C is down and never answers, so its copy goes to node D, the next healthy node on the ring, with a hint naming C, and D hands the write off when C returns.

A get makes the same journey. A reads its own copy, asks B and C (or D in C's place) for theirs and, once R = 2 answers are in, returns the version that supersedes the others, or all of them as siblings if they are concurrent; a replica that answered with an older version is then sent the newest, which is read repair. Within each node a read checks the memtable and only the SSTables whose Bloom filters admit the key, while flushes turn full memtables into new SSTables and compaction merges SSTables into fewer, larger ones.

Two background processes keep the cluster honest. Each node gossips its ring view and heartbeats with a random peer every second, so news of a failure reaches all 300 nodes within seconds, and each node's failure detector decides locally whom to stop waiting for. The anti-entropy job compares the Merkle trees of ranges that two replicas share, here B and C once C is back, and copies only the keys that differ.

### Deep Dives

#### Quorums, sloppy quorums and hinted handoff

The naive settings sit at the extremes. Writing synchronously to all three replicas makes every write visible to every read, but each write waits for the slowest replica and fails when any one is down, so with a node down at almost every moment some range is always refusing writes. Writing to one replica and copying in the background is fast and always available, but a read elsewhere misses the write, and a crash before the copy loses a write already acknowledged.

Quorums sit between. A write succeeds when W of the N replicas acknowledge and a read when R answer, and if R + W > N every read set shares a replica with every write set, so a read sees the newest acknowledged version. Dynamo's common setting, N = 3 with R = W = 2, survives one lost replica on both paths; W = 3 with R = 1 makes reads cheap and writes fragile, W = 1 with R = 3 does the reverse, and R = W = 1 promises only eventual convergence. Waiting for the fastest W of N also trims the tail, since one replica stuck in a garbage-collection pause slows nothing. Quorums are still not linearizable: a write that reached one replica and timed out can be seen by one read and missed by the next, and under last-write-wins the newest version is simply the largest timestamp, which clock skew can get wrong.

Strict quorums still refuse writes when a partition cuts the coordinator off from the other two replicas. Dynamo's sloppy quorum sends reads and writes to the first N healthy nodes of the preference list instead: with B and C unreachable, the write lands on A and on the next nodes round the ring, which keep it in their hint stores until the partition heals. The cost is the overlap. Until the hints arrive, a read answered by B and C misses the write, R + W > N notwithstanding. Cassandra declines that trade: its hints never count towards the consistency level except at the weakest level, ANY, so its quorums refuse writes rather than give up the overlap.

Hints are best effort: a stand-in can die before delivering them, and a node down longer than the hint window, three hours by default in Cassandra, gets none. Anti-entropy closes the gap without comparing a terabyte key by key. Each replica keeps a Merkle tree per key range whose leaves hash small sub-ranges and whose parents hash their children; two replicas compare roots and descend only where the hashes differ. A range here holds about 1.3 million keys, so a tree of 2^15 leaves finds one stale key in fifteen levels of comparisons and ships one leaf of about forty keys. Building a tree reads the whole range, so repair runs throttled, and the trees must be rebuilt whenever ranges move.

#### Concurrent writes: vector clocks or last-write-wins

Two clients can update one key at the same moment through different coordinators, or on the two sides of a partition, and both writes succeed; that is what always writable means. Last-write-wins settles it by timestamp: every replica keeps the version with the largest, and the losing write vanishes silently. The clocks decide who lost, so a coordinator whose clock runs two seconds fast beats every write made elsewhere in the next two seconds. For single-writer data, immutable values and caches that loss never happens or never matters, and Cassandra resolves every cell this way.

Vector clocks keep both. A clock is a list of (node, counter) pairs; a coordinator increments its own counter on each write, and version X supersedes version Y when every counter in X is at least the matching one in Y. When neither supersedes the other, the store keeps both as siblings and returns both, and the client puts back a merge whose clock supersedes them.

```text
put via A                  D1  [A:1]
put via A, context D1      D2  [A:2]              supersedes D1
put via B, context D2      D3  [A:2, B:1]   ┐ neither supersedes
put via C, context D2      D4  [A:2, C:1]   ┘ the other: siblings
get → D3, D4; client merges; put via A, context D3 + D4
                           D5  [A:3, B:1, C:1]    supersedes D3 and D4
```

The merge is where the design leaks into the application. Dynamo's shopping cart takes the union of its siblings, so an added item is never lost, but a deleted one can reappear. Clocks grow with every coordinator, so Dynamo dropped the oldest pair once a clock reached about ten, accepting an occasional false conflict. CRDTs, counters and sets whose merge is built in, remove the application's merge step; Riak added them, and Chapter 11 meets them again. Hence the per-table choice: last-write-wins for profiles and sessions, siblings for carts and anything that users edit from several devices at once.

#### The storage engine: commit log, memtable and SSTables

Each node absorbs 5,000 writes a second, indefinitely. A B-tree updates pages in place, so puts to random keys become random page writes, each rewriting a whole page to change one record. An append-only log with an in-memory hash index, the design of Bitcask, Riak's default backend, writes sequentially but must hold all billion keys of a node in RAM.

A log-structured merge tree writes sequentially without that index: a put is appended to the commit log for durability and inserted into the memtable, a sorted in-memory structure such as a skip list. A full memtable is written out as an SSTable, an immutable file of key-sorted blocks with a block index and a Bloom filter, and the log it covered is discarded. A get checks the memtable, then the SSTables: each file's Bloom filter (#146), at 10 bits per key, rules out about 99 percent of the files that lack the key, and in a file that may hold it, a binary search (#14) of the block index finds the one block to read. A key can have versions in the memtable and in several SSTables, and the read reconciles them by version rather than by file age, because a hint or a repair can deliver an old version late. Each entry also carries a local sequence number, so a scan pinned to a snapshot sees only entries written at or before it, the lookup of the time-based key-value store (#92); that gives the repair job a range that holds still while writes continue.

Compaction stops the files from piling up. It streams several sorted SSTables through a min-heap, a k-way merge (#20), keeps each key's winning version and writes one new file in a single sequential pass. A delete writes a tombstone instead of removing anything, since older files and replicas that missed the delete still hold the value; compaction may purge the tombstone only after a grace period, ten days by default in Cassandra, within which repair must carry it to every replica, or the value comes back. The price is amplification: compaction rewrites each byte several times, a read may touch several files, and dead versions occupy space until merged. Size-tiered compaction favours writes but needs free space equal to a merge's inputs; leveled compaction keeps each level's files disjoint, so a read touches about one file per level, at the cost of more rewriting. Hence 2 TB of disk for 1 TB of data.

### Scaling and Bottlenecks

Virtual nodes earn their place when the cluster changes. With one random token per machine, the busiest of 300 owns about six times the average share and a new machine relieves only its neighbour; with 256 tokens the busiest owns about a fifth more than average, and new and dead machines alike exchange thin slices with hundreds of peers at once. Consistent hashing (#139) bounds the movement: the 301st machine takes about a 301st of the data, where hashing modulo the node count would move nearly all of it. The cost is that almost any two failures in different zones now share some range, leaving its keys below quorum. Cassandra's documentation warns that more tokens decrease availability, and version 4.0 cut the default from 256 tokens to 16, placed by a balancing allocator.

Compaction and repair compete with client reads for every disk, so both run throttled; a growing compaction backlog is the first sign of a node falling behind. A hot key lives on three machines however big the cluster grows, so it needs a cache in front (Chapter 4), reads at ONE across its replicas, or splitting in the application. Every node gossips the full membership, which Dynamo's authors found works for a few hundred nodes but is not trivial to scale to tens of thousands. Across regions, the preference list places replicas in every region, a local quorum (Cassandra's LOCAL_QUORUM) keeps latency inside one, and remote replicas catch up asynchronously.

### Failure Modes

A single failed node is routine: quorums of two carry on, drivers route around it, and its 18 GB an hour of hints replay, throttled, when it returns. A node down past the hint window stays stale until repair runs. A node gone for good is removed by an operator, and its ranges re-replicate many-to-many in minutes. Removal is manual, as in Dynamo, because a silent node may only be rebooting or paused, and treating that as a departure would shuffle a terabyte for nothing.

For the same reason the failure detector suspects rather than convicts. An accrual detector, the phi detector in Cassandra, raises suspicion as silence grows relative to a peer's usual heartbeat rhythm instead of applying a fixed timeout, and a false suspicion costs a few hints, never data. A partition lets both sides accept writes; when it heals, hints flow and siblings appear, while last-write-wins tables silently keep only the later-stamped side, so their nodes alarm on clock drift to keep "later" meaningful.

A crash loses the memtable, which the commit log replays on restart. Cassandra by default acknowledges before syncing and syncs the log every ten seconds, relying for those seconds on replicas in other zones, which rarely lose power together. And deleted values return as zombies whenever repair falls behind the tombstone grace period.

### Trade-offs and Alternatives

The real alternative is a leader-based store: shard the key space and replicate each shard with Raft, as CockroachDB and TiKV do, or with Paxos, as Spanner does (Chapter 38). A shard's leader appends writes to a replicated log and commits once a majority holds them, and a leader holding a lease serves linearizable reads. Nothing conflicts, so vector clocks, siblings and read repair disappear and compare-and-set becomes easy. The price mirrors Dynamo's strengths: writes funnel through one machine per shard, a shard refuses writes while it elects a new leader, and the minority side of a partition cannot write at all. Amazon's DynamoDB service, despite its name, is built this way: each partition is a Multi-Paxos group whose leader takes every write and every strongly consistent read.

Choose by the requirement that hurts most. Carts, sessions and sensor streams, whose writes must never be refused, pick the leaderless design; anything that needs one winner, a ledger (Chapter 24) or a lock (Chapter 39), picks consensus. Within either design, range partitioning, as in Bigtable and HBase, restores scans at the price of hot ranges that must be split, and a B-tree gives read-mostly workloads steadier reads than an LSM tree.

### What Interviewers Probe

Expect six questions. Why does R + W > N work? Every read set overlaps every write set; then add that sloppy quorums, partial writes and clock skew break it. Which N, R and W? Three replicas in three zones with R = W = 2, and what W = 1 or R = 1 would trade. What if a replica is down during a write? A sloppy quorum and a hint, handoff on recovery, Merkle-tree repair behind both. How are concurrent writes resolved? Siblings when the application can merge, last-write-wins when loss is acceptable, CRDTs when the data type allows. Why virtual nodes? Even load and parallel rebuilds. How does a get find a key on disk, and what does a delete do? Memtable, Bloom filters, block index and one block read; a tombstone that must outlive repair.

Strong candidates raise four points unprompted: tail latency, hidden by waiting for the fastest W of N; the difference between UNAVAILABLE and a timeout whose write may still land; the hot key that consistent hashing cannot spread; and the leader-based alternative, with the requirement that would make them switch. The best answers end where the requirements began: the store is always writable because it is willing to return conflicts, and every mechanism in it exists to make that bargain safe.

*Algorithms:* #139 Consistent Hashing · #146 Bloom Filter · #20 Merge K Sorted Arrays · #92 Time-Based Key-Value Store · #14 Binary Search
