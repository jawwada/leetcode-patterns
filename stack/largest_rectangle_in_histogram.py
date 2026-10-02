"""
Largest Rectangle in Histogram (LeetCode 84)  — Hard
Pattern: Monotonic stack

Problem
-------
Given bar heights (each of width 1), return the area of the largest rectangle that fits
entirely inside the histogram.
Example: heights = [2,1,5,6,2,3] -> 10 (height 5 spanning the bars 5 and 6).

Brute force
-----------
For each bar i, treat heights[i] as the rectangle's height and expand left and right while
neighbours are >= heights[i]; area = heights[i] * width. O(n^2) time, O(1) space. The wasted
work: the expansion for bar i re-walks bars that an earlier, shorter bar already walked, and
finds the same boundaries ("nearest shorter bar on each side") repeatedly.

From brute force to optimal
---------------------------
The redundancy is recomputing "nearest shorter bar to the left/right" by walking. Observation:
both boundaries can be found by a single left-to-right pass with a stack of indices whose
heights are non-decreasing. When bar i is shorter than the stack top, i is the top's right
boundary, and the element beneath the top is its left boundary (the nearest shorter bar to
its left, by the stack's ordering). So pop it, compute its area, and keep popping while the
top is taller than i. Appending a sentinel height 0 flushes every remaining bar. Each index
is pushed and popped once.

Intuition
---------
A bar's best rectangle extends until the first shorter bar on each side. A stack sorted by
height lets each bar discover its right boundary at the moment a shorter bar arrives, and
its left boundary is simply its predecessor in the stack.

Geometric view
--------------
Sweep a vertical line left to right. The stack holds a rising staircase of "open" bars. When
the sweep line meets a bar lower than the staircase top, the top steps are closed one by one:
each closed step's rectangle spans from just after the step below it to just before the sweep
line, with the step's own height.

Steps
-----
1. stack = [], best = 0. Iterate i over heights plus a trailing 0 sentinel.
2. While stack and heights[stack[-1]] > h: top = pop; left = stack[-1] if stack else -1;
   best = max(best, heights[top] * (i - left - 1)).
3. Push i.
4. Return best.

Complexity: O(n) time, O(n) space — each index is pushed and popped at most once.
Pitfalls: Width formula (i - left - 1, not i - left); popping on >= vs > (both give correct
area, but be consistent); forgetting the sentinel or a final flush loop.
"""
from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []                                   # indices with non-decreasing heights
        best = 0
        for i, h in enumerate(heights + [0]):        # sentinel 0 flushes the stack
            while stack and heights[stack[-1]] > h:
                top = stack.pop()                    # i is top's first shorter bar on the right
                left = stack[-1] if stack else -1    # nearest shorter bar on the left
                best = max(best, heights[top] * (i - left - 1))
            stack.append(i)
        return best


def brute_force(heights: List[int]) -> int:
    best = 0
    for i, h in enumerate(heights):
        left = right = i                             # re-walks the neighbours for every bar
        while left > 0 and heights[left - 1] >= h:
            left -= 1
        while right < len(heights) - 1 and heights[right + 1] >= h:
            right += 1
        best = max(best, h * (right - left + 1))
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [[2, 1, 5, 6, 2, 3], [2, 4], [1], [2, 2, 2], [5, 4, 3, 2, 1], [0, 0], [1, 2, 3, 4, 5]]
    assert s.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10
    assert s.largestRectangleArea([2, 4]) == 4
    assert s.largestRectangleArea([1]) == 1
    assert s.largestRectangleArea([2, 2, 2]) == 6
    assert s.largestRectangleArea([1, 2, 3, 4, 5]) == 9
    for c in cases:
        assert s.largestRectangleArea(c) == brute_force(c)
    print("ok")
