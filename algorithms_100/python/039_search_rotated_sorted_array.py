"""
Search in a Rotated Sorted Array - One Half Is Always Sorted

A sorted array of distinct values was rotated at an unknown pivot. Return the
index of the target, or -1 if it is absent, in O(log n) time:
[6, 7, 0, 1, 2, 4, 5], target 0 -> 2.
"""


# --- algorithm ---
def search_rotated(nums, target):
    """Binary search; the sorted half tells which side can hold the target.
    O(log n) time, O(1) space."""
    lo = 0
    hi = len(nums) - 1                          # closed window [lo, hi]
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:               # left half is sorted
            if nums[lo] <= target and target < nums[mid]:
                hi = mid - 1                    # target inside the left half
            else:
                lo = mid + 1                    # so it must be on the right
        else:                                   # right half is sorted
            if nums[mid] < target and target <= nums[hi]:
                lo = mid + 1                    # target inside the right half
            else:
                hi = mid - 1                    # so it must be on the left
    return -1


# --- try it ---
print(search_rotated([6, 7, 0, 1, 2, 4, 5], 0))     # -> 2
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))     # -> 4
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 3))     # -> -1
print(search_rotated([3, 1], 1))                    # -> 1
