"""
Spiral Matrix (LeetCode 54)  — Medium
Pattern: Shrinking boundary traversal

Problem
-------
Given an m x n matrix, return all its elements in clockwise spiral order, starting at
the top-left and moving right.
Example: [[1,2,3],[4,5,6],[7,8,9]] -> [1, 2, 3, 6, 9, 8, 7, 4, 5].

Brute force
-----------
Simulate a walker: keep a visited matrix, a direction (right, down, left, up) and a
position; step forward while the next cell is in bounds and unvisited, otherwise turn
clockwise. O(m*n) time but O(m*n) extra space for the visited grid, and every step
does a bounds-and-visited check. The waste is the visited matrix and the per-step
checks: the spiral's turning points are completely predictable from four boundary
numbers, so tracking visitation cell by cell is unnecessary.

From brute force to optimal
---------------------------
The walker only ever turns when it hits the edge of the not-yet-visited rectangle, and
that rectangle is always a sub-rectangle described by four numbers: top, bottom, left,
right. So replace the visited grid with those four bounds. Peel one layer per loop
iteration: walk the top row left->right, then the right column top->bottom, then (if
a row remains) the bottom row right->left, then (if a column remains) the left column
bottom->top. After each side, move its bound inward. The two "if" guards handle the
case where the remaining rectangle collapses to a single row or column, which
otherwise double-counts.

Intuition
---------
A spiral is just the outer ring of the rectangle, followed by the spiral of the
rectangle one size smaller. Tracking the current rectangle with four bounds captures
all the state the walker needs; cells are never revisited because bounds only move
inward.

Geometric view
--------------
Picture an onion of rectangular rings. Four fences — top, bottom, left, right — mark
the current ring. The traversal runs along the top fence, down the right fence,
back along the bottom fence, up the left fence, and then each fence steps in by one
cell. When the fences cross, every cell has been emitted.

Steps
-----
1. top, bottom, left, right = 0, m - 1, 0, n - 1; result = [].
2. While top <= bottom and left <= right:
3.   emit matrix[top][left..right]; top += 1.
4.   emit matrix[top..bottom][right]; right -= 1.
5.   if top <= bottom: emit matrix[bottom][right..left] reversed; bottom -= 1.
6.   if left <= right: emit matrix[bottom..top][left] reversed; left += 1.
7. Return result.

Complexity: O(m*n) time, O(1) extra space ignoring the output — each cell is emitted
exactly once.
Pitfalls: omitting the two re-checks after shrinking top and right (duplicates on a
1xN or Nx1 remainder); wrong inclusive/exclusive range ends; non-square matrices
tested only with squares.
"""
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        result: List[int] = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        while top <= bottom and left <= right:
            for c in range(left, right + 1):            # top row ->
                result.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):            # right column v
                result.append(matrix[r][right])
            right -= 1
            if top <= bottom:                           # a row still remains
                for c in range(right, left - 1, -1):    # bottom row <-
                    result.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:                           # a column still remains
                for r in range(bottom, top - 1, -1):    # left column ^
                    result.append(matrix[r][left])
                left += 1
        return result


def brute_force(matrix: List[List[int]]) -> List[int]:
    m, n = len(matrix), len(matrix[0])
    visited = [[False] * n for _ in range(m)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r = c = d = 0
    result = []
    for _ in range(m * n):
        result.append(matrix[r][c])
        visited[r][c] = True
        nr, nc = r + directions[d][0], c + directions[d][1]
        if not (0 <= nr < m and 0 <= nc < n and not visited[nr][nc]):
            d = (d + 1) % 4
            nr, nc = r + directions[d][0], c + directions[d][1]
        r, c = nr, nc
    return result


if __name__ == "__main__":
    s = Solution()
    assert s.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert s.spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert s.spiralOrder([[1, 2, 3]]) == [1, 2, 3]
    assert s.spiralOrder([[1], [2], [3]]) == [1, 2, 3]
    assert s.spiralOrder([[7]]) == [7]
    cases = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
        [[1, 2, 3]], [[1], [2], [3]], [[7]],
        [[1, 2], [3, 4], [5, 6], [7, 8]],
    ]
    for case in cases:
        assert s.spiralOrder(case) == brute_force(case)
    print("ok")
