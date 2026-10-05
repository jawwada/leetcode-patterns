"""
Combination Sum II (LeetCode 40) - Medium
Area: backtracking
Key operations: sort, break when candidate > remaining, skip a duplicate sibling (i > start), append / recurse from i + 1 / pop

Given candidates (values may repeat) and a target, return every unique combination whose sum is
target. Each index may be used at most once; two combinations are the same if they hold the same
values. Return the combinations sorted.
Example: candidates = [10, 1, 2, 7, 6, 1, 5], target = 8 -> [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
        log(f"{'  ' * len(path)}path {path} remaining {remaining} | choices {nums[start:]}")
        if remaining == 0:
            result.append(path[:])
            log(f"{'  ' * len(path)}  remaining 0: record {path}")
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:
                log(f"{'  ' * len(path)}  {nums[i]} > {remaining}: break, the rest are bigger")
                break
            if i > start and nums[i] == nums[i - 1]:
                log(f"{'  ' * len(path)}  skip nums[{i}] = {nums[i]}: same value as its left sibling")
                continue
            path.append(nums[i])
            dfs(i + 1, remaining - nums[i])
            path.pop()

    dfs(0, target)
    return sorted(result)


# --- demo ---
def demo():
    return solve([10, 1, 2, 7, 6, 1, 5], 8)


# --- tests ---
def tests():
    assert solve([10, 1, 2, 7, 6, 1, 5], 8) == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    assert solve([2, 5, 2, 1, 2], 5) == [[1, 2, 2], [5]]
    assert solve([2, 2], 5) == []                 # impossible
    assert solve([2, 2], 6) == []                 # no reuse of an index
    assert solve([1, 1, 1, 1], 4) == [[1, 1, 1, 1]]
    assert solve([1, 1, 1, 1], 2) == [[1, 1]]     # one copy, not six
    assert solve([], 3) == []
    assert solve([3], 3) == [[3]]
    original = [3, 1, 2]
    solve(original, 3)
    assert original == [3, 1, 2]                  # input not sorted in place
    import random
    for _ in range(200):
        cands = [random.randint(1, 6) for _ in range(random.randint(0, 7))]
        target = random.randint(1, 12)
        assert solve(cands, target) == brute_force(cands, target), (cands, target)


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
