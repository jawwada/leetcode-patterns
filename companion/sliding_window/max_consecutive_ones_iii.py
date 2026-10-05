"""
Max Consecutive Ones III (LeetCode 1004) - Medium
Chapter: sliding_window
Pattern: Variable-size sliding window

Given a binary array nums and an integer k, you may flip at most k zeros to ones. Return
the length of the longest run of consecutive ones you can get.
Example: nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], k = 2 -> 6 (flip the zeros at indices 4 and 5).
"""


# --- brute force ---
def brute_force(nums, k):
    """For every start, walk right until the (k+1)-th zero appears. O(n^2) time, O(1) space."""
    best = 0
    for start in range(len(nums)):
        zeros = 0                                   # recounted from scratch for every start
        for end in range(start, len(nums)):
            if nums[end] == 0:
                zeros += 1
            if zeros > k:
                break
            length = end - start + 1
            if length > best:
                best = length
    return best


# --- optimal ---
def longest_ones(nums, k):
    """Longest window with at most k zeros: grow right, trim left. O(n) time, O(1) space."""
    left = 0
    zeros = 0                   # zeros inside the window [left, right]
    best = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        while zeros > k:                            # k+1 zeros inside: push left past one zero
            if nums[left] == 0:
                zeros -= 1
            left += 1
        length = right - left + 1
        if length > best:
            best = length
    return best


# --- try the brute force ---
print(brute_force([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2))                            # -> 6
print(brute_force([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3))    # -> 10
print(brute_force([0, 0, 0], 0))                                                    # -> 0
print(brute_force([1, 1, 1], 0))                                                    # -> 3


# --- try the optimal ---
print(longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2))                            # -> 6
print(longest_ones([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3))    # -> 10
print(longest_ones([0, 0, 0], 0))                                                    # -> 0
print(longest_ones([1, 1, 1], 0))                                                    # -> 3
