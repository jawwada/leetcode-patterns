"""
Max Area of Island (LeetCode 695)  — Medium
Pattern: Grid flood fill (DFS/BFS)

Problem
-------
Given an m x n binary grid, an island is a maximal 4-connected group of 1s. Return the
largest island area (number of cells), or 0 if there is no land.
Example: [[0,1,0],[1,1,0],[0,0,1]] -> 3.

Brute force
-----------
From every land cell independently, run a DFS with its own local visited set and record
the size reached; take the max. Each cell of an island of size k is the start of a DFS
that walks all k cells, so one island costs O(k^2) and the total is O((mn)^2) time in
the worst case, O(mn) space. The wasted step is recomputing the size of the same island
once per cell it contains.

From brute force to optimal
---------------------------
The redundancy is measuring the same island k times. Observation: the area of an island
is a property of the component, not of the starting cell, so one measurement per
component suffices. Share the visited state across all starts (sink 1s to 0s as you go):
then a DFS launched from a cell only ever covers cells nobody has counted before, each
island is measured exactly once from its first-scanned cell, and the total work is O(mn).

Intuition
---------
Same scan as Number of Islands, but instead of counting floods, each flood returns how
many cells it swallowed. Keep the largest return value. Sinking cells as you count them
is what makes the count exact and the total linear.

Geometric view
--------------
Picture the grid as a map with lakes of 1s. A scanning pointer walks row by row; when it
hits land it drops an expanding wavefront (DFS stack) that eats the whole island and
tallies the cells eaten. Each island is eaten once; the biggest meal is the answer.

Steps
-----
1. For every cell, if it is 1: run a flood fill from it that sets each visited cell to 0
   and counts cells.
2. Update best = max(best, flood size).
3. Return best (0 if the grid has no 1s).

Complexity: O(m*n) time, O(m*n) space — each cell is sunk once; the stack may hold the whole island.
Pitfalls: counting a cell on pop rather than on push can double-count when pushed twice;
forgetting that the answer is 0 (not -inf) for an all-water grid.
"""
from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])

        def flood(r: int, c: int) -> int:
            grid[r][c] = 0
            stack, area = [(r, c)], 1
            while stack:
                x, y = stack.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                        grid[nx][ny] = 0  # claim on push so each cell is counted once
                        area += 1
                        stack.append((nx, ny))
            return area

        best = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    best = max(best, flood(r, c))
        return best


def brute_force(grid: List[List[int]]) -> int:
    # Measure the island from EVERY land cell with a private visited set; take the max.
    rows, cols = len(grid), len(grid[0])

    def size_from(r: int, c: int) -> int:
        seen, stack = {(r, c)}, [(r, c)]
        while stack:
            x, y = stack.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1 and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        return len(seen)

    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                best = max(best, size_from(r, c))
    return best


if __name__ == "__main__":
    import copy

    s = Solution()
    g1 = [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ]
    g2 = [[0, 0, 0, 0, 0, 0, 0, 0]]
    g3 = [[1]]
    g4 = [[0, 1, 0], [1, 1, 0], [0, 0, 1]]
    for g, want in ((g1, 6), (g2, 0), (g3, 1), (g4, 3)):
        assert brute_force(copy.deepcopy(g)) == want
        assert s.maxAreaOfIsland(copy.deepcopy(g)) == want
    print("ok")
