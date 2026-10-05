"""
Find K-th Smallest Pair Distance (LeetCode 719) - Hard
Chapter: binary_search
Pattern: Binary search on the answer

The distance of a pair (i, j) with i < j is |nums[i] - nums[j]|. Return the k-th smallest
distance among all n(n-1)/2 pairs.
Example: nums = [1, 3, 1], k = 1 -> 0 (distances 2, 0, 2; sorted 0, 2, 2)
"""


# --- brute force ---
def brute_force(nums, k):
    """List every pair distance, sort, read index k - 1. O(n^2 log n) time, O(n^2) space."""
    distances = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            distances.append(abs(nums[i] - nums[j]))
    distances.sort()
    return distances[k - 1]


# --- optimal ---
def count_pairs_within(nums, limit):
    """How many pairs of the SORTED nums have distance <= limit: two pointers. O(n) time."""
    count = 0
    left = 0
    for right in range(len(nums)):
        while nums[right] - nums[left] > limit:
            left += 1                     # shrink until the window spans at most limit
        count += right - left             # every index in [left, right) pairs with right
    return count


def smallest_distance_pair(nums, k):
    """Binary search the smallest distance with at least k pairs at or below it. O(n log D)."""
    nums = sorted(nums)
    left = 0
    right = nums[-1] - nums[0]            # the largest possible distance
    while left < right:
        mid = (left + right) // 2
        if count_pairs_within(nums, mid) >= k:
            right = mid                   # at least k pairs fit under mid: try smaller
        else:
            left = mid + 1
    return left


# --- try the brute force ---
print(brute_force([1, 3, 1], 1))                              # -> 0
print(brute_force([1, 6, 1], 3))                              # -> 5
print(brute_force([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18))      # -> 2
print(brute_force([1, 100], 1))                               # -> 99


# --- try the optimal ---
print(smallest_distance_pair([1, 3, 1], 1))                              # -> 0
print(smallest_distance_pair([1, 6, 1], 3))                              # -> 5
print(smallest_distance_pair([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18))      # -> 2
print(smallest_distance_pair([1, 100], 1))                               # -> 99
