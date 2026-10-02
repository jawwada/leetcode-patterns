"""
Minimum Cost to Make at Least One Valid Path in a Grid (LeetCode 1368)  — Hard
Pattern: 0-1 BFS (deque shortest path)

Problem
-------
Each cell of an m x n grid holds an arrow: 1 right, 2 left, 3 down, 4 up. Following the
arrow out of a cell is free; changing a cell's arrow costs 1 (each cell at most once).
Return the minimum cost so that a path from (0,0) following the arrows reaches (m-1,n-1).
Example: [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]] -> 3.

Brute force
-----------
Treat the grid as a graph where every cell has 4 out-edges: cost 0 along its arrow, cost 1
in the other three directions. Run Bellman-Ford style relaxation: repeatedly sweep all
cells and relax all 4 moves until no cost changes. Each sweep is O(m*n) and up to m*n
sweeps may be needed -> O((m*n)^2) time, O(m*n) space. The waste: every sweep re-relaxes
every cell, including cells whose cost is already final.

From brute force to optimal
---------------------------
The redundancy is relaxing cells in arbitrary order instead of in order of cost. Dijkstra
fixes that by settling cells in increasing cost with a heap: O(mn log mn). Second
observation: every edge weighs 0 or 1, so a full heap is unnecessary -- a deque that keeps
cells sorted by cost suffices: a 0-cost move keeps the same cost (push FRONT), a 1-cost
move is exactly one level deeper (push BACK). Popping from the front always yields a
minimum-cost cell, exactly like Dijkstra, in O(1) per operation -> O(m*n).

Intuition
---------
Start at (0,0) with cost 0. Ride the free arrows as far as they go (these cells join the
current cost layer at the front of the deque). Only when the free moves are exhausted do we
spend 1 to turn, which puts a cell in the next layer at the back. Because the deque is
processed front to back, the first time the target cell is popped its cost is minimal.

Geometric view
--------------
Picture water poured at (0,0) that flows freely along arrows: it fills every cell reachable
at cost 0 first. Then it "pays" one unit to spill sideways into neighbouring cells, which
start their own free flows, and so on. The deque is the waterfront: free spreads at the
front, paid spills queued at the back, so the front always holds the cheapest cells.

Steps
-----
1. cost[r][c] = inf except cost[0][0] = 0; dq = deque([(0,0)]).
2. Pop (r, c) from the front. For each of the 4 directions k: step = 0 if grid[r][c] points
   that way, else 1.
3. If cost[r][c] + step < cost[nr][nc]: update, appendleft when step == 0, append otherwise.
4. Return cost[m-1][n-1].

Complexity: O(m*n) time, O(m*n) space — each cell is relaxed through 4 edges with O(1) deque operations.
Pitfalls: mapping arrow values 1..4 to the wrong directions; using a plain FIFO queue
(breaks optimality -- 0-cost moves must go to the FRONT); marking cells visited on push
instead of relaxing by cost (a cell can be improved after a first expensive discovery).
"""
from collections import deque
from typing import List


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))  # value 1,2,3,4 -> index 0,1,2,3
        cost = [[float("inf")] * n for _ in range(m)]
        cost[0][0] = 0
        dq = deque([(0, 0)])
        while dq:
            r, c = dq.popleft()
            for k, (dr, dc) in enumerate(dirs):
                nr, nc = r + dr, c + dc
                if not (0 <= nr < m and 0 <= nc < n):
                    continue
                step = 0 if grid[r][c] == k + 1 else 1  # free along the arrow, 1 to turn
                if cost[r][c] + step < cost[nr][nc]:
                    cost[nr][nc] = cost[r][c] + step
                    if step == 0:
                        dq.appendleft((nr, nc))  # same cost layer: process before paid moves
                    else:
                        dq.append((nr, nc))
        return cost[m - 1][n - 1]


def brute_force(grid: List[List[int]]) -> int:
    # Bellman-Ford over cells: sweep every cell and relax all 4 moves until nothing changes.
    m, n = len(grid), len(grid[0])
    dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
    cost = [[float("inf")] * n for _ in range(m)]
    cost[0][0] = 0
    changed = True
    while changed:
        changed = False
        for r in range(m):
            for c in range(n):
                for k, (dr, dc) in enumerate(dirs):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n:
                        step = 0 if grid[r][c] == k + 1 else 1
                        if cost[r][c] + step < cost[nr][nc]:
                            cost[nr][nc] = cost[r][c] + step
                            changed = True
    return cost[m - 1][n - 1]


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]], 3),
        ([[1, 1, 3], [3, 2, 2], [1, 1, 4]], 0),
        ([[1, 2], [4, 3]], 1),
        ([[2, 2, 2], [2, 2, 2]], 3),
        ([[4]], 0),
    )
    for g, want in cases:
        assert brute_force(g) == want
        assert s.minCost(g) == want
    print("ok")
