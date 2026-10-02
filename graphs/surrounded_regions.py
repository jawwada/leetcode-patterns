"""
Surrounded Regions (LeetCode 130)  — Medium
Pattern: Multi-source reverse BFS/DFS from the boundary

Problem
-------
Given an m x n board of 'X' and 'O', capture (flip to 'X') every region of 'O's that is
completely surrounded by 'X', i.e. that does not touch the border. Modify in place.
Example: [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
-> [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]].

Brute force
-----------
For every 'O' cell, flood-fill its region with a private visited set and check whether
any cell of the region lies on the border; if none does, flip the whole region. Every
cell of a region of size k launches a flood of size k, so a board that is all 'O' costs
O((mn)^2) time, O(mn) space. The waste is re-flooding and re-checking a region once per
cell it contains.

From brute force to optimal
---------------------------
The redundancy is deciding "is this region safe?" separately for each of its cells.
Observation: a region is safe exactly when it is reachable from a border 'O', so flip the
question around: start ONE traversal from all border 'O's at once and mark every 'O' it
reaches as safe. Everything unmarked is, by definition, surrounded. One multi-source BFS
visits each cell at most once -> O(mn), and no per-region border test is needed at all.

Intuition
---------
Do not look for what is surrounded; look for what is NOT. Any 'O' connected to the edge
escapes capture. Mark all escapees with a temporary letter (say 'S') via BFS from the
border, then one final sweep: 'O' -> 'X' (captured), 'S' -> 'O' (restored).

Geometric view
--------------
Picture the board's rim as a coastline and every border 'O' as a harbour. A BFS tide
flows inland from all harbours through connected 'O' cells; the frontier is the queue.
'O' islands the tide never reaches are inland lakes with no outlet, and those are the
ones that get filled with 'X'.

Steps
-----
1. Collect every border cell that is 'O' into a queue and mark it 'S'.
2. BFS: pop (r, c), for each in-bounds neighbour that is 'O', mark 'S' and enqueue.
3. Sweep the whole board: 'O' -> 'X', 'S' -> 'O'.

Complexity: O(m*n) time, O(m*n) space — each cell is enqueued at most once; the queue can hold O(mn) cells.
Pitfalls: scanning only corners rather than all four edges; flipping to 'X' before the
border BFS finishes (cells still needed as 'O'); forgetting to restore the sentinel.
"""
from collections import deque
from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        rows, cols = len(board), len(board[0])
        queue = deque()
        for r in range(rows):
            for c in range(cols):
                if (r in (0, rows - 1) or c in (0, cols - 1)) and board[r][c] == "O":
                    board[r][c] = "S"  # safe: touches the border
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                    board[nr][nc] = "S"
                    queue.append((nr, nc))
        for r in range(rows):
            for c in range(cols):
                board[r][c] = "O" if board[r][c] == "S" else "X"


def brute_force(board: List[List[str]]) -> None:
    # For every 'O', flood its region with a private visited set; flip only if no
    # member of the region lies on the border.
    rows, cols = len(board), len(board[0])
    for r0 in range(rows):
        for c0 in range(cols):
            if board[r0][c0] != "O":
                continue
            region, stack, on_border = {(r0, c0)}, [(r0, c0)], False
            while stack:
                r, c = stack.pop()
                on_border |= r in (0, rows - 1) or c in (0, cols - 1)
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O" and (nr, nc) not in region:
                        region.add((nr, nc))
                        stack.append((nr, nc))
            if not on_border:
                for r, c in region:
                    board[r][c] = "X"


if __name__ == "__main__":
    import copy

    s = Solution()
    b1 = [["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]
    want1 = [["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]]
    b2 = [["X"]]
    b3 = [["O", "O"], ["O", "O"]]
    b4 = [["O", "X", "O"], ["X", "O", "X"], ["O", "X", "O"]]
    want4 = [["O", "X", "O"], ["X", "X", "X"], ["O", "X", "O"]]
    for b, want in ((b1, want1), (b2, [["X"]]), (b3, [["O", "O"], ["O", "O"]]), (b4, want4)):
        a, c = copy.deepcopy(b), copy.deepcopy(b)
        s.solve(a)
        brute_force(c)
        assert a == want and c == want
    print("ok")
