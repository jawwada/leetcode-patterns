"""
Search a 2D Matrix (LeetCode 74) - Medium
Chapter: binary_search
Pattern: Binary search on a sorted array

An m x n matrix has every row sorted ascending, and the first element of each row is greater
than the last element of the previous row. Return True if target is in the matrix.
Example: matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 3 -> True
"""


# --- brute force ---
def brute_force(matrix, target):
    """Look at every cell. O(m * n) time, O(1) space."""
    for row in matrix:
        for value in row:
            if value == target:
                return True
    return False


# --- optimal ---
def search_2d_matrix(matrix, target):
    """Binary search the rows laid end to end as one sorted list. O(log(m * n)) time, O(1)."""
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return False
    rows = len(matrix)
    cols = len(matrix[0])
    left = 0
    right = rows * cols - 1            # positions in the imaginary flat list
    while left <= right:
        mid = (left + right) // 2
        row = mid // cols              # fold the flat position back into the grid
        col = mid % cols
        value = matrix[row][col]
        if value == target:
            return True
        if value < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


# --- try the brute force ---
print(brute_force([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3))    # -> True
print(brute_force([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13))   # -> False
print(brute_force([[1]], 1))                                                 # -> True
print(brute_force([[1, 3]], 2))                                              # -> False


# --- try the optimal ---
print(search_2d_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3))    # -> True
print(search_2d_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13))   # -> False
print(search_2d_matrix([[1]], 1))                                                 # -> True
print(search_2d_matrix([[1, 3]], 2))                                              # -> False
