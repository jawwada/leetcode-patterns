"""
Binary Search Variants (basics: searches)
In a sorted list: find x, the first index >= x, the first index > x, and how often x occurs.
  nums = [1, 2, 2, 2, 5, 7], x = 2  ->  index 2, lower 1, upper 4, count 3

Idea: look at the middle and drop the half that cannot hold the answer.
      The bounds search the half-open range [lo, hi): everything left of lo is too small,
      everything from hi on qualifies, so where lo meets hi is the first qualifying index.

Pseudocode:
  binary_search: lo, hi = 0, len - 1           # closed range [lo, hi]
      while lo <= hi:
          mid = (lo + hi) // 2
          if nums[mid] == x: return mid
          if nums[mid] < x: lo = mid + 1 else hi = mid - 1
      return -1

  lower_bound: lo, hi = 0, len                 # half-open [lo, hi); first i with nums[i] >= x
      while lo < hi:
          mid = (lo + hi) // 2
          if nums[mid] < x: lo = mid + 1 else hi = mid   # mid qualifies: keep it
      return lo

  upper_bound: same loop, test nums[mid] <= x  # first i with nums[i] > x
  count = upper_bound - lower_bound

Time O(log n) each, space O(1).
"""


def binary_search(nums, x):
    lo, hi = 0, len(nums) - 1            # closed range [lo, hi]
    while lo <= hi:                      # lo == hi is still one candidate
        mid = (lo + hi) // 2
        if nums[mid] == x:
            return mid
        if nums[mid] < x:
            lo = mid + 1                 # x is to the right
        else:
            hi = mid - 1                 # x is to the left
    return -1


def lower_bound(nums, x):
    lo, hi = 0, len(nums)                # half-open, may return len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x:
            lo = mid + 1                 # too small, answer is right of mid
        else:
            hi = mid                     # mid qualifies, keep it in range
    return lo


def upper_bound(nums, x):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= x:               # only change: <= also skips every x
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_occurrences(nums, x):
    return upper_bound(nums, x) - lower_bound(nums, x)   # every x sits in [lower, upper)


if __name__ == "__main__":
    nums = [1, 2, 2, 2, 5, 7]
    print(binary_search(nums, 2), binary_search(nums, 3))    # 2 -1
    print(lower_bound(nums, 2), upper_bound(nums, 2))        # 1 4
    print(count_occurrences(nums, 2))                        # 3
    print(lower_bound(nums, 8), count_occurrences(nums, 3))  # 6 0
