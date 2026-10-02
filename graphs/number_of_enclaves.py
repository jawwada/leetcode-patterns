"""
Number of Enclaves (LeetCode 1020)  — Medium
Pattern: Multi-source reverse BFS/DFS from the boundary

Problem
-------
In an m x n grid, 1 is land and 0 is sea. A move goes to a 4-adjacent land cell or off
the edge of the grid. Return the number of land cells from which you can NOT walk off
the grid. Example: [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]] -> 3 ((1,0) touches the
border and escapes; the other three are enclosed).

Brute force
-----------
For every land cell, run its own BFS/DFS and check whether it can reach any border
cell. A single search can cover the whole island, so an island of size k costs O(k^2),
O((m*n)^2) overall, O(m*n) space. The waste: all cells of one island share the same
answer, but each recomputes it from scratch.

From brute force to optimal
---------------------------
The redundancy is answering the same reachability question once per cell of an island.
Reverse the question: instead of "can this cell reach the border?", ask "which cells can
the border reach?". Escape is symmetric (land paths are undirected), so flood fill from
every border land cell and sink everything reached. What remains as 1 is exactly the
enclaves; count them. Each cell is sunk at most once: O(m*n). This is the user's
original approach, with the recursion replaced by an explicit stack.

Intuition
---------
A land cell escapes iff its island touches the border. Sink all border-touching islands
in one sweep starting from the edge; count the land left standing.

Geometric view
--------------
Picture the sea rising from outside the frame: it pours in through every border land
cell and drowns its whole island. Islands fully surrounded by inner water stay dry; the
dry cells are the answer.

Steps
-----
1. Push every border cell that is land.
2. DFS: pop a cell, if still land set it to 0 and push its 4 neighbours.
3. Count the remaining 1s.

Complexity: O(m*n) time, O(m*n) space — each cell sunk once; stack bounded by grid size.
Pitfalls: counting islands instead of cells; deep recursion on a 500x500 grid (use an
explicit stack); forgetting the corner/edge cells on both axes.
"""
from typing import List


class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        stack = [(r, c) for r in range(m) for c in range(n)
                 if (r in (0, m - 1) or c in (0, n - 1)) and grid[r][c] == 1]
        while stack:  # sink everything the border can reach
            r, c = stack.pop()
            if 0 <= r < m and 0 <= c < n and grid[r][c] == 1:
                grid[r][c] = 0
                stack.extend(((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)))
        return sum(map(sum, grid))


def brute_force(grid: List[List[int]]) -> int:
    # Separate search from every land cell to see if it can step off the grid: O((m*n)^2).
    m, n = len(grid), len(grid[0])
    count = 0
    for sr in range(m):
        for sc in range(n):
            if grid[sr][sc] != 1:
                continue
            seen, stack, escapes = {(sr, sc)}, [(sr, sc)], False
            while stack and not escapes:
                r, c = stack.pop()
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if not (0 <= nr < m and 0 <= nc < n):
                        escapes = True
                    elif grid[nr][nc] == 1 and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            count += not escapes
    return count


if __name__ == "__main__":
    import copy

    s = Solution()
    cases = [([[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]], 3),
             ([[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]], 0),
             ([[1]], 0),
             ([[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 1, 0, 1, 1], [0, 0, 0, 0, 0]], 3)]
    for g, want in cases:
        assert brute_force(copy.deepcopy(g)) == want
        assert s.numEnclaves(copy.deepcopy(g)) == want
    print("ok")
