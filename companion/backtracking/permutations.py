"""
Permutations (LeetCode 46) - Medium
Chapter: backtracking
Pattern: Backtracking with a used-set

Given an array of distinct integers, return all possible orderings (permutations) of its
elements, in any order.
Example: [1,2,3] -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]. Example: [1] -> [[1]].
"""
from itertools import product     # every sequence of n picks from a pool, repeats allowed


# --- brute force ---
def brute_force(nums):
    """Every length-n sequence over nums (n^n of them), keep those with no repeat. O(n^n * n)."""
    n = len(nums)
    out = []
    for seq in product(nums, repeat=n):
        if len(set(seq)) == n:            # no value repeated; checked only once fully built
            out.append(list(seq))
    return out


# --- optimal ---
def permute(nums):
    """DFS placing one unused value per level; used flags refuse repeats early. O(n! * n)."""
    result = []
    used = [False] * len(nums)
    dfs(nums, used, [], result)
    return result


def dfs(nums, used, path, result):
    if len(path) == len(nums):
        result.append(path[:])
        return
    for i in range(len(nums)):
        if used[i]:
            continue                      # already in the path: this branch is dead
        used[i] = True
        path.append(nums[i])
        dfs(nums, used, path, result)
        path.pop()
        used[i] = False                   # restore for the sibling branches


# --- try the brute force ---
print(brute_force([1, 2, 3]))   # -> [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
print(brute_force([0, 1]))      # -> [[0, 1], [1, 0]]
print(brute_force([1]))         # -> [[1]]
print(len(brute_force([1, 2, 3, 4, 5])))   # -> 120


# --- try the optimal ---
print(permute([1, 2, 3]))       # -> [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
print(permute([0, 1]))          # -> [[0, 1], [1, 0]]
print(permute([1]))             # -> [[1]]
print(len(permute([1, 2, 3, 4, 5])))   # -> 120
