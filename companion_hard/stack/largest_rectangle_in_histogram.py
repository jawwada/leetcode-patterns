"""
Largest Rectangle in Histogram (LeetCode 84) - Hard
Chapter: stack
Pattern: Monotonic stack

Given bar heights of width 1, return the area of the largest rectangle that fits entirely
inside the histogram.
Example: heights = [2, 1, 5, 6, 2, 3] -> 10 (height 5 spanning the bars 5 and 6).
"""


# --- brute force ---
def brute_force(heights):
    """Expand each bar left and right while neighbours are as tall. O(n^2) time, O(1) space."""
    best = 0
    for i in range(len(heights)):
        h = heights[i]
        left = i
        right = i
        while left > 0 and heights[left - 1] >= h:          # re-walks bars walked before
            left -= 1
        while right < len(heights) - 1 and heights[right + 1] >= h:
            right += 1
        best = max(best, h * (right - left + 1))
    return best


# --- optimal ---
def largest_rectangle_area(heights):
    """Stack of indices with rising heights; a shorter bar closes the taller ones. O(n) time."""
    bars = heights + [0]                        # the final 0 flushes every open bar
    stack = []                                  # indices whose heights never decrease
    best = 0
    for i in range(len(bars)):
        while stack and bars[stack[-1]] > bars[i]:
            top = stack.pop()                   # bar i is the first shorter bar to its right
            if stack:
                left = stack[-1]                # nearest shorter bar to its left
            else:
                left = -1
            best = max(best, bars[top] * (i - left - 1))
        stack.append(i)
    return best


# --- try the brute force ---
print(brute_force([2, 1, 5, 6, 2, 3]))   # -> 10
print(brute_force([2, 4]))               # -> 4
print(brute_force([2, 2, 2]))            # -> 6
print(brute_force([1, 2, 3, 4, 5]))      # -> 9


# --- try the optimal ---
print(largest_rectangle_area([2, 1, 5, 6, 2, 3]))   # -> 10
print(largest_rectangle_area([2, 4]))               # -> 4
print(largest_rectangle_area([2, 2, 2]))            # -> 6
print(largest_rectangle_area([1, 2, 3, 4, 5]))      # -> 9
