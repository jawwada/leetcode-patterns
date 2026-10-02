"""
Minimum Number of Refueling Stops (LeetCode 871)  — Hard
Pattern: Greedy with a max-heap of passed-but-unused options (refuel only when stuck)

Problem
-------
A car starts with startFuel litres and must reach position target, using one litre per mile.
stations[i] = [position, fuel] are sorted by position. Return the minimum number of refuelling
stops needed, or -1 if the target is unreachable. The tank is unlimited.
Example: target=100, startFuel=10, stations=[[10,60],[20,30],[30,30],[60,40]] -> 2 (stop at
10 for 60 litres, then at 60 for 40). target=1, startFuel=1, [] -> 0. target=100,
startFuel=1, [[10,100]] -> -1.

Brute force
-----------
Try every subset of stations: drive in order, refuel at the chosen ones, check the fuel never
goes negative before the next chosen station and the target, and keep the smallest feasible
subset. O(2^n * n) time -- exponential -- O(n) space. The waste: whether the car can pass
station i depends only on the total fuel collected so far, not on which stations supplied it,
so subsets with the same count and the same chosen prefix are re-simulated endlessly.

From brute force to optimal
---------------------------
The redundancy is deciding at each station whether to stop, as if the decision had to be made
on the spot. Observation: the fuel from a station we have already driven PAST can be banked
retroactively -- it does not matter whether we poured it in when we passed or "pretend" we
did later, as long as every stop we count is a station we actually reached. So drive forward
greedily without stopping and keep the fuel amounts of all passed stations in a max-heap.
Whenever the next position is out of reach, retroactively take the LARGEST passed station
(fewest stops for the most range), repeat until the position is reachable or the heap runs
dry (then -1). Each station is pushed once and popped at most once: O(n log n). The exchange
argument: any optimal plan that refuelled at a smaller passed station instead of the largest
can swap to the largest without reducing fuel at any point.

Intuition
---------
Procrastinate the decision. Driving past a station costs nothing; you only need to commit to
stops when you would otherwise run dry, and at that moment you know exactly which stations are
behind you. Picking the biggest available tank each time minimises the number of commits.

Geometric view
--------------
A number line from 0 to target with station ticks. The car's reach is a bar from 0 to
startFuel. Each station the bar covers drops its fuel into a max-heap triangle. When the next
tick (or the target) lies beyond the bar's end, pull the apex of the triangle out and extend
the bar by that amount; keep pulling until the tick is covered or the triangle is empty.

Steps
-----
1. Append [target, 0] to the stations so the target is handled like any stop; fuel = startFuel.
2. passed = [] (max-heap of fuel amounts, negated), stops = 0.
3. For each (pos, gas): while fuel < pos: if passed is empty return -1; fuel += pop max; stops += 1.
4. Push gas onto passed (we have now reached this station).
5. Return stops.

Complexity: O(n log n) time, O(n) space — each station is pushed once and popped at most once.
Pitfalls: Refuelling eagerly at every station (counts stops you did not need); forgetting to
treat the target as the final "station"; comparing fuel < pos with the station's own fuel
already added (you can only take fuel from stations you have reached).
"""
import heapq
from typing import List


class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:
        passed = []                                   # max-heap (negated) of fuel at passed stations
        fuel, stops = startFuel, 0
        for pos, gas in stations + [[target, 0]]:     # treat the target as the last stop
            while fuel < pos:                         # cannot reach pos: retroactively refuel
                if not passed:
                    return -1
                fuel -= heapq.heappop(passed)         # take the largest tank we drove past
                stops += 1
            heapq.heappush(passed, -gas)              # reached pos: its fuel is now available
        return stops


def brute_force(target: int, startFuel: int, stations: List[List[int]]) -> int:
    # Exponential: every subset of stations, simulated in order; keep the smallest feasible one.
    n, best = len(stations), -1
    for mask in range(1 << n):
        fuel, ok = startFuel, True
        for i in range(n):
            if mask >> i & 1:
                if fuel < stations[i][0]:
                    ok = False
                    break
                fuel += stations[i][1]
        if ok and fuel >= target:
            count = bin(mask).count("1")
            if best < 0 or count < best:
                best = count
    return best


if __name__ == "__main__":
    s = Solution()
    cases = (
        ((100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]), 2),
        ((1, 1, []), 0),
        ((100, 1, [[10, 100]]), -1),
        ((100, 50, [[25, 25], [50, 50]]), 1),               # exactly reaching a station is fine
        ((100, 25, [[25, 25], [50, 25], [75, 25]]), 3),
    )
    for args, want in cases:
        assert s.minRefuelStops(*args) == want, (args, want)
        assert brute_force(*args) == want, (args, want)
    import random
    random.seed(871)
    for _ in range(200):
        target, start = random.randint(10, 80), random.randint(0, 30)
        n = random.randint(0, 8)
        positions = sorted(random.sample(range(1, target), n))   # constraint: positions < target
        st = [[p, random.randint(0, 30)] for p in positions]
        assert s.minRefuelStops(target, start, st) == brute_force(target, start, st), (target, start, st)
    print("ok")
