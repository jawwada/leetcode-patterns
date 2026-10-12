---
rank: 5
slug: news_feed
---

A news feed shows each user the newest posts of the accounts they follow. When an account with two thousand followers posts "Landing in Tokyo" with a photo, the tweet should reach the top of all two thousand home timelines within seconds, and each follower expects the app to open on a page already merged from everyone they follow. Reads far outnumber posts, and the follower graph is wildly skewed: most accounts have a few hundred followers or fewer, the largest more than a hundred million. Three questions decide the design: whether to assemble a timeline when a tweet is written or when it is read, what to do about accounts with tens of millions of followers, and how to keep hundreds of millions of precomputed timelines in memory without paying for the ones nobody reads.

### Requirements

A user posts tweets of up to 280 characters with optional photos or video, replies to, retweets and likes tweets, and follows and unfollows accounts. The home timeline shows the tweets of everyone the user follows, newest first, with a ranked variant; the user timeline shows one account's own tweets. Both scroll back into older tweets, the home timeline can fetch what arrived since it was opened, and every tweet shows its like and retweet counts.

Assume 300 M daily and 500 M monthly active users. A timeline page is served in under 200 ms at the 99th percentile, and reading stays available, at 99.99 percent, even while posting is degraded. A new tweet reaches followers within five seconds, Twitter's own target, and its author sees it at once; beyond that, timelines are eventually consistent and counts may lag by seconds. An acknowledged tweet is never lost, while everything derived from tweets, cached timelines included, can be rebuilt. Search, trending topics (Chapter 23), direct messages (Chapter 6), notifications (Chapter 20), ads and moderation are out of scope.

### Estimates

```text
tweets      500 M per day / 86,400 s ≈ 5,800/s (peak ×3: 17,000/s)
reads       300 M DAU × 20 loads = 6 B/day ≈ 70,000/s (peak ×3: 210,000/s)
fan-out     × 100 cached followers per tweet ≈ 580,000 inserts/s (peak 1.7 M/s)
pull        70,000 reads/s × 200 followees = 14 M list reads/s, 24× the inserts
hydration   70,000 pages/s × 20 tweets = 1.4 M tweet lookups/s
home lists  800 entries × 32 B ≈ 25 KB per user × 500 M = 12.8 TB
            × 3 replicas ≈ 38 TB of RAM ≈ 300 servers of 128 GB
user lists  100 M monthly posters × 200 entries × 32 B ≈ 640 GB
tweets      500 M × 300 B = 150 GB/day ≈ 55 TB/year before replication
media       10% of tweets × 1 MB of renditions = 50 TB/day ≈ 18 PB/year
media out   70,000 pages/s × 2 images × 200 KB ≈ 28 GB/s ≈ 220 Gbps, via CDN
graph       500 M users × 200 follows = 100 B edges × 2 ways × 20 B ≈ 4 TB
```

The lines assume 20 timeline loads per daily user, 200 followees per user, and 100 cached timelines reached by an average tweet once celebrities are set aside. Precomputing timelines multiplies writes by a hundred, yet assembling them at read time would cost twenty-four times as much work, with a person waiting on two hundred lookups; the work belongs on the write side, where a queue can absorb it. The precomputed timelines fill 38 TB of RAM even holding only ids, only 800 per user and only for monthly actives, so memory is the main cost, and users who stop reading must stop costing it. Media outweighs text three hundred to one, so it lives in object storage behind a CDN, off the timeline path.

### API

```text
POST   /api/v1/tweets                            Idempotency-Key: <uuid>
       {"text": "Landing in Tokyo", "media_ids": ["7731"],
        "reply_to": null, "retweet_of": null}
       201 {"id": "2109577314195361797", "created_at": "2026-10-12T09:30:00Z"}
       400 text too long or unknown media        429 posting too fast
POST   /api/v1/media       201 {"media_id": "7731", "upload_url": "https://..."}
PUT    /api/v1/me/following/{user_id}     201, or 204 if already following
DELETE /api/v1/me/following/{user_id}     204
PUT    /api/v1/me/likes/{tweet_id}        201, or 204 if already liked
DELETE /api/v1/me/likes/{tweet_id}        204
GET    /api/v1/timelines/home?count=20&max_id=2109577304089870338
       200 {"tweets": [{"id": "...", "author": {...}, "text": "...",
            "media": [...], "likes": 1204, "retweets": 88}],
            "next_max_id": "2109572954907283455"}
GET    /api/v1/timelines/home?since_id=2109577314195361797    200 newer only
GET    /api/v1/users/{user_id}/tweets?count=20&max_id=...     200 same shape
```

Posting carries an Idempotency-Key, so a client that retries after a timeout gets its original tweet back. Follows and likes are PUT and DELETE on a resource named by the pair of ids, idempotent by construction: liking twice leaves one like. Media is uploaded first, straight to object storage through the pre-signed URL that the media call returns, so a tweet carries only media ids. Timelines page with cursors, never offsets: max_id continues from the cursor the previous page returned, and since_id fetches the tweets newer than the newest one shown, the pair of parameters Twitter's public API used. Ids travel as strings because a JavaScript number holds integers exactly only up to 2^53, which is why Twitter's API added an id_str field. The gateway authenticates every call and rate-limits posting.

### Data Model

```text
tweets         tweet_id PK (Snowflake) | author_id | text | media_ids
               | reply_to | retweet_of | created_at | deleted
               partitioned by hash(tweet_id), 3 replicas
by_author      (author_id, tweet_id DESC) PK          one account's tweets
following      (follower_id, followee_id) PK | created_at
followers      (followee_id, follower_id) PK | created_at   same edge reversed
likes          (tweet_id, user_id) PK | created_at          one like per user
counts         tweet_id PK | likes | retweets | replies     job-written only
home:{user}    Redis list of (tweet_id 8 B, author_id 8 B, flags 4 B),
               newest first, capped at 800, TTL 30 days renewed on read
user:{author}  Redis list of the author's newest 200 entries, TTL 30 days,
               refilled from by_author on a miss
media/{id}     object store, one blob per rendition, served by the CDN
```

Every access is a lookup by key or a short range scan, so tweets, the author index and the graph live in a partitioned wide-column store such as Bigtable or Cassandra. Tweets are partitioned by a hash of the id, not by its range, because Snowflake ids grow with time and range partitioning would send every new tweet to the last partition. The by_author index clusters an account's tweets by descending id, so a profile page or a followee's newest tweets is one range scan. The graph is stored twice, the way Twitter's FlockDB stored every edge in both directions: following serves rebuilds and the celebrity lookup, followers serves fan-out, each with a single-partition scan. The Redis lists are derived data, rebuildable from by_author and following, so losing them costs latency, never tweets. An entry holds the tweet id, the author id and four bytes of flags for retweets and replies, the layout Twitter used: 20 bytes instead of the kilobyte of a hydrated tweet.

### Architecture

```dot
rankdir=TB;
app     [label="mobile / web app", class=client];
cdn     [label="CDN", class=edge];
gw      [label="API gateway", class=edge];
blob    [label="object store\nmedia", class=store];
tl      [label="timeline service\nmerge, rank, hydrate"];
social  [label="graph service"];
post    [label="tweet service\nSnowflake ids"];
edges   [label="follow edges", class=store];
events  [label="events\nKafka", class=queue];
fanout  [label="fan-out\nworkers", class=worker];
counter [label="counter\njob", class=worker];
tcache  [label="tweet cache", class=cache];
home    [label="home timelines\nRedis", class=cache];
utl     [label="user timelines\nRedis", class=cache];
tweets  [label="tweet store", class=store];
app -> cdn [label=" media"];
app -> blob [label=" upload"];
cdn -> blob [label=" miss"];
app -> gw;
gw -> post [label=" post, like"];
post -> tweets;
post -> utl [label=" push"];
post -> events [style=dashed];
events -> fanout [style=dashed];
fanout -> social [label=" followers"];
fanout -> home [label=" LPUSHX"];
fanout -> utl [label=" backfill"];
events -> counter [style=dashed];
counter -> tweets [label=" counts"];
gw -> social [label=" follow"];
social -> edges;
social -> events [style=dashed];
gw -> tl [label=" read"];
tl -> home;
tl -> utl;
tl -> social [label=" followees"];
tl -> tcache;
tcache -> tweets [label=" miss"];
utl -> tweets [label=" miss"];
{rank=same; app; cdn}
{rank=same; gw; blob}
{rank=same; post; tl; social}
{rank=same; utl; tcache; home}
{rank=same; fanout; counter}
```

The write path starts at the app, which uploads any photo straight to the object store and posts the tweet through the API gateway to the tweet service. The tweet service mints a time-ordered Snowflake id (#145) in process, with no coordination. It writes the tweet to the tweet store, pushes the entry onto the author's list in user timelines, publishes an event to Kafka and answers 201. Fan-out workers consume the event, page through the author's followers from the graph service, and push the entry onto each follower's list in home timelines with LPUSHX, trimming it to 800 with LTRIM. Likes go through the tweet service too, a retweet being just a tweet with retweet_of set, and the counter job folds their events into the counts table of the tweet store. A follow goes to the graph service, which writes both directions of the edge to the follow edges store and publishes a follow event; a fan-out worker then backfills the follower's cached timeline with the followee's latest entries from user timelines, and an unfollow strips that author's entries.

The read path enters through the same gateway. The timeline service reads the user's list from home timelines, asks the graph service which followees are celebrities, an answer it caches for a minute, and takes their newest entries and the user's own from user timelines, which fall through to the by_author index of the tweet store on a miss. It merges the lists, ranks them if the user chose the ranked timeline, and hydrates a page of twenty with one multi-get to the tweet cache, which falls through to the tweet store. Media URLs point at the CDN, which fetches from the object store on a miss. A user with no list in home timelines gets one rebuilt, as the second deep dive explains.

### Deep Dives

#### Fan-out on write, fan-out on read, and the celebrity hybrid

Fan-out on read is the natural first design, the one Design Twitter (#46) builds: keep each author's tweets in time order and, when a user opens the home timeline, merge the newest tweets of everyone they follow with a heap, the k-way merge of #20. Writes are trivial and nothing is stored twice. Reads are the problem: 14 M list reads a second, every page waiting on the slowest of two hundred lookups on different machines, and the same merge recomputed on every refresh.

Fan-out on write does the merge once, at posting time, by pushing each new entry onto the cached timeline of every follower. A read becomes one Redis lookup plus hydration, and the cost moves to 580,000 inserts a second, but asynchronous ones, which Kafka buffers, workers batch per Redis shard, and nobody waits for as long as they land within five seconds. Push breaks only at the top of the follower distribution. A tweet from an account with 100 M followers is 100 M inserts, about a minute of the whole fleet's peak capacity; Twitter's engineers reported that a tweet from Lady Gaga could take up to five minutes to reach her 31 million followers.

The hybrid pushes for ordinary accounts and pulls for celebrities. Accounts above a threshold, say a million followers, are not fanned out, and their tweets reach only their own list in user timelines. At read time the timeline service merges the reader's cached list with the lists of the celebrities they follow and with the reader's own list, a k-way merge of a few dozen sorted lists instead of two hundred. Twitter described moving to exactly this. The merge orders by id, after sorting each list because concurrent workers can land entries slightly out of order, and that is correct only because a Snowflake id carries its timestamp in the high bits; #46 rightly warns against ordering by ids that are mere labels. Merging the reader's own list also gives read-your-writes for free.

The pulled lists are the hottest keys in the system, so every timeline server holds them in its own memory, refreshed each second: even 100,000 accounts above the line, at 100 entries of 20 bytes, come to 200 MB. The threshold is a dial. An account's cost is its follower count times its posting rate, so the rule weighs both, with hysteresis, entering the pull set at a million followers and leaving it below 800,000 so that an account near the line does not flap. Switching needs no migration: the graph service updates its in-memory celebrity set, a tweet both pushed and pulled is dropped as a duplicate id, and an account leaving the set stays pulled for a few days, until pushed tweets have replaced its pulled ones.

#### Timelines only for the people who read them

Fan-out on write buys latency with memory: 38 TB of RAM even with 20-byte entries, Twitter's cap of 800 entries and three replicas, and a timeline kept for someone who never opens the app is pure waste. Twitter cached timelines only for users who had logged in within the last 30 days, and two Redis primitives make that policy run itself.

Each home key carries a 30-day time-to-live that the timeline service renews on every read, a cache with expiring keys (#94) whose deadline only reads move. Fan-out cannot keep a timeline alive, because Redis leaves a key's TTL untouched when a command such as LPUSH merely adds to the list, and fan-out writes with LPUSHX, which pushes only when the list already exists. Once a timeline expires, every tweet aimed at that follower is a no-op costing a round trip and no memory, and no worker ever asks who is active.

A returning user misses and gets a rebuild, fan-out on read performed once: the timeline service fetches the followees from the graph service, takes each one's newest entries from user timelines and merges them with the heap of #20 until it has 800, about two hundred small reads and tens of milliseconds. The first page comes straight from the merge, and the list is written to Redis for the rest. The rebuild starts when the user signs in or opens the app, so it is usually done before the feed is requested. One race needs care: a tweet fanned out during the rebuild would meet a missing key and vanish. So the rebuild first creates the list holding a placeholder, letting LPUSHX land new tweets from that moment, then appends the merged history behind them and removes the placeholder; a tweet that arrives both ways is dropped as a duplicate.

#### Building a page: cursors, hydration, counts and ranking

Offsets cannot page a timeline: new tweets arrive at the head while a user reads, so "skip twenty" would repeat the bottom of page one on page two. The cursor is the id of the last tweet shown; the next page asks for ids below it, and the new-tweets banner for ids above the newest. Snowflake ids are unique and time-ordered, so the cursor survives any number of insertions and needs no server state. The cached timeline ends after 800 entries, and Twitter's API stopped there too.

Hydration turns ids into tweets. At 1.4 M lookups a second it needs a memcached tier keyed by tweet id, holding the last three days of tweets, about 450 GB, plus older ones still being read; a page is one multi-get sent in parallel to the servers that own its ids. The same step drops deleted tweets and those from blocked or muted accounts, and folds several retweets of one tweet into a single entry. Filtering here is what makes a delete cheap: mark the row deleted, evict the cached copy, and every timeline still holding the id skips it, with no fan-out of deletions.

Counts are derived, never incremented in place. A like writes its (tweet_id, user_id) row and publishes an event, and the counter job sums events per tweet and writes each count every few seconds, so a viral tweet taking 50,000 likes a second costs the counts table one write per interval. The cache keeps counts under their own key with a TTL of a few seconds. Chapter 50 takes counting at this scale further.

Ranking reorders this backbone. The merged in-network entries and out-of-network candidates, whose generation Chapter 47 covers, are scored by a model that predicts engagement from features such as the reader's affinity to the author, the tweet's age and how fast it is gathering likes, and a size-k heap (#19) keeps the best few hundred as a ranked snapshot stored in home timelines for the session. Twitter's 2023 description of its For You timeline drew about 1,500 candidates per request, roughly half from accounts the reader follows. A ranked order is not monotonic in id, so its cursor is an opaque token into the snapshot, and pages neither repeat nor skip tweets as scores change.

### Scaling and Bottlenecks

The fan-out tier breaks first, because bursts outrun averages: Twitter's record, 143,199 tweets in one second during a 2013 broadcast of Castle in the Sky in Japan, was twenty-five times its average of 5,700, and every tweet is multiplied again by its followers. Kafka absorbs the burst, the stateless fan-out workers scale out on consumer lag and batch hundreds of inserts into each Redis round trip, and an account just below the celebrity line has its followers split into chunks that several workers process in parallel. Under the worst burst, delivery stretches from seconds to a minute, and nothing is lost.

The home timeline cluster shards by user id with consistent hashing (#139), and resharding it is unusually cheap: a moved timeline need not be copied, because the rebuild path recreates it on the next read. A viral tweet's reads are absorbed by the tweet cache, its hottest entries also held in each timeline server's memory for a second or two. The hundred-million-row follower lists of the biggest accounts are never read by fan-out at all. Across regions, each region holds replicas of the tweet and graph stores and runs its own fan-out into its own timeline cache, fed by the replicated event stream, so a reader is served entirely by the nearest region.

### Failure Modes

A failed Redis node is covered by the two other replicas of its lists. If all three copies of a shard are lost, its users are rebuilt on their next read. Losing much of the cluster at once is the dangerous case, because millions of rebuilds would hammer the graph service and user timelines, so rebuilds pass an admission limit, and users still waiting get a smaller merge of a few dozen followees.

If fan-out stalls, tweets wait in Kafka, which keeps days of events, so timelines go stale but nothing is lost. If the tweet service crashes between storing a tweet and publishing its event, the client's retry with the same idempotency key finds the tweet and publishes again; publishing from the store's change stream would also cover clients that never retry, and pages drop duplicate ids either way. An unreachable tweet store partition costs a page only the tweets it holds, because hydration returns what it found. If the graph service is down, fan-out pauses and follows fail, but reads continue from cached timelines with the last known celebrity answer. And a celebrity's burst of tweets, the classic failure of pure push, costs the hybrid one list push per tweet.

### Trade-offs and Alternatives

Push or pull trades write amplification and memory against read latency, and the shape of the follower graph decides. Facebook's news feed went the other way: its Multifeed design keeps recent actions on in-memory leaf servers and has aggregators fetch, rank and merge candidates at read time, which suits a feed that is ranked anyway and a friend graph whose degree is capped. A product whose posts are mostly unread, or whose every read is ranked from scratch, should pull; Twitter's skew needs the hybrid, with the threshold sliding it between the two.

Storing ids rather than tweets keeps entries at 20 bytes and makes a delete one write, at the price of hydration on every read. The 800-entry cap and the 30-day horizon trade deep scrolling and a returning user's first second against tens of terabytes of RAM. A chronological timeline is cheap and trivially paged; a ranked one engages more but costs a model evaluation per candidate and a stateful cursor.

### What Interviewers Probe

Expect six questions. Why not build the timeline at read time? Because 14 M list reads a second is twenty-four times the cost of fan-out, and every page would wait on its slowest lookup. What about celebrities? Pull them at read time above a threshold weighted by posting rate, with hysteresis. How much memory do timelines take? About 38 TB with ids only, 800 entries and three replicas, which is why inactive users get none. How do you paginate? With an id cursor that relies on Snowflake ids being time-ordered, and a snapshot token once the feed is ranked. What happens on follow and unfollow? A follow event backfills the followee's recent entries and an unfollow strips them, cheap because every entry carries its author id. How do counts survive a viral tweet? Likes are rows, counts are aggregated asynchronously, and the hot row takes one write every few seconds.

Strong candidates raise four more points unprompted: the TTL and LPUSHX pair that makes inactive users free, the race between a rebuild and fan-out, the celebrity lists as the hottest keys and therefore held in every timeline server's memory, and the author seeing their own tweet at once with no special write. Interviewers rarely care which queue or database you name. They care that the work happens where nobody is waiting, and that you know which accounts break that rule.

*Algorithms:* #46 Design Twitter · #20 Merge K Sorted Arrays · #145 Unique ID Generator · #19 Top-K Elements · #94 Cache with Expiring Keys · #139 Consistent Hashing
