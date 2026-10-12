"""
Permutations - Backtracking with a Used Array

Given an array of distinct integers, return all of its orderings, in any
order: [1, 2, 3] -> [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2],
[3, 2, 1]].
"""


# --- algorithm ---
def backtrack(nums, used, path, result):
    """Fill the next slot with each unused value in turn. n! leaves."""
    if len(path) == len(nums):
        result.append(path.copy())      # every slot filled: one permutation
        return
    for i in range(len(nums)):
        if used[i]:
            continue                    # nums[i] already sits in the path
        used[i] = True                  # choose
        path.append(nums[i])
        backtrack(nums, used, path, result)
        path.pop()                      # un-choose, in reverse order
        used[i] = False


def permutations(nums):
    """Used-array backtracking over n slots. O(n * n!) time."""
    used = [False] * len(nums)
    result = []
    backtrack(nums, used, [], result)
    return result


# --- try it ---
result = permutations([1, 2, 3])
print(result[0:3])                  # -> [[1, 2, 3], [1, 3, 2], [2, 1, 3]]
print(result[3:6])                  # -> [[2, 3, 1], [3, 1, 2], [3, 2, 1]]
print(permutations([0, 1]))         # -> [[0, 1], [1, 0]]
print(permutations([5]))            # -> [[5]]
print(len(permutations([1, 2, 3, 4, 5])))   # -> 120
