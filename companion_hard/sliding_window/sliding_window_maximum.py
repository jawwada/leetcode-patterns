"""
Sliding Window Maximum (LeetCode 239) - Hard
Chapter: sliding_window
Pattern: Monotonic deque

Given nums and a window size k, return the maximum of every contiguous window of size k
from left to right.
Example: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3 -> [3, 3, 5, 5, 6, 7].
"""
from collections import deque       # pop from both ends in O(1)


# --- brute force ---
def brute_force(nums, k):
    """Rescan all k values of every window. O(n * k) time, O(1) extra space."""
    out = []
    for start in range(len(nums) - k + 1):
        biggest = nums[start]
        for j in range(start + 1, start + k):   # k - 1 of these were scanned last time too
            if nums[j] > biggest:
                biggest = nums[j]
        out.append(biggest)
    return out


# --- optimal ---
def max_sliding_window(nums, k):
    """Deque of indices whose values decrease; the front is the max. O(n) time, O(k) space."""
    candidates = deque()                        # indices; values strictly decrease front to back
    out = []
    for i in range(len(nums)):
        while candidates and nums[candidates[-1]] <= nums[i]:
            candidates.pop()                    # smaller and older: never a maximum again
        candidates.append(i)
        if candidates[0] <= i - k:              # the front slid out of the window
            candidates.popleft()
        if i >= k - 1:                          # the first full window ends at k - 1
            out.append(nums[candidates[0]])
    return out


# --- try the brute force ---
print(brute_force([1, 3, -1, -3, 5, 3, 6, 7], 3))   # -> [3, 3, 5, 5, 6, 7]
print(brute_force([1], 1))                          # -> [1]
print(brute_force([9, 8, 7, 6], 2))                 # -> [9, 8, 7]
print(brute_force([4, 4, 4], 2))                    # -> [4, 4]


# --- try the optimal ---
print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))   # -> [3, 3, 5, 5, 6, 7]
print(max_sliding_window([1], 1))                          # -> [1]
print(max_sliding_window([9, 8, 7, 6], 2))                 # -> [9, 8, 7]
print(max_sliding_window([4, 4, 4], 2))                    # -> [4, 4]
