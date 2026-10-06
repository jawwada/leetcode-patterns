"""
Subsets (basics: backtracking)
Return every subset (the power set) of a list of distinct numbers.
  [1, 2, 3]  ->  [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

Idea: every node of the recursion tree is a subset, so record the path on entry.
      Then for each later number: choose it, recurse from the next index, unchoose it.
      Recursing from i + 1 means no number is picked twice or out of order.

Pseudocode:
  backtrack(start):
      record a copy of path
      for i in start .. n-1:
          path.append(nums[i])      # choose
          backtrack(i + 1)          # only numbers after i
          path.pop()                # unchoose
  backtrack(0)

Time O(n * 2^n) (2^n subsets, O(n) to copy each), space O(n) recursion depth.
"""


def subsets(nums):
    result, path = [], []

    def backtrack(start):
        result.append(path[:])           # every node is a subset: record a copy
        for i in range(start, len(nums)):
            path.append(nums[i])         # choose
            backtrack(i + 1)             # only numbers after i
            path.pop()                   # unchoose

    backtrack(0)
    return result


if __name__ == "__main__":
    print(subsets([1, 2, 3]))  # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    print(subsets([5, 7]))     # [[], [5], [5, 7], [7]]
    print(subsets([]))         # [[]]
