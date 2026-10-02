"""
Maximum Product Subarray (LeetCode 152)  — Medium
Pattern: Running max & min carry (Kadane variant)

Problem
-------
Given an integer array nums, return the largest product of any non-empty contiguous
subarray. Values may be negative or zero.
Example: nums = [2,3,-2,4] -> 6 (subarray [2,3]); nums = [-2,0,-1] -> 0.

Brute force
-----------
Fix every start i, extend the end j to the right while multiplying a running product, and
keep the best. O(n^2) time, O(1) space. The wasted work: for each new end j we redo the
products of all starts i <= j, although the best product ending at j only depends on the
products ending at j-1.

From brute force to optimal
---------------------------
The redundancy is recomputing every product that ends at j. Plain Kadane ("keep the best
product ending here") fails because a negative number flips order: the most negative
product so far becomes the largest one after multiplying by a negative. Observation: the
extreme products ending at j can only come from x itself, x * (max ending at j-1) or
x * (min ending at j-1). So carry two numbers — hi and lo — instead of all n products, and
update both from the previous pair in O(1). A 0 collapses both to 0, restarting the run.
(The original solution scanned prefix products left-to-right and right-to-left, resetting
at zeros; that is also O(n) / O(1) and works because the best product inside a zero-free
block is always a prefix or a suffix of that block.)

Intuition
---------
Sign is the whole difficulty. Keeping the largest AND the smallest product ending at the
current index means that whichever one a negative number flips into the lead is already in
hand. The global answer is the best hi seen at any index.

Geometric view
--------------
Picture two lines riding over the array: hi on top, lo on the bottom. A positive x stretches
both away from zero; a negative x swaps them (mirror across zero) before stretching; a zero
collapses both onto 0. The answer is the highest point the top line ever reaches.

Steps
-----
1. hi = lo = best = nums[0].
2. For each x after the first: candidates = (x, hi*x, lo*x).
3. hi = max(candidates), lo = min(candidates) — computed from the OLD hi/lo.
4. best = max(best, hi). Return best.

Complexity: O(n) time, O(1) space — one pass carrying two products.
Pitfalls: Updating hi before using it to compute lo; initialising best to 0 (wrong for
[-3]); forgetting that x alone may beat extending (restart after a zero).
"""
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        hi = lo = best = nums[0]
        for x in nums[1:]:
            # a negative x turns the smallest product into the largest, so carry both
            cands = (x, hi * x, lo * x)
            hi, lo = max(cands), min(cands)
            best = max(best, hi)
        return best


def brute_force(nums: List[int]) -> int:
    best = nums[0]
    for i in range(len(nums)):
        prod = 1
        for j in range(i, len(nums)):   # every end re-extends from every start
            prod *= nums[j]
            best = max(best, prod)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [([2, 3, -2, 4], 6), ([-2, 0, -1], 0), ([-3], -3), ([-2, 3, -4], 24),
             ([0, 2], 2), ([-1, -1], 1), ([2, -5, -2, -4, 3], 24)]
    for nums, want in cases:
        assert s.maxProduct(nums) == want, nums
        assert brute_force(nums) == want, nums
    print("ok")
