---
rank: 8
slug: video_platform
---

A video platform accepts a file from anyone with a camera and plays it back to anyone with a screen. A creator's phone uploads a ten-minute, 750 MB vlog over a patchy connection; minutes later one viewer watches it at 360p on a train and another at 1080p on a television, both starting within a couple of seconds. The upload side is a batch-processing system and the watch side a content delivery problem measured in tens of terabits a second. Three questions decide the design: how to get gigabytes in over a connection that keeps dropping, how to turn one upload into a dozen streamable renditions fast enough at 500 hours of video a minute, and how to let every player pick the best quality its network can sustain without stalling.

### Requirements

A creator uploads a video of up to 256 GB or 12 hours, the limits YouTube sets, from a browser or a phone, and the upload survives dropped connections and app restarts. They set a title, a description and a visibility (public, unlisted or private), and the platform turns the file into streamable renditions and publishes it. A viewer watches on any device and network, with a quick start, quality that adapts to the connection, and seeking. Every video shows a view count, and a channel page lists a creator's uploads.

Take the scale YouTube has published, 500 hours uploaded a minute and a billion hours watched a day, and assume 5 billion views a day. Playback starts in under two seconds for most viewers and rarely stalls, and watching stays available at 99.99% even when uploading or processing is down. An acknowledged upload is never lost. A ten-minute video is watchable within minutes at standard definition, with HD and 4K following, as on YouTube. View counts may lag by a minute or two and are approximate until a daily recount. Recommendations (Chapter 47), live streaming (Chapter 32), comments and likes (Chapter 50), search, ads and DRM (Chapter 9) are out of scope.

### Estimates

```text
uploads     500 h of video per minute = 30,000 s of video every second
videos      720,000 h/day at 10 min each ≈ 4.3 M uploads/day ≈ 50/s
ingest      30,000 s/s × 10 Mbps source = 300 Gbps ≈ 3.2 PB/day of originals
ladder      144p to 1080p at 0.1, 0.3, 0.6, 1.2, 2.5, 5 Mbps ≈ 10 Mbps, H.264
renditions  + VP9 at ≈ 0.6× the bits ≈ 15 Mb per second of video ≈ 4.9 PB/day
storage     ≈ 8 PB/day ≈ 3 EB/year; erasure coded at 1.5× ≈ 4.4 EB/year raw
transcode   assume 20 core-s per second of video → 600,000 cores, always busy
watching    1 B h/day over 24 h ≈ 42 M concurrent streams (evening peak ×2)
egress      42 M × 2 Mbps average ≈ 84 Tbps (peak ≈ 170 Tbps)
segments    4 s each → 42 M streams / 4 s ≈ 10 M requests/s of ~1 MB each
origin      caches serve 95% → origin sends 5% of 84 Tbps ≈ 4 Tbps
views       5 B/day ≈ 58,000 view events/s (peak ≈ 115,000/s)
metadata    4.3 M videos/day × 2 KB ≈ 9 GB/day ≈ 3 TB/year
```

Three numbers drive the design. Egress, 84 Tbps on average and twice that at peak, is nearly 300 times the ingest, so delivery must come from caches near viewers, where every point of hit ratio is worth about 0.8 Tbps of origin traffic. Storage grows by 3 EB a year and is kept forever, so cost per byte decides where each byte lives. Transcoding keeps 600,000 cores busy, which makes it a fleet-wide batch system with priorities; Google even built its own transcoding chip, Argos, for YouTube. The metadata, a few terabytes a year behind a cache, and the view events, a modest stream, are hard only where one video is hot.

### API

```text
POST /v1/uploads                                   Idempotency-Key: <uuid>
     {"title": "...", "bytes": 750000000, "part_bytes": 8388608}
     201 {"video_id": "q3Vf8kLm2Xa", "upload_id": "u-91x", "parts": 90,
          "urls": ["https://store.../u-91x/1?expires=...&sig=...", ...]}
PUT  <part url>                   body: one part, Content-MD5: <part hash>
     200 ETag: "<etag>"             403 URL expired → ask for fresh URLs
GET  /v1/uploads/{upload_id}
     200 {"received": [1, 2, 3, 5], "urls": {"4": "...", "6": "..."}}
POST /v1/uploads/{upload_id}/complete
     202 {"video_id": "q3Vf8kLm2Xa", "status": "processing"}

GET  /v1/videos/{video_id}
     200 {"title": "...", "status": "ready", "duration_s": 612,
          "views": 18234, "manifest": "https://cdn.../master.3.mpd?tok=..."}
     404 unknown or private            451 blocked in this country
GET  <cdn>/v/{video_id}/{rendition_id}/{n}.m4s     200, immutable, cached
POST /v1/views  {"video_id": "...", "session": "...", "played_s": 30}  202
GET  /v1/channels/{channel_id}/videos?cursor=...   200 {"items", "next"}
```

Video bytes never touch the API servers: each part's pre-signed URL carries a signature over the bucket, key, part number and expiry that the object store verifies itself. The `Idempotency-Key` makes a retried create return the same video, a re-sent part simply overwrites itself, and complete is safe to repeat. An expired URL (403) or a restarted app calls `GET /v1/uploads/{id}`, which lists the parts already stored and issues fresh URLs for the rest; that is the whole resume mechanism. Complete answers 202 because processing has only begun. The metadata call enforces visibility (404 for a private video, 451 Unavailable For Legal Reasons for a region block) and returns a manifest URL with a short-lived signed token, which edges verify without calling the origin and leave out of the cache key (Chapter 15). The view beacon answers 202 because it is counted later, and channel listings page with an opaque cursor.

### Data Model

```text
videos       video_id PK (64 random bits, 11 chars) | channel_id | title
             | description | duration_s | visibility | status | manifest_v
             status: uploading, processing, ready, failed, blocked
             sharded by hash(video_id), cached by video_id
by_channel   (channel_id, created_at) PK → video_id            channel page
renditions   (video_id, rendition_id) PK | codec | height | kbps | tier
uploads      upload_id PK | video_id | bytes | part_bytes | expires_at
tasks        (video_id, task_id) PK | dependents | waiting_on | state
             | priority | attempts | lease_owner | lease_until
view_counts  video_id PK | views | updated_at     written by the aggregator
objects      orig/{video_id}                          original, cold class
             v/{video_id}/{rendition_id}/{n}.m4s      segments, immutable
             v/{video_id}/master.{manifest_v}.m3u8 | .mpd   manifests
```

The metadata is small, relational and read-heavy, so a sharded relational store fits: YouTube built Vitess in 2010 to shard MySQL for this kind of data, and Spanner would serve as well. Hot reads are by `video_id`, so rows shard by its hash, and channel pages read `by_channel` instead of scattering over every shard. Ids are 64 random bits in eleven URL-safe base64 characters, the shape of YouTube's own ids, and they are random rather than counted because an unlisted video is protected only by its id being unguessable. A decade of uploads, 16 billion ids in a space of 1.8 × 10^19, collides only a handful of times, and a conditional insert turns each collision into a retry. The tasks table shares its video's shard, so finishing a task and releasing its dependents is one local transaction, with compare-and-set on the lease; view counts live apart so that a viral counter never contends with metadata writes. Segment paths are deterministic, so a rerun task simply overwrites its own unpublished output, and a published URL never changes. Adding HD or a codec writes a new master manifest under the next `manifest_v` and repoints the row, so no cache ever mixes two encodes.

### Architecture

```dot
rankdir=TB;
watch    [label="watch API"];
edgec    [label="edge cache\nin ISPs", class=edge];
creator  [label="creator app", class=client];
vev      [label="view events", class=queue];
upev     [label="upload\nevents", class=queue];
viewer   [label="viewer app\nABR player", class=client];
workers  [label="transcode\nworkers", class=worker];
meta     [label="metadata DB", class=store];
sched    [label="DAG scheduler"];
counts   [label="view counts", class=store];
orig     [label="originals\nstore", class=store];
agg      [label="view\naggregator", class=worker];
regional [label="regional\ncache", class=edge];
segs     [label="segment store\nhot / warm / cold", class=store];
mcache   [label="metadata\ncache", class=cache];
upapi    [label="upload API"];
tier     [label="tiering job", class=worker];
upapi -> meta [label=" video row"];
vev -> agg -> counts;
viewer -> watch [label=" metadata,\nviews"];
sched -> workers [dir=both, label=" lease tasks"];
workers -> orig [label=" read source", constraint=false];
upapi -> upev [style=dashed, label=" uploaded"];
regional -> segs [label=" miss"];
workers -> segs [label=" write\nsegments"];
watch -> mcache [label=" 1. get"];
watch -> vev [style=dashed, label=" view event"];
viewer -> edgec [label=" manifest,\nsegments"];
upev -> sched;
watch -> counts [label=" count", constraint=false];
creator -> orig [label=" PUT parts"];
tier -> sched [label=" re-encode", constraint=false];
watch -> meta [label=" 2. on miss"];
agg -> tier [style=dashed, label=" hot videos"];
creator -> upapi [label=" start,\ncomplete"];
tier -> segs [label=" move tiers"];
edgec -> regional [label=" miss"];
sched -> meta [label=" tasks, ready", constraint=false];
upapi -> orig [label=" open,\nassemble"];
{rank=same; creator; viewer}
{rank=same; upapi; watch; edgec}
{rank=same; upev; vev}
{rank=same; workers; counts; tier}
```

The upload path starts at the creator app, which asks the upload API to start an upload. The API writes a video row to the metadata DB, opens a multipart upload in the originals store and returns the part URLs. The app PUTs the parts straight into the originals store, then calls complete; the upload API has the store assemble the parts, marks the row processing and publishes on the upload events topic. The DAG scheduler consumes the event, writes the video's task graph into the metadata DB and leases ready tasks to transcode workers, which read their slice of the source from the originals store and write segments, playlists and thumbnails to the segment store. When the standard-definition tasks finish, the scheduler records the renditions in the metadata DB and marks the video ready; HD and the second codec follow as new manifest versions.

The watch path starts at the viewer app. The watch API reads metadata from the metadata cache, falling back to the metadata DB, adds the count from view counts and returns a signed manifest URL. The ABR player fetches the manifest and segments from an edge cache inside the viewer's ISP, a tier Google runs as Google Global Cache; the edge fills misses from a regional cache, which fills from the segment store.

Once a playback qualifies as a view, the player sends a beacon to the watch API, which publishes it on the view events topic. The view aggregator, a stream job, folds those events into per-minute increments written to view counts in batches, and flags videos that are turning hot. The tiering job moves their renditions between the hot, warm and cold classes of the segment store and asks the DAG scheduler to re-encode those whose audience justifies an expensive codec.

### Deep Dives

#### Uploading gigabytes over a connection that drops

The naive upload is one POST of the whole file to an API server. Over a 10 Mbps uplink the 750 MB file takes ten minutes, and one dropped connection, a tunnel or a hand-over from Wi-Fi to cellular, throws it all away; a 50 GB file would need eleven unbroken hours. The API fleet would also carry all 300 Gbps of ingress in some 30,000 long-lived requests, which every deploy would kill.

Instead, split the file into 8 MiB parts, so that a failure costs one part, under seven seconds of sending. Send each part directly to the object store through its pre-signed URL, so that ingest scales with the store rather than the API and a fast link can push several parts at once. And make the server the source of truth for progress: the store records each part that arrived, checked against the client's Content-MD5 hash, so corruption is caught part by part and resuming after any interruption is one call that lists what is missing. On complete the store assembles the parts, and the API checks the total size against the create call.

The cost is bookkeeping. S3-style multipart uploads need parts of at least 5 MiB, except the last, and allow at most 10,000 of them, so the part size grows with the file: a 256 GB upload needs parts of about 26 MB. Abandoned parts occupy storage until a lifecycle rule aborts multipart uploads left incomplete for a few days, and a janitor fails the matching video rows.

#### Transcoding as a DAG of chunk tasks

The naive pipeline gives one worker the whole file and one long ffmpeg command that writes every rendition in turn. A ten-minute video waits for one machine to encode twelve ten-minute renditions, an hour of 4K takes many hours, a crash at 90% starts over, and short videos queue behind long ones.

Split the work along time and along renditions instead. A probe task reads the codecs, duration and frame rate and rejects files that do not decode. A split task cuts the timeline into one-minute chunks on the 4-second segment grid, and each pair of chunk and rendition becomes one encode task. Every encoder forces a keyframe at each 4-second boundary, so all renditions break at the same instants, which is what lets a player switch between them. Audio is encoded separately and shared by every rendition. A package task per rendition joins its chunks into CMAF segments, fragmented MP4 that both HLS and DASH accept, and publish writes the master manifests. Thumbnails, the copyright match (YouTube's is Content ID) and the safety classifiers branch off the probe and gate publish.

```text
probe → split ─┬→ encode chunk 1 × 12 ─┐
  │            ├→ encode chunk 2 × 12 ─┼→ package × 12 ─┐
  │            └→ encode chunk k × 12 ─┘                │
  ├→ encode audio ──────────────────────────────────────┤
  ├→ thumbnails ────────────────────────────────────────┼→ publish
  └→ copyright and safety checks ───────────────────────┘
```

The scheduler runs the graph with Kahn's algorithm (#40): each task counts the unfinished tasks it waits on, tasks at zero are ready, and finishing one decrements its dependents and releases those that reach zero. Ready tasks enter the job scheduler's priority queue (#149), and workers lease them, extending the lease while they work; if a worker dies, the lease lapses and another worker takes the task. Execution is therefore at least once, which is safe because tasks write to deterministic paths. A task that fails three times fails the video, since a file that crashes the encoder tends to crash it every time.

A ten-minute video becomes 10 × 12 = 120 encode tasks that run in parallel and finish in about the time of one chunk. With the other tasks that is about 6,500 tasks a second across all uploads, so the scheduler's state is sharded by video id (Chapter 30). A straggler that runs far longer than its siblings gets a speculative duplicate, the backup-task trick of MapReduce. Priorities run a fresh upload's standard-definition path first, its HD and VP9 renditions next, and backfills last, on spare capacity. The price of chunking is a little compression, because each chunk restarts the encoder's rate control and look-ahead; minute-long chunks keep that small.

#### Adaptive bitrate: aligned segments and a player that chooses

The naive player downloads one MP4 at one quality: 1080p stalls on a 3 Mbps connection, 360p looks poor on a television, and a mobile link that changes speed gets no adjustment at all. The server cannot choose for it either, because only the player knows how full its buffer is and how fast its last download arrived.

Adaptive bitrate streaming moves the choice into the player. Each rendition is cut into 4-second segments, and because keyframes were forced on the same grid, segment n of every rendition covers the same four seconds and starts with a keyframe. A manifest, either an HLS master playlist pointing to one media playlist per rendition or a DASH MPD with one Representation per rendition, lists each rendition's bandwidth, resolution, codec and segments. The player picks a rendition for every segment, and a switch at a boundary is seamless.

```text
  time   0 s      4 s      8 s      12 s     16 s
 1080p   │K·······│K·······│K·······│K·······│
  720p   │K·······│K·······│K·······│K·······│
  360p   │K·······│K·······│K·······│K·······│
player      360p  →  720p  → 1080p  →  720p     K = keyframe
```

Two signals drive the pick. A throughput rule takes the highest rendition below a safety margin of the measured download rate; it reacts fast but chases noise and oscillates. A buffer rule picks from how many seconds are already buffered; it is stable but blind at start-up. The reference DASH player, dash.js, uses its throughput rule at start-up and after a seek and switches to BOLA, a buffer-based rule, once the buffer is healthy. Players start at a modest rendition so that the first segment arrives quickly, and step down early rather than stall.

Segment length is the dial. Two-second segments adapt and start faster but double the requests and, since each opens with a keyframe, cost compression; six-second ones do the opposite, and this design takes four.

### Scaling and Bottlenecks

Egress breaks first, and only the edge can absorb it. The hot set is easy: a premiere is about a gigabyte of renditions requested by millions, and request coalescing turns its simultaneous misses into one upstream fetch per layer (Chapter 4). The long tail is hard, because if every first request were cached, one-hit wonders would evict the hot set. So an edge admits a segment only on its second request, remembering first requests in a Bloom filter (#146), and evicts the least recently used segments (#44). Unlike a Netflix catalogue (Chapter 9), billions of user videos are too unpredictable to pre-position, so this design caches on demand and pre-warms only obvious hits.

Storage grows by 3 EB a year, so cost per byte rules it. Popularity is skewed and fades with age, so the tiering job keeps segments of recent and popular videos on replicated fast storage, erasure codes everything else on dense disks at 1.5 times its size instead of three copies (Chapter 33), and holds originals in a cold class for future re-encodes.

Counting views is the classic hot-key problem: a database increment per view fails on the video everyone is watching, whose single row would take tens of thousands of increments a second. Instead view events are partitioned by session rather than by video, so a viral video spreads over every partition, and each aggregator task drops bots and repeated sessions and writes one increment per video per minute; a video drawing 50,000 views a second costs a hundred writes a minute across a hundred tasks instead of three million. Counts lag by a minute, and a daily recount from the archived events corrects them, which is why a displayed count can occasionally drop. Tiering needs hotness per region over the last hour, which comes from a count-min sketch (#147) with a small heap of top entries (#19): fixed memory, one pass, and an error that only overestimates, so at worst a lukewarm video is promoted early (Chapter 23 builds the sketch).

### Failure Modes

A transcode worker that dies loses only its lease, and its task reruns over the same objects. A poison file that crashes or hangs the decoder exhausts its retries and fails the video with a reason for the creator; because media files are untrusted input to complex decoders, workers run sandboxed, with access to nothing but the stores. A failed scheduler is replaced by a standby that reads all of its state from the tasks table. If processing falls behind, uploads still succeed, since originals are durable once complete returns; priorities keep fresh standard-definition encodes moving while backfills pause.

Playback degrades gracefully because caches serve nearly all of it. If a region's segment store is down, edges keep serving what they hold and misses fail over to another region's replica. A failed edge is routed around by DNS, and the player retries a failed segment on another host. While a metadata shard fails over to a replica, its videos stay readable from the cache, and only uploads, edits and processing on that shard wait. A stalled view pipeline freezes the counts, which catch up from the topic's retained log; playback never waits on counting.

### Trade-offs and Alternatives

The biggest dial is how much to encode up front. The full ladder in two codecs for every upload spends compute on videos nobody watches; encoding on first request saves it but makes the first viewer wait. This design takes the middle: a standard ladder for everything; AV1 only for videos that earn it, since an expensive codec costs its compute once and saves bandwidth on every view; and, for the coldest videos, rarely used renditions dropped and regenerated on demand. Netflix's per-title encoding tunes the ladder to each title, which pays for thousands of titles watched millions of times (Chapter 9) but not for four million uploads a day. H.264 plays everywhere, while VP9 and AV1 need noticeably fewer bits but cost far more to encode and are not decoded by every device, so the manifest offers several codecs.

Separate segment files are the simplest to cache, but a ten-minute video in twelve renditions is 1,800 objects, nearly 8 billion a day. Storing each rendition as one fragmented MP4 addressed by byte range, which DASH's SegmentBase and HLS's EXT-X-BYTERANGE both support, cuts that to twelve, at the price of range-aware caching. For uploads, Google's resumable upload protocol tracks a single committed byte offset rather than a set of parts, which is simpler state but limits an upload to one connection. And view counts are approximate because they are a display; billed views, like ad impressions, must be counted exactly once (Chapter 28).

### What Interviewers Probe

Expect six questions. How do you upload a 10 GB file from a phone? In parts, straight to the object store through pre-signed URLs, resuming by listing the parts received. Why not transcode on one machine? A DAG of chunk-by-rendition tasks finishes in the time of the slowest chunk and survives crashes task by task. How does the player switch quality without a glitch? Keyframe-aligned segments on a shared grid, chosen by throughput and buffer. How soon is a new video watchable? Within minutes, at standard definition first. How do you deliver 170 Tbps? From caches inside ISPs, with immutable URLs and an admission filter against the long tail. How do you count views on a viral video? Session-partitioned events aggregated per minute and reconciled later.

Strong candidates add four points unprompted: uploaded media is hostile input, so decoders run sandboxed; unlisted videos depend on unguessable ids; versioned, immutable URLs remove cache invalidation from the problem; and the real constraints are egress and storage cost, which is why codecs and tiers follow popularity.

*Algorithms:* #149 Job Scheduler · #40 Kahn's Algorithm · #147 Count-Min Sketch · #19 Top-K Elements · #146 Bloom Filter · #44 LRU Cache
