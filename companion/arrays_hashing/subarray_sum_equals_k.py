"""
Subarray Sum Equals K (LeetCode 560) - Medium
Chapter: arrays_hashing
Pattern: Prefix sum + hash map of counts

Given an integer array nums (which may contain negatives and zeros) and an integer
k, return the number of contiguous subarrays whose elements sum to k.
Example: nums = [1, 1, 1], k = 2 -> 2 (the subarrays at indices 0..1 and 1..2).
"""


# --- brute force ---
def brute_force(nums, k):
    """For every start, extend the end and keep a running sum. O(n^2) time, O(1) space."""
    n = len(nums)
    answer = 0
    for start in range(n):
        running = 0
        for end in range(start, n):
            running += nums[end]
            if running == k:
                answer += 1
    return answer


# --- optimal ---
def subarray_sum(nums, k):
    """Count earlier prefix sums equal to prefix - k. O(n) time, O(n) space."""
    counts = {0: 1}  # prefix sum -> times seen; the empty prefix counts once
    prefix = 0
    answer = 0
    for value in nums:
        prefix += value
        answer += counts.get(prefix - k, 0)  # each earlier prefix at prefix - k ends a k-sum here
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer


# --- try the brute force ---
print(brute_force([1, 1, 1], 2))       # -> 2
print(brute_force([1, 2, 3], 3))       # -> 2
print(brute_force([1, -1, 0], 0))      # -> 3
print(brute_force([0, 0, 0, 0], 0))    # -> 10


# --- try the optimal ---
print(subarray_sum([1, 1, 1], 2))       # -> 2
print(subarray_sum([1, 2, 3], 3))       # -> 2
print(subarray_sum([1, -1, 0], 0))      # -> 3
print(subarray_sum([0, 0, 0, 0], 0))    # -> 10
