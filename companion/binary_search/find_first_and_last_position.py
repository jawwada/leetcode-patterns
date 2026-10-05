"""
Find First and Last Position of Element in Sorted Array (LeetCode 34) - Medium
Chapter: binary_search
Pattern: Binary search for a boundary (lower / upper bound)

Given a non-decreasing array nums and a target, return [first, last], the indices of the
first and last occurrence of target, or [-1, -1] if it is absent, in O(log n) time.
Example: nums = [5, 7, 7, 8, 8, 10], target = 8 -> [3, 4]; target = 6 -> [-1, -1]
"""


# --- brute force ---
def brute_force(nums, target):
    """Scan once, remembering the first and the latest match. O(n) time, O(1) space."""
    first = -1
    last = -1
    for i in range(len(nums)):
        if nums[i] == target:
            if first == -1:
                first = i          # only the first match sets this
            last = i               # every match moves this forward
    return [first, last]


# --- optimal ---
def first_index_at_least(nums, value):
    """First index whose element is >= value, or len(nums) if there is none. O(log n)."""
    left = 0
    right = len(nums)              # half-open range [left, right): right may be len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < value:
            left = mid + 1         # mid is too small
        else:
            right = mid            # mid qualifies, but an earlier index might too
    return left


def find_first_and_last_position(nums, target):
    """Two boundary searches: first >= target, first > target. O(log n) time, O(1) space."""
    first = first_index_at_least(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]            # target is absent
    last = first_index_at_least(nums, target + 1) - 1   # one before the first value > target
    return [first, last]


# --- try the brute force ---
print(brute_force([5, 7, 7, 8, 8, 10], 8))   # -> [3, 4]
print(brute_force([5, 7, 7, 8, 8, 10], 6))   # -> [-1, -1]
print(brute_force([2, 2, 2, 2], 2))          # -> [0, 3]
print(brute_force([1, 3], 3))                # -> [1, 1]


# --- try the optimal ---
print(find_first_and_last_position([5, 7, 7, 8, 8, 10], 8))   # -> [3, 4]
print(find_first_and_last_position([5, 7, 7, 8, 8, 10], 6))   # -> [-1, -1]
print(find_first_and_last_position([2, 2, 2, 2], 2))          # -> [0, 3]
print(find_first_and_last_position([1, 3], 3))                # -> [1, 1]
