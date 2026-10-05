"""
Set Matrix Zeroes (LeetCode 73) - Medium
Chapter: math_geometry
Pattern: In-place markers (reuse first row/column as flags)

Given an m x n matrix, if a cell is 0, set its entire row and column to 0, in place.
Follow-up: use O(1) extra space.
Example: [[1, 1, 1], [1, 0, 1], [1, 1, 1]] -> [[1, 0, 1], [0, 0, 0], [1, 0, 1]].
"""


# --- brute force ---
def brute_force(matrix):
    """Snapshot the matrix; for each original zero, clear its row and column. O(m*n*(m+n)) time."""
    rows = len(matrix)
    cols = len(matrix[0])
    snapshot = []
    for row in matrix:
        snapshot.append(row[:])              # a copy, so new zeros are not mistaken for old ones
    for r in range(rows):
        for c in range(cols):
            if snapshot[r][c] == 0:
                for k in range(cols):
                    matrix[r][k] = 0
                for k in range(rows):
                    matrix[k][c] = 0


# --- optimal ---
def set_matrix_zeroes(matrix):
    """Use row 0 and column 0 of the matrix itself as the flags. O(m*n) time, O(1) extra space."""
    rows = len(matrix)
    cols = len(matrix[0])
    first_col_zero = False                   # column 0 needs its own flag: cell (0, 0) is taken
    for r in range(rows):
        if matrix[r][0] == 0:
            first_col_zero = True
    for r in range(rows):                    # mark: matrix[r][0] flags row r, matrix[0][c] col c
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
    for r in range(1, rows):                 # apply the flags to everything but row 0 / column 0
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if matrix[0][0] == 0:                    # cell (0, 0) carries the flag for row 0
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0


# --- try the brute force ---
m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
brute_force(m)
print(m)   # -> [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
brute_force(m)
print(m)   # -> [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
m = [[1], [0], [3]]
brute_force(m)
print(m)   # -> [[0], [0], [0]]
m = [[1, 1], [0, 1]]
brute_force(m)
print(m)   # -> [[0, 1], [0, 0]]


# --- try the optimal ---
m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
set_matrix_zeroes(m)
print(m)   # -> [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
set_matrix_zeroes(m)
print(m)   # -> [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
m = [[1], [0], [3]]
set_matrix_zeroes(m)
print(m)   # -> [[0], [0], [0]]
m = [[1, 1], [0, 1]]
set_matrix_zeroes(m)
print(m)   # -> [[0, 1], [0, 0]]
