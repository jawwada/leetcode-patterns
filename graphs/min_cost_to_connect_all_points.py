"""
Min Cost to Connect All Points (LeetCode 1584)  — Medium
Pattern: Minimum spanning tree (Prim's with heap)

Problem
-------
Given n points on a plane, the cost of connecting two points is their Manhattan distance.
Return the minimum total cost to connect all points (a minimum spanning tree of the
complete graph).
Example: [[0,0],[2,2],[3,10],[5,2],[7,0]] -> 20.

Brute force
-----------
Kruskal without union-find: generate all n(n-1)/2 edges, sort by weight, and for each edge
in order check with a DFS over the accepted edges whether its endpoints are already
connected; accept if not. Sorting is O(n^2 log n), and each of the O(n^2) edges may trigger
an O(n) DFS -> O(n^3) time, O(n^2) space. The waste is re-deriving connectivity by
traversal for each candidate edge.

From brute force to optimal
---------------------------
Two independent fixes. (a) Replace the connectivity DFS with union-find -> Kruskal in
O(n^2 log n), dominated by sorting the edge list. (b) Avoid materialising/sorting all
edges at all: Prim's grows one tree from an arbitrary start; the cut property says the
cheapest edge leaving the tree is always safe, so we only ever need "the cheapest edge
from the tree to each outside vertex". Keep those candidates in a min-heap: when a vertex
joins, push its distance to every unvisited vertex. O(n^2 log n) time but O(n^2) heap in
the worst case; an array-based Prim (no heap, scan for the minimum) is O(n^2) time and
O(n) space and is actually optimal on a dense complete graph. The heap version is what
interviewers usually expect to see.

Intuition
---------
Start with any point "in". Repeatedly add the outside point that is closest to ANY point
already in; that edge can never be beaten (cut property). A min-heap of (cost, point)
hands you that closest point each time; stale entries (points already added) are popped
and skipped.

Geometric view
--------------
Picture the points on graph paper. The tree is a growing blob of connected points. At
each step draw the shortest possible line from the blob to a point outside it and absorb
that point. The heap is a sorted list of candidate lines from the blob's current members
to the outside; the shortest valid one is always on top.

Steps
-----
1. visited = set(); heap = [(0, 0)]; total = 0.
2. Pop (cost, i); if i visited skip; mark visited, total += cost.
3. For every unvisited j, push (manhattan(i, j), j).
4. Stop when all n points are visited; return total.

Complexity: O(n^2 log n) time, O(n^2) space — each added vertex pushes up to n candidates; heap can hold O(n^2) entries.
Pitfalls: pushing the start with a non-zero cost; forgetting to skip stale pops (would
double-add a vertex's cost); using Euclidean instead of Manhattan distance.
"""
import heapq
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        visited = [False] * n
        heap = [(0, 0)]  # (cost to join the tree, point index)
        total = added = 0
        while added < n:
            cost, i = heapq.heappop(heap)
            if visited[i]:
                continue  # stale: i joined earlier via a cheaper edge
            visited[i] = True
            total += cost
            added += 1
            xi, yi = points[i]
            for j in range(n):
                if not visited[j]:
                    xj, yj = points[j]
                    heapq.heappush(heap, (abs(xi - xj) + abs(yi - yj), j))
        return total


def brute_force(points: List[List[int]]) -> int:
    # Kruskal without union-find: sort all edges, accept an edge only if a DFS over the
    # accepted edges shows its endpoints are not yet connected.
    n = len(points)
    edges = sorted(
        (abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j)
        for i in range(n) for j in range(i + 1, n)
    )
    adj = [[] for _ in range(n)]
    total = 0
    for w, u, v in edges:
        seen, stack = {u}, [u]
        while stack:
            cur = stack.pop()
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if v not in seen:
            adj[u].append(v)
            adj[v].append(u)
            total += w
    return total


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]], 20),
        ([[3, 12], [-2, 5], [-4, 1]], 18),
        ([[0, 0]], 0),
        ([[0, 0], [1, 1], [1, 0], [-1, 1]], 4),
    )
    for p, want in cases:
        assert brute_force(p) == want
        assert s.minCostConnectPoints(p) == want
    print("ok")
