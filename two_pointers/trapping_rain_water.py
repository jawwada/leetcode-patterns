"""
Trapping Rain Water (LeetCode 42)  — Hard
Pattern: Converging two pointers with running maxima

Problem
-------
Given an elevation map height[i] (bar widths 1), compute how much water it traps
after raining. Water above bar i is min(maxLeft(i), maxRight(i)) - height[i], if positive.
Example: height = [0,1,0,2,1,0,1,3,2,1,2,1] -> 6.

Brute force
-----------
For every index i, scan left to find the tallest bar, scan right to find the tallest
bar, and add min(maxL, maxR) - height[i]. O(n^2) time, O(1) space. The repeated work
is the two scans: maxLeft(i+1) is just max(maxLeft(i), height[i]), so recomputing it
from scratch for each i repeats almost the same scan n times.

From brute force to optimal
---------------------------
Step 1: precompute two arrays, maxLeft and maxRight, each in one pass; then one more
pass sums the water. O(n) time, O(n) space. Step 2 removes the arrays: the water at i
depends on min(maxLeft, maxRight), so we only need to know which side's maximum is
the smaller one. Walk two pointers inward keeping leftMax and rightMax. If
leftMax < rightMax, then the left pointer's water is fixed at leftMax - height[left]
no matter what lies between (some bar to the right is already at least rightMax >
leftMax), so we can settle it and advance left. Symmetrically for the right. Each
index is settled exactly once with O(1) state.

Intuition
---------
The water level at a bar is set by the LOWER of the tallest bars on each side. When
you know the left-side maximum is lower than something already seen on the right,
the right side's exact maximum is irrelevant for that bar — the left maximum wins.
That one-sided certainty is what lets two pointers replace two arrays.

Geometric view
--------------
Picture the skyline with two walls, L on the left and R on the right, each carrying
the tallest bar it has passed. Water fills from the lower wall's side: the pointer on
the side with the smaller running maximum steps inward and pours water up to that
maximum. The two running maxima only increase as the walls close in.

Steps
-----
1. left = 0, right = n - 1, leftMax = rightMax = 0, water = 0.
2. While left < right:
3.   if height[left] < height[right]: leftMax = max(leftMax, height[left]); water += leftMax - height[left]; left += 1.
4.   else: rightMax = max(rightMax, height[right]); water += rightMax - height[right]; right -= 1.
5. Return water.

Complexity: O(n) time, O(1) space — each iteration settles one index.
Pitfalls: comparing leftMax to rightMax but forgetting to update them before adding
water; adding negative water (update the max first, then the difference is >= 0);
the two-array version is acceptable but the interviewer will ask for O(1) space.
"""
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max = right_max = 0
        water = 0
        while left < right:
            if height[left] < height[right]:
                # right side has a bar >= height[right] > height[left], so the
                # water above `left` is bounded by the left maximum alone
                left_max = max(left_max, height[left])
                water += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                water += right_max - height[right]
                right -= 1
        return water


def brute_force(height: List[int]) -> int:
    water = 0
    for i in range(len(height)):
        max_left = max(height[:i + 1])
        max_right = max(height[i:])
        water += min(max_left, max_right) - height[i]
    return water


if __name__ == "__main__":
    s = Solution()
    assert s.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert s.trap([4, 2, 0, 3, 2, 5]) == 9
    assert s.trap([]) == 0
    assert s.trap([3, 2, 1]) == 0
    assert s.trap([5, 0, 5]) == 5
    for case in ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], [4, 2, 0, 3, 2, 5], [3, 2, 1], [5, 0, 5], [2, 0, 2, 0, 2]):
        assert s.trap(case) == brute_force(case)
    print("ok")
