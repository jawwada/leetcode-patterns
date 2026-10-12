"""
Two Sum (LeetCode 1) - Medium
Area: arrays & hashing
Key operations: compute the complement, look it up in a dict, insert after the check, return indices

Given an unsorted array of integers and a target, return the indices of the two numbers that add up
to the target. Exactly one answer exists and an element may not be used twice.
Example: nums = [3, 5, 2, 7, 11], target = 9 -> [2, 3] because nums[2] + nums[3] = 2 + 7 = 9
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int], target: int) -> List[int]:
    """Try every pair i < j. O(n^2): for a fixed nums[i] the one value we want is already known
    (target - nums[i]), yet the whole suffix is rescanned to find it."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# --- optimal ---
def solve(nums: List[int], target: int) -> List[int]:
    """One pass with a dict value -> index of every number seen so far: ask whether the complement
    is already there, then insert the current number. O(n) time, O(n) space."""
    seen = {}  # value -> index of an earlier element
    for i in range(len(nums)):
        v = nums[i]
        need = target - v
        if need in seen:
            return [seen[need], i]
        seen[v] = i  # insert after the check so v cannot pair with itself
    return []


# --- demo ---
def demo():
    nums, target = [3, 5, 2, 7, 11], 9
    return solve(nums, target)


# --- bugs ---
BUGS = [
    {
        "replace": "        need = target - v",
        "with":    "        need = v - target",
        "fix": "the complement is target - v",
        "why": "With v - target the lookup asks for the wrong partner; on [3, 5, 2, 7, 11] with target 9 it pairs 11 with the earlier 2 (need 11 - 9 = 2) and returns [2, 4], whose sum is 13.",
        "decoys": [
            {"line": "        if need in seen:", "change": "should test need in nums"},
            {"line": "        seen[v] = i  # insert after the check so v cannot pair with itself", "change": "should run before the if"},
            {"line": "    return []", "change": "should return [-1, -1]"},
        ],
    },
    {
        "replace": "            return [seen[need], i]",
        "with":    "            return [need, v]",
        "fix": "return the indices seen[need] and i",
        "why": "The problem asks for positions; returning the values gives [2, 7] for the docstring example instead of [2, 3], and the values may not even be valid indices.",
        "decoys": [
            {"line": "        need = target - v", "change": "should be target + v"},
            {"line": "    seen = {}  # value -> index of an earlier element", "change": "should be a set of values"},
            {"line": "        v = nums[i]", "change": "should be nums[i + 1]"},
        ],
    },
    {
        "replace": "        seen[v] = i  # insert after the check so v cannot pair with itself",
        "with":    "        seen[i] = v  # insert after the check so v cannot pair with itself",
        "fix": "key is the value v, stored value is the index i",
        "why": "With index -> value the lookup 'need in seen' tests indices instead of numbers, so [2, 7, 11, 15] with target 9 never finds 2 and returns [].",
        "decoys": [
            {"line": "        if need in seen:", "change": "should be if need in seen and seen[need] != i"},
            {"line": "            return [seen[need], i]", "change": "should be [i, seen[need]]"},
            {"line": "    for i in range(len(nums)):", "change": "should start the loop at index 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
