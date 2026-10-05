"""
Subarrays with K Different Integers (LeetCode 992) - Hard
Chapter: sliding_window
Pattern: Exactly-K = atMost(K) - atMost(K-1)

Given an integer array nums and an integer k, count the contiguous subarrays whose number
of distinct values is exactly k.
Example: nums = [1, 2, 1, 2, 3], k = 2 -> 7 ([1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2],
[1,2,1,2]).
"""


# --- brute force ---
def brute_force(nums, k):
    """From every start, extend right with a set of values seen. O(n^2) time, O(k) space."""
    count = 0
    for start in range(len(nums)):
        seen = set()                            # rebuilt for every start
        for end in range(start, len(nums)):
            seen.add(nums[end])
            if len(seen) > k:                   # more values can only add distinct ones
                break
            if len(seen) == k:
                count += 1
    return count


# --- optimal ---
def at_most(nums, limit):
    """Count subarrays with at most `limit` distinct values with one window. O(n) time."""
    counts = {}                                 # value -> copies inside the window
    left = 0
    total = 0
    for right in range(len(nums)):
        value = nums[right]
        counts[value] = counts.get(value, 0) + 1
        while len(counts) > limit:              # too many distinct values: shrink from the left
            counts[nums[left]] -= 1
            if counts[nums[left]] == 0:
                del counts[nums[left]]          # gone from the window, so not distinct any more
            left += 1
        total += right - left + 1               # every start in [left, right] works
    return total


def subarrays_with_k_distinct(nums, k):
    """exactly(k) = atMost(k) - atMost(k - 1), two linear passes. O(n) time, O(k) space."""
    return at_most(nums, k) - at_most(nums, k - 1)


# --- try the brute force ---
print(brute_force([1, 2, 1, 2, 3], 2))   # -> 7
print(brute_force([1, 2, 1, 3, 4], 3))   # -> 3
print(brute_force([1, 1, 1], 1))         # -> 6
print(brute_force([1, 2, 3], 4))         # -> 0


# --- try the optimal ---
print(subarrays_with_k_distinct([1, 2, 1, 2, 3], 2))   # -> 7
print(subarrays_with_k_distinct([1, 2, 1, 3, 4], 3))   # -> 3
print(subarrays_with_k_distinct([1, 1, 1], 1))         # -> 6
print(subarrays_with_k_distinct([1, 2, 3], 4))         # -> 0
