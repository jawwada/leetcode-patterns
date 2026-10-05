"""
Contains Duplicate III (LeetCode 220) - Hard
Chapter: arrays_hashing
Pattern: Sliding window of value buckets

Given an integer array nums and two integers index_diff and value_diff, decide whether there
are two different indices i, j with |i - j| <= index_diff and |nums[i] - nums[j]| <= value_diff.
Example: nums = [1, 2, 3, 1], index_diff = 3, value_diff = 0 -> True (the two 1s are 3 apart).
         nums = [1, 5, 9, 1, 5, 9], index_diff = 2, value_diff = 3 -> False.
"""


# --- brute force ---
def brute_force(nums, index_diff, value_diff):
    """Compare each element with the next index_diff elements. O(n * k) time, O(1) space."""
    n = len(nums)
    for i in range(n):
        last = min(i + index_diff, n - 1)
        for j in range(i + 1, last + 1):
            if abs(nums[i] - nums[j]) <= value_diff:
                return True
    return False


# --- optimal ---
def contains_duplicate_iii(nums, index_diff, value_diff):
    """Buckets of width value_diff + 1 over the last index_diff values. O(n) time, O(k) space."""
    width = value_diff + 1  # two values in the same bucket differ by at most value_diff
    buckets = {}  # bucket id -> the single value stored in it
    for i in range(len(nums)):
        x = nums[i]
        b = x // width  # floor division keeps negatives correct
        if b in buckets:
            return True
        for neighbour in (b - 1, b + 1):  # close values can only be in adjacent buckets
            if neighbour in buckets and abs(buckets[neighbour] - x) <= value_diff:
                return True
        buckets[b] = x
        if i >= index_diff:  # keep only the last index_diff indices
            old = nums[i - index_diff]
            del buckets[old // width]
    return False


# --- try the brute force ---
print(brute_force([1, 2, 3, 1], 3, 0))         # -> True
print(brute_force([1, 5, 9, 1, 5, 9], 2, 3))   # -> False
print(brute_force([1, 0, 1, 1], 1, 2))         # -> True
print(brute_force([-3, 3], 2, 4))              # -> False


# --- try the optimal ---
print(contains_duplicate_iii([1, 2, 3, 1], 3, 0))         # -> True
print(contains_duplicate_iii([1, 5, 9, 1, 5, 9], 2, 3))   # -> False
print(contains_duplicate_iii([1, 0, 1, 1], 1, 2))         # -> True
print(contains_duplicate_iii([-3, 3], 2, 4))              # -> False
