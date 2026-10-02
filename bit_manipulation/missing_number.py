"""
Missing Number (LeetCode 268)  — Easy
Pattern: XOR cancellation

Problem
-------
Given an array of n distinct numbers taken from the range [0, n], exactly one number of the range
is missing. Return it, in O(n) time and O(1) extra space.
Example: [3,0,1] -> 2.  [0,1] -> 2.  [9,6,4,2,3,5,7,0,1] -> 8.

Brute force
-----------
For each candidate value v in 0..n, scan the array to see whether v is present; the first absent
one is the answer. O(n^2) time, O(1) space. (Sorting first gives O(n log n); a hash set gives
O(n) time but O(n) space.) The waste: each of the n+1 membership tests re-reads the whole array;
nothing learned from testing v=0 helps when testing v=1.

From brute force to optimal
---------------------------
The redundancy is n+1 independent linear scans. Observation: the multiset {0..n} together with
the array contains every value twice except the missing one, which appears once. That is
precisely the Single Number setup, so XOR-ing all indices 0..n together with all array values
cancels every pair and leaves the missing number. Equivalent arithmetic view: the expected sum
n(n+1)/2 minus the actual sum; XOR is preferred because it can never overflow in fixed-width
languages.

Intuition
---------
Pair each index with each value. Every value that is present appears once as an array element and
once as an index (or as n), so they cancel under XOR; the missing value appears only as an index.

Geometric view
--------------
Two rows of binary columns: the indices 0..n and the array values. Fold both rows into one
parity row with XOR; every value that appears in both rows flips each of its bit columns twice
(no net change), and the row left standing is the number that appeared in the index row alone.

Steps
-----
1. acc = n (the one index that has no array slot).
2. For i, v in enumerate(nums): acc ^= i ^ v.
3. Return acc.

Complexity: O(n) time, O(1) space — one pass, one accumulator.
Pitfalls: Forgetting to include n itself in the XOR (indices only go to n-1); off-by-one in the
sum formula; using `in` on the list inside a loop (quadratic).
"""
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        acc = len(nums)                 # index n has no array slot: seed with it
        for i, v in enumerate(nums):
            acc ^= i ^ v                # present values appear as both index and value: cancel
        return acc


def brute_force(nums: List[int]) -> int:
    for v in range(len(nums) + 1):
        if v not in nums:               # linear membership scan per candidate: O(n^2)
            return v
    return -1


if __name__ == "__main__":
    s = Solution()
    assert s.missingNumber([3, 0, 1]) == 2
    assert s.missingNumber([0, 1]) == 2
    assert s.missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    assert s.missingNumber([0]) == 1                       # missing n
    assert s.missingNumber([1]) == 0                       # missing 0
    for nums in ([3, 0, 1], [0, 1], [9, 6, 4, 2, 3, 5, 7, 0, 1], [0], [1]):
        assert s.missingNumber(nums) == brute_force(nums), nums
    print("ok")
