"""
Combination Sum II (LeetCode 40) - Medium
Area: backtracking
Key operations: sort, break when candidate > remaining, skip a duplicate sibling (i > start), append / recurse from i + 1 / pop

Given candidates (values may repeat) and a target, return every unique combination whose sum is
target. Each index may be used at most once; two combinations are the same if they hold the same
values. Return the combinations sorted.
Example: candidates = [10, 1, 2, 7, 6, 1, 5], target = 8 -> [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
"""
from typing import List


# --- brute force ---
def brute_force(candidates: List[int], target: int) -> List[List[int]]:
    """Every index subset by bitmask, keep the ones summing to target, dedupe by sorted tuple.
    O(n * 2^n): subsets already past the target are still decoded and summed, and combinations that
    differ only in WHICH copy of a repeated value they use are generated apart and merged late."""
    n = len(candidates)
    seen = set()
    for mask in range(1 << n):
        chosen = sorted(candidates[i] for i in range(n) if mask >> i & 1)
        if sum(chosen) == target:
            seen.add(tuple(chosen))
    return sorted(list(t) for t in seen)


# --- optimal ---
def solve(candidates: List[int], target: int) -> List[List[int]]:
    """Sort, then DFS over indices: break once a candidate exceeds what is left (everything after it is
    bigger) and skip a value equal to its left sibling (same subtree). O(2^n) worst case, O(n) path."""
    nums = sorted(candidates)
    result, path = [], []

    def dfs(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:
                break
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            dfs(i + 1, remaining - nums[i])
            path.pop()

    dfs(0, target)
    return sorted(result)


# --- demo ---
def demo():
    return solve([10, 1, 2, 7, 6, 1, 5], 8)


# --- bugs ---
BUGS = [
    {
        "replace": "            dfs(i + 1, remaining - nums[i])",
        "with":    "            dfs(i, remaining - nums[i])",
        "fix": "recurse from i + 1: each index may be used at most once",
        "why": "Recursing from i lets the same index be picked again, so [2, 2] with target 6 returns [[2, 2, 2]] and the example gains combinations like [2, 2, 2, 2].",
        "decoys": [
            {"line": "            if nums[i] > remaining:", "change": "should be >= to prune one step earlier"},
            {"line": "                break", "change": "should be continue, a later candidate may still fit"},
            {"line": "    return sorted(result)", "change": "should return result without sorting"},
        ],
    },
    {
        "replace": "            if i > start and nums[i] == nums[i - 1]:",
        "with":    "            if i > 0 and nums[i] == nums[i - 1]:",
        "fix": "compare i with start: skip a duplicate only when it is a sibling at this level, not a child",
        "why": "With i > 0 the second 1 is skipped even when it follows the first 1 down the path, so the example loses [1, 1, 6].",
        "decoys": [
            {"line": "            path.append(nums[i])", "change": "should append the index i instead"},
            {"line": "    nums = sorted(candidates)", "change": "sorting is unnecessary, use candidates as given"},
            {"line": "        if remaining == 0:", "change": "should be remaining <= 0"},
        ],
    },
    {
        "replace": "            if nums[i] > remaining:",
        "with":    "            if nums[i] >= remaining:",
        "fix": "break only when the candidate is strictly larger: an exact fit completes a combination",
        "why": "A candidate equal to what is left is a solution; with >= the loop breaks before taking it, so [1, 7] and [2, 6] vanish from the example.",
        "decoys": [
            {"line": "            path.pop()", "change": "should pop only when remaining > 0"},
            {"line": "    dfs(0, target)", "change": "should start at dfs(1, target)"},
            {"line": "            result.append(path[:])", "change": "should append path itself, the copy is wasteful"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
