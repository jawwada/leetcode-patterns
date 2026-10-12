"""
Median of K Sorted Arrays - Binary Search on the Value

Given k sorted arrays of integers holding N >= 1 values in total, return the
median of all of them (the average of the two middle values when N is even):
[[1, 4, 9], [2, 3, 7, 10], [5, 8]] -> 5.
"""
import math                         # math.inf seeds the running min and max


# --- algorithm ---
def count_at_most(arr, value):
    """Upper bound (#14): how many values of sorted arr are <= value.
    O(log L)."""
    lo = 0
    hi = len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= value:
            lo = mid + 1
        else:
            hi = mid
    return lo


def kth_smallest(arrays, rank):
    """Smallest value v with at least rank values <= v, by binary search on
    v from the smallest to the largest value. O(k log L log R)."""
    lo = math.inf
    hi = -math.inf
    for arr in arrays:
        if len(arr) > 0:
            lo = min(lo, arr[0])        # smallest first element
            hi = max(hi, arr[-1])       # largest last element
    while lo < hi:
        mid = (lo + hi) // 2
        count = 0
        for arr in arrays:
            count += count_at_most(arr, mid)
        if count >= rank:
            hi = mid                    # mid already covers rank values
        else:
            lo = mid + 1                # too few values are <= mid
    return lo


def median_k_sorted(arrays):
    """One order statistic for odd N, the average of two for even N.
    O(k log L log R)."""
    total = 0
    for arr in arrays:
        total += len(arr)
    if total % 2 == 1:
        return kth_smallest(arrays, total // 2 + 1)
    low = kth_smallest(arrays, total // 2)
    high = kth_smallest(arrays, total // 2 + 1)
    return (low + high) / 2


# --- try it ---
arrays = [[1, 4, 9], [2, 3, 7, 10], [5, 8]]
print(median_k_sorted(arrays))                      # -> 5
print(kth_smallest(arrays, 6))                      # -> 7
print(median_k_sorted([[1, 2], [3, 4]]))            # -> 2.5
print(median_k_sorted([[-5, -1], [], [-3]]))        # -> -3
