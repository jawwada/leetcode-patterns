"""
Subsets (LeetCode 78) - Medium
Chapter: backtracking
Pattern: Backtracking include/exclude decision tree

Given an array of distinct integers, return all possible subsets (the power set) in any
order, with no duplicate subsets.
Example: [1,2,3] -> [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]].
"""


# --- brute force ---
def brute_force(nums):
    """Each bitmask 0 .. 2^n - 1 names one subset; decode each from scratch. O(n * 2^n)."""
    n = len(nums)
    out = []
    for mask in range(2 ** n):
        subset = []
        for i in range(n):
            if (mask >> i) % 2 == 1:      # bit i of mask is 1: nums[i] is in this subset
                subset.append(nums[i])
        out.append(subset)
    return out


# --- optimal ---
def subsets(nums):
    """DFS over include / skip decisions sharing one path list. O(n * 2^n), the output size."""
    result = []
    dfs(nums, 0, [], result)
    return result


def dfs(nums, start, path, result):
    result.append(path[:])                # every node of the decision tree is a subset
    for i in range(start, len(nums)):
        path.append(nums[i])              # choose nums[i]
        dfs(nums, i + 1, path, result)    # only later indices may follow: no duplicates
        path.pop()                        # un-choose, then try the next element


# --- try the brute force ---
# any order is accepted, so the demos print the subsets sorted
print(sorted(brute_force([1, 2, 3])))   # -> [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
print(brute_force([0]))                 # -> [[], [0]]
print(brute_force([]))                  # -> [[]]
print(len(brute_force([1, 2, 3, 4, 5])))   # -> 32


# --- try the optimal ---
# any order is accepted, so the demos print the subsets sorted
print(sorted(subsets([1, 2, 3])))       # -> [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
print(subsets([0]))                     # -> [[], [0]]
print(subsets([]))                      # -> [[]]
print(len(subsets([1, 2, 3, 4, 5])))    # -> 32
