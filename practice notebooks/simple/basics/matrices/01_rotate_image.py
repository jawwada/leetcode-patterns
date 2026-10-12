"""
Rotate Image (basics: matrices)
Rotate an n x n matrix 90 degrees clockwise, in place.
  [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  ->  [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

Idea: transposing mirrors the matrix over its main diagonal (rows become columns).
      Reversing every row then turns that mirror image into a clockwise turn.

Pseudocode:
  transpose:
      for i in 0..n-1:
          for j in i+1..n-1:             # above the diagonal only: each pair once
              swap matrix[i][j] and matrix[j][i]
  reverse every row

Time O(n^2), space O(1).
"""


def rotate_image(matrix):
    n = len(matrix)
    for i in range(n):                   # transpose
        for j in range(i + 1, n):        # j > i: swap each pair once
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:                   # then reverse every row
        row.reverse()
    return matrix


if __name__ == "__main__":
    print(rotate_image([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    print(rotate_image([[1, 2], [3, 4]]))                   # [[3, 1], [4, 2]]
    print(rotate_image([[5]]))                              # [[5]]
