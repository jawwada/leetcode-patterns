"""
Two Sum II - Input Array Is Sorted (LeetCode 167) - Medium
Chapter: two_pointers
Pattern: Converging two pointers on sorted input

Given a 1-indexed array sorted in non-decreasing order and a target, return the
1-based indices [i, j] with i < j of the two numbers that sum to target. Exactly one
solution exists and you must use O(1) extra space.
Example: numbers = [2, 7, 11, 15], target = 9 -> [1, 2].
"""


# --- brute force ---
def brute_force(numbers, target):
    """Try every pair i < j, ignoring the sort order. O(n^2) time, O(1) space."""
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]  # the problem wants 1-based indices
    return []


# --- optimal ---
def two_sum_sorted(numbers, target):
    """Pointers at both ends; the sum says which one to move. O(n) time, O(1) space."""
    left = 0
    right = len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]  # 1-based indices
        if total < target:
            left += 1  # too small: only a bigger left value can raise the sum
        else:
            right -= 1  # too big: only a smaller right value can lower it
    return []


# --- try the brute force ---
print(brute_force([2, 7, 11, 15], 9))                 # -> [1, 2]
print(brute_force([2, 3, 4], 6))                      # -> [1, 3]
print(brute_force([-1, 0], -1))                       # -> [1, 2]
print(brute_force([1, 2, 3, 4, 4, 9, 56, 90], 8))     # -> [4, 5]


# --- try the optimal ---
print(two_sum_sorted([2, 7, 11, 15], 9))                 # -> [1, 2]
print(two_sum_sorted([2, 3, 4], 6))                      # -> [1, 3]
print(two_sum_sorted([-1, 0], -1))                       # -> [1, 2]
print(two_sum_sorted([1, 2, 3, 4, 4, 9, 56, 90], 8))     # -> [4, 5]
