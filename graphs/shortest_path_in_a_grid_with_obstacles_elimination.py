"""
Shortest Path in a Grid with Obstacles Elimination (LeetCode 1293)  — Hard
Pattern: BFS over augmented states (position + bitmask/budget)

Problem
-------
In a 0/1 grid you walk 4-directionally from (0,0) to (m-1,n-1). You may step onto at most k
obstacle cells (1s), destroying them. Return the minimum number of steps, or -1.
Example: grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1 -> 6 via
(0,0)->(0,1)->(0,2)->(1,2)->(2,2)->(3,2)*->(4,2), eliminating the obstacle at (3,2).
grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1 -> -1.

Brute force
-----------
Pick which obstacles to delete: for every subset of at most k obstacle cells, clear them and run a
plain BFS on the resulting grid; take the shortest result. With B obstacles that is
O(C(B, <= k) * m * n) time, O(m * n) space; exponential in k. The waste: nearly all subsets
delete obstacles far from any useful path, and the BFS over the open region is repeated from
scratch for every subset even though the regions mostly coincide.

From brute force to optimal
---------------------------
The redundancy is deciding WHICH obstacles to delete in advance. Observation: a path only cares how
many eliminations it has spent so far, not which cells they were; so a walk's situation is
(row, col, eliminations left). That is at most m * n * (k + 1) states and every step is a unit
edge (stepping on a 1 decrements the budget), so one BFS over the state graph finds the shortest
walk, and the per-subset searches collapse into a single search that shares all common prefixes.
The visited set must be on the full state: reaching a cell with more budget left is a genuinely
better situation than reaching it earlier with less. One more pruning: if k >= m + n - 2 the
Manhattan walk is always affordable, so answer m + n - 2 immediately.

Intuition
---------
Augment the position with the resource that constrains the walk. A cell is not one node but k + 1
nodes (one per remaining budget), obstacles are edges that cost a unit of budget, and BFS depth is
still the number of steps because every edge still costs one step.

Geometric view
--------------
k + 1 stacked copies of the grid. In copy j (j eliminations left) you move freely on 0-cells;
stepping on a 1-cell drops you one copy down (to j - 1) if j > 0, otherwise it is a wall. The BFS
wave spreads inside each layer and leaks downward at obstacles; the first time any layer reaches
the bottom-right cell, the depth is the answer.

    layer k=1 (budget left 1):      layer k=0:
    0 0 0   wave: 0 1 2             . . .
    1 1 0               3           . . .
    0 0 0               4           . . .
    0 1 1               5*  <- stepping on the 1 drops to layer 0 at depth 5
    0 0 0                           . . 6  <- target reached

Steps
-----
1. If k >= m + n - 2 return m + n - 2 (this also covers the 1x1 grid, answer 0).
2. queue = [(0, 0, k)], seen = {(0, 0, k)}, steps = 0.
3. Process a layer: pop (r, c, left); if (r, c) is the target return steps.
4. For each in-bounds neighbour: nl = left - grid[nr][nc]; skip if nl < 0; else push
   (nr, nc, nl) if unseen. After the layer, steps += 1.
5. Return -1 when the queue empties.

Complexity: O(m * n * k) time and space — each (cell, budget) state is expanded once with 4
neighbours.
Pitfalls: visited keyed on (r, c) only (wrong: a later arrival with more budget may be the only
way through); forgetting the target check at push time versus pop time (either works, be
consistent); not handling the 1x1 grid; letting the budget go negative.
"""
from collections import deque
from itertools import combinations
from typing import List


class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        R, C = len(grid), len(grid[0])
        if k >= R + C - 2:
            return R + C - 2                                  # the Manhattan walk is affordable
        queue = deque([(0, 0, k)])                            # (row, col, eliminations left)
        seen = {(0, 0, k)}
        steps = 0
        while queue:
            for _ in range(len(queue)):
                r, c, left = queue.popleft()
                if (r, c) == (R - 1, C - 1):
                    return steps
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < R and 0 <= nc < C:
                        nl = left - grid[nr][nc]              # stepping on a 1 spends one
                        if nl >= 0 and (nr, nc, nl) not in seen:
                            seen.add((nr, nc, nl))
                            queue.append((nr, nc, nl))
            steps += 1
        return -1


def brute_force(grid: List[List[int]], k: int) -> int:
    # Choose which obstacles to clear (every subset of size <= k), BFS the cleared grid, keep the best.
    R, C = len(grid), len(grid[0])
    obstacles = [(r, c) for r in range(R) for c in range(C) if grid[r][c] == 1]

    def bfs(cleared: set) -> int:
        dist, queue = {(0, 0): 0}, deque([(0, 0)])
        while queue:
            r, c = queue.popleft()
            if (r, c) == (R - 1, C - 1):
                return dist[(r, c)]
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in dist \
                        and (grid[nr][nc] == 0 or (nr, nc) in cleared):
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))
        return -1

    best = -1
    for size in range(min(k, len(obstacles)) + 1):           # C(B, <= k) subsets, each a full BFS
        for subset in combinations(obstacles, size):
            d = bfs(set(subset))
            if d >= 0 and (best < 0 or d < best):
                best = d
    return best


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1, 6),
        ([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1, -1),
        ([[0]], 0, 0),                                        # already at the target
        ([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 2, 4),            # two eliminations open a straight route
        ([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0, 10),            # no eliminations: detour
        ([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 1, 6),
    )
    for grid, k, want in cases:
        assert s.shortestPath(grid, k) == want, (grid, k)
        assert brute_force(grid, k) == want, (grid, k)
    print("ok")
