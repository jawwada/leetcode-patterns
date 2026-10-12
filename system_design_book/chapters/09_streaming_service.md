---
rank: 9
slug: streaming_service
---

A subscription streaming service such as Netflix lets a member press Play on any title of a curated catalog and watch at once, at the best quality the connection and the screen allow. Unlike the video platform of Chapter 8, whose long tail of uploads nobody can forecast, Netflix knows every title it serves and can predict what each region will watch tomorrow. So the cloud runs only the control plane, and the video comes from Netflix's own CDN: appliances installed inside internet providers' networks. Three questions decide the design: how to place the right files on those appliances before anyone asks, how to steer each play to an appliance that holds them, and how to get from Play through a DRM license to the first frame within two seconds.

### Requirements

A member picks a profile, browses rows of titles and presses Play on a TV, phone or browser. Playback resumes where any of the account's devices stopped, offers audio and subtitles in many languages and adapts its quality to the network. A title plays only where and while it is licensed, the plan caps resolution and simultaneous streams, and a new season goes live at a fixed minute, often worldwide.

Assume 250 M accounts watching two hours a day, peaking at about 40 M concurrent streams in the evening. Playback must start within two seconds for 95% of plays, with rebuffering well under 1% of viewing time. Every play needs the control plane, so it must reach 99.99% availability and survive the loss of a cloud region; the data plane must survive any appliance or site failing with at worst a brief dip in quality. Studios require hardware-backed DRM and protected video outputs for HD and 4K. Bookmarks may lag by a minute, but rights and stream limits are checked on every play, and the origin must never lose a master or an encode. Recommendations (Chapter 47), billing, offline downloads and live events (Chapter 32) are out of scope.

### Estimates

```text
viewing      assume 250 M accounts × 2 h a day = 500 M hours a day
concurrency  500 M h / 24 h ≈ 21 M streams on average; evening peak ×2 ≈ 40 M
egress       40 M streams × 4 Mb/s average ≈ 160 Tb/s at the global peak
per day      500 M h × 3,600 s × 4 Mb/s ≈ 7 × 10^18 bits ≈ 0.9 EB a day
appliance    assume 100 TB of storage and 100 Gb/s ≈ 25,000 streams at 4 Mb/s
fleet        160 Tb/s / (100 Gb/s × 80% target load) ≈ 2,000 appliances' worth
catalog      50,000 hours × ~50 GB for all encodes of an hour ≈ 2.5 PB
one site     3 appliances = 300 TB ≈ 12% of the catalog, chosen by popularity
nightly fill 2% of 300 TB = 6 TB in an 8-hour window ≈ 1.7 Gb/s
offload      the site averages 100 Gb/s ≈ 1.1 PB served a day per 6 TB filled
play starts  assume 1 B a day ≈ 12,000/s; peak ×2 ≈ 23,000/s
bookmarks    40 M streams × one position write every 60 s ≈ 670,000 writes/s
```

Egress dominates. Pushing 160 Tb/s, about an exabyte a day, out of a few cloud regions through transit providers makes no sense; it has to be served from inside the viewers' own networks. That is about 2,000 appliances' worth of throughput, and since every site is sized for its own evening peak and keeps spares, the real fleet is far larger: a decade into the programme, Netflix reported 18,000 servers in 6,000 locations across 175 countries. Storage is the opposite constraint. The catalog is a few petabytes and a small site holds an eighth of it, so each site's contents must be chosen. Fill is a rounding error that can wait for idle hours, and in the control plane bookmark writes outnumber play starts thirty to one.

### API

```text
POST /v1/playback/manifest                      Authorization: Bearer <token>
     {"title_id": 81234567, "profile_id": "p42", "device_id": "d9",
      "caps": {"codecs": ["av1", "hevc"], "drm": "widevine-L1", "hdcp": "2.2"}}
     200 {"session": "<signed token>", "resume_ms": 1834000,
          "video": [{"codec": "av1", "kbps": 3100, "res": "1080p",
                     "key_id": "k-hd",
                     "urls": ["https://a12.isp.example/...",
                              "https://ix-fra3.example/..."]}],
          "audio": [...], "subtitles": [...]}
     403 title not licensed in this country    409 plan's stream limit reached

POST /v1/playback/license
     {"session": "<signed token>", "challenge": "<CDM license request>"}
     200 {"license": "<keys sealed for this CDM, plus policy>"}
     403 security level or output protection too low for the keys asked

GET  https://a12.isp.example/<file_id>?t=<signed token>   Range: bytes=0-65535
     206 Partial Content    403 bad or expired token    404 file not here

POST /v1/playback/events  {"session": "...", "type": "heartbeat",
                           "position_ms": 1894000}               204 No Content
```

The manifest call carries the device's capabilities, so the server can choose codecs, resolutions and keys, and it returns several ranked URLs per file, so the client can fail over without asking again. Sessions are keyed by device, so a retry replaces that device's session instead of counting a second stream. The signed session token lets the license service trust its claims (account, title, country, highest allowed resolution) without a lookup. Appliances know nothing about members; they check each URL's token, signed with a key they share with the control plane, locally. That token protects bandwidth, not content: the bytes are ciphertext, and only a license opens them.

### Data Model

```text
titles      title_id PK | kind | season, episode | names, art by locale
rights      (title_id, country) PK | starts_at | ends_at | max_quality
streams     (title_id, stream_id) PK | codec | res | kbps | file_id | key_id
files       file_id PK | bytes | sha256 | origin_path   (a few million rows)
            catalog tables: replicated to every region, read from memory
keys        key_id PK | content key wrapped by a master key
            readable only by the license service
viewing     (profile_id, title_id) PK | position_ms | updated_at
sessions    (account_id, device_id) PK | title_id | TTL 2 min, kept alive by
            heartbeats; both in Cassandra, partitioned by the first key
appliances  appliance_id PK | cluster_id | prefixes | health | files_held
placement   (cluster_id, file_id) PK | appliance_ids     rebuilt every night
```

The catalog tables are small, read on every play and changed only when encodes or contracts arrive, so they are replicated to every region and served from memory. Streams and files are immutable, and a re-encode gets a new file id, so appliances keep files for weeks with no invalidation at all. Keys live apart from everything else, because one leaked content key unlocks a title on every appliance in the world. Positions and sessions carry the write load and go to Cassandra (Chapter 3), partitioned by profile and by account: a resume or a stream count reads one partition, a heartbeat overwrites one row, and the TTL ends a crashed device's session by itself. Cache control owns the appliance and placement tables, and placement is regenerated every night, never edited.

### Architecture

```dot
rankdir=TB;
app     [label="TV / phone app", class=client];
subgraph cluster_cloud {
  label="control plane: cloud, three regions";
  style="rounded,dashed"; color="#9CA3AF";
  gw      [label="API gateway", class=edge];
  encode  [label="encoding\npipeline", class=worker];
  play    [label="playback\nAPI"];
  lic     [label="license\nservice"];
  keys    [label="key store", class=store];
  origin  [label="origin\nobject store", class=store];
  catalog [label="catalog\nand rights", class=store];
  view    [label="viewing history\nand sessions", class=store];
  events  [label="playback\nevents", class=queue];
  steer   [label="steering\nservice"];
  planner [label="fill\nplanner", class=worker];
  cc      [label="cache\ncontrol"];
}
subgraph cluster_oc {
  label="data plane:\nOpen Connect";
  style="rounded,dashed"; color="#9CA3AF";
  ix  [label="IX\nappliances", class=edge];
  oca [label="ISP\nappliances", class=edge];
}
app -> gw [label=" play, license,\n heartbeats"];
app -> ix [style=dashed, label=" fallback"];
app -> oca [label=" range\n GETs"];
gw -> play;
gw -> lic;
play -> catalog;
play -> view [label=" bookmarks"];
play -> events [style=dashed];
play -> steer [label=" URLs for files"];
lic -> keys;
encode -> keys [label=" keys"];
encode -> origin [label=" encrypted files"];
origin -> ix [style=dashed, label=" fill"];
ix -> oca [style=dashed, label=" off-peak fill"];
events -> planner [style=dashed];
planner -> cc [label=" placements"];
steer -> cc [dir=back, label=" routes, health,\n files held"];
cc -> oca [dir=back, style=dashed, label=" reports"];
{rank=same; gw; encode}
{rank=same; play; lic; keys}
{rank=same; planner; cc; oca}
```

The ingest path starts at the encoding pipeline, which turns each studio master into dozens of encrypted files (video rungs for each codec, audio tracks, subtitles), writes them to the origin object store and puts their content keys in the key store. Each night the fill planner reads the playback events, a Kafka topic, ranks files region by region and hands the placements to cache control. Every appliance checks in with cache control, reporting its health, the BGP routes it has learned and the files on its disks, and gets back its manifest; in its off-peak window it downloads what it lacks, ISP appliances from the IX appliances at internet exchange points and IX appliances from the origin.

The play path starts at the TV or phone app, whose request reaches the playback API through the API gateway. The playback API checks the title's rights for the member's country in the catalog, reads the resume point and registers the session in the viewing history, picks the streams this device can decode and protect, and asks the steering service for URLs. Steering answers from the state cache control has assembled: which appliances can reach this client, hold the files and are healthy. The app then sends its license challenge to the license service, which takes the content keys from the key store and returns them sealed for that device.

The stream path carries all the video and never touches the cloud. The app fetches byte ranges from the first URL, usually an ISP appliance a few milliseconds away, and moves to the next, often an IX appliance, if a request fails or slows down. A heartbeat every minute lets the playback API store the bookmark and emit the event that feeds the next night's ranking.

### Deep Dives

#### Placing files before anyone asks for them

A conventional CDN (Chapter 15) is a pull-through cache: an edge server that misses fetches the object from upstream and, when its disk is full, evicts the least recently used one (#44). For Netflix it fails in three ways. Misses arrive with demand, so upstream links fill at the evening peak, when they are busiest and most expensive for the ISP. A premiere turns every cold cache into a miss in the same minute. And LRU judges a file by its last access, so an evening of one-off viewing can evict what a million members will want tomorrow.

Netflix's alternative is proactive caching, which by its own account cut the demand on upstream capacity by several orders of magnitude. Each day the fill planner scores every file in each region by bytes streamed divided by bytes stored, its offload per byte of disk, smoothed by an exponentially weighted moving average so that recent days count most; unreleased titles are scored from forecasts. Keeping the top K files that fit the cluster (#19) is the greedy answer to a knapsack of offload, within one file of the optimum because each file is tiny next to a 100 TB appliance. Consistent hashing (#139) spreads the chosen files over the cluster's appliances, with extra replicas for the hottest. Placement becomes repeatable, so any service can compute where a file lives, and adding or retiring an appliance moves only its own share. Within each appliance, memory holds the hottest byte ranges under LRU (#44).

An appliance fetches only the difference between its manifest and its disks, from a peer in its own cluster when one has the file and from the tier above otherwise, so the origin feeds only the IX tier; the planner damps churn, since a file that drops out and comes back is filled twice. The price of forecasting is error: a surprise hit is missing from small sites on its first evening. Nothing fails, because steering hands out only appliances that hold a file, so those plays go to IX sites, which keep the whole catalog, until the next fill. Encryption adds one more freedom: a premiere's files can sit in an ISP's rack for days, useless without a license.

#### Steering each play to the right appliance

DNS and anycast, the usual tools (Chapter 15), both steer blind. DNS usually sees the viewer's resolver, not the viewer, and its answer holds for everyone behind that resolver until the TTL expires; anycast follows BGP to a nearby site but knows nothing of its files or its load. Netflix has a better hook: every play already asks the control plane for a manifest, so steering happens there, once per play, by handing out URLs.

Each embedded appliance holds a BGP session with its ISP's router and learns the prefixes the ISP wants it to serve, which keeps the ISP in charge of which customers reach which box. For a play, the steering service finds the most specific learned prefix covering the client's address, a longest-prefix match over a binary trie (#43). Netflix has described the ranking as most specific route first, then shortest AS path, then lowest MED (a preference the ISP signals in BGP), then geographic distance, so an appliance inside the viewer's own ISP beats an IX site. Candidates must also hold the files and be healthy, and among equals this design picks by a weighted random choice in proportion to spare capacity (#106).

Load needs a feedback loop, because one decision commits a whole session to an appliance. Netflix has described a PID controller that holds appliances near 80% of capacity by trimming the share of new plays sent to them and spilling the rest to the next-best location. The client is the last stage of steering: it holds several URLs per file and, on an error or a slow appliance, resumes the same byte range elsewhere, so a failure in mid-stream costs at most a dip in bitrate. No play starts without the control plane, but a play needs a manifest and a license anyway, so steering adds no round trip.

#### From Play to the first frame: encodes, a license, two seconds

Startup begins in the encoding pipeline. The ladder of renditions and the chunked, parallel transcoding behind it are those of Chapter 8; a curated catalog changes how much effort each title earns. Netflix's original fixed ladder ran from 235 kb/s at 320×240 to 5,800 kb/s at 1080p for every title, wasting bits on flat animation and starving grainy live action. Per-title encoding, introduced in 2015, measures each title's rate-quality curve with trial encodes and builds a ladder for it; later work tunes the parameters shot by shot, scored by VMAF, Netflix's open-source perceptual quality metric. The compute is paid once per title and repaid on every stream, and leaner rungs mean more titles per appliance and faster first segments.

Files are encrypted with AES under Common Encryption (CENC), whose per-system headers let one file serve Widevine, PlayReady and FairPlay devices that share its cipher scheme, so the catalog is not stored once per DRM; each resolution tier has its own key. The device's content decryption module (CDM) produces a license request bound to that device. The license service checks the session token, the security level and the output protection, and returns only the keys the device may use, sealed for that CDM alone: a phone running Widevine in software (L3) gets only the SD key, and a 4K key can demand HDCP 2.2 on the HDMI link.

The naive start spends its budget on round trips and on bytes the player wants before it shows anything:

```text
phone: 100 ms round trip to the cloud, 40 ms to the appliance, 10 Mb/s link
                                     serial, naive      prefetched, start low
manifest (1 round trip + 50 ms)      150 ms             0, fetched earlier
license  (1 round trip + 50 ms)      150 ms             0, fetched earlier
TCP + TLS 1.3 to the appliance        80 ms             80 ms
first media (1 round trip + bytes) 1,240 ms             240 ms
  naive: 4 s at 3 Mb/s = 12 Mb      start low: 2 s at 1 Mb/s = 2 Mb
decode and show the first frame      100 ms             100 ms
time to first frame                ≈ 1.7 s              ≈ 0.4 s
```

Prefetching manifests and licenses for the likeliest plays, the next episode or the title in focus, takes both cloud calls off the critical path. When the prefetch missed, the license and the first media request run in parallel, because ciphertext can be downloaded before its key arrives. The player starts on a low rung with a two-second buffer and climbs as the buffer grows. The costs are license-service load, since most prefetched licenses go unused, and a stream limit that must count heartbeating sessions, not issued licenses.

### Scaling and Bottlenecks

The data plane scales by adding appliances, and the binding constraint depends on the site. A small embedded site runs out of disk first, so it holds the head of the ranking and leans on IX sites; a large one runs out of throughput at prime time and gets more appliances and more replicas of the hottest files. On a premiere night the busiest sites hit their limit first, and the controller spills new plays to the next location before any appliance is full. Peaks, and with them the fill windows, roll west with the time zones.

In the control plane, 23,000 play starts a second is easy for stateless services; the 670,000 bookmark writes a second are the real load, which Cassandra absorbs by adding nodes. Each steering server holds its whole world in memory, the prefix trie and the map from files to appliances, a few gigabytes refreshed continuously from cache control, so any server answers any play. The fill planner is a nightly batch job over millions of files and thousands of clusters, parallel by region.

### Failure Modes

An appliance that dies mid-stream is invisible to the viewer: the next range request fails, the player resumes from the same offset at the next URL, and a buffer of tens of seconds covers the switch, while cache control notices the silence and steering stops sending plays there. If a whole embedded site or its uplink fails, clients fall back to IX appliances over peering, which is what those sites are sized for.

The control plane is the dangerous dependency, because no play starts without it. It runs active-active in three cloud regions, and Netflix rehearses failure on purpose: Chaos Monkey terminates production instances at random, and Chaos Kong simulates the loss of a whole region to prove that traffic moves to the others. Every call between services has a timeout and a fallback, the circuit-breaker pattern that Netflix's Hystrix library popularised: without personalisation the home page shows popular rows, and with a slow viewing history playback starts from the device's last known position. Streams already playing barely notice an outage, since they need the cloud only for buffered heartbeats and license renewals. A premiere is a planned surge of manifest and license requests, so those fleets are scaled up beforehand.

### Trade-offs and Alternatives

Owning the CDN is a bet on volume and predictability. Netflix streamed through commercial CDNs before Open Connect began in 2011, and a new service should do the same, ideally through several, until its traffic is a large share of what ISPs carry; only then are free appliances a good deal for the ISP and a hardware fleet a good deal for the service. Proactive placement is the same bet for content: it wins for a curated catalog with scheduled releases, while the long tail of Chapter 8 needs pull-through caches and live events (Chapter 32) cannot be pre-positioned at all.

Steering by URL ties each play to the control plane in exchange for placement that knows about files and load; DNS or anycast would decouple the two and lose that precision, the right trade for small objects without sessions. One file per stream, read by byte ranges, keeps the files to place in the millions and lets an appliance send straight from disk to socket, while separate segment files suit generic CDNs that cache each segment as its own object. Hardware-backed DRM, finally, trades device reach for the studios' trust.

### What Interviewers Probe

Expect six questions. Why not buy a CDN? At this volume and predictability, appliances inside ISPs save transit for both sides and let content be placed before demand; below that volume, buy one. How does content reach the appliances? A nightly plan ranks files by offload per byte, keeps what fits each cluster, places it by consistent hashing, and the appliances fill off-peak. What if the nearby appliance lacks a title? Steering only hands out appliances that hold it, so the play goes to an IX site. How is the appliance chosen? Learned BGP prefixes, longest-prefix match, file availability, health and a load controller, with spare URLs for failover. How does playback start within two seconds? Prefetch, fetch media alongside the license, start low. Where is DRM enforced? In the license service and the device's CDM, never on the appliance, which holds only ciphertext.

Strong candidates add three points unprompted: a playing stream needs nothing from the cloud, so a control-plane outage spares everyone already watching; encryption is what makes it safe to park unreleased titles in third-party racks; and the scarce resource is egress, so the whole design exists to move 160 Tb/s as short a distance as possible.

*Algorithms:* #19 Top-K Elements · #139 Consistent Hashing · #43 Trie · #106 Random Pick with Weight · #44 LRU Cache
