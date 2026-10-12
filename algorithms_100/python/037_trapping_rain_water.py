"""
Trapping Rain Water - Two Pointers with Running Walls

Given the heights of bars of width 1, return how many units of rain water
they trap between them:
[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] -> 6.
"""


# --- algorithm ---
def trap(height):
    """Water at i is min(tallest left, tallest right) - height[i]; the side
    with the lower running wall is settled, so move it. O(n), O(1) space."""
    left = 0
    right = len(height) - 1
    left_max = 0                    # tallest bar in height[0..left]
    right_max = 0                   # tallest bar in height[right..n-1]
    water = 0
    while left < right:
        left_max = max(left_max, height[left])
        right_max = max(right_max, height[right])
        if left_max < right_max:    # right wall taller: settle left
            water += left_max - height[left]
            left += 1
        else:                       # left wall as tall: settle right
            water += right_max - height[right]
            right -= 1
    return water


# --- try it ---
print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # -> 6
print(trap([4, 2, 0, 3, 2, 5]))                     # -> 9
print(trap([2, 0, 2]))                              # -> 2
print(trap([1, 2, 3]))                              # -> 0
print(trap([]))                                     # -> 0
