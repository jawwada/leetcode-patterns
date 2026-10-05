"""
Binary Search (LeetCode 704) - Easy
Chapter: binary_search
Pattern: Binary search on a sorted array

Given a sorted ascending array of distinct integers nums and a target, return the index of
target, or -1 if it is absent, in O(log n) time.
Example: nums = [-1, 0, 3, 5, 9, 12], target = 9 -> 4
"""


# --- brute force ---
def brute_force(nums, target):
    """Check every index from the left. O(n) time, O(1) space."""
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1


# --- optimal ---
def binary_search(nums, target):
    """Halve the candidate range [left, right] on every probe. O(log n) time, O(1) space."""
    left = 0
    right = len(nums) - 1
    while left <= right:               # if target exists it is inside [left, right]
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1             # everything up to mid is too small
        else:
            right = mid - 1            # everything from mid on is too big
    return -1


# --- try the brute force ---
print(brute_force([-1, 0, 3, 5, 9, 12], 9))   # -> 4
print(brute_force([-1, 0, 3, 5, 9, 12], 2))   # -> -1
print(brute_force([5], 5))                    # -> 0
print(brute_force([], 1))                     # -> -1


# --- try the optimal ---
print(binary_search([-1, 0, 3, 5, 9, 12], 9))   # -> 4
print(binary_search([-1, 0, 3, 5, 9, 12], 2))   # -> -1
print(binary_search([5], 5))                    # -> 0
print(binary_search([], 1))                     # -> -1
