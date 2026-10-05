"""
Product of Array Except Self (LeetCode 238) - Medium
Chapter: arrays_hashing
Pattern: Prefix and suffix accumulation

Given an integer array nums, return answer where answer[i] is the product of all
elements except nums[i], without using division and in O(n) time.
Example: nums = [1, 2, 3, 4] -> [24, 12, 8, 6].
"""


# --- brute force ---
def brute_force(nums):
    """For each i multiply every other element. O(n^2) time, O(1) extra space."""
    n = len(nums)
    answer = []
    for i in range(n):
        product = 1
        for j in range(n):
            if j != i:
                product = product * nums[j]
        answer.append(product)
    return answer


# --- optimal ---
def product_except_self(nums):
    """Left products pass, then right products pass. O(n) time, O(1) extra space."""
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix  # product of everything left of i (stamp first, then include i)
        prefix = prefix * nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] = answer[i] * suffix  # times the product of everything right of i
        suffix = suffix * nums[i]
    return answer


# --- try the brute force ---
print(brute_force([1, 2, 3, 4]))          # -> [24, 12, 8, 6]
print(brute_force([-1, 1, 0, -3, 3]))     # -> [0, 0, 9, 0, 0]
print(brute_force([0, 0, 2]))             # -> [0, 0, 0]
print(brute_force([5, 2]))                # -> [2, 5]


# --- try the optimal ---
print(product_except_self([1, 2, 3, 4]))          # -> [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))     # -> [0, 0, 9, 0, 0]
print(product_except_self([0, 0, 2]))             # -> [0, 0, 0]
print(product_except_self([5, 2]))                # -> [2, 5]
