"""
N-Queens (LeetCode 51) - Hard
Chapter: backtracking
Pattern: Row-by-row backtracking with column/diagonal sets

Place n queens on an n x n board so that no two attack each other (same row, column or
diagonal). Return every distinct board as a list of strings, Q for a queen and . for empty.
Example: n=4 -> [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]; n=1 -> [["Q"]].
"""
from itertools import permutations   # every ordering of a list


# --- helpers ---
def draw_board(columns):
    """columns[row] = the column of that row's queen -> the board as a list of strings."""
    rows = []
    for col in columns:
        rows.append("." * col + "Q" + "." * (len(columns) - col - 1))
    return rows


# --- brute force ---
def brute_force(n):
    """One queen per row: try each column permutation, keep diagonal-free boards. O(n! n^2)."""
    boards = []
    for columns in permutations(range(n)):        # n! placements, checked only when complete
        if no_diagonal_attack(columns):
            boards.append(draw_board(columns))
    return boards


def no_diagonal_attack(columns):
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            if abs(columns[i] - columns[j]) == j - i:   # same diagonal
                return False
    return True


# --- optimal ---
def n_queens(n):
    """Place queens row by row; three sets say which columns and diagonals are taken. O(n!)."""
    result = []
    place(n, 0, [], set(), set(), set(), result)
    return result


def place(n, row, queens, cols, diag, anti, result):
    if row == n:
        result.append(draw_board(queens))
        return
    for col in range(n):
        if col in cols or row - col in diag or row + col in anti:
            continue                              # under attack: skip this whole subtree
        cols.add(col)
        diag.add(row - col)                       # "\" diagonal: row - col is constant
        anti.add(row + col)                       # "/" diagonal: row + col is constant
        queens.append(col)
        place(n, row + 1, queens, cols, diag, anti, result)
        queens.pop()                              # undo everything before trying the next column
        cols.remove(col)
        diag.remove(row - col)
        anti.remove(row + col)


# --- try the brute force ---
# any order is accepted, so the demos print the boards sorted
print(sorted(brute_force(4)))
# -> [['..Q.', 'Q...', '...Q', '.Q..'], ['.Q..', '...Q', 'Q...', '..Q.']]
print(brute_force(1))           # -> [['Q']]
print(brute_force(3))           # -> []
print(len(brute_force(6)))      # -> 4


# --- try the optimal ---
# any order is accepted, so the demos print the boards sorted
print(sorted(n_queens(4)))
# -> [['..Q.', 'Q...', '...Q', '.Q..'], ['.Q..', '...Q', 'Q...', '..Q.']]
print(n_queens(1))              # -> [['Q']]
print(n_queens(3))              # -> []
print(len(n_queens(6)))         # -> 4
