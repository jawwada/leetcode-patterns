"""
Matrix Traversal Patterns (basics: matrices)
Walk an m x n matrix by rows, by columns and by anti-diagonals, and list a cell's neighbors.
  [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  ->  anti-diagonals [1, 2, 4, 3, 5, 7, 6, 8, 9]

Idea: the cells with the same r + c form one anti-diagonal; d = r + c runs 0..m+n-2.
      A neighbor is the cell plus a direction vector, kept only if it lands inside.

Pseudocode:
  row_major:  for r: for c: take matrix[r][c]
  col_major:  for c: for r: take matrix[r][c]
  neighbors(r, c, dirs):
      for (dr, dc) in dirs:
          nr, nc = r + dr, c + dc
          keep (nr, nc) if 0 <= nr < m and 0 <= nc < n
  anti_diagonals:
      for d in 0..m+n-2:
          for r in max(0, d-n+1)..min(m-1, d):    # keeps c = d - r inside
              take matrix[r][d - r]                # top-right to bottom-left

Time O(m*n) per walk, O(1) per neighbors call; space O(1) besides the output.
"""

DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]              # up, down, left, right
DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]    # plus the 4 diagonals


def row_major(matrix):
    return [x for row in matrix for x in row]           # row by row


def col_major(matrix):
    m, n = len(matrix), len(matrix[0])
    return [matrix[r][c] for c in range(n) for r in range(m)]   # column by column


def neighbors(matrix, r, c, dirs=DIRS4):
    m, n = len(matrix), len(matrix[0])
    out = []
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n:                 # keep only cells inside
            out.append((nr, nc))
    return out


def anti_diagonals(matrix):
    m, n = len(matrix), len(matrix[0])
    out = []
    for d in range(m + n - 1):                          # d = r + c
        for r in range(max(0, d - n + 1), min(m - 1, d) + 1):   # c = d - r stays inside
            out.append(matrix[r][d - r])
    return out


if __name__ == "__main__":
    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(row_major(grid))               # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(col_major(grid))               # [1, 4, 7, 2, 5, 8, 3, 6, 9]
    print(anti_diagonals(grid))          # [1, 2, 4, 3, 5, 7, 6, 8, 9]
    print(neighbors(grid, 0, 0, DIRS8))  # [(1, 0), (0, 1), (1, 1)]
