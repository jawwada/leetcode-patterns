"""
Find Peak Element - Binary Search Uphill

Given an array in which no two neighbors are equal, return the index of a
peak, a value larger than both neighbors, where the positions just outside
the array count as -infinity. Any peak will do:
[1, 2, 1, 3, 5, 6, 4] -> 5 (index 1 would be valid too).
"""


# --- algorithm ---
def find_peak_element(nums):
    """Climb toward the higher of nums[mid] and nums[mid + 1]: a peak lies
    that way, so half the range can go. O(log n) time, O(1) space."""
    lo = 0
    hi = len(nums) - 1              # closed window [lo, hi] holds a peak
    while lo < hi:
        mid = (lo + hi) // 2        # mid < hi, so nums[mid + 1] exists
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1            # rising: a peak lies right of mid
        else:
            hi = mid                # falling: a peak at mid or left of it
    return lo


# --- try it ---
print(find_peak_element([1, 2, 1, 3, 5, 6, 4]))    # -> 5
print(find_peak_element([1, 2, 3, 1]))             # -> 2
print(find_peak_element([0, 2, 5, 9, 7, 3]))       # -> 3
print(find_peak_element([5, 4, 3]))                # -> 0
print(find_peak_element([7]))                      # -> 0
