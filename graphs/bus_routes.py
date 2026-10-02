"""
Bus Routes (LeetCode 815)  — Hard
Pattern: BFS over routes via a stop -> routes index (implicit graph)

Problem
-------
routes[i] is the list of stops bus i cycles through. Starting at stop source (not on a bus) you
want to reach stop target; return the minimum number of buses you must take, or -1.
Example: routes = [[1,2,7],[3,6,7]], source 1, target 6 -> 2 (bus 0 to stop 7, then bus 1).
source == target -> 0.

Brute force
-----------
Build the "route graph" explicitly: two routes are adjacent if they share a stop, so compare every
pair of routes with a set intersection, then BFS over route nodes from every route containing
source until one containing target is dequeued. With R routes of total length S this costs
O(R^2 * S/R) = O(R * S) to build the graph (R up to 500, S up to 10^5 stops) and O(R^2) space for
the adjacency. The waste: most pairs of routes share nothing, yet every pair is compared, and a
stop shared by 100 routes is rediscovered 100*99/2 times once per pair.

From brute force to optimal
---------------------------
The redundancy is the all-pairs intersection test. Observation: routes are adjacent through a
stop, so index the other way round: stop -> list of routes that visit it (one pass over the input,
O(S)). The neighbours of a route are then "for each stop on it, every route through that stop",
which enumerates exactly the real edges with no failed comparisons. BFS over routes with two
visited sets: routes already boarded (never board twice) and stops already expanded (a stop's
route list is scanned once, so the total work is bounded by the index size). The answer is the BFS
depth of the first route that contains target.

Intuition
---------
Count buses, not stops: a bus ride is one BFS edge, however many stops it covers. The graph's
nodes are routes, the start is the set of routes through source (all at depth 1), and reaching any
route that contains target finishes. The stop -> routes map is the adjacency list of the bipartite
stop/route graph; BFS over it alternates stop, route, stop, route.

Geometric view
--------------
A bipartite picture: route nodes on the left, stop nodes on the right, an edge for every
(route, stop) membership. Boarding a bus = stepping left, riding to a stop = stepping right. BFS
frontier k holds all routes reachable with k buses; expanding a route lights all of its stops, and
each lit stop lights all of its routes for frontier k+1.

Steps
-----
1. If source == target return 0. Build stop_to_routes from the input.
2. queue = all routes through source with distance 1; seen_routes = that set; seen_stops = {source}.
3. Pop (route, buses). For each stop on the route: if stop == target return buses.
4. If the stop is new, mark it and push every unseen route through it with buses + 1.
5. Queue empty -> return -1.

Complexity: O(S) time, O(S) space — S = total stops over all routes; every (route, stop) pair is
touched a constant number of times via the two visited sets.
Pitfalls: forgetting source == target (answer 0, not 1); marking only routes or only stops
visited (quadratic blow-up on big routes); counting stops instead of buses; returning when the
target route is pushed with the wrong distance.
"""
from collections import defaultdict, deque
from typing import List


class Solution:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        if source == target:
            return 0
        stop_to_routes = defaultdict(list)                # the implicit adjacency
        for i, route in enumerate(routes):
            for stop in route:
                stop_to_routes[stop].append(i)
        seen_routes = set(stop_to_routes[source])
        seen_stops = {source}
        queue = deque((i, 1) for i in seen_routes)        # board any bus at source: 1 bus
        while queue:
            i, buses = queue.popleft()
            for stop in routes[i]:
                if stop == target:
                    return buses
                if stop in seen_stops:
                    continue                              # its routes were already enqueued
                seen_stops.add(stop)
                for j in stop_to_routes[stop]:
                    if j not in seen_routes:
                        seen_routes.add(j)
                        queue.append((j, buses + 1))
        return -1


def brute_force(routes: List[List[int]], source: int, target: int) -> int:
    # Explicit route graph via all-pairs set intersection, then BFS over routes.
    if source == target:
        return 0
    sets = [set(r) for r in routes]
    R = len(routes)
    adj = [[j for j in range(R) if j != i and sets[i] & sets[j]] for i in range(R)]   # O(R^2) pairs
    queue = deque((i, 1) for i in range(R) if source in sets[i])
    seen = {i for i, _ in queue}
    while queue:
        i, buses = queue.popleft()
        if target in sets[i]:
            return buses
        for j in adj[i]:
            if j not in seen:
                seen.add(j)
                queue.append((j, buses + 1))
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 2, 7], [3, 6, 7]], 1, 6, 2),
        ([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12, -1),
        ([[1, 7], [3, 5]], 5, 5, 0),                                   # already there
        ([[1, 2], [2, 3], [3, 4], [4, 5]], 1, 5, 4),                   # chain of transfers
        ([[1, 2, 3]], 4, 3, -1),                                       # source on no route
    )
    for routes, src, dst, want in cases:
        assert s.numBusesToDestination(routes, src, dst) == want, (routes, src, dst)
        assert brute_force(routes, src, dst) == want, (routes, src, dst)
    print("ok")
