"""
Sliding Window Maximum (LeetCode 239)
Return the maximum of every window of size k as it slides across nums.
  nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3  ->  [3, 3, 5, 5, 6, 7]

Idea: keep a deque of indices whose values decrease front to back, so the front
      is always the window max. A new value kicks out smaller ones from the back;
      the front is dropped once it slides out of the window.

Pseudocode:
  dq = deque()                    # indices, values decreasing
  for i, x in nums:
      pop back while nums[back] <= x
      push i
      pop front if it left the window (dq[0] <= i - k)
      if window is full: output nums[dq[0]]

Time O(n), space O(k).
"""
from collections import deque


def max_sliding_window(nums, k):
    dq = deque()                         # indices, values decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:  # smaller values can never be max again
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:               # front slid out of the window
            dq.popleft()
        if i >= k - 1:                   # window is full
            out.append(nums[dq[0]])
    return out


if __name__ == "__main__":
    print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3, 3, 5, 5, 6, 7]
    print(max_sliding_window([1], 1))                          # [1]
    print(max_sliding_window([9, 8, 7, 6], 2))                 # [9, 8, 7]
