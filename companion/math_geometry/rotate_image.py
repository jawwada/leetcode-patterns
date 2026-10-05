"""
Rotate Image (LeetCode 48) - Medium
Chapter: math_geometry
Pattern: Transpose + reverse rows (in-place matrix rotation)

Rotate an n x n matrix by 90 degrees clockwise in place, without allocating a second matrix.
Example: [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]].
"""


# --- brute force ---
def brute_force(matrix):
    """Copy each cell to its rotated spot in a new matrix, then copy back. O(n^2) time, space."""
    n = len(matrix)
    rotated = []
    for r in range(n):
        rotated.append([0] * n)
    for r in range(n):
        for c in range(n):
            rotated[c][n - 1 - r] = matrix[r][c]   # row r of the input becomes column n-1-r
    for r in range(n):
        matrix[r] = rotated[r]


# --- optimal ---
def rotate_image(matrix):
    """Transpose across the diagonal, then reverse each row. O(n^2) time, O(1) extra space."""
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):            # only above the diagonal, or every swap is undone
            temp = matrix[r][c]
            matrix[r][c] = matrix[c][r]
            matrix[c][r] = temp
    for row in matrix:
        row.reverse()                        # mirror left <-> right: transpose + flip = rotation


# --- try the brute force ---
m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
brute_force(m)
print(m)   # -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
brute_force(m)
print(m)   # -> [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
m = [[1, 2], [3, 4]]
brute_force(m)
print(m)   # -> [[3, 1], [4, 2]]


# --- try the optimal ---
m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate_image(m)
print(m)   # -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
rotate_image(m)
print(m)   # -> [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
m = [[1, 2], [3, 4]]
rotate_image(m)
print(m)   # -> [[3, 1], [4, 2]]
