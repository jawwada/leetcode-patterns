"""
Patching Array (LeetCode 330)  — Hard
Pattern: Greedy reach (furthest reachable index)

Problem
-------
Given a sorted array nums and an integer n, add (patch) the minimum number of integers so that
every value in [1, n] is the sum of some subset of the array. Return that minimum count.
Example: nums = [1,3], n = 6 -> 1 (patch 2: sums 1..6 are all reachable).
nums = [1,5,10], n = 20 -> 2 (patch 2 and 4).

Brute force
-----------
Compute the set of all subset sums of the current array (2^k subsets), find the smallest value
m <= n that is missing, patch m, and repeat until nothing is missing. Each round is exponential
in the array length, so the whole thing is exponential; space is the subset-sum set, up to O(n).
The wasted work: materialising every subset sum when the only fact we ever use is "which prefix
[1, reach] is fully covered" — a single integer.

From brute force to optimal
---------------------------
The redundancy is the full subset-sum set. Observation: process nums in sorted order and keep
`reach` = largest value such that every sum in [1, reach] is buildable. If the next number x is
<= reach + 1, adding it extends coverage to [1, reach + x] contiguously (every old sum s gives a
new sum s + x, and the new sums start at x <= reach + 1 so no hole opens). If x > reach + 1, the
value reach + 1 is unreachable no matter what later (larger) numbers do, so we must patch, and the
best patch is reach + 1 itself: it doubles the coverage to [1, 2*reach + 1], which is the most any
single patch can add. The invariant "[1, reach] fully covered" replaces the exponential set, and
coverage at least doubles per patch, so there are O(log n) patches and O(len + log n) steps total.

Intuition
---------
Coverage is always a contiguous prefix [1, reach]. A number x <= reach + 1 glues onto that prefix
and lengthens it by x; a bigger x would leave reach + 1 as a hole. When a hole is forced, fill it
with the hole itself — that is the largest value you can insert without creating a new hole, and
it exactly doubles the prefix.

Geometric view
--------------
The covered prefix is a solid bar from 1 to reach. Each array element that starts at or before
the bar's right end plus one extends the bar by its own length. When the next element starts
beyond the bar's end, we lay down a bar of exactly the current length right after it (patch =
reach + 1) and the bar doubles.

Steps
-----
1. reach = 0, patches = 0, i = 0.
2. While reach < n:
3.   if i < len(nums) and nums[i] <= reach + 1: reach += nums[i]; i += 1
4.   else: reach += reach + 1 (patch value reach + 1); patches += 1.
5. Return patches.

Complexity: O(len(nums) + log n) time, O(1) space — each loop step either consumes an element
            or doubles reach.
Pitfalls: patching with a value smaller than reach + 1 (wastes a patch); comparing nums[i] <=
          reach instead of reach + 1 (misses that x = reach + 1 is fine); stopping at reach >= n
          before checking that remaining elements are irrelevant (they are, so this is fine, but
          continuing to add them does no harm either).
"""
from typing import List


class Solution:
    def minPatches(self, nums: List[int], n: int) -> int:
        reach = 0            # invariant: every sum in [1, reach] is buildable
        patches = i = 0
        while reach < n:
            if i < len(nums) and nums[i] <= reach + 1:
                reach += nums[i]           # no hole: [1, reach] + x covers [1, reach + x]
                i += 1
            else:
                reach += reach + 1         # patch with reach + 1: coverage doubles
                patches += 1
        return patches


def brute_force(nums: List[int], n: int) -> int:
    """Rebuild all subset sums (exponential) each round, patch the smallest missing value."""
    arr = list(nums)
    patches = 0
    while True:
        sums = {0}
        for x in arr:
            sums |= {s + x for s in sums if s + x <= n}
        missing = next((m for m in range(1, n + 1) if m not in sums), None)
        if missing is None:
            return patches
        arr.append(missing)
        patches += 1


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([1, 3], 6, 1),
        ([1, 5, 10], 20, 2),
        ([1, 2, 2], 5, 0),
        ([], 7, 3),               # edge: empty array -> patch 1, 2, 4
        ([1, 2, 31, 33], 2147483647, 28),
    ]
    for nums, n, want in cases:
        assert s.minPatches(nums, n) == want, (nums, n)
    for nums, n, want in cases[:4]:
        assert brute_force(nums, n) == want, (nums, n)

    random.seed(330)
    for _ in range(300):
        nums = sorted(random.randint(1, 12) for _ in range(random.randint(0, 6)))
        n = random.randint(1, 40)
        assert s.minPatches(nums, n) == brute_force(nums, n), (nums, n)
    print("ok")
