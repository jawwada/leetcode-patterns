---
rank: 4
slug: distributed_cache
---

A distributed cache is a fleet of memory servers, usually Memcached or Redis, that sits between the application servers and the database. It answers most reads from RAM: a page that needs a hundred records gets them in one batched round trip of about a millisecond, and the database, sized for the misses alone, sees a few percent of the reads. Holding bytes in memory is the easy part. Three questions decide the design: how keys spread over the nodes and what moves when nodes come and go, how the cache stays consistent with a database it does not own, and what protects both when everyone wants one key at once, or misses it at once.

### Requirements

Application teams store serialized records under string keys: get one key or many, set a key with a time to live (TTL), delete a key. Values are opaque blobs of up to 1 MB, the cache evicts on its own when full, and each team's keys live in a namespace with a quota. Readers fill the cache on a miss and writers delete from it after committing to the database, the pattern called cache-aside.

Assume 2 M lookups a second at peak, one write per hundred lookups, and a hit ratio of at least 98 percent, because the database is provisioned for the misses alone. A get takes under a millisecond at the 99th percentile. The cache is not durable, but no single failure may push the database past its provisioned load. Consistency is eventual and bounded: other readers may see an old value briefly, never beyond its TTL, and a writer sees its own write at once. The database itself (Chapter 3), edge caching (Chapter 15) and Redis as a primary store are out of scope.

### Estimates

```text
lookups      1 M/s average, peak ×2 = 2 M/s    (a 50-key multi-get counts 50)
writes       1 per 100 lookups → 20,000/s at peak, each followed by a delete
misses       1% cold tail + ≤ 1% re-reads after deletes → hit ratio ≥ 98%
database     2% × 2 M = 40,000 reads/s at peak       (at 90% hits: 200,000/s)
hot set      2 B records; assume 15% draw 99% of lookups → 300 M items
item         1 KB value + 50 B key + 100 B per-key overhead ≈ 1.15 KB
memory       300 M × 1.15 KB ≈ 345 GB of RAM, before replicas
shards       2 M/s / 100,000/s per shard (assumed) = 20 shards, ≈ 17 GB each
bandwidth    2 M × 1 KB = 2 GB/s ≈ 16 Gbps in all, 0.8 Gbps per shard
hot key      one key at 5% of lookups = 100,000/s = a whole shard
lost shard   its 98,000 hits/s turn into DB reads: 40,000 → 138,000/s (×3.5)
```

The numbers make three points. The hit ratio sizes the database: each point is worth 20,000 database reads a second, so 90 percent instead of 98 means a database five times larger. Throughput, not memory, sets the shard count: the hot set's 345 GB would fit on a few large machines, but 2 M lookups a second need twenty shards of about 17 GB each. And more of the same nodes is not enough: one popular key saturates a shard, and one lost shard multiplies the database's load by three and a half, so hot keys and failures need mechanisms of their own.

### API

```text
get(key)                     → HIT value [hot]
                             → MISS lease=<64-bit token>   caller refills
                             → WAIT                        refill under way
get_multi([key, …])          → {key: HIT | MISS | WAIT}    one call per shard
set(key, value, ttl, lease)  → STORED | NOT_STORED         lease revoked
delete(key)                  → DELETED | NOT_FOUND         revokes leases

library calls, the only ones application code makes
fetch(key, ttl, loader)      → value    get, lease, load, set; retry on WAIT
invalidate(key)              → ok       delete, after the database commit
```

Application code never speaks this protocol. It calls fetch with a loader that reads the database, and the library does the rest, retrying a few milliseconds later on WAIT, so leases, negative caching and the in-process tier work the same at every call site. Deletes can be retried, replayed and reordered freely; sets of different values cannot, which is why a set carries a lease. get_multi queries the shards in parallel, so a hundred keys cost one round trip, and every call has a timeout of a few milliseconds.

### Data Model

```text
item       key → value (≤ 1 MB) | expires_at | flags | LRU or LFU bits
key        "<namespace>:<type>:<id>:v<schema>"    e.g. "user:profile:42:v3"
placement  hash(key) on a ring of 200 virtual nodes per shard → owner
ttl        1 hour ± 10% jitter by default; negative entries 30 s
lease      key → (64-bit token, issued_at)   on the key's own shard, 10 s life
negative   key → NOT_FOUND marker            set when the loader finds no row
hot copy   "user:profile:42:v3#0" … "#7"    8 copies, scattered by the ring
L1         per app server, hot keys only     TTL 2 s, a few hundred MB
```

Each shard is an in-memory hash table holding copies of what the database owns, so any entry can be evicted or lost at the cost of one miss. The key carries a namespace, for quotas and per-team hit ratios, and a schema version, so a deploy that changes the serialization switches to v4 keys and lets v3 age out. A lease lives on its key's shard, so one server arbitrates every fill of that key. Negative entries keep lookups for missing rows, from a scanner probing random ids for instance, off the database; the delete that follows a create removes them. The engine is Redis: replication with failover gives each shard a warm standby, and a short Lua script makes "store only if this lease is still valid" one atomic step.

### Architecture

```dot
rankdir=TB;
users  [label="users", class=client];
db     [label="database\nsource of truth", class=store];
app    [label="app servers\ncache library + L1"];
config [label="config store\nring + hot-key list", class=store];
tailer [label="commit-log\ntailer", class=worker];
inval  [label="invalidations", class=queue];
router [label="cache router\nsidecar per host"];
hot    [label="hot-key\ndetector", class=worker];
subgraph cluster_shards {
  label="cache cluster: 20 shards on a hash ring"; style="rounded,dashed"; color="#9CA3AF";
  s1 [label="shard 1\n+ replica", class=cache];
  s2 [label="shard 2\n+ replica", class=cache];
  sn [label="shard 20\n+ replica", class=cache];
}
users -> app [label=" request"];
db -> app [dir=back, label=" read on miss,\n write"];
app -> router [label=" get / set / delete"];
db -> tailer [style=dashed, label=" commit log"];
tailer -> inval [style=dashed];
inval -> router [style=dashed, label=" delete k"];
router -> s1;
router -> s2;
router -> sn;
router -> hot [style=dashed, label=" sampled\n keys"];
hot -> config [style=dashed, label=" hot keys", constraint=false];
config -> router [style=dashed, label=" ring +\n hot list"];
app -> config [style=invis];
{rank=same; db; app; config}
{rank=same; tailer; inval; router; hot}
```

A user's request reaches an app server, whose cache library first checks its L1, a small in-process table of keys flagged as hot. Otherwise it hands the lookup to the cache router, a sidecar proxy in the style of Facebook's mcrouter or Twitter's Twemproxy, which hashes each key onto the ring and sends one request per shard. A hit returns at once. A miss returns a lease: the library reads the row from the database primary and sets it with the lease through the router, while readers that arrive meanwhile get WAIT and, retrying, usually find the value.

A write commits to the database, then the library deletes the affected keys through the router, so the writer's next request reads its own write. In the background, the commit-log tailer reads the database's log of committed changes, maps each changed row to its cache keys and publishes them on the invalidations stream, and router instances delete each key, retrying until the shard acknowledges.

Routers also send a 1 percent sample of their lookups to the hot-key detector, which publishes a hot-key list to the config store; the config store, which also holds the ring, pushes both to every router. Responses for hot keys carry the flag that puts them in L1, and the router spreads those keys over several shards.

### Deep Dives

#### Keeping the cache consistent with the database

The obvious write path updates the cached value after updating the database, and two concurrent writers break it: they commit v2 then v3, but their cache updates can arrive in the opposite order and leave v2 cached until its TTL expires. Deleting removes the ordering problem, because deletes are idempotent and commute, and the next reader refills from the only place that knows the latest value. The delete must follow the commit, or a reader can refill the old value in between. Even then a slow reader can poison the cache:

```text
reader A                    writer B                        cache
get k → MISS                                                (empty)
read DB → v1
                            commit v2
                            delete k                        (empty)
set k = v1 ───────────────────────────────────────────────→ v1, stale
```

A read v1 before the commit and set it after the delete, so the cache holds v1 until its TTL expires. Leases, from Facebook's memcache paper, close this race. On a miss the shard returns a 64-bit token bound to the key, a set must present it, and a delete revokes every outstanding token, so A's set is refused with NOT_STORED and the next reader fetches v2. The cost is a little state per key being refilled and an occasional wasted database read. The alternative is versioned values: each value carries its row's version, a set succeeds only if it is newer than what is stored, and writers leave a short-lived tombstone with the new version instead of deleting. Versions need no lease state, but every writer must know the version it committed and they do nothing for stampedes, so this design uses leases. Fills always read the primary, because a fill from a lagging replica would cache the old value after the delete and no lease could notice.

All of this assumes the delete arrives, yet an app server that crashes just after its commit never sends one, which is why the tailer exists. The database's log is durable and ordered, so the tailer resumes from its last position after a crash and replays anything it may have missed, the same reason Facebook's invalidation daemons, mcsqueal, read the commit log. The TTL is the last line of defence: no stale value outlives it. Data that must never be stale, a balance or a seat count, is read from the database.

#### Hot keys and stampedes

Consistent hashing gives every key one home, which is the problem when one key draws 5 percent of all lookups: 100,000 a second land on one shard and starve every other key on it, and adding shards changes nothing. The detector finds such keys by counting the routers' samples in a count-min sketch (#147) over ten-second windows and keeping the heaviest in a small heap (#19); keys above half a percent of traffic go on the hot list.

Two remedies follow. The library keeps hot keys in L1 for two seconds, so 1,000 app servers fetch a key at most 500 times a second however many users read it, at the cost of two seconds of staleness; Redis 6 client-side caching can shorten that by pushing an invalidation to every client that read the key. The router also writes the key as eight suffixed copies, which the ring scatters over different shards, and reads one of them at random, so each copy carries 12,500 lookups a second; deletes must reach all eight, which is why the hot list is global and shared by the routers that carry invalidations. Big values hit the network first: a 500 KB value read 10,000 times a second needs 40 Gbps, more than a 25 Gbps card carries, so such values are compressed, split across shards or served from L1.

A stampede is the opposite failure: a popular key expires or is deleted, and every concurrent reader misses at once. At 100,000 lookups a second and 20 ms per database read, 2,000 queries for that key are in flight before the first refill lands. Coalescing in each process, as Go's singleflight does, caps that at one per app server, still a thousand. A per-key lock in the cache, a Redis SET with NX and a few seconds' expiry, caps it at one for the fleet, and a lease is that lock with revocation added: the shard grants one lease per key every ten seconds and tells everyone else to WAIT. With leases, Facebook saw the peak database rate for herd-prone keys fall from 17,000 to 1,300 queries a second. Keys that expire by TTL can be refreshed before anyone misses: with probabilistic early expiration (XFetch), a reader recomputes early when `now - delta * beta * ln(rand()) >= expiry`, where delta is the recompute time and beta about 1, so usually one reader refreshes just before expiry. Jittering TTLs by 10 percent keeps keys filled together from expiring together.

#### Eviction and the memory budget

A cache is always full, so eviction decides the hit ratio. Exact LRU (#44), a hash map over a doubly linked list, costs two pointers per item and turns every hit into a write to a shared list, which needs a lock in a multithreaded server. Redis keeps no list: each object stores a 24-bit last-access clock, and on eviction Redis samples five keys and drops the one idle longest, which on power-law workloads comes close to true LRU.

LRU's weakness is the scan: a batch job that reads every record once flushes the hot set. LFU (#93) protects popular keys but must also forget, or yesterday's viral key squats forever; Redis's LFU mode keeps, in the same 24 bits, a logarithmic counter that by default saturates near a million hits and decays every minute. In-process caches do better still with W-TinyLFU, as in Java's Caffeine, where a count-min sketch estimates how often recent keys were seen and a newcomer is admitted only if it is more popular than the item it would evict.

TTL is a different tool: expiry bounds staleness, eviction bounds memory. Expired entries go lazily when read and through a background sweep that samples keys with TTLs, as in a cache with expiring keys (#94). Bookkeeping costs memory too. A memcached item carries a header of about fifty bytes, and Redis spends on the order of a hundred bytes per key on its hash-table entry and object headers, which is why the estimates budget 1.15 KB per 1 KB value. Memcached's slab allocator, which splits 1 MB pages into chunk sizes 1.25 times apart, can also waste up to a fifth of a chunk and strands pages in the wrong class when value sizes shift.

### Scaling and Bottlenecks

Throughput per shard is the first limit. Redis executes commands on one thread, so a shard is one process, and twenty primaries with their replicas share a handful of many-core machines, each replica on a different rack from its primary. Shards sit on a consistent-hashing ring (#139): with one point per shard the busiest of twenty typically holds three times its fair share, and with 200 virtual nodes each it holds 10 to 20 percent more than average. A twenty-first shard takes over 1/21 of the keys, about 5 percent, where hashing modulo the shard count would move 95 percent, a full flush. The moved keys arrive cold, so resizes run off peak, or the router falls back to the old owner on a miss while deletes go to both. Redis Cluster instead hashes keys into 16,384 slots and migrates slots with their data, redirecting clients with ASK and MOVED.

Multi-gets are the next limit. A page whose hundred keys span all twenty shards sends twenty requests, so more shards do not mean fewer requests per shard, and the page waits for the slowest: `1 - 0.99^20 ≈ 0.18` of pages meet some shard's 1-in-100 slow reply. Facebook replicated small key families fetched this way onto more servers rather than split them further. Across regions, each region runs its own cluster in front of its own database replica, and its tailer reads that replica's log, so a key is invalidated only once the local replica holds the new value.

### Failure Modes

When a primary dies, its replica is promoted within seconds, as Redis Sentinel or Redis Cluster do, and the router reads from the replica meanwhile, so the database never sees that shard's misses. Replication is asynchronous, so the new primary may lack the last writes the old one acknowledged. A lost set costs a miss, but a lost delete leaves a stale value, so after a failover the tailer replays the last minute of that shard's invalidations, which is harmless because deletes are idempotent.

If both copies die, the ring drops the shard and its keys land cold on its neighbours, adding 98,000 database reads a second, which coalescing and a rate limiter (Chapter 2) in front of the database turn into a slowdown rather than an outage. A slow shard is worse than a dead one, so calls have short timeouts and a circuit breaker. A shard that leaves the ring and returns may hold values whose deletes went elsewhere, so it rejoins empty. A cold cluster must never send its misses straight to the database: Facebook's warm-up fills them from a warm cluster, with a two-second hold-off after each delete that refuses re-adds, so a copied stale value cannot land on top of an invalidation.

### Trade-offs and Alternatives

The write strategy is the central choice. Cache-aside, used here, caches only what is read and turns a cache failure into a slowdown, paying with the stale-set race and a miss after each write. Read-through moves loading into the cache layer, as DynamoDB Accelerator (DAX) does, with the same semantics; this design's fetch is read-through in the library and cache-aside on the wire. Write-through updates cache and database together, so freshly written keys never miss, but it adds write latency, caches data nobody reads and still cannot make the two writes atomic. Write-back acknowledges writes from the cache and flushes them in batches, absorbing bursts such as the counters of Chapter 50, but a node lost before its flush loses acknowledged writes, so the cache must be replicated and persisted, at which point it has become a database.

Invalidation is optional too: for data that may be a minute stale, a TTL alone is correct and needs no tailer. Replicas double the memory, to about 700 GB. Facebook's memcache keeps no standby per server, sending a dead server's traffic to a Gutter pool of about 1 percent of the servers whose entries expire quickly, rather than rehashing it onto neighbours that a hot key could knock over next. A design built that way would pick Memcached, multithreaded and leaner per item, whose meta protocol gives one client a win flag to refill a missing key and tells the rest a refill is under way.

### What Interviewers Probe

Expect these questions. Why delete rather than update the cache on a write? Deletes are idempotent and commute, while reordered updates leave the older value behind. Can delete-on-write still cache a stale value? Yes, through the stale set, until the TTL expires, unless fills carry leases or versions. What moves when you add a node? About 1/(N+1) of the keys with consistent hashing, nearly all of them with modulo hashing. What about a key read a million times a second? Detect it, keep it in process for a second or two, and replicate it across shards. What happens when a popular key expires? A stampede, contained by leases, coalescing, early refresh and TTL jitter. LRU or LFU? LRU for recency, LFU when scans pollute the cache, both approximated by sampling in Redis. What if a node dies? A replica takes over, deletes are replayed, and a rate limiter shields the database.

Strong candidates raise three points unprompted: the hit ratio sizes the database, so 98 against 90 percent is a fivefold difference; negative caching keeps lookups for missing rows off the database; and every cached record is a consistency decision, so they say what may be stale, for how long, and which reads must go to the database instead.

*Algorithms:* #44 LRU Cache · #93 LFU Cache · #94 Cache with Expiring Keys · #139 Consistent Hashing · #147 Count-Min Sketch · #19 Top-K Elements
