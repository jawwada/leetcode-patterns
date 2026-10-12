# Design Underground System

*LeetCode 1396 · Medium · Pattern: Two hash maps (in-flight state + aggregated statistics) · Reading time ~7 min*

## The problem

Implement UndergroundSystem: checkIn(id, station, t), checkOut(id, station, t), and getAverageTime(start, end) -> the
mean travel time over all completed trips from start to end so far. A customer is checked in at most once at a time
and every queried route has at least one trip.

```text
Example: 45 checks in at Leyton@3 and out at Waterloo@15, 27 in
  at Leyton@10 and out at Waterloo@20 -> getAverageTime(Leyton,
  Waterloo) = (12 + 10) / 2 = 11.0.
```

## What the problem is really asking

A metro system records passengers. `checkIn(id, station, t)` says passenger `id` entered at `station` at time `t`. `checkOut(id, station, t)` says they left at `station` at time `t`. `getAverageTime(start, end)` returns the mean travel time of all *completed* trips that went from `start` to `end` — direction matters, so A→B and B→A are different routes. A passenger is inside at most one journey at a time, and a queried route always has at least one completed trip.

The answer to a query is a float. The state has to bridge two calls that belong together (a check-in and its later check-out) and also accumulate a statistic over every trip ever made. What makes it interesting is deciding how much of that history you actually need.

```text
 45: Leyton@3   -> Waterloo@15    12 min
 27: Leyton@10  -> Waterloo@20    10 min
 32: Paradise@8 -> Cambridge@22   14 min
 avg(Leyton, Waterloo) = (12 + 10) / 2 = 11.0
```

## Do it by hand first

You are the station clerk with two sheets of paper.

When someone taps in, you jot on sheet one: "45 — Leyton, 3". When they tap out at Waterloo at 15, you find their line, compute 15 - 3 = 12, and cross the line out — that journey is over. Now you need to remember the 12 somewhere for future averages. Do you write "Leyton→Waterloo: 12" on sheet two, and later "Leyton→Waterloo: 10" underneath? When someone asks for the average, you would add up the column. A sharper clerk keeps just two numbers per route on sheet two: total minutes and number of trips. Each finished trip adds to both.

```text
 sheet 1 (open journeys)     sheet 2 (routes)
 45: Leyton, 3   (crossed)   Leyton->Waterloo: 12 min, 1 trip
 32: Paradise, 8
 27: Leyton, 10
```

Your hand kept two kinds of facts with very different lifetimes: open journeys, which live from tap-in to tap-out, and route totals, which live forever but never grow beyond two numbers.

## The first honest attempt

Keep the open journeys in a dict, and on checkout append `(start, end, duration)` to a list of trips. `getAverageTime` filters the list for the route, sums, and divides.

`checkIn` and `checkOut` are O(1). `getAverageTime` is O(T) for T trips ever completed, and memory grows by one record per trip forever.

```text
 trips: (L,W,12) (P,C,14) (L,W,10) (L,W,14) (A,B,5) ...
 avg(L,W) asked 3 times:
  q1 sums 12+10         = 22 / 2
  q2 sums 12+10+14      = 36 / 3   <- 12 and 10 re-added
  q3 sums 12+10+14+...         <- re-added again
```

The repeated work: a completed trip never changes, yet every query re-reads and re-adds it, along with every unrelated trip in the log.

## The turning point

**Claim: an average is fully determined by a sum and a count, and both can be updated by one addition each when a trip completes.**

Justification: the mean of durations d1..dk is (d1 + ... + dk) / k. Adding a new trip d(k+1) changes the sum by d(k+1) and the count by 1. Nothing about the individual earlier trips is needed for any future query, because queries only ask for averages.

So aggregate eagerly. Apply the chapter's method:

- `checkOut` must know where and when this passenger started → `in_transit: id -> (station, t)`, written by `checkIn`, popped by `checkOut`.
- `getAverageTime` must know the total and count for a route → `stats: (start, end) -> [total, count]`, updated by `checkOut`.

Each operation touches one entry of one or two maps. Notice how the two maps differ in lifetime: `in_transit` entries are born at check-in and die at check-out, so its size is the number of people currently on the network; `stats` entries live forever but there is only one per route that has ever been travelled, regardless of how many trips.

The key must be the *ordered pair* `(start, end)`. Keying by start alone mixes destinations; keying by an unordered pair mixes directions.

What the tracker remembers: open journeys, and two numbers per route. What it forgets: every individual completed trip, the moment it is folded into its route's totals.

```text
 start, t0 = in_transit.pop(id)
 cell = stats.setdefault((start, station), [0, 0])
 cell[0] += t - t0
 cell[1] += 1
```

## Watch it work

The example from the problem, then one extra trip: check in 45, 32, 27; check out 45, 27, 32; query; check in 10; check out 10; query. L = Leyton, W = Waterloo, P = Paradise, C = Cambridge.

```text
Frame 1  checkIn 45@L,3  32@P,8  27@L,10
 in_transit: {45:(L,3), 32:(P,8), 27:(L,10)}
 stats:      {}
```
Three open journeys; no trip has completed, so no statistics yet.

```text
Frame 2  checkOut(45, W, 15)
 pop 45 -> (L,3); duration 15-3 = 12
 in_transit: {32:(P,8), 27:(L,10)}
 stats:      {(L,W): [12, 1]}
```
The journey is removed from the open map and folded into its route.

```text
Frame 3  checkOut(27, W, 20); checkOut(32, C, 22)
 27: 20-10 = 10  -> (L,W): [22, 2]
 32: 22-8  = 14  -> (P,C): [14, 1]
 in_transit: {}
```
The second Leyton trip adds to the same cell; Paradise gets its own.

```text
Frame 4  getAverageTime(L, W) -> 11.0
 stats[(L,W)] = [22, 2] -> 22 / 2
```
One lookup and one division, no matter how many trips exist.

```text
Frame 5  checkIn(10, L, 24)
 in_transit: {10:(L,24)}
 stats: {(L,W):[22,2], (P,C):[14,1]}
```
An open journey does not affect any average yet.

```text
Frame 6  checkOut(10, W, 38); getAverageTime(L, W) -> 12.0
 duration 38-24 = 14 -> (L,W): [36, 3]
 in_transit: {}
 36 / 3 = 12.0
```
The new trip shifts the average; the old trips were never revisited.

Through every frame, each stats cell equals the sum and count of all completed trips on that route, and in_transit holds exactly the passengers currently inside.

## Why it is correct

Invariant: (1) `in_transit` contains exactly the passengers who have checked in but not yet out, with their start station and time; (2) for every ordered pair `(s, e)`, `stats[(s, e)]` holds the sum and count of durations of all completed trips from s to e. `checkIn` adds one open journey, preserving (1). `checkOut` removes the passenger's open journey (preserving 1) and adds exactly that trip's duration and one to its route's cell (preserving 2). Given (2), `total / count` is by definition the mean of all completed trips on the route, which is what `getAverageTime` must return.

## Cost

- **Time:** O(1) average per operation — a constant number of dict operations and arithmetic.
- **Space:** O(P + R) — P passengers currently in transit plus R distinct routes travelled; no per-trip storage.

The trip-log version is O(T) per query and O(T) space, T being trips ever completed.

## Variations you will meet

- **Average over the last k trips, or the last hour.** Sum and count are no longer enough; each route needs its own queue with a running sum — the moving average or the hit counter, one per key.
- **Median or percentile travel time.** Averages compress to two numbers; medians do not. Each route needs two heaps or a sorted structure.
- **Average as of a past time.** Keep, per route, a list of (time, running total, running count) and bisect by time — the next problem's idea.
- **Invalid input (checkout without check-in).** In production, `in_transit.pop(id, None)` and decide what to log; in the interview, say the guarantee lets you skip it.

## What to carry forward

Split state by lifetime — short-lived in-flight records in one map, permanent statistics compressed to (sum, count) in another — and fold each event in the moment it completes. The next problem keeps the history instead of compressing it: every value a key ever had, so you can ask what it was at time t.
