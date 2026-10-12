"""
Combination Sum II (LeetCode 40)
Return every unique combination of candidates (each used at most once) that sums to target.
  candidates = [10, 1, 2, 7, 6, 1, 5], target = 8  ->  [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]

Idea: sort first. Then DFS picking indices left to right:
      - stop the loop once a number is bigger than what is left (all later ones are bigger too)
      - skip a number equal to its left sibling at the same level (it would repeat a combination)

Pseudocode:
  sort nums
  dfs(start, remaining):
      if remaining == 0: record a copy of path
      for i in start .. n-1:
          if nums[i] > remaining: break
          if i > start and nums[i] == nums[i-1]: continue
          path.append(nums[i]); dfs(i + 1, remaining - nums[i]); path.pop()

Time O(2^n) worst case, space O(n) for the path.
"""


def combination_sum2(candidates, target):
    nums = sorted(candidates)
    result, path = [], []

    def dfs(start, remaining):
        if remaining == 0:                            # exact sum: record
            result.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:                   # too big, and so is everything after
                break
            if i > start and nums[i] == nums[i - 1]:  # duplicate sibling: same subtree
                continue
            path.append(nums[i])
            dfs(i + 1, remaining - nums[i])           # i + 1: each index used once
            path.pop()

    dfs(0, target)
    return result


if __name__ == "__main__":
    print(combination_sum2([10, 1, 2, 7, 6, 1, 5], 8))  # [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    print(combination_sum2([2, 5, 2, 1, 2], 5))         # [[1, 2, 2], [5]]
