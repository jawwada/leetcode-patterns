"""
Maximum Subarray (LeetCode 53) - Medium
Chapter: greedy
Pattern: Greedy running sum (Kadane)

Given an integer array nums, return the largest sum of any contiguous non-empty subarray.
Example: [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> 6 (the subarray [4, -1, 2, 1]).
"""


# --- brute force ---
def brute_force(nums):
    """Try every start, extend the end one step at a time. O(n^2) time, O(1) space."""
    best = nums[0]
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):
            total = total + nums[end]        # running sum of nums[start..end]
            if total > best:
                best = total
    return best


# --- optimal ---
def maximum_subarray(nums):
    """One running sum; restart it whenever it goes negative. O(n) time, O(1) space."""
    current = nums[0]                        # best sum of a subarray ending here
    best = nums[0]
    for i in range(1, len(nums)):
        if current < 0:
            current = nums[i]                # a negative running sum is dead weight: restart
        else:
            current = current + nums[i]
        if current > best:
            best = current
    return best


# --- try the brute force ---
print(brute_force([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # -> 6
print(brute_force([5, 4, -1, 7, 8]))                  # -> 23
print(brute_force([-3, -1, -2]))                      # -> -1
print(brute_force([2, -1, 2, -1, 2]))                 # -> 4


# --- try the optimal ---
print(maximum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # -> 6
print(maximum_subarray([5, 4, -1, 7, 8]))                  # -> 23
print(maximum_subarray([-3, -1, -2]))                      # -> -1
print(maximum_subarray([2, -1, 2, -1, 2]))                 # -> 4
