"""
Search a 2D Matrix II (basics: matrices)
Every row is sorted left to right and every column top to bottom. Is target in the matrix?
  [[1, 4, 7], [2, 5, 8], [3, 6, 9]], target = 5  ->  True

Idea: start at the top-right corner. A value bigger than target rules out its whole column
      (everything below is bigger); a smaller one rules out its whole row (everything to
      the left is smaller). Each step drops a row or a column: a staircase walk.

Pseudocode:
  r, c = 0, n - 1                         # top-right corner
  while r < m and c >= 0:
      if matrix[r][c] == target: return True
      if matrix[r][c] > target: c -= 1    # drop the column
      else: r += 1                        # drop the row
  return False

Time O(m + n), space O(1).
"""


def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    m, n = len(matrix), len(matrix[0])
    r, c = 0, n - 1                      # top-right corner
    while r < m and c >= 0:
        x = matrix[r][c]
        if x == target:
            return True
        if x > target:
            c -= 1                       # too big: drop this column
        else:
            r += 1                       # too small: drop this row
    return False


if __name__ == "__main__":
    grid = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22],
            [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
    print(search_matrix(grid, 5))    # True
    print(search_matrix(grid, 20))   # False
    print(search_matrix(grid, 18))   # True
