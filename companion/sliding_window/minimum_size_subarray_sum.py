"""
Minimum Size Subarray Sum (LeetCode 209) - Medium
Chapter: sliding_window
Pattern: Variable-size sliding window

Given an array of positive integers nums and a target, return the smallest length of a
contiguous subarray whose sum is >= target, or 0 if no such subarray exists.
Example: target = 7, nums = [2, 3, 1, 2, 4, 3] -> 2 (the subarray [4, 3]).
"""


# --- brute force ---
def brute_force(target, nums):
    """For every start, add to the right until the sum reaches target. O(n^2) time, O(1) space."""
    best = 0
    for start in range(len(nums)):
        total = 0                                   # re-summed from scratch for every start
        for end in range(start, len(nums)):
            total += nums[end]
            if total >= target:
                length = end - start + 1
                if best == 0 or length < best:
                    best = length
                break
    return best


# --- optimal ---
def min_sub_array_len(target, nums):
    """Grow right until heavy enough, then trim left while still heavy. O(n) time, O(1) space."""
    left = 0
    total = 0
    best = 0
    for right in range(len(nums)):
        total += nums[right]
        while total >= target:                      # valid window: record it, then try shorter
            length = right - left + 1
            if best == 0 or length < best:
                best = length
            total -= nums[left]                     # drop the left element instead of re-summing
            left += 1
    return best


# --- try the brute force ---
print(brute_force(7, [2, 3, 1, 2, 4, 3]))                # -> 2
print(brute_force(4, [1, 4, 4]))                         # -> 1
print(brute_force(11, [1, 1, 1, 1, 1, 1, 1, 1]))         # -> 0
print(brute_force(15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8]))  # -> 2


# --- try the optimal ---
print(min_sub_array_len(7, [2, 3, 1, 2, 4, 3]))                # -> 2
print(min_sub_array_len(4, [1, 4, 4]))                         # -> 1
print(min_sub_array_len(11, [1, 1, 1, 1, 1, 1, 1, 1]))         # -> 0
print(min_sub_array_len(15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8]))  # -> 2
