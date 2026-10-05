"""
Subsets With Duplicates - Fundamentals
Chapter: fundamentals/backtracking
Key operations: sort, skip nums[i] == nums[i-1] when i > start, choose, recurse from i+1, unchoose

Return every distinct subset of an array that may contain duplicates (LeetCode 90). Sorting puts
equal values side by side; on one level of the tree only the first of a run of equal values may be
chosen. Results sorted.
Example: [1, 2, 2] -> [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
"""


# --- algorithm ---
def backtrack(nums, start, path, res):
    """Record the current path, then try to extend it with each value from start onward."""
    res.append(path[:])   # copy: path keeps changing below
    for i in range(start, len(nums)):
        if i > start and nums[i] == nums[i - 1]:   # on one level, only the first of equal values
            continue
        path.append(nums[i])          # choose
        backtrack(nums, i + 1, path, res)
        path.pop()                    # unchoose


def subsets_with_duplicates(nums):
    """Sort, then the start-index template with one skip rule. O(n * 2^n)."""
    nums = sorted(nums)
    res = []
    backtrack(nums, 0, [], res)
    return sorted(res)


# --- try it ---
print(subsets_with_duplicates([1, 2, 2]))   # -> [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
print(subsets_with_duplicates([2, 2, 2]))   # -> [[], [2], [2, 2], [2, 2, 2]]
print(subsets_with_duplicates([3, 1]))      # -> [[], [1], [1, 3], [3]]
print(subsets_with_duplicates([]))          # -> [[]]
