"""
Majority Element (LeetCode 169) - Easy
Chapter: arrays_hashing
Pattern: Boyer-Moore voting

Given an array of size n, return the element that appears more than n / 2 times.
A majority element always exists. Follow-up: O(n) time and O(1) space.
Example: nums = [2, 2, 1, 1, 1, 2, 2] -> 2.
"""


# --- brute force ---
def brute_force(nums):
    """Count every value from scratch with a full scan. O(n^2) time, O(1) space."""
    n = len(nums)
    for value in nums:
        occurrences = 0
        for other in nums:
            if other == value:
                occurrences += 1
        if occurrences > n // 2:
            return value
    return -1


# --- optimal ---
def majority_element(nums):
    """Boyer-Moore voting: cancel pairs of different values. O(n) time, O(1) space."""
    candidate = nums[0]
    count = 0
    for value in nums:
        if count == 0:
            candidate = value  # the previous candidate was fully cancelled out
        if value == candidate:
            count += 1
        else:
            count -= 1
    return candidate


# --- try the brute force ---
print(brute_force([3, 2, 3]))                 # -> 3
print(brute_force([2, 2, 1, 1, 1, 2, 2]))     # -> 2
print(brute_force([1]))                       # -> 1
print(brute_force([5, 1, 5, 1, 5]))           # -> 5


# --- try the optimal ---
print(majority_element([3, 2, 3]))             # -> 3
print(majority_element([2, 2, 1, 1, 1, 2, 2]))  # -> 2
print(majority_element([1]))                   # -> 1
print(majority_element([5, 1, 5, 1, 5]))       # -> 5
