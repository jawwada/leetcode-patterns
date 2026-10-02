"""
Valid Sudoku (LeetCode 36)  — Medium
Pattern: Hash set per row/column/box

Problem
-------
Given a 9x9 board of digits '1'-'9' and '.' for empty, decide whether the FILLED
cells are valid: no digit repeats in any row, any column, or any of the nine 3x3
boxes. Do not check solvability. Example: a board where row 0 contains two '5's -> False.

Brute force
-----------
For each of the 81 cells, scan its entire row, its entire column and its 3x3 box
looking for the same digit elsewhere. O(81 * 27) comparisons, O(1) space. The waste
is that each row is re-scanned by all nine of its cells (likewise columns and boxes),
so every pair of cells in the same unit is compared twice and every unit is read
nine times instead of once.

From brute force to optimal
---------------------------
The brute force asks "does this digit appear elsewhere in my row?" by scanning. That
is a membership question, and a set answers it in O(1). Give each row, each column
and each box its own set; then one pass over the board does all 27 checks at once:
for each filled cell, test-and-insert its digit into the three sets it belongs to. A
repeat is detected the moment the second copy is inserted. The only non-obvious part
is addressing the box: (r // 3, c // 3) identifies which of the 9 boxes a cell is in.

Intuition
---------
Validity is 27 independent "all distinct" constraints. "All distinct" over a stream
is checked by inserting into a set and watching for a collision. Doing all 27 sets
simultaneously in one sweep is just bookkeeping.

Geometric view
--------------
Picture the 9x9 grid with three overlays: 9 horizontal bands, 9 vertical bands, and
a 3x3 tiling of boxes. Every cell lies under exactly one band of each kind. The
sweep moves row by row; each filled cell "lights up" its digit in the three overlays
it sits under, and a cell that finds its digit already lit in any overlay fails.

Steps
-----
1. Create three lists of 9 empty sets: rows, cols, boxes.
2. For each cell (r, c) with digit d != '.', compute b = (r // 3) * 3 + c // 3.
3. If d is already in rows[r], cols[c] or boxes[b], return False.
4. Otherwise add d to all three.
5. Return True after the sweep.

Complexity: O(1) time, O(1) space — the board is fixed at 81 cells; expressed as
O(n^2) time and O(n) space for an n x n board.
Pitfalls: computing the box index with (r // 3, c // 3) only in one direction; checking
empty cells '.' as duplicates; thinking the puzzle must be solvable.
"""
from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                d = board[r][c]
                if d == ".":
                    continue
                b = (r // 3) * 3 + c // 3   # which of the nine 3x3 boxes
                if d in rows[r] or d in cols[c] or d in boxes[b]:
                    return False
                rows[r].add(d)
                cols[c].add(d)
                boxes[b].add(d)
        return True


def brute_force(board: List[List[str]]) -> bool:
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d == ".":
                continue
            for k in range(9):
                if k != c and board[r][k] == d:
                    return False
                if k != r and board[k][c] == d:
                    return False
            br, bc = 3 * (r // 3), 3 * (c // 3)
            for i in range(br, br + 3):
                for j in range(bc, bc + 3):
                    if (i, j) != (r, c) and board[i][j] == d:
                        return False
    return True


def _board(rows: List[str]) -> List[List[str]]:
    return [list(row) for row in rows]


if __name__ == "__main__":
    s = Solution()
    valid = _board([
        "53..7....", "6..195...", ".98....6.",
        "8...6...3", "4..8.3..1", "7...2...6",
        ".6....28.", "...419..5", "....8..79",
    ])
    invalid_row = _board([
        "83..7....", "6..195...", ".98....6.",
        "8...6...3", "4..8.3..1", "7...2...6",
        ".6....28.", "...419..5", "....8..79",
    ])  # two 8s in column 0 / box 0
    invalid_box = _board([
        "53..7....", "6..195...", ".95....6.",
        "8...6...3", "4..8.3..1", "7...2...6",
        ".6....28.", "...419..5", "....8..79",
    ])  # two 5s in the top-left box
    empty = _board(["........."] * 9)
    assert s.isValidSudoku(valid) is True
    assert s.isValidSudoku(invalid_row) is False
    assert s.isValidSudoku(invalid_box) is False
    assert s.isValidSudoku(empty) is True
    for b in (valid, invalid_row, invalid_box, empty):
        assert s.isValidSudoku(b) == brute_force(b)
    print("ok")
