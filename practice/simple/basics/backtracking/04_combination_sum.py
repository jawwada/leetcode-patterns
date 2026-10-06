"""
Combination Sum (basics: backtracking)
Return every combination of distinct positive candidates that sums to target; reuse is allowed.
  candidates = [2, 3, 6, 7], target = 7  ->  [[2, 2, 3], [7]]

Idea: sort the candidates. Recurse from i (not i + 1) so the same candidate can be taken again.
      Once a candidate is bigger than what remains, every later one is too: break.

Pseudocode:
  cands = sorted(candidates)
  backtrack(start, remaining):
      if remaining == 0: record a copy of path; return
      for i in start .. n-1:
          if cands[i] > remaining: break      # too big, and so is every later one
          path.append(cands[i]); backtrack(i, remaining - cands[i]); path.pop()
  backtrack(0, target)

Time exponential in target / smallest candidate (the tree depth), space O(target / smallest).
"""


def combination_sum(candidates, target):
    cands = sorted(candidates)
    result, path = [], []

    def backtrack(start, remaining):
        if remaining == 0:                      # exact sum: record a copy
            result.append(path[:])
            return
        for i in range(start, len(cands)):
            if cands[i] > remaining:            # too big, and so is every later one
                break
            path.append(cands[i])               # choose
            backtrack(i, remaining - cands[i])  # i, not i + 1: reuse allowed
            path.pop()                          # unchoose

    backtrack(0, target)
    return result


if __name__ == "__main__":
    print(combination_sum([2, 3, 6, 7], 7))  # [[2, 2, 3], [7]]
    print(combination_sum([2, 3, 5], 8))     # [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    print(combination_sum([2], 1))           # []
