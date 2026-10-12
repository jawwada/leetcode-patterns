"""
Binary Search - The Lower-Bound Template

Given a sorted array and a target, return the first index whose value is at
least the target, or len(nums) if every value is smaller:
[1, 3, 3, 5, 8, 9], target 3 -> 1.
"""


# --- algorithm ---
def lower_bound(nums, target):
    """First index i with nums[i] >= target, len(nums) if none. O(log n)."""
    lo = 0
    hi = len(nums)              # half-open [lo, hi); len(nums) means "none"
    while lo < hi:              # the window still holds an unknown index
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1        # mid and everything left of it are too small
        else:
            hi = mid            # mid qualifies: the answer is mid or left of it
    return lo


def upper_bound(nums, target):
    """First i with nums[i] > target: the same loop, <= for <. O(log n)."""
    lo = 0
    hi = len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:     # equal values count as too small here
            lo = mid + 1
        else:
            hi = mid
    return lo


def search(nums, target):
    """Exact search: a present target sits at its lower bound. O(log n)."""
    i = lower_bound(nums, target)
    if i < len(nums) and nums[i] == target:
        return i
    return -1


def search_range(nums, target):
    """First and last index, [-1, -1] if absent: two searches, O(log n)."""
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    return [first, upper_bound(nums, target) - 1]


# --- try it ---
nums = [1, 3, 3, 5, 8, 9]
print(lower_bound(nums, 3))         # -> 1
print(lower_bound(nums, 4))         # -> 3
print(search(nums, 4))              # -> -1
print(search_range(nums, 3))        # -> [1, 2]
print(lower_bound(nums, 10))        # -> 6
