"""
Count of Smaller Numbers After Self (LeetCode 315) - Hard
Chapter: arrays_hashing
Pattern: Merge sort counting

Given an integer array nums, return counts where counts[i] is how many elements to the
right of index i are strictly smaller than nums[i].
Example: [5, 2, 6, 1] -> [2, 1, 1, 0] (right of 5: 2 and 1; right of 2: 1; right of 6: 1).
"""


# --- brute force ---
def brute_force(nums):
    """For each i, scan every j > i and count the smaller ones. O(n^2) time, O(1) space."""
    counts = []
    for i in range(len(nums)):
        smaller = 0
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[i]:
                smaller += 1
        counts.append(smaller)
    return counts


# --- optimal ---
def merge_sort(nums, idx, lo, hi, counts):
    """Sort idx[lo:hi] by value; add to counts while merging. Recursive helper."""
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    merge_sort(nums, idx, lo, mid, counts)
    merge_sort(nums, idx, mid, hi, counts)
    merged = []
    i = lo
    j = mid
    while i < mid and j < hi:
        if nums[idx[j]] < nums[idx[i]]:
            merged.append(idx[j])
            j += 1
        else:
            # the j - mid right-half elements already emitted are smaller and come later
            counts[idx[i]] += j - mid
            merged.append(idx[i])
            i += 1
    while i < mid:  # left leftovers: every right element was smaller
        counts[idx[i]] += j - mid
        merged.append(idx[i])
        i += 1
    merged.extend(idx[j:hi])  # right leftovers, already in order
    idx[lo:hi] = merged


def count_smaller(nums):
    """Merge sort the indices and count right-half elements that pass each left one. O(n log n)."""
    n = len(nums)
    counts = [0] * n
    idx = list(range(n))  # sort indices so each element keeps its identity
    merge_sort(nums, idx, 0, n, counts)
    return counts


# --- try the brute force ---
print(brute_force([5, 2, 6, 1]))   # -> [2, 1, 1, 0]
print(brute_force([-1, -1]))       # -> [0, 0]
print(brute_force([]))             # -> []
print(brute_force([3, 3, 2, 1]))   # -> [2, 2, 1, 0]


# --- try the optimal ---
print(count_smaller([5, 2, 6, 1]))   # -> [2, 1, 1, 0]
print(count_smaller([-1, -1]))       # -> [0, 0]
print(count_smaller([]))             # -> []
print(count_smaller([3, 3, 2, 1]))   # -> [2, 2, 1, 0]
