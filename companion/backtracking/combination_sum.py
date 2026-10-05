"""
Combination Sum (LeetCode 39) - Medium
Chapter: backtracking
Pattern: Backtracking with start index and sum pruning

Given distinct positive candidates and a target, return all unique combinations (each
candidate may be reused any number of times) that sum to target; order inside a
combination does not matter.
Example: candidates=[2,3,6,7], target=7 -> [[2,2,3],[7]].
"""
from itertools import combinations_with_replacement   # every multiset of a given size


# --- brute force ---
def brute_force(candidates, target):
    """Build every multiset of every possible size, keep those summing to target. Exponential."""
    out = []
    max_size = target // min(candidates)          # more picks than this always overshoot
    for size in range(1, max_size + 1):
        for combo in combinations_with_replacement(candidates, size):
            if sum(combo) == target:              # built fully, checked late
                out.append(list(combo))
    return out


# --- optimal ---
def combination_sum(candidates, target):
    """DFS with a start index (no reordered duplicates) and a sum bound to prune. Exponential."""
    candidates = sorted(candidates)
    result = []
    dfs(candidates, 0, target, [], result)
    return result


def dfs(candidates, start, remaining, path, result):
    if remaining == 0:
        result.append(path[:])
        return
    for i in range(start, len(candidates)):
        if candidates[i] > remaining:
            break                                 # sorted: every later candidate is too big too
        path.append(candidates[i])
        dfs(candidates, i, remaining - candidates[i], path, result)   # same i: reuse allowed
        path.pop()


# --- try the brute force ---
# any order is accepted, so the demos print the combinations sorted
print(sorted(brute_force([2, 3, 6, 7], 7)))   # -> [[2, 2, 3], [7]]
print(sorted(brute_force([2, 3, 5], 8)))      # -> [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
print(brute_force([2], 1))                    # -> []
print(brute_force([1], 2))                    # -> [[1, 1]]


# --- try the optimal ---
# any order is accepted, so the demos print the combinations sorted
print(sorted(combination_sum([2, 3, 6, 7], 7)))   # -> [[2, 2, 3], [7]]
print(sorted(combination_sum([2, 3, 5], 8)))      # -> [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
print(combination_sum([2], 1))                    # -> []
print(combination_sum([1], 2))                    # -> [[1, 1]]
