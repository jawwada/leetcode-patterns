"""
Subarray Sum Equals K (LeetCode 560) - Medium
Area: arrays & hashing
Key operations: running prefix sum, count lookup of prefix - k, record the prefix in the count dict

Given an integer array nums (negatives and zeros allowed) and an integer k, return the number of
contiguous subarrays whose elements sum to k.
Example: nums = [1, 2, 3, -3, 3], k = 3 -> 5 ([1,2], [1,2,3,-3], [3], [3,-3,3] and the last [3])
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int], k: int) -> int:
    """For every start extend the end, accumulating the sum. O(n^2): the sum of nums[i..j] is rebuilt
    for every start i although it is just prefix[j + 1] - prefix[i], two numbers known in advance."""
    n = len(nums)
    answer = 0
    for i in range(n):
        running = 0
        for j in range(i, n):
            running += nums[j]
            if running == k:
                answer += 1
    return answer


# --- optimal ---
def solve(nums: List[int], k: int) -> int:
    """sum(i..j) == k means prefix[j + 1] - prefix[i] == k. Sweep j with a running prefix and a dict
    counting every earlier prefix: add how many of them equal prefix - k. O(n) time, O(n) space."""
    counts = {0: 1}  # prefix sum -> how many prefixes had it; the empty prefix counts once
    prefix = 0
    answer = 0
    for i, v in enumerate(nums):
        prefix += v
        answer += counts.get(prefix - k, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer


# --- demo ---
def demo():
    nums, k = [1, 2, 3, -3, 3], 3
    return solve(nums, k)


# --- bugs ---
BUGS = [
    {
        "replace": "    counts = {0: 1}  # prefix sum -> how many prefixes had it; the empty prefix counts once",
        "with":    "    counts = {}  # prefix sum -> how many prefixes had it; the empty prefix counts once",
        "fix": "seed with {0: 1} for the empty prefix",
        "why": "Without the seed, subarrays that start at index 0 are never counted: [1, 1, 1] with k = 2 returns 1 instead of 2.",
        "decoys": [
            {"line": "    prefix = 0", "change": "should start at nums[0]"},
            {"line": "        answer += counts.get(prefix - k, 0)", "change": "should add 1 when prefix - k is in counts"},
            {"line": "        counts[prefix] = counts.get(prefix, 0) + 1", "change": "should run before the answer update"},
        ],
    },
    {
        "replace": "        answer += counts.get(prefix - k, 0)",
        "with":    "        answer += counts.get(k - prefix, 0)",
        "fix": "look up prefix - k, not k - prefix",
        "why": "k - prefix is the wrong difference, so [1, 2, 3, -3, 3] with k = 3 returns 2 instead of 5.",
        "decoys": [
            {"line": "        prefix += v", "change": "should assign prefix = v"},
            {"line": "    counts = {0: 1}  # prefix sum -> how many prefixes had it; the empty prefix counts once", "change": "should start as {0: 0}"},
            {"line": "    return answer", "change": "should return answer - 1"},
        ],
    },
    {
        "replace": "        counts[prefix] = counts.get(prefix, 0) + 1",
        "with":    "        counts[prefix] = 1",
        "fix": "increment the count, the same prefix can repeat",
        "why": "Repeated prefix sums are counted once, so [1, 2, 3, -3, 3] with k = 3 (prefix 3 appears twice) returns 4 instead of 5.",
        "decoys": [
            {"line": "    answer = 0", "change": "should start at counts[0]"},
            {"line": "    for i, v in enumerate(nums):", "change": "should enumerate from 1"},
            {"line": "        answer += counts.get(prefix - k, 0)", "change": "should be counts.get(prefix, 0)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
