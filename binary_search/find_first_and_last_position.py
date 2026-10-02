"""
Find First and Last Position of Element in Sorted Array (LeetCode 34)  — Medium
Pattern: Binary search for a boundary (lower / upper bound)

Problem
-------
Given a non-decreasing array `nums` and a `target`, return [first, last] indices of target, or
[-1, -1] if absent. Must be O(log n).
Example: nums = [5,7,7,8,8,10], target = 8 -> [3, 4].

Brute force
-----------
Scan once recording the first and last index where nums[i] == target. O(n) time, O(1) space.
The wasted work: every element not equal to target still costs a comparison, and even the
"find any occurrence then expand outward" variant degrades to O(n) when the array is all target.

From brute force to optimal
---------------------------
The redundancy is walking through the run of equal values. Observation: "nums[i] >= target" is a
monotone predicate (F...F T...T) whose first True is the left boundary, and "nums[i] > target" is
another monotone predicate whose first True is one past the right boundary. Each boundary is a
single lower-bound binary search, independent of how long the run of targets is. Two searches,
O(log n) total, no expansion step.

Intuition
---------
Reduce "find the range" to "find two boundaries", and make each boundary the first index where a
yes/no question flips. lower_bound(target) gives the first index with value >= target;
lower_bound(target+1) gives the first index with value > target, i.e. last+1. If the first index
is out of range or does not hold target, it is absent.

Geometric view
--------------
Draw the sorted array as stairs. The run of equal targets is a flat step. One search lands on the
left edge of that step (first >= target), the other lands on the left edge of the NEXT step
(first > target). The answer is [left_edge, next_edge - 1].

Steps
-----
1. lower(x): lo = 0, hi = n; while lo < hi: mid; if nums[mid] < x: lo = mid+1 else hi = mid; return lo.
2. first = lower(target).
3. If first == n or nums[first] != target: return [-1, -1].
4. last = lower(target + 1) - 1.
5. Return [first, last].

Complexity: O(log n) time, O(1) space — two half-open binary searches.
Pitfalls: using the closed-interval template (hi = n-1) and then indexing nums[n]; expanding
linearly from a found index (worst case O(n)); off-by-one on `last`.
"""
from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def lower(x: int) -> int:            # first index i with nums[i] >= x, or n
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        first = lower(target)
        if first == len(nums) or nums[first] != target:
            return [-1, -1]
        return [first, lower(target + 1) - 1]   # first index > target, minus one


def brute_force(nums: List[int], target: int) -> List[int]:
    first = last = -1
    for i, x in enumerate(nums):
        if x == target:
            if first == -1:
                first = i
            last = i
    return [first, last]


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([5, 7, 7, 8, 8, 10], 8, [3, 4]),
        ([5, 7, 7, 8, 8, 10], 6, [-1, -1]),
        ([], 0, [-1, -1]),
        ([2, 2, 2, 2], 2, [0, 3]),
        ([1, 3], 3, [1, 1]),
    ]
    for nums, t, want in cases:
        assert s.searchRange(nums, t) == want
        assert brute_force(nums, t) == want
    print("ok")
