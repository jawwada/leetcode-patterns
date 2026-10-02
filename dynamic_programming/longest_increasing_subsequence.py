"""
Longest Increasing Subsequence (LeetCode 300)  — Medium
Pattern: Patience sorting (tails array + binary search)

Problem
-------
Given an integer array nums, return the length of the longest strictly increasing
subsequence (elements in order, not necessarily contiguous).
Example: [10,9,2,5,3,7,101,18] -> 4 (e.g. 2,3,7,101).  [7,7,7] -> 1.

Brute force
-----------
Recursion over (i, prev): at index i either skip nums[i] or, if nums[i] > nums[prev],
take it. That enumerates all 2^n subsequences: O(2^n) time, O(n) stack. The waste: the
best continuation from index i after last-taken value v is recomputed for every path that
arrives at (i, v).

From brute force to optimal
---------------------------
Step 1 (O(2^n) -> O(n^2), the user's original DP). Overlapping subproblems: the longest
increasing subsequence ENDING at index i is the same no matter how we reached it.
State: dp[i] = length of the LIS that ends exactly at nums[i].
Recurrence: dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i]), default 1.
Order: i left to right; answer max(dp). This is O(n^2) because each i rescans all j < i.
Step 2 (O(n^2) -> O(n log n)). The redundancy is the linear scan for "best dp[j] with a
smaller value". Observation: for each length L we only need the SMALLEST possible tail of
an increasing subsequence of length L; a smaller tail is never worse. Those tails form a
strictly increasing array, so for each x we binary-search the first tail >= x and
overwrite it (or append, extending the longest length by one). len(tails) is the answer.

Intuition
---------
tails[L-1] is the lowest value any increasing subsequence of length L can end on so far.
A new x either extends the longest one (x beats every tail) or improves some tail by
lowering it, which makes future extensions easier. tails itself is not an LIS, only its
length is meaningful.

Geometric view
--------------
Patience solitaire: deal cards left to right; put each card on the leftmost pile whose
top is >= the card, or start a new pile on the right. Pile tops increase left to right,
so placement is a binary search. The number of piles equals the LIS length.

Steps
-----
1. tails = [].
2. For x in nums: i = bisect_left(tails, x).
3.   If i == len(tails): append x; else tails[i] = x.
4. Return len(tails).

Complexity: O(n log n) time, O(n) space — one binary search per element.
Pitfalls: bisect_right would allow equal values (non-strict LIS); treating tails as the
actual subsequence; the O(n^2) DP must take max over all j, not just j = i - 1.
"""
from bisect import bisect_left
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []  # tails[L-1] = smallest tail of an increasing run of length L
        for x in nums:
            i = bisect_left(tails, x)  # first tail >= x (strictly increasing)
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x
        return len(tails)


def brute_force(nums: List[int]) -> int:
    # Take-or-skip recursion over every subsequence: O(2^n).
    def best(i: int, prev: int) -> int:
        if i == len(nums):
            return 0
        skip = best(i + 1, prev)
        if prev == -1 or nums[i] > nums[prev]:
            return max(skip, 1 + best(i + 1, i))
        return skip

    return best(0, -1)


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [([10, 9, 2, 5, 3, 7, 101, 18], 4), ([0, 1, 0, 3, 2, 3], 4),
             ([7, 7, 7, 7, 7, 7, 7], 1), ([5], 1), ([4, 10, 4, 3, 8, 9], 3)]
    for nums, want in cases:
        assert s.lengthOfLIS(nums) == want
        assert brute_force(nums) == want
    rng = random.Random(1)
    for _ in range(200):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(1, 10))]
        assert s.lengthOfLIS(nums) == brute_force(nums), nums
    print("ok")
