"""
Combination Sum - Unlimited Reuse with a Start Index

Given distinct positive integers and a target, return every combination of
them that sums to the target; a number may be used any number of times, and
order does not matter: [2, 3, 6, 7], target 7 -> [[2, 2, 3], [7]].
"""


# --- algorithm ---
def backtrack(candidates, start, remaining, path, result):
    """Extend path from index start on, reusing i; break at an overshoot."""
    if remaining == 0:
        result.append(path.copy())      # exact hit: one combination
        return
    for i in range(start, len(candidates)):
        if candidates[i] > remaining:
            break                       # sorted: every later one is bigger
        path.append(candidates[i])      # choose
        # pass i, not i + 1: the same candidate may be chosen again
        backtrack(candidates, i, remaining - candidates[i], path, result)
        path.pop()                      # un-choose


def combination_sum(candidates, target):
    """Sort, then start-index backtracking that may reuse i. Exponential."""
    candidates = sorted(candidates)     # makes the break above valid
    result = []
    backtrack(candidates, 0, target, [], result)
    return result


# --- try it ---
print(combination_sum([2, 3, 6, 7], 7))   # -> [[2, 2, 3], [7]]
print(combination_sum([2, 3, 5], 8))      # -> [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
print(combination_sum([7, 3, 2], 7))      # -> [[2, 2, 3], [7]]
print(combination_sum([2], 1))            # -> []
