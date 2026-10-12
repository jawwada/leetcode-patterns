"""
Search in Rotated Sorted Array (LeetCode 33)
Find target's index in a sorted array that was rotated (distinct values), or -1.
  nums = [4, 5, 6, 7, 0, 1, 2], target = 0  ->  4

Idea: cut at mid and one half is always sorted. If target lies inside the
      sorted half's range go there, otherwise go to the other half.

Pseudocode:
  lo, hi = 0, n - 1
  while lo <= hi:
      mid = (lo + hi) // 2
      if nums[mid] == target: return mid
      if nums[lo] <= nums[mid]:            # left half sorted
          if nums[lo] <= target < nums[mid]: hi = mid - 1 else lo = mid + 1
      else:                                # right half sorted
          if nums[mid] < target <= nums[hi]: lo = mid + 1 else hi = mid - 1
  return -1

Time O(log n), space O(1).
"""


def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                     # target inside left half
            else:
                lo = mid + 1
        else:                                    # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                     # target inside right half
            else:
                hi = mid - 1
    return -1


if __name__ == "__main__":
    print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))  # 4
    print(search_rotated([4, 5, 6, 7, 0, 1, 2], 3))  # -1
    print(search_rotated([5, 1, 3], 5))              # 0
