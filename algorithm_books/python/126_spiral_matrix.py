"""
Spiral Matrix - Walk the Boundary, Then Shrink It

Given an m x n matrix, return all of its elements in clockwise spiral order,
starting at the top-left corner and moving right: rows [1, 2, 3, 4],
[5, 6, 7, 8], [9, 10, 11, 12] -> [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7].
"""


# --- algorithm ---
def spiral_order(matrix):
    """Read the four sides of the outer ring, shrinking a bound after each
    side. O(m * n) time, O(1) extra space besides the output."""
    result = []
    if len(matrix) == 0:
        return result
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for col in range(left, right + 1):          # top row, left to right
            result.append(matrix[top][col])
        top += 1
        for row in range(top, bottom + 1):          # right column, downward
            result.append(matrix[row][right])
        right -= 1
        if top <= bottom:                           # a bottom row is unread
            for col in range(right, left - 1, -1):  # bottom row, leftward
                result.append(matrix[bottom][col])
            bottom -= 1
        if left <= right:                           # a left column is unread
            for row in range(bottom, top - 1, -1):  # left column, upward
                result.append(matrix[row][left])
            left += 1
    return result


# --- try it ---
matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(spiral_order(matrix))     # -> [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
square = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(spiral_order(square))     # -> [1, 2, 3, 6, 9, 8, 7, 4, 5]
print(spiral_order([[1, 2, 3]]))            # -> [1, 2, 3]
print(spiral_order([[1], [2], [3]]))        # -> [1, 2, 3]
print(spiral_order([]))                     # -> []
