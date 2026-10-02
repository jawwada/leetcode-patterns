"""
Search in Rotated Sorted Array (LeetCode 33)  — Medium
Pattern: Binary search on a rotated sorted array

Problem
-------
A sorted array of distinct integers was rotated at an unknown pivot. Return the index of `target`
or -1, in O(log n).
Example: nums = [4,5,6,7,0,1,2], target = 0 -> 4.

Brute force
-----------
Linear scan for target. O(n) time, O(1) space. The wasted work: at every probe we know which of
the two sorted runs we are standing in and could discard the entire other side, but a scan only
discards one element.

From brute force to optimal
---------------------------
The redundancy is not exploiting that every half [lo, mid] or [mid, hi] has at least one side
that is properly sorted. Observation: if nums[lo] <= nums[mid], the left half is sorted; if
target lies in [nums[lo], nums[mid]) go left, otherwise go right. Symmetrically when the right
half is sorted. Deciding "is target inside the sorted half?" takes O(1) because a sorted half is
described by its two endpoints. So each probe still halves the range, and we never need to find
the pivot first.

Intuition
---------
At any mid, one of the two halves is a plain sorted array. Check whether the target fits inside
that sorted half's value range; if yes, recurse there, if no, the target must be in the other
(messy) half. Always test the sorted half because only there can membership be decided from the
endpoints alone.

Geometric view
--------------
Two rising segments; the cliff falls in exactly one of the halves [lo..mid] or [mid..hi]. The
half without the cliff is a clean ramp whose min and max are its endpoints. Ask "does target's
height fall on this ramp?" and move lo or hi accordingly.

Steps
-----
1. lo = 0, hi = n - 1. While lo <= hi: mid = (lo+hi)//2; if nums[mid] == target return mid.
2. If nums[lo] <= nums[mid] (left half sorted):
   - if nums[lo] <= target < nums[mid]: hi = mid - 1 else lo = mid + 1.
3. Else (right half sorted):
   - if nums[mid] < target <= nums[hi]: lo = mid + 1 else hi = mid - 1.
4. Return -1.

Complexity: O(log n) time, O(1) space — one standard binary search with an O(1) side test.
Pitfalls: using `<` instead of `<=` in `nums[lo] <= nums[mid]` breaks the two-element case;
mixing strict/non-strict in the range tests so target == endpoint goes the wrong way.
"""
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:                    # left half [lo, mid] is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                                        # right half [mid, hi] is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1


def brute_force(nums: List[int], target: int) -> int:
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1], 0, -1),
        ([3, 1], 1, 1),
        ([5, 1, 3], 5, 0),
    ]
    for nums, t, want in cases:
        assert s.search(nums, t) == want
        assert brute_force(nums, t) == want
    print("ok")
