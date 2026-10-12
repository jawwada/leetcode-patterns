"""
Two Sum - Hash Map of Complements

Given an array of integers and a target, return the indices of the two numbers
that add up to the target (exactly one pair exists):
[2, 7, 11, 15], target 9 -> [0, 1].
"""


# --- algorithm ---
def two_sum(nums, target):
    """One pass; look up target - x before storing x. O(n) time and space."""
    seen = {}                       # value -> index
    for i in range(len(nums)):
        need = target - nums[i]
        if need in seen:            # partner appeared earlier
            return [seen[need], i]
        seen[nums[i]] = i           # store only after checking
    return []


# --- try it ---
print(two_sum([2, 7, 11, 15], 9))   # -> [0, 1]
print(two_sum([3, 2, 4], 6))        # -> [1, 2]
print(two_sum([3, 3], 6))           # -> [0, 1]
print(two_sum([1, 2], 7))           # -> []
