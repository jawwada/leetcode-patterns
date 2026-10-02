"""
Trapping Rain Water II (LeetCode 407)  — Hard
Pattern: Min-heap frontier expanding inward from the boundary (lowest wall first)

Problem
-------
Given an m x n elevation map, return the volume of water trapped after raining. Water can only
escape over the border, flowing through 4-directionally adjacent cells.
Example: [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]] -> 4. Only the middle row is interior;
its cells (1,1)=2, (1,2)=1, (1,3)=3, (1,4)=2 all fill to level 3, holding
(3-2) + (3-1) + (3-3) + (3-2) = 1 + 2 + 0 + 1 = 4.

Brute force
-----------
Let level[c] be the final water surface at cell c. Border cells have level = height (water
runs off). Every interior cell obeys level[c] = max(height[c], min over neighbours of level).
Initialise interior levels to infinity and sweep the grid repeatedly, lowering levels by that
rule, until a full sweep changes nothing; the answer is sum(level - height). Each sweep is
O(mn) and the number of sweeps can be O(mn) (a level drop can propagate one cell per sweep
along a snaking path), so O((mn)^2) time, O(mn) space. The waste: every sweep re-examines
every cell although only cells next to a just-lowered neighbour can change.

From brute force to optimal
---------------------------
The redundancy is visiting cells whose level cannot change yet. Observation: the water level
at a cell equals the minimax path value to the border -- the smallest, over all escape paths,
of the tallest wall on the path. That is exactly a shortest-path problem with "max" instead of
"sum", so Dijkstra applies: start from all border cells (their level is their own height) in a
min-heap keyed by level, repeatedly pop the lowest cell on the frontier, and for each unvisited
neighbour set its level to max(popped level, its height), bank the difference as water, and
push it. Popping in increasing order guarantees that when a cell is settled, no lower escape
route exists. Each cell enters the heap once: O(mn log(mn)).

Intuition
---------
Imagine the outer ring as a dam of varying height, and water rising from the outside. The
weakest point of the dam is its lowest cell; water pours over it into the neighbour behind,
which either sits lower (fills up to the dam's level, trapping water) or higher (becomes part
of a new, taller wall). Either way that neighbour now belongs to the dam and the old low point
is retired. Always breach the lowest cell of the current dam and the fill levels come out
exactly right.

Geometric view
--------------
A ring of boundary cells drawn as a closed curve with heights as colours; a min-heap triangle
holds the ring with its lowest cell at the apex. Each step pops the apex, pulls its unvisited
neighbours into the ring at height max(apex level, own height), and the ring shrinks inward.
The volume accumulates as the sum over cells of (level they joined the ring at - own height).

Steps
-----
1. Push every border cell (height, r, c) into a min-heap and mark it visited.
2. While the heap is not empty: pop (level, r, c).
3. For each unvisited 4-neighbour (nr, nc): mark visited; water += max(0, level - h[nr][nc]);
   push (max(level, h[nr][nc]), nr, nc).
4. Return water.

Complexity: O(mn log(mn)) time, O(mn) space — every cell is pushed and popped once; the visited
grid and heap are the extra memory.
Pitfalls: Pushing the neighbour's own height instead of max(level, height) (water level never
drops as you move inward); forgetting to mark visited at push time (cells get pushed twice
with different levels); grids with fewer than 3 rows or columns hold nothing.
"""
import heapq
from typing import List


class Solution:
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        m, n = len(heightMap), len(heightMap[0])
        seen = [[False] * n for _ in range(m)]
        frontier = []                                 # min-heap of (water level, r, c)
        for r in range(m):
            for c in range(n):
                if r in (0, m - 1) or c in (0, n - 1):
                    seen[r][c] = True
                    frontier.append((heightMap[r][c], r, c))
        heapq.heapify(frontier)
        water = 0
        while frontier:
            level, r, c = heapq.heappop(frontier)     # lowest point of the current dam
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc]:
                    seen[nr][nc] = True
                    h = heightMap[nr][nc]
                    water += max(0, level - h)        # fills up to the dam's level
                    heapq.heappush(frontier, (max(level, h), nr, nc))
        return water


def brute_force(heightMap: List[List[int]]) -> int:
    # Relax level[c] = max(h[c], min(neighbour levels)) over the whole grid until stable.
    m, n = len(heightMap), len(heightMap[0])
    inf = float("inf")
    level = [[h if r in (0, m - 1) or c in (0, n - 1) else inf
              for c, h in enumerate(row)] for r, row in enumerate(heightMap)]
    changed = True
    while changed:
        changed = False
        for r in range(1, m - 1):
            for c in range(1, n - 1):
                low = min(level[r - 1][c], level[r + 1][c], level[r][c - 1], level[r][c + 1])
                new = max(heightMap[r][c], low)
                if new < level[r][c]:
                    level[r][c] = new
                    changed = True
    return sum(level[r][c] - heightMap[r][c] for r in range(m) for c in range(n))


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]], 4),
        ([[3, 3, 3, 3, 3], [3, 2, 2, 2, 3], [3, 2, 1, 2, 3], [3, 2, 2, 2, 3], [3, 3, 3, 3, 3]], 10),
        ([[1, 2], [3, 4]], 0),                                  # no interior cells
        ([[5, 5, 5], [5, 1, 5], [5, 5, 5]], 4),
        ([[5, 5, 5], [5, 1, 5], [5, 0, 5]], 0),                 # the low border cell drains it
    )
    for grid, want in cases:
        assert s.trapRainWater(grid) == want, (grid, want)
        assert brute_force(grid) == want, (grid, want)
    import random
    random.seed(407)
    for _ in range(150):
        m, n = random.randint(1, 6), random.randint(1, 6)
        grid = [[random.randint(0, 9) for _ in range(n)] for _ in range(m)]
        assert s.trapRainWater(grid) == brute_force(grid), grid
    print("ok")
