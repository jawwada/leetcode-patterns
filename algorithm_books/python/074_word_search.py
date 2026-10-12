"""
Word Search - Grid Backtracking with In-Place Marks

Given a grid of letters and a word, decide whether the word can be spelled by
a path of horizontally or vertically adjacent cells, each used at most once:
grid ABCE / SFCS / ADEE, word "ABCCED" -> True.
"""


# --- algorithm ---
def dfs(board, word, row, col, k):
    """Can word[k:] be spelled from cell (row, col) on? Marks its own path."""
    if k == len(word):
        return True                     # every letter matched
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return False                    # off the grid
    if board[row][col] != word[k]:
        return False                    # wrong letter, or a '#' on the path
    board[row][col] = "#"               # mark: this cell is on the path
    found = False
    for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if dfs(board, word, row + d_row, col + d_col, k + 1):
            found = True
            break
    board[row][col] = word[k]           # unmark on the way back
    return found


def exist(board, word):
    """Try every cell as the first letter. O(m * n * 3^L) worst case."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if dfs(board, word, row, col, 0):
                return True
    return False


# --- try it ---
board = [list("ABCE"), list("SFCS"), list("ADEE")]   # rows of letters
print(exist(board, "ABCCED"))   # -> True
print(exist(board, "SEE"))      # -> True
print(exist(board, "ABCB"))     # -> False
print(board[0])                 # -> ['A', 'B', 'C', 'E']
