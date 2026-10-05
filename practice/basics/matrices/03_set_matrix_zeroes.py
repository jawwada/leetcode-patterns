"""
Set Matrix Zeroes (LeetCode 73) - Basics
Area: matrices
Key operations: record flags for row 0 and column 0 first, mark in the first row/column, zero the inside, finish the borders

Given an m x n matrix, if a cell is 0 set its entire row and column to 0, in place, with O(1) extra
space. The first row and the first column are reused as the markers for "this column / this row must
be zeroed"; two booleans remember whether they themselves need zeroing.
Example: [[0,1,2,0],[3,4,5,2],[1,3,1,5]] -> [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
    log(f"flags: zero row 0 = {row0}, zero column 0 = {col0}")
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = matrix[0][c] = 0
    log("markers set in row 0 and column 0:\n" + "\n".join(f"    {row}" for row in matrix))
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    log("inside zeroed from the markers:\n" + "\n".join(f"    {row}" for row in matrix))
    if row0:
        matrix[0][:] = [0] * n
    if col0:
        for r in range(m):
            matrix[r][0] = 0
    log("borders finished from the flags:\n" + "\n".join(f"    {row}" for row in matrix))
    return matrix


# --- demo ---
def demo():
    return solve([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]])


# --- tests ---
def tests():
    assert solve([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]) == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    assert solve([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    assert solve([[1, 0, 1], [1, 1, 1]]) == [[0, 0, 0], [1, 0, 1]]  # zero in row 0 but not in the corner
    assert solve([[1, 1], [0, 1]]) == [[0, 1], [0, 0]]  # zero in column 0 but not in the corner
    assert solve([[1]]) == [[1]] and solve([[0]]) == [[0]]
    assert solve([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
    assert solve([[1, 2, 3], [4, 5, 6], [7, 8, 0]]) == [[1, 2, 0], [4, 5, 0], [0, 0, 0]]
    import random
    rng = random.Random(0)
    for _ in range(200):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        a = [[0 if rng.random() < 0.2 else rng.randint(1, 9) for _ in range(n)] for _ in range(m)]
        assert solve([row[:] for row in a]) == brute_force(a), a


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
