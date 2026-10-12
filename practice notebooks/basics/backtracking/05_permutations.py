"""
Permutations (LeetCode 46) - Basics
Area: backtracking
Key operations: mark used[i], choose nums[i], recurse with no start index, unmark and unchoose

Return every ordering of an array of distinct integers. Unlike subsets, every element is still a
candidate at every level, so a used[] flag per index says which ones are already in the path.
Results sorted.
Example: [1, 2, 3] -> [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
"""
from itertools import product
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[List[int]]:
    """Enumerate all n^n sequences over nums and keep those with no repeated element. O(n * n^n); almost all sequences are rejected."""
    n = len(nums)
    res = []
    for seq in product(nums, repeat=n):
        if len(set(seq)) == n:
            res.append(list(seq))
    return sorted(res)


# --- optimal ---
def solve(nums: List[int]) -> List[List[int]]:
    """Fill positions left to right; used[i] marks the elements already in the path. O(n * n!)."""
    res, path = [], []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
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
    return solve([1, 2, 3])


# --- bugs ---
BUGS = [
    {
        "replace": "        for i in range(len(nums)):",
        "with":    "        for i in range(len(path), len(nums)):",
        "fix": "permutations have no start index: every unused element is a candidate at every level",
        "why": "The subsets habit of starting after the current position loses every ordering that goes back: [1, 2, 3] never produces [2, 1, 3].",
        "decoys": [
            {"line": "            used[i] = True", "change": "should be set after the recursive call"},
            {"line": "            path.pop()", "change": "should be path.pop(0)"},
            {"line": "    used = [False] * len(nums)", "change": "should be [True] * len(nums)"},
        ],
    },
    {
        "replace": "        if len(path) == len(nums):",
        "with":    "        if len(path) == len(nums) - 1:",
        "fix": "a permutation is complete when the path holds all n elements",
        "why": "Recording one element early returns n-1 length prefixes: [1, 2, 3] gives [1, 2], [1, 3], [2, 1] and so on.",
        "decoys": [
            {"line": "            res.append(path[:])", "change": "should append path"},
            {"line": "            used[i] = False", "change": "should be removed; used is reset by the caller"},
            {"line": "    backtrack()", "change": "should be called once per element"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
