"""
N-Queens (LeetCode 51) - Medium-Hard
Area: backtracking
Key operations: one queen per row, attacked = column / diagonal r - c / anti-diagonal r + c sets, add / recurse / remove

Place n queens on an n x n board so that no two share a row, column or diagonal. Return every
distinct board as a list of strings ('Q' queen, '.' empty), sorted.
Example: n = 4 -> [["..Q.", "Q...", "...Q", ".Q.."], [".Q..", "...Q", "Q...", "..Q."]]
"""
from itertools import permutations
from typing import List


# --- helpers ---
def render(queens: List[int], n: int) -> List[str]:
    """queens[r] = column of the queen in row r -> the board as rows of '.' and 'Q'."""
    return ["." * c + "Q" + "." * (n - c - 1) for c in queens]


# --- brute force ---
def brute_force(n: int) -> List[List[str]]:
    """One queen per row and per column is a permutation of columns: try all n! of them and keep those
    with no two queens on a diagonal. O(n! * n^2): a prefix already in conflict is still completed in
    every possible way and each completion is checked pairwise at the end."""
    boards = []
    for perm in permutations(range(n)):
        if all(abs(perm[i] - perm[j]) != j - i for i in range(n) for j in range(i + 1, n)):
            boards.append(render(list(perm), n))
    return sorted(boards)


# --- optimal ---
def solve(n: int) -> List[List[str]]:
    """Row by row, try each column not under attack; a queen at (r, c) owns column c, diagonal r - c and
    anti-diagonal r + c, so three sets answer 'attacked?' in O(1). O(n!) nodes, O(n) extra space."""
    result, queens = [], []
    cols, diag, anti = set(), set(), set()

    def dfs(r: int) -> None:
        if r == n:
            result.append(render(queens, n))
            return
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue
            cols.add(c); diag.add(r - c); anti.add(r + c)
            queens.append(c)
            dfs(r + 1)
            queens.pop()
            cols.discard(c); diag.discard(r - c); anti.discard(r + c)

    dfs(0)
    return sorted(result)


# --- demo ---
def demo():
    return solve(4)


# --- bugs ---
BUGS = [
    {
        "replace": "            if c in cols or r - c in diag or r + c in anti:",
        "with":    "            if c in cols or r + c in diag or r + c in anti:",
        "fix": "the two diagonals need different keys: r - c for the '\\' diagonal and r + c for the '/' one",
        "why": "diag is filled with r - c but queried with r + c, so '\\' attacks go unnoticed and n = 4 returns boards with two queens on one diagonal.",
        "decoys": [
            {"line": "            cols.add(c); diag.add(r - c); anti.add(r + c)", "change": "should run after the recursive call"},
            {"line": "        if r == n:", "change": "should be r == n - 1"},
            {"line": "    return sorted(result)", "change": "should return len(result)"},
        ],
    },
    {
        "replace": "            cols.discard(c); diag.discard(r - c); anti.discard(r + c)",
        "with":    "            cols.discard(c); diag.discard(r - c)",
        "fix": "remove the anti-diagonal too: every mark made before the recursive call must be undone after it",
        "why": "A lifted queen keeps guarding its '/' diagonal, so later branches are pruned wrongly and n = 4 loses solutions.",
        "decoys": [
            {"line": "            queens.pop()", "change": "should be queens.pop(0)"},
            {"line": "            dfs(r + 1)", "change": "should be dfs(r)"},
            {"line": "        for c in range(n):", "change": "should be range(r, n)"},
        ],
    },
    {
        "replace": "        if r == n:",
        "with":    "        if r == n - 1:",
        "fix": "a board is complete when all n rows hold a queen, which is r == n",
        "why": "Boards are recorded with n - 1 queens, so n = 1 returns [[]] and n = 4 returns many partial boards.",
        "decoys": [
            {"line": "            queens.append(c)", "change": "should append r"},
            {"line": "    dfs(0)", "change": "should be dfs(1)"},
            {"line": "    result, queens = [], []", "change": "queens should start as [0]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
