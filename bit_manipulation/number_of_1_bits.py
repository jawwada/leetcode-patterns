"""
Number of 1 Bits (LeetCode 191)  — Easy
Pattern: Clear lowest set bit (n & (n - 1))

Problem
-------
Given a 32-bit unsigned integer n, return the number of 1 bits in its binary representation
(the Hamming weight).
Example: 11 (0b1011) -> 3.  128 (0b10000000) -> 1.  2^32 - 1 -> 32.

Brute force
-----------
Loop over all 32 bit positions; for each, shift the number right by i and test the lowest bit.
O(32) time, O(1) space. The waste: every one of the 32 positions is inspected even when the
number has only one set bit; the loop count does not depend on the answer at all.

From brute force to optimal
---------------------------
The redundancy is visiting zero bits. Observation: n - 1 flips the lowest set bit of n to 0 and
every bit below it to 1, so n & (n - 1) clears EXACTLY the lowest set bit and leaves everything
else untouched. Each such operation removes one 1-bit, so repeating it until n is 0 takes
exactly k iterations where k is the answer. The loop now does work proportional to the number
of set bits, skipping all zero bits for free.

Intuition
---------
n & (n - 1) is "delete the rightmost 1". Count how many deletions it takes to reach zero.

Geometric view
--------------
Binary columns: 1011. Subtracting 1 borrows from the rightmost 1, turning it and all trailing
zeros into 0 followed by 1s (1010). AND-ing keeps only columns where both have a 1, which is
the original minus its rightmost 1. Each step knocks out one more column from the right.

Steps
-----
1. count = 0.
2. While n: n &= n - 1; count += 1.
3. Return count.

Complexity: O(k) time where k is the number of set bits (at most 32), O(1) space.
Pitfalls: Using str(bin(n)).count("1") in an interview without explaining the bit trick; in
languages with signed ints, a right shift of negatives sign-extends and never terminates (use
unsigned shift); misreading n & (n - 1) as n & ~(n - 1), which isolates the lowest bit instead.
"""


class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1          # erase the lowest set bit; one iteration per 1-bit
            count += 1
        return count


def brute_force(n: int) -> int:
    count = 0
    for i in range(32):         # inspects all 32 columns regardless of how many are set
        if (n >> i) & 1:
            count += 1
    return count


if __name__ == "__main__":
    s = Solution()
    assert s.hammingWeight(11) == 3
    assert s.hammingWeight(128) == 1
    assert s.hammingWeight(0) == 0                        # no set bits
    assert s.hammingWeight(2**32 - 1) == 32               # all set bits
    for n in (11, 128, 0, 2**32 - 1, 2**31, 123456789):
        assert s.hammingWeight(n) == brute_force(n), n
    print("ok")
