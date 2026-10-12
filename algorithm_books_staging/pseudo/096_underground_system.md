---
rank: 96
slug: underground_system
---

Design the tracker behind a metro's fare gates. `check_in(card_id, station, t)` records a card entering, `check_out(card_id, station, t)` records the same card leaving, and `get_average_time(start, end)` returns the average duration of every finished trip that went from `start` to `end`. A card has at most one open trip, every trip ends later than it began, and a query always names a route with at least one finished trip. A card that enters at Leyton at time 3 and leaves at Waterloo at 15 rides for 12 minutes; with a second Leyton-to-Waterloo trip of 10 minutes, the average is `11.0`.

The brute force logs every finished trip and scans the log on each query, `O(trips)` per average, and every scan re-adds numbers that can never change again. An average is a total divided by a count, and both grow by a single addition when a trip ends, so the tracker can do the work at write time and keep just those two numbers per route. That is the core pattern of tracker designs: decide what the reads will ask, aggregate it as the writes arrive, and make every read a lookup. Two maps hold the whole state, one for each lifetime of the data. `open_trips` sends each card in the system to where and when it entered, and an entry lives only from check-in to check-out. `routes` sends each ordered pair `(start, end)` to its `[total_time, count]`, and an entry lives forever, in two numbers. A check-out moves a trip from the first map into the second: it removes the card's entry, computes the duration and folds it into its route's totals, so a trip is forgotten the moment it is counted.

Picture the open trips as a waiting room and the routes as a grid of counters, one cell per ordered pair of stations. A check-in walks into the waiting room, a check-out walks out and adds one trip to one cell, and a query divides the two numbers in one cell.

```text
after the three check-ins, open_trips holds
    45 → (Leyton, 3)     32 → (Paradise, 8)     27 → (Leyton, 10)

call                          trip time      routes cell after the call
check_out(45, Waterloo, 15)   15 - 3 = 12    (Leyton, Waterloo) → [12, 1]
check_out(27, Waterloo, 20)   20 - 10 = 10   (Leyton, Waterloo) → [22, 2]
check_out(32, Cambridge, 22)  22 - 8 = 14    (Paradise, Cambridge) → [14, 1]
get_average_time(Paradise, Cambridge) = 14 / 1 = 14.0
get_average_time(Leyton, Waterloo)    = 22 / 2 = 11.0
check_in(10, Leyton, 24)      still open     no cell changes
get_average_time(Leyton, Waterloo)    = 22 / 2 = 11.0
check_out(10, Waterloo, 38)   38 - 24 = 14   (Leyton, Waterloo) → [36, 3]
get_average_time(Leyton, Waterloo)    = 36 / 3 = 12.0
open_trips is empty again
```

```pseudo
CLASS UndergroundSystem
    FUNCTION Init()
        self.open_trips ← empty map     // card_id → (start station, start time)
        self.routes ← empty map         // (start, end) → [total_time, count]

    FUNCTION CheckIn(card_id, station, t)
        self.open_trips[card_id] ← (station, t)

    FUNCTION CheckOut(card_id, station, t)
        (start, start_time) ← self.open_trips[card_id]
        self.open_trips.remove(card_id)     // the trip is over
        route ← (start, station)            // direction matters
        IF route NOT IN self.routes
            self.routes[route] ← [0, 0]     // [total_time, count]
        self.routes[route][0] ← self.routes[route][0] + t - start_time
        self.routes[route][1] ← self.routes[route][1] + 1

    FUNCTION GetAverageTime(start, end)
        (total_time, count) ← self.routes[(start, end)]
        RETURN total_time / count
```

Every call is a constant number of hash-map operations, so each runs in `O(1)`, and the memory is one entry per card in the system plus one per route ever completed, never one per trip. The signals are averages, counts, sums and totals asked again and again over a stream of events: the tracker answers in `O(1)` because it stores the ingredients of the answer instead of the events. Ask for a median or a percentile and two numbers no longer suffice; the values themselves must be kept, as in the two heaps of #21. The hit counter of #45 aggregates the same way, one counter per second instead of per route, and Design A Leaderboard keeps each player's running score as it arrives. The classic mistakes are keying the totals by the start station alone or by an unordered pair, although Leyton to Waterloo and Waterloo to Leyton are different routes, and forgetting to remove the card at check-out, so that `open_trips` keeps every card that ever rode and no longer tells who is inside. In a language whose `/` truncates integers, the average must be computed in floating point.

*Practice:* LC 1396 Design Underground System · LC 362 Design Hit Counter · LC 1244 Design A Leaderboard · LC 2034 Stock Price Fluctuation
