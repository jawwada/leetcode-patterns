"""
Subsets With Duplicates (LeetCode 90) - Basics
Area: backtracking
Key operations: sort first, skip nums[i] == nums[i - 1] when i > start, choose, recurse from i + 1, unchoose

Return every distinct subset of an array that may contain duplicates. Sorting puts equal values side
by side; on one level of the tree only the first of a run of equal values may be chosen. Results sorted.
Example: [1, 2, 2] -> [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int]) -> List[List[int]]:
    """Enumerate all 2^n bitmasks, sort each subset, drop duplicates with a set. O(n log n * 2^n); builds every duplicate before discarding it."""
    seen = set()
    for mask in range(1 << len(nums)):
        seen.add(tuple(sorted(x for i, x in enumerate(nums) if mask >> i & 1)))
    return sorted(list(t) for t in seen)


# --- optimal ---
def solve(nums: List[int]) -> List[List[int]]:
    """Sort, then the start-index template with one rule: on a level, take only the first of equal values. O(n * 2^n)."""
    nums = sorted(nums)
    res, path = [], []

    def backtrack(start: int) -> None:
        res.append(path[:])
        log("  " * len(path) + f"record {path}")
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                log("  " * (len(path) + 1) + f"skip {nums[i]} at i={i}: equal to nums[{i - 1}] on this level")
                continue
            path.append(nums[i])
            log("  " * len(path) + f"choose {nums[i]} -> path {path}")
            backtrack(i + 1)
            path.pop()
            log("  " * (len(path) + 1) + f"unchoose {nums[i]} -> path {path}")

    backtrack(0)
    return sorted(res)


# --- demo ---
def demo():
    return solve([1, 2, 2])


# --- tests ---
def tests():
    assert solve([1, 2, 2]) == [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    assert solve([2, 1, 2]) == [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]  # unsorted input
    assert solve([1, 1, 1]) == [[], [1], [1, 1], [1, 1, 1]]
    assert solve([]) == [[]]
    assert solve([4]) == [[], [4]]
    import random
    rng = random.Random(0)
    for _ in range(200):
        a = [rng.randint(1, 3) for _ in range(rng.randint(0, 6))]
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "            if i > start and nums[i] == nums[i - 1]:",
        "with":    "            if i > 0 and nums[i] == nums[i - 1]:",
        "fix": "skip a duplicate only when it is not the first candidate of this level: i > start",
        "why": "With i > 0 the second 2 is also skipped when it is the first choice of a deeper level, so [1, 2, 2] loses [1, 2, 2] and [2, 2].",
        "decoys": [
            {"line": "            backtrack(i + 1)", "change": "should be backtrack(start + 1)"},
            {"line": "        res.append(path[:])", "change": "should append only when len(path) > 0"},
            {"line": "    return sorted(res)", "change": "should be sorted(set(res))"},
        ],
    },
    {
        "replace": "    nums = sorted(nums)",
        "with":    "    nums = list(nums)",
        "fix": "sort first; the skip rule only works when equal values are adjacent",
        "why": "Without sorting, [2, 1, 2] has its 2s apart, the rule never fires, and [2] and [1, 2] appear twice.",
        "decoys": [
            {"line": "        for i in range(start, len(nums)):", "change": "should be range(start + 1, len(nums))"},
            {"line": "            path.pop()", "change": "should be path.pop(0)"},
            {"line": "    backtrack(0)", "change": "should be backtrack(1)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
