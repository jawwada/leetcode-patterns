"""
Binary Search (LeetCode 704)  — Easy
Pattern: Binary search on a sorted array

Problem
-------
Given a sorted (ascending) array of distinct integers `nums` and a `target`, return the index of
`target` if present, otherwise -1. Must run in O(log n).
Example: nums = [-1,0,3,5,9,12], target = 9 -> 4 (nums[4] == 9).

Brute force
-----------
Scan left to right and return the first index whose value equals target. O(n) time, O(1) space.
The wasted work: every comparison that says "too small" or "too big" only eliminates ONE element,
even though sortedness tells us it eliminates an entire side of the array.

From brute force to optimal
---------------------------
The redundancy is throwing away one element per comparison. Observation: if nums[mid] < target,
every index <= mid is also < target (sorted), so the whole left half is dead; symmetrically for
">" . So one comparison can halve the live range instead of shrinking it by one. The data
structure is just two indices `lo`, `hi` with the invariant "if target is in nums, it lies in
[lo, hi]". Each step halves the range, giving log2(n) comparisons.

Intuition
---------
Keep a closed interval [lo, hi] that is guaranteed to contain the target if it exists. Probe the
middle; based on the comparison, discard the half that cannot contain the target. When the
interval becomes empty (lo > hi), the target is absent.

Geometric view
--------------
Picture the array as a number line. Two brackets `[lo ... hi]` enclose the candidates. Each probe
at the midpoint snaps one bracket to just past the midpoint, so the enclosed length halves every
step: n, n/2, n/4, ... 1, 0.

Steps
-----
1. lo = 0, hi = len(nums) - 1.
2. While lo <= hi: mid = (lo + hi) // 2.
3. If nums[mid] == target return mid.
4. If nums[mid] < target: lo = mid + 1 (target is strictly right of mid).
5. Else hi = mid - 1.
6. Loop exits -> return -1.

Complexity: O(log n) time, O(1) space — the candidate range halves each iteration.
Pitfalls: using `lo < hi` with a closed interval skips the last element; forgetting the `+1/-1`
causes an infinite loop when lo == hi; in C-like languages `(lo+hi)` can overflow (use lo+(hi-lo)//2).
"""
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:                      # closed interval [lo, hi]
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1                 # target strictly right of mid
            else:
                hi = mid - 1                 # target strictly left of mid
        return -1


def brute_force(nums: List[int], target: int) -> int:
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([-1, 0, 3, 5, 9, 12], 9, 4),
        ([-1, 0, 3, 5, 9, 12], 2, -1),
        ([5], 5, 0),
        ([5], -5, -1),
        ([], 1, -1),
    ]
    for nums, t, want in cases:
        assert s.search(nums, t) == want
        assert brute_force(nums, t) == want
    print("ok")
