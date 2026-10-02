"""
Set Matrix Zeroes (LeetCode 73)  — Medium
Pattern: In-place markers (reuse first row/column as flags)

Problem
-------
Given an m x n matrix, if a cell is 0, set its entire row and column to 0. Do it in
place. Follow-up: O(1) extra space.
Example: [[1,1,1],[1,0,1],[1,1,1]] -> [[1,0,1],[0,0,0],[1,0,1]].

Brute force
-----------
Make a copy of the matrix; for every zero in the copy, zero out that row and column in
the original. O(m*n*(m+n)) time, O(m*n) space. (The slightly smarter O(m+n) space
version records which rows and columns contain a zero in two sets, then zeroes them in
a second pass.) The waste in the naive version is the repeated row/column clearing —
a row with k zeros is cleared k times — and the copy exists only to distinguish
"original zero" from "zero we just wrote".

From brute force to optimal
---------------------------
The O(m+n) sets are the right idea: we only need two bit-vectors, "row r has a zero"
and "column c has a zero". Observation: the matrix already contains two unused
vectors of exactly that size — the first row and the first column. Store the column
flags in row 0 and the row flags in column 0. The only conflict is cell (0, 0), which
would have to carry both the row-0 flag and the column-0 flag; resolve it with ONE
extra boolean for "column 0 must be zeroed" and let (0, 0) represent row 0. Then
process the interior cells using the flags, and finally fix row 0 and column 0 last
(because they are the flag storage, they must be touched after everything else).

Intuition
---------
The information needed is just m + n bits. Any cell in row r that is zero means the
whole row will be zeroed anyway, so writing a flag into matrix[r][0] destroys nothing
of value — row r and column c are doomed regardless. The first row/column become a
scratchpad because their contents are fully determined by the flags themselves.

Geometric view
--------------
Picture the grid with its first row and first column highlighted as a header strip.
Pass 1 scans the body and, for each zero, paints a marker on the header strip in that
row and in that column. Pass 2 scans the body again and zeroes any cell whose row
header or column header is marked. Pass 3 handles the header strip itself: row 0
using the (0, 0) flag, column 0 using the separate boolean.

Steps
-----
1. first_col_zero = any(matrix[r][0] == 0 for r in range(m)).
2. For each r, c with c >= 1: if matrix[r][c] == 0, set matrix[r][0] = 0 and matrix[0][c] = 0.
3. For r in 1..m-1, c in 1..n-1: if matrix[r][0] == 0 or matrix[0][c] == 0, set matrix[r][c] = 0.
4. If matrix[0][0] == 0, zero all of row 0.
5. If first_col_zero, zero all of column 0.

Complexity: O(m*n) time, O(1) extra space — two sweeps plus two line clears, one boolean.
Pitfalls: zeroing row 0 / column 0 BEFORE processing the interior (destroys the flags);
forgetting the separate boolean for column 0 and letting (0, 0) do double duty;
processing cells with c == 0 in the marking step (overwrites row flags).
"""
from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        first_col_zero = any(matrix[r][0] == 0 for r in range(m))
        # mark: matrix[r][0] flags row r, matrix[0][c] flags column c (c >= 1)
        for r in range(m):
            for c in range(1, n):
                if matrix[r][c] == 0:
                    matrix[r][0] = 0
                    matrix[0][c] = 0
        # apply flags to the interior (everything except row 0 / column 0)
        for r in range(1, m):
            for c in range(1, n):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0
        if matrix[0][0] == 0:            # row-0 flag lives in (0, 0)
            for c in range(n):
                matrix[0][c] = 0
        if first_col_zero:               # column 0 handled by the separate boolean
            for r in range(m):
                matrix[r][0] = 0


def brute_force(matrix: List[List[int]]) -> None:
    m, n = len(matrix), len(matrix[0])
    snapshot = [row[:] for row in matrix]
    for r in range(m):
        for c in range(n):
            if snapshot[r][c] == 0:
                for k in range(n):
                    matrix[r][k] = 0
                for k in range(m):
                    matrix[k][c] = 0


if __name__ == "__main__":
    s = Solution()
    a = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    s.setZeroes(a)
    assert a == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    b = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    s.setZeroes(b)
    assert b == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    c = [[1, 2, 3]]
    s.setZeroes(c)
    assert c == [[1, 2, 3]]
    d = [[1], [0], [3]]
    s.setZeroes(d)
    assert d == [[0], [0], [0]]
    cases = [
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],
        [[1, 2, 3]], [[1], [0], [3]], [[0]],
        [[1, 2], [3, 4]], [[1, 0], [1, 1]], [[1, 1], [0, 1]],
    ]
    for case in cases:
        x = [row[:] for row in case]
        y = [row[:] for row in case]
        s.setZeroes(x)
        brute_force(y)
        assert x == y
    print("ok")
