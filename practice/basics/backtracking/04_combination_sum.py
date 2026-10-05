"""
Combination Sum (LeetCode 39) - Basics
Area: backtracking
Key operations: sort candidates, choose cands[i], recurse from i (reuse allowed), prune when cands[i] > remaining, unchoose

Given distinct positive candidates and a target, return every combination (with unlimited reuse of
each candidate) whose sum is the target. Each combination is non-decreasing; results sorted.
Example: candidates [2, 3, 6, 7], target 7 -> [[2, 2, 3], [7]]
"""
from itertools import combinations_with_replacement
from typing import List


# --- brute force ---
def brute_force(candidates: List[int], target: int) -> List[List[int]]:
    """For every size r up to target // min, enumerate all multisets of size r and keep those summing to target. Exponential; sums are never pruned."""
    cands = sorted(candidates)
    res = []
    for r in range(target // cands[0] + 1):
        for combo in combinations_with_replacement(cands, r):
            if sum(combo) == target:
                res.append(list(combo))
    return sorted(res)


# --- optimal ---
def solve(candidates: List[int], target: int) -> List[List[int]]:
    """Sorted candidates; recurse from i (not i + 1) to allow reuse; break once a candidate exceeds what remains. O(branches * target)."""
    cands = sorted(candidates)
    res, path = [], []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(cands)):
            if cands[i] > remaining:
                break
            path.append(cands[i])
            backtrack(i, remaining - cands[i])
            path.pop()

    backtrack(0, target)
    return sorted(res)


# --- demo ---
def demo():
    return solve([2, 3, 6, 7], 7)


# --- bugs ---
BUGS = [
    {
        "replace": "            backtrack(i, remaining - cands[i])",
        "with":    "            backtrack(i + 1, remaining - cands[i])",
        "fix": "pass i, not i + 1: the same candidate may be used again",
        "why": "With i + 1 every candidate is used at most once, so [2, 3, 6, 7] with target 7 loses [2, 2, 3] and returns only [7].",
        "decoys": [
            {"line": "            if cands[i] > remaining:", "change": "should be >="},
            {"line": "        for i in range(start, len(cands)):", "change": "should start from 0"},
            {"line": "    backtrack(0, target)", "change": "should be backtrack(1, target)"},
        ],
    },
    {
        "replace": "            if cands[i] > remaining:",
        "with":    "            if cands[i] >= remaining:",
        "fix": "a candidate equal to the remaining sum is exactly the one that completes a combination; prune only when strictly greater",
        "why": "The exact fit is pruned away, so remaining never reaches 0 and the answer is always empty.",
        "decoys": [
            {"line": "        if remaining == 0:", "change": "should be remaining <= 0"},
            {"line": "            path.append(cands[i])", "change": "should append i"},
            {"line": "    cands = sorted(candidates)", "change": "sorting is unnecessary here"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
