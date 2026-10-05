"""
Container With Most Water (LeetCode 11) - Medium
Chapter: two_pointers
Pattern: Converging two pointers, move the limiting side

Given heights of n vertical lines at x = 0..n-1, choose two lines that together with
the x-axis form the container holding the most water; the area is
min(h[i], h[j]) * (j - i). Return the maximum area.
Example: height = [1, 8, 6, 2, 5, 4, 8, 3, 7] -> 49 (indices 1 and 8).
"""


# --- brute force ---
def brute_force(height):
    """Measure every pair of walls. O(n^2) time, O(1) space."""
    n = len(height)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = min(height[i], height[j]) * (j - i)  # water level is the shorter wall
            best = max(best, area)
    return best


# --- optimal ---
def max_area(height):
    """Start widest; always move the shorter wall inward. O(n) time, O(1) space."""
    left = 0
    right = len(height) - 1
    best = 0
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        best = max(best, area)
        if height[left] < height[right]:
            left += 1  # the shorter wall can never be part of a better pair
        else:
            right -= 1
    return best


# --- try the brute force ---
print(brute_force([1, 8, 6, 2, 5, 4, 8, 3, 7]))    # -> 49
print(brute_force([1, 1]))                         # -> 1
print(brute_force([4, 3, 2, 1, 4]))                # -> 16
print(brute_force([2, 3, 10, 5, 7, 8, 9]))         # -> 36


# --- try the optimal ---
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))    # -> 49
print(max_area([1, 1]))                         # -> 1
print(max_area([4, 3, 2, 1, 4]))                # -> 16
print(max_area([2, 3, 10, 5, 7, 8, 9]))         # -> 36
