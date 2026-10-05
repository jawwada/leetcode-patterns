"""
Trapping Rain Water (LeetCode 42) - Hard
Chapter: two_pointers
Pattern: Converging two pointers with running maxima

Given an elevation map height[i] of bars of width 1, return how much water it holds after
rain. Above bar i the water is min(tallest bar to its left, tallest to its right) - height[i].
Example: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] -> 6.
"""


# --- brute force ---
def brute_force(height):
    """For each bar scan left and right for the tallest bar. O(n^2) time, O(1) space."""
    water = 0
    for i in range(len(height)):
        max_left = 0
        for j in range(0, i + 1):  # tallest bar from 0 to i
            max_left = max(max_left, height[j])
        max_right = 0
        for j in range(i, len(height)):  # tallest bar from i to the end
            max_right = max(max_right, height[j])
        water += min(max_left, max_right) - height[i]
    return water


# --- optimal ---
def trap(height):
    """Two pointers inward; the lower side's water level is settled. O(n) time, O(1) space."""
    left = 0
    right = len(height) - 1
    left_max = 0
    right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            # the right side has a bar taller than height[left], so left_max alone sets the level
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


# --- try the brute force ---
print(brute_force([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # -> 6
print(brute_force([4, 2, 0, 3, 2, 5]))                     # -> 9
print(brute_force([3, 2, 1]))                              # -> 0
print(brute_force([5, 0, 5]))                              # -> 5


# --- try the optimal ---
print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # -> 6
print(trap([4, 2, 0, 3, 2, 5]))                     # -> 9
print(trap([3, 2, 1]))                              # -> 0
print(trap([5, 0, 5]))                              # -> 5
