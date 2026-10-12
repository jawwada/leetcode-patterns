---
rank: 14
slug: maps_navigation
---

A maps service draws the planet at any zoom, turns a typed address into a point, and guides a driver sixty kilometres with an arrival time that already knows about the crash on the motorway. Asked at five in the afternoon for directions from downtown San Francisco to Mountain View, it must return a route, two alternatives and an ETA of 58 minutes within a few hundred milliseconds. Three questions decide the design: how to serve a map of the world without drawing anything per request, how to find a shortest path through hundreds of millions of road segments in milliseconds when plain Dijkstra takes seconds, and how to pour live traffic into that search every minute without discarding the preprocessing that made it fast.

### Requirements

A user pans and zooms a map from the whole globe down to a single street, optionally with live traffic. They search for an address or a place and get a point back (geocoding), or press on the map and get its address (reverse geocoding). They ask for driving directions and get the best route and up to two alternatives, each with turn-by-turn steps and a traffic-aware ETA; during the trip the ETA stays current and the app reroutes when the driver strays or a clearly faster road appears.

Assume 500 million daily users. Tiles must arrive within 100 ms at the 99th percentile and routes within a second. A new jam should reach the routes within about two minutes, and most ETAs should land within 10 percent of the actual drive. Maps and routing must stay up at 99.99 percent, and a navigating phone must keep guiding through a lost connection. The map may trail reality by a day and traffic by a minute or two, but the map database, years of edits, must never lose data; raw GPS traces are disposable once aggregated. Transit, Street View, business listings and map editing are out of scope.

### Estimates

```text
tile requests  500 M users × 3 sessions × 40 uncached tiles = 60 B/day
               ≈ 700,000/s × 20 KB ≈ 110 Gbit/s; peak ×3: 2.1 M/s
raster tiles   zoom 0..18: (4^19 - 1) / 3 ≈ 9.2 × 10^10 per style and language
vector tiles   zoom 0..14: (4^15 - 1) / 3 ≈ 3.6 × 10^8; a third hold land,
               × 20 KB ≈ 2.4 TB, one set shared by every style
route queries  300 M/day ≈ 3,500/s; peak ×3 ≈ 10,000/s
route CPU      10,000/s × 3 candidates × 5 ms ≈ 150 cores
road graph     300 M nodes × 12 B + 700 M edges × 8 B ≈ 9 GB of flat arrays;
               with overlay, turn costs, coordinates ≈ 25 GB: fits one server
navigation     100 M trips × 30 min / 1,440 min ≈ 2 M live; peak ×3 ≈ 6 M
uploads        6 M phones × one fix per 5 s = 1.2 M/s × 50 B ≈ 60 MB/s
re-scoring     6 M live routes once a minute ≈ 100,000 sums/s
metric delta   ~20 M segments change speed a minute × 8 B ≈ 160 MB/min
profiles       700 M segments × 672 quarter hours × 1 B ≈ 470 GB raw;
               a shared curve id + free-flow speed, 3 B each ≈ 2 GB
```

The numbers split the system three ways. The map is a caching problem: two million tile requests a second for a pyramid small enough to copy to every edge location, but only because the tiles are vectors. Routing is a latency problem, not a capacity one: the world's graph fits in one server's memory and the load needs about 150 cores, so routers scale by replication, and the hard part is answering in milliseconds. Traffic is a streaming problem: 1.2 million fixes a second become 160 MB of new weights a minute for every router.

### API

```text
GET  /tiles/v3/{layer}/{z}/{x}/{y}.mvt                  (served by the CDN)
     200 <vector tile>   304 Not Modified   404 outside the pyramid
     base layer: max-age=86400 + ETag          traffic layer: max-age=60
GET  /api/v1/geocode?q=1600+amphitheatre+pkwy&near=37.42,-122.08
     200 {"results": [{"place_id": "p81f3", "lat": 37.4220, "lng": -122.0841,
                       "name": "...", "address": "..."}]}
GET  /api/v1/reverse?lat=37.4220&lng=-122.0841      200 {"address": "..."}
POST /api/v1/routes
     {"origin": {"lat": 37.7897, "lng": -122.3942, "heading": 270},
      "destination": {"place_id": "p81f3"}, "depart": "now", "alternatives": 2}
     200 {"routes": [{"route_token": "...", "polyline": "...", "eta_s": 3480,
                      "distance_m": 59800, "steps": [...], "traffic": [...]}]}
     400 invalid coordinates      200 {"routes": []} when no road connects
POST /api/v1/nav  {"route_token": "...", "destination": {...}}
     201 {"session_id": "n52e"}
POST /api/v1/nav/{session_id}/fixes                     every 5 s while driving
     {"fixes": [{"t": ..., "lat": ..., "lng": ..., "speed": ...,
                 "heading": ...}]}
     200 {"eta_s": 3110, "reroute": null}         or a new route and "saves_s"
     404 unknown session → the phone restarts it from its route_token
```

Tile URLs carry no user or session, so one cached copy serves everyone at an edge location; `v3` is the tile schema. Base tiles revalidate daily with their ETag, so an unchanged tile costs a 304 without a body; traffic tiles live for a minute. Other calls carry an app token and are rate limited per device. A route returns an encoded polyline, voice-guidance steps, traffic per stretch and an opaque `route_token` encoding its segment ids. Navigation needs no push channel: the phone uploads a fix every five seconds anyway, and each response carries the fresh ETA and any better route; timestamps make a retried upload harmless.

### Data Model

```text
segments  segment_id PK | from, to | geometry | class | limits | names, house #s
          map database, the source of truth: split by S2 cell, versioned
graph     per release, flat arrays in RAM on every router: first_out[node]
          → edges (head, segment_id); turn table; cell of each node
metric    per minute: weight[edge] + border-to-border costs of every cell
speeds    segment_id → live speed, samples, updated_at | free_flow, curve_id
tiles     (layer, quadkey) PK → MVT blob, ETag            sorted key-value
places    place_id PK | name | category | lat, lng | address | S2 cells
          + inverted index: token → place_ids, sorted by popularity
probes    Kafka, keyed by session_id, kept 7 days: t, lat, lng, speed, heading
```

The map database is the source everything is compiled from, and nothing serves from it directly: segments with geometry, class, limits, turn restrictions, names and house-number ranges, plus places, in a durable store such as Spanner or Bigtable, split by S2 cell (Google's hierarchy of cells on the sphere) and versioned per release. Each release compiles a graph of flat arrays that every router holds in memory, because a query touches thousands of edges in no useful order, too many random reads for any disk; the metric, every edge's travel time plus each cell's border-to-border costs, is kept apart because it changes every minute. Tiles are keyed by quadkey in a sorted store, so the tiles inside any tile share its key as a prefix and sit in one contiguous range. Places, and streets with their house-number ranges, sit in an inverted index (#150) from name and address tokens to ids, with S2 cell ids as extra tokens, so "pizza" near the viewport is an intersection of posting lists. Probes are keyed by session, so a trip's fixes reach one map-matching worker in order.

### Architecture

```dot
rankdir=TB;
phone   [label="phone app", class=client];
cdn     [label="CDN edge", class=edge];
gw      [label="API gateway", class=edge];
tsrv    [label="tile server"];
tiles   [label="tile store\nby quadkey", class=store];
geo     [label="geocoder"];
places  [label="places\nindex", class=store];
route   [label="routing service\ngraph in RAM"];
eta     [label="ETA service"];
nav     [label="navigation\nservice"];
probes  [label="GPS\nprobes", class=queue];
match   [label="map matcher", class=worker];
speeds  [label="speed store\nlive + profiles", class=cache];
cust    [label="customizer", class=worker];
hist    [label="profile job", class=worker];
mapdb   [label="map\ndatabase", class=store];
build   [label="build jobs", class=worker];
phone -> cdn [label=" tiles"];
phone -> gw [label=" API calls"];
cdn -> tsrv [label=" miss"];
tsrv -> tiles;
tsrv -> speeds [label=" traffic"];
gw -> geo;
geo -> places;
gw -> route;
gw -> nav;
route -> eta [label=" score"];
nav -> eta [label=" re-score"];
nav -> route [label=" reroute"];
nav -> probes [style=dashed];
probes -> match [style=dashed];
probes -> hist [style=dashed];
match -> speeds [style=dashed];
hist -> speeds [style=dashed];
eta -> speeds;
cust -> speeds;
route -> cust [dir=back, style=dashed, label=" metric"];
tiles -> build [dir=back];
places -> build [dir=back];
route -> build [dir=back, style=dashed];
build -> mapdb [dir=back];
{rank=same; cdn -> gw [style=invis]}
{rank=same; geo -> tsrv -> route -> nav [style=invis]}
{rank=same; places -> tiles -> eta -> probes [style=invis]}
{rank=same; build -> cust -> match [style=invis]}
{rank=same; mapdb -> speeds -> hist [style=invis]}
```

The map path touches no application server on a hit. The phone app works out which tiles cover its viewport and asks the CDN edge for each by layer, z, x and y. A miss goes to a stateless tile server, which reads base tiles from the tile store and renders traffic tiles from the speed store. On each release the build jobs cut tiles from the map database, refresh the places index and compile the graph that the routing service loads.

Everything else enters through the API gateway. The geocoder ranks candidates from the places index by text match, popularity and distance from the viewport, interpolates a house number along its segment's range when no exact point exists, and answers reverse lookups from the same index by S2 cell. The routing service snaps both ends of a request to their nearest segments, using the heading so that a northbound driver is not snapped to the southbound carriageway, finds the best route and a few alternatives on the current metric, and has the ETA service score each from the speed store.

During a trip the phone posts a fix every five seconds to the navigation service, which tracks progress, has the ETA service re-score the rest of the route each minute, asks the routing service for a new route when traffic turns, and publishes the fix, stripped of identity, to the GPS probes topic. From there the path is asynchronous: the map matcher writes per-segment speeds to the speed store every minute, the customizer folds them, profiles for roads without fresh probes and closures into the minute's metric for every routing replica, and a weekly profile job folds the week's probes into the profiles.

### Deep Dives

#### The map as a pyramid of tiles

Drawing an image per request fails twice: every viewport is a slightly different rectangle, so nothing is reused, and a render farm would draw two million maps a second. The fix is a fixed grid. Web Mercator projects the earth, cut off at about 85 degrees of latitude, onto a square; zoom 0 is that square as one tile, and every tile splits into four at the next zoom, so the pyramid is a quadtree (#148). A million people looking at Manhattan now request the same few hundred URLs, which a CDN (Chapter 15) serves well.

```text
zoom z    2^z × 2^z tiles; tile (z, x, y) has four children at zoom z + 1:
          (2x, 2y)  (2x + 1, 2y)  (2x, 2y + 1)  (2x + 1, 2y + 1)
x         ⌊(lng + 180) / 360 × 2^z⌋
y         ⌊(1 - ln(tan(lat) + sec(lat)) / pi) / 2 × 2^z⌋, lat in radians
quadkey   one base-4 digit per zoom from the bits of x and y, so tile "1203"
          lies inside "120", and every subtree is one contiguous key range
```

What a tile holds is the second decision. Images are easy on the client, but the pyramid to zoom 18 is 9.2 × 10^10 tiles for every style, language and screen density. Vector tiles carry geometry as integer coordinates on a 4,096-unit grid, the usual extent of the Mapbox Vector Tile format, and the phone styles and draws them, so one tile set serves every theme, language, rotation and tilt. Vectors also scale: a zoom-14 tile spans about 2.4 km at the equator, so its grid resolves 60 cm, and the phone overzooms it to street level; stopping at zoom 14 rather than 18 divides the pyramid by 4^4 = 256. The cost moves to the device, so the builder simplifies lines at low zooms (Douglas–Peucker, minor roads dropped) and pads each tile with a small buffer so features meet cleanly at its edges.

Tiles change in two rhythms. A release touches a small fraction of the world, so the builder re-cuts only changed tiles and purges those URLs from the CDN. Traffic changes every minute, so it is a separate layer with a one-minute lifetime; baked into the base map, it would invalidate the heaviest tiles every minute.

#### Shortest paths on a continent

Intersections are nodes and directed segments are edges, weighted by travel time; turn restrictions and turn costs are modelled by making each segment a node and each allowed turn an edge, which every technique below handles unchanged. Breadth-first search (#39) would find the fewest segments, the wrong question; Dijkstra's algorithm (#42), the same search with a priority queue keyed by travel time, finds the fastest. But it settles every node nearer than the destination, a disc around the origin, which across a country is millions of nodes and seconds of CPU.

A* adds a lower bound on the remaining time, straight-line distance over the network's top speed, which steers the search and keeps it optimal; on travel times the bound is weak, since it assumes motorway speed across every field. Bidirectional search, which stops once the smallest keys of the two queues sum to at least the best meeting found, replaces one disc with two of half the radius and roughly halves the work. Neither knows that long trips use motorways.

Contraction hierarchies teach the graph that fact in advance. Rank the nodes by importance and contract them from the least important up: remove v and, for each pair of its neighbours u and w, add a shortcut u → w weighing as much as the path through v, unless a small local Dijkstra, the witness search, finds a path that avoids v and is no longer. Nodes whose removal adds few shortcuts go first, so cul-de-sacs vanish early and motorway junctions last.

```text
contract v   u ──3── v ──4── w   becomes   u ──7── w  (shortcut via v)
             unless a witness path from u to w of cost ≤ 7 avoids v
query s→t    a forward search from s and a backward one from t, each
             following only edges that climb in rank; the answer is
             min over meeting nodes m of dist(s, m) + dist(m, t)
```

The query is exact because contraction preserves every distance: any shortest path, with its low-ranked stretches replaced by shortcuts, climbs to one highest node and then descends, so the forward search finds the climb and the backward search the descent. On a continent the two settle a few hundred nodes in well under a millisecond, and each shortcut records the node it bypasses, so the route unpacks into real segments.

The price is preprocessing, minutes for a country and hours for the planet, and shortcuts bake in the weights beneath them: one motorway crash changes the true cost of thousands. So the preprocessing is split in two, the idea behind customizable route planning, which Microsoft researchers built and Bing Maps adopted in 2012. A partitioner cuts the network into nested cells along its natural narrow cuts, rivers, ridges and the few bridges across them, a step that depends only on the map. Customization then computes, for the current metric, the travel time between every pair of each cell's border nodes, bottom-up through the levels; cells are independent, so it runs in parallel in seconds for a continent, and only cells with changed roads, and those above them, need it. A query walks real streets only in the origin's and destination's cells and crosses the rest on the border tables of ever larger cells, in a few milliseconds. OSRM ships both engines and recommends the multi-level one whenever traffic must flow in, and this design does the same.

#### Live traffic, ETA and rerouting

Averaging the speeds phones report is the naive traffic system, and noise defeats it: GPS drifts tens of metres between tall buildings, a frontage road runs beside the motorway, and a van parked at the kerb reports zero. So the map matcher first decides which road each trip was on. It treats true positions as the hidden states of a hidden Markov model: a fix probably came from a nearby segment, and a step between fixes is likely when the driving distance between candidates matches the straight-line distance; the Viterbi algorithm, run a few fixes behind real time, picks the likeliest sequence of segments. The job then takes the median travel time per segment per minute, publishes only when several distinct phones agree, blends thin readings toward the profile, and pre-aggregates before shuffling by segment, because a rush-hour motorway is a hot key.

Live speeds describe the roads now, but the driver reaches the end of a long trip an hour later. So the ETA service walks each candidate with a clock: live speeds near the start, then a blend toward the profile for the quarter hour in which the car reaches each later segment, plus a learned correction for what averages miss, such as queues at junctions. Google and DeepMind have published that their model is a graph neural network over supersegments, runs of adjacent segments that share heavy traffic, and that it improved live ETA accuracy by up to 50 percent in some cities. Scoring only a handful of candidates keeps that model out of the search.

Rerouting has two triggers. Straying is detected on the phone, which holds the route and asks for a new one from its position and heading, so the answer does not begin with a U-turn. A better route is detected on the server: each minute the navigation service has the rest of every trip re-scored, a cheap sum, and only when an ETA worsens does it ask for a fresh search, offering the result only if it saves a real share of the trip, with hysteresis against flapping. Advice also changes the traffic it predicts: sending every driver down the same side street makes the next jam, so suggestions go to a fraction of drivers at a time.

### Scaling and Bottlenecks

The tile path scales with the CDN: demand concentrates on cities, so hit rates are high, and each edge fetches a traffic tile at most once a minute because concurrent misses are coalesced.

Routing runs out of memory and metric bandwidth before CPU. Each replica holds the graph and two metrics, the one it serves and the one it is loading, and swaps atomically; the metric is a small fraction of the graph, so double-buffering is cheap. The customizer publishes only the minute's 160 MB of changed weights and each replica re-customizes the affected cells itself, deterministically, so all replicas reach the same version. Replicas are added per region for latency and redundancy, not capacity.

Navigation is the busiest API at 1.2 million uploads a second. The gateway maps sessions to navigation servers by consistent hashing (#139) with virtual nodes, so a lost server's sessions spread evenly over the rest. The probe topic partitions by session and the aggregation by segment, both scaling with partitions and workers as in Chapter 12.

### Failure Modes

A navigating phone survives the network first: it prefetches tiles along the route corridor and keeps the route and steps, so guidance continues through a cellular dead zone on GPS alone, and through a tunnel by extrapolating along the route. If the tile origin fails, phones use their caches and the CDN serves stale tiles. If a navigation server dies, its trips' next uploads get a 404 and the phones restart their sessions from the route token.

The dangerous failures are silent ones in the data. If the traffic pipeline stalls, the customizer lets live speeds older than a few minutes decay toward their profiles, so a stale jam does not divert drivers for an hour; if the customizer itself stalls, routers keep serving the last metric. A bad metric, say one that zeroes motorway weights, would misroute everyone at once, so the customizer checks a customized copy first, against the usual share of changed edges and canary routes with known answers, and routers keep the previous version for rollback; graph releases pass the same gate. Probes can be gamed: in 2020 the artist Simon Weckert pulled 99 phones in a handcart through Berlin and conjured jams on empty streets, so the matcher discounts devices moving in lockstep. History misleads too: when the 2020 lockdowns cut traffic by up to half, Google reweighted its models toward the last two to four weeks of history.

### Trade-offs and Alternatives

The router trades query speed for freshness. Contraction hierarchies answer fastest for metrics that rarely change, such as walking; customizable route planning pays a few milliseconds per query for a metric that changes every minute; customizable contraction hierarchies, a contraction order fixed once from a nested-dissection partition with shortcut weights recomputed per metric, sit between. Routing on the current metric and scoring on arrival time is an approximation; time-dependent routing, with weights that vary by time of day, finds the truly fastest long route at much higher cost.

Replicating the graph keeps each query on one machine. A graph too large for memory, or offline routing on a phone, calls for geographic tiles as in the open-source Valhalla router, which stores three levels for highways, arterials and local roads and loads only the tiles a route needs. Raster tiles keep a niche for static map images and devices that cannot draw vectors.

### What Interviewers Probe

Expect six questions. How do you draw the map? A Web Mercator tile pyramid addressed by z, x and y, a quadtree, served from the CDN as vectors. Why not Dijkstra? It settles millions of nodes on a long trip. Does A* fix that? Barely, because the straight-line bound must assume motorway speed. How do contraction hierarchies work, and why are they exact? Shortcuts from contracting unimportant nodes first, an upward search from both ends, and every shortest path has one highest node. How does traffic get in without redoing the preprocessing? Partition once and recompute each cell's border costs every minute. How is the ETA computed? Live speeds near the start, profiles for when the car reaches later segments, and a learned correction.

Strong candidates raise four points unprompted: map matching, because raw GPS is too noisy to average; the feedback loop of rerouting; probe privacy, with rotating session ids, trimmed trip ends and only segment aggregates kept; and a validation gate on every metric. Interviewers rarely care which partitioner you name. They care that no query runs Dijkstra across a continent, and that the precomputation survives a world that changes every minute.

*Algorithms:* #42 Dijkstra's Algorithm · #148 Quadtree · #150 Inverted Index · #139 Consistent Hashing
