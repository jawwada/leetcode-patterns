"""
Patching Array (LeetCode 330) - Hard
Chapter: greedy
Pattern: Greedy reach (furthest reachable index)

Given a sorted array nums and an integer n, add (patch) the minimum number of integers so that
every value in [1, n] is the sum of some subset of the array; return that count.
Example: nums = [1,3], n = 6 -> 1 (patch 2); nums = [1,5,10], n = 20 -> 2 (patch 2 and 4).
"""


# --- brute force ---
def brute_force(nums, n):
    """Each round list every subset sum, patch the smallest missing value, repeat. Exponential."""
    arr = list(nums)
    patches = 0
    while True:
        sums = subset_sums(arr, n)
        missing = 0
        for value in range(1, n + 1):
            if value not in sums:
                missing = value                   # the smallest value nobody can build
                break
        if missing == 0:
            return patches
        arr.append(missing)
        patches += 1


def subset_sums(arr, limit):
    """Every subset sum of arr that is <= limit, built one element at a time."""
    sums = {0}
    for x in arr:
        with_x = set()
        for s in sums:
            if s + x <= limit:
                with_x.add(s + x)
        sums = sums | with_x
    return sums


# --- optimal ---
def patching_array(nums, n):
    """reach = every sum in [1, reach] is buildable; patch reach + 1 when the next number is big"""
    reach = 0
    patches = 0
    i = 0
    while reach < n:
        if i < len(nums) and nums[i] <= reach + 1:
            reach += nums[i]                      # no hole: [1, reach] + x covers [1, reach + x]
            i += 1
        else:
            reach += reach + 1                    # patch with reach + 1: coverage doubles
            patches += 1
    return patches


# --- try the brute force ---
print(brute_force([1, 3], 6))          # -> 1
print(brute_force([1, 5, 10], 20))     # -> 2
print(brute_force([1, 2, 2], 5))       # -> 0
print(brute_force([], 7))              # -> 3


# --- try the optimal ---
print(patching_array([1, 3], 6))       # -> 1
print(patching_array([1, 5, 10], 20))  # -> 2
print(patching_array([1, 2, 2], 5))    # -> 0
print(patching_array([], 7))           # -> 3
