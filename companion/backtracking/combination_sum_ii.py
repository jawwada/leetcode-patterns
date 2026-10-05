"""
Combination Sum II (LeetCode 40) - Medium
Chapter: backtracking
Pattern: Backtracking with sort + skip-duplicates-at-same-depth

Given candidates (which may repeat) and a target, return all unique combinations summing
to target where each candidate index is used at most once.
Example: candidates=[10,1,2,7,6,1,5], target=8 -> [[1,1,6],[1,2,5],[1,7],[2,6]].
"""


# --- brute force ---
def brute_force(candidates, target):
    """Every index subset by bitmask; sum it; collapse duplicates in a set. O(n * 2^n)."""
    n = len(candidates)
    seen = set()
    for mask in range(2 ** n):
        chosen = []
        for i in range(n):
            if (mask >> i) % 2 == 1:          # bit i of mask is 1: candidates[i] is chosen
                chosen.append(candidates[i])
        if sum(chosen) == target:             # summed only after full decoding
            seen.add(tuple(sorted(chosen)))   # duplicates collapse here, after the fact
    out = []
    for combo in seen:
        out.append(list(combo))
    return out


# --- optimal ---
def combination_sum2(candidates, target):
    """Sort, DFS with a sum bound, skip equal values at the same depth. Exponential, pruned."""
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
            break                                 # sorted: later values are even bigger
        if i > start and candidates[i] == candidates[i - 1]:
            continue                              # same value as the sibling before: same subtree
        path.append(candidates[i])
        dfs(candidates, i + 1, remaining - candidates[i], path, result)   # i + 1: each index once
        path.pop()


# --- try the brute force ---
# any order is accepted, so the demos print the combinations sorted
cands = [10, 1, 2, 7, 6, 1, 5]
print(sorted(brute_force(cands, 8)))           # -> [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
print(sorted(brute_force([2, 5, 2, 1, 2], 5)))          # -> [[1, 2, 2], [5]]
print(brute_force([2, 2], 5))                           # -> []
print(brute_force([1, 1, 1, 1], 4))                     # -> [[1, 1, 1, 1]]


# --- try the optimal ---
# any order is accepted, so the demos print the combinations sorted
cands = [10, 1, 2, 7, 6, 1, 5]
print(sorted(combination_sum2(cands, 8)))      # -> [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
print(sorted(combination_sum2([2, 5, 2, 1, 2], 5)))          # -> [[1, 2, 2], [5]]
print(combination_sum2([2, 2], 5))                           # -> []
print(combination_sum2([1, 1, 1, 1], 4))                     # -> [[1, 1, 1, 1]]
