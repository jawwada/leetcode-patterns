"""
Permutations With Duplicates - Fundamentals
Chapter: fundamentals/backtracking
Key operations: sort, skip nums[i] == nums[i-1] unless used[i-1], mark, choose, unmark, unchoose

Return every distinct ordering of an array that may contain duplicates (LeetCode 47). Sorting
makes equal values adjacent; among a run of equal values the recursion must take them left to
right, so an equal value whose left twin is not yet used is skipped on this level. Results sorted.
Example: [1, 1, 2] -> [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
"""


# --- algorithm ---
def backtrack(nums, used, path, res):
    """Append every unused value to path; record it when every value has been placed."""
    if len(path) == len(nums):
        res.append(path[:])   # copy: path keeps changing below
        return
    for i in range(len(nums)):
        if used[i]:
            continue
        if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:   # equal values: left to right
            continue
        used[i] = True                # mark and choose
        path.append(nums[i])
        backtrack(nums, used, path, res)
        path.pop()                    # unchoose and unmark
        used[i] = False


def permutations_with_duplicates(nums):
    """Sort, then used[] flags plus one skip rule; no duplicate is ever generated. O(n * n!)."""
    nums = sorted(nums)
    used = [False] * len(nums)
    res = []
    backtrack(nums, used, [], res)
    return sorted(res)


# --- try it ---
print(permutations_with_duplicates([1, 1, 2]))   # -> [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
print(permutations_with_duplicates([2, 2]))      # -> [[2, 2]]
print(permutations_with_duplicates([3, 1]))      # -> [[1, 3], [3, 1]]
print(permutations_with_duplicates([]))          # -> [[]]
