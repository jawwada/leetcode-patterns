"""
Combinations n Choose k (basics: backtracking)
Return every combination of k numbers chosen from 1..n.
  n = 4, k = 2  ->  [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

Idea: the subsets template, but record only when the path holds k numbers.
      Prune: once the numbers left (i..n) are fewer than the open slots, stop the loop.

Pseudocode:
  backtrack(start):
      if len(path) == k: record a copy of path; return
      for i in start .. n:
          if n - i + 1 < k - len(path): break    # numbers left < open slots
          path.append(i); backtrack(i + 1); path.pop()
  backtrack(1)

Time O(k * C(n, k)) (C(n, k) results, O(k) to copy each), space O(k) recursion depth.
"""


def combinations(n, k):
    result, path = [], []

    def backtrack(start):
        if len(path) == k:               # path is full: record a copy
            result.append(path[:])
            return
        for i in range(start, n + 1):
            if n - i + 1 < k - len(path):  # numbers left (i..n) < open slots
                break
            path.append(i)               # choose
            backtrack(i + 1)             # only numbers after i
            path.pop()                   # unchoose

    backtrack(1)
    return result


if __name__ == "__main__":
    print(combinations(4, 2))  # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    print(combinations(3, 3))  # [[1, 2, 3]]
    print(combinations(3, 1))  # [[1], [2], [3]]
