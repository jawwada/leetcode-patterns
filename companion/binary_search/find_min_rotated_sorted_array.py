"""
Find Minimum in Rotated Sorted Array (LeetCode 153) - Medium
Chapter: binary_search
Pattern: Binary search on a rotated sorted array

A sorted array of distinct integers was rotated between 1 and n times, so [0, 1, 2, 4, 5, 6, 7]
may have become [4, 5, 6, 7, 0, 1, 2]. Return the minimum element in O(log n) time.
Example: nums = [3, 4, 5, 1, 2] -> 1
"""


# --- brute force ---
def brute_force(nums):
    """Keep the smallest value seen while scanning. O(n) time, O(1) space."""
    best = nums[0]
    for value in nums:
        if value < best:
            best = value
    return best


# --- optimal ---
def find_min_rotated_sorted_array(nums):
    """Compare mid with the right end to tell which run mid is on. O(log n) time, O(1) space."""
    left = 0
    right = len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1         # mid is on the high run: the drop is to the right of mid
        else:
            right = mid            # mid is on the low run: the minimum is mid or earlier
    return nums[left]


# --- try the brute force ---
print(brute_force([3, 4, 5, 1, 2]))          # -> 1
print(brute_force([4, 5, 6, 7, 0, 1, 2]))    # -> 0
print(brute_force([11, 13, 15, 17]))         # -> 11
print(brute_force([2, 1]))                   # -> 1


# --- try the optimal ---
print(find_min_rotated_sorted_array([3, 4, 5, 1, 2]))          # -> 1
print(find_min_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2]))    # -> 0
print(find_min_rotated_sorted_array([11, 13, 15, 17]))         # -> 11
print(find_min_rotated_sorted_array([2, 1]))                   # -> 1
