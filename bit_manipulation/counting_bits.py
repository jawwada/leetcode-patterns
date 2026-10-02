"""
Counting Bits (LeetCode 338)  — Easy
Pattern: Reuse the count of i >> 1

Problem
-------
Given n, return an array ans of length n + 1 where ans[i] is the number of 1-bits in the
binary representation of i. Example: n = 5 -> [0,1,1,2,1,2]
(0, 1, 10, 11, 100, 101).

Brute force
-----------
Popcount each i independently by testing all 32 bit positions (the user's original
solution). O(32 * n) = O(n log U) time, O(1) extra space. The waste: the bits of i above
position 0 are exactly the bits of i >> 1, whose count we computed a moment ago and are
now recounting from scratch.

From brute force to optimal
---------------------------
The redundancy is recounting the high bits of i. Observation: i >> 1 drops only the
lowest bit, so popcount(i) = popcount(i >> 1) + (i & 1). Because i >> 1 < i, that value
is already in the output array when we reach i, so a single left-to-right pass fills the
array with one shift, one AND and one add per entry. O(n) time, O(1) extra space beyond
the output.

Intuition
---------
Every number is its half with one bit appended on the right. The count for i is the
count for its half, plus one if the appended bit is 1.

Geometric view
--------------
Lay the numbers out as the nodes of an implicit binary tree: i's parent is i >> 1, and
going to the left/right child appends a 0/1. Each node's count is its parent's count plus
the label on the edge, filled in level by level.

Steps
-----
1. bits = [0] * (n + 1).
2. For i in 1..n: bits[i] = bits[i >> 1] + (i & 1).
3. Return bits.

Complexity: O(n) time, O(1) extra space — constant work per entry.
Pitfalls: using bits[i - 1] (wrong relation); bin(i).count('1') is fine but still
O(log i) per number; off-by-one on the length (n + 1 entries).
"""
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        bits = [0] * (n + 1)
        for i in range(1, n + 1):
            bits[i] = bits[i >> 1] + (i & 1)  # half's count + lowest bit
        return bits


def brute_force(n: int) -> List[int]:
    # Test all 32 bit positions of every number: O(32 * n).
    result = []
    for num in range(n + 1):
        result.append(sum(1 for b in range(32) if num & (1 << b)))
    return result


if __name__ == "__main__":
    s = Solution()
    assert s.countBits(2) == [0, 1, 1]
    assert s.countBits(5) == [0, 1, 1, 2, 1, 2]
    assert s.countBits(0) == [0]
    for n in (0, 1, 7, 64, 1000):
        assert s.countBits(n) == brute_force(n)
    print("ok")
