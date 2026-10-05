"""
Set Matrix Zeroes (LeetCode 73) - Basics
Area: matrices
Key operations: record flags for row 0 and column 0 first, mark in the first row/column, zero the inside, finish the borders

Given an m x n matrix, if a cell is 0 set its entire row and column to 0, in place, with O(1) extra
space. The first row and the first column are reused as the markers for "this column / this row must
be zeroed"; two booleans remember whether they themselves need zeroing.
Example: [[0,1,2,0],[3,4,5,2],[1,3,1,5]] -> [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
"""


# --- brute force ---
def brute_force(matrix):
    """Collect the zero rows and zero columns in two sets, then build a new matrix. O(m*n) time, O(m + n) extra space."""
    m, n = len(matrix), len(matrix[0])
    rows = {r for r in range(m) for c in range(n) if matrix[r][c] == 0}
    cols = {c for r in range(m) for c in range(n) if matrix[r][c] == 0}
    return [[0 if r in rows or c in cols else matrix[r][c] for c in range(n)] for r in range(m)]


# --- optimal ---
def solve(matrix):
    """Flags for row 0 / column 0, markers in row 0 / column 0 for the rest, zero the inside, then the borders. O(m*n), O(1) space."""
    m, n = len(matrix), len(matrix[0])
    row0 = any(x == 0 for x in matrix[0])
    col0 = any(matrix[r][0] == 0 for r in range(m))
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = matrix[0][c] = 0
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if row0:
        matrix[0][:] = [0] * n
    if col0:
        for r in range(m):
            matrix[r][0] = 0
    return matrix


# --- demo ---
def demo():
    return solve([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]])


# --- bugs ---
BUGS = [
    {
        "replace": "            if matrix[r][0] == 0 or matrix[0][c] == 0:",
        "with":    "            if matrix[r][0] == 0 and matrix[0][c] == 0:",
        "fix": "a cell is zeroed when its row OR its column is marked",
        "why": "Only cells at the intersection of a marked row and a marked column are zeroed, so most of the row and column keep their values: the 3x3 example with a center 0 stays almost unchanged.",
        "decoys": [
            {"line": "            if matrix[r][c] == 0:", "change": "should be != 0"},
            {"line": "    m, n = len(matrix), len(matrix[0])", "change": "should be len(matrix[0]), len(matrix)"},
            {"line": "        matrix[0][:] = [0] * n", "change": "should be [0] * m"},
        ],
    },
    {
        "replace": "                matrix[r][0] = matrix[0][c] = 0",
        "with":    "                matrix[r][0] = 0",
        "fix": "mark BOTH the row (column 0) and the column (row 0) of a zero cell",
        "why": "Columns are never marked, so only rows get zeroed: [[1,1,1],[1,0,1],[1,1,1]] keeps 1 at (0,1) and (2,1).",
        "decoys": [
            {"line": "    col0 = any(matrix[r][0] == 0 for r in range(m))", "change": "should check matrix[0][r]"},
            {"line": "    if col0:", "change": "should be if row0"},
            {"line": "    if row0:", "change": "should be if matrix[0][0] == 0"},
        ],
    },
    {
        "replace": "    if row0:",
        "with":    "    if matrix[0][0] == 0:",
        "fix": "use the flag computed BEFORE marking; the corner only says whether the original corner was zero",
        "why": "A zero elsewhere in row 0 does not change the corner, so row 0 is left alone: [[1,0,1],[1,1,1]] keeps its first row.",
        "decoys": [
            {"line": "    row0 = any(x == 0 for x in matrix[0])", "change": "should be all(...)"},
            {"line": "    if col0:", "change": "should be if not col0"},
            {"line": "            matrix[r][0] = 0", "change": "should be matrix[0][r] = 0"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
