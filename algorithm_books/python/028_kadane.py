"""
Kadane's Algorithm - Maximum Subarray: Extend or Restart

Given a non-empty array of integers, return the largest sum of a contiguous
subarray together with its first and last index:
[-2, 1, -3, 4, -1, 2, 1, -5, 4] -> (6, 3, 6), the subarray [4, -1, 2, 1].
"""


# --- algorithm ---
def max_subarray(nums):
    """Extend the run ending here, or restart at x. O(n) time, O(1) space."""
    ending_here = nums[0]           # best sum of a subarray that ends at i
    start = 0                       # where that subarray begins
    best = nums[0]                  # not 0: all may be negative
    best_start = 0
    best_end = 0
    for i in range(1, len(nums)):
        if ending_here < 0:         # a negative run only drags x down: restart
            ending_here = nums[i]
            start = i
        else:
            ending_here = ending_here + nums[i]     # extend the run
        if ending_here > best:      # improved: copy the bounds
            best = ending_here
            best_start = start
            best_end = i
    return best, best_start, best_end


# --- try it ---
print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # -> (6, 3, 6)
print(max_subarray([5, 4, -1, 7, 8]))                  # -> (23, 0, 4)
print(max_subarray([-3, -1, -2]))                      # -> (-1, 1, 1)
print(max_subarray([7]))                               # -> (7, 0, 0)
