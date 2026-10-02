"""
Minimum Weighted Subgraph With the Required Paths (LeetCode 2203)  — Hard
Pattern: Dijkstra (min-heap shortest paths)

Problem
-------
A weighted directed graph on n nodes. Return the minimum total weight of a subgraph in
which both src1 and src2 can reach dest, or -1 if no such subgraph exists.
Example: n=6, edges=[[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],
[4,5,1]], src1=0, src2=1, dest=5 -> 9 (edges 1->0, 0->2, 2->3, 3->4, 4->5).

Brute force
-----------
The two required paths must merge at some node x (possibly a source or dest itself) and
share the x -> dest tail. For every candidate x run three shortest-path computations
(src1 -> x, src2 -> x, x -> dest) with a simple O(V*E) Bellman-Ford each, and take the
minimum sum over x. O(V^2 * E) time, O(V) space. The waste: the src1 and src2 searches
are identical for every x and are recomputed n times, and each x -> dest search is a
separate traversal when all of them end at the same node.

From brute force to optimal
---------------------------
First redundancy: shortest paths from src1 and src2 do not depend on x -- compute them ONCE
each with Dijkstra (O(E log V)) and read d1[x], d2[x] from the arrays, dropping to
O(V * E log V) for the remaining per-x dest searches. Second redundancy: "distance from x
to dest, for every x" is a single-SOURCE problem in the REVERSED graph -- run Dijkstra from
dest over reversed edges once and read dd[x]. Three Dijkstra runs total, then a linear
scan over x minimising d1[x] + d2[x] + dd[x]: O(E log V).

Intuition
---------
Any valid subgraph contains a path src1 -> dest and a path src2 -> dest; follow them from
dest backwards and they share a common tail starting at some meeting node x. The optimal
subgraph is therefore three shortest paths glued at x, and the best x is found by trying
all of them with precomputed distances. Reversing edges turns "many targets, one source"
into "one source": Dijkstra from dest on the reversed graph gives every x -> dest distance.

Geometric view
--------------
Picture a Y shape: two arms starting at src1 and src2 that join at x, then one stem from x
down to dest. d1 and d2 are the lengths of the arms measured from the two sources outward;
dd is the stem length measured from dest backwards (hence the reversed graph). Slide x over
every node and pick the Y with the smallest total length.

Steps
-----
1. Build forward adjacency and reversed adjacency.
2. d1 = dijkstra(forward, src1); d2 = dijkstra(forward, src2); dd = dijkstra(reversed, dest).
3. best = min over x of d1[x] + d2[x] + dd[x].
4. Return -1 if best is infinite, else best.

Complexity: O((V + E) log V) time, O(V + E) space — three Dijkstra runs plus two adjacency lists.
Pitfalls: forgetting the reversed graph and running Dijkstra from every x; overflow-style
sums with inf (use float('inf') and check before returning); assuming the meeting node is
dest or a source only -- it can be any intermediate node.
"""
import heapq
from typing import List


class Solution:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        fwd = [[] for _ in range(n)]
        rev = [[] for _ in range(n)]
        for u, v, w in edges:
            fwd[u].append((v, w))
            rev[v].append((u, w))

        def dijkstra(adj: List[List[tuple]], src: int) -> List[float]:
            dist = [float("inf")] * n
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heapq.heappop(heap)
                if d > dist[u]:
                    continue  # stale entry
                for v, w in adj[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        heapq.heappush(heap, (dist[v], v))
            return dist

        d1 = dijkstra(fwd, src1)
        d2 = dijkstra(fwd, src2)
        dd = dijkstra(rev, dest)  # dd[x] = shortest x -> dest in the original graph
        best = min(d1[x] + d2[x] + dd[x] for x in range(n))
        return -1 if best == float("inf") else best


def brute_force(n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
    # For each meeting node x, run three Bellman-Ford searches and sum the three distances.
    def bellman_ford(src: int) -> List[float]:
        dist = [float("inf")] * n
        dist[src] = 0
        for _ in range(n - 1):
            for u, v, w in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        return dist

    best = float("inf")
    for x in range(n):
        best = min(best, bellman_ford(src1)[x] + bellman_ford(src2)[x] + bellman_ford(x)[dest])
    return -1 if best == float("inf") else best


if __name__ == "__main__":
    s = Solution()
    cases = (
        (6, [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3], [2, 3, 4], [3, 4, 2], [4, 5, 1]], 0, 1, 5, 9),
        (3, [[0, 1, 1], [2, 1, 1]], 0, 1, 2, -1),
        (3, [[0, 2, 5], [1, 2, 5]], 0, 1, 2, 10),
        (4, [[0, 3, 10], [1, 3, 10], [0, 2, 1], [1, 2, 1], [2, 3, 1]], 0, 1, 3, 3),
        (2, [[0, 1, 4]], 0, 1, 1, 4),
    )
    for n, e, a, b, d, want in cases:
        assert brute_force(n, e, a, b, d) == want
        assert s.minimumWeight(n, e, a, b, d) == want
    print("ok")
