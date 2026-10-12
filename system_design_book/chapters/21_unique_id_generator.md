---
rank: 21
slug: unique_id_generator
---

Every message, order, photo and log line needs a key before it is written, and once the data lives on hundreds of shards, no single database's auto-increment can hand those keys out. A unique ID generator mints them, a million a second, without its machines ever consulting each other. A call returns `103061599543693317`, a 64-bit number that no other caller will ever receive, and its bits say it was minted at 09:30:00.123 UTC on 12 October 2026 by node 17 in region 1. Three questions decide the design: how to divide 64 bits between time, machine and sequence, how to give every generator a machine number that no other generator holds, and what to do when a clock runs backwards.

### Requirements

A calling service asks for one id or a batch and receives 64-bit integers that are unique across every region, forever. Ids grow with time, strictly from any one generator and roughly across generators: ids minted more than 100 ms apart, anywhere, sort in the order they were created. Any id decodes into its creation time, region and node without a lookup, so ids help with debugging and time-range queries and serve as pagination cursors.

Assume a peak of one million ids a second across three regions. A call must return within a millisecond at the 99th percentile, and the generator must be more available than any database that uses its ids, because every insert waits on it; that rules out a consensus round or a cross-region call per id. Uniqueness is absolute, since a duplicate key silently merges two records, which is worse than an outage. Ids fit a signed 64-bit integer, so they work as `BIGINT` keys and Java `long` values, and the scheme must last decades. Out of scope are gapless numbering such as invoice numbers, unguessable tokens, which need a cryptographic random generator, short human-readable codes (Chapter 1), and an exact global order of commits, which is the job of Spanner's TrueTime (Chapter 38).

### Estimates

```text
demand    20 B new objects/day / 86,400 s ≈ 230,000 ids/s
          peak ×4 ≈ 0.93 M, call it 1 M ids/s
time      41 bits of ms: 2^41 ms ≈ 2.2 × 10^12 ms ≈ 69.7 years
          epoch 2026-01-01 → lasts to Sept 2095; epoch 1970 → only to 2039
sequence  12 bits: 4,096 ids per ms per node → 4.1 M ids/s per node
nodes     10 bits = 3 region bits (8 regions) + 7 node bits (128 per region)
ceiling   1,024 nodes × 4.1 M/s ≈ 4.2 × 10^9 ids/s, ~4,500 × the peak
fleet     assume ~100 k calls/s per node: 1 M calls/s needs 10 nodes
          run 8 per region × 3 regions = 24; any two regions: 1.6 M/s
per node  1 M/s / 16 nodes (one region down) ≈ 63 ids/ms, 1.5% of 4,096
keys      20 B × 365 = 7.3 T keys/year × 8 B saved (64 vs 128 bits)
          ≈ 58 TB a year in every index that stores the key
JSON      2^53 / 2^22 = 2^31 ms ≈ 25 days: after that, every id > 2^53
```

One node could mint four million ids a second, so what limits a node is the cost of a call, not the sequence field, and batching answers that. The scarce resource is node numbers: a region's 128 are plenty for a dedicated fleet of eight and hopeless if each of tens of thousands of application processes ran its own generator, which is the main reason this design is a small service. Keeping ids at 64 bits saves tens of terabytes a year in every index, and counting from the service's launch instead of from 1970 buys 69 years instead of 13. The last line is an API constraint: twenty-five days after the epoch, every id is too large for a JavaScript number, which is exact only up to 2^53.

### API

```text
rpc NextIds(NextIdsRequest) returns (IdRange)  in-region, mTLS, 2 ms deadline
    NextIdsRequest    {count: 1..4096}
    IdRange           {first: 103061599543693317, count: 64}
                      ids are first, first+1, ..., first+count-1; count may
                      be less than asked: what is left of this millisecond
    INVALID_ARGUMENT  count outside 1..4096
    UNAVAILABLE       clock behind the last id issued, or reservation lapsed
                      → the client library retries on another id node

library  decode(id) → {time_ms, region, node, sequence}     local, no call
```

NextIds needs no idempotency key: a retry simply receives new ids, and the ids lost with a timed-out response leave gaps that harm no one. The response is a range because consecutive sequence numbers within one millisecond are consecutive integers, so 64 ids or 4,000 cost the same sixteen bytes; a request for more than the current millisecond has left gets the remainder and asks again. Calls are internal, authenticated with mutual TLS, and never leave the region, and decoding is a few shifts and masks done in the library. Services that expose ids in JSON send them as strings, which is why Twitter's API carries an `id_str` beside its numeric ids, and they use ids directly as cursors, as in `GET /messages?before=103061599543693317&limit=50`.

### Data Model

```text
id layout, a versioned constant (bit 63 is the most significant)
  bit  63       sign, always 0     every id is a positive BIGINT
  bits 62..22   ms since epoch     41 bits; epoch 2026-01-01T00:00:00Z
  bits 21..19   region             3 bits; static, from region config
  bits 18..12   node               7 bits; leased from the region's ZooKeeper
  bits 11..0    sequence           12 bits; restarts at 0 each millisecond

ZooKeeper, one ensemble per region
  /idgen/config                 epoch, layout version, region number
  /idgen/nodes/017/owner        ephemeral: host, process id, start time
  /idgen/nodes/017/reserved     reserved_until_ms, advanced by conditional set

id node memory    node | last_ms | sequence | reserved_until_ms
issued ids        never stored anywhere
```

What this model lacks is the point. There is no table of issued ids and no write per id anywhere, because uniqueness is a property of the layout, not of a lookup, and that is why the generator scales without a storage tier. The only shared state says which node holds which number and how far ahead in time its claim reaches: a few hundred small records per region, written every few minutes, that must be linearizable, because two nodes must never both believe they own number 17. That is what a consensus-backed coordination store such as ZooKeeper or etcd provides (Chapter 39), and a relational table updated with compare-and-set would serve as well. Each region keeps its own ensemble, since the region bits already separate the regions' ids, and region numbers are static configuration.

### Architecture

```dot
rankdir=LR;
compound=true;
subgraph cluster_r1 {
  label="region 1"; style="rounded,dashed"; color="#9CA3AF";
  posts [label="post service\n+ id client library", class=client];
  msgs  [label="message service\n+ id client library", class=client];
  subgraph cluster_ids1 {
    label="id nodes"; style="rounded"; color="#9CA3AF";
    n17 [label="id node 17"];
    n18 [label="id node 18"];
    n23 [label="id node 23"];
  }
  zk1   [label="ZooKeeper\nowners, reservations", class=store];
  table [label="posts table\nkey = id", class=store];
}
subgraph cluster_r2 {
  label="region 2"; style="rounded,dashed"; color="#9CA3AF";
  chat [label="chat service\n+ id client library", class=client];
  m04  [label="id node 4"];
  zk2  [label="ZooKeeper", class=store];
}
ntp   [label="NTP servers\nslew only, leap smear", class=external];
mon   [label="clock-offset\nmonitor", class=worker];
posts -> n17 [label=" NextIds(1)"];
posts -> n18 [label=" retry on\n UNAVAILABLE"];
msgs  -> n23 [label=" NextIds(64)"];
posts -> table [label=" insert row"];
n18 -> zk1 [ltail=cluster_ids1, label=" claim, renew"];
chat -> m04 [label=" NextIds"];
m04 -> zk2 [label=" claim, renew"];
ntp -> n18 [lhead=cluster_ids1, label=" time"];
ntp -> m04 [label=" time"];
n23 -> mon [ltail=cluster_ids1, style=dashed, label=" offsets"];
m04 -> mon [style=dashed, label=" offsets"];
```

The issue path never leaves the region and never touches a disk. When the post service needs a key, its id client library picks one of the region's id nodes and sends NextIds. The node reads its clock, compares it with the last millisecond it used, advances the sequence in memory and returns a range, and the post service inserts its row into the posts table with that id as the key. If the node answers UNAVAILABLE or misses the deadline, the library asks another id node; ids from different nodes differ in their node bits, so a retry can never produce a duplicate. The message service fetches 64 ids at a time and hands them out over the next few milliseconds.

The lease path runs at startup and then every five minutes: an id node claims a free node number in the region's ZooKeeper ensemble and reserves time ahead, for reasons the second deep dive explains. On the time path, every id node disciplines its clock against the NTP servers, which never step a running clock and which smear leap seconds, and reports its measured offset to the clock-offset monitor, which alerts on any node drifting away from its peers. Region 2 runs the same stack with its own region number and its own ensemble, so its chat service mints ids that can never collide with region 1's, with no traffic between the regions at all.

### Deep Dives

#### Choosing a scheme, then spending 64 bits

The obvious generator is the database's own auto-increment column, and its single primary is the problem: it caps the company's insert rate, it is a single point of failure, and its numbers leak volume, the German tank problem in miniature. Flickr's ticket servers split the work between two MySQL servers set to `auto_increment_increment = 2`, one with offset 1 and the other with offset 2, each id costing a `REPLACE INTO` a one-row table and a `SELECT LAST_INSERT_ID()`. That is still a database write per id, the odd and even halves drift apart, and a third server means re-stepping all of them. Leasing ranges, as Chapter 1 does for short codes (#100), removes the write per id, but a server still counting through an old block issues small numbers long after another has started a newer one, so ids stop sorting by time. UUIDv4 needs no coordination at all, with 122 random bits and a 50% chance of a single duplicate only after 2.7 × 10^18 ids, but it is twice the size, and random keys scatter inserts across a B-tree, so the working set is the whole index rather than its right edge. UUIDv7 (RFC 9562) puts a 48-bit millisecond timestamp in front of 74 random bits, which restores time order but not the size.

Snowflake, built at Twitter in 2010 (#145), keeps time order in 64 bits by replacing randomness with structure.

```text
  63  62                              22   21  19   18  12   11       0
┌───┬────────────────────────────────────┬────────┬────────┬────────────┐
│ 0 │ ms since 2026-01-01                │ region │ node   │ sequence   │
│   │ 41 bits                            │ 3 bits │ 7 bits │ 12 bits    │
│   │ 24,571,800,123                     │ 1      │ 17     │ 5          │
└───┴────────────────────────────────────┴────────┴────────┴────────────┘
24,571,800,123 ms after the epoch = 2026-10-12 09:30:00.123 UTC
id = ms << 22 | region << 19 | node << 12 | sequence = 103061599543693317
```

The sign bit stays zero so ids are positive in signed types. Forty-one bits of milliseconds from a custom epoch make numeric order time order, ten bits name the generator so that two generators can never collide, and twelve bits count within a millisecond. Minting is a clock read, a comparison and an increment. In a new millisecond the sequence restarts at zero, and if it passes 4,095 the node waits for the next millisecond, which is the whole answer to sequence overflow. The costs are a 69-year lifetime, a dependence on clocks that the last deep dive confronts, and badly distributed low bits: at a few dozen ids per millisecond nearly every sequence number is small, so `id % 1024` sends almost every row to the first few dozen shards, and consumers hash an id before sharding by it. The split itself is a dial. Instagram mints ids inside PostgreSQL with 41 bits of time, 13 of logical shard and 10 of sequence, so every id names the shard that holds its row.

#### Leasing node numbers that never collide

The naive ways to number nodes fail silently. A number in each machine's configuration works until a copied file or a cloned virtual machine produces two node 17s, and nothing notices until two rows share a key. Deriving it from the host, as Sonyflake does by default with the low 16 bits of the private IP address, breaks when addresses are reused or outgrow the field. Random choice is worse than it sounds: eight nodes picking among 128 numbers collide one time in five.

This design leases numbers from ZooKeeper, which is how Snowflake chose its worker numbers at startup. A starting node creates the ephemeral znode `/idgen/nodes/017/owner`. Creation fails if the znode exists, so one live node owns each number, and the znode vanishes when its owner's session ends. That alone is not enough, because a node cut off from ZooKeeper keeps serving and learns that its session expired only when it reconnects, by which time a new owner may be minting with its number.

So each number also carries a persistent reservation, `reserved_until_ms`. The owner never issues an id stamped later than the reservation, and every five minutes it pushes the reservation an hour ahead with a conditional set that fails if anyone else has written the record. A node that claims a number reads the reservation first and issues nothing until its own clock has passed it. Successive owners of a number therefore mint from disjoint stretches of time, the old owner's ids stamped at or before the reservation and the new owner's after it, whatever their clocks say and even if the old owner never learns it was replaced. The new owner's first conditional write also makes the old owner's next renewal fail, which tells it to stop.

The cost is about five ZooKeeper writes a minute for the whole fleet, and none per id. A crashed node's number stays unusable for up to an hour, so a restarting node takes a number whose reservation has already passed, and a region with 128 numbers and eight nodes has plenty. If ZooKeeper itself goes down, running nodes keep minting for at least 55 minutes; only new nodes cannot start.

#### When the clock runs backwards

A generator that trusts the wall clock duplicates ids the first time the clock moves backwards. Stepped back 300 ms, a node re-enters milliseconds it has already used, restarts its sequence at zero and mints ids it has already handed out. That happens more often than people expect. By default ntpd steps a clock that is more than 128 ms off instead of slewing it, a leap second makes POSIX time repeat a second, a virtual machine resumed after a pause or a migration can find its clock badly wrong, and operators set clocks by hand. On 1 January 2017 a leap second made time run backwards inside Cloudflare's DNS servers, and code that computed a negative duration crashed.

The first defence is the guard Snowflake shipped with: remember the last millisecond used, and if the clock reads earlier, refuse to issue until it has caught up. This design grades the response by the size of the step. A few milliseconds are waited out inside the call. A larger step makes the node answer UNAVAILABLE, so clients move to another node until its clock catches up, and after a step of minutes the node gives up its number and claims one whose reservation its clock has already passed. Borrowing future milliseconds instead, by staying on the last millisecond and moving ahead whenever the sequence fills, keeps a node available but stamps ids ahead of real time, which suits an in-process library that has no other node to fail over to. The guard lives in memory and dies with the process; the reservation covers restarts, because it is at least as late as every id its number has issued.

The second defence keeps clocks from going backwards at all. The NTP daemon slews a running clock instead of stepping it, and ntpd changes the rate by at most half a millisecond per second, so a 100 ms error takes over three minutes to correct but time never turns back; it steps only at boot, before the generator starts. Leap seconds are smeared, the way Google's public NTP servers stretch one across 24 hours from noon to noon UTC. What remains is skew between nodes, and skew bounds the ordering promise: ids from one node strictly increase, but ids from two nodes are ordered only as well as their clocks agree, about a millisecond on a good local network. Snowflake promised k-sorting within a second and aimed for tens of milliseconds; this design promises 100 ms and usually achieves a few. Exact order across machines needs Spanner's TrueTime, which bounds the uncertainty and waits it out.

### Scaling and Bottlenecks

A node first runs out of calls, at around 100,000 a second, while its sequence could support forty times as many ids. Batching moves that limit, but the client library discards a cached range after ten milliseconds, because an id carries the time it was minted rather than the time it is used. Node numbers run out next, once the hottest callers embed the generator in process, as Chapter 5's tweet service does. The layout can then trade sequence bits for node bits, thirteen node bits and six sequence bits giving each region 8,192 generators of 64 ids per millisecond, and the switch is safe at an agreed future millisecond: ids stamped before it use the old split, ids stamped after it the new one, and ids with different timestamps cannot collide.

The real hazard sits downstream, in the stores that use ids as keys. In a B-tree on one machine, such as an InnoDB table or a PostgreSQL index, rising keys are ideal, because every insert lands on the rightmost page. In a range-partitioned store such as Bigtable, HBase or Spanner they are a hotspot, because every new row lands in the tablet holding the highest keys and one server takes the whole write load. Spanner's documentation warns against monotonically increasing keys and offers bit-reversed sequences for exactly this reason. Bit-reversing the id or prefixing a hash spreads the writes at the price of scans in id order, and stores that hash the partition key, such as Cassandra and DynamoDB, are unaffected.

### Failure Modes

A crashed id node loses nothing but unused sequence numbers: callers retry on another node within their deadline, and the restarted process claims a fresh number. If a region's ZooKeeper ensemble fails, running nodes keep minting for at least 55 minutes and only new nodes cannot start, so the outage is an alert rather than an incident unless it coincides with a large deploy. A node partitioned from ZooKeeper stops at its reservation, and its number cannot be reused before then, so a partition can delay ids but never duplicate them.

A clock that steps backwards takes one node out of rotation for the length of the step. A clock that leaps forward is worse: the node mints ids stamped in the future, which sort after ids not yet created, and once corrected it must wait out the jump or abandon its number. The NTP servers therefore draw on several upstream sources, so that a single bad one is outvoted. Each node refuses requests while its measured offset exceeds 40 ms, which, with the ten-millisecond limit on cached ranges, keeps the ordering error within the 100 ms of the requirements, and the clock-offset monitor alerts long before that. A failed region costs the others nothing, since they mint with their own region bits. The last line of defence is the consuming table's primary key: a duplicate-key error is treated as an incident, because by construction it cannot happen.

### Trade-offs and Alternatives

The central trade is where the generator runs. A service, as here, needs few node numbers and keeps the clocks that matter on a handful of carefully run machines, and it pays with a round trip on every insert and a dependency that must be more available than the databases it serves. A library inside each process, as in Chapter 5, removes the hop and the dependency, and it pays with a node number per process and trustworthy clocks on every host; the hottest callers justify that price.

UUIDv7 is the right answer whenever 128 bits are affordable: it needs no infrastructure at all, so even a phone that is offline can mint ids that will never collide. Ticket servers or leased ranges fit when ids must be short and dense and time order does not matter, as with the codes of Chapter 1. A single database sequence is the simplest choice below a few thousand inserts a second, though not even it is gapless: a PostgreSQL sequence never rolls back, so aborted transactions leave holes, and truly gapless numbering needs a counter row updated inside every inserting transaction, which serializes them all. Twitter considered ZooKeeper sequential nodes before building Snowflake and rejected them on performance and availability. When order must be exact rather than approximate, the answer is not an id at all but a commit timestamp from Spanner's TrueTime (Chapter 38) or an offset in a single log partition (Chapter 12).

### What Interviewers Probe

Expect six questions. Why not a UUID? Version 4 is 128 mostly random bits that scatter B-tree inserts; version 7 fixes the order but not the size, and is the right choice whenever size does not matter. What happens to the 4,097th id in a millisecond? It waits for the next millisecond. How are node numbers assigned, and what stops two nodes sharing one? An ephemeral ZooKeeper lease plus a time reservation, so even a partitioned old owner cannot overlap a new one. What happens when the clock goes backwards? The guard refuses until the clock catches up, NTP slews instead of stepping, leap seconds are smeared, and the reservation covers restarts. How long does the scheme last? 69 years from a custom epoch; counted from 1970 it would run out in 2039. Are the ids sorted? Strictly per node, and across nodes only to within clock skew.

That last answer has a sharp edge that strong candidates raise unprompted: an id orders creation, not commit. A reader that polls for ids above its cursor can skip a row minted early but committed late, or minted on a node with a slow clock, so change feeds re-read a short window behind the cursor or follow a commit-ordered log instead. Paging across shards works well, because every shard's ids sort into one time order: the reader asks each shard for its next ids below the cursor and merges the sorted lists (#20). Strong candidates also point out that `id % 1024` keeps only sequence bits, that rising keys hotspot range-partitioned stores, that ids reveal their creation time to anyone who sees them, and that JSON must carry ids as strings.

*Algorithms:* #145 Unique ID Generator · #100 URL Shortener · #20 Merge K Sorted Arrays
