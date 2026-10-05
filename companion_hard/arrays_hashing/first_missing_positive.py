"""
First Missing Positive (LeetCode 41) - Hard
Chapter: arrays_hashing
Pattern: Index as hash (in-place cyclic placement)

Given an unsorted integer array nums, return the smallest positive integer that is
not in it, in O(n) time and O(1) extra space.
Example: [3, 4, -1, 1] -> 2.   [1, 2, 0] -> 3.   [7, 8, 9] -> 1.
"""


# --- brute force ---
def brute_force(nums):
    """Try 1, 2, 3, ... and scan the array for each candidate. O(n^2) time, O(1) space."""
    candidate = 1
    while candidate in nums:  # each test scans the whole array
        candidate += 1
    return candidate


# --- optimal ---
def first_missing_positive(nums):
    """Park value v at index v - 1, then find the first wrong slot. O(n) time, O(1) space."""
    n = len(nums)
    for i in range(n):
        # keep swapping until slot i holds an out-of-range value or a value already home
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            home = nums[i] - 1
            nums[i], nums[home] = nums[home], nums[i]
    for i in range(n):
        if nums[i] != i + 1:  # slot i should hold i + 1
            return i + 1
    return n + 1  # every value 1..n is present


# --- try the brute force ---
print(brute_force([1, 2, 0]))          # -> 3
print(brute_force([3, 4, -1, 1]))      # -> 2
print(brute_force([7, 8, 9, 11, 12]))  # -> 1
print(brute_force([1, 1]))             # -> 2


# --- try the optimal ---
print(first_missing_positive([1, 2, 0]))          # -> 3
print(first_missing_positive([3, 4, -1, 1]))      # -> 2
print(first_missing_positive([7, 8, 9, 11, 12]))  # -> 1
print(first_missing_positive([1, 1]))             # -> 2
