"""
Search a 2D Matrix II (LeetCode 240) - Basics
Area: matrices
Key operations: start at the top-right corner, move left when too big, move down when too small

Every row is sorted left to right and every column top to bottom. Return whether target is present.
From the top-right corner a value larger than target rules out its whole column (everything below is
bigger), a smaller one rules out its whole row (everything to the left is smaller), so each step
discards a row or a column.
Example: [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target 5 -> True
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(matrix, target):
    """Scan every cell. O(m*n); ignores the sorted order the staircase walk exploits."""
    return any(x == target for row in matrix for x in row)


# --- optimal ---
def solve(matrix, target):
    """Staircase from the top-right: too big -> left (drop the column), too small -> down (drop the row). O(m + n)."""
    if not matrix or not matrix[0]:
        return False
    m, n = len(matrix), len(matrix[0])
    r, c = 0, n - 1
    while r < m and c >= 0:
        x = matrix[r][c]
        if x == target:
            log(f"({r},{c}) = {x} == {target}: FOUND")
            return True
        if x > target:
            log(f"({r},{c}) = {x} > {target}: column {c} ruled out, move left")
            c -= 1
        else:
            log(f"({r},{c}) = {x} < {target}: row {r} ruled out, move down")
            r += 1
        log(f"    remaining rows {r}..{m - 1}, cols 0..{c}")
    log(f"walked off the matrix at ({r},{c}): not found")
    return False


# --- demo ---
def demo():
    matrix = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
    return solve(matrix, 5)


# --- tests ---
def tests():
    M = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
    assert solve(M, 5) is True
    assert solve(M, 20) is False
    assert solve(M, 18) is True  # bottom-left corner: the last column checked is 0
    assert solve(M, 30) is True and solve(M, 1) is True and solve(M, 15) is True
    assert solve(M, 0) is False and solve(M, 31) is False
    assert solve([], 1) is False and solve([[]], 1) is False
    assert solve([[5]], 5) is True and solve([[5]], 4) is False
    assert solve([[1, 3, 5]], 3) is True and solve([[1], [3], [5]], 5) is True
    import random
    rng = random.Random(0)
    for _ in range(200):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        a = [[3 * r + 3 * c + rng.randint(0, 2) for c in range(n)] for r in range(m)]  # sorted both ways
        target = rng.randint(-1, 3 * (m + n))
        assert solve(a, target) == brute_force(a, target), (a, target)


# --- bugs ---
BUGS = [
    {
        "replace": "    r, c = 0, n - 1",
        "with":    "    r, c = 0, 0",
        "fix": "start at the TOP-RIGHT corner: it is the only corner where one comparison rules out a whole row or column",
        "why": "From the top-left both moves lead to bigger values, so a smaller cell can never be reached: target 5 in the example walks 1, 2, 3, 10 and gives up.",
        "decoys": [
            {"line": "    m, n = len(matrix), len(matrix[0])", "change": "should be len(matrix[0]), len(matrix)"},
            {"line": "        x = matrix[r][c]", "change": "should be matrix[c][r]"},
            {"line": "        if x == target:", "change": "should come after the two moves"},
        ],
    },
    {
        "replace": "        if x > target:",
        "with":    "        if x < target:",
        "fix": "a value BIGGER than target discards its column (move left); a smaller one discards its row (move down)",
        "why": "The moves are swapped, so the walk runs down the last column and off the matrix: target 5 is reported missing.",
        "decoys": [
            {"line": "            c -= 1", "change": "should be c = 0"},
            {"line": "            r += 1", "change": "should be r = m - 1"},
            {"line": "            return True", "change": "should return (r, c)"},
        ],
    },
    {
        "replace": "    while r < m and c >= 0:",
        "with":    "    while r < m and c > 0:",
        "fix": "column 0 is a valid column: the walk continues while c >= 0",
        "why": "Any target that lives in column 0 is never compared: 18 in the example is reported missing.",
        "decoys": [
            {"line": "    if not matrix or not matrix[0]:", "change": "should be if not matrix only"},
            {"line": "        return False", "change": "should return None"},
            {"line": "    return solve(matrix, 5)", "change": "should search for 20"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
