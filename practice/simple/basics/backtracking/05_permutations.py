"""
Permutations (basics: backtracking)
Return every ordering of a list of distinct numbers.
  [1, 2, 3]  ->  [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

Idea: fill positions left to right. Unlike subsets there is no start index: any number not
      yet in the path may go next, so a used[] flag per index remembers what is taken.

Pseudocode:
  backtrack():
      if len(path) == n: record a copy of path; return
      for i in 0 .. n-1:
          if used[i]: continue
          used[i] = True; path.append(nums[i])     # choose
          backtrack()
          path.pop(); used[i] = False              # unchoose
  backtrack()

Time O(n * n!) (n! orderings, O(n) to copy each), space O(n) recursion depth.
"""


def permutations(nums):
    result, path = [], []
    used = [False] * len(nums)           # used[i]: nums[i] is already in the path

    def backtrack():
        if len(path) == len(nums):       # every position filled: record a copy
            result.append(path[:])
            return
        for i in range(len(nums)):       # no start index: scan every number
            if used[i]:
                continue
            used[i] = True               # choose
            path.append(nums[i])
            backtrack()
            path.pop()                   # unchoose
            used[i] = False

    backtrack()
    return result


if __name__ == "__main__":
    print(permutations([1, 2, 3]))  # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    print(permutations([0, 1]))     # [[0, 1], [1, 0]]
    print(permutations([7]))        # [[7]]
