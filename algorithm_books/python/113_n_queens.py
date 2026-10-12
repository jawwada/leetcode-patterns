"""
N-Queens - Columns and Diagonals as Sets

Place n queens on an n x n board so that no two share a row, a column or a
diagonal, and return every such board as a list of row strings:
n = 4 -> two boards, ['.Q..', '...Q', 'Q...', '..Q.'] and its mirror image.
"""


# --- helpers ---
def draw(queens):
    """queens[r] is the column of row r's queen; spell each row. O(n^2)."""
    n = len(queens)
    board = []
    for col in queens:
        board.append("." * col + "Q" + "." * (n - 1 - col))
    return board


# --- algorithm ---
def backtrack(n, row, queens, cols, diags, anti_diags, boards):
    """Try each safe column in this row, then fill the rows below it."""
    if row == n:
        boards.append(draw(queens))     # every row holds a queen
        return
    for col in range(n):
        if col in cols or (row - col) in diags or (row + col) in anti_diags:
            continue                    # attacked: a column or a diagonal
        queens.append(col)              # place the queen
        cols.add(col)
        diags.add(row - col)
        anti_diags.add(row + col)
        backtrack(n, row + 1, queens, cols, diags, anti_diags, boards)
        queens.pop()                    # remove it, undoing all four marks
        cols.remove(col)
        diags.remove(row - col)
        anti_diags.remove(row + col)


def solve_n_queens(n):
    """One queen per row; three sets make each safety check O(1)."""
    boards = []
    backtrack(n, 0, [], set(), set(), set(), boards)
    return boards


# --- try it ---
boards = solve_n_queens(4)
print(boards[0])                    # -> ['.Q..', '...Q', 'Q...', '..Q.']
print(boards[1])                    # -> ['..Q.', 'Q...', '...Q', '.Q..']
print(len(solve_n_queens(8)))       # -> 92
print(solve_n_queens(3))            # -> []
print(solve_n_queens(1))            # -> [['Q']]
