---
rank: 22
slug: web_search_engine
---

A web search engine takes a few words, `"new york" pizza`, and in a couple of hundred milliseconds returns the ten most useful pages out of fifty billion, each with a snippet that shows why it matched. The crawler of Chapter 17 has already fetched the pages; this chapter turns them into an index and the index into ranked results. Three questions decide the design: how to lay out the index so that a query reads only the postings it needs, how to split a 100 TB index across a thousand machines and still answer in tens of milliseconds, and how to rank in stages so that the expensive models see a thousand candidates instead of millions of matches.

### Requirements

A user submits a query of a few words, optionally with quoted phrases, and receives the ten most relevant pages, each with its title, URL and a snippet that shows the query words in context, and can page on to later results. Relevance draws on a page's text, its title, the anchor text of the links that point at it, and the page's importance in the link graph. The index follows the web: a new article on a news site must be searchable within minutes of being crawled, and every other change within a day.

Assume an index of 50 billion pages and 5 billion queries a day. The results page must be ready in 200 ms at the median and 500 ms at the 99th percentile, measured at the front end. Search must survive the loss of machines, racks and whole data centres, and a lost shard may cost a sliver of the results but never the page. Consistency is loose: results may trail the crawl by minutes, and two users may briefly see different versions of the index. Only the crawl repository needs durability, since every index can be rebuilt from it. Crawling itself (Chapter 17), autocomplete (Chapter 16), ads, personalization, image and video search, and the details of spam fighting are out of scope.

### Estimates

```text
queries      5 B a day / 86,400 s             ≈ 58,000 QPS (peak ×2: 115,000)
cache        assume 40% hit the result cache  → 69,000 ≈ 70,000 QPS at peak
corpus       50 B pages × ~1,000 words, ~6 KB of text each         ≈ 300 TB
index        compressed positional postings ≈ 1/3 of the text     ≈ 100 TB
doc store    page text compressed ~3× for snippets                 ≈ 100 TB
shards       100 TB / 100 GB in each leaf's memory = 1,000 × 50 M pages
leaf load    70,000 QPS × 1,000 shards                     = 70 M lookups/s
replicas     at 1,000 lookups/s per leaf: 70,000 leaves = 70 per shard
tail         1,000 leaves, each slow 0.1% of the time: 1 - 0.999^1000 ≈ 63%
fresh tier   1 B new or changed pages a day ≈ 12,000/s; a day ≈ 2 TB of index
result cache 100 M recent queries × 5 KB per entry                 ≈ 500 GB
rollout      100 GB × 70,000 leaves per daily build = 7 PB a day ≈ 80 GB/s
```

Three numbers shape the design. The index is 100 TB, so it is cut into a thousand shards of 50 M pages, each small enough to live in the memory of one leaf server, which lets a leaf scan postings in milliseconds instead of seeking on disk. Every uncached query touches every shard, so the fleet is sized by queries times shards rather than by bytes: 70 million shard lookups a second need about 70,000 leaves, and each point of cache hit rate saves more than a thousand of them. And a thousand-way fan-out turns rare slowness into common slowness: if each leaf stalls one time in a thousand, 63% of queries wait for a stalled leaf. The fresh tier, by contrast, is small, since a day of changes is 2% of the corpus.

### API

```text
GET /search?q=%22new+york%22+pizza&start=0&num=10&lang=en&region=us
    200 {"results": [{"url": "...", "title": "...", "snippet": "..."}],
         "next_start": 10, "corrected_query": null}
    400 empty or overlong query        429 automated traffic, slow down

rpc Leaf.Search(terms, phrases, k=10, deadline_ms)
    → {"hits": [(url_hash, score, features)], "partial": false}
rpc DocServer.Snippets(url_hashes, terms) → [(url, title, snippet)]
```

Search is a GET: safe, idempotent and cacheable, so a retry is harmless and the result cache can key on the normalized query, language and region. Pagination is an offset rather than a cursor because nothing is stored per user. The API serves at most the first 100 results, deeper than people read, and the cache entry holds all 100, so pages two to ten cost only snippet lookups. Searching needs no login, but scrapers are throttled with 429 by the rate limiter of Chapter 2. Inside the cluster every RPC carries a deadline, and a leaf that runs out of time returns the best it has found with `partial` set, because a slightly incomplete answer on time beats a perfect one late.

### Data Model

```text
repository  url → fetched_at | content_hash | html | outlinks     (Chapter 17)
base shard  shard = hash(url) mod 1,000; doc_id = rank by static score
lexicon     term → global doc_freq | max_score | offsets of its postings
postings    term → blocks of 128 (doc_id gap, tf, field bits), bit-packed;
            skip entry per block: last doc_id | highest score in the block
positions   (term, doc_id) → position gaps, in a stream of their own
forward     doc_id → url_hash | length | static_score | quality | language
deletes     per base shard: bitmap of doc_ids superseded since the build
fresh shard same layout in memory, doc_ids in arrival order, appended live
docs        url_hash → url | title | compressed text        on doc servers
cache       hash(normalized q, lang, region) → top 100 url_hashes + snippets
```

Nothing on the serving side is a database. A base shard is a set of immutable files, built offline, copied to every replica and replaced whole by the next build; a leaf holds its shard in memory and changes nothing but the deletes bitmap. Doc IDs are dense integers local to a shard, assigned in order of static score, so the best pages come first in every postings list. The lexicon stores each term's corpus-wide document frequency rather than the shard's own, so every shard computes the same idf and scores from different shards can be compared. Positions sit in a stream of their own because they are the bulkier part of the index and only phrase and proximity scoring reads them. The repository is the crawler's wide-column table keyed by URL, which the batch build scans in bulk. Fresh shards share the layout but live in memory and grow by appending. The doc servers keep compressed page text, sharded like the index, and the result cache is a distributed in-memory cache (Chapter 4) with LRU eviction (#44), whose entries expire after minutes for newsy queries and after hours for the rest, since a cached page cannot see what the fresh tier has learned since.

### Architecture

```dot
rankdir=TB;
browser [label="browser", class=client];
fe      [label="front end", class=edge];
qs      [label="query service\nrewrite, spell", class=service];
cache   [label="result cache", class=cache];
root    [label="root\nmerge top-k", class=service];
ranker  [label="ranker\nfinal model", class=service];
docs    [label="doc servers\nsnippets", class=store];
parents [label="parent\naggregators", class=service];
leaves  [label="base index leaves\n1,000 shards × 70", class=service];
fresh   [label="fresh index\nleaves", class=service];
dfs     [label="shard files\non DFS", class=store];
sidx    [label="stream indexer", class=worker];
batch   [label="batch indexer\ndaily", class=worker];
pr      [label="PageRank job", class=worker];
stream  [label="change stream", class=queue];
repo    [label="page repository\n(Chapter 17)", class=store];
browser -> fe [label=" GET /search"];
fe -> qs;
qs -> cache [label=" 1. lookup"];
qs -> root [label=" 2. on miss"];
qs -> docs [label=" 3. snippets"];
root -> ranker [label=" top 1,000"];
root -> parents [label=" fan-out"];
parents -> leaves;
root -> fresh;
leaves -> dfs [dir=back, style=dashed, label=" load"];
docs -> dfs [dir=back, style=dashed];
dfs -> batch [dir=back, style=dashed];
batch -> repo [dir=back, style=dashed, label=" daily\n snapshot"];
pr -> batch [style=dashed, label=" static scores"];
repo -> pr [style=dashed, label=" link graph"];
fresh -> sidx [dir=back, style=dashed, label=" add"];
leaves -> sidx [dir=back, style=dashed, label=" deletes"];
sidx -> stream [dir=back, style=dashed];
stream -> repo [dir=back, style=dashed, label=" changed\n pages"];
{rank=same; browser; fe}
{rank=same; qs; cache}
{rank=same; root; ranker; docs}
{rank=same; leaves; fresh}
{rank=same; dfs; batch; sidx; stream}
{rank=same; repo; pr}
```

The query path starts at the browser and reaches the nearest serving cluster, each of which holds a complete copy of the index, so a query never leaves its data centre. The front end terminates TLS and renders the page. The query service normalizes the query, corrects its spelling, adds synonyms and looks it up in the result cache, and a hit returns at once. On a miss it hands the rewritten query to the root, which sends it through about thirty parent aggregators to one replica of each of the 1,000 base index leaves, and directly to the fresh index leaves. Each leaf intersects its postings, scores the matches and returns its ten best with their features. The parents merge their leaves' lists, the root keeps the best 1,000 and passes them to the ranker, whose model orders them, and the query service asks the doc servers for the titles and snippets of the first ten, fills the cache and answers.

The index path runs the other way, from the crawl up to the leaves, in two lanes. The batch lane runs once a day: the batch indexer reads a snapshot of the page repository, parses and tokenizes every page, inverts it into postings shard by shard and writes the shard files to the distributed file system, folding in the static scores that the PageRank job computes from the same snapshot's link graph. Base index leaves and doc servers then load the new files, a few replicas at a time. The fresh lane runs continuously: the repository publishes every new or changed page to the change stream, and the stream indexer adds each one to the fresh index leaves within a minute and sends a delete for its old version to the base index leaves of its shard, so the stale copy stops matching at once.

### Deep Dives

#### Postings: building, compressing and intersecting them

The naive engine scans the pages for the query words, which at 300 TB of text is hopeless for even one query, and a relational table of (term, page) rows would hold tens of trillions of rows and answer every AND with a join. The inverted index (#150) turns the corpus inside out: for each term, the list of documents that contain it, sorted by doc ID, each posting carrying the doc ID, the term frequency, bits for the fields it occurred in (title, anchor text, body) and, in the separate stream, its positions.

Building it is a sort. The batch indexer walks each shard's pages in doc ID order, so every term's postings come out already sorted; it accumulates them in memory, writes a sorted run whenever the buffer fills, and merges the runs into the final postings with a k-way merge (#20). Anchor text needs one shuffle first, grouping the text of every link by the URL it points to, so that a page is indexed under the words other pages use for it.

Compression decides whether the index fits in memory. A posting stores the gap to the previous doc ID instead of the ID itself, and gaps are small exactly where lists are long: a term in 1% of a 50 M-page shard has 500,000 postings with an average gap of 100, which needs 7 bits instead of 32. Gaps are packed in blocks of 128 at the bit width of the largest gap in the block, the layout Lucene uses, and such blocks decode with SIMD instructions at more than a billion integers a second on one core. Positions are gap-coded within each document the same way. Every block also gets a skip entry with its last doc ID and its highest score.

Intersection starts from the rarest term. For each doc ID on its list, the cursor on every other list jumps over whole blocks whose last doc ID is smaller, decodes the one block that may hold the target and binary-searches it (#14), so the cost follows the short list rather than the long one. A phrase adds one step for the documents that survive: walk the position lists of `new` and `york` together like a merge, looking for a position p followed by p + 1. Positions are decoded only for these few candidates, so a phrase costs little more than an AND. The price of all this packing is that the index cannot be edited in place; changes reach it through the next build or through the fresh tier.

#### Sharding by document, and the tail of a thousand-way fan-out

There are two ways to cut an inverted index. Partitioning by term gives each machine the complete postings of some terms, which looks efficient, since a three-word query then touches three machines instead of a thousand. It fails on every other count. The postings of `new` across 50 billion pages run to gigabytes, and intersecting them with those of `pizza` means shipping one list to the other's machine; popular terms turn their machines into hot spots; indexing one page touches the hundreds of machines that own its words; and a dead machine makes some words unsearchable. Partitioning by document makes each shard a complete search engine over 50 M pages. Every query goes to every shard, each shard evaluates it locally, and only ten small results per shard cross the network; load is even by construction, and losing a shard loses 0.1% of the pages rather than whole words. Google described this layout in 2003: index shards that each hold a randomly chosen subset of the documents, each served by its own pool of machines.

The shard of a page is hash(url) mod 1,000, and that randomness pays twice. Scores from different shards are comparable once every shard uses the global document frequencies, and each shard needs to return very little: the global top 1,000 lands about one per shard, and the chance that any shard holds more than ten of them is about one in a hundred thousand. So each leaf returns its best ten, each parent merges the sorted lists of its thirty-odd leaves (#20), and the root keeps the overall best 1,000 in a min-heap (#19). Resharding needs no consistent hashing either: it is just a build with a new shard count, rolled out one serving cluster at a time.

The hard part is the tail. A query is as slow as its slowest leaf, and the estimate showed that a one-in-a-thousand stall per leaf delays 63% of queries. Three mechanisms from Google's paper *The Tail at Scale* keep the tail short. A hedged request sends a second copy to another replica of a shard when the first has not answered within the 95th-percentile latency, which adds about 5% load and removes most stragglers. A deadline lets the root answer without a shard that is still silent, which costs a random 0.1% of the web and almost never changes the first page. And a canary request sends each new query to one or two leaves before the other thousand, so a query that crashes leaves, a query of death, takes down two machines instead of the fleet. Replicas, seventy per shard spread across the serving clusters, supply the throughput: a replica adds queries per second, a shard adds pages.

#### Ranking in stages, with early termination

The naive ranker runs the best model on every match. A common term matches hundreds of millions of pages, so even at a microsecond per page the cheapest score would cost minutes of CPU per query, and a learned model costs far more per page. Ranking is therefore a cascade in which every stage is more expensive per page and sees far fewer pages.

The first stage runs on each leaf over the matching pages and adds a text score to a static one. The text score is BM25, a refinement of TF-IDF, and the static score comes mostly from PageRank:

```text
bm25(d, q) = sum over query terms t of  idf(t) × tf × (k1 + 1) / (tf + K)
K          = k1 × (1 - b + b × len(d) / avg_len)          k1 ≈ 1.2, b ≈ 0.75
idf(t)     = ln(1 + (N - df + 0.5) / (df + 0.5))     N pages, df pages with t
PR(p)      = 0.15 / N + 0.85 × sum over pages q linking to p of PR(q) / out(q)
```

Through idf a rare term weighs more than a common one, through k1 each further repetition of a word adds less, and through b a long page earns nothing for its length alone; scored per field, a match in the title or anchor text counts for more than one in the body. PageRank is the chance that a random surfer is on the page if they follow a random link 85% of the time and jump to a random page otherwise. The PageRank job computes it by applying the last line to every page of the link graph, pass after pass, until the values settle.

Early termination keeps this stage cheap. The leaf keeps its best candidates so far in a min-heap (#19), and the smallest score in the heap is the threshold a new page must beat. Each block's skip entry stores the highest score inside it, so a block whose bounds, summed over the query terms, fall below the threshold is skipped without being decoded; this is block-max WAND, which Lucene adopted in version 8. Because doc IDs follow static score, the best pages come first, the threshold climbs early, and most blocks of a long list are never touched.

The second stage, still on the leaf, re-scores the few hundred survivors with a small learned model over richer features: how close together the query words occur, exact phrase matches, freshness, language, and the spam and quality scores of the forward index. The third stage is the ranker, a large model, gradient-boosted trees in the LambdaMART style or a neural network that reads the query and the page together, applied to the 1,000 merged candidates. It sees the list as a whole, so it also collapses near-duplicates and limits each site to a couple of results. The models learn from human relevance judgments and from click logs corrected for position bias. The price of the cascade is recall: a page the first stage drops can never be rescued by a better model later, so the early stages are tuned to keep generously.

### Scaling and Bottlenecks

The leaves are most of the fleet, CPU-bound, and the first thing to run out. Their number grows with queries times pages, so the levers that matter cut the work per query, which is why the result cache and early termination are tuned against the leaf count. More pages mean more shards and a wider fan-out, more queries mean more replicas, and the two-level tree keeps the root's fan-in at about thirty parents; a third level would follow if shards reached the tens of thousands.

The quieter bottleneck is moving the index. A daily build sends 100 GB to each of 70,000 leaves, 7 PB a day, so each serving cluster pulls one copy of every shard from the distributed file system and spreads it among its own machines peer to peer. Leaves switch a few replicas per shard at a time and warm up on replayed queries before taking traffic, so capacity never dips. Each build records the change-stream offset of its snapshot, and a leaf that loads it replays the deletes from that offset, so no stale page reappears; the fresh tier drops its older pages only when every shard has switched, and the root collapses duplicates by URL hash during the handover. The fresh tier scales on writes rather than reads: 12,000 page updates a second land on top of the full query load, so it holds a single day and is split into enough shards that each absorbs its share of updates in memory.

### Failure Modes

A leaf that dies is invisible: the next request for its shard goes to another of the seventy replicas, and a request already in flight is covered by the hedge. A shard whose replicas are all unhealthy in one cluster costs that cluster 0.1% of the web until the root sends that shard's requests to a neighbouring cluster, and a cluster that fails outright is handled by DNS steering its users elsewhere, which works because every cluster holds the full index and carries headroom for a neighbour's load.

The dangerous failures hit every machine at once, because every machine sees every query. Canary requests stop a query of death. A bad build, corrupt or merely worse at ranking, must not spread: each build passes sanity checks on shard sizes and term counts and an evaluation against the previous build on a fixed set of judged queries, goes live in one cluster first, and leaves keep the previous build on local disk so they can switch back in minutes. Overload degrades quality rather than availability: leaves that fall behind raise their early-termination thresholds and return slightly worse results on time.

When the stream indexer falls behind, results grow staler but stay correct, since the base index still answers everything; its lag is the freshness metric to alert on. A stampede on a suddenly popular query in the first minutes of breaking news is absorbed by the query service, which coalesces identical in-flight misses so that one evaluation answers them all.

### Trade-offs and Alternatives

Document partitioning buys even load and graceful failure at the cost of a thousand-way fan-out; term partitioning fits only workloads of single-term lookups, where no two lists ever have to meet. Holding the index in memory buys latency with RAM. A smaller engine keeps postings on SSD, lets the operating system's page cache hold the hot lists, as Elasticsearch does, and pays a few milliseconds per query.

The daily build with a fresh tier is simple to validate and roll back and keeps the base index fully compacted, at the price of two indexing paths and a handover between them. Google went the other way in 2010: its Caffeine index updates continuously, built on Percolator's incremental transactions over Bigtable, and the Percolator paper reports that this halved the average age of documents in search results. A product that needs minutes of freshness for every page, not just for news, should pay for incremental indexing; most should start with tiers.

Numbering documents by static score is what makes early termination work, while numbering them by URL compresses better, because pages of one site share words and sit next to each other; an index that is always searched exhaustively, such as one over logs or code, should number by URL. Finally, an inverted index finds only pages that contain the query's words. Engines increasingly add a dense retriever, an embedding per page and a nearest-neighbour search, whose candidates join the first stage, and pay for it with a second index and more memory per page.

### What Interviewers Probe

Expect the conversation to circle seven questions. Why partition by document and not by term? Even load, local intersection, small results on the wire and graceful loss of a shard, where term partitioning would ship gigabytes of postings between machines. How do you get the global top ten from a thousand shards? Comparable scores from global document frequencies, each leaf's best ten, merges up the aggregation tree, and the probability argument for why ten per leaf is enough. How big is the index and where does it live? Fifty billion pages make 100 TB of postings, held in memory across 1,000 shards with 70 replicas each. How does a phrase query work? Positions, checked only on the pages that survive the AND. How does a new page appear within minutes? The fresh tier, with a deletes bitmap masking the stale base copy. How do you rank? BM25 and PageRank on the matches, then learned models on fewer and fewer candidates. What happens when one leaf is slow? Hedged requests, deadlines and partial results.

Strong candidates raise four points unprompted: the tail arithmetic of a thousand-way fan-out, which makes hedging a requirement rather than an optimization; global statistics, without which scores from different shards cannot be merged; doc IDs in static-score order, which make early termination work; and the danger of a bad build or a query of death that reaches every machine at once. Interviewers rarely want the BM25 formula recited. They want to hear that the most expensive model never sees more than a thousand pages.

*Algorithms:* #150 Inverted Index · #20 Merge K Sorted Arrays · #19 Top-K Elements · #14 Binary Search · #44 LRU Cache
