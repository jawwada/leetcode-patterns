"""
Maximal Rectangle (LeetCode 85)  — Hard
Pattern: Monotonic stack

Problem
-------
Given an m x n binary matrix of '0'/'1' characters, return the area of the largest
rectangle containing only '1's.
Example: [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],
          ["1","0","0","1","0"]] -> 6 (the 2 x 3 block in rows 1-2, columns 2-4).

Brute force
-----------
Enumerate every pair of corners (r1,c1) <= (r2,c2) and check that every cell inside is
'1'. There are O(m^2 n^2) rectangles and each check costs O(mn), so O(m^3 n^3) time,
O(1) space. The wasted work is re-scanning the same cells: the rectangle (r1,c1,r2,c2)
and (r1,c1,r2,c2+1) share almost all their cells, yet both are checked from scratch.

From brute force to optimal
---------------------------
Step 1 (O(m^2 n^2) -> O(m n^2) or O(m^2 n)): fix the bottom row r and record, for each
column c, height[c] = number of consecutive '1's ending at row r. Then the tallest
rectangle whose bottom edge is on row r and spans columns [c1, c2] has height
min(height[c1..c2]) — the 2-D question has become "largest rectangle in a histogram",
which brute-forces in O(n^2) per row. Step 2 (per-row O(n^2) -> O(n)): in the
histogram, bar c's maximal rectangle extends left to the first shorter bar and right to
the first shorter bar. A monotonic increasing stack finds both boundaries for every bar
in one pass: when bar c is shorter than the stack top, the top's right boundary is c and
its left boundary is the new top. Each bar is pushed and popped once, so each row costs
O(n) and the whole matrix O(mn).

Intuition
---------
A rectangle of 1s is defined by its bottom row and the shortest column of 1s rising
above it. Sweeping the bottom row downward and maintaining "how many 1s stand above me"
per column turns each row into a histogram. In a histogram, every maximal rectangle is
pinned by some bar that is its shortest; when a shorter bar arrives from the right, every
taller bar on the stack has just discovered its right wall and can be settled.

Geometric view
--------------
Picture the matrix as stacked skylines: row r's skyline has a bar of height h at column
c when the last h cells above and including (r, c) are 1s. A '0' resets the bar to the
ground. On each skyline a stack of columns with increasing heights climbs from left to
right; a drop in height pops the taller columns and each popped column sweeps out a
rectangle between its two nearest shorter neighbours.

Steps
-----
1. heights = [0] * n. For each row: heights[c] = heights[c] + 1 if cell is '1' else 0.
2. Run largest-rectangle-in-histogram on heights with a sentinel 0 appended.
3.   Keep a stack of indices with increasing heights. For each index i (including the
     sentinel): while heights[i] < heights[stack top], pop top; its width is
     i - (new top) - 1 (or i if the stack is empty); update best.
4. Return the best area over all rows.

Complexity: O(m n) time, O(n) space — each row's histogram pass pushes/pops every column once.
Pitfalls: forgetting the sentinel so bars still on the stack at the row's end are never
measured; resetting heights to 0 on a '0' (not decrementing); using <= vs < when popping
(either gives the right area but be consistent); cells are strings, not ints.
"""
from typing import List


class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        n = len(matrix[0])
        heights = [0] * (n + 1)          # heights[n] is a permanent 0 sentinel
        best = 0
        for row in matrix:
            for c in range(n):
                heights[c] = heights[c] + 1 if row[c] == "1" else 0
            stack = []                   # indices with strictly increasing heights
            for i in range(n + 1):
                while stack and heights[i] < heights[stack[-1]]:
                    h = heights[stack.pop()]
                    left = stack[-1] if stack else -1
                    best = max(best, h * (i - left - 1))
                stack.append(i)
        return best


def brute_force(matrix: List[List[str]]) -> int:
    m, n = len(matrix), len(matrix[0]) if matrix else 0
    best = 0
    for r1 in range(m):
        for c1 in range(n):
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    if all(matrix[r][c] == "1"
                           for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):
                        best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))
    return best


if __name__ == "__main__":
    s = Solution()
    m1 = [["1", "0", "1", "0", "0"],
          ["1", "0", "1", "1", "1"],
          ["1", "1", "1", "1", "1"],
          ["1", "0", "0", "1", "0"]]
    assert s.maximalRectangle(m1) == 6
    assert s.maximalRectangle([["0"]]) == 0
    assert s.maximalRectangle([["1"]]) == 1
    assert s.maximalRectangle([["0", "0"]]) == 0
    assert s.maximalRectangle([["1", "1"], ["1", "1"]]) == 4
    assert s.maximalRectangle([]) == 0
    import random
    random.seed(85)
    cases = [m1, [["0"]], [["1"]], [["1", "1"], ["1", "1"]]]
    for _ in range(30):
        m, n = random.randint(1, 5), random.randint(1, 5)
        cases.append([[random.choice("01") for _ in range(n)] for _ in range(m)])
    for case in cases:
        assert s.maximalRectangle(case) == brute_force(case)
    print("ok")
