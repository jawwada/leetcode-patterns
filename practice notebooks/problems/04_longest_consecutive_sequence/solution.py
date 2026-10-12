"""
Longest Consecutive Sequence (LeetCode 128) - Medium
Area: arrays & hashing
Key operations: put the values in a set, skip x when x - 1 is present, walk x, x+1, x+2, ... while present

Given an unsorted integer array, return the length of the longest run of consecutive integer values
(values, not positions) in O(n) time.
Example: nums = [100, 4, 200, 1, 3, 2] -> 4, the run 1, 2, 3, 4
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> int:
    """From every element count upward using list membership. O(n^3) worst case: each 'in nums' is
    a linear scan, and a run is re-walked from every one of its members, not just from its start."""
    best = 0
    for x in nums:
        length = 1
        while x + length in nums:
            length += 1
        best = max(best, length)
    return best


# --- optimal ---
def solve(nums: List[int]) -> int:
    """Set for O(1) membership; walk upward only from values x whose x - 1 is absent (run starts),
    so every value is stepped on by exactly one walk. O(n) time, O(n) space."""
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:
            continue
        length = 1
        while x + length in values:
            length += 1
        best = max(best, length)
    return best


# --- demo ---
def demo():
    return solve([100, 4, 200, 1, 3, 2])


# --- bugs ---
BUGS = [
    {
        "replace": "        if x - 1 in values:",
        "with":    "        if x + 1 in values:",
        "fix": "a run start has x - 1 absent, test x - 1",
        "why": "Testing x + 1 skips every value except the top of each run, and walking up from a top always stops at once, so [100, 4, 200, 1, 3, 2] returns 1.",
        "decoys": [
            {"line": "        while x + length in values:", "change": "should test x + length + 1"},
            {"line": "        length = 1", "change": "should start counting at 0"},
            {"line": "    values = set(nums)", "change": "should be sorted(set(nums))"},
        ],
    },
    {
        "replace": "        best = max(best, length)",
        "with":    "        best = length",
        "fix": "keep the maximum: best = max(best, length)",
        "why": "Without max, best is just the length of whichever run start the set happens to visit last, so a long run measured early is forgotten.",
        "decoys": [
            {"line": "            length += 1", "change": "should be length = x + length"},
            {"line": "        if x - 1 in values:", "change": "should test x - 1 in nums"},
            {"line": "    return best", "change": "should return best - 1"},
        ],
    },
    {
        "replace": "            continue",
        "with":    "            break",
        "fix": "continue: skip this x, do not end the search",
        "why": "break abandons the loop at the first value that is not a run start, so any run whose start comes later in the set is never measured: [1, 2, 10, 11, 12] can return 2 or 0.",
        "decoys": [
            {"line": "        while x + length in values:", "change": "should be while x + length in nums"},
            {"line": "    best = 0", "change": "should start best at 1"},
            {"line": "    for x in values:", "change": "should iterate over nums instead"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
