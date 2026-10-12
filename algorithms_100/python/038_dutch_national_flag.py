"""
Dutch National Flag - Three-Way Partition in One Pass

Given an array holding only 0s, 1s and 2s (three colors), sort it in place in
a single pass with O(1) extra space:
[2, 0, 2, 1, 1, 0] -> [0, 0, 1, 1, 2, 2].
"""


# --- algorithm ---
def sort_colors(nums):
    """Grow the 0s from the left and the 2s from the right; the 1s are left
    in the middle. One pass, O(n) time, O(1) space."""
    low = 0                         # nums[0..low-1] are 0s
    mid = 0                         # nums[low..mid-1] are 1s
    high = len(nums) - 1            # nums[high+1..n-1] are 2s
    while mid <= high:              # nums[mid..high] is still unseen
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1                # the block of 1s shifts right
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1               # mid stays: this value is unseen


# --- try it ---
colors = [2, 0, 2, 1, 1, 0]
sort_colors(colors)
print(colors)                       # -> [0, 0, 1, 1, 2, 2]
colors = [1, 2, 0]
sort_colors(colors)
print(colors)                       # -> [0, 1, 2]
colors = [2, 2, 0, 0]
sort_colors(colors)
print(colors)                       # -> [0, 0, 2, 2]
