"""
Matrix Traversal Patterns - Basics
Area: matrices
Key operations: row-major and column-major walks, anti-diagonals by r + c, 4/8 direction vectors with bounds checks

An m x n matrix can be walked row by row, column by column, or along anti-diagonals: the cells with
the same r + c form one anti-diagonal, and there are m + n - 1 of them. solve returns the
anti-diagonal order, each diagonal read top-right to bottom-left; the other walks and the neighbor
vectors are shown in the trace and checked in the tests.
Example: [[1,2,3],[4,5,6],[7,8,9]] -> [1, 2, 4, 3, 5, 7, 6, 8, 9]
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(matrix):
    """List every cell, sort by (r + c, r), read the values. O(mn log mn); the direct walk never sorts."""
    m, n = len(matrix), len(matrix[0])
    cells = sorted(((r, c) for r in range(m) for c in range(n)), key=lambda rc: (rc[0] + rc[1], rc[0]))
    return [matrix[r][c] for r, c in cells]


# --- optimal ---
DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def row_major(matrix):
    return [x for row in matrix for x in row]


def col_major(matrix):
    return [matrix[r][c] for c in range(len(matrix[0])) for r in range(len(matrix))]


def neighbors(matrix, r, c, dirs=DIRS4):
    """In-bounds neighbor coordinates of (r, c). O(1): at most 8 checks."""
    m, n = len(matrix), len(matrix[0])
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < m and 0 <= c + dc < n]


def solve(matrix):
    """Anti-diagonal d holds the cells with r + c == d; r runs from max(0, d-n+1) to min(m-1, d). O(m*n)."""
    m, n = len(matrix), len(matrix[0])
    log(f"row-major    {row_major(matrix)}")
    log(f"column-major {col_major(matrix)}")
    log(f"4-neighbors of (0,0) {neighbors(matrix, 0, 0)} | 8-neighbors of ({m // 2},{n // 2}) {neighbors(matrix, m // 2, n // 2, DIRS8)}")
    out = []
    for d in range(m + n - 1):
        seg = []
        for r in range(max(0, d - n + 1), min(m - 1, d) + 1):
            seg.append(matrix[r][d - r])
        out += seg
        log(f"anti-diagonal r+c={d}: rows {max(0, d - n + 1)}..{min(m - 1, d)} -> {seg} | out {out}")
    return out


# --- demo ---
def demo():
    return solve([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


# --- tests ---
def tests():
    M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert solve(M) == [1, 2, 4, 3, 5, 7, 6, 8, 9]
    assert solve([[1, 2, 3, 4]]) == [1, 2, 3, 4]
    assert solve([[1], [2], [3]]) == [1, 2, 3]
    assert solve([[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 4, 5, 6]
    assert solve([[1, 2, 3], [4, 5, 6]]) == [1, 2, 4, 3, 5, 6]
    assert solve([[7]]) == [7]
    assert row_major(M) == [1, 2, 3, 4, 5, 6, 7, 8, 9] and col_major(M) == [1, 4, 7, 2, 5, 8, 3, 6, 9]
    assert neighbors(M, 0, 0) == [(1, 0), (0, 1)] and neighbors(M, 2, 2) == [(1, 2), (2, 1)]
    assert sorted(neighbors(M, 1, 1, DIRS8)) == sorted((r, c) for r in range(3) for c in range(3) if (r, c) != (1, 1))
    assert neighbors(M, 0, 2, DIRS8) == [(1, 2), (0, 1), (1, 1)] and neighbors([[1]], 0, 0, DIRS8) == []
    import random
    rng = random.Random(0)
    for _ in range(200):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        a = [[rng.randint(0, 9) for _ in range(n)] for _ in range(m)]
        assert solve(a) == brute_force(a), a
        assert col_major(a) == row_major([list(col) for col in zip(*a)]), a
        r, c = rng.randrange(m), rng.randrange(n)
        assert all(0 <= nr < m and 0 <= nc < n for nr, nc in neighbors(a, r, c, DIRS8)), (a, r, c)
        assert len(neighbors(a, r, c, DIRS8)) == len({(nr, nc) for nr in range(max(0, r - 1), min(m, r + 2)) for nc in range(max(0, c - 1), min(n, c + 2))}) - 1


# --- bugs ---
BUGS = [
    {
        "replace": "        for r in range(max(0, d - n + 1), min(m - 1, d) + 1):",
        "with":    "        for r in range(max(0, d - n + 1), min(m - 1, d)):",
        "fix": "range excludes its end, so the last row of the diagonal needs + 1",
        "why": "Every anti-diagonal loses its bottom-left cell: the 3x3 example returns [2, 3, 5, 6] with only 4 values.",
        "decoys": [
            {"line": "    for d in range(m + n - 1):", "change": "should be range(m + n)"},
            {"line": "            seg.append(matrix[r][d - r])", "change": "should be matrix[d - r][r]"},
            {"line": "        out += seg", "change": "should be out += seg[::-1]"},
        ],
    },
    {
        "replace": "    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < m and 0 <= c + dc < n]",
        "with":    "    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr <= m and 0 <= c + dc <= n]",
        "fix": "valid rows are 0..m-1 and valid columns 0..n-1: the upper bound check is strict",
        "why": "Cells on the bottom row and right column get out-of-range neighbors like (m, c), which would raise IndexError when read.",
        "decoys": [
            {"line": "DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right", "change": "should include (0, 0)"},
            {"line": "DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]", "change": "should drop the four diagonals"},
            {"line": "    return [matrix[r][c] for c in range(len(matrix[0])) for r in range(len(matrix))]", "change": "should loop r first"},
        ],
    },
    {
        "replace": "    for d in range(m + n - 1):",
        "with":    "    for d in range(m + n - 2):",
        "fix": "there are m + n - 1 anti-diagonals (r + c runs from 0 to m + n - 2 inclusive)",
        "why": "The last anti-diagonal, the single bottom-right cell, is never emitted: the example ends at 8.",
        "decoys": [
            {"line": "        seg = []", "change": "should be seg = [matrix[d][0]]"},
            {"line": "    return out", "change": "should return seg"},
            {"line": "    return [x for row in matrix for x in row]", "change": "should be [row for row in matrix]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
