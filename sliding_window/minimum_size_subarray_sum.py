"""
Minimum Size Subarray Sum (LeetCode 209)  — Medium
Pattern: Variable-size sliding window

Problem
-------
Given an array of positive integers nums and a target, return the minimal length of a
contiguous subarray whose sum is >= target, or 0 if none exists.
Example: target = 7, nums = [2,3,1,2,4,3] -> 2 ([4,3]).

Brute force
-----------
For every start i, add elements to the right until the running sum reaches target, record
the length. O(n^2) time, O(1) space. The wasted work: start i+1 re-adds elements whose sum
we just computed; the new sum is simply the old sum minus nums[i].

From brute force to optimal
---------------------------
The redundancy is re-summing an overlapping range. Observation: because all numbers are
positive, the window sum is strictly monotone in both edges -- adding on the right increases
it, removing on the left decreases it. So once [left, right] reaches target we shrink left
while the sum stays >= target, recording each valid length; when it drops below target no
window ending at right can help, so we resume growing right. Each edge only moves
rightwards, giving a linear two-pointer sweep with a running sum (no prefix array).

Intuition
---------
Grow the window on the right until it is "heavy enough"; then trim from the left while it
remains heavy enough, recording lengths. Positivity guarantees trimming can only lighten it
and growing can only make it heavier, so no configuration is missed.

Geometric view
--------------
A caterpillar crawls along the array: its head R stretches forward until the body weighs
>= target, then its tail L catches up until the weight drops below target. The shortest
body length observed while heavy is the answer.

Steps
-----
1. left = 0, total = 0, best = inf.
2. For each right: total += nums[right].
3. While total >= target: best = min(best, right - left + 1); total -= nums[left]; left += 1.
4. Return 0 if best is inf else best.

Complexity: O(n) time, O(1) space — each index is added once and removed once.
Pitfalls: Using `if` instead of `while` when shrinking; applying this to arrays with
negatives or zeros (monotonicity breaks; needs prefix sums + binary search / deque);
returning inf instead of 0 when no window qualifies.
"""
from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = total = 0
        best = float("inf")
        for right, x in enumerate(nums):
            total += x
            while total >= target:                   # valid: record, then try shorter
                best = min(best, right - left + 1)
                total -= nums[left]
                left += 1
        return 0 if best == float("inf") else best


def brute_force(target: int, nums: List[int]) -> int:
    best = 0
    for i in range(len(nums)):
        total = 0                                    # re-summed for every start
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                if best == 0 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [(7, [2, 3, 1, 2, 4, 3]), (4, [1, 4, 4]), (11, [1, 1, 1, 1, 1, 1, 1, 1]), (15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8]), (3, [3])]
    assert s.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2
    assert s.minSubArrayLen(4, [1, 4, 4]) == 1
    assert s.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    assert s.minSubArrayLen(15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8]) == 2
    for c in cases:
        assert s.minSubArrayLen(*c) == brute_force(*c)
    print("ok")
