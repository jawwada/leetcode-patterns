"""
Find Peak Element (LeetCode 162)  — Medium
Pattern: Binary search on a monotone predicate

Problem
-------
A peak is an element strictly greater than its neighbours. Given `nums` where nums[i] != nums[i+1]
and imaginary nums[-1] = nums[n] = -inf, return the index of ANY peak in O(log n).
Example: nums = [1,2,1,3,5,6,4] -> 1 or 5 (both are peaks).

Brute force
-----------
Scan and return the first i with nums[i] > nums[i+1] (or n-1 if none). O(n) time, O(1) space.
The wasted work: each comparison only confirms "still climbing" for one step, though the fact
that we are climbing guarantees a peak exists somewhere ahead — we could leap instead of step.

From brute force to optimal
---------------------------
The redundancy is walking uphill one step at a time. Observation: if nums[mid] < nums[mid+1] we
are on an ascending slope, and because the array ends in -inf the slope MUST eventually come down,
so a peak exists in (mid, hi]; otherwise nums[mid] > nums[mid+1] and a peak exists in [lo, mid]
(walk left from mid: either we keep ascending to index lo whose left is -inf, or we hit a peak).
The predicate "nums[i] > nums[i+1]" is therefore safe to binary search even though it is not
globally monotone — the invariant "a peak exists in [lo, hi]" is maintained.

Intuition
---------
You do not need the global maximum, just any local one. Whichever direction is uphill from mid,
a peak is guaranteed in that direction because the array is fenced by -inf on both ends. So move
toward the higher neighbour and halve the range.

Geometric view
--------------
Picture a mountain range with cliffs dropping to -inf at both ends. Stand at mid and look at the
next point to the right. If it is higher, the ground must eventually fall before the right cliff,
so a summit lies to the right; shrink lo. If it is lower, you are on a downhill or at a summit;
shrink hi to mid. The window always contains a summit.

Steps
-----
1. lo = 0, hi = n - 1.
2. While lo < hi: mid = (lo+hi)//2.
3. If nums[mid] < nums[mid+1]: lo = mid + 1 (uphill to the right).
4. Else hi = mid (mid could itself be the peak).
5. Return lo.

Complexity: O(log n) time, O(1) space — standard halving.
Pitfalls: accessing nums[mid+1] when mid == n-1 (avoided by `lo < hi` so mid < hi); using
`hi = mid - 1` which can skip the peak; thinking you need the maximum element.
"""
from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:                       # mid < hi, so nums[mid + 1] is always valid
            mid = (lo + hi) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1                 # uphill to the right: a peak lies there
            else:
                hi = mid                     # downhill (or peak) at mid: keep it
        return lo


def brute_force(nums: List[int]) -> int:
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            return i
    return len(nums) - 1


def is_peak(nums: List[int], i: int) -> bool:
    left = nums[i - 1] if i > 0 else float("-inf")
    right = nums[i + 1] if i + 1 < len(nums) else float("-inf")
    return left < nums[i] > right


if __name__ == "__main__":
    s = Solution()
    cases = [[1, 2, 3, 1], [1, 2, 1, 3, 5, 6, 4], [1], [2, 1], [1, 2], [3, 2, 1]]
    for nums in cases:
        assert is_peak(nums, s.findPeakElement(nums))
        assert is_peak(nums, brute_force(nums))
    assert s.findPeakElement([1, 2, 3, 1]) == 2 == brute_force([1, 2, 3, 1])
    print("ok")
