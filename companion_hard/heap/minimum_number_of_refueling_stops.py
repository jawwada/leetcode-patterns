"""
Minimum Number of Refueling Stops (LeetCode 871) - Hard
Chapter: heap
Pattern: Greedy with a max-heap of passed-but-unused options (refuel only when stuck)

A car starts with start_fuel litres and must reach position target, using one litre per mile.
stations[i] = [position, fuel] are sorted by position and lie before the target. Return the
minimum number of refuelling stops, or -1 if the target is unreachable; the tank is unlimited.
Example: target = 100, start_fuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]] -> 2.
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def brute_force(target, start_fuel, stations):
    """Try every subset of stations in driving order; keep the smallest that arrives. O(2^n n)."""
    n = len(stations)
    best = -1
    for mask in range(1 << n):                 # bit i of mask = 1 means we stop at station i
        fuel = start_fuel
        stops = 0
        arrived = True
        for i in range(n):
            if (mask >> i) & 1 == 1:
                if fuel < stations[i][0]:      # ran dry before reaching this chosen station
                    arrived = False
                    break
                fuel += stations[i][1]
                stops += 1
        if arrived and fuel >= target:
            if best < 0 or stops < best:
                best = stops
    return best


# --- optimal ---
def min_refuel_stops(target, start_fuel, stations):
    """Drive past stations; when stuck, retroactively take the biggest tank passed. O(n log n)."""
    passed = []                                # -fuel of stations driven past: root = biggest tank
    fuel = start_fuel
    stops = 0
    waypoints = stations + [[target, 0]]       # the target acts as a last station with no fuel
    for position, gas in waypoints:
        while fuel < position:                 # cannot reach it yet: refuel at a passed station
            if len(passed) == 0:
                return -1
            fuel += -heapq.heappop(passed)
            stops += 1
        heapq.heappush(passed, -gas)           # reached it: its fuel is available from now on
    return stops


# --- try the brute force ---
print(brute_force(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]))   # -> 2
print(brute_force(1, 1, []))                                            # -> 0
print(brute_force(100, 1, [[10, 100]]))                                 # -> -1
print(brute_force(100, 25, [[25, 25], [50, 25], [75, 25]]))             # -> 3


# --- try the optimal ---
print(min_refuel_stops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]))   # -> 2
print(min_refuel_stops(1, 1, []))                                            # -> 0
print(min_refuel_stops(100, 1, [[10, 100]]))                                 # -> -1
print(min_refuel_stops(100, 25, [[25, 25], [50, 25], [75, 25]]))             # -> 3
