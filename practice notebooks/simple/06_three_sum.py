"""
3Sum (LeetCode 15)
Return all unique triplets that sum to zero.
  [-1, 0, 1, 2, -1, -4]  ->  [[-1, -1, 2], [-1, 0, 1]]

Idea: sort, fix the first number, then find the other two with two pointers
      (sum too small: move lo right, too big: move hi left). Skip equal neighbours to avoid duplicates.

Pseudocode:
  sort nums
  for i in range(n):
      skip if nums[i] == nums[i-1]
      lo, hi = i + 1, n - 1
      while lo < hi:
          total < 0 -> lo += 1;  total > 0 -> hi -= 1
          total == 0 -> record, move both, skip duplicates

Time O(n^2), space O(1) extra (besides sorting).
"""


def three_sum(nums):
    nums = sorted(nums)
    n = len(nums)
    result = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:     # same first number as before
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:                        # need bigger
                lo += 1
            elif total > 0:                      # need smaller
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo, hi = lo + 1, hi - 1
                while lo < hi and nums[lo] == nums[lo - 1]:   # skip duplicates
                    lo += 1
    return result


if __name__ == "__main__":
    print(three_sum([-1, 0, 1, 2, -1, -4]))   # [[-1, -1, 2], [-1, 0, 1]]
    print(three_sum([0, 0, 0, 0]))            # [[0, 0, 0]]
    print(three_sum([0, 1, 1]))               # []
