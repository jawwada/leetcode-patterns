"""
Median of Two Sorted Arrays - Binary Search the Partition

Given two sorted arrays with at least one value between them, return the
median of all their values together in O(log(m + n)) time:
[1, 3, 8, 9, 15] and [7, 11, 18, 19, 21, 25] -> 11.
"""
import math                         # math.inf: a cut at the edge sees infinity


# --- algorithm ---
def value_at(arr, k):
    """arr[k], or -inf before the start and +inf past the end. O(1)."""
    if k < 0:
        return -math.inf
    if k >= len(arr):
        return math.inf
    return arr[k]


def find_median(a, b):
    """Binary search the cut i in the shorter array; b's cut j follows.
    O(log min(m, n)) time, O(1) space."""
    if len(a) > len(b):
        a, b = b, a                 # search the shorter array
    m = len(a)
    n = len(b)
    half = (m + n + 1) // 2         # size of the left part
    lo = 0
    hi = m
    while lo <= hi:
        i = (lo + hi) // 2          # a[:i] goes to the left part
        j = half - i                # b[:j] fills the rest of it
        a_left = value_at(a, i - 1)
        a_right = value_at(a, i)
        b_left = value_at(b, j - 1)
        b_right = value_at(b, j)
        if a_left <= b_right and b_left <= a_right:    # every left <= right
            if (m + n) % 2 == 1:
                return max(a_left, b_left)
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
        if a_left > b_right:
            hi = i - 1              # too much of a on the left: cut a earlier
        else:
            lo = i + 1              # too little of a on the left: cut a later


# --- try it ---
print(find_median([1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25]))    # -> 11
print(find_median([1, 3], [2]))                                 # -> 2
print(find_median([1, 2], [3, 4]))                              # -> 2.5
print(find_median([], [4]))                                     # -> 4
