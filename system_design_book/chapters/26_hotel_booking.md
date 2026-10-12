---
rank: 26
slug: hotel_booking
---

A booking site like Airbnb lets a guest find a place to stay and reserve it for a run of nights. A guest pans the map over Lisbon, asks for two people from 30 December to 2 January, sees the few hundred homes that are free on all three nights, opens one and pays. Bookings are rare next to searches, but each one has to be exactly right, because a family that arrives to find another family in the flat is the failure the business cannot absorb. Three questions decide the design: how to search millions of listings by place and by dates when availability changes with every booking, how to guarantee that no night is sold twice when two guests click at the same moment, and how to keep the nights for a guest while a payment that can take minutes completes.

### Requirements

A guest searches by map area, dates and party size, with filters for price, property type and amenities, and gets back the listings that are free on every night of the stay, each with its total price. They open a listing to see its rules and a calendar of free nights, reserve it, pay, and may later cancel under the listing's cancellation policy. Hosts set nightly prices, minimum stays and blocked nights. A home is unique and takes one booking a night; a hotel lists room types instead, pools of identical rooms sold many times a night, and may deliberately sell a few more rooms than it has.

Assume ten million listings, a million bookings and a hundred million searches a day, and note that the two halves of the system want opposite things. Search must answer within 300 ms at the 99th percentile with 99.99% availability, and it may lag the true calendars by a few seconds. Booking may take a couple of seconds and may refuse requests during a database failover, but it must never sell a night of a home twice or a room type beyond its capacity plus its overbooking allowance. A confirmed reservation must survive the loss of a data centre, and a retried request must never create a second reservation or a second charge. Reviews, messaging, host payouts, photos (Chapter 19), price suggestions and fraud scoring are out of scope.

### Estimates

```text
listings      10 M (9 M homes, 1 M hotel room types), calendars a year ahead
bookings      1 M per day / 86,400 s ≈ 12/s (peak ×5: 60/s), 4 nights each
holds         2 per booking (half of checkouts abandoned) ≈ 23/s, peak 120/s
occupancy     4 M nights/day × 365 = 1.46 B of 3.65 B listing-nights ≈ 40%
searches      100 per booking = 100 M/day ≈ 1,200/s (peak ×3: 3,500/s)
page views    30 per booking = 30 M/day ≈ 350/s, each reads 3 months of nights
search CPU    3,500/s × 20 ms ≈ 70 busy cores → a dozen 16-core replicas
index         10 M × 2 KB (location, attributes, rules, base price) ≈ 20 GB
calendars     365 bits ≈ 46 B × 10 M ≈ 460 MB; prices 2 B × 365 × 10 M ≈ 7 GB
index feed    2 M holds + 1 M expiries + 10 M host edits ≈ 13 M/day ≈ 150/s
claims        4 M nights/day kept a year → 1.5 B rows × 50 B ≈ 75 GB
counters      1 M room types × 365 nights = 365 M rows × 50 B ≈ 18 GB
reservations  1 M/day × 1 KB ≈ 365 GB a year, 3.7 TB over ten years
```

Three numbers shape the design. Searches outnumber bookings a hundred to one and each asks about thousands of listings, so search runs from memory and never touches the database that takes bookings. Bookings and holds together peak at about 120 a second, a load one relational database could carry, so the inventory database is sharded for headroom rather than throughput, and it can afford real transactions, a row for every claimed night and a constraint checked on every write. And the whole search index, a year of availability and prices included, is under 30 GB, which fits in one machine's memory: every search replica holds all of it, no query scatters across shards, and capacity grows by adding replicas.

### API

```text
GET  /api/v1/search?bbox=38.69,-9.23,38.80,-9.09&check_in=2026-12-30
          &check_out=2027-01-02&guests=2&max_price=350&cursor=<opaque>
     200 {"results": [{"listing_id": "L82", "total": 912.00, "rating": 4.9}],
          "next_cursor": "..."}

GET  /api/v1/listings/{id}                   200 {title, rules, amenities, ...}
GET  /api/v1/listings/{id}/calendar?from=2026-12-01&months=3
     200 {"nights": [{"date": "2026-12-30", "free": true, "price": 290.00}]}
PUT  /api/v1/listings/{id}/calendar          host: prices, minimum stays, blocks
     200 updated                             409 a night is already booked

POST /api/v1/reservations                    Idempotency-Key: <uuid>
     {"listing_id": "L82", "check_in": "2026-12-30", "check_out": "2027-01-02",
      "guests": 2, "expected_total": 912.00, "payment_method": "pm_7Q"}
     201 {"reservation_id": "R5", "status": "held" | "confirmed",
          "hold_expires_at": "...", "next_action": "3ds" | null}
     409 nights taken or price changed       422 breaks a rule (minimum stay)

GET  /api/v1/reservations/{id}
     200 {"status": "held" | "confirmed" | "expired" | "canceled", ...}

POST /api/v1/reservations/{id}/cancel        Idempotency-Key: <uuid>
     200 {"status": "canceled", "refund": 456.00}
```

Search takes the visible map area as a bounding box and pages with an opaque cursor; availability can move between pages, which a results page tolerates. The reservation call carries an `Idempotency-Key`, stored on the reservation row itself, so a retry after a timeout or a second click returns the original reservation instead of creating another. It also carries the total the guest was shown, and if the host has changed a price in the meantime, the service answers 409 with the new total rather than charge an amount the guest never saw. A 201 with status `held` means the nights are taken and the payment is still running, for example while the guest answers a 3-D Secure challenge from their bank, and the client polls the reservation until it is confirmed or has expired.

### Data Model

```text
listings      listing_id PK | host_id | kind (home | room_type) | lat, lng
              | tz | max_guests | units | min_nights | base_price | policy
night_rules   (listing_id, night) PK | price | min_nights      sparse overrides
claims        (listing_id, night) PK | reservation_id     homes: taken nights
inventory     (listing_id, night) PK | units | sold | overbook    room types
              CHECK (sold <= units + overbook)
reservations  (listing_id, reservation_id) PK | guest_id | check_in
              | check_out | rooms | status | hold_expires_at | total
              | policy (copied at booking) | idem_key
              UNIQUE (listing_id, idem_key), INDEX (status, hold_expires_at)
              inventory DB: the four tables above, sharded by hash(listing_id)
by_guest      (guest_id, check_in) → (listing_id, reservation_id)
              sharded by guest_id, filled asynchronously
```

Every row a booking touches, the reservation and its claims or counters, leads with `listing_id`, and the inventory database is sharded by a hash of it, so a booking is a single-shard transaction and each shard enforces its unique keys alone. A relational database fits because writes are modest and the design leans on what relational databases do best, multi-row transactions and constraints; MySQL under Vitess or PostgreSQL with Citus shards this way. A home's claims hold a row only for a night that is taken, by a stay, a hold or a host's block (a reservation with no guest), so free nights cost nothing. A room type needs a counter for every future night, since a counter must exist before it can be checked, and a daily job adds the night that has just come within a year. A night is a date in the listing's time zone, so neither daylight saving nor the guest's location can shift it. The cancellation policy is copied onto the reservation, so a host who tightens it later cannot change a stay already sold. Listing descriptions live in their own listings DB, and the by_guest table behind a guest's list of trips is kept up to date from the change stream, off the booking path.

### Architecture

```dot
rankdir=TB;
guest   [label="guest app", class=client];
host    [label="host app", class=client];
gw      [label="API gateway", class=edge];
search  [label="search replicas\nquadtree + calendars"];
listing [label="listing service"];
booking [label="booking service"];
sweeper [label="hold sweeper", class=worker];
listdb  [label="listings DB", class=store];
invdb   [label="inventory DB\nsharded by listing", class=store];
pay     [label="payment service"];
psp     [label="payment provider", class=external];
cdc     [label="change stream", class=queue];
indexer [label="index builder", class=worker];
notify  [label="notification\nservice"];
guest -> gw [label=" search, book"];
host -> gw [label=" prices, blocks"];
gw -> search [label=" GET /search"];
gw -> listing [label=" listing page"];
gw -> booking [label=" reservations,\n calendars"];
listing -> listdb;
booking -> invdb [label=" claim, confirm"];
sweeper -> invdb [label=" expire holds"];
booking -> pay [label=" authorize"];
pay -> psp [dir=both, label=" charge,\n webhook"];
invdb -> cdc [style=dashed, label=" CDC"];
listdb -> cdc [style=dashed];
cdc -> indexer [style=dashed];
search -> indexer [dir=back, style=dashed, label=" bits, prices"];
pay -> cdc [dir=back, style=dashed, label=" capture"];
cdc -> notify [style=dashed, label=" confirmed"];
{rank=same; guest; host}
{rank=same; search; listing; booking; sweeper}
```

The read path starts at the guest app. The API gateway sends a search to any of the search replicas, each holding the whole index in memory: a quadtree over listing coordinates, the attributes the filters need, and every listing's calendar for the coming year as a bitmap with its nightly prices. The replica finds the listings inside the map area, drops those that fail a filter or are taken on any night of the stay, totals the survivors' prices, ranks them and returns a page without a single network call. A listing page comes from the listing service, which reads the listings DB, and its calendar from the booking service, which reads a replica of the inventory DB, because a guest about to choose dates deserves fresher data than the index.

The write path runs through the booking service, which owns the inventory DB. A reservation claims the nights in one short transaction and commits them as a hold, asks the payment service (Chapter 24) to authorize the guest's card with the payment provider, and then confirms in a second transaction. Hosts' prices and blocks arrive from the host app through the same service and the same claims, so a host can never block a night a guest has just booked. The hold sweeper releases holds whose payment never completed.

The asynchronous path starts at the databases. Change data capture reads the commit logs of both databases into the change stream, a Kafka topic partitioned by `listing_id` so that each listing's changes stay in order, and the index builder applies them to every search replica within a few seconds. The same stream carries a confirmation's side effects: the payment service captures the authorized amount, and the notification service (Chapter 20) tells the guest and the host. Because these effects follow committed rows, a crash just after a commit delays an email but never loses it; the change stream plays the part of the transactional outbox of Chapter 24.

### Deep Dives

#### No double bookings: one row per claimed night

The naive booking checks that no existing reservation overlaps the requested dates, the overlap test of My Calendar I (#98), and inserts the new one if none does. Two guests who ask at the same moment for 30 December to 2 January and for 31 December to 3 January both see no overlap, both insert, and both commit. A transaction does not save them under snapshot isolation, which is what PostgreSQL's repeatable read provides, because the two write different rows and nothing in them conflicts. This is write skew, and only serializable isolation catches it, by aborting one of the two.

Pessimistic locking makes the writers take turns: each booking first locks the listing's own row with `SELECT ... FOR UPDATE`, a row that always exists, and only then checks and inserts. It is correct only as long as every code path that touches a calendar, from host blocks to calendar imports and support tools, takes the same lock, and one lock per listing queues a hotel's hundreds of rooms behind a single row. Optimistic versioning avoids the waiting by writing the calendar back only if its version has not moved since it was read. Collisions are rare for a home, but every price edit by the host fails a booking in flight, and on a contested night the retries pile up.

The simplest guarantee is a constraint. The claims table has the primary key (listing_id, night), and a booking inserts its reservation and one claim per night in a single transaction. If any night is already taken, the insert of that night violates the key and the whole transaction rolls back, leaving no partial stay behind. The database checks a unique key against uncommitted rows too, so of two racing guests the second waits and fails the moment the first commits. Nothing is read first, no lock has to be remembered, no retry loop is needed, and the guarantee holds at read committed. Host blocks and imported calendars are claims as well, so one constraint protects every writer, and because the key starts with the shard key, each shard enforces it alone. The costs are about four rows per booking, deletes on cancellation and expiry, and inserting the nights in date order so that two overlapping stays queue behind each other instead of deadlocking.

```text
BEGIN;                                                -- a home, three nights
INSERT INTO reservations (listing_id, reservation_id, guest_id, check_in,
       check_out, status, hold_expires_at, idem_key)
VALUES ('L82', 'R5', 'G7', '2026-12-30', '2027-01-02', 'HELD',
       now() + interval '10 minutes', 'k-3f9');
INSERT INTO claims (listing_id, night, reservation_id)
VALUES ('L82', '2026-12-30', 'R5'), ('L82', '2026-12-31', 'R5'),
       ('L82', '2027-01-01', 'R5');      -- duplicate key → ROLLBACK, 409
COMMIT;

UPDATE inventory SET sold = sold + 1                  -- a hotel room type
 WHERE listing_id = 'H3-KING' AND night >= '2026-12-30'
   AND night < '2027-01-02' AND sold + 1 <= units + overbook;
                                 -- 3 rows → claimed; fewer → ROLLBACK, 409
```

A hotel room type breaks the one-booking-per-night rule on purpose, the situation of My Calendar II (#98), where overlaps are allowed up to a limit. Its rows are counters, one per night, and a booking adds its rooms with a guarded update that must match every night of the stay. At read committed each update locks its row and re-checks the condition against the latest committed value, with the CHECK constraint as a backstop, and a lock held for a few milliseconds still allows a few hundred bookings a second on one night. The `overbook` column is the hotel's overbooking policy made explicit. Revenue management sets it per night from the history of no-shows and late cancellations, and on the rare night when every guest turns up, the front desk walks one to a comparable hotel at the hotel's expense. Homes keep it at zero, since a unique flat has no twin to send the second family to.

#### Search by place and dates

Finding listings near a place is the proximity search of Chapter 27. Each replica keeps a quadtree (#148) over listing coordinates, split until no leaf holds more than a few hundred listings, so a map of central Lisbon visits a handful of small leaves. Dates are the hard part. Asking the inventory DB which candidates are free fails on volume: a whole-city view holds about 30,000 listings, so 3,500 searches a second would become a hundred million claim lookups a second against the database that takes bookings. Precomputing the free listings for every possible stay fails the other way, because a year holds more than ten thousand distinct stays of up to a month and a single booking changes the answer for every stay that overlaps it.

The chosen structure is a bitmap per listing. Bit i is set when the night i days into the window is claimed, blocked or closed, so a year takes 365 bits and all ten million calendars 460 MB. A stay from night i to night j is free when the bitmap AND a mask of bits i through j - 1 is zero, a few machine-word operations per candidate, so 30,000 candidates filter in well under a millisecond. The bitmap is a Range Module (#142) over a one-year horizon: a booking removes a range, a cancellation adds it back, and a search asks whether a whole range is still free.

```text
night        0 1 2 3 4 5 6 7 8 9 …   (0 = first night of the window)
calendar     0 0 1 1 0 0 0 0 1 0 …   (1 = claimed, blocked or closed)
stay 4 → 7   0 0 0 0 1 1 1 0 0 0 …   calendar & mask = 0 → all three free
stay 6 → 9   0 0 0 0 0 0 1 1 1 0 …   calendar & mask ≠ 0 → night 8 taken
```

Minimum stays and allowed check-in days are checked in the same pass, and the nightly prices beside the bitmap let the replica total each stay for sorting and for the price filter. Flexible dates, a weekend in December or a week in March, intersect the bitmap's free runs with the guest's acceptable windows, the two-pointer walk of Interval List Intersections (#66), and any piece at least as long as the stay is a stay the listing can take.

The cost is staleness. A listing booked a second ago can still appear in results, and the guest who tries to book it gets a 409 from the claim and a list of similar listings. Search is a hint and the claim is the truth, which is why the index never needs to be transactionally consistent with the database. Holds set bits too, so an abandoned checkout hides a listing for up to ten minutes, one more reason to keep holds short.

#### Holds, payment and idempotent reservations

Payment is the slow, external step in the middle of a booking, and both naive orders fail. Keeping the claiming transaction open while the card is charged holds rows locked and a connection busy for seconds, or minutes if the bank asks for a 3-D Secure challenge, so a slow payment provider becomes a database outage. Charging first and claiming afterwards means refunding every guest who loses the race.

So a booking is two short transactions with the payment between them. The first claims the nights as a hold: the reservation is `HELD`, with `hold_expires_at` ten minutes ahead by the database's clock, so application servers with skewed clocks cannot disagree about it. The booking service then has the payment service authorize the total without capturing it, keyed by the reservation id so that a retry can never authorize twice. When the authorization succeeds, at once for most cards or through the provider's webhook after a challenge, the second transaction moves the row from `HELD` to `CONFIRMED` only if it is still `HELD`, and the committed confirmation, read from the change stream, triggers the capture and the emails. A request-to-book listing, whose host has a day to accept, keeps the hold for that day with only the authorization taken.

Expiry is the competing transition. The hold sweeper scans each shard every few seconds through the index on `(status, hold_expires_at)`, moves overdue holds to `EXPIRED`, deletes their claims and voids their authorizations, and a booking that collides with an expired hold does the same on the spot and retries once. This is a cache with expiring keys (#94) in database form, lazy expiry when a key is touched and a periodic sweep for the rest. Confirm and expire are conditional updates of the same row, so exactly one of them wins, and because the booking service extends a hold while an authorization is in progress, a payment that outlives its hold is rare and costs a voided authorization, never a double booking.

The `Idempotency-Key` sits on the reservation under UNIQUE (listing_id, idem_key), so a retry or a second click finds the existing reservation and returns its state, and a flow that crashed between the hold and the payment resumes from there. Cancellation is one more conditional transition, `CONFIRMED` to `CANCELED`, committed together with deleting the claims or decrementing the counters. The refund follows the policy copied onto the reservation and reaches the payment service under the cancellation's own key, and the freed nights reach search through the change stream.

### Scaling and Bottlenecks

Search is the tier that grows. Replicas are identical, so capacity means adding more of them, a few in each region near the guests. The bitmap filter costs well under a millisecond, so nearly all of the 20 ms per search goes to ranking, and the first lever is a cheap pre-score that sends only the best few hundred candidates to the full model. If the index ever outgrows memory, it splits by region along quadtree cells, and a map that straddles a border queries two shards. Applying every change, about 150 a second, costs each replica almost nothing.

The inventory DB is sharded by a hash of `listing_id` rather than by geography, so a festival in one city spreads its bookings across all shards. The hottest unit is one row, a large hotel's room type on New Year's Eve, and even that takes a few hundred bookings a second. Unlike the on-sales of Chapter 25, where a hundred thousand fans want the same seats in the same minute and a waiting room is the only answer, demand for stays spreads over millions of listings and nights, so the database absorbs the contention directly. Each listing's rows live in a home region near the listing; a booking from another continent pays a round trip of a hundred milliseconds or so on a step that already waits on a bank, while search replicas run in every region.

### Failure Modes

If an inventory shard's primary fails, a synchronous replica in another zone takes over within seconds. Transactions in flight abort and clients retry with the same idempotency key, which is exactly what the key is for, and meanwhile bookings on that shard fail with 503 while search and the other shards carry on: the system would rather refuse a booking than sell a night twice. If the change stream or the index builder stalls, search grows stale but stays up and more guests meet a 409. Lag is monitored per partition, and a restarted replica loads the latest index snapshot, which records the stream offset it reflects, and replays from there.

If the payment provider is slow, the booking service extends the pending holds and the payment service can fail over to a second provider (Chapter 24); holds that do expire release their nights to other guests, so an outage costs bookings, never inventory. If the hold sweeper stops, expired holds hide their nights from search, but colliding bookings still expire them, so correctness survives. A duplicate webhook meets a conditional update and changes nothing. What no transaction can stop is a host who lists the same home on another site. Calendar feeds in iCal format, which each site polls, narrow that gap, hotels push availability everywhere through channel managers, and a booking that still slips through is resolved by rebooking the guest.

### Trade-offs and Alternatives

The central choice is where the guarantee lives. Claim rows put it in a unique key, which any relational database enforces and a key-value store expresses as a conditional put; DynamoDB can write a stay's nights as one transaction of puts conditioned on the key not existing. PostgreSQL can state the rule directly with an exclusion constraint, `EXCLUDE USING gist (listing_id WITH =, stay WITH &&)` over a date range, using the btree_gist extension for the equality: one row per reservation instead of one per night, at the price of a GiST index and a feature most databases lack. Serializable isolation would make even the naive check-then-insert correct, but it pays with aborts under contention and leaves correctness to whatever isolation level each code path uses.

Bitmaps inside each replica are fast but custom. A site with a few hundred thousand listings should use Elasticsearch instead, indexing booked periods in a `date_range` field and excluding listings whose periods intersect the stay with a must-not clause, and accept that every booking re-indexes a document that becomes searchable only after the next refresh, a second later by default. Holds trade inventory for certainty: a ten-minute hold occasionally hides a listing from a guest who would have paid, while a site without holds must charge inside the claim or refund the losers. Overbooking trades a rare walked guest for fuller hotels, a trade homes cannot make.

### What Interviewers Probe

Expect the conversation to circle six questions. How do you prevent double bookings? One claim row per night under a unique key, inserted with the reservation in one transaction. Why is a transaction that checks and then inserts not enough? Write skew: under snapshot isolation both transactions commit. Pessimistic or optimistic locking? Neither for homes, because the constraint is simpler; for hotel counters, a guarded update that locks each night's row for a few milliseconds. What if the payment succeeds after the hold expired? Authorize during the hold, capture only after the confirmation commits, and void the authorization if expiry won. How does search know availability at 3,500 queries a second? In-memory bitmaps fed by change data capture, seconds stale, with the claim as the final check. How do retries stay safe? An idempotency key stored on the reservation under a unique constraint.

Strong candidates raise four more points unprompted: host blocks and calendar imports must go through the same claims, or the guarantee has a hole; holds expire by the database's clock; a night is a date in the listing's time zone; and the overbooking allowance is a business policy stored as data, not a bug the code tolerates. Above all, interviewers listen for the moment the candidate splits the system into a search that may be stale and a booking that must be exact, because the rest of the design follows from that split.

*Algorithms:* #98 My Calendar I and II · #142 Range Module · #66 Interval List Intersections · #148 Quadtree · #94 Cache with Expiring Keys
