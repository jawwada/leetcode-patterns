"""
Combinations n Choose k (LeetCode 77) - Basics
Area: backtracking
Key operations: choose i, recurse from i + 1, prune when fewer numbers remain than open slots, unchoose

Return every combination of k numbers chosen from 1..n, each combination in increasing order.
Results sorted.
Example: n = 4, k = 2 -> [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
"""
from typing import List


# --- brute force ---
def brute_force(n: int, k: int) -> List[List[int]]:
    """Enumerate all 2^n bitmasks and keep those with exactly k bits set. O(n * 2^n); most masks have the wrong size."""
    res = []
    for mask in range(1 << n):
        if bin(mask).count("1") == k:
            res.append([i + 1 for i in range(n) if mask >> i & 1])
    return sorted(res)


# --- optimal ---
def solve(n: int, k: int) -> List[List[int]]:
    """Start-index template plus a size check: stop the loop once the numbers left cannot fill the path. O(k * C(n, k))."""
    res, path = [], []

    def backtrack(start: int) -> None:
        if len(path) == k:
            res.append(path[:])
            return
        for i in range(start, n + 1):
            if n - i + 1 < k - len(path):
                break
            path.append(i)
            backtrack(i + 1)
            path.pop()

    backtrack(1)
    return sorted(res)


# --- demo ---
def demo():
    return solve(4, 2)


# --- bugs ---
BUGS = [
    {
        "replace": "            if n - i + 1 < k - len(path):",
        "with":    "            if n - i < k - len(path):",
        "fix": "the numbers still available including i are n - i + 1, not n - i",
        "why": "Pruning one step too early drops every combination that ends at n: solve(4, 2) loses [3, 4], [2, 4] and [1, 4].",
        "decoys": [
            {"line": "        if len(path) == k:", "change": "should be >= k"},
            {"line": "        for i in range(start, n + 1):", "change": "should be range(start, n)"},
            {"line": "    backtrack(1)", "change": "should be backtrack(0)"},
        ],
    },
    {
        "replace": "            backtrack(i + 1)",
        "with":    "            backtrack(start + 1)",
        "fix": "the next number must come after the one just chosen: recurse from i + 1",
        "why": "From start + 1 a chosen number can be chosen again: solve(4, 2) produces [2, 2] and [3, 3].",
        "decoys": [
            {"line": "            path.append(i)", "change": "should append i + 1"},
            {"line": "            path.pop()", "change": "should be path.pop(0)"},
            {"line": "    return sorted(res)", "change": "should return res unsorted"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
