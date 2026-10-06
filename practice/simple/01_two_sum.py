"""
Two Sum (LeetCode 1)
Return the indices of the two numbers that add up to target.
  nums = [3, 5, 2, 7, 11], target = 9  ->  [2, 3]   (2 + 7)

Idea: for each number, the partner it needs is already known (target - num).
      Remember every number seen so far in a dict, so the partner lookup is O(1).

Pseudocode:
  seen = {}                       # value -> index
  for i, num in nums:
      need = target - num
      if need in seen: return [seen[need], i]
      seen[num] = i               # add AFTER the check (no self-pairing)

Time O(n), space O(n).
"""


def two_sum(nums, target):
    seen = {}                            # value -> index
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:                 # partner was seen earlier
            return [seen[need], i]
        seen[num] = i                    # store after the check
    return []


if __name__ == "__main__":
    print(two_sum([3, 5, 2, 7, 11], 9))  # [2, 3]
    print(two_sum([3, 3], 6))            # [0, 1]
