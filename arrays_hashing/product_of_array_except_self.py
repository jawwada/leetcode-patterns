"""
Product of Array Except Self (LeetCode 238)  — Medium
Pattern: Prefix and suffix accumulation

Problem
-------
Given an integer array nums, return an array answer where answer[i] is the product
of all elements except nums[i]. You must not use division and must run in O(n).
Example: nums = [1, 2, 3, 4] -> [24, 12, 8, 6].

Brute force
-----------
For each index i, multiply every other element in a nested loop. O(n^2) time, O(1)
extra space. The wasted work is obvious once you compare two neighbouring answers:
answer[i] and answer[i+1] share n - 2 of the same factors, yet the brute force
recomputes that shared product from scratch each time.

From brute force to optimal
---------------------------
The product of "everything except i" is the product of "everything to the left of i"
times "everything to the right of i". Both of those are running products that can be
built incrementally: prefix[i] = prefix[i-1] * nums[i-1] in a left-to-right pass,
suffix likewise right-to-left. Two passes instead of n^2 multiplications. To hit O(1)
extra space, write the prefix products straight into the output array, then sweep
right-to-left carrying the suffix product in a single variable and multiply it in.

Intuition
---------
Splitting "all but one" into a left part and a right part turns an exclusion problem
into two inclusion problems, and inclusion problems are prefix sums (here prefix
products). Division is unnecessary because you never "remove" nums[i] — you simply
never multiply it in.

Geometric view
--------------
Picture two arrows sweeping toward each other over the array. The left arrow drags a
growing product of everything behind it and stamps it into each cell. The right
arrow then drags its own product leftward and multiplies it into the stamped value.
Every cell ends up holding (product of its left) * (product of its right).

Steps
-----
1. Initialise answer = [1] * n.
2. Left pass: carry prefix = 1; for i in 0..n-1 set answer[i] = prefix, then prefix *= nums[i].
3. Right pass: carry suffix = 1; for i in n-1..0 set answer[i] *= suffix, then suffix *= nums[i].
4. Return answer.

Complexity: O(n) time, O(1) extra space — two linear passes; the output array does
not count toward extra space.
Pitfalls: multiplying nums[i] into the carry BEFORE stamping (includes self);
reaching for division, which breaks on zeros and violates the constraint; mishandling
arrays with two or more zeros (the two-pass method handles them automatically).
"""
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [1] * n
        prefix = 1
        for i in range(n):
            answer[i] = prefix          # product of everything left of i
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix         # times product of everything right of i
            suffix *= nums[i]
        return answer


def brute_force(nums: List[int]) -> List[int]:
    n = len(nums)
    answer = []
    for i in range(n):
        prod = 1
        for j in range(n):
            if j != i:
                prod *= nums[j]
        answer.append(prod)
    return answer


if __name__ == "__main__":
    s = Solution()
    assert s.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert s.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert s.productExceptSelf([0, 0, 2]) == [0, 0, 0]
    assert s.productExceptSelf([5, 2]) == [2, 5]
    for case in ([1, 2, 3, 4], [-1, 1, 0, -3, 3], [0, 0, 2], [5, 2]):
        assert s.productExceptSelf(case) == brute_force(case)
    print("ok")
