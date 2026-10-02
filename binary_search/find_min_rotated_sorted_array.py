"""
Find Minimum in Rotated Sorted Array (LeetCode 153)  — Medium
Pattern: Binary search on a rotated sorted array

Problem
-------
A sorted array of distinct integers was rotated between 1 and n times (e.g. [0,1,2,4,5,6,7]
became [4,5,6,7,0,1,2]). Return the minimum element in O(log n).
Example: nums = [3,4,5,1,2] -> 1.

Brute force
-----------
Scan the array and keep the smallest value seen. O(n) time, O(1) space. The wasted work: the
array is two sorted runs glued together, and the minimum is exactly the seam; comparing every
element ignores that any single comparison against the right end tells you which run you are in.

From brute force to optimal
---------------------------
The redundancy is testing every element when one comparison can discard half. Observation: for
any index mid, if nums[mid] > nums[hi] then mid sits in the left (larger) run and the seam — the
minimum — is strictly to the right of mid; otherwise mid is in the right run (or the array is
unrotated) and the minimum is at mid or to its left. That rule is a monotone predicate, so binary
search with `lo < hi`, shrinking to `lo = mid+1` or `hi = mid`, converges on the seam.

Intuition
---------
Compare the middle with the RIGHT end, never the left. The right end is always in the right
(smaller) run, so "mid > right" means we are still on the high plateau and must jump over the
cliff; "mid <= right" means we are already past the cliff and the minimum is at or before mid.

Geometric view
--------------
Plot values vs index: a rising line, a vertical drop (the cliff), then another rising line that
stays below the first. The minimum is the point right after the drop. Each probe asks "am I above
or below the level of the last element?" and moves lo/hi to pinch the cliff.

Steps
-----
1. lo = 0, hi = n - 1.
2. While lo < hi: mid = (lo+hi)//2.
3. If nums[mid] > nums[hi]: lo = mid + 1 (minimum is right of mid).
4. Else hi = mid (minimum is at mid or left of it).
5. Return nums[lo].

Complexity: O(log n) time, O(1) space — half the range is discarded each probe.
Pitfalls: comparing against nums[lo] (ambiguous when the half is unrotated); using `hi = mid - 1`
which can skip the minimum; `lo <= hi` with this update rule loops forever.
"""
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1                 # mid is on the high run; cliff is to the right
            else:
                hi = mid                     # mid is on the low run; min is at mid or left
        return nums[lo]


def brute_force(nums: List[int]) -> int:
    best = nums[0]
    for x in nums:
        if x < best:
            best = x
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([3, 4, 5, 1, 2], 1),
        ([4, 5, 6, 7, 0, 1, 2], 0),
        ([11, 13, 15, 17], 11),
        ([2, 1], 1),
        ([1], 1),
    ]
    for nums, want in cases:
        assert s.findMin(nums) == want
        assert brute_force(nums) == want
    print("ok")
