"""
Container With Most Water (LeetCode 11)  — Medium
Pattern: Converging two pointers, move the limiting side

Problem
-------
Given heights of n vertical lines at x = 0..n-1, choose two lines that, with the
x-axis, form the container holding the most water. Area = min(h[i], h[j]) * (j - i).
Return the maximum area.
Example: height = [1, 8, 6, 2, 5, 4, 8, 3, 7] -> 49 (lines at index 1 and 8).

Brute force
-----------
Evaluate min(h[i], h[j]) * (j - i) for every pair i < j and keep the maximum. O(n^2)
time, O(1) space. The waste: once we know the shorter of the two walls, every pair
that keeps that shorter wall and brings the other wall CLOSER is provably worse
(width shrinks, height cannot exceed the short wall), yet the brute force still
evaluates all of them.

From brute force to optimal
---------------------------
Start with the widest container (left = 0, right = n - 1). Its height is capped by the
shorter wall. Any other container that still uses that shorter wall is narrower and
no taller, so it is strictly worse — we can discard the shorter wall entirely and
never consider it again. Move the pointer on the shorter side inward. Each step
eliminates one wall from all future consideration, so n - 1 steps examine everything
that could possibly beat the best so far. Ties can move either side.

Intuition
---------
Area is width times the smaller height. We trade width for the chance of a taller
pair, but only moving the SHORT side can ever increase the height; moving the tall
side can only lose width while the height stays capped by the same short wall.

Geometric view
--------------
Picture the skyline of bars with two walls L and R at the extremes. The water level
is the shorter wall. Each step, demolish the shorter wall and slide that pointer
inward; the water level can rise, the width shrinks by one. Track the best rectangle
seen as the two walls approach each other.

Steps
-----
1. left = 0, right = n - 1, best = 0.
2. While left < right: best = max(best, min(h[left], h[right]) * (right - left)).
3.   If h[left] < h[right], left += 1; else right -= 1.
4. Return best.

Complexity: O(n) time, O(1) space — each iteration moves one pointer inward.
Pitfalls: moving the taller side; computing area with the max height instead of min;
stopping when heights are equal instead of moving one side.
"""
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            best = max(best, min(height[left], height[right]) * (right - left))
            if height[left] < height[right]:
                left += 1          # shorter wall can never be part of a better pair
            else:
                right -= 1
        return best


def brute_force(height: List[int]) -> int:
    n = len(height)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            best = max(best, min(height[i], height[j]) * (j - i))
    return best


if __name__ == "__main__":
    s = Solution()
    assert s.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert s.maxArea([1, 1]) == 1
    assert s.maxArea([4, 3, 2, 1, 4]) == 16
    assert s.maxArea([1, 2, 1]) == 2
    for case in ([1, 8, 6, 2, 5, 4, 8, 3, 7], [1, 1], [4, 3, 2, 1, 4], [1, 2, 1], [2, 3, 10, 5, 7, 8, 9]):
        assert s.maxArea(case) == brute_force(case)
    print("ok")
