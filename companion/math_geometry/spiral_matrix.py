"""
Spiral Matrix (LeetCode 54) - Medium
Chapter: math_geometry
Pattern: Shrinking boundary traversal

Given an m x n matrix, return all its elements in clockwise spiral order, starting at the
top-left corner and moving right.
Example: [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [1, 2, 3, 6, 9, 8, 7, 4, 5].
"""


# --- brute force ---
def brute_force(matrix):
    """Walk cell by cell with a visited grid; turn right when blocked. O(m*n) time and space."""
    rows = len(matrix)
    cols = len(matrix[0])
    visited = []
    for r in range(rows):
        visited.append([False] * cols)
    row_step = [0, 1, 0, -1]                 # the four directions: right, down, left, up
    col_step = [1, 0, -1, 0]
    r = 0
    c = 0
    direction = 0
    result = []
    for step in range(rows * cols):
        result.append(matrix[r][c])
        visited[r][c] = True
        next_r = r + row_step[direction]
        next_c = c + col_step[direction]
        in_grid = 0 <= next_r < rows and 0 <= next_c < cols
        if not in_grid or visited[next_r][next_c]:   # blocked: turn clockwise
            direction = (direction + 1) % 4
            next_r = r + row_step[direction]
            next_c = c + col_step[direction]
        r = next_r
        c = next_c
    return result


# --- optimal ---
def spiral_matrix(matrix):
    """Peel one layer at a time using four shrinking bounds. O(m*n) time, O(1) extra space."""
    result = []
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):     # top row, left to right
            result.append(matrix[top][c])
        top = top + 1
        for r in range(top, bottom + 1):     # right column, top to bottom
            result.append(matrix[r][right])
        right = right - 1
        if top <= bottom:                    # a row is still left (else the top row repeats)
            for c in range(right, left - 1, -1):   # bottom row, right to left
                result.append(matrix[bottom][c])
            bottom = bottom - 1
        if left <= right:                    # a column is still left
            for r in range(bottom, top - 1, -1):   # left column, bottom to top
                result.append(matrix[r][left])
            left = left + 1
    return result


# --- try the brute force ---
print(brute_force([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))         # -> [1, 2, 3, 6, 9, 8, 7, 4, 5]
print(brute_force([[1, 2, 3, 4], [5, 6, 7, 8]]))              # -> [1, 2, 3, 4, 8, 7, 6, 5]
print(brute_force([[1], [2], [3]]))                           # -> [1, 2, 3]
print(brute_force([[1, 2], [3, 4], [5, 6], [7, 8]]))          # -> [1, 2, 4, 6, 8, 7, 5, 3]


# --- try the optimal ---
print(spiral_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))       # -> [1, 2, 3, 6, 9, 8, 7, 4, 5]
print(spiral_matrix([[1, 2, 3, 4], [5, 6, 7, 8]]))            # -> [1, 2, 3, 4, 8, 7, 6, 5]
print(spiral_matrix([[1], [2], [3]]))                         # -> [1, 2, 3]
print(spiral_matrix([[1, 2], [3, 4], [5, 6], [7, 8]]))        # -> [1, 2, 4, 6, 8, 7, 5, 3]
