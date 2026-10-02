"""
Zigzag Conversion (LeetCode 6)  — Medium
Pattern: Row buckets with a bouncing row pointer

Problem
-------
Write the string s in a zigzag over numRows rows (down the first column, then diagonally up to
row 0, then down again...) and read it row by row.
Example: "PAYPALISHIRING", 3 rows ->
  P   A   H   N
  A P L S I I G
  Y   I   R      -> "PAHNAPLSIIGYIR".   With 4 rows -> "PINALSIGYAHRPI".

Brute force
-----------
Simulate the drawing literally: allocate a numRows x n grid of blanks, walk the zigzag placing
each character at its (row, col) coordinate (the column advances on every diagonal step), then
scan the whole grid row-major and collect the non-blank cells. O(numRows * n) time and space.
The wasted work is the grid: most cells stay blank (the diagonals leave gaps), yet we allocate
and later scan every one of them.

From brute force to optimal
---------------------------
The output only needs to know WHICH row each character lands on, never its column, because
within a row characters keep their original left-to-right order. So drop the grid and keep one
string builder per row. The row index for successive characters just bounces: 0,1,...,numRows-1,
numRows-2,...,1,0,1,... so a single pointer with a step of +1/-1 that reverses at the top and
bottom rows assigns each character in O(1). Concatenate the rows at the end. The simulation
collapses to one linear pass with numRows lists whose total size is n.

Intuition
---------
Zigzag = a ball bouncing between the floor and ceiling as the string streams past. The column
is irrelevant to the answer; the bounce tells you the row, and the stream order tells you the
position within the row.

Geometric view
--------------
s:   P A Y P A L I S H I R I N G
row: 0 1 2 1 0 1 2 1 0 1 2 1 0 1      step flips at row 0 and row numRows-1
rows[0] = P A H N
rows[1] = A P L S I I G
rows[2] = Y I R          -> join rows top to bottom.

Steps
-----
1. If numRows == 1 or numRows >= len(s): return s (no zigzag).
2. rows = [[] for each row]; r = 0; step = 1.
3. For each ch: rows[r].append(ch); if r == 0: step = 1; elif r == numRows-1: step = -1; r += step.
4. Return the concatenation of all rows.

Complexity: O(n) time, O(n) space — each character is appended to exactly one row list.
Pitfalls: numRows == 1 makes the step logic loop forever without the guard; flipping the step
          BEFORE appending (shifts every row by one); numRows larger than the string.
"""


class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s
        rows = [[] for _ in range(numRows)]
        r, step = 0, 1
        for ch in s:
            rows[r].append(ch)
            if r == 0:
                step = 1                   # bounce off the top
            elif r == numRows - 1:
                step = -1                  # bounce off the bottom
            r += step
        return "".join("".join(row) for row in rows)


def brute_force(s: str, numRows: int) -> str:
    """Draw the zigzag into a real numRows x n grid, then read it row by row."""
    if numRows == 1:
        return s
    grid = [[""] * len(s) for _ in range(numRows)]
    r, c, going_down = 0, 0, True
    for ch in s:
        grid[r][c] = ch
        if going_down:
            if r == numRows - 1:
                going_down, r, c = False, r - 1, c + 1
            else:
                r += 1
        else:
            if r == 0:
                going_down, r = True, r + 1
            else:
                r, c = r - 1, c + 1
    return "".join(cell for row in grid for cell in row if cell)


if __name__ == "__main__":
    sol = Solution()
    assert sol.convert("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"
    assert sol.convert("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"
    assert sol.convert("A", 1) == "A"
    assert sol.convert("AB", 1) == "AB"                 # edge: one row
    assert sol.convert("ABC", 5) == "ABC"               # edge: more rows than characters
    for s in ["PAYPALISHIRING", "ABCDEFGHIJ", "A", "AB", "ABC"]:
        for k in range(1, 6):
            assert sol.convert(s, k) == brute_force(s, k), (s, k)
    print("ok")
