"""
Container With Most Water - Always Move the Shorter Wall

Vertical lines with the given heights stand at x = 0, 1, ..., n - 1. Return
the most water two of them can hold together with the x-axis, where lines i
and j hold min(height[i], height[j]) * (j - i):
[1, 8, 6, 2, 5, 4, 8, 3, 7] -> 49.
"""


# --- algorithm ---
def max_area(height):
    """Start with the widest pair and move the shorter wall inward: it caps
    every narrower pair it belongs to. O(n) time, O(1) space."""
    left = 0
    right = len(height) - 1
    best = 0
    while left < right:
        width = right - left
        area = min(height[left], height[right]) * width
        best = max(best, area)
        if height[left] < height[right]:
            left += 1               # left wall is shorter: retire it
        else:
            right -= 1              # right wall is shorter or tied
    return best


# --- try it ---
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))    # -> 49
print(max_area([1, 1]))                         # -> 1
print(max_area([4, 3, 2, 1, 4]))                # -> 16
print(max_area([1, 2, 4, 3]))                   # -> 4
