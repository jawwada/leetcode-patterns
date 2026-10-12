"""
Largest Rectangle in Histogram - Monotonic Increasing Stack

Given bar heights of a histogram whose bars all have width 1, return the area
of the largest rectangle that fits inside it:
[2, 1, 5, 6, 2, 3] -> 10 (the bars 5 and 6, height 5, width 2).
"""


# --- algorithm ---
def largest_rectangle_area(heights):
    """Stack of indices with rising heights; a shorter bar ends the popped
    bar's rectangle on the right. O(n) time, O(n) space."""
    bars = heights + [0]            # the 0 sentinel flushes the stack
    stack = []                      # indices; heights never fall
    best = 0
    for i in range(len(bars)):
        while len(stack) > 0 and bars[stack[-1]] > bars[i]:
            height = bars[stack.pop()]      # its rectangle ends at i - 1
            if len(stack) > 0:
                left = stack[-1] + 1        # just right of the new stack top
            else:
                left = 0                    # empty stack: reaches index 0
            width = i - left
            best = max(best, height * width)
        stack.append(i)
    return best


# --- try it ---
print(largest_rectangle_area([2, 1, 5, 6, 2, 3]))  # -> 10
print(largest_rectangle_area([2, 4]))              # -> 4
print(largest_rectangle_area([1, 2, 3]))           # -> 4
print(largest_rectangle_area([3, 3, 3]))           # -> 9
