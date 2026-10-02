"""
Sudoku Solver (LeetCode 37)  — Hard
Pattern: Constraint backtracking with bitmasks (most-constrained cell first)

Problem
-------
Fill a partially filled 9x9 board (digits '1'-'9', '.' for empty) in place so that every row,
every column and every 3x3 box contains each digit exactly once. The input has exactly one
solution.
Example: a board whose first row is "53..7...." is completed to "534678912" and so on.

Brute force
-----------
Scan for the first empty cell, try the digits 1..9 in order, and for each digit walk the whole
row, column and box (27 cells) to check it is legal; recurse, undo on failure.
Exponential: O(9^E) leaves in the worst case for E empty cells, each node paying O(27) to validate.
The waste is twofold: (1) every placement rescans 27 cells to rediscover which digits are already
used, information that could be kept incrementally; (2) the first empty cell is expanded even when
it has 6 legal digits while another cell has exactly 1 - the search branches 6 ways where it could
branch once.

From brute force to optimal
---------------------------
Redundancy 1 is the 27-cell rescan. Observation: "digit d is already used in row r" is a set
membership, so keep one 9-bit mask per row, per column and per box; the legal digits of a cell are
the complement of the OR of its three masks, computed in O(1), and a placement is three OR-ins
that are undone with three XORs. Redundancy 2 is branching on a loosely constrained cell: every
subtree below a wrong choice is explored before the contradiction surfaces in some other cell.
Observation (minimum remaining values): pick the empty cell with the fewest legal digits; a cell
with 0 candidates makes the branch die immediately and a cell with 1 candidate is a forced move
that costs nothing. Together these cut the search tree from millions of nodes to a few hundred on
typical puzzles. The invariant: masks always equal the digits currently on the board.

Intuition
---------
Sudoku is "assign a value to each variable subject to all-different constraints". Backtracking is
the only general tool, so the game is pruning: detect contradictions as early as possible (masks
make the legality test free) and always extend the partial solution where the fewest options
remain (so wrong guesses are discovered after one or two levels, not twenty).

Geometric view
--------------
Picture three 9x9 "shadow" grids of bits: one lit per (row, digit), (col, digit), (box, digit).
A cell's candidates are the dark digits in all three shadows at once. The search tree is very
narrow: at each level we choose the cell whose shadow intersection is smallest, so most levels
have one child (forced), a few have two or three, and dead ends (zero candidates) are cut on sight.

Steps
-----
1. Scan the board once: build rows[9], cols[9], boxes[9] bitmasks and the list of empty cells.
2. dfs(): if no empty cells remain, the board is solved.
3. Choose the empty cell with the fewest candidates (candidates = ~(row|col|box) & 0x3FE).
4. For each set bit d: place d (board, three masks), recurse, and on failure undo all four.
5. If no digit works, put the cell back on the list and return False to the caller.

Complexity: O(9^E) time worst case but tiny in practice, O(E) space — the masks are 27 ints and
the recursion depth equals the number of empty cells.
Pitfalls: forgetting to undo the masks (not just the board) when backtracking; using bit 0 for
digit 1 and mixing it up with 1 << d; computing the box index as r // 3 + c // 3 instead of
r // 3 * 3 + c // 3.
"""
from copy import deepcopy
from typing import List


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9     # bit d set <=> digit d already used
        empties = []
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    empties.append((r, c))
                else:
                    bit = 1 << int(board[r][c])
                    rows[r] |= bit; cols[c] |= bit; boxes[r // 3 * 3 + c // 3] |= bit

        def candidates(r: int, c: int) -> int:        # 9-bit mask of legal digits for (r, c)
            return ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & 0x3FE

        def dfs() -> bool:
            if not empties:
                return True
            # MRV: expand the cell with the fewest legal digits (0 -> immediate dead end)
            i = min(range(len(empties)), key=lambda k: bin(candidates(*empties[k])).count("1"))
            empties[i], empties[-1] = empties[-1], empties[i]
            r, c = empties.pop()
            b = r // 3 * 3 + c // 3
            cand = candidates(r, c)
            while cand:
                bit = cand & -cand                        # lowest candidate digit
                cand ^= bit
                rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
                board[r][c] = str(bit.bit_length() - 1)
                if dfs():
                    return True
                rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
            board[r][c] = "."
            empties.append((r, c))
            empties[i], empties[-1] = empties[-1], empties[i]
            return False

        dfs()


def brute_force(board: List[List[str]]) -> None:
    # First empty cell, digits 1..9 in order, legality by rescanning row + column + box.
    def legal(r: int, c: int, d: str) -> bool:
        br, bc = r // 3 * 3, c // 3 * 3
        return all(board[r][k] != d and board[k][c] != d and
                   board[br + k // 3][bc + k % 3] != d for k in range(9))

    def solve() -> bool:
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for d in "123456789":
                        if legal(r, c, d):
                            board[r][c] = d
                            if solve():
                                return True
                            board[r][c] = "."
                    return False                          # exponential: no digit fits here
        return True

    solve()


def valid(board: List[List[str]]) -> bool:
    units = [[(r, c) for c in range(9)] for r in range(9)]
    units += [[(r, c) for r in range(9)] for c in range(9)]
    units += [[(br + k // 3, bc + k % 3) for k in range(9)] for br in (0, 3, 6) for bc in (0, 3, 6)]
    return all(sorted(board[r][c] for r, c in u) == list("123456789") for u in units)


if __name__ == "__main__":
    s = Solution()
    puzzle = [list(row) for row in [
        "53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
        "7...2...6", ".6....28.", "...419..5", "....8..79"]]
    expected = [list(row) for row in [
        "534678912", "672195348", "198342567", "859761423", "426853791",
        "713924856", "961537284", "287419635", "345286179"]]
    a, b = deepcopy(puzzle), deepcopy(puzzle)
    s.solveSudoku(a); brute_force(b)
    assert a == expected and b == expected

    harder = [list(row) for row in [                      # 17-clue style puzzle, many empties
        "..9748...", "7........", ".2.1.9...", "..7...24.", ".64.1.59.",
        ".98...3..", "...8.3.2.", "........6", "...2759.."]]
    h = deepcopy(harder)
    s.solveSudoku(h)
    assert valid(h) and all(h[r][c] == harder[r][c] for r in range(9) for c in range(9)
                            if harder[r][c] != ".")

    full = deepcopy(expected)                              # edge: nothing to fill
    s.solveSudoku(full)
    assert full == expected
    print("ok")
