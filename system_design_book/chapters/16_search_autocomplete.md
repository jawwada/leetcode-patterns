---
rank: 16
slug: search_autocomplete
---

Search autocomplete, or typeahead, offers whole queries while the user is still typing one. Type `how to t` and the box offers `how to tie a tie`, `how to take a screenshot` and a few more, changing with every keystroke before the next one lands. The service only reads, at a ferocious rate: every search costs several requests, each must be answered faster than a person types, and the answer for a prefix is the same for everyone who types it. Three questions decide the design: how to find the ten best completions of a prefix without looking at the millions of queries that start with it, how to turn billions of logged searches into rankings that stay fresh when news breaks, and how to keep a request per keystroke off the servers.

### Requirements

As the user types, the service returns up to ten completions of the text so far, ranked by how many people searched for them recently. Suggestions are kept per locale, so `fo` completes differently in `en-US` and `fr-FR`. A query that suddenly takes off, such as the name of a storm about to make landfall, must appear within minutes. Sexual, violent, hateful, dangerous and defamatory completions must never appear, and reviewers must be able to take one down within minutes. A query becomes a suggestion only after many different people have searched for it, so one person's private search is never offered to a stranger.

Assume 5 billion searches a day. Suggestions must appear within about 100 ms of the keystroke, which leaves the data center 10 ms at the 99th percentile. The service should be available 99.99% of the time, and its failures must be invisible: a slow or failed request shows nothing, and the search box keeps working. Consistency is loose: base rankings may be a day old, trending ones a few minutes. Search results (Chapter 22), spelling correction and ads are out of scope; typo tolerance and personalization appear at the end only as extensions.

### Estimates

```text
searches     5 B per day / 86,400 s                   ≈ 58,000 searches/s
suggest      ~10 requests per search, after debouncing ≈ 580,000 requests/s
peak         ×2 → 1.2 M/s; browser + CDN answer half → 600,000/s to servers
response     10 phrases × ~30 B + JSON ≈ 500 B;  1.2 M/s × 500 B ≈ 5 Gbps
budget       100 ms ≈ 60 ms network + 20 ms browser + 10 margin + 10 server
logs         5 B × 200 B ≈ 1 TB/day → daily counts 1.5 B rows × 40 B = 60 GB
phrases      kept if ≥ 50 distinct users searched them → assume 500 M
trie nodes   radix trie: ≤ 2 nodes per phrase → ≤ 1 B nodes
lists        1 B nodes × 64 B (ten 4-byte ids + label, links) ≈ 64 GB
phrase table 500 M × (30 B text + 4 B score) ≈ 17 GB → index ≈ 80 GB
shards       8 prefix ranges × 10 GB; × 3 replicas × 4 regions = 96 servers
CPU          600,000/s / 20,000 per server = 30 servers' worth
trending     58,000/s over 16 workers ≈ 3,600/s each ≈ 3.3 M per 15 min
sketch       4 rows × 2^18 counters × 4 B = 4 MB per worker-minute
error        ≤ e/2^18 × 3.3 M ≈ 34 extra counts, with probability 1 - e^-4 ≈ 98%
```

Three numbers shape the design. A million requests a second with 10 ms each rules out anything but a lookup in memory, and since a 500-byte answer depends only on the prefix, caches can take much of the load. Ten completions precomputed at every trie node make an index of about 80 GB, too big to copy to every server and comfortable as eight shards of 10 GB. And replication, not CPU, sizes the fleet: thirty machines could carry the load, but three replicas of eight shards in each of four regions leave each server about 6,000 requests a second, headroom for a lost region or a hot range. A terabyte of logs a day is routine for a batch job, and a 4 MB sketch counts a trending worker's searches to within a few dozen.

### API

```text
GET  /v1/complete?q=how+to+t&locale=en-US         sent after a pause in typing
     200 {"q": "how to t",
          "s": ["how to tie a tie", "how to take a screenshot", ...]}
     Cache-Control: public, max-age=60            up to 10 phrases, best first
     200 {"q": "zzqx", "s": []}                   nothing to suggest
     400 missing q or unknown locale               429 over the rate limit

POST /v1/admin/takedowns                           policy team, authenticated
     {"pattern": "...", "match": "phrase | prefix | term", "locale": "*"}
     201 {"rule_id": "tk_8812"}        enforced by every frontend in seconds

search event, written to the query log by the search frontend
     {query, locale, ts, user_hash, typed_prefix, picked_rank}
```

The completion call is a bare GET whose answer depends on nothing but its URL, with no cookie, account or history, which lets browsers, the CDN and the servers share one answer for `how to t` among millions of people. The client normalizes the text first, lower-casing it, collapsing spaces and applying Unicode normalization, so that `How  to T` and `how to t` are one cache key. The response echoes `q` because replies can overtake one another, and the client shows a reply only while its `q` still matches the box. An empty list is an ordinary, cacheable 200. Reads need no idempotency; scrapers harvesting the corpus prefix by prefix meet a rate limiter (Chapter 2) and a 429. The search event is internal: `typed_prefix` and `picked_rank` tell the pipeline whether a search came from a suggestion.

### Data Model

```text
query_log     Kafka topic partitioned by hash(query), kept 7 days
daily_counts  (locale, query, day) → users | picked             no user ids
              users: distinct searchers that day; picked: came via a suggestion
              columnar files, one set per day, kept 30 days
snapshot v42  immutable files per locale, written by the builder each night
  manifest    shard map: sorted range starts of 3-character keys → shard
  top table   every prefix of 1 or 2 characters → its ten best, as text
  shard k     one key range, e.g. ["sa", "sh"): whole subtrees as a radix
              trie, every node → top-10 phrase ids; phrase_id → text | score
overlay       per locale, every minute: phrase → users a day | expires_at
blocklist     rule_id PK | locale | match | pattern | reason | created_at
```

No database sits on the request path. The query log is a Kafka topic (Chapter 12), partitioned by a hash of the query so each trending worker sees every search for its share of phrases. The daily job counts distinct users and discards their ids, so what is kept for a month says how many people searched for a phrase, never who. A snapshot is a set of immutable files in object storage. Each shard file is a flat array of nodes that point to one another by offset, so a server loads it with one sequential read, and its lists hold ids from its own phrase table, since every completion of a node lies in that node's subtree. The blocklist is tiny but must be exactly right, so it lives in a small relational database that frontends reread every few seconds.

### Architecture

```dot
rankdir=TB;
user   [label="browser or app\ndebounce, local cache", class=client];
cdn    [label="CDN edge\n60 s cache", class=edge];
policy [label="policy service\ntakedowns"];
search [label="search frontend"];
fe     [label="suggest frontend\ntop table, merge, filter"];
block  [label="blocklist", class=store];
log    [label="query log\nKafka", class=queue];
shards [label="trie shards\nprefix ranges, replicated", class=cache];
trend  [label="trending job\nBloom filter, sketch", class=worker];
daily  [label="daily aggregation", class=worker];
snaps  [label="snapshot store\nimmutable files", class=store];
build  [label="index builder\nscore, filter, top-10", class=worker];
counts [label="daily counts\n30 days", class=store];
user -> cdn [label=" GET /complete"];
user -> search [label=" submit search"];
cdn -> fe [label=" miss"];
fe -> shards [label=" top 10 for prefix"];
shards -> snaps [dir=back, style=dashed, label=" load, swap"];
snaps -> build [dir=back, label=" v42"];
build -> counts [dir=back, label=" nightly"];
daily -> counts;
log -> daily;
search -> log [style=dashed, label=" search event"];
log -> trend [style=dashed];
fe -> trend [dir=back, style=dashed, label=" overlay"];
cdn -> policy [dir=back, style=dashed, label=" purge"];
policy -> block;
fe -> block [dir=back, style=dashed, label=" rules"];
block -> build [label=" filter"];
{rank=same; cdn; policy; search}
policy -> search [style=invis];
{rank=same; fe; block; log}
block -> log [style=invis];
{rank=same; shards; trend; daily}
{rank=same; snaps; build; counts}
```

The read path starts in the browser, which waits for a short pause in typing, checks its own cache and sends `GET /v1/complete`. The CDN edge answers popular prefixes from its cache, and a miss goes to a suggest frontend in the nearest region. The frontend normalizes the prefix and answers one- and two-character prefixes from the top table in its memory. Anything longer goes to one replica of the trie shard that owns its first three characters, which walks its trie and returns the node's ten phrases with their scores. The frontend merges in the overlay's trending phrases for that prefix, drops anything the blocklist matches and returns the list with a one-minute cache lifetime. A request touches one shard, no disk and no database.

The rankings come from what people search for, not what they type. When the user submits a search, the search frontend appends a search event to the query log. The trending job reads the log as it is written and every minute sends the suggest frontends a new overlay of phrases whose rate has jumped. The daily aggregation job reduces each day of the log to daily counts, and every night the index builder turns thirty days of them into scores, filters the phrases through its classifier and the blocklist, builds the tries and writes snapshot v42 to the snapshot store, from which the trie shards load and swap it in.

Takedowns take a third path. A reviewer files a rule with the policy service, which stores it in the blocklist, read by the frontends within seconds and by the next build, and purges from the CDN the cached answers for every prefix of the phrase.

### Deep Dives

#### Ten answers per prefix, computed ahead of time

The obvious design keeps the phrases in a trie (#43), walks to the node for the prefix and collects the best ten from everything below it, which is how the in-memory design of #97 answers. The walk is cheap and the collection is not: below `s` lie millions of phrases, and even with a heap (#19) that keeps only the best ten, visiting them all takes far longer than 10 ms. A database fails the same way, since `WHERE phrase LIKE 's%' ORDER BY score DESC LIMIT 10` finds the range in an index quickly and then reads and sorts every row in it. Both costs grow with the number of completions, and the shortest prefixes, typed most, have the most.

Precomputing turns the answer into a lookup. The builder stores at every node the ten best phrases below it, as ids sorted by score, and a request walks the prefix and returns the list, a few microseconds for `how` and for `how to tie a bow tie` alike. A prefix that ends inside an edge needs no node of its own: every phrase that begins with `wea` continues through the edge `ather`, so the node below that edge holds the answer.

```text
node                top 3 completions below it (users a day)
"we"                weather 9.0k · weather tomorrow 4.0k · weather radar 3.0k
├─ "ather" ●        weather 9.0k · weather tomorrow 4.0k · weather radar 3.0k
│  └─ " "           weather tomorrow 4.0k · weather radar 3.0k
│     ├─ "tomorrow" ●
│     └─ "radar" ●
├─ "b"              website builder 1.2k · webcam test 0.9k
│  ├─ "site builder" ●
│  └─ "cam test" ●
└─ "dding dresses" ●
● ends a phrase; a leaf holds one phrase and needs no list
```

Three choices keep the lists small. They hold 4-byte phrase ids, 40 bytes for ten instead of about 300 for the strings. The trie is a radix trie, whose edges carry runs of characters, so it has at most two nodes per phrase where a plain trie has one for every distinct prefix. And a leaf needs no list at all. That is how 500 million phrases fit in about 80 GB.

The builder sorts each shard's phrases, which lets it build the trie in one pass, and fills the lists children first: a node's list is the best ten among its own phrase and its children's lists. Those are already sorted, so this is a merge of sorted lists (#20) through a heap over their heads that stops after ten items, a few dozen operations per node. The price is that the lists are frozen at build time.

#### Fresh rankings: nightly snapshots and a trending overlay

The design of #97 keeps cached lists exact by editing them in place, which works there because counts only grow: the sentence just typed is the only one whose rank changes, and it can only climb. Here scores also fall, as each day's weight decays and bursts of popularity age out, and a node that keeps only its ten best cannot know which phrase becomes eleventh when one of them drops. Editing in place would also mean 58,000 searches a second, each rewriting a couple of dozen lists on every replica of a structure serving a million reads a second. Lists can only be recomputed from the full counts.

So the base index is rebuilt every night, never edited. The daily aggregation job reduces each day of the log to one row per locale and query, with the distinct users who searched for it and how many of them arrived by picking a suggestion. The builder scores each phrase by a weighted mean of its daily users over thirty days, the weights halving every seven days, so a score reads as users a day; picked searches count at a fraction, or the suggestions would rank themselves. It drops phrases that fewer than 50 distinct users searched for, counting each user once a day, which keeps private searches private and makes planting a suggestion expensive, and phrases that the classifier flags or the blocklist matches.

Each trie server then downloads its shard's new 10 GB file while serving, loads it into a second region of memory and checks it against checksums, golden prefixes with known answers and the share of lists that changed since yesterday. It flips a pointer, lets requests in flight finish on the old copy and frees it, at the cost of memory for two copies. Canaries go first, and yesterday's file stays on disk for rollback.

A nightly build cannot see breaking news, so a streaming path adds an overlay, with the machinery of Chapter 23. Each of the trending job's sixteen workers reads the log partitions for its share of queries. It drops repeats by testing each (user, query) pair against Bloom filters (#146) of the pairs seen in the last two quarter-hours, so a person or bot hammering one query counts once, and adds the rest to a count-min sketch (#147) for the current minute. The sketch estimates any phrase's count without storing phrases, which matters in a window that is mostly long tail: Google has said for years that about 15% of the queries it sees each day are new to it. Summing the last fifteen minute-sketches estimates the window, and since sketches add exactly, adding the newest minute and subtracting the oldest keeps the sum current. Phrases above a floor of a few hundred users enter a bounded min-heap of candidates (#19), and every minute the worker projects each one's daily rate, 96 times its fifteen-minute count. A phrase running at twice its base score joins the overlay once the classifier passes it, under stricter rules than the build's, because nobody has reviewed it.

```text
prefix "storm k"          users a day   from
storm kestrel                 480,000   overlay: 5,000 users in 15 min × 96
storm kestrel path             96,000   overlay: 1,000 users in 15 min × 96
storm king art center             900   base list from last night's build
storm king mountain               400   base list
```

Each frontend builds from the overlay a miniature trie with its own lists and merges its list for the prefix with the shard's, both sorted by score (#20), taking the higher score for a phrase in both; the best ten of the two lists are exactly the best ten overall. Overlay entries expire fifteen minutes after they were last published, so if the trending job stalls, old news fades instead of staying pinned at the top.

#### A request per keystroke

Sending every keystroke straight to the servers wastes work, since the same short prefixes are asked for constantly, and misbehaves, since a fast typist's replies arrive out of order. Three layers cut the load, each where it is cheapest.

The client waits for a pause of a few tens of milliseconds, so a burst of keystrokes sends one request; it cancels requests the user has typed past and keeps recent answers, so backspacing is free. It can also answer early: when `we` becomes `wea`, the phrases of the `we` list that start with `wea` are already right, since a phrase among the ten best for `we` is among the ten best for `wea`, and the reply only fills in the rest.

The CDN works because the answer is shared. Prefixes of up to three characters, a few tens of thousands per locale, are asked for constantly, and one requested a hundred times a second at a PoP misses once in 6,000 requests even with a 60-second lifetime. The short lifetime bounds how stale a trending list can be at the edge and how long a browser keeps a phrase that was taken down, while costing almost nothing on the prefixes that matter. Longer prefixes miss more often, so the caches absorb about half the load rather than nearly all.

The shards must split the rest so that each request touches one of them. Splitting by first letter is the classic mistake, since far more English queries begin with `s` than with `x`. The builder instead cuts the sorted three-character keys into ranges that balance memory and traffic, and each range holds whole subtrees, so one shard answers every prefix of three or more characters. The completions of a shorter prefix such as `s` span shards, so the builder computes those lists globally into the top table on every frontend. For scripts such as Chinese, where a character says far more than a Latin letter, the cut comes after one character.

### Scaling and Bottlenecks

Memory per shard is the first limit, and the easiest to move, because every build writes a new shard map: a range that outgrows its budget is cut in two by the next build, and nothing migrates, since the index is rebuilt nightly anyway. Traffic is lumpier than memory, so each range gets replicas in proportion to its requests, and the CDN keeps the hottest prefixes off the shards. Frontends are stateless; the top table, overlay and blocklist they hold come to a few megabytes per locale.

The pipeline scales by partitioning. The daily job is a MapReduce over a terabyte, the builder works on locales and ranges in parallel, and the top table's list for `s` is a k-way merge (#20) of the root lists of every key that begins with `s`. Snapshots, about a terabyte a day across the fleet, are copied once into each region's object store and fetched locally. Each of the four regions holds every shard of the locales it serves, and the overlay and blocklist are broadcast to all of them. The trending job is the only stateful stream, and its state is fifteen minutes deep, so adding workers means repartitioning the log and waiting a quarter of an hour.

### Failure Modes

A trie server that dies fails the frontends' health checks, and its shard's other replicas take its traffic. A slow server is likelier, especially while it loads a snapshot, so frontends hedge: a request still unanswered at the 95th-percentile latency goes to a second replica too, and the first answer wins, a technique Google described in *The Tail at Scale* that cuts the tail sharply for a few percent more requests. If no replica answers in time, the frontend returns the top table's list for the first two characters filtered to the prefix, correct if short, or nothing. A lost region is steered around by DNS and the CDN.

A bad snapshot is the dangerous failure, because it is wrong everywhere at once; validation stops most, canaries the rest, and rollback takes minutes. If the pipeline stops, users notice nothing: servers keep the last good snapshot. If the trending job stops, the overlay expires and frontends fall back to the base index.

The quieter failure is a bad suggestion. A completion reads as the search engine's own words, and in 2013 Germany's Federal Court of Justice held that a search engine must prevent a defamatory completion once told about it. So the defences are layered: the distinct-user threshold makes planting a phrase expensive, the classifier screens every phrase before it enters the index or the overlay, and a takedown reaches through every cache, filtered by frontends within seconds, purged from the CDN, forgotten by browsers within a minute and removed for good by the next build. Until then, a list that lost a phrase shows nine.

### Trade-offs and Alternatives

The central trade is computing answers ahead of time: lookups that cost only the length of the prefix, paid for with memory, a pipeline and staleness that the overlay patches. Collecting completions at query time needs only phrases and scores and updates in place, the better design for a small corpus: a shop's 100,000 product names fit in a sorted array where a binary search finds a prefix's range and a short scan ranks it. Between the two, a sorted phrase array with a range-maximum structure over the scores finds any prefix's ten best without per-node lists, for a fraction of the memory and a few times the CPU. Off the shelf, Elasticsearch's completion suggester keeps a finite-state transducer per index segment in memory and suits site search, and a key-value store with a list per prefix, in Redis or Bigtable, is easiest to run at medium scale, at the price of a row per prefix and a network hop.

Ranking is the other dial. Popularity with decay is easy to explain, cache and debug, where production systems rank candidates with learned models. Personalization collides with caching, since a per-user list cannot be shared, so the global list stays cacheable and the client merges in matches from the user's recent searches, kept on the device. Typo tolerance is costly in a trie, because every allowed edit branches the walk; the cheap forms allow one edit only after the first few characters, or map common misspellings, mined from queries users retyped, to their corrections.

### What Interviewers Probe

Expect six questions. Why not `LIKE 'prefix%'` in a database? Its cost grows with the matches, so precompute the ten best per node and pay only for the length of the prefix. How big is the index? Two radix nodes per phrase and ten 4-byte ids per node, about 80 GB in eight shards. How do you shard it? By ranges of three-character keys balanced by size and traffic, with shorter prefixes in a table on every frontend, so a request touches one shard. How do new counts reach the servers? Nightly rebuilds swapped in as snapshots, never edits in place, because a node that keeps ten phrases cannot know the eleventh. How does breaking news appear within minutes? A count-min sketch over the stream finds phrases running far above their base, and an overlay merges them in at query time. How do you survive a request per keystroke? Debounce and reuse in the client, a one-minute CDN lifetime, and no fan-out behind it.

Strong candidates raise four points unprompted: privacy, since a phrase must come from many distinct users before strangers see it; safety, with a classifier at build time and a blocklist that reaches through the caches; the feedback loop, since suggestions create the searches they are ranked by; and graceful degradation, since slow suggestions are worse than none. Interviewers rarely care which trie library you pick. They care that nothing heavier than a memory lookup stands between a keystroke and its answer.

*Algorithms:* #97 Design Search Autocomplete System · #43 Trie · #19 Top-K Elements · #20 Merge K Sorted Arrays · #147 Count-Min Sketch · #146 Bloom Filter
