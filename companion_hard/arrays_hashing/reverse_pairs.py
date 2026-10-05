"""
Reverse Pairs (LeetCode 493) - Hard
Chapter: arrays_hashing
Pattern: Merge sort counting

Given an integer array nums, count the pairs i < j with nums[i] > 2 * nums[j].
Example: [1, 3, 2, 3, 1] -> 2 (pairs (1, 4) and (3, 4), both 3 > 2 * 1).
         [2, 4, 3, 5, 1] -> 3.
"""


# --- brute force ---
def brute_force(nums):
    """Test every pair i < j. O(n^2) time, O(1) space."""
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > 2 * nums[j]:
                count += 1
    return count


# --- optimal ---
def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def sort_and_count(arr):
    """Return (arr sorted, number of reverse pairs inside arr). Recursive helper."""
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, count_left = sort_and_count(arr[:mid])
    right, count_right = sort_and_count(arr[mid:])
    count = count_left + count_right
    j = 0  # right[0:j] are exactly the values r with 2 * r < x
    for x in left:  # x increases, so j never moves back
        while j < len(right) and 2 * right[j] < x:
            j += 1
        count += j
    return merge(left, right), count


def reverse_pairs(nums):
    """Merge sort; count cross pairs with a two-pointer walk at each merge. O(n log n) time."""
    ordered, count = sort_and_count(nums)
    return count


# --- try the brute force ---
print(brute_force([1, 3, 2, 3, 1]))   # -> 2
print(brute_force([2, 4, 3, 5, 1]))   # -> 3
print(brute_force([5]))               # -> 0
print(brute_force([-5, -3, -1, 0]))   # -> 1


# --- try the optimal ---
print(reverse_pairs([1, 3, 2, 3, 1]))   # -> 2
print(reverse_pairs([2, 4, 3, 5, 1]))   # -> 3
print(reverse_pairs([5]))               # -> 0
print(reverse_pairs([-5, -3, -1, 0]))   # -> 1
