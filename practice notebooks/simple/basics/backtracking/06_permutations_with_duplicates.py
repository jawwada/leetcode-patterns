"""
Permutations With Duplicates (basics: backtracking)
Return every distinct ordering of a list that may contain duplicates.
  [1, 1, 2]  ->  [[1, 1, 2], [1, 2, 1], [2, 1, 1]]

Idea: sort so equal values sit side by side, then use equal values strictly left to right:
      a copy whose left twin is not in the path yet is skipped, so each ordering is built once.

Pseudocode:
  sort nums
  backtrack():
      if len(path) == n: record a copy of path; return
      for i in 0 .. n-1:
          if used[i]: continue
          if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue   # twin goes first
          used[i] = True; path.append(nums[i])     # choose
          backtrack()
          path.pop(); used[i] = False              # unchoose
  backtrack()

Time O(n * n!) worst case (all values distinct), space O(n) recursion depth.
"""


def permutations_with_duplicates(nums):
    nums = sorted(nums)                  # equal values become adjacent
    result, path = [], []
    used = [False] * len(nums)           # used[i]: nums[i] is already in the path

    def backtrack():
        if len(path) == len(nums):       # every position filled: record a copy
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue                 # left twin not used yet: this copy waits
            used[i] = True               # choose
            path.append(nums[i])
            backtrack()
            path.pop()                   # unchoose
            used[i] = False

    backtrack()
    return result


if __name__ == "__main__":
    print(permutations_with_duplicates([1, 1, 2]))  # [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    print(permutations_with_duplicates([2, 1, 2]))  # [[1, 2, 2], [2, 1, 2], [2, 2, 1]]
    print(permutations_with_duplicates([3, 3]))     # [[3, 3]]
