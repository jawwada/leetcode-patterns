"""
Valid Sudoku (LeetCode 36) - Medium
Chapter: arrays_hashing
Pattern: Hash set per row/column/box

Given a 9x9 board with digits '1'-'9' and '.' for empty cells, decide whether the
filled cells are valid: no digit repeats in any row, any column, or any of the nine
3x3 boxes. Solvability is not required.
Example: a board whose first column holds two '8's -> False.
"""


# --- helpers ---
def build_board(rows):
    """Turn 9 strings like '53..7....' into a 9x9 list of single characters."""
    board = []
    for row in rows:
        board.append(list(row))
    return board


# --- brute force ---
def brute_force(board):
    """For each filled cell, scan its row, column and box. O(81 * 27) steps, O(1) space."""
    for row in range(9):
        for col in range(9):
            digit = board[row][col]
            if digit == ".":
                continue
            for k in range(9):
                if k != col and board[row][k] == digit:  # same digit elsewhere in the row
                    return False
                if k != row and board[k][col] == digit:  # same digit elsewhere in the column
                    return False
            box_row = 3 * (row // 3)  # top-left corner of this cell's 3x3 box
            box_col = 3 * (col // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if (i != row or j != col) and board[i][j] == digit:
                        return False
    return True


# --- optimal ---
def valid_sudoku(board):
    """One set per row, column and box; one sweep. O(81) steps, O(81) space."""
    rows = []
    cols = []
    boxes = []
    for _ in range(9):
        rows.append(set())
        cols.append(set())
        boxes.append(set())
    for row in range(9):
        for col in range(9):
            digit = board[row][col]
            if digit == ".":
                continue
            box = (row // 3) * 3 + col // 3  # which of the nine 3x3 boxes, numbered 0..8
            if digit in rows[row] or digit in cols[col] or digit in boxes[box]:
                return False
            rows[row].add(digit)
            cols[col].add(digit)
            boxes[box].add(digit)
    return True


# --- try the brute force ---
valid = build_board(["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
                     "7...2...6", ".6....28.", "...419..5", "....8..79"])
bad_column = build_board(["83..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
                          "7...2...6", ".6....28.", "...419..5", "....8..79"])
bad_box = build_board(["53..7....", "6..195...", ".95....6.", "8...6...3", "4..8.3..1",
                       "7...2...6", ".6....28.", "...419..5", "....8..79"])
print(brute_force(valid))       # -> True
print(brute_force(bad_column))  # -> False  (two 8s in column 0)
print(brute_force(bad_box))     # -> False  (two 5s in the top-left box)


# --- try the optimal ---
valid = build_board(["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
                     "7...2...6", ".6....28.", "...419..5", "....8..79"])
bad_column = build_board(["83..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
                          "7...2...6", ".6....28.", "...419..5", "....8..79"])
bad_box = build_board(["53..7....", "6..195...", ".95....6.", "8...6...3", "4..8.3..1",
                       "7...2...6", ".6....28.", "...419..5", "....8..79"])
print(valid_sudoku(valid))       # -> True
print(valid_sudoku(bad_column))  # -> False  (two 8s in column 0)
print(valid_sudoku(bad_box))     # -> False  (two 5s in the top-left box)
