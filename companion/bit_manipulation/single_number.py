"""
Single Number (LeetCode 136) - Easy
Chapter: bit_manipulation
Pattern: XOR cancellation

Every element of a non-empty array appears exactly twice except one, which appears once.
Find that element in linear time using constant extra space.
Example: [4, 1, 2, 1, 2] -> 4.
"""


# --- brute force ---
def brute_force(nums):
    """For each number, count its copies in the whole array. O(n^2) time, O(1) space."""
    for x in nums:
        count = 0
        for y in nums:                       # rescan the array for every element
            if y == x:
                count = count + 1
        if count == 1:
            return x
    return -1


# --- optimal ---
def single_number(nums):
    """XOR everything together: pairs cancel. O(n) time, O(1) space."""
    result = 0
    for x in nums:
        result = result ^ x                  # a ^ a = 0, so every pair vanishes, in any order
    return result


# --- try the brute force ---
print(brute_force([2, 2, 1]))          # -> 1
print(brute_force([4, 1, 2, 1, 2]))    # -> 4
print(brute_force([1]))                # -> 1
print(brute_force([-3, 7, -3]))        # -> 7


# --- try the optimal ---
print(single_number([2, 2, 1]))          # -> 1
print(single_number([4, 1, 2, 1, 2]))    # -> 4
print(single_number([1]))                # -> 1
print(single_number([-3, 7, -3]))        # -> 7
