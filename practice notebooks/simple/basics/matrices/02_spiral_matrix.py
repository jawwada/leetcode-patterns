"""
Spiral Matrix (basics: matrices)
Return every element of an m x n matrix in clockwise spiral order.
  [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  ->  [1, 2, 3, 6, 9, 8, 7, 4, 5]

Idea: keep four walls (top, bottom, left, right); walk one side, then move that wall in.
      After the top row and the right column a row or column may be used up, so check
      again before walking the bottom row and the left column.

Pseudocode:
  top, bottom, left, right = 0, m-1, 0, n-1
  while top <= bottom and left <= right:
      top row, left -> right;          top += 1
      right column, top -> bottom;     right -= 1
      if top <= bottom: bottom row, right -> left;   bottom -= 1
      if left <= right: left column, bottom -> top;  left += 1

Time O(m*n), space O(1) besides the output.
"""


def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):           # top row, left -> right
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):           # right column, going down
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:                          # a row remains
            for c in range(right, left - 1, -1):   # bottom row, right -> left
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                          # a column remains
            for r in range(bottom, top - 1, -1):   # left column, going up
                out.append(matrix[r][left])
            left += 1
    return out


if __name__ == "__main__":
    print(spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # [1, 2, 3, 6, 9, 8, 7, 4, 5]
    print(spiral_order([[1, 2, 3], [4, 5, 6]]))             # [1, 2, 3, 6, 5, 4]
    print(spiral_order([[1], [2], [3]]))                    # [1, 2, 3]
