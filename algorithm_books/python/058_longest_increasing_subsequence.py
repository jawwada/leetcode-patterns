"""
Longest Increasing Subsequence - Patience Sorting with Binary Search

Given an array of integers, return the length of its longest strictly
increasing subsequence (kept in order, not necessarily adjacent):
[10, 9, 2, 5, 3, 7, 101, 18] -> 4 (for example 2, 3, 7, 18).
"""


# --- algorithm ---
def lower_bound(values, target):
    """First index i with values[i] >= target, len(values) if none. O(log n)."""
    lo = 0
    hi = len(values)                # half-open [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def length_of_lis(nums):
    """tails[k] is the smallest tail of an increasing subsequence of length
    k + 1; each x replaces the first tail >= x or extends. O(n log n)."""
    tails = []
    for x in nums:
        i = lower_bound(tails, x)   # how many tails are smaller than x
        if i == len(tails):
            tails.append(x)         # x extends the longest subsequence
        else:
            tails[i] = x            # a smaller tail for length i + 1
    return len(tails)


# --- try it ---
print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))     # -> 4
print(length_of_lis([0, 1, 0, 3, 2, 3]))               # -> 4
print(length_of_lis([7, 7, 7, 7]))                     # -> 1
print(length_of_lis([4, 5, 6, 1]))                     # -> 3
print(length_of_lis([]))                               # -> 0
