"""
Largest Rectangle in Histogram (LeetCode 84) - Medium-Hard
Area: monotonic stack
Key operations: push index, pop while top is taller, width from the new top, sentinel 0 flushes the stack

Given the heights of a histogram's bars (each bar has width 1), return the area of the largest
rectangle that fits entirely inside the histogram.
Example: [2, 1, 5, 6, 2, 3] -> 10 (height 5 spanning the bars 5 and 6)
"""
from typing import List


# --- brute force ---
def brute_force(heights: List[int]) -> int:
    """For each bar use its height and walk left and right while the neighbours are at least as
    tall. O(n^2): the same walls are rediscovered by every bar of a plateau."""
    best = 0
    for i, h in enumerate(heights):
        left = right = i
        while left > 0 and heights[left - 1] >= h:
            left -= 1
        while right < len(heights) - 1 and heights[right + 1] >= h:
            right += 1
        best = max(best, h * (right - left + 1))
    return best


# --- optimal ---
def solve(heights: List[int]) -> int:
    """Stack of bar indices whose heights increase bottom to top. A bar shorter than the top closes
    the top: the closed bar's rectangle runs from the bar below it (exclusive) to i (exclusive).
    A sentinel 0 at the end closes every bar. Each index is pushed once and popped once: O(n)."""
    bars = heights + [0]  # the sentinel is shorter than every real bar
    best = 0
    stack = []  # indices; bars[stack] is increasing from bottom to top
    for i, h in enumerate(bars):
        while stack and bars[stack[-1]] > h:
            top = stack.pop()
            left = stack[-1] if stack else -1
            area = bars[top] * (i - left - 1)
            best = max(best, area)
        stack.append(i)
    return best


# --- demo ---
def demo():
    return solve([2, 1, 5, 6, 2, 3])


# --- bugs ---
BUGS = [
    {
        "replace": "            area = bars[top] * (i - left - 1)",
        "with":    "            area = bars[top] * (i - left)",
        "fix": "the width is i - left - 1: both walls are exclusive",
        "why": "The rectangle lies strictly between the two shorter bars at left and i, so it is i - left - 1 wide; counting one wall overstates every area, [2, 1, 5, 6, 2, 3] gives 15.",
        "decoys": [
            {"line": "        while stack and bars[stack[-1]] > h:", "change": "should be < h"},
            {"line": "            left = stack[-1] if stack else -1", "change": "should be stack[0]"},
            {"line": "        stack.append(i)", "change": "should push h, not i"},
        ],
    },
    {
        "replace": "            left = stack[-1] if stack else -1",
        "with":    "            left = stack[-1] if stack else 0",
        "fix": "an empty stack means no shorter bar on the left, so the left wall is at -1",
        "why": "With no shorter bar to the left the rectangle starts at index 0, so the exclusive wall is -1; using 0 drops one column, [2, 2, 2] gives 4 instead of 6.",
        "decoys": [
            {"line": "            area = bars[top] * (i - left - 1)", "change": "should be bars[top] * (i - left + 1)"},
            {"line": "    bars = heights + [0]  # the sentinel is shorter than every real bar", "change": "sentinel should be -1"},
            {"line": "            best = max(best, area)", "change": "should be best = area"},
        ],
    },
    {
        "replace": "    bars = heights + [0]  # the sentinel is shorter than every real bar",
        "with":    "    bars = list(heights)  # the sentinel is shorter than every real bar",
        "fix": "append a sentinel 0 so the bars still on the stack at the end get closed",
        "why": "Without the sentinel nothing pops the final increasing run, so [1, 2, 3, 4, 5] returns 0.",
        "decoys": [
            {"line": "            top = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "    stack = []  # indices; bars[stack] is increasing from bottom to top", "change": "should start with 0 pushed"},
            {"line": "    return best", "change": "should return best or bars[0]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
