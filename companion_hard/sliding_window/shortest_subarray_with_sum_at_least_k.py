"""
Shortest Subarray with Sum at Least K (LeetCode 862) - Hard
Chapter: sliding_window
Pattern: Monotonic deque

Given an integer array nums whose values may be negative and an integer k, return the
length of the shortest non-empty contiguous subarray with sum >= k, or -1 if none exists.
Example: nums = [2, -1, 2], k = 3 -> 3 (only the whole array reaches 3); nums = [1, 2],
k = 4 -> -1.
"""
import math                         # math.inf is "longer than any subarray"
from collections import deque       # pop from both ends in O(1)


# --- brute force ---
def brute_force(nums, k):
    """Running sum from every start; negatives mean no early stop. O(n^2) time, O(1) space."""
    best = math.inf
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):     # a later negative may be undone, so scan on
            total += nums[end]
            if total >= k and end - start + 1 < best:
                best = end - start + 1
    if best == math.inf:
        return -1
    return best


# --- optimal ---
def shortest_subarray(nums, k):
    """Prefix sums plus a deque of starts with increasing sums. O(n) time, O(n) space."""
    prefix = [0]                                # prefix[j] = sum of the first j values
    for x in nums:
        prefix.append(prefix[-1] + x)
    best = math.inf
    starts = deque()                            # indices whose prefix sums strictly increase
    for j in range(len(prefix)):
        while starts and prefix[j] - prefix[starts[0]] >= k:
            best = min(best, j - starts[0])     # the front works; a later j is only longer
            starts.popleft()
        while starts and prefix[j] <= prefix[starts[-1]]:
            starts.pop()                        # farther away and no smaller: dominated by j
        starts.append(j)
    if best == math.inf:
        return -1
    return best


# --- try the brute force ---
print(brute_force([1], 1))                        # -> 1
print(brute_force([1, 2], 4))                     # -> -1
print(brute_force([2, -1, 2], 3))                 # -> 3
print(brute_force([84, -37, 32, 40, 95], 167))    # -> 3


# --- try the optimal ---
print(shortest_subarray([1], 1))                        # -> 1
print(shortest_subarray([1, 2], 4))                     # -> -1
print(shortest_subarray([2, -1, 2], 3))                 # -> 3
print(shortest_subarray([84, -37, 32, 40, 95], 167))    # -> 3
