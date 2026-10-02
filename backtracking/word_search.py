"""
Word Search (LeetCode 79)  — Medium
Pattern: Grid DFS backtracking with in-place visited marking

Problem
-------
Given an m x n grid of letters and a word, return True if the word can be traced through
horizontally or vertically adjacent cells, using each cell at most once.
Example: board=[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="ABCCED" -> True;
word="ABCB" -> False (the B would have to be reused).

Brute force
-----------
From every cell, enumerate every self-avoiding path of exactly len(word) cells (up to 4^L of
them), spell out the letters along each path, and compare the whole string to word at the end.
O(m * n * 4^L * L) time, O(L) space. The waste: a path whose FIRST letter is already wrong is
still extended for L-1 more steps and its string is still built; almost all 4^L paths are dead
after one or two letters, but the comparison happens only at the leaf.

From brute force to optimal
---------------------------
The redundancy is extending paths that have already failed. Observation: the path spells the
word prefix by prefix, so compare the current cell against word[k] at step k and cut the branch
immediately on a mismatch. Nothing else about the search changes: same DFS, same "each cell once"
rule, but the live tree is now only the paths that match a prefix of the word, which on real
boards is tiny. Visited bookkeeping is done in place by overwriting the cell with a sentinel
before recursing and restoring it after, saving a separate O(m n) visited matrix.

Intuition
---------
Walk the grid letter by letter, matching the word as you go; the moment a cell does not match
the next letter, turn back. Temporarily blank a cell while standing on it so you cannot step on
it twice.

Geometric view
--------------
From each matching start cell grows a 4-ary decision tree (up/right/down/left). Branches are
drawn only as far as the letters agree with the word; a mismatch or an off-grid/blanked cell
ends the branch (pruned). The path on the grid is a snake of blanked cells that retracts as the
recursion returns.

Steps
-----
1. For each cell (r, c) call dfs(r, c, 0).
2. dfs: if k == len(word) return True. If (r, c) is off-grid or board[r][c] != word[k] return False.
3. Save the letter, overwrite the cell with "#", try the four neighbours with k + 1.
4. Restore the letter; return whether any neighbour succeeded.

Complexity: O(m * n * 3^L) time (first step 4 ways, later steps at most 3 since we cannot go
back), O(L) recursion space.
Pitfalls: Forgetting to restore the cell after the recursion (corrupts later searches); checking
bounds after indexing (IndexError / negative-index wraparound); not short-circuiting once found.
"""
from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int, k: int) -> bool:
            if k == len(word):
                return True
            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[k]:
                return False                                # prune: off-grid, used, or mismatch
            saved, board[r][c] = board[r][c], "#"           # mark visited in place
            found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                     or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
            board[r][c] = saved                             # un-mark on the way back
            return found

        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


def brute_force(board: List[List[str]], word: str) -> bool:
    rows, cols, L = len(board), len(board[0]), len(word)

    def paths(r, c, visited, letters):                      # every self-avoiding path of length L
        if len(letters) == L:
            return "".join(letters) == word                  # compared only at the leaf
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if paths(nr, nc, visited | {(nr, nc)}, letters + [board[nr][nc]]):
                    return True
        return False

    return any(paths(r, c, {(r, c)}, [board[r][c]]) for r in range(rows) for c in range(cols))


if __name__ == "__main__":
    s = Solution()
    grid = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert s.exist([row[:] for row in grid], "ABCCED") is True
    assert s.exist([row[:] for row in grid], "SEE") is True
    assert s.exist([row[:] for row in grid], "ABCB") is False          # would need to reuse B
    assert s.exist([["a"]], "a") is True                                # 1x1 grid
    assert s.exist([["a"]], "ab") is False
    for word in ("ABCCED", "SEE", "ABCB", "ESEE", "FCS"):
        assert s.exist([row[:] for row in grid], word) == brute_force(grid, word), word
    assert grid == [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]  # restored
    print("ok")
