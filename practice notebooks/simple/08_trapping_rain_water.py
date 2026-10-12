"""
Trapping Rain Water (LeetCode 42)
Given bar heights, return how much rain water is trapped between them.
  [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]  ->  6

Idea: water above a bar = min(tallest on left, tallest on right) - bar.
      Walk two pointers inward; the side with the lower bar is settled by its own
      running max, because the other side already has something taller.

Pseudocode:
  left, right = 0, n - 1
  while left < right:
      if h[left] < h[right]:
          left_max = max(left_max, h[left]); water += left_max - h[left]; left += 1
      else:
          right_max = max(right_max, h[right]); water += right_max - h[right]; right -= 1

Time O(n), space O(1).
"""


def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:          # left side is settled
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:                                     # right side is settled
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


if __name__ == "__main__":
    print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6
    print(trap([4, 2, 0, 3, 2, 5]))                     # 9
