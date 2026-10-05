"""
Two Sum (LeetCode 1) - Easy
Chapter: arrays_hashing
Pattern: Hash map complement lookup

Given an integer array nums and an integer target, return the indices of the two
numbers that add up to target. Exactly one answer exists and you may not use the
same element twice.
Example: nums = [2, 7, 11, 15], target = 9 -> [0, 1] because 2 + 7 = 9.
"""


# --- brute force ---
def brute_force(nums, target):
    """Try every pair i < j. O(n^2) time, O(1) space."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# --- optimal ---
def two_sum(nums, target):
    """Remember each value's index; look up the complement. O(n) time, O(n) space."""
    seen = {}  # value -> index where we saw it
    for i in range(len(nums)):
        need = target - nums[i]
        if need in seen:
            return [seen[need], i]
        seen[nums[i]] = i  # insert after the lookup so an element never pairs with itself
    return []


# --- try the brute force ---
print(brute_force([2, 7, 11, 15], 9))        # -> [0, 1]
print(brute_force([3, 2, 4], 6))             # -> [1, 2]
print(brute_force([3, 3], 6))                # -> [0, 1]
print(brute_force([-1, -2, -3, -4, -5], -8))  # -> [2, 4]


# --- try the optimal ---
print(two_sum([2, 7, 11, 15], 9))        # -> [0, 1]
print(two_sum([3, 2, 4], 6))             # -> [1, 2]
print(two_sum([3, 3], 6))                # -> [0, 1]
print(two_sum([-1, -2, -3, -4, -5], -8))  # -> [2, 4]
