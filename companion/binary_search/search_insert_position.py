"""
Search Insert Position (LeetCode 35) - Easy
Chapter: binary_search
Pattern: Binary search for a boundary (lower / upper bound)

Given a sorted array of distinct integers and a target, return the index of target if it is
present, otherwise the index where it would be inserted to keep the array sorted, in O(log n).
Example: nums = [1, 3, 5, 6], target = 5 -> 2; target = 2 -> 1; target = 7 -> 4
"""


# --- brute force ---
def brute_force(nums, target):
    """Walk left to right to the first value that is >= target. O(n) time, O(1) space."""
    for i in range(len(nums)):
        if nums[i] >= target:
            return i               # found target, or the spot where it would go
    return len(nums)               # every value is smaller: insert at the end


# --- optimal ---
def search_insert_position(nums, target):
    """Binary search for the first index with nums[i] >= target. O(log n) time, O(1) space."""
    left = 0
    right = len(nums) - 1
    answer = len(nums)             # if nothing is >= target, insert at the end
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] >= target:
            answer = mid           # mid qualifies; look further left for an earlier one
            right = mid - 1
        else:
            left = mid + 1         # mid is too small, so is everything before it
    return answer


# --- try the brute force ---
print(brute_force([1, 3, 5, 6], 5))   # -> 2
print(brute_force([1, 3, 5, 6], 2))   # -> 1
print(brute_force([1, 3, 5, 6], 7))   # -> 4
print(brute_force([1, 3, 5, 6], 0))   # -> 0


# --- try the optimal ---
print(search_insert_position([1, 3, 5, 6], 5))   # -> 2
print(search_insert_position([1, 3, 5, 6], 2))   # -> 1
print(search_insert_position([1, 3, 5, 6], 7))   # -> 4
print(search_insert_position([1, 3, 5, 6], 0))   # -> 0
