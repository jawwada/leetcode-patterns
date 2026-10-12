"""
Container With Most Water (LeetCode 11)
Pick two walls that, with the x-axis, hold the most water.
  [1, 8, 6, 2, 5, 4, 8, 3, 7]  ->  49   (walls 8 and 7, width 7)

Idea: start with the widest pair. The shorter wall limits the height, and any
      narrower pair keeping it can only be worse, so move the shorter wall inward.

Pseudocode:
  lo, hi = 0, n - 1
  while lo < hi:
      area = min(h[lo], h[hi]) * (hi - lo)
      best = max(best, area)
      move the shorter wall inward

Time O(n), space O(1).
"""


def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        area = min(height[lo], height[hi]) * (hi - lo)
        best = max(best, area)
        if height[lo] < height[hi]:      # shorter wall moves inward
            lo += 1
        else:
            hi -= 1
    return best


if __name__ == "__main__":
    print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # 49
    print(max_area([1, 1]))                        # 1
