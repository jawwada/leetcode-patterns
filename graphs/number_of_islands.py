"""
Number of Islands (LeetCode 200)  — Medium
Pattern: Grid flood fill (DFS/BFS)

Problem
-------
Given an m x n grid of '1' (land) and '0' (water), count the islands. An island is a
maximal group of '1's connected 4-directionally (not diagonally).
Example: [["1","1","0"],["0","1","0"],["0","0","1"]] -> 2.

Brute force
-----------
For every land cell, run a full DFS from it and collect the set of cells it reaches; then
dedupe those sets (e.g. keep only the DFS whose start is the lexicographically smallest
cell in its component). Every cell of an island of size k is explored k times, so total
work is O((mn)^2) in the worst case (one giant island), O(mn) extra space. The wasted step
is re-exploring a component we have already fully seen.

From brute force to optimal
---------------------------
The redundancy is re-walking cells that already belong to a counted island. Observation:
once a DFS from any cell of an island finishes, every cell of that island has been
visited, so no other cell of it should ever start a new search. Exploit it by marking
cells as visited the moment we touch them (sink the '1' to '0', or use a visited set); a
new DFS starts only from an unvisited '1', and each such start is exactly one island.
Every cell is now entered at most once -> O(mn).

Intuition
---------
"Count the number of times you have to start a new flood." Scan the grid row by row;
whenever you hit land that is still unvisited, that is a brand-new island, so count it,
then sink the whole island so no other cell of it will trigger another count.

Geometric view
--------------
Picture pouring paint onto the grid: each time the scan pointer lands on dry land it
pours, and paint spreads to all 4-connected land. The number of pours is the answer.
The DFS stack is the "wet front" of the paint expanding outward from the pour point.

Steps
-----
1. Loop over every cell (r, c).
2. If grid[r][c] == '1': increment the count and flood-fill from (r, c).
3. Flood fill: set the cell to '0', then recurse/push its 4 in-bounds land neighbours.
4. Return the count.

Complexity: O(m*n) time, O(m*n) space — every cell is sunk once; stack can hold a whole island.
Pitfalls: forgetting bounds checks; mutating input when the caller still needs it (copy if so);
recursion depth on 300x300 grids — use an explicit stack.
"""
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        count = 0

        def sink(r: int, c: int) -> None:
            stack = [(r, c)]
            grid[r][c] = "0"
            while stack:
                x, y = stack.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                        grid[nx][ny] = "0"  # mark on push, not on pop, to avoid duplicates
                        stack.append((nx, ny))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    sink(r, c)
        return count


def brute_force(grid: List[List[str]]) -> int:
    # From every land cell, explore its whole component without any shared visited state;
    # count the cell only if it is the smallest (row, col) in that component.
    rows, cols = len(grid), len(grid[0])

    def component(r: int, c: int) -> set:
        seen = {(r, c)}
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1" and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        return seen

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and min(component(r, c)) == (r, c):
                count += 1
    return count


if __name__ == "__main__":
    import copy

    s = Solution()
    g1 = [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
    g2 = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
    g3 = [["0"]]
    g4 = [["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]
    for g, want in ((g1, 1), (g2, 3), (g3, 0), (g4, 5)):
        assert brute_force(copy.deepcopy(g)) == want
        assert s.numIslands(copy.deepcopy(g)) == want
    print("ok")
