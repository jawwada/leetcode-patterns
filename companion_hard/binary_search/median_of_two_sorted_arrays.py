"""
Median of Two Sorted Arrays (LeetCode 4) - Hard
Chapter: binary_search
Pattern: Binary search on a partition

Given two sorted arrays nums1 and nums2, return the median of their combined sorted order in
O(log(m + n)) time.
Example: nums1 = [1, 3], nums2 = [2] -> 2.0; nums1 = [1, 2], nums2 = [3, 4] -> 2.5
"""
import math                            # math.inf is a number bigger than everything


# --- brute force ---
def brute_force(nums1, nums2):
    """Merge everything, sort, read the middle. O((m + n) log(m + n)) time."""
    merged = sorted(nums1 + nums2)
    size = len(merged)
    if size % 2 == 1:
        return float(merged[size // 2])
    return (merged[size // 2 - 1] + merged[size // 2]) / 2


# --- optimal ---
def value_at(arr, i):
    """arr[i], with -inf before the start and +inf past the end."""
    if i < 0:
        return -math.inf
    if i >= len(arr):
        return math.inf
    return arr[i]


def median_of_two_sorted_arrays(nums1, nums2):
    """Binary search how many of the shorter array belong to the left half. O(log(min(m, n)))."""
    shorter = nums1
    longer = nums2
    if len(shorter) > len(longer):
        shorter, longer = longer, shorter
    total = len(shorter) + len(longer)
    half = (total + 1) // 2               # size of the left half
    left = 0
    right = len(shorter)
    while left <= right:
        i = (left + right) // 2           # i values of shorter go to the left half
        j = half - i                      # the rest of the left half comes from longer
        shorter_left = value_at(shorter, i - 1)
        shorter_right = value_at(shorter, i)
        longer_left = value_at(longer, j - 1)
        longer_right = value_at(longer, j)
        if shorter_left > longer_right:
            right = i - 1                 # took too many from shorter
        elif longer_left > shorter_right:
            left = i + 1                  # took too few from shorter
        elif total % 2 == 1:
            return float(max(shorter_left, longer_left))
        else:
            left_max = max(shorter_left, longer_left)
            right_min = min(shorter_right, longer_right)
            return (left_max + right_min) / 2


# --- try the brute force ---
print(brute_force([1, 3], [2]))                                  # -> 2.0
print(brute_force([1, 2], [3, 4]))                               # -> 2.5
print(brute_force([], [1]))                                      # -> 1.0
print(brute_force([1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]))        # -> 6.0


# --- try the optimal ---
print(median_of_two_sorted_arrays([1, 3], [2]))                                  # -> 2.0
print(median_of_two_sorted_arrays([1, 2], [3, 4]))                               # -> 2.5
print(median_of_two_sorted_arrays([], [1]))                                      # -> 1.0
print(median_of_two_sorted_arrays([1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]))        # -> 6.0
