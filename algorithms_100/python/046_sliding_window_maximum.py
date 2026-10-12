"""
Sliding Window Maximum - Monotonic Deque

Given an array and a window size k, return the maximum of every window of k
consecutive values as the window slides from left to right:
[9, 7, 8, 3, 2, 5, 1], k 3 -> [9, 8, 8, 5, 5].
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def max_sliding_window(nums, k):
    """Deque of indices whose values decrease from front to back; the front
    is the window max. Each index enters and leaves once: O(n) time."""
    window = deque()                # indices of the candidates
    result = []
    for i in range(len(nums)):
        while len(window) > 0 and nums[window[-1]] <= nums[i]:
            window.pop()            # older and no larger: never needed again
        window.append(i)
        if window[0] <= i - k:
            window.popleft()        # the front slid out of the window
        if i >= k - 1:
            result.append(nums[window[0]])  # the front holds the window max
    return result


# --- try it ---
print(max_sliding_window([9, 7, 8, 3, 2, 5, 1], 3))    # -> [9, 8, 8, 5, 5]
nums = [1, 3, -1, -3, 5, 3, 6, 7]
print(max_sliding_window(nums, 3))                     # -> [3, 3, 5, 5, 6, 7]
print(max_sliding_window([4, 4, 4], 2))                # -> [4, 4]
print(max_sliding_window([5], 1))                      # -> [5]
