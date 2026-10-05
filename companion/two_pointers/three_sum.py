"""
3Sum (LeetCode 15) - Medium
Chapter: two_pointers
Pattern: Sort + fixed element + converging two pointers

Given an integer array nums, return all unique triplets [a, b, c] with a + b + c == 0;
the result must not contain duplicate triplets (any order).
Example: nums = [-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0, 1]].
"""


# --- helpers ---
def tidy(triplets):
    """Sort inside each triplet and then sort the triplets, so any valid answer prints the same."""
    tidied = []
    for triplet in triplets:
        tidied.append(sorted(triplet))
    return sorted(tidied)


# --- brute force ---
def brute_force(nums):
    """Try every triple i < j < k; a set removes duplicates. O(n^3) time."""
    n = len(nums)
    found = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted([nums[i], nums[j], nums[k]])))  # sorted so clones match
    result = []
    for triplet in found:
        result.append(list(triplet))
    return result


# --- optimal ---
def three_sum(nums):
    """Sort; fix one value, two-pointer the rest, skip repeats. O(n^2) time."""
    nums.sort()
    n = len(nums)
    result = []
    for i in range(n - 2):
        if nums[i] > 0:
            break  # everything after is positive too, no zero sum possible
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # same anchor as last time gives the same triplets
        left = i + 1
        right = n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1  # step over clones of the value just used
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
    return result


# --- try the brute force ---
print(tidy(brute_force([-1, 0, 1, 2, -1, -4])))        # -> [[-1, -1, 2], [-1, 0, 1]]
print(tidy(brute_force([0, 1, 1])))                    # -> []
print(tidy(brute_force([0, 0, 0])))                    # -> [[0, 0, 0]]
print(tidy(brute_force([-2, 0, 0, 2, 2])))             # -> [[-2, 0, 2]]


# --- try the optimal ---
print(tidy(three_sum([-1, 0, 1, 2, -1, -4])))        # -> [[-1, -1, 2], [-1, 0, 1]]
print(tidy(three_sum([0, 1, 1])))                    # -> []
print(tidy(three_sum([0, 0, 0])))                    # -> [[0, 0, 0]]
print(tidy(three_sum([-2, 0, 0, 2, 2])))             # -> [[-2, 0, 2]]
