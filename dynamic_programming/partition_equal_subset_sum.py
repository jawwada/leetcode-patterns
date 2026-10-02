"""
Partition Equal Subset Sum (LeetCode 416)  — Medium
Pattern: 0/1 knapsack reachability (bitset)

Problem
-------
Given an array of positive integers, decide whether it can be split into two subsets
with equal sums. Example: [1,5,11,5] -> True ([1,5,5] and [11]).  [1,2,3,5] -> False
(total 11 is odd).

Brute force
-----------
The total must be even; then ask whether some subset sums to target = total / 2.
Recursion can(i, t): either take nums[i] (t - nums[i]) or skip it. That explores all 2^n
subsets: O(2^n) time, O(n) stack. The waste: many different take/skip histories arrive
at the same (i, remaining t) pair and each re-explores the identical suffix.

From brute force to optimal
---------------------------
Overlapping subproblems: the answer to can(i, t) depends only on i and t, and there are
just n * (target + 1) such pairs (the user's original memo table had exactly that shape).
State: reach_i = set of sums achievable using the first i numbers.
Recurrence: reach_{i+1} = reach_i  U  {s + nums[i] : s in reach_i}, reach_0 = {0}.
Order: process numbers one by one; each row depends only on the previous row, so one
1-D boolean row suffices (iterate t downward so each number is used once). Space/time
trick: store the row as the bits of one Python int: reach |= reach << x does the whole
row update in one word-parallel shift. Answer: bit `target` is set. O(n * target / w)
time, O(target) bits.

Intuition
---------
You don't care WHICH subset makes a sum, only WHETHER that sum is possible. Track the set
of possible sums; adding a number x shifts every possible sum up by x and unions the
result in. If target ever becomes possible, the rest of the array forms the other half.

Geometric view
--------------
Picture a strip of light bulbs numbered 0..total, only bulb 0 lit. Each number x copies
the current lit pattern, slides the copy x places to the right, and overlays it. After
all numbers, check whether the bulb at total / 2 is lit.

Steps
-----
1. total = sum(nums); if odd return False; target = total // 2.
2. reach = 1 (only sum 0 is reachable).
3. For x in nums: reach |= reach << x.
4. Return (reach >> target) & 1 == 1.

Complexity: O(n * total / 64) time, O(total) bits space — one big-int shift-or per number.
Pitfalls: forgetting the odd-total early exit; in the boolean-array version, iterating t
upward reuses a number twice; the 2-D memo version needs the remaining-target < 0 guard.
"""
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        reach = 1  # bit s set <=> some subset sums to s
        for x in nums:
            reach |= reach << x
        return (reach >> (total // 2)) & 1 == 1


def brute_force(nums: List[int]) -> bool:
    # Take-or-skip every element looking for a subset summing to half: O(2^n).
    total = sum(nums)
    if total % 2:
        return False

    def can(i: int, t: int) -> bool:
        if t == 0:
            return True
        if i == len(nums) or t < 0:
            return False
        return can(i + 1, t - nums[i]) or can(i + 1, t)

    return can(0, total // 2)


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [([1, 5, 11, 5], True), ([1, 2, 3, 5], False), ([2, 2], True),
             ([1], False), ([3, 3, 3, 4, 5], True), ([100, 1, 1, 2], False)]
    for nums, want in cases:
        assert s.canPartition(nums) == want
        assert brute_force(nums) == want
    rng = random.Random(7)
    for _ in range(200):
        nums = [rng.randint(1, 12) for _ in range(rng.randint(1, 12))]
        assert s.canPartition(nums) == brute_force(nums), nums
    print("ok")
