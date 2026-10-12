"""
Minimum Size Subarray Sum - Shrink While the Sum Is Enough

Given an array of positive integers and a positive target, return the length
of the shortest contiguous subarray whose sum is at least the target, or 0 if
there is none: [2, 3, 1, 2, 4, 3], target 7 -> 2 (the subarray [4, 3]).
"""


# --- algorithm ---
def min_subarray_len(nums, target):
    """Grow the window on the right; while its sum reaches the target, record
    its length and shrink it from the left. O(n) time, O(1) space."""
    left = 0
    window_sum = 0                  # sum of nums[left..right]
    best = len(nums) + 1            # longer than any real window
    for right in range(len(nums)):
        window_sum += nums[right]           # expand: take one more value
        while window_sum >= target:         # enough: record, then shrink
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1
    if best > len(nums):
        return 0                    # no window ever reached the target
    return best


# --- try it ---
print(min_subarray_len([2, 3, 1, 2, 4, 3], 7))      # -> 2
print(min_subarray_len([1, 4, 4], 4))               # -> 1
print(min_subarray_len([1, 1, 1, 1, 7], 7))         # -> 1
print(min_subarray_len([1, 1, 1, 1, 1], 11))        # -> 0
print(min_subarray_len([], 3))                      # -> 0
