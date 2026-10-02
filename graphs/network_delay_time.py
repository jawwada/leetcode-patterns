"""
Network Delay Time (LeetCode 743)  — Medium
Pattern: Dijkstra (min-heap shortest paths)

Problem
-------
n nodes 1..n, directed edges times[i] = (u, v, w) meaning a signal takes w to travel
u -> v. A signal is sent from node k. Return the time for ALL nodes to receive it, or -1
if some node never does.
Example: times=[[2,1,1],[2,3,1],[3,4,1]], n=4, k=2 -> 2.

Brute force
-----------
Bellman-Ford style relaxation: dist[k]=0, others inf; repeat n-1 times: for every edge
(u, v, w) set dist[v] = min(dist[v], dist[u] + w). O(V * E) time, O(V) space. The waste:
every round rescans all E edges, including edges leaving nodes whose distance has not
changed since the last round, so most relaxations do nothing. (Alternatively: Dijkstra
with a plain list and a linear scan for the minimum each step is O(V^2 + E) -- same
idea, the data structure is what is missing.)

From brute force to optimal
---------------------------
The redundancy is relaxing edges out of nodes whose distance is not yet final or has not
changed. Observation (Dijkstra): with non-negative weights, the unsettled node with the
smallest tentative distance is already final -- no later path can undercut it -- so we
can settle nodes in increasing distance order and relax each node's out-edges exactly
once. Picking the minimum efficiently is the job of a min-heap: push (dist, node) when a
distance improves, pop the smallest, skip stale entries. O((V + E) log V).

Intuition
---------
Expand outward from k in order of arrival time. The heap always hands you the node that
is about to receive the signal next; when you pop it, its time is final, so relax its
neighbours. The answer is the largest finalised time, or -1 if some node was never
popped.

Geometric view
--------------
Picture the signal as a wavefront whose radius is "time". Nodes are settled in the order
the wavefront reaches them; the heap holds candidate arrival events (time, node) sorted
by time. Popping the earliest event advances the wavefront to that node and schedules
new events for its out-edges. The last node to be reached fixes the answer.

Steps
-----
1. Build adjacency u -> [(v, w)].
2. heap = [(0, k)], dist = {}.
3. Pop (d, u); if u in dist skip (stale); dist[u] = d; push (d + w, v) for each v not yet
   settled.
4. Return max(dist.values()) if len(dist) == n else -1.

Complexity: O((V + E) log V) time, O(V + E) space — each edge may push one heap entry; heap pops are log-sized.
Pitfalls: not skipping stale heap entries (wrong answers only with a decrease-key bug, but
wasted work always); 1-indexed nodes; disconnected nodes must yield -1, not 0.
"""
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adj = defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        dist = {}
        heap = [(0, k)]
        while heap:
            d, u = heapq.heappop(heap)
            if u in dist:
                continue  # stale entry: u was settled with a smaller distance
            dist[u] = d
            for v, w in adj[u]:
                if v not in dist:
                    heapq.heappush(heap, (d + w, v))
        return max(dist.values()) if len(dist) == n else -1


def brute_force(times: List[List[int]], n: int, k: int) -> int:
    # Bellman-Ford: n-1 rounds, each relaxing EVERY edge.
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    worst = max(dist[1:])
    return -1 if worst == INF else worst


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2, 2),
        ([[1, 2, 1]], 2, 1, 1),
        ([[1, 2, 1]], 2, 2, -1),
        ([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1, 3),
        ([], 1, 1, 0),
    )
    for t, n, k, want in cases:
        assert brute_force(t, n, k) == want
        assert s.networkDelayTime(t, n, k) == want
    print("ok")
