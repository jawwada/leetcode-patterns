"""
Unique Paths III (LeetCode 980)  — Hard
Pattern: Hamiltonian-path DFS on a grid with a remaining-cells counter

Problem
-------
A grid holds exactly one 1 (start), one 2 (end), some 0s (empty) and some -1s (obstacles). Count
the 4-directional walks from start to end that visit EVERY empty cell exactly once and never touch
an obstacle or repeat a cell.
Example: [[1,0,0,0],[0,0,0,0],[0,0,2,-1]] -> 2.  [[0,1],[2,0]] -> 0 (whichever empty cell the
start steps to first, its only onward move is the end, leaving the other empty cell unvisited).

Brute force
-----------
A valid walk is an ordering of the k empty cells. Enumerate all k! permutations and, for each,
check that start -> perm[0] -> ... -> perm[k-1] -> end is a chain of adjacent cells.
O(k! * k) time, O(k) space; exponential. The waste: a permutation whose first two cells are not
neighbours is still generated together with all (k-2)! orderings of its tail, every one of which is
rejected for the same reason.

From brute force to optimal
---------------------------
The redundancy is generating orderings whose prefix is already impossible. Observation: a walk
can be grown one step at a time, and the only cells that may follow (r, c) are its four unvisited
non-obstacle neighbours. So do DFS from the start, marking cells in place as visited, and count how
many empty cells are still unvisited (todo). Reaching the end is a success only if todo == 0;
reaching it earlier is a dead end (the walk cannot continue past the end). Dead prefixes die at the
first bad step instead of after (k-2)! completions, and the counter makes the "all cells used" check
O(1) at the leaf. In-place marking (grid[r][c] = -1, restored on return) needs no visited set.

Intuition
---------
This is Hamiltonian path counting on a small grid: no polynomial algorithm, so the job is a clean
exhaustive search with early termination. The two things to track are "where am I" and "how many
cells are still owed"; the end cell acts as a sink that is only accepted when the debt is zero.

Geometric view
--------------
A snake growing from the start cell; its body (marked -1) is the DFS stack drawn on the floor.
At each head position the snake tries up to four moves into unmarked cells; when it corners
itself (no unmarked neighbour) the tail retracts one cell and the next direction is tried. Only
snakes that cover the whole floor and end on the 2 are counted.

Steps
-----
1. One pass: find start (sr, sc), count empties; todo = empties + 1 (the end cell itself).
2. dfs(r, c, todo): if grid[r][c] == 2 return 1 if todo == 0 else 0.
3. Save grid[r][c], set it to -1 (visited), sum dfs over the 4 neighbours that are in bounds and
   hold 0 or 2, passing todo - 1.
4. Restore grid[r][c]; return the sum.
5. Answer = dfs(sr, sc, todo).

Complexity: O(4^(R*C)) time worst case (the walk has at most 3 real choices per step, so
O(3^(R*C)) in practice), O(R*C) space for the recursion — the grid is at most 20 cells.
Pitfalls: counting a path that reaches the end with empties left over; forgetting to count the
end cell in todo (off by one); not restoring the cell on backtrack; stepping onto the start
again (it is marked while on the stack, so this is only a problem if you unmark too early).
"""
from itertools import permutations
from typing import List


class Solution:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        R, C = len(grid), len(grid[0])
        todo = 1                                            # empties still to visit + the end cell
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 1:
                    sr, sc = r, c
                elif grid[r][c] == 0:
                    todo += 1

        def dfs(r: int, c: int, todo: int) -> int:
            if grid[r][c] == 2:
                return 1 if todo == 0 else 0                # end reached: all cells used?
            saved, grid[r][c] = grid[r][c], -1              # mark the cell while on the path
            count = 0
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] in (0, 2):
                    count += dfs(nr, nc, todo - 1)
            grid[r][c] = saved                              # unmark on backtrack
            return count

        return dfs(sr, sc, todo)


def brute_force(grid: List[List[int]]) -> int:
    # Every ordering of the empty cells; keep those forming an adjacent chain start -> ... -> end.
    cells = {v: (r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v in (1, 2)}
    empties = [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 0]

    def adjacent(a, b) -> bool:
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    count = 0
    for order in permutations(empties):                     # k! orderings, checked only when complete
        chain = (cells[1],) + order + (cells[2],)
        if all(adjacent(chain[i], chain[i + 1]) for i in range(len(chain) - 1)):
            count += 1
    return count


if __name__ == "__main__":
    s = Solution()
    assert s.uniquePathsIII([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]]) == 2
    assert s.uniquePathsIII([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]]) == 4
    assert s.uniquePathsIII([[0, 1], [2, 0]]) == 0
    assert s.uniquePathsIII([[1, 2]]) == 1                              # adjacent, nothing to visit
    small = (
        [[0, 1], [2, 0]], [[1, 2]], [[1, 0, 0], [0, 0, 2]], [[1, 0, 0], [0, -1, 0], [0, 0, 2]],
        [[1, 0, 0], [0, 0, 0], [2, 0, 0]], [[1, 0, 0, 0], [0, 0, 0, 2]],
    )
    for g in small:                                                     # k <= 7 empties
        a = s.uniquePathsIII([row[:] for row in g])
        assert a == brute_force(g), (g, a)
    print("ok")
