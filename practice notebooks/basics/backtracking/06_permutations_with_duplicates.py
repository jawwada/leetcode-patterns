"""
Permutations With Duplicates (LeetCode 47) - Basics
Area: backtracking
Key operations: sort first, skip nums[i] == nums[i - 1] when used[i - 1] is False, mark used, choose, unmark and unchoose

Return every distinct ordering of an array that may contain duplicates. Sorting makes equal values
adjacent; among a run of equal values the recursion must take them left to right, so an equal value
whose left twin is not yet used is skipped on this level. Results sorted.
Example: [1, 1, 2] -> [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
"""
from itertools import permutations
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[List[int]]:
    """Generate all n! index permutations and drop duplicates with a set. O(n * n!); every duplicate ordering is built before being discarded."""
    return sorted(list(p) for p in set(permutations(nums)))


# --- optimal ---
def solve(nums: List[int]) -> List[List[int]]:
    """used[] flags plus one rule: an equal value may be chosen only after its left twin has been used. O(n * n!) worst case, no duplicates generated."""
    nums = sorted(nums)
    res, path = [], []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return sorted(res)


# --- demo ---
def demo():
    return solve([1, 1, 2])


# --- bugs ---
BUGS = [
    {
        "replace": "            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:",
        "with":    "            if i > 0 and nums[i] == nums[i - 1]:",
        "fix": "skip the duplicate only while its left twin is unused; once the twin is in the path this copy is legal",
        "why": "Skipping every non-first equal value means the second 1 can never follow the first: [1, 1, 2] returns no permutation containing both 1s.",
        "decoys": [
            {"line": "            if used[i]:", "change": "should be if not used[i]"},
            {"line": "            used[i] = False", "change": "should come before path.pop()"},
            {"line": "    backtrack()", "change": "should be backtrack(0)"},
        ],
    },
    {
        "replace": "    nums = sorted(nums)",
        "with":    "    nums = list(nums)",
        "fix": "sort first; the twin rule only sees duplicates that are adjacent",
        "why": "For [1, 2, 1] the two 1s are not neighbours, nothing is skipped, and [1, 2, 1] is reported twice.",
        "decoys": [
            {"line": "        for i in range(len(nums)):", "change": "should be range(len(path), len(nums))"},
            {"line": "            res.append(path[:])", "change": "should append path"},
            {"line": "    return sorted(res)", "change": "should be sorted(set(res))"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
