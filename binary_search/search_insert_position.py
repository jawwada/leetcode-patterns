"""
Search Insert Position (LeetCode 35)  — Easy
Pattern: Binary search for a boundary (lower / upper bound)

Problem
-------
Given a sorted array of distinct integers and a target, return the index of target if
present, otherwise the index where it would be inserted to keep the array sorted.
Must run in O(log n). Example: nums = [1,3,5,6], target = 5 -> 2; target = 2 -> 1;
target = 7 -> 4.

Brute force
-----------
Scan left to right and return the first index i with nums[i] >= target, or n if none.
O(n) time, O(1) space. The waste: sortedness is ignored — after seeing nums[i] < target
we already know every index before i is also too small, yet we keep checking one by one.

From brute force to optimal
---------------------------
Both "found" and "insert here" are the same question: the first index whose value is
>= target (the lower bound). Observation: the predicate nums[i] >= target is False...False
then True...True across a sorted array, so a single comparison at mid discards half the
candidates. Keep ans = n (insert at the end if nothing qualifies); when nums[mid] >= target,
record mid and search left for an earlier qualifier; otherwise search right. This is the
original solution's structure, unchanged.

Intuition
---------
We are hunting the boundary between "too small" and "big enough". Every probe tells us on
which side of the boundary mid lies, so the boundary's possible range halves each step.

Geometric view
--------------
Picture the array as F F F T T T under the predicate "value >= target". [lo, hi] is a
shrinking bracket around the first T; each probe chops off the half that cannot contain it
and the bracket collapses onto the boundary in log n steps.

Steps
-----
1. lo, hi = 0, n - 1; ans = n.
2. While lo <= hi: mid = (lo + hi) // 2.
3. If nums[mid] >= target: ans = mid, hi = mid - 1 (look for an earlier T).
4. Else lo = mid + 1. Return ans.

Complexity: O(log n) time, O(1) space — the bracket halves every iteration.
Pitfalls: Returning -1 when target is missing; forgetting the insert-at-end case (ans = n);
off-by-one when mixing hi = mid with while lo <= hi (infinite loop).
"""
from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        ans = len(nums)                  # if nothing is >= target, insert at the end
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] >= target:      # mid is a candidate; look for an earlier one
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans


def brute_force(nums: List[int], target: int) -> int:
    for i, x in enumerate(nums):         # ignores sortedness: checks every index
        if x >= target:
            return i
    return len(nums)


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 3, 5, 6], 5, 2), ([1, 3, 5, 6], 2, 1), ([1, 3, 5, 6], 7, 4),
             ([1, 3, 5, 6], 0, 0), ([1], 1, 0), ([], 3, 0)]
    for nums, t, want in cases:
        assert s.searchInsert(nums, t) == want
        assert brute_force(nums, t) == want
    print("ok")
