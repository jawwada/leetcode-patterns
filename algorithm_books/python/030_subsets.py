"""
Subsets - Choose, Recurse, Un-Choose

Given an array of distinct integers, return every subset (the power set),
each exactly once, in any order:
[1, 2, 3] -> [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]].
"""


# --- algorithm ---
def backtrack(nums, start, path, result):
    """Record path, then extend it by each index from start on. 2^n calls."""
    result.append(path.copy())          # every node of the tree is a subset
    for i in range(start, len(nums)):
        path.append(nums[i])            # choose nums[i]
        backtrack(nums, i + 1, path, result)    # only later indices below
        path.pop()                      # un-choose: path is as it was


def subsets(nums):
    """Start-index backtracking, one tree node per subset. O(n * 2^n)."""
    result = []
    backtrack(nums, 0, [], result)
    return result


# --- try it ---
result = subsets([1, 2, 3])
print(result)   # -> [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
print(subsets([7]))                     # -> [[], [7]]
print(subsets([]))                      # -> [[]]
print(len(subsets([1, 2, 3, 4, 5])))    # -> 32
