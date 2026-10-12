---
rank: 15
slug: cdn
---

A content delivery network is a fleet of caching proxies in a couple of hundred cities that serves other companies' content from a point of presence, a PoP, near each user. A shop points `static.example.com` at the CDN, and a shopper in Sydney who asks for `/img/hero.v42.jpg` gets it from a server in Sydney in about 30 ms, not from the shop's origin in Virginia, where the handshakes and the request alone take 600 ms. Three questions decide the design: how to send each user to a near, healthy PoP, how to make the cache hit so each origin sees a trickle instead of a flood, and how to change content already cached in two hundred places.

### Requirements

A customer creates a property (hostnames, an origin such as web servers or a storage bucket, caching rules and a TLS certificate) and points its hostname at the CDN with a DNS CNAME record. End users fetch anything under it over HTTPS, and the CDN answers from cache or from the origin, obeying its headers and the customer's rules. Customers purge by URL, tag or everything, prefetch files before a launch, and see logs and hit ratios.

Assume 20 M requests a second and 16 Tbps at peak through 200 PoPs. A hit should add under 10 ms to the round trip to the PoP. The edge must survive losing a server or a PoP without customer action and keep serving cached content while the control plane or an origin is down. Origins should see under 5% of requests for cacheable content. Freshness is the consistency model: an object may be one TTL out of date, but once a purge is reported done, which takes under five seconds, no PoP serves the old version. Edge code, media processing (Chapter 8), firewall rules and billing are out of scope.

### Estimates

```text
requests    10 M/s average, 20 M/s at peak, over 200 PoPs
egress      20 M/s × 100 KB average response = 2 TB/s ≈ 16 Tbps at peak
big PoP     the top 20 PoPs carry half: 8 Tbps / 20 = 400 Gbps each
servers     400 Gbps / 20 Gbps per server = 20, ×1.5 headroom → 30 per big PoP
fleet       20 big PoPs × 30 + 180 small PoPs × 5 ≈ 1,500 servers
PoP cache   30 × 24 TB SSD = 720 TB if keys are partitioned, 24 TB if copied
index       24 TB / 100 KB = 240 M objects × 100 B ≈ 24 GB of RAM per server
origin      90% edge hits → 2 M misses/s; 80% shield hits → 400 K/s (2%)
new object  wanted in 200 PoPs: 200 origin fetches without a shield, 1 with
latency     origin 200 ms away: TCP + TLS 1.3 + GET = 3 RTT = 600 ms;
            PoP 10 ms away: 30 ms on a hit, ≈ 230 ms on a miss (warm link)
purges      2,000/s × 100 B ≈ 200 KB/s to each of the 1,500 servers
logs        10 M/s × 300 B × 86,400 s ≈ 260 TB/day before compression
```

Bandwidth, not request count, sizes the fleet: the scarce resources are ports and peering at each PoP, and the server count follows from the gigabits each machine can encrypt and send. Thirty servers that each cache whatever they are asked for hold the same popular objects thirty times and give the PoP 24 TB of distinct content; partitioning the keys gives it 720 TB, with the index still in RAM. Two cache tiers leave origins 2% of requests, and the shield turns a new object's 200 origin fetches into one. Even uncacheable content gets faster, because the handshakes cross 10 ms instead of 200. Purges are trivial in volume; the hard part is reaching 1,500 servers reliably within seconds.

### API

```text
GET  https://static.example.com/img/hero.v42.jpg          (end users)
     If-None-Match: "a1b2"           Range: bytes=0-1048575
     200 | 206 Partial Content | 304 Not Modified | 502/504 origin failed
     Age: 1840        Cache-Status: edge; hit

origin response headers that steer the CDN
     CDN-Cache-Control: max-age=86400, stale-while-revalidate=60
     Cache-Control: public, max-age=300                     (browsers)
     Surrogate-Key: product-123 shoes  Vary: Accept-Encoding  ETag: "a1b2"

PUT  /v1/properties/{id}                    If-Match: "v18"   (customers)
     {"hostnames": [...], "origin": "...", "rules": [...], "cert": "..."}
     200 {"version": "v19"}     412 changed since v18     400 invalid rule
POST /v1/properties/{id}/purge
     {"urls": [...]}  or  {"tags": ["product-123"]}  or  {"all": true}
     202 {"purge_id": "pg_81f"}
GET  /v1/purges/{purge_id}
     200 {"state": "done", "pops_acked": 200, "pops_total": 200}
POST /v1/properties/{id}/prefetch    {"urls": [...]}           202
```

The data plane is plain HTTP, steered by standard headers from the origin. `CDN-Cache-Control` (RFC 9213) sets the edge's lifetime apart from the browser's `Cache-Control`, so a page can live a day at the edge, where it can be purged, and five minutes in browsers, where it cannot. `Vary` names the request headers that change the response, `ETag` lets a cache revalidate with a bodiless 304, `Surrogate-Key`, Fastly's name for tags, groups objects for purging, and `Age` with `Cache-Status` (RFC 9211) tells the client how old its copy is and which cache served it. On the authenticated control API, a configuration write carries its base version in `If-Match`, so concurrent edits end in a 412 rather than a silent overwrite. A purge returns 202 and reports done once every serving PoP has acknowledged it; purging twice is harmless, so it needs no idempotency key.

### Data Model

```text
control plane: strongly consistent store, a few GB in total
properties    property_id PK | account | origins | rules | cert_id
              | generation | version
hostnames     hostname PK → property_id        one owner per name, verified
certificates  cert_id PK | hostnames | chain | encrypted private key
purge_log     (shard, seq) PK | property_id | url | tag | all | issued_at
pop_acks      (pop_id, shard) PK → applied_seq | last_seen

edge server: index in RAM, bodies on local SSD
cache key     property_id · generation · host · path · kept params, sorted
              · normalized Vary values  (· slice number for large files)
index         hash(key) → SSD offset | size | fetched_at | expires_at
              | etag | tag ids              LRU order, about 100 B per entry
purge map     (property_id, tag) → last purge time     dropped after a sweep
```

The control plane holds a few kilobytes per property but must be exactly right, so it lives in a strongly consistent database such as Spanner (Chapter 38). The `hostnames` table is the security boundary: whoever owns a name there gets its traffic and certificate, so a name is accepted only after a DNS or HTTP challenge proves control. Edge servers never read the store on the request path; each change, certificates included, becomes an immutable snapshot on every server, which keeps serving with its last one when the control plane is unreachable. The purge log is ordered within each shard like a Kafka partition (Chapter 12), and `pop_acks` records how far each PoP has applied it.

On the edge, the index is a hash table in RAM keyed by a 128-bit hash of the cache key, kept in LRU order (#44) for eviction and checked for expiry on every lookup (#94). A large file is stored as slices of a few megabytes, so a range request fetches only the slices it touches. The `generation` inside every key makes purging a whole property one increment: the old keys become unreachable and age out of the LRU.

### Architecture

```dot
rankdir=TB;
user     [label="user\nbrowser or app", class=client];
customer [label="customer\nconsole or API", class=client];
dns      [label="GeoDNS\nmapping", class=edge];
subgraph cluster_pop {
  label="edge PoP (one of 200)"; style="rounded,dashed"; color="#9CA3AF";
  lb     [label="routers + L4 LB\nanycast, ECMP", class=edge];
  front  [label="edge servers\nTLS, cache key", class=edge];
  agent  [label="PoP agent", class=service];
  owner  [label="owner server\nhash ring, SSD", class=cache];
}
subgraph cluster_shield {
  label="shield PoP near origin"; style="rounded,dashed"; color="#9CA3AF";
  shield [label="shield caches\ncoalesce misses", class=cache];
}
origin   [label="customer origin\nservers or bucket", class=external];
subgraph cluster_ctl {
  label="control plane"; style="rounded,dashed"; color="#9CA3AF";
  api    [label="control API\nconfig, purge"];
  cfg    [label="config store", class=store];
  plog   [label="purge log", class=queue];
}
logs     [label="access logs", class=queue];
agg      [label="log aggregation", class=worker];
user -> dns [label=" 1. resolve"];
user -> lb [label=" 2. HTTPS GET"];
lb -> dns [style=dashed, label=" health, load"];
lb -> front;
front -> owner [label=" hash(key)"];
owner -> shield [label=" miss"];
shield -> origin [label=" miss, once"];
customer -> api;
api -> cfg;
api -> plog;
cfg -> agent [style=dashed, label=" snapshots"];
plog -> agent [style=dashed, label=" purges"];
agent -> front [style=dashed];
front -> logs [style=dashed];
logs -> agg;
{rank=same; user; customer; api}
user -> customer [style=invis];
{rank=same; dns; lb; cfg; plog}
{rank=same; front; agent}
```

The user's resolver follows the customer's CNAME to the CDN's GeoDNS servers (step 1), whose mapping answers with an anycast address chosen from the health and load reports of every PoP's routers and L4 load balancers. BGP delivers the connection (step 2) to the nearest PoP announcing that address, where routers spread connections over the L4 load balancers with ECMP and those hand them to edge servers, the layer of Chapter 40.

The edge server terminates TCP and TLS, picking the certificate by the SNI name in the client's hello, finds the property in its configuration snapshot and builds the cache key. It serves the few thousand hottest objects from its own RAM and hashes anything else onto the PoP's consistent-hash ring, asking the owner server, which serves from RAM or SSD; edge and owner are two roles of the same machines. On a miss the owner asks the shield caches, a PoP near the origin chosen for the property, and on a second miss the shield fetches from the customer origin over a warm, pooled connection. The response streams back and is stored in both tiers when its headers allow. Every request leaves a line in the access logs, a Kafka stream that a log aggregation job rolls up per property and minute for dashboards and billing.

The control path is asynchronous. The customer's changes go through the control API into the config store and the purge log, and a PoP agent in every PoP pulls new snapshots and purges, applies them to each of its servers and reports what it applied. Nothing on the request path waits for the control plane.

### Deep Dives

#### Steering users to a near, healthy PoP

A static DNS map from countries to PoPs fails three ways: countries are a poor proxy for network distance, the map ignores load, and a dead PoP keeps receiving users until someone edits it. Steering must measure, with one of two tools.

GeoDNS answers each query from a continuously recomputed map of PoP health, load and measured distance to the querying network; Akamai built its business on DNS mapping. It gives precise control, such as moving 30% of a city's users to a second PoP. But the authoritative server sees the resolver, not the user, a gap that EDNS Client Subnet (RFC 7871) closes only for resolvers that send it, and answers are cached for their TTL, so changes land only as caches expire.

Anycast has every PoP announce the same prefix over BGP, and each network delivers packets to the announcement it considers closest. A PoP that withdraws loses its users to the next nearest as BGP converges, usually within seconds, and a worldwide botnet's flood is split across every PoP; Cloudflare runs its whole network this way. The price is control: BGP chooses by policy and path length, not latency, and an overloaded PoP can shed load only bluntly, by withdrawing routes. A route change mid-connection delivers packets to a PoP that never saw the connection, which answers with a TCP reset; that is rare, and long downloads resume with a range request.

This design layers the two. GeoDNS hands out one of a few anycast addresses, each announced by a regional group of PoPs; within a group, anycast picks the PoP and handles failures, and across groups the map moves a fraction of users off a group that runs hot. Microsoft's FastRoute layered anycast addresses in a similar way. The cost is running both a measurement system and a BGP operation with good peering.

#### Making the cache hit

Every miss costs the user a long round trip and the origin capacity, and five effects cause them.

Fragmentation stores the same bytes under many keys: `?utm_source=mail&v=7` and `?v=7&utm_source=news` name one file, and a careless `Vary: User-Agent` splits every object into a variant per browser build. The edge normalizes before it hashes, keeping only the query parameters the customer marks as significant, sorted, and reducing each `Vary` header to a few buckets, such as the encodings it stores or a device class.

```text
request  GET /js/app.js?utm_source=mail&v=7&lang=en
         Accept-Encoding: gzip, deflate, br    User-Agent: Mozilla/5.0 (iPhone…
key      812 · gen 3 · static.example.com/js/app.js?lang=en&v=7 · br
```

Duplication wastes the PoP: if requests land on servers at random, every server caches the same objects. Consistent hashing (#139) gives each key one owner, and a server that joins or fails moves only its own share. It was invented for this very problem, in a 1997 paper on web caching whose authors included two of Akamai's founders. Ownership would let a viral object melt its owner, so every server also keeps the hottest objects in its own RAM.

Independent misses multiply: with one tier, each of the 200 PoPs fetches every object it serves from the origin itself. The shield takes the edge misses, so the origin sees about one fetch per object per TTL, at the cost of an extra hop on a double miss; CloudFront's Origin Shield and Fastly's shielding work this way.

Herds arrive at once: fifty thousand clients may want a new release in the same second. Request coalescing allows one fetch in flight per key, and later requests share its bytes as they stream in. A PoP's requests for a key already meet at its owner and the shield coalesces again, so the herd reaches the origin as one request. An uncacheable response releases its waiters and marks the key to skip coalescing for a while, which Varnish calls hit-for-pass.

One-hit wonders pollute the disk: many objects are requested exactly once, and writing them wears the SSD and evicts useful ones. Akamai's answer was to cache an object only on its second request, remembering recently seen keys in a Bloom filter (#146) at a few bits each; this design keeps two filters and swaps them every few hours, so old keys age out.

#### Changing content cached in two hundred cities

Looping over 1,500 servers to delete a URL is slow, leaves no record on servers that were down, and cannot express "every page that shows product 123". Three tools replace it, in order of preference.

Versioned URLs need no invalidation: a build puts a content hash in the file name, `app.3f9a1c.js`, served with `Cache-Control: public, max-age=31536000, immutable`, and a deploy publishes new names and changes only the HTML that refers to them. HTML and other content that cannot be renamed gets a short TTL with revalidation: on expiry the edge sends its `ETag` in a conditional request, an unchanged origin answers 304, and `stale-while-revalidate` keeps users on the old copy meanwhile.

Purges handle the rest. PoP agents pull new entries from the purge log within a fraction of a second, broadcast them to their servers and report the highest sequence number applied. A purge is done once every PoP serving traffic has passed it: a PoP that lags while the others keep up is drained, its routes withdrawn, until it catches up, and one cut off longer than the log's retention treats everything cached before the gap as stale.

Every server receives every purge, so applying one must be cheap. A URL purge deletes the URL's index entries and a property purge bumps the generation, but scanning 240 M entries for a tag two thousand times a second is impossible. Each server instead records the purge time against the tag and checks lazily: an object fetched before the last purge of any of its tags counts as purged. A sweeper walks the index every half hour deleting such objects, and a record is dropped once a sweep that began after it has finished, so records live at most an hour: about 7 M of them at 64 bytes, under 500 MB. Varnish's bans work the same way.

```text
purge map  (812, product-123) → 10:04:17
object     /img/shoe.jpg   fetched 10:01:55   tags product-123, shoes
lookup     at 10:04:30: fetched before its tag's purge → purged, refetch
```

A hard purge, the default, deletes the object. A soft purge, which Fastly also offers, only marks it stale: the next request revalidates, cheaply if nothing changed, and the customer may let the stale copy be served while the origin is down, trading the purge guarantee for availability.

### Scaling and Bottlenecks

Network capacity runs out first at a busy PoP, so each PoP is planned for its own peak plus a failed neighbour's traffic, the 1.5× headroom of the estimates. TLS handshakes are the main CPU cost: ECDSA certificates are much cheaper to sign with than RSA, and session tickets encrypted under keys shared across the PoP let a returning client resume on any server.

Hot spots are the subtle limit. A viral object concentrates on its owner, which the RAM tier absorbs, with consistent hashing with bounded loads as a backstop: a request that would push its owner past, say, 1.25 times the average load goes to the next server on the ring. A huge customer concentrates its misses on one shield, so big properties get a shield per region. The control plane talks to 200 PoP agents, not 1,500 servers, and a new PoP's traffic share rises gradually while its cache warms.

### Failure Modes

A dead server is dropped by the load balancer's health checks, and its slice of the ring falls to the others. A dead PoP withdraws its anycast routes, or loses them when its BGP sessions drop, and neighbours with headroom take its users within seconds, their colder caches leaning on the shield. Worse is the gray failure, a PoP still announcing routes while serving errors, so each PoP probes itself end to end and withdraws when the probes fail.

A failed shield is replaced by the next on the property's list; with none left, edges go to the origin behind a per-origin rate limiter (#138). A failing origin is what the CDN exists for: fresh objects are served normally, expired ones under `stale-if-error`, errors are cached for a few seconds, and only content with no usable copy gets a 502 or 504. When the control plane is down, PoPs keep serving from their last snapshot, and new configuration and purges wait, reported as pending rather than done.

The worst CDN outages are self-inflicted. In June 2021 a customer's valid configuration change triggered a latent bug in Fastly's software, and 85% of its network returned errors until the change was disabled. Changes therefore roll out in stages, a canary server, one PoP, a region, then the world, with health gates and a one-command rollback. Against attacks, anycast spreads the flood across the fleet, and the origin accepts connections only from the CDN, so attackers cannot go around the edge.

### Trade-offs and Alternatives

This design pulls: it fetches on the first request, caches exactly what is popular and asks nothing of the customer, at the price of a first miss per object. A push CDN places content before anyone asks, which suits a large, known catalog; Netflix's Open Connect fills its appliances off-peak with what it predicts will be watched (Chapter 9), paying in storage for content nobody requests. The prefetch endpoint is the middle path, warming shields before a launch. DNS mapping suits a video CDN whose long, heavy flows must be placed precisely, and anycast suits a web CDN that must absorb attacks. Thousands of small clusters inside ISPs sit one hop from users but split the cache into pieces that hit less often; a couple of hundred large PoPs hit more and are simpler to run. Customers who will not hand over private keys can keep them, with the edge asking their key server for each full handshake's private-key operation, as in Cloudflare's Keyless SSL.

### What Interviewers Probe

Expect six questions. How does a user reach the nearest PoP? DNS mapping or anycast, their costs, and why layering them gives control and fast failover. What is in the cache key? Host, path, significant query parameters sorted, normalized `Vary` values, and why `Vary: User-Agent` is a disaster. How do a PoP's servers share a cache? Consistent hashing to an owner, the hottest objects in every server's RAM. How do you change cached content? Versioned URLs, short TTLs with revalidation, and purges through an acknowledged log with lazy tag invalidation. What happens when a hot object appears or expires? Coalescing at owner and shield, and `stale-while-revalidate`. What happens when a PoP fails? Its routes are withdrawn, neighbours with headroom take its users, and the shield absorbs their misses.

Strong candidates raise three points unprompted: protecting the origin with the shield, coalescing, stale content on errors and an origin that accepts only the CDN; terminating TLS at the edge, because three round trips over 10 ms beat three over 200; and staged rollouts, because a CDN's biggest risk is its own global configuration push. Interviewers rarely care which vendor does what. They care that every miss is treated as expensive, and that each layer makes misses rarer and collapses them into one.

*Algorithms:* #139 Consistent Hashing · #44 LRU Cache · #94 Cache with Expiring Keys · #146 Bloom Filter · #138 Rate Limiter
