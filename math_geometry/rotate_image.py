"""
Rotate Image (LeetCode 48)  — Medium
Pattern: Transpose + reverse rows (in-place matrix rotation)

Problem
-------
Rotate an n x n matrix 90 degrees clockwise IN PLACE (no second matrix).
Example: [[1,2,3],[4,5,6],[7,8,9]] -> [[7,4,1],[8,5,2],[9,6,3]].

Brute force
-----------
Allocate a new n x n matrix and copy each cell to its rotated position:
new[c][n-1-r] = old[r][c]. Then copy the new matrix back over the old one. O(n^2)
time, O(n^2) space. The waste is the second matrix: every cell is written twice
(once into the copy, once back), and the copy exists only because we did not know how
to move cells without overwriting ones we still need.

From brute force to optimal
---------------------------
The rotation maps (r, c) -> (c, n-1-r). Decompose it into two simpler moves that ARE
easy to do in place: the transpose (r, c) -> (c, r) swaps pairs of cells across the
main diagonal and never overwrites anything unsaved; then reversing each row maps
(c, r) -> (c, n-1-r). Composing the two gives exactly the clockwise rotation. Both
steps are swap-based, so no scratch matrix is needed. (The alternative — rotating
4-cell cycles ring by ring — also works but is fiddlier to index.)

Intuition
---------
A 90-degree rotation is a reflection across the main diagonal followed by a
horizontal flip. Reflections are trivially in place because they pair cells up and
swap them. Two reflections compose into the rotation.

Geometric view
--------------
Hold a square card. Step 1 (transpose): flip it over along the top-left to
bottom-right diagonal — the first row becomes the first column. Step 2 (reverse
rows): flip it left-to-right like turning a page. The picture now sits rotated 90
degrees clockwise. Counter-clockwise is transpose + reverse columns.

Steps
-----
1. n = len(matrix).
2. Transpose: for r in range(n), for c in range(r + 1, n): swap matrix[r][c], matrix[c][r].
3. Reverse each row: for row in matrix: row.reverse().

Complexity: O(n^2) time, O(1) extra space — each cell is swapped at most twice.
Pitfalls: transposing with the full inner range (swaps everything back to where it
started); reversing columns instead of rows (gives the counter-clockwise rotation);
returning a new matrix when the problem demands in-place.
"""
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for r in range(n):                      # transpose across the main diagonal
            for c in range(r + 1, n):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
        for row in matrix:                      # then mirror each row left<->right
            row.reverse()


def brute_force(matrix: List[List[int]]) -> None:
    n = len(matrix)
    rotated = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            rotated[c][n - 1 - r] = matrix[r][c]
    for r in range(n):
        matrix[r] = rotated[r]


if __name__ == "__main__":
    s = Solution()
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    s.rotate(m)
    assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    s.rotate(m)
    assert m == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
    m = [[1]]
    s.rotate(m)
    assert m == [[1]]
    for case in ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 2], [3, 4]], [[1]]):
        x = [row[:] for row in case]
        y = [row[:] for row in case]
        s.rotate(x)
        brute_force(y)
        assert x == y
    print("ok")
