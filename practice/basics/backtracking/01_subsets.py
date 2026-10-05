"""
Subsets (LeetCode 78) - Basics
Area: backtracking
Key operations: record the path, choose nums[i], recurse from i + 1, unchoose

Return every subset (the power set) of an array of distinct integers. Results are sorted so the
output is deterministic.
Example: [1, 2, 3] -> [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int]) -> List[List[int]]:
    """Enumerate all 2^n bitmasks and keep the elements whose bit is set. O(n * 2^n); no tree, no pruning possible."""
    res = []
    for mask in range(1 << len(nums)):
        res.append([x for i, x in enumerate(nums) if mask >> i & 1])
    return sorted(res)


# --- optimal ---
def solve(nums: List[int]) -> List[List[int]]:
    """Start-index template: every node of the recursion tree is a subset; branch on each i >= start. O(n * 2^n)."""
    res, path = [], []

    def backtrack(start: int) -> None:
        res.append(path[:])
        log("  " * len(path) + f"record {path}")
        for i in range(start, len(nums)):
            path.append(nums[i])
            log("  " * len(path) + f"choose {nums[i]} -> path {path}")
            backtrack(i + 1)
            path.pop()
            log("  " * (len(path) + 1) + f"unchoose {nums[i]} -> path {path}")

    backtrack(0)
    return sorted(res)


# --- demo ---
def demo():
    return solve([1, 2, 3])


# --- tests ---
def tests():
    assert solve([1, 2, 3]) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert solve([]) == [[]]
    assert solve([7]) == [[], [7]]
    assert solve([3, 1]) == [[], [1], [3], [3, 1]]  # unsorted input is fine: subsets keep input order
    import random
    rng = random.Random(0)
    for _ in range(200):
        a = rng.sample(range(1, 10), rng.randint(0, 6))
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "            backtrack(i + 1)",
        "with":    "            backtrack(start + 1)",
        "fix": "recurse from i + 1 so the next choice comes after the element just chosen",
        "why": "Recursing from start + 1 lets an element be chosen twice: [1, 2, 3] produces [1, 3, 3] and other non-subsets.",
        "decoys": [
            {"line": "        for i in range(start, len(nums)):", "change": "should be range(start + 1, len(nums))"},
            {"line": "            path.pop()", "change": "should be path.pop(0)"},
            {"line": "    backtrack(0)", "change": "should be backtrack(1)"},
        ],
    },
    {
        "replace": "        res.append(path[:])",
        "with":    "        res.append(path)",
        "fix": "append a copy (path[:]) because path keeps being mutated by later choose/unchoose steps",
        "why": "Every recorded subset is the same list object, which is empty again when the recursion finishes: the answer is eight empty lists.",
        "decoys": [
            {"line": "            path.append(nums[i])", "change": "should append i"},
            {"line": "    return sorted(res)", "change": "should return res unsorted"},
            {"line": "            backtrack(i + 1)", "change": "should be backtrack(i)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
