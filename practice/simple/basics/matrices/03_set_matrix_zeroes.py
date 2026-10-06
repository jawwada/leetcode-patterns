"""
Set Matrix Zeroes (basics: matrices)
If a cell is 0, set its whole row and column to 0, in place, with O(1) extra space.
  [[1, 1, 1], [1, 0, 1], [1, 1, 1]]  ->  [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

Idea: use the first row and the first column as markers ("zero this column / row").
      Marking overwrites them, so first remember in two flags whether they hold a 0
      themselves, and zero them last.

Pseudocode:
  row0 = first row has a 0;  col0 = first column has a 0
  for each inner cell (r >= 1, c >= 1) that is 0:
      matrix[r][0] = 0;  matrix[0][c] = 0          # mark its row and its column
  for each inner cell: if matrix[r][0] == 0 or matrix[0][c] == 0: set it to 0
  if row0: zero the first row
  if col0: zero the first column

Time O(m*n), space O(1).
"""


def set_matrix_zeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    row0 = any(x == 0 for x in matrix[0])               # remember before marking
    col0 = any(matrix[r][0] == 0 for r in range(m))
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = 0                        # mark the row
                matrix[0][c] = 0                        # mark the column
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:  # row or column marked
                matrix[r][c] = 0
    if row0:                                            # borders last
        for c in range(n):
            matrix[0][c] = 0
    if col0:
        for r in range(m):
            matrix[r][0] = 0
    return matrix


if __name__ == "__main__":
    print(set_matrix_zeroes([[1, 1, 1], [1, 0, 1], [1, 1, 1]]))  # [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    print(set_matrix_zeroes([[0, 1, 2], [3, 4, 5]]))             # [[0, 0, 0], [0, 4, 5]]
    print(set_matrix_zeroes([[1, 0, 1], [1, 1, 1]]))             # [[0, 0, 0], [1, 0, 1]]
