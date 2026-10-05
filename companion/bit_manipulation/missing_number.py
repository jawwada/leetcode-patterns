"""
Missing Number (LeetCode 268) - Easy
Chapter: bit_manipulation
Pattern: XOR cancellation

Given an array of n distinct numbers taken from the range 0..n, exactly one number of the range
is missing. Return it in O(n) time and O(1) extra space.
Example: [3, 0, 1] -> 2; [9, 6, 4, 2, 3, 5, 7, 0, 1] -> 8.
"""


# --- brute force ---
def brute_force(nums):
    """Scan the array once for every candidate 0..n. O(n^2) time, O(1) space."""
    for candidate in range(len(nums) + 1):
        found = False
        for x in nums:                       # a full scan per candidate
            if x == candidate:
                found = True
                break
        if not found:
            return candidate
    return -1


# --- optimal ---
def missing_number(nums):
    """XOR all indices 0..n with all values; pairs cancel. O(n) time, O(1) space."""
    n = len(nums)
    result = n                               # index n has no slot in the array: start with it
    for i in range(n):
        result = result ^ i                  # a present value appears once as an index...
        result = result ^ nums[i]            # ...and once as a value, so it cancels out
    return result


# --- try the brute force ---
print(brute_force([3, 0, 1]))                      # -> 2
print(brute_force([9, 6, 4, 2, 3, 5, 7, 0, 1]))    # -> 8
print(brute_force([0]))                            # -> 1
print(brute_force([1]))                            # -> 0


# --- try the optimal ---
print(missing_number([3, 0, 1]))                      # -> 2
print(missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))    # -> 8
print(missing_number([0]))                            # -> 1
print(missing_number([1]))                            # -> 0
