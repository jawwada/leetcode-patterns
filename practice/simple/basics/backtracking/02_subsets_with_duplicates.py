"""
Subsets With Duplicates (basics: backtracking)
Return every distinct subset of a list that may contain duplicates.
  [1, 2, 2]  ->  [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]

Idea: sort so equal values sit side by side, then run the subsets template with one rule:
      on one level of the tree only the first of a run of equal values may be chosen,
      because a later copy at the same level would rebuild the very same subsets.

Pseudocode:
  sort nums
  backtrack(start):
      record a copy of path
      for i in start .. n-1:
          if i > start and nums[i] == nums[i-1]: continue    # value already tried here
          path.append(nums[i]); backtrack(i + 1); path.pop()
  backtrack(0)

Time O(n * 2^n), space O(n) recursion depth.
"""


def subsets_with_duplicates(nums):
    nums = sorted(nums)                  # equal values become adjacent
    result, path = [], []

    def backtrack(start):
        result.append(path[:])           # every node is a subset: record a copy
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                 # same value already tried on this level
            path.append(nums[i])         # choose
            backtrack(i + 1)             # only numbers after i
            path.pop()                   # unchoose

    backtrack(0)
    return result


if __name__ == "__main__":
    print(subsets_with_duplicates([1, 2, 2]))  # [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    print(subsets_with_duplicates([2, 1, 2]))  # [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    print(subsets_with_duplicates([3, 3, 3]))  # [[], [3], [3, 3], [3, 3, 3]]
