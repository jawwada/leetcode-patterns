"""
Swim in Rising Water (LeetCode 778)  — Hard
Pattern: Minimax path via min-heap (bottleneck Dijkstra)

Problem
-------
An n x n grid of distinct elevations 0..n*n-1. At time t the water level is t and you can
move between 4-adjacent cells whose elevations are both <= t. Starting at (0,0), return the
least t at which you can reach (n-1,n-1).
Example: [[0,2],[1,3]] -> 3.  [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],
[11,17,18,19,20],[10,9,8,7,6]] -> 16.

Brute force
-----------
For t = 0, 1, 2, ... run a BFS from (0,0) through cells with elevation <= t and stop at the
first t that reaches the goal. Up to n^2 values of t, each BFS O(n^2) -> O(n^4) time,
O(n^2) space. The waste: the BFS at level t+1 re-walks the entire region already explored
at level t, and many consecutive t values do not change the reachable region at all.

From brute force to optimal
---------------------------
First redundancy: scanning t linearly. The predicate "goal reachable at level t" is
monotone (true stays true as t grows), so binary search t over [0, n^2) with one BFS per
probe -> O(n^2 log n). Second redundancy: even binary search rediscovers the same region
each probe. Reformulate: the answer is the minimum over paths of the MAXIMUM elevation on
the path (a bottleneck shortest path). Dijkstra works for this because max(a, b) is
monotone like addition: pop the cell with the smallest "worst elevation so far"; the first
time the goal is popped that value is optimal. One pass -> O(n^2 log n) with no repeated
traversals, and in practice far fewer cells touched.

Intuition
---------
Grow the reachable region one cell at a time, always admitting the lowest-elevation cell on
its border. The water level needed so far is the highest cell admitted. When the goal is
admitted, that running maximum is the answer: any other route would have had to admit some
cell at least that high. A min-heap keyed on max(level so far, cell elevation) picks the
next border cell in O(log n).

Geometric view
--------------
Picture the grid as terrain and the water rising from the top-left corner. The flooded
region expands by always submerging the lowest dry cell touching it; the heap is the
shoreline sorted by height. The answer is the height of the water when the far corner
gets wet -- the lowest "pass" over the ridge separating the two corners.

Steps
-----
1. heap = [(grid[0][0], 0, 0)], seen = {(0,0)}.
2. Pop (t, r, c); if (r, c) is the goal return t.
3. For each unseen in-bounds neighbour: mark seen and push (max(t, grid[nr][nc]), nr, nc).

Complexity: O(n^2 log n) time, O(n^2) space — each cell is pushed/popped once from a heap of size O(n^2).
Pitfalls: pushing grid[nr][nc] instead of max(t, grid[nr][nc]) (loses the bottleneck);
forgetting that the start cell's own elevation counts; with binary search, using
elevation < t instead of <= t.
"""
import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        heap = [(grid[0][0], 0, 0)]  # (highest elevation on the path so far, r, c)
        seen = {(0, 0)}
        while heap:
            t, r, c = heapq.heappop(heap)
            if r == n - 1 and c == n - 1:
                return t
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                    seen.add((nr, nc))  # later pops have t' >= t, so max(t', cell) cannot beat this
                    heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
        return -1


def brute_force(grid: List[List[int]]) -> int:
    # Scan t upward; at each t run a BFS restricted to cells with elevation <= t.
    n = len(grid)
    for t in range(n * n):
        if grid[0][0] > t:
            continue
        seen, stack = {(0, 0)}, [(0, 0)]
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen and grid[nr][nc] <= t:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        if (n - 1, n - 1) in seen:
            return t
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[0, 2], [1, 3]], 3),
        ([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]], 16),
        ([[0]], 0),
        ([[3, 2], [0, 1]], 3),
        ([[7, 5, 3], [8, 6, 1], [0, 2, 4]], 7),
    )
    for g, want in cases:
        assert brute_force(g) == want
        assert s.swimInWater(g) == want
    print("ok")
