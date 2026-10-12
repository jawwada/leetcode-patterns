"""
Search a 2D Matrix - Staircase from the Top-Right Corner

Given a matrix whose rows are sorted left to right and whose columns are
sorted top to bottom, report whether a target is present:
[[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22],
 [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], target 5 -> True.
"""


# --- algorithm ---
def staircase_search(matrix, target):
    """Rows and columns sorted: start at the top-right corner; each step
    rules out a whole row or column. O(m + n) time, O(1) space."""
    if len(matrix) == 0:
        return False
    row = 0
    col = len(matrix[0]) - 1        # top-right: row's max, column's min
    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1                # the rest of this column is bigger still
        else:
            row += 1                # the rest of this row is smaller still
    return False


def flattened_search(matrix, target):
    """Each row starts above the previous row's end: one lower-bound search
    over the flat positions 0 .. m*n - 1. O(log(m n)) time, O(1) space."""
    if len(matrix) == 0:
        return False
    cols = len(matrix[0])
    lo = 0
    hi = len(matrix) * cols         # half-open [lo, hi) of flat positions
    while lo < hi:
        mid = (lo + hi) // 2
        value = matrix[mid // cols][mid % cols]     # fold into a cell
        if value < target:
            lo = mid + 1
        else:
            hi = mid
    if lo == len(matrix) * cols:
        return False                # every value is smaller than the target
    return matrix[lo // cols][lo % cols] == target


# --- try it ---
grid = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
print(staircase_search(grid, 5))            # -> True
print(staircase_search(grid, 20))           # -> False
rows = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
print(flattened_search(rows, 3))            # -> True
print(flattened_search(rows, 13))           # -> False
print(flattened_search(rows, 61))           # -> False
