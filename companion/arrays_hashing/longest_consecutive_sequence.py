"""
Longest Consecutive Sequence (LeetCode 128) - Medium
Chapter: arrays_hashing
Pattern: Hash set with sequence-start detection

Given an unsorted integer array, return the length of the longest run of
consecutive integer values (values, not positions), in O(n) time.
Example: nums = [100, 4, 200, 1, 3, 2] -> 4, from the run 1, 2, 3, 4.
"""


# --- brute force ---
def brute_force(nums):
    """From every element count upward, each check a list scan. O(n^3) worst, O(1) space."""
    best = 0
    for start in nums:
        length = 1
        while start + length in nums:  # 'in' on a list scans the whole list every time
            length += 1
        best = max(best, length)
    return best


# --- optimal ---
def longest_consecutive(nums):
    """Set lookups; only walk a run from its smallest value. O(n) time, O(n) space."""
    values = set(nums)
    best = 0
    for start in values:
        if start - 1 in values:
            continue  # not the start of a run; the run is counted from its true start
        length = 1
        while start + length in values:
            length += 1
        best = max(best, length)
    return best


# --- try the brute force ---
print(brute_force([100, 4, 200, 1, 3, 2]))             # -> 4
print(brute_force([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))     # -> 9
print(brute_force([]))                                 # -> 0
print(brute_force([1, 1, 1]))                          # -> 1


# --- try the optimal ---
print(longest_consecutive([100, 4, 200, 1, 3, 2]))             # -> 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))     # -> 9
print(longest_consecutive([]))                                 # -> 0
print(longest_consecutive([1, 1, 1]))                          # -> 1
