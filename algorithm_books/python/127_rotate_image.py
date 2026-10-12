"""
Rotate Image - Transpose, Then Reverse Each Row

Rotate an n x n matrix by 90 degrees clockwise in place, without allocating
a second matrix:
[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]].
"""


# --- algorithm ---
def rotate(matrix):
    """Transpose, then reverse each row: the cell (r, c) lands on
    (c, n - 1 - r). O(n^2) time, O(1) extra space."""
    n = len(matrix)
    for row in range(n):                    # transpose: mirror on the diagonal
        for col in range(row + 1, n):       # above the diagonal only
            temp = matrix[row][col]
            matrix[row][col] = matrix[col][row]
            matrix[col][row] = temp
    for row in range(n):
        reverse_row(matrix[row])            # mirror left to right


def reverse_row(cells):
    """Reverse one row in place, swapping its ends inward. O(n)."""
    left = 0
    right = len(cells) - 1
    while left < right:
        cells[left], cells[right] = cells[right], cells[left]
        left += 1
        right -= 1


# --- try it ---
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate(matrix)
print(matrix)                   # -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
square = [[1, 2], [3, 4]]
rotate(square)
print(square)                   # -> [[3, 1], [4, 2]]
big = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
rotate(big)
print(big[0], big[3])           # -> [15, 13, 2, 5] [16, 7, 10, 11]
for turn in range(3):
    rotate(big)                 # three more quarter turns make a full turn
print(big[0], big[3])           # -> [5, 1, 9, 11] [15, 14, 12, 16]
