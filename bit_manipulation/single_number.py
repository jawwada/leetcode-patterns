"""
Single Number (LeetCode 136)  — Easy
Pattern: XOR cancellation

Problem
-------
Every element of a non-empty array appears exactly twice except one, which appears once. Find
that element in linear time using constant extra space.
Example: [4,1,2,1,2] -> 4.  [2,2,1] -> 1.  [1] -> 1.

Brute force
-----------
For each element, scan the whole array and count its occurrences; return the one with count 1.
O(n^2) time, O(1) space. (A hash map of counts is O(n) time but O(n) space, which the problem
forbids.) The waste: every element is compared against every other element, re-discovering the
same pairs over and over; the pairing information is computed n times and never stored.

From brute force to optimal
---------------------------
The redundancy is re-scanning to find each element's partner. Observation: we never need to
know WHICH element pairs with which, only that pairs cancel. XOR has exactly that algebra:
a ^ a = 0, a ^ 0 = a, and it is commutative and associative, so the order of the elements does
not matter. XOR-ing the entire array therefore cancels every pair regardless of position and
leaves the single number. One pass, one integer of state, and the "pair bookkeeping" happens
implicitly inside the bit columns.

Intuition
---------
Look at any single bit position across all numbers: a value that appears twice contributes an
even number of 1s there, so the parity of that column is determined by the lone value alone.
XOR computes exactly that parity for all 32 columns at once.

Geometric view
--------------
Write the numbers in binary as rows, one column per bit. Pairs of equal rows cancel column by
column (two 1s in a column flip the running parity twice, back to 0). After all rows are
folded in, the parity row that remains IS the unpaired number.

Steps
-----
1. acc = 0.
2. For each x in nums: acc ^= x.
3. Return acc.

Complexity: O(n) time, O(1) space — one pass, one accumulator.
Pitfalls: Reaching for a hash set or sorting (violates the O(1) space spirit); assuming XOR
works when the duplicates appear three times (it does not; that variant needs bit counting mod 3).
"""
from functools import reduce
from operator import xor
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums, 0)     # pairs cancel (a ^ a = 0); the loner survives


def brute_force(nums: List[int]) -> int:
    for x in nums:
        if sum(1 for y in nums if y == x) == 1:   # rescans the array for every element
            return x
    return -1


if __name__ == "__main__":
    s = Solution()
    assert s.singleNumber([2, 2, 1]) == 1
    assert s.singleNumber([4, 1, 2, 1, 2]) == 4
    assert s.singleNumber([1]) == 1                       # single element
    assert s.singleNumber([-3, 7, -3]) == 7               # negatives
    for nums in ([2, 2, 1], [4, 1, 2, 1, 2], [1], [-3, 7, -3], [0, 0, 5]):
        assert s.singleNumber(nums) == brute_force(nums), nums
    print("ok")
