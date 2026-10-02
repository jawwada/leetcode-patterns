"""
Reverse Bits (LeetCode 190)  — Easy
Pattern: Bit-by-bit shift and accumulate

Problem
-------
Reverse the bits of a 32-bit unsigned integer: bit 0 becomes bit 31, bit 1 becomes bit 30, etc.
Example: 43261596 (00000010100101000001111010011100) -> 964176192 (00111001011110000010100101000000).
Example: 1 -> 2147483648 (2^31).

Brute force
-----------
Convert to a binary string, zero-pad on the left to 32 characters, reverse the string, and parse
it back with int(..., 2). O(32) time, O(32) space. The waste: three separate passes over a
32-character text buffer (format, reverse, parse) plus heap allocation for the strings, to do what
is really a fixed sequence of shifts and ORs on a single machine word.

From brute force to optimal
---------------------------
The redundancy is the detour through text. Observation: reversing 32 bits is "read the input
from the right, write the output from the left". Reading from the right is n & 1 followed by
n >>= 1; writing from the left is result = (result << 1) | bit. Running that 32 times moves
each bit from position i to position 31 - i directly in the register, no allocation, no parsing.
(The constant-time refinement swaps halves, then quarters, then bytes, nibbles, pairs, single
bits with masks: 5 steps instead of 32, which is what hardware-oriented code does.)

Intuition
---------
Peel the lowest bit off the input and push it onto the bottom of the output; after 32 peels the
first bit peeled has been pushed up 31 times and sits at the top. The two numbers behave like a
conveyor belt feeding a stack.

Geometric view
--------------
Two 32-column rows. Each step the input row shifts right (its rightmost column falls off) and
the output row shifts left (making room at the right), and the fallen column is dropped into
that gap. After 32 steps the order of the columns is mirrored.

Steps
-----
1. result = 0.
2. Repeat 32 times: result = (result << 1) | (n & 1); n >>= 1.
3. Return result.

Complexity: O(32) = O(1) time, O(1) space — fixed 32 iterations on two integers.
Pitfalls: Looping only until n becomes 0 (leading zeros of the input must become trailing
zeros of the output: always do all 32 iterations); in C/Java forgetting the unsigned shift;
in Python forgetting that ints are unbounded so you must mask or loop exactly 32 times.
"""


class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for _ in range(32):                      # all 32 columns, even the leading zeros
            result = (result << 1) | (n & 1)     # push the input's lowest bit onto the output
            n >>= 1
        return result


def brute_force(n: int) -> int:
    bits = format(n, "032b")                     # text detour: format, reverse, parse
    return int(bits[::-1], 2)


if __name__ == "__main__":
    s = Solution()
    assert s.reverseBits(0b00000010100101000001111010011100) == 964176192
    assert s.reverseBits(0b11111111111111111111111111111101) == 3221225471
    assert s.reverseBits(0) == 0                                     # all zeros
    assert s.reverseBits(1) == 2**31                                 # bit 0 -> bit 31
    for n in (43261596, 4294967293, 0, 1, 2**32 - 1, 0xF0F0F0F0):
        assert s.reverseBits(n) == brute_force(n), n
    print("ok")
