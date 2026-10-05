"""
Maximum Average Subarray II (LeetCode 644) - Hard
Chapter: binary_search
Pattern: Binary search on the answer

Given an integer array nums and an integer k, find a contiguous subarray of length at least k
with the largest average and return that average; any answer within 1e-5 is accepted.
Example: nums = [1, 12, -5, -6, 50, 3], k = 4 -> 12.75 (the average of [12, -5, -6, 50])
"""
import math                            # math.inf is a number bigger than everything


# --- brute force ---
def brute_force(nums, k):
    """Average every subarray of length >= k and keep the best. O(n^2) time."""
    best = -math.inf
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):
            total += nums[end]
            length = end - start + 1
            if length >= k:
                best = max(best, total / length)
    return best


# --- optimal ---
def has_average_at_least(nums, k, x):
    """Is there a subarray of length >= k with average >= x? O(n) time."""
    prefix = [0.0]                            # prefix sums of (value - x)
    for value in nums:
        prefix.append(prefix[-1] + value - x)
    smallest_before = 0.0                     # min of prefix[0 .. end - k]
    for end in range(k, len(nums) + 1):
        smallest_before = min(smallest_before, prefix[end - k])
        if prefix[end] - smallest_before >= 0:
            return True                       # that stretch has sum of (value - x) >= 0
    return False


def maximum_average_subarray(nums, k):
    """Binary search the average over the real line until the gap is tiny. O(n log(R / eps))."""
    left = float(min(nums))
    right = float(max(nums))
    while right - left > 1e-6:
        mid = (left + right) / 2
        if has_average_at_least(nums, k, mid):
            left = mid                        # mid is reachable: look higher
        else:
            right = mid                       # nobody reaches mid: look lower
    return left


# --- try the brute force ---
print(round(brute_force([1, 12, -5, -6, 50, 3], 4), 5))   # -> 12.75
print(round(brute_force([5], 1), 5))                      # -> 5.0
print(round(brute_force([-1, -2, -3], 2), 5))             # -> -1.5
print(round(brute_force([4, 4, 4, 4], 2), 5))             # -> 4.0


# --- try the optimal ---
print(round(maximum_average_subarray([1, 12, -5, -6, 50, 3], 4), 5))   # -> 12.75
print(round(maximum_average_subarray([5], 1), 5))                      # -> 5.0
print(round(maximum_average_subarray([-1, -2, -3], 2), 5))             # -> -1.5
print(round(maximum_average_subarray([4, 4, 4, 4], 2), 5))             # -> 4.0
