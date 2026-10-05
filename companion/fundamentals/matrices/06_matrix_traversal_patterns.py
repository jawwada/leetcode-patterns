"""
Matrix Traversal Patterns - Fundamentals
Chapter: fundamentals/matrices
Key operations: row-major and column-major walks, anti-diagonals by r + c, 4/8 direction vectors

An m x n matrix can be walked row by row, column by column, or along anti-diagonals: the cells with
the same row + col form one anti-diagonal, and there are m + n - 1 of them. The direction vectors
DIRS4 / DIRS8 plus a bounds check give the neighbors of a cell, the first step of any grid BFS/DFS.
Example: anti_diagonals([[1,2,3],[4,5,6],[7,8,9]]) -> [1, 2, 4, 3, 5, 7, 6, 8, 9]
"""


# --- algorithm ---
DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]                 # up, down, left, right
DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]       # plus the four diagonals


def row_major(matrix):
    """Row by row, left to right. O(m*n)."""
    out = []
    for row in matrix:
        for value in row:
            out.append(value)
    return out


def col_major(matrix):
    """Column by column, top to bottom. O(m*n)."""
    out = []
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            out.append(matrix[row][col])
    return out


def neighbors(matrix, row, col, dirs):
    """In-bounds neighbor coordinates of (row, col) along the given direction vectors. O(1)."""
    rows = len(matrix)
    cols = len(matrix[0])
    out = []
    for dr, dc in dirs:
        nr = row + dr
        nc = col + dc
        if 0 <= nr < rows and 0 <= nc < cols:     # strict upper bound: valid rows are 0..m-1
            out.append((nr, nc))
    return out


def anti_diagonals(matrix):
    """Diagonal d holds the cells with row + col == d, read top-right to bottom-left. O(m*n)."""
    rows = len(matrix)
    cols = len(matrix[0])
    out = []
    for d in range(rows + cols - 1):              # m + n - 1 diagonals: row + col runs 0..m+n-2
        first_row = max(0, d - cols + 1)
        last_row = min(rows - 1, d)
        for row in range(first_row, last_row + 1):    # + 1: range excludes its end
            out.append(matrix[row][d - row])
    return out


# --- try it ---
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(row_major(grid))                  # -> [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(col_major(grid))                  # -> [1, 4, 7, 2, 5, 8, 3, 6, 9]
print(anti_diagonals(grid))             # -> [1, 2, 4, 3, 5, 7, 6, 8, 9]
print(anti_diagonals([[1, 2, 3, 4], [5, 6, 7, 8]]))   # -> [1, 2, 5, 3, 6, 4, 7, 8]
print(neighbors(grid, 0, 0, DIRS4))     # -> [(1, 0), (0, 1)]
print(neighbors(grid, 2, 2, DIRS8))     # -> [(1, 2), (2, 1), (1, 1)]
