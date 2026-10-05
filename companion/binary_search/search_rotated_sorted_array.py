"""
Search in Rotated Sorted Array (LeetCode 33) - Medium
Chapter: binary_search
Pattern: Binary search on a rotated sorted array

A sorted array of distinct integers was rotated at an unknown pivot. Return the index of
target, or -1 if it is absent, in O(log n) time.
Example: nums = [4, 5, 6, 7, 0, 1, 2], target = 0 -> 4; target = 3 -> -1
"""


# --- brute force ---
def brute_force(nums, target):
    """Check every index. O(n) time, O(1) space."""
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1


# --- optimal ---
def search_rotated_sorted_array(nums, target):
    """One half of [left, right] is always sorted; test target against it. O(log n), O(1)."""
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:                          # left half [left, mid] is sorted
            if nums[left] <= target and target < nums[mid]:
                right = mid - 1                              # target fits in the sorted half
            else:
                left = mid + 1                               # so it must be in the other half
        else:                                                # right half [mid, right] is sorted
            if nums[mid] < target and target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


# --- try the brute force ---
print(brute_force([4, 5, 6, 7, 0, 1, 2], 0))   # -> 4
print(brute_force([4, 5, 6, 7, 0, 1, 2], 3))   # -> -1
print(brute_force([3, 1], 1))                  # -> 1
print(brute_force([5, 1, 3], 5))               # -> 0


# --- try the optimal ---
print(search_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 0))   # -> 4
print(search_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 3))   # -> -1
print(search_rotated_sorted_array([3, 1], 1))                  # -> 1
print(search_rotated_sorted_array([5, 1, 3], 5))               # -> 0
