"""
Binary Search Variants - Fundamentals
Chapter: fundamentals/searches
Key operations: mid = (lo + hi) // 2, keep the half that can hold the answer, lower/upper bound

On a sorted array find the index of x (or -1), the first index whose value is >= x (lower bound),
the first index whose value is > x (upper bound), and count = upper - lower. Both bounds use the
half-open range [lo, hi) and may return len(nums).
Example: [1, 2, 2, 2, 5, 7], x=2 -> index 2, lower 1, upper 4, count 3
"""


# --- algorithm ---
def binary_search(nums, x):
    """Closed range [lo, hi]; stop when it is empty. O(log n)."""
    lo = 0
    hi = len(nums) - 1
    while lo <= hi:                    # <= : a range of one element still has to be checked
        mid = (lo + hi) // 2
        if nums[mid] == x:
            return mid
        if nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(nums, x):
    """First index with nums[i] >= x. Half-open [lo, hi); lo is the first index that may work."""
    lo = 0
    hi = len(nums)                     # hi may be the answer: "no such index" is len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x:
            lo = mid + 1               # mid is too small, the answer is to its right
        else:
            hi = mid                   # mid works, but something to its left might too
    return lo


def upper_bound(nums, x):
    """First index with nums[i] > x: same loop, the only change is <= instead of <."""
    lo = 0
    hi = len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= x:             # <= : equal values are still "too small" here
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_of(nums, x):
    """How many times x occurs: the slots between the two bounds. O(log n)."""
    return upper_bound(nums, x) - lower_bound(nums, x)


# --- try it ---
print(binary_search([1, 2, 2, 2, 5, 7], 2))   # -> 2
print(lower_bound([1, 2, 2, 2, 5, 7], 2))     # -> 1
print(upper_bound([1, 2, 2, 2, 5, 7], 2))     # -> 4
print(count_of([1, 2, 2, 2, 5, 7], 2))        # -> 3
print(binary_search([1, 3, 5], 4))            # -> -1
print(lower_bound([1, 3, 5], 9))              # -> 3  (past the end: nothing is >= 9)
