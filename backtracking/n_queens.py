"""
N-Queens (LeetCode 51)  — Hard
Pattern: Row-by-row backtracking with column/diagonal sets

Problem
-------
Place n queens on an n x n board so that no two attack each other (same row, column or diagonal).
Return every distinct board as a list of strings where "Q" is a queen and "." is empty.
Example: n=4 -> [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]].  n=1 -> [["Q"]].

Brute force
-----------
One queen per row is forced, so try every permutation of column indices (n! boards), then check
every pair of queens for a shared diagonal and keep the valid boards.
O(n! * n^2) time, O(n) space beyond the output. The waste: a permutation whose first two queens
already attack each other diagonally is still completed and then checked pairwise; the (n-2)!
completions of that doomed prefix are all generated and all rejected.

From brute force to optimal
---------------------------
The redundancy is completing placements that are already in conflict. Observation: placing
queens row by row, a new queen at (r, c) conflicts with earlier queens iff column c, diagonal
r - c, or anti-diagonal r + c is already taken. Three hash sets answer that in O(1), so a conflict
is detected the moment it is created and the whole subtree below it is skipped. The search tree
has n children per level but most are cut immediately; the surviving leaves are exactly the
solutions. Using permutations was already a big pruning (no two queens in one column); the sets
add the diagonals and move the check from the leaf to the node.

Intuition
---------
Fill the board one row at a time; for each row try every column that is not under attack. A
queen at (r, c) owns one column, one "\\" diagonal (constant r - c) and one "/" diagonal
(constant r + c), so three sets fully describe "under attack".

Geometric view
--------------
A tree with n levels (rows) and up to n children per node (columns). Each placed queen shades
its column and two diagonals on the board below; the children of a node are only the unshaded
squares of the next row. When a row has no unshaded square the branch dies and the last queen is
lifted. Leaves at depth n are solutions.

Steps
-----
1. cols, diag (r - c), anti (r + c) = empty sets; queens = [] (column chosen for each row).
2. dfs(r): if r == n, render the board from queens and record it.
3. For c in range(n): skip if c in cols or r - c in diag or r + c in anti.
4. Add to the three sets, append c, dfs(r + 1), then remove / pop.
5. Call dfs(0), return result.

Complexity: O(n!) time (upper bound on the surviving tree), O(n) space for the sets and the
recursion beyond the output.
Pitfalls: Using r + c for both diagonals (they need different keys); forgetting to remove from
the sets on backtrack; rendering the board as rows of columns swapped (queens[r] is the column
of row r).
"""
from itertools import permutations
from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result: List[List[str]] = []
        queens: List[int] = []                      # queens[r] = column of the queen in row r
        cols, diag, anti = set(), set(), set()      # attacked columns, r-c diagonals, r+c diagonals

        def dfs(r: int) -> None:
            if r == n:
                result.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
                return
            for c in range(n):
                if c in cols or r - c in diag or r + c in anti:
                    continue                        # under attack: prune this branch
                cols.add(c); diag.add(r - c); anti.add(r + c)
                queens.append(c)
                dfs(r + 1)
                queens.pop()
                cols.discard(c); diag.discard(r - c); anti.discard(r + c)

        dfs(0)
        return result


def brute_force(n: int) -> List[List[str]]:
    out = []
    for cols in permutations(range(n)):                              # n! column assignments
        ok = all(abs(cols[i] - cols[j]) != j - i                     # checked only when complete
                 for i in range(n) for j in range(i + 1, n))
        if ok:
            out.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
    return out


if __name__ == "__main__":
    s = Solution()
    four = s.solveNQueens(4)
    assert sorted(four) == sorted([[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]])
    assert s.solveNQueens(1) == [["Q"]]
    assert s.solveNQueens(2) == [] and s.solveNQueens(3) == []      # no solutions
    assert len(s.solveNQueens(6)) == 4 and len(s.solveNQueens(8)) == 92
    for n in range(1, 7):
        assert sorted(s.solveNQueens(n)) == sorted(brute_force(n)), n
    print("ok")
