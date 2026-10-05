"""
Range Sum Query 2D - Mutable (LeetCode 308) - Hard
Chapter: design
Pattern: 2D Fenwick tree (binary indexed tree) + inclusion-exclusion

Design NumMatrix(matrix) with update(row, col, val), which sets one cell, and
sumRegion(row1, col1, row2, col2), which returns the sum of that inclusive rectangle. Updates and
queries are interleaved, many of each.
Example: matrix [[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]:
sumRegion(2,1,4,3) -> 8; update(3,2,2); sumRegion(2,1,4,3) -> 10.
"""


# --- helpers ---
def copy_matrix(matrix):
    rows = []
    for row in matrix:
        rows.append(row[:])
    return rows


# --- brute force ---
class BruteForce:
    """Plain matrix: update writes one cell, sumRegion adds up the rectangle. O(m*n) per query."""

    def __init__(self, matrix):
        self.cells = copy_matrix(matrix)

    def update(self, row, col, val):
        self.cells[row][col] = val

    def sumRegion(self, row1, col1, row2, col2):
        total = 0
        for r in range(row1, row2 + 1):       # every cell, every query
            for c in range(col1, col2 + 1):
                total += self.cells[r][c]
        return total


# --- optimal ---
def lowest_bit(x):
    """The value of the lowest set bit of x: 12 = 0b1100 -> 4. It is the block size at index x."""
    return x & -x


class NumMatrix:
    """2D Fenwick tree: a point update and a prefix sum each touch O(log m * log n) nodes."""

    def __init__(self, matrix):
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.vals = copy_matrix(matrix)       # current cell values, to turn "set" into "add delta"
        self.tree = []                        # 1-indexed: tree[i][j] sums a block ending at (i, j)
        for i in range(self.m + 1):
            self.tree.append([0] * (self.n + 1))
        for r in range(self.m):
            for c in range(self.n):
                self.add(r, c, matrix[r][c])

    def add(self, r, c, delta):
        i = r + 1
        while i <= self.m:
            j = c + 1
            while j <= self.n:
                self.tree[i][j] += delta
                j += lowest_bit(j)            # next node whose column block covers j
            i += lowest_bit(i)                # next node whose row block covers i

    def prefix(self, r, c):
        """Sum of the first r rows x first c columns (0-indexed cells [0, r) x [0, c))."""
        total = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                total += self.tree[i][j]
                j -= lowest_bit(j)            # jump to the block just before this one
            i -= lowest_bit(i)
        return total

    def update(self, row, col, val):
        self.add(row, col, val - self.vals[row][col])   # Fenwick wants a delta, not a value
        self.vals[row][col] = val

    def sumRegion(self, row1, col1, row2, col2):
        whole = self.prefix(row2 + 1, col2 + 1)
        above = self.prefix(row1, col2 + 1)
        left = self.prefix(row2 + 1, col1)
        corner = self.prefix(row1, col1)      # removed twice, so add it back once
        return whole - above - left + corner


# --- try the brute force ---
grid = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
nm = BruteForce(grid)
print(nm.sumRegion(2, 1, 4, 3))   # -> 8
nm.update(3, 2, 2)
print(nm.sumRegion(2, 1, 4, 3))   # -> 10
print(nm.sumRegion(0, 0, 4, 4))   # -> 60
one = BruteForce([[5]])
one.update(0, 0, -3)
print(one.sumRegion(0, 0, 0, 0))  # -> -3


# --- try the optimal ---
grid = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
nm = NumMatrix(grid)
print(nm.sumRegion(2, 1, 4, 3))   # -> 8
nm.update(3, 2, 2)
print(nm.sumRegion(2, 1, 4, 3))   # -> 10
print(nm.sumRegion(0, 0, 4, 4))   # -> 60
one = NumMatrix([[5]])
one.update(0, 0, -3)
print(one.sumRegion(0, 0, 0, 0))  # -> -3
