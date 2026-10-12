"""
Prefix Sum + Hash Map - Subarray Sum Equals K

Given an array of integers (negatives allowed) and an integer k, count the
contiguous subarrays whose sum is exactly k:
[2, -1, 1, 2], k 2 -> 4.
"""


# --- algorithm ---
def subarray_sum(nums, k):
    """Count earlier prefix sums equal to prefix - k. O(n) time and space."""
    prefix_count = {}               # prefix sum -> how many times seen
    prefix_count[0] = 1             # the empty prefix, before index 0
    prefix = 0
    total = 0
    for x in nums:
        prefix += x                 # sum of nums up to and including x
        # each earlier prefix equal to prefix - k starts one subarray of sum k
        total += prefix_count.get(prefix - k, 0)
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1   # record last
    return total


# --- try it ---
print(subarray_sum([2, -1, 1, 2], 2))   # -> 4
print(subarray_sum([1, 1, 1], 2))       # -> 2
print(subarray_sum([1, 2, 3], 3))       # -> 2
print(subarray_sum([0, 0, 0], 0))       # -> 6
