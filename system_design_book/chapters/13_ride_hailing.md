---
rank: 13
slug: ride_hailing
---

A ride-hailing service puts a rider into a nearby driver's car within minutes. A rider in Midtown Manhattan enters a destination, sees a price of $23.40 and a pickup in four minutes, and taps Request; seconds later a driver three blocks away gets an offer, accepts it and appears on the rider's map, moving. Behind that screen two million drivers report their position every four seconds. Three questions decide the design: how to keep that many moving points searchable by location, how to give each trip to exactly one driver and each driver at most one trip, and how to price a neighbourhood where riders outnumber drivers.

### Requirements

A rider sets a pickup and a destination, sees nearby cars, gets an upfront price and a pickup time, and requests a ride. The service offers the trip to one driver at a time, and each driver has 15 seconds to accept or decline. Once a driver accepts, the rider watches the car approach, the driver starts and ends the trip, and the rider pays the quoted price. Either side can cancel before the trip starts. Drivers go online, stream their position and go offline. Prices rise where requests outrun the available drivers.

Assume 20 M trips a day and 2 M drivers online at the global peak. The first offer should reach a driver within a few seconds, and the rider's map should trail the real car by about one reporting interval. Positions are soft state: a lost fix is replaced four seconds later, so the location path favours throughput and availability over durability. Trip and driver state is the opposite. No driver may hold two trips, no request may summon two cars, and an accepted trip must survive the loss of a machine or a zone, so those writes are strongly consistent. Ride pooling, scheduled rides, deliveries, driver onboarding and payouts, fraud and the routing engine itself (Chapter 14) are out of scope.

### Estimates

```text
online drivers  2 M at the global peak, one GPS fix every 4 s
location fixes  2 M / 4 s = 500,000 writes/s
cell changes    50 km/h across a 1.1 km cell ≈ 80 s = 1 fix in 20
ingest          500,000 × ~100 B per fix = 50 MB/s ≈ 400 Mbit/s in all
index memory    2 M drivers × ~300 B with both maps ≈ 600 MB for the planet
busiest metro   100,000 drivers online / 4 s = 25,000 fixes/s
trips           20 M per day / 86,400 s ≈ 230/s (peak ×3: 700/s)
offers          ~1.5 per trip ≈ 1,000 offers/s at peak
quotes          5 per trip = 100 M per day ≈ 1,200/s (peak ×3: 3,500/s)
nearby cars     250,000 open rider apps / 5 s refresh = 50,000 reads/s
trip records    20 M × 1 KB = 20 GB per day ≈ 7 TB per year
trip traces     20 M × 300 fixes (20 min) × 50 B = 300 GB/day ≈ 110 TB/year
```

The location stream dominates. Half a million writes a second against fifty thousand reads inverts the usual ratio of a web service, and each write overwrites the last and is worthless four seconds later. A database would log, replicate and re-index every fix for a durability nobody needs, so positions live in memory. The planet's whole index is 600 MB, so memory is no reason to shard; write rate and blast radius are, and a shard per city would leave one machine to absorb a metro's New Year's Eve, so the index shards by cell. Trips arrive seven hundred times more slowly than fixes, so every change to a trip or a driver can afford a strongly consistent transaction. That split between fast soft state and slow hard state is the heart of the design.

### API

```text
WS   /v1/driver/stream                  one connection per online driver
     ↑ fix    {"seq": 4411, "ts": 1791838812, "lat": 40.7549,
               "lng": -73.9840, "heading": 87, "speed": 9.2, "accuracy": 6}
     ↓ offer  {"offer_id": "of_7Hq", "trip_id": "tr_91X", "pickup": {...},
               "pickup_eta_s": 240, "expires_in_s": 15}
POST /v1/offers/{offer_id}/accept       200 {"trip": {...}}    409 expired
POST /v1/offers/{offer_id}/decline      204

POST /v1/quotes  {"pickup": {...}, "dropoff": {...}, "product": "standard"}
     200 {"quote_id": "q_5mN", "price": "23.40", "surge": 1.3,
          "pickup_eta_s": 240, "expires_at": "2026-10-12T21:05:12Z"}
GET  /v1/nearby?lat=40.7549&lng=-73.9840   200 {"cars": [{"lat": ..., ...}]}

POST /v1/trips   Idempotency-Key: <uuid>   {"quote_id": "q_5mN"}
     201 {"trip_id": "tr_91X", "state": "MATCHING"}
     409 rider already has an active trip      422 quote expired
POST /v1/trips/{trip_id}/transitions   {"from": "ACCEPTED", "to": "ARRIVED"}
     200 {"state": "ARRIVED", "version": 4}    409 trip is now CANCELLED
WS   /v1/trips/{trip_id}/live           ↓ driver position and state changes
```

Drivers hold a WebSocket instead of posting each fix, because the server must push offers the moment they exist, and one long-lived connection carries both directions with a few bytes of framing per fix instead of a request and a response. Fixes are fire-and-forget, and the sequence number lets the server drop a duplicate or a stale fix resent after a reconnect. An offer that cannot reach the app falls back to a push notification. The trip request carries an `Idempotency-Key`, because a rider on a flaky network who taps Request twice must not summon two cars, and the rider's single active-trip slot turns any other duplicate into a 409. Every transition, cancellation included, names the state it leaves, so a driver who taps Arrived just after the rider cancelled gets a 409 instead of overwriting the cancellation.

### Data Model

```text
riders        rider_id PK | active_trip_id | payment_method | rating
driver_state  driver_id PK | state: offline, available, offered, on_trip
              | offer_id | offer_expires_at | trip_id | next_trip_id | version
trips         trip_id PK | rider_id | driver_id | state | version | quote_id
              | pickup | dropoff | price | time of each transition
offers        offer_id PK | trip_id | driver_id | sent_at | outcome
              these four: one transactional store, each split by its key
quotes        quote_id PK → price, surge, route summary | expires in 5 min
geo index     in memory per shard: cell_id → {driver_id}
              and driver_id → (lat, lng, heading, product, state, seq, ts)
              shard = consistent hash of the level-12 cell; 30 s TTL
surge         cell_id → (multiplier, computed_at), rewritten every minute
traces        (trip_id, seq) → (ts, lat, lng); wide-column, then object store
```

The first four tables share one store with multi-row transactions, because the writes that matter touch two rows: a request inserts the trip and claims the rider's active-trip slot, and an accept moves both the trip and the driver. Spanner fits, and Uber rebuilt its fulfillment platform on Cloud Spanner for exactly that transactional consistency; a sharded relational database also works if a trip and its driver can change together. The `version` columns make every change a compare-and-set. The geo index lives only in memory, refilled from the stream. Quotes need only a key-value store with a TTL, or none if a quote is a signed token. Traces land in a wide-column store keyed by trip, for disputes and re-pricing, and age into object storage.

### Architecture

```dot
rankdir=TB;
rider    [label="rider app", class=client];
driver   [label="driver app", class=client];
gw       [label="API gateway", class=edge];
conn     [label="connection\ngateway", class=edge];
pricing  [label="pricing service"];
trip     [label="trip service"];
loc      [label="location service"];
eta      [label="ETA service\nroad graph"];
dispatch [label="dispatch service"];
geo      [label="geo index\nin memory", class=cache];
surgec   [label="surge cache", class=cache];
store    [label="trip store\ntrips, drivers", class=store];
locev    [label="location events", class=queue];
tripev   [label="trip events", class=queue];
surge    [label="surge job", class=worker];
traces   [label="trace archive", class=store];
pay      [label="payment service"];
psp      [label="card processor", class=external];
rider -> gw [label=" quote, request"];
driver -> gw [label=" accept, start, end"];
rider -> conn [label=" live trip", dir=both];
driver -> conn [label=" fixes, offers", dir=both];
gw -> pricing;
gw -> trip;
gw -> loc [label=" nearby"];
conn -> loc [label=" fixes"];
loc -> conn [style=dashed];
loc -> geo [label=" upsert, read"];
loc -> locev [style=dashed];
pricing -> eta [label=" route"];
pricing -> surgec;
pricing -> tripev [label=" quotes", style=dashed];
trip -> dispatch [label=" match"];
trip -> store;
trip -> tripev [style=dashed];
dispatch -> eta [label=" ETAs"];
dispatch -> geo [label=" search"];
dispatch -> store [label=" reserve"];
dispatch -> conn [label=" offer"];
tripev -> surge [style=dashed, label=" demand"];
locev -> surge [style=dashed, label=" supply"];
surge -> surgec;
tripev -> pay [style=dashed];
pay -> psp [label=" hold, capture"];
locev -> traces [style=dashed];
{rank=same; rider; driver}
{rank=same; gw; conn}
{rank=same; pricing; trip; loc}
{rank=same; eta; dispatch; geo}
{rank=same; surgec; store; locev}
{rank=same; tripev; surge; traces}
{rank=same; pay; psp}
```

The location path starts at the driver app, which keeps one WebSocket open to the connection gateway. The gateway hands each fix to the location service, which drops implausible ones (an old sequence number, a jump that would need 300 km/h), computes the S2 cell and upserts the driver into the geo index shard that owns it. It also publishes every fix to the location events topic in Kafka (Chapter 12), keyed by driver id so each driver's fixes stay in order, for the surge job and for the trace archive, which keeps the fixes of drivers on trips. For a driver with a trip, the location service also pushes the fix back through the connection gateway to the rider, so the rider's map moves without waiting on Kafka.

Riders reach the services through the API gateway, and the nearby-cars map is a small read of the geo index through the location service. A quote goes to the pricing service, which asks the ETA service for the route, reads the pickup cell's multiplier from the surge cache, returns a price that holds for five minutes and publishes the quote on the trip events topic as a demand signal. A request goes to the trip service, which writes the trip as MATCHING in the trip store and hands it to the dispatch service.

The dispatch service searches the geo index around the pickup, asks the ETA service how long each candidate needs, reserves the best with a conditional write in the trip store and sends the offer through the connection gateway. The driver's accept returns through the API gateway to the trip service, which moves trip and driver forward in one transaction; arriving, starting and ending follow the same route.

Slower work runs off the trip events topic, where the trip service publishes every transition it commits. The payment service asks the card processor for an authorization hold when a trip is requested and captures the fare when it completes, keyed by trip id so a retried capture never charges twice (Chapter 24). The surge job joins demand from trip events with supply from location events and writes each cell's multiplier to the surge cache once a minute.

### Deep Dives

#### Indexing two million moving drivers

The obvious index is a table of positions with B-tree indexes on latitude and longitude, but a latitude range is a band around the whole planet that the longitude range must filter row by row. PostGIS's R-tree answers the query well, yet every fix still rewrites an indexed row, half a million times a second, for data that is stale in four seconds.

Cells fix both problems. A geohash interleaves the bits of longitude and latitude, so each prefix names a rectangle and nearby points usually share a long prefix. Google's S2 library builds the same kind of hierarchy on the six faces of a cube, a quadtree (#148) on each face with cells numbered along a Hilbert curve into 64-bit ids, and finding a fix's cell is pure arithmetic. Each index shard holds two hash maps, driver id to position, state and cell, and cell id to the drivers inside. An update overwrites the driver's entry and moves it between sets only when its cell changes, so it costs O(1) and never rebalances anything. With level-13 cells of about 1.3 km², a car at city speed changes cell once every twenty fixes. That is why the quadtree stays frozen at one level: an adaptive one suits places that never move (Chapter 27), but under moving points its leaves would split and merge without rest, so the fixed grid handles density at query time, searching outward one ring of cells at a time.

```text
2 2 2 2 2      0   the pickup's cell
2 1 1 1 2      1   ring 1: 8 more cells, 9 in all; complete to 1 cell width
2 1 0 1 2      2   ring 2: 16 more, 25 in all; complete to 2 cell widths
2 1 1 1 2          ring k adds 8k cells; at level 13, 1 cell width ≈ 1.1 km
2 2 2 2 2
```

After ring k the search has seen every driver within k cell widths of the pickup, wherever the pickup sits in its cell. The corners of the block hold farther drivers, and a closer one may still sit in the next ring, so the search keeps the ten nearest in a max-heap of size ten (#19) and stops when the heap is full and its top, the farthest of the ten, lies inside the complete radius. Entries expire 30 seconds after their last fix, checked lazily by searches and swept from a min-heap of deadlines (#94), so a phone that dies in a tunnel stops receiving offers. Shards own level-12 cells, four level-13 cells each, placed on index servers by consistent hashing (#139), the way Uber's dispatch system sharded on S2 cell ids. A ring-1 search spans four level-12 cells, so it asks at most four servers, in parallel. Filtering a crowded cell or walking empty rings takes microseconds in memory; the round trips dominate.

#### Matching without double booking

Giving the trip to the nearest driver fails twice. Straight-line distance lies: a driver 300 metres away across a river can be twelve minutes out, while one a kilometre away on the right avenue is three. And two requests a moment apart can both pick the same idle driver, because the read that finds a driver and the write that assigns them are separate steps.

Dispatch therefore ranks a shortlist by ETA. Rather than route each candidate, the ETA service runs one Dijkstra search (#42) from the pickup over the reversed road graph, where a node's distance is its driving time to the pickup under live traffic (Chapter 14), and stops once every candidate is settled or the frontier passes fifteen minutes. Drivers finishing a nearby trip join the shortlist at their remaining time plus the drive from the drop-off, since a car freeing up around the corner beats an idle one across town.

The reservation is the lock. Dispatch claims the best candidate with a conditional write on the driver's row, setting an offer id and an expiry fifteen seconds out, provided the driver is available, holds an expired offer, or is finishing a trip with nothing queued after it. Only one dispatcher can win; a loser moves to its next candidate. The accept runs one transaction that assigns the trip to the driver and moves it to ACCEPTED, provided the driver still holds this unexpired offer and the trip is still MATCHING, so a late accept gets a 409. A decline or a timeout frees the driver for the next candidate. The expiry inside the condition is the lazy expiry of #94: nothing has to wake up to free a driver, so a crashed dispatcher leaves nothing locked. Every arrow of the trip's state machine is a conditional write of the same kind, so when a rider cancels just as the driver accepts, exactly one write commits.

```text
MATCHING ─accept→ ACCEPTED ─arrive→ ARRIVED ─start→ IN_PROGRESS ─end→ COMPLETED
MATCHING ─decline or 15 s timeout→ MATCHING again, offer the next candidate
MATCHING ─no driver within 2 minutes→ UNFULFILLED
MATCHING, ACCEPTED, ARRIVED ─cancel by rider or driver→ CANCELLED
```

Offering trips one at a time in arrival order is also greedy, and greedy matching wastes drivers when requests cluster.

```text
pickup ETA, minutes     driver X   driver Y
rider A                     2          5
rider B, 1 s later          3          9
one at a time   A→X 2 + B→Y 9 = 11 minutes, B waits 9
batched         A→Y 5 + B→X 3 =  8 minutes, nobody waits more than 5
```

Uber's matching does this: it waits a few seconds and pairs the nearby requests and drivers it has gathered to lower the total wait. Each request's Dijkstra search fills one row of the matrix, and the Hungarian algorithm solves the assignment exactly in O(n³). The cost is latency: each decline adds up to fifteen seconds, so dispatch caps the offers per trip, widens the rings between rounds and gives up after two minutes.

#### Surge pricing from sliding windows

Surge fixes a local imbalance: where riders outnumber available drivers, a higher price trims demand and pulls drivers in. An instantaneous count jumps whenever a bus empties or a driver turns a corner, and a price per city misses the stadium that just let out, so the design measures each S2 level-12 cell, about 5 km², over a five-minute sliding window.

Each cell keeps two counters as rings of ten 30-second buckets, the bucketed window of the hit counter (#45): every 30 seconds the oldest bucket is zeroed and reused, and the window's total is a sum of ten numbers. Demand counts quotes and requests with a pickup in the cell. Supply counts driver-seconds: each fix from an available driver adds four, so the total divided by 300 is the average number of available drivers over five minutes, and a car passing through counts for little. Once a minute the surge job, partitioned by cell, maps demand over supply through a curve that stays at 1.0 until demand clearly exceeds supply and then climbs to a cap. It then smooths twice. Each multiplier is blended with its eight neighbours', so the price does not jump at a street that happens to be a cell border, and it moves at most one step a minute, so noise does not make it flicker.

The quote locks the multiplier, so the trip costs what the rider saw even if the cell cools a minute later; that is why quotes expire. The cost is a lag of a minute or two, acceptable because drivers take minutes to respond too, and cell size trades noise for locality, since a small cell sees too few requests to measure. Uber built H3, a grid of hexagons, partly for this job: a hexagon's six neighbours all sit at one distance, which makes smoothing uniform, while a square's sit at two.

### Scaling and Bottlenecks

The location path breaks first, and it breaks by geography. Connection gateways and the location service scale out freely, but the geo index has hot spots: an airport or a stadium at peak packs thousands of drivers and searches into a few cells, so a hot level-12 cell is split among four servers by its children, and replicas absorb searches. Hashing a coarser cell would keep most searches on one server at the price of a lumpier spread, the dial between fan-out and balance. Nearby-car reads come from per-cell answers cached for two seconds.

Dispatch shards by area too, so requests that compete for the same drivers meet in one process; the busiest metro's few dozen requests a second fit one dispatcher. The ETA service is the costliest compute: 700 bounded searches a second are cheap, but 3,500 quote routes a second across whole cities need the contraction hierarchies of Chapter 14. Going multi-region is easy because a trip never leaves its city: each region runs the whole stack for its own cities, and only accounts, payment methods and ratings replicate globally.

### Failure Modes

Losing a geo index server loses nothing durable. Its cells move to the next servers on the hash ring, and within four seconds every driver in them reports again; replicas close even that gap, and a search that cannot reach a shard uses the rest and widens its rings. Drivers of a failed connection gateway reconnect elsewhere with jittered backoff and resend buffered fixes, and an offer lost meanwhile simply times out. A phone that loses signal drops out of the index after 30 seconds, but its trip carries on in the trip store and the app uploads its trace on reconnecting.

A dispatcher that dies leaves trips in MATCHING whose offers expire by themselves, and the trip service hands them to another dispatcher, because all matching state is on the trip row. Uber's 2015 dispatch system went further for datacenter failover, sending each driver's phone an encrypted digest of its trip state so that a new datacenter could rebuild trips from the phones' next updates. The trip store replicates synchronously across zones, so an acknowledged accept survives the loss of a zone. Events go to an outbox row in the same transaction and are relayed after the commit, so a crash in between only delays a charge. If the card processor is down, captures wait with their idempotency keys; if the surge job stalls, pricing ignores multipliers more than a few minutes old and falls back to 1.0.

### Trade-offs and Alternatives

The index trade is cells against trees: a fixed grid makes updates O(1), while an adaptive quadtree or an R-tree answers queries more tightly and pays on every move, which suits only places that never move. A smaller service needs no custom index: Redis's GEOADD and GEOSEARCH keep positions in a sorted set scored by a 52-bit geohash, and one instance holds a city's drivers comfortably.

Matching trades latency for quality: batching lowers the average wait at the cost of a few seconds, which pays only where requests are dense. Broadcasting a trip to several drivers and taking the first accept would match faster, but drivers who keep losing trips they accepted stop trusting offers. One grid for index and pricing keeps a single cell id flowing through the system; hexagons for pricing would cost a second grid.

### What Interviewers Probe

Expect five questions. How do you find nearby drivers fast? Cells in memory, searched ring by ring until the tenth-nearest driver lies inside the completed radius. How do you stop a driver getting two trips? A conditional write reserves the driver with an expiring offer, and one transaction commits the accept to trip and driver. What if the driver ignores the offer? It lapses after fifteen seconds with no timer, and the next candidate gets it. Is the nearest driver the best? No: rank by ETA from one reverse Dijkstra search, and batch where requests are dense. How does surge work? Windowed supply and demand per cell, a curve, smoothing in space and time, and a quote that locks the price.

Strong candidates raise three points unprompted: soft state at a high rate and hard state at a low rate, each in the storage that fits it; sharding by geography all the way down; and the phone as part of the system, buffering fixes, retrying idempotently, even backing up its own trip state. Interviewers care less about which grid you name than about keeping the location stream out of the database.

*Algorithms:* #148 Quadtree · #19 Top-K Elements · #42 Dijkstra's Algorithm · #139 Consistent Hashing · #94 Cache with Expiring Keys · #45 Design Hit Counter
