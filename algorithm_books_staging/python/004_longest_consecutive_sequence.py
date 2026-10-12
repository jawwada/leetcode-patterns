"""
Longest Consecutive Sequence - Count Only from the Start of a Run

Given an unsorted array of integers, return the length of the longest run of
consecutive values, wherever they sit in the array:
[100, 4, 200, 1, 3, 2] -> 4 (the run 1, 2, 3, 4).
"""


# --- algorithm ---
def longest_consecutive(nums):
    """Walk up a run only from its start, a value whose num - 1 is missing.
    Each value is touched at most twice. O(n) time and space."""
    values = set(nums)              # O(1) lookups; duplicates collapse
    best = 0
    for num in values:              # the set, so each start walks once
        if num - 1 in values:
            continue                # inside a run: its start counts it
        length = 1
        while num + length in values:
            length += 1             # one more step up the run
        best = max(best, length)
    return best


# --- try it ---
print(longest_consecutive([100, 4, 200, 1, 3, 2]))           # -> 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))   # -> 9
print(longest_consecutive([-1, 5, -3, -2, 5, 0]))            # -> 4
print(longest_consecutive([7, 7, 7]))                        # -> 1
print(longest_consecutive([]))                               # -> 0
