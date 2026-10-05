"""
Word Search (LeetCode 79) - Medium
Chapter: backtracking
Pattern: Grid DFS backtracking with in-place visited marking

Given an m x n grid of letters and a word, return True if the word can be traced through
horizontally or vertically adjacent cells, using each cell at most once.
Example: board=[[A,B,C,E],[S,F,C,S],[A,D,E,E]], word="ABCCED" -> True;
word="ABCB" -> False because the B would be reused.
"""


# --- brute force ---
def brute_force(board, word):
    """From every cell list every self-avoiding path of len(word) cells; compare at the end."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if paths(board, word, row, col, [(row, col)], board[row][col]):
                return True
    return False


def paths(board, word, row, col, visited, letters):
    # visited = cells on the path so far, letters = the string they spell
    if len(letters) == len(word):
        return letters == word                       # compared only once the path is complete
    for step_row, step_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        next_row = row + step_row
        next_col = col + step_col
        if next_row < 0 or next_row >= len(board) or next_col < 0 or next_col >= len(board[0]):
            continue
        if (next_row, next_col) in visited:
            continue                                 # each cell at most once
        new_visited = visited + [(next_row, next_col)]
        new_letters = letters + board[next_row][next_col]
        if paths(board, word, next_row, next_col, new_visited, new_letters):
            return True
    return False


# --- optimal ---
def exist(board, word):
    """DFS from every cell, matching word[k] at step k; visited marked in place. O(m*n*4^L)."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if dfs(board, word, row, col, 0):
                return True
    return False


def dfs(board, word, row, col, k):
    if k == len(word):
        return True                                  # every letter matched
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return False
    if board[row][col] != word[k]:
        return False                                 # mismatch (or cell in use): prune right now
    saved = board[row][col]
    board[row][col] = "#"                            # mark visited in place
    found = False
    for step_row, step_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if dfs(board, word, row + step_row, col + step_col, k + 1):
            found = True
            break
    board[row][col] = saved                          # un-mark on the way back
    return found


# --- try the brute force ---
grid = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
print(brute_force(grid, "ABCCED"))   # -> True
print(brute_force(grid, "SEE"))      # -> True
print(brute_force(grid, "ABCB"))     # -> False
print(brute_force([["a"]], "ab"))    # -> False


# --- try the optimal ---
grid = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
print(exist(grid, "ABCCED"))   # -> True
print(exist(grid, "SEE"))      # -> True
print(exist(grid, "ABCB"))     # -> False
print(exist([["a"]], "ab"))    # -> False
