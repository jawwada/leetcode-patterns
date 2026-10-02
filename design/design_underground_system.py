"""
Design Underground System (LeetCode 1396)  — Medium
Pattern: Two hash maps (in-flight state + aggregated statistics)

Problem
-------
Implement UndergroundSystem: checkIn(id, station, t), checkOut(id, station, t), and
getAverageTime(start, end) -> mean travel time over ALL completed trips from start to end so
far. A customer is checked in at most once at a time; every queried route has >= 1 trip.
Example: 45 in Leyton@3, out Waterloo@15; 32 in Paradise@8, out Cambridge@22; 27 in Leyton@10,
out Waterloo@20 -> avg(Leyton,Waterloo) = (12 + 10) / 2 = 11.0.

Brute force
-----------
Record every completed trip as (start, end, duration) in a list; getAverageTime scans the list,
summing durations and counting trips for that route. O(1) checkIn/checkOut, O(trips) per
query, O(trips) space. The wasted work is re-summing the same completed trips on every query,
although none of them can ever change once recorded.

From brute force to optimal
---------------------------
An average is fully determined by (sum, count), and both are updated by a single addition when
a trip completes. So aggregate eagerly: stats[(start, end)] = [total_time, trip_count], updated
in checkOut; getAverageTime becomes one dict lookup and one division. checkOut needs the
customer's start station and time, so a second map in_transit[id] = (station, t) holds that
until checkout and is deleted immediately after. The tracker remembers per-route running
totals and per-customer in-flight state; it can forget individual trips the moment they are
folded into the totals.

Intuition
---------
Separate the two lifetimes of data: a customer's open journey lives briefly (one map keyed by
id, popped on checkout); a route's statistics live forever but compress to two numbers (one
map keyed by (start, end)). Each operation touches exactly one entry of one map.

Geometric view
--------------
in_transit: { 45: (Leyton, 3),  32: (Paradise, 8) }        <- open journeys
checkOut(45, Waterloo, 15) pops 45, and adds 12 to:
stats: { (Leyton, Waterloo): [12, 1],  ... }                 <- closed routes
Later trips keep adding to the same cell; the query reads total / count.

Steps
-----
1. in_transit = {} ; stats = {}.
2. checkIn: in_transit[id] = (station, t).
3. checkOut: start, t0 = in_transit.pop(id); cell = stats.setdefault((start, station), [0, 0]);
   cell[0] += t - t0; cell[1] += 1.
4. getAverageTime: total, count = stats[(start, end)]; return total / count.

Complexity: O(1) time per operation, O(customers in transit + distinct routes) space —
            each call is a constant number of dict operations.
Pitfalls: keying stats by start station only (route = ordered pair); not popping the customer
          on checkout (stale entry, memory leak); integer division.
"""
import random


class UndergroundSystem:
    def __init__(self):
        self.in_transit = {}    # id -> (start station, check-in time)
        self.stats = {}         # (start, end) -> [total travel time, trip count]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.in_transit[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start, t0 = self.in_transit.pop(id)
        cell = self.stats.setdefault((start, stationName), [0, 0])
        cell[0] += t - t0
        cell[1] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total, count = self.stats[(startStation, endStation)]
        return total / count


class BruteForce:
    """Log every finished trip; getAverageTime re-scans the whole log, O(trips)."""

    def __init__(self):
        self.open = {}
        self.trips = []

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.open[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start, t0 = self.open.pop(id)
        self.trips.append((start, stationName, t - t0))

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        durations = [d for s, e, d in self.trips if s == startStation and e == endStation]
        return sum(durations) / len(durations)


if __name__ == "__main__":
    u = UndergroundSystem()
    u.checkIn(45, "Leyton", 3)
    u.checkIn(32, "Paradise", 8)
    u.checkIn(27, "Leyton", 10)
    u.checkOut(45, "Waterloo", 15)
    u.checkOut(27, "Waterloo", 20)
    u.checkOut(32, "Cambridge", 22)
    assert u.getAverageTime("Paradise", "Cambridge") == 14.0
    assert u.getAverageTime("Leyton", "Waterloo") == 11.0
    u.checkIn(10, "Leyton", 24)
    assert u.getAverageTime("Leyton", "Waterloo") == 11.0     # open journey doesn't count
    u.checkOut(10, "Waterloo", 38)
    assert u.getAverageTime("Leyton", "Waterloo") == 12.0

    e = UndergroundSystem()                                   # edge: same customer id re-used
    e.checkIn(1, "A", 0)
    e.checkOut(1, "B", 5)
    e.checkIn(1, "B", 6)
    e.checkOut(1, "A", 7)
    assert e.getAverageTime("A", "B") == 5.0 and e.getAverageTime("B", "A") == 1.0

    random.seed(7)
    fast, slow = UndergroundSystem(), BruteForce()
    stations, open_ids, t = "ABCD", set(), 0
    for _ in range(1500):
        t += 1
        r = random.random()
        if r < 0.4:
            cid = random.randint(0, 30)
            if cid not in open_ids:
                st = random.choice(stations)
                fast.checkIn(cid, st, t)
                slow.checkIn(cid, st, t)
                open_ids.add(cid)
        elif r < 0.8 and open_ids:
            cid = random.choice(sorted(open_ids))
            st = random.choice(stations)
            fast.checkOut(cid, st, t)
            slow.checkOut(cid, st, t)
            open_ids.remove(cid)
        elif slow.trips:
            s, e_, _ = random.choice(slow.trips)
            assert abs(fast.getAverageTime(s, e_) - slow.getAverageTime(s, e_)) < 1e-9
    print("ok")
