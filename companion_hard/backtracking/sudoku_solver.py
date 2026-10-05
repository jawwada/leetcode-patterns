"""
Sudoku Solver (LeetCode 37) - Hard
Chapter: backtracking
Pattern: Constraint backtracking with bitmasks (most-constrained cell first)

Fill a partially filled 9x9 board (digits '1'-'9', '.' for empty) in place so that every row,
every column and every 3x3 box contains each digit exactly once. The input has one solution.
Example: the classic board whose first row is "53..7...." gets the first row "534678912".
"""


# --- helpers ---
PUZZLE = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
          "7...2...6", ".6....28.", "...419..5", "....8..79"]
SOLVED = ["534678912", "672195348", "198342567", "859761423", "426853791",
          "713924856", "961537284", "287419635", "345286179"]


def make_board(rows):
    """Nine strings -> a 9x9 grid of characters that the solver fills in place."""
    board = []
    for row in rows:
        board.append(list(row))
    return board


def show(board):
    """The 9x9 grid back as one line of nine 9-character words."""
    words = []
    for row in board:
        words.append("".join(row))
    return " ".join(words)


# --- brute force ---
def brute_force(board):
    """First empty cell, digits 1..9 in order, legality by rescanning row, column, box. O(9^E)."""
    solve_first_empty(board)
    return board


def legal(board, row, col, digit):
    """True when digit is not yet in the cell's row, column or 3x3 box (27 cells scanned)."""
    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for k in range(9):
        if board[row][k] == digit or board[k][col] == digit:
            return False
        if board[box_row + k // 3][box_col + k % 3] == digit:
            return False
    return True


def solve_first_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == ".":
                for digit in "123456789":
                    if legal(board, row, col, digit):
                        board[row][col] = digit
                        if solve_first_empty(board):
                            return True
                        board[row][col] = "."     # undo and try the next digit
                return False                      # no digit fits here: backtrack
    return True                                   # no empty cell left: solved


# --- optimal ---
def sudoku_solver(board):
    """Bitmasks of used digits per row, column, box; fill the tightest cell first. O(9^E) worst."""
    rows = [0] * 9                                # bit d is on <=> digit d is already in that row
    cols = [0] * 9
    boxes = [0] * 9
    empties = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == ".":
                empties.append((row, col))
            else:
                bit = 1 << int(board[row][col])
                rows[row] |= bit
                cols[col] |= bit
                boxes[row // 3 * 3 + col // 3] |= bit
    fill(board, rows, cols, boxes, empties)
    return board


def candidates(rows, cols, boxes, row, col):
    """Mask of digits still legal at (row, col): bits 1..9 that no row, column or box mask has."""
    used = rows[row] | cols[col] | boxes[row // 3 * 3 + col // 3]
    return ~used & 0x3FE                          # 0x3FE = bits 1..9 on, bit 0 off


def most_constrained(rows, cols, boxes, empties):
    """Index in empties of the cell with the fewest legal digits (0 options = dead branch)."""
    best = 0
    fewest = 10
    for i in range(len(empties)):
        row, col = empties[i]
        options = bin(candidates(rows, cols, boxes, row, col)).count("1")
        if options < fewest:
            fewest = options
            best = i
    return best


def fill(board, rows, cols, boxes, empties):
    if not empties:
        return True
    i = most_constrained(rows, cols, boxes, empties)
    row, col = empties.pop(i)
    box = row // 3 * 3 + col // 3
    for digit in range(1, 10):
        bit = 1 << digit
        if candidates(rows, cols, boxes, row, col) & bit == 0:
            continue
        rows[row] |= bit
        cols[col] |= bit
        boxes[box] |= bit
        board[row][col] = str(digit)
        if fill(board, rows, cols, boxes, empties):
            return True
        rows[row] ^= bit                          # undo the masks too, not just the board
        cols[col] ^= bit
        boxes[box] ^= bit
    board[row][col] = "."
    empties.insert(i, (row, col))                 # put the cell back where it was
    return False


# --- try the brute force ---
print(show(brute_force(make_board(PUZZLE))))
# -> 534678912 672195348 198342567 859761423 426853791 713924856 961537284 287419635 345286179
print(show(brute_force(make_board(SOLVED))) == " ".join(SOLVED))   # -> True (nothing to fill)


# --- try the optimal ---
print(show(sudoku_solver(make_board(PUZZLE))))
# -> 534678912 672195348 198342567 859761423 426853791 713924856 961537284 287419635 345286179
print(show(sudoku_solver(make_board(SOLVED))) == " ".join(SOLVED))   # -> True (nothing to fill)
