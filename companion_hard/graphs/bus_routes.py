"""
Bus Routes (LeetCode 815) - Hard
Chapter: graphs
Pattern: BFS on implicit graph (stop -> routes index)

routes[i] lists the stops that bus i cycles through. You start at stop source (not on a bus) and
want to reach stop target. Return the minimum number of buses to take, or -1 if impossible;
if source == target the answer is 0.
Example: routes = [[1,2,7],[3,6,7]], source = 1, target = 6 -> 2 (bus 0 to stop 7, then bus 1).
"""
from collections import deque      # popleft is O(1)


# --- brute force ---
def share_a_stop(route_a, route_b):
    """True when the two routes have at least one stop in common."""
    for stop in route_a:
        if stop in route_b:
            return True
    return False


def brute_force(routes, source, target):
    """Build the route graph by testing every pair of routes, then BFS over routes. O(R^2 * S)."""
    if source == target:
        return 0
    count = len(routes)
    adjacent = []                                  # adjacent[i] = routes sharing a stop with i
    for i in range(count):
        adjacent.append([])
        for j in range(count):                     # every pair is tested, most share nothing
            if j != i and share_a_stop(routes[i], routes[j]):
                adjacent[i].append(j)
    queue = deque()
    seen = set()
    for i in range(count):
        if source in routes[i]:                    # board any bus at source: 1 bus
            queue.append((i, 1))
            seen.add(i)
    while queue:
        route, buses = queue.popleft()
        if target in routes[route]:
            return buses
        for other in adjacent[route]:
            if other not in seen:
                seen.add(other)
                queue.append((other, buses + 1))
    return -1


# --- optimal ---
def index_by_stop(routes):
    """stop -> list of the routes that visit it."""
    routes_through = {}
    for i in range(len(routes)):
        for stop in routes[i]:
            if stop not in routes_through:
                routes_through[stop] = []
            routes_through[stop].append(i)
    return routes_through


def bus_routes(routes, source, target):
    """Index stop -> routes once, then BFS over routes through shared stops. O(total stops)."""
    if source == target:
        return 0
    routes_through = index_by_stop(routes)         # the implicit adjacency
    queue = deque()
    seen_routes = set()
    for route in routes_through.get(source, []):   # board any bus at source: 1 bus
        queue.append((route, 1))
        seen_routes.add(route)
    seen_stops = {source}
    while queue:
        route, buses = queue.popleft()
        for stop in routes[route]:
            if stop == target:
                return buses
            if stop in seen_stops:                 # its routes were already enqueued
                continue
            seen_stops.add(stop)
            for other in routes_through[stop]:
                if other not in seen_routes:
                    seen_routes.add(other)
                    queue.append((other, buses + 1))
    return -1


# --- try the brute force ---
print(brute_force([[1, 2, 7], [3, 6, 7]], 1, 6))                                 # -> 2
print(brute_force([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12))    # -> -1
print(brute_force([[1, 7], [3, 5]], 5, 5))                                       # -> 0
print(brute_force([[1, 2], [2, 3], [3, 4], [4, 5]], 1, 5))                       # -> 4


# --- try the optimal ---
print(bus_routes([[1, 2, 7], [3, 6, 7]], 1, 6))                                 # -> 2
print(bus_routes([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12))    # -> -1
print(bus_routes([[1, 7], [3, 5]], 5, 5))                                       # -> 0
print(bus_routes([[1, 2], [2, 3], [3, 4], [4, 5]], 1, 5))                       # -> 4
