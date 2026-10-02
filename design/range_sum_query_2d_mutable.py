"""
Range Sum Query 2D - Mutable (LeetCode 308)  — Hard
Pattern: 2D Fenwick tree (binary indexed tree) + inclusion-exclusion

Problem
-------
Design NumMatrix(matrix) with update(row, col, val) that sets one cell and
sumRegion(row1, col1, row2, col2) that returns the sum of the inclusive rectangle. Updates and
queries are interleaved, many of each.
Example: matrix [[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]];
sumRegion(2,1,4,3) -> 8; update(3,2,2); sumRegion(2,1,4,3) -> 10.

Brute force
-----------
Store the matrix. update writes one cell in O(1); sumRegion loops over every cell of the
rectangle: O(m*n) per query, O(m*n) space. The wasted work is re-adding cells that were already
added by earlier queries over overlapping rectangles; nothing from a previous sum is reused. (A
2D prefix-sum table makes queries O(1) but every update rebuilds O(m*n) of the table, which is
the same waste moved to the other operation.)

From brute force to optimal
---------------------------
The redundancy is recomputing full sums when either a query or an update touches many cells.
The observation from 1D: a Fenwick tree stores partial sums over blocks whose size is the lowest
set bit of the index, so both a point update and a prefix sum touch only O(log n) blocks, and the
same trick applies independently along each axis. Node tree[i][j] stores the sum of the block
rows (i - lowbit(i), i] x cols (j - lowbit(j), j]. A point update walks i += i & -i and, for each
i, walks j += j & -j: O(log m * log n) nodes. A prefix sum P(r, c) walks downward the same way.
The rectangle sum is inclusion-exclusion of four prefix rectangles. Keep a plain copy of the
matrix so update can turn "set to val" into "add val - old", the delta a Fenwick tree needs.

Intuition
---------
A Fenwick tree is a set of nested blocks arranged so that any prefix decomposes into O(log n)
blocks (one per set bit of the length) and any point lies in O(log n) blocks. Doing this along
rows and columns at once gives a grid of blocks where a point is in O(log m log n) of them and a
prefix rectangle is the union of O(log m log n) of them. Updates and queries meet in the middle
instead of one of them being linear.

Geometric view
--------------
Picture the matrix padded to 1-indexed coordinates; node (i, j) is a rectangle whose bottom-right
corner is (i, j) and whose height and width are the lowest set bits of i and j. A point update
lights up a staircase of ever-larger rectangles going down-right; a prefix query collects a
staircase going up-left. sumRegion is the usual picture: big prefix rectangle minus the strip
above, minus the strip to the left, plus the corner removed twice.

Steps
-----
1. Keep vals (copy of the matrix) and tree of size (m+1) x (n+1), 1-indexed.
2. _add(r, c, delta): for i from r+1 stepping i += i & -i while i <= m, and for j from c+1
   stepping j += j & -j while j <= n: tree[i][j] += delta.
3. _prefix(r, c): the same walks downward (i -= i & -i, j -= j & -j), summing tree[i][j]; this
   is the sum of the top-left r x c rectangle.
4. update: _add(row, col, val - vals[row][col]); store val.
5. sumRegion: P(r2+1, c2+1) - P(r1, c2+1) - P(r2+1, c1) + P(r1, c1).

Complexity: O(log m * log n) per update and query, O(m*n) space — each walk touches one node per
            set bit along each axis; build is O(m*n log m log n) by repeated _add.
Pitfalls: off-by-one between 0-indexed cells and 1-indexed tree; forgetting the delta (adding val
          instead of val - old); inclusion-exclusion with r1 instead of r1 - 1 in 1-indexed terms.
"""
import random
from typing import List


class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        self.m, self.n = len(matrix), len(matrix[0])
        self.vals = [row[:] for row in matrix]                      # current cell values
        self.tree = [[0] * (self.n + 1) for _ in range(self.m + 1)]  # 1-indexed 2D BIT
        for r in range(self.m):
            for c in range(self.n):
                self._add(r, c, matrix[r][c])

    def _add(self, r: int, c: int, delta: int) -> None:
        i = r + 1
        while i <= self.m:
            j = c + 1
            while j <= self.n:
                self.tree[i][j] += delta
                j += j & -j                       # next node whose column block covers j
            i += i & -i

    def _prefix(self, r: int, c: int) -> int:     # sum of the first r rows x first c cols
        total, i = 0, r
        while i > 0:
            j = c
            while j > 0:
                total += self.tree[i][j]
                j -= j & -j
            i -= i & -i
        return total

    def update(self, row: int, col: int, val: int) -> None:
        self._add(row, col, val - self.vals[row][col])             # Fenwick wants a delta
        self.vals[row][col] = val

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        p = self._prefix
        return (p(row2 + 1, col2 + 1) - p(row1, col2 + 1)
                - p(row2 + 1, col1) + p(row1, col1))


class BruteForce:
    """Plain matrix: update is O(1), sumRegion loops over the whole rectangle."""

    def __init__(self, matrix: List[List[int]]):
        self.a = [row[:] for row in matrix]

    def update(self, row: int, col: int, val: int) -> None:
        self.a[row][col] = val

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return sum(self.a[r][c] for r in range(row1, row2 + 1) for c in range(col1, col2 + 1))


if __name__ == "__main__":
    nm = NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    assert nm.sumRegion(2, 1, 4, 3) == 8
    nm.update(3, 2, 2)
    assert nm.sumRegion(2, 1, 4, 3) == 10
    assert nm.sumRegion(0, 0, 4, 4) == 60                          # whole matrix after update
    one = NumMatrix([[5]])                                          # 1x1 edge case
    one.update(0, 0, -3)
    assert one.sumRegion(0, 0, 0, 0) == -3

    random.seed(8)
    for _ in range(30):
        m, n = random.randint(1, 7), random.randint(1, 7)
        mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
        fast, slow = NumMatrix(mat), BruteForce(mat)
        for _ in range(100):
            if random.random() < 0.4:
                r, c, v = random.randrange(m), random.randrange(n), random.randint(-9, 9)
                fast.update(r, c, v)
                slow.update(r, c, v)
            else:
                r1, r2 = sorted(random.choices(range(m), k=2))
                c1, c2 = sorted(random.choices(range(n), k=2))
                assert fast.sumRegion(r1, c1, r2, c2) == slow.sumRegion(r1, c1, r2, c2)
    print("ok")
