"""
Min Cost to Connect All Points (LeetCode 1584) - Medium
Area: graphs
Key operations: heap pop the cheapest outside point, skip stale entries, add it to the tree, push its distances to every outside point

Given n points on a plane, connecting two points costs their Manhattan distance |x1 - x2| + |y1 - y2|.
Return the minimum total cost to connect all points (a minimum spanning tree of the complete graph).
Example: [[0,0],[2,2],[3,10],[5,2],[7,0]] -> 20
"""
import heapq
from typing import List


# --- brute force ---
def brute_force(points: List[List[int]]) -> int:
    """Kruskal: list ALL n(n-1)/2 edges, sort them, accept each edge whose endpoints are in different
    components (union-find). O(n^2 log n) time and O(n^2) space; the waste is materialising and
    sorting every edge when only the cheapest edge leaving the growing tree ever matters."""
    n = len(points)
    edges = sorted((abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j)
                   for i in range(n) for j in range(i + 1, n))
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri
            total += w
    return total


# --- optimal ---
def solve(points: List[List[int]]) -> int:
    """Prim: grow one tree; a min-heap of (cost, point) holds the cheapest known edge from the tree
    to each outside point. Every added point pushes n candidates: O(n^2 log n)."""
    n = len(points)
    in_tree = [False] * n
    heap = [(0, 0)]  # (cost to join the tree, point index); start with point 0 for free
    total = joined = 0
    while joined < n:
        cost, i = heapq.heappop(heap)
        if in_tree[i]:
            continue
        in_tree[i] = True
        total += cost
        joined += 1
        xi, yi = points[i]
        for j, (xj, yj) in enumerate(points):
            if not in_tree[j]:
                heapq.heappush(heap, (abs(xi - xj) + abs(yi - yj), j))
    return total


# --- demo ---
def demo():
    return solve([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]])


# --- bugs ---
BUGS = [
    {
        "replace": "                heapq.heappush(heap, (abs(xi - xj) + abs(yi - yj), j))",
        "with":    "                heapq.heappush(heap, (cost + abs(xi - xj) + abs(yi - yj), j))",
        "fix": "push the edge cost alone; Prim is not Dijkstra, path length does not accumulate",
        "why": "Adding the cost that i paid turns the key into a distance from the start, so the tree picks edges by path length instead of edge weight: [[0,0],[10,0],[1,1],[11,1]] returns 24 instead of 14.",
        "decoys": [
            {"line": "        in_tree[i] = True", "change": "should be set before the stale check"},
            {"line": "    heap = [(0, 0)]  # (cost to join the tree, point index); start with point 0 for free", "change": "should start as [(0, 0), (0, 1)]"},
            {"line": "            if not in_tree[j]:", "change": "should be if j != i"},
        ],
    },
    {
        "replace": "    while joined < n:",
        "with":    "    while joined < n - 1:",
        "fix": "all n points must join the tree: while joined < n",
        "why": "A tree has n - 1 edges but n points; stopping one early leaves the last point unconnected, so [[0,0],[1,1]] returns 0 instead of 2.",
        "decoys": [
            {"line": "        joined += 1", "change": "should be joined += cost"},
            {"line": "        total += cost", "change": "should be total = max(total, cost)"},
            {"line": "        xi, yi = points[i]", "change": "should be points[joined]"},
        ],
    },
    {
        "replace": "                heapq.heappush(heap, (abs(xi - xj) + abs(yi - yj), j))",
        "with":    "                heapq.heappush(heap, (abs(xi - xj) + (yi - yj), j))",
        "fix": "Manhattan distance takes the absolute value of both differences",
        "why": "A negative y difference makes an edge look cheaper than it is (even negative), so the tree picks wrong edges and the total is wrong: [[3,12],[-2,5],[-4,1]] returns 3 instead of 18.",
        "decoys": [
            {"line": "        cost, i = heapq.heappop(heap)", "change": "should be i, cost = heapq.heappop(heap)"},
            {"line": "        for j, (xj, yj) in enumerate(points):", "change": "should iterate range(i + 1, n)"},
            {"line": "    return total", "change": "should return total // 2 since every edge is pushed twice"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
