"""
Search a 2D Matrix II - Fundamentals
Chapter: fundamentals/matrices
Key operations: start at the top-right corner, move left when too big, move down when too small

Every row is sorted left to right and every column top to bottom. Return whether target is present.
From the top-right corner a value larger than target rules out its whole column (cells below are
bigger), a smaller one rules out its whole row (everything to the left is smaller).
Example: [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], 5 -> True
"""


# --- algorithm ---
def search_matrix(matrix, target):
    """Staircase from top-right: too big -> left (drop column), too small -> down (drop row)."""
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return False
    rows = len(matrix)
    cols = len(matrix[0])
    row = 0
    col = cols - 1                # top-right: the corner where one compare rules out a whole line
    while row < rows and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1              # everything below is bigger: drop this column
        else:
            row += 1              # everything to the left is smaller: drop this row
    return False


# --- try it ---
grid = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]]
print(search_matrix(grid, 5))        # -> True
print(search_matrix(grid, 20))       # -> False
print(search_matrix(grid, 18))       # -> True
print(search_matrix([[1]], 2))       # -> False
