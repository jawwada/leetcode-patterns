"""
Reverse Bits and Shifts - Fundamentals
Chapter: fundamentals/bits
Key operations: bit = n & 1, result = result << 1 | bit, n >>= 1, & 0xFFFFFFFF makes >> logical

LeetCode 190: reverse the 32 bits of an unsigned integer. Thirty-two rounds: take the lowest bit
of n, shift the result left and OR the bit in, shift n right. Python's >> is arithmetic (it keeps
the sign: -8 >> 1 == -4, it floors); a logical right shift of 32 bits is (n & 0xFFFFFFFF) >> k.
Example: reverse_bits(0b00000010100101000001111010011100) -> 964176192
         (that is 0b00111001011110000010100101000000)
"""


# --- algorithm ---
def reverse_bits(n):
    """Peel the lowest bit of n and push it into the result from the right, 32 times. O(32)."""
    result = 0
    for i in range(32):   # exactly 32 rounds, even after n reaches 0: the leading zeros count too
        bit = n & 1
        result = (result << 1) | bit
        n = n >> 1
    return result


def logical_right_shift(n, k):
    """Python's >> keeps the sign (arithmetic); mask to 32 bits first to shift in zeros. O(1)."""
    unsigned = n & 0xFFFFFFFF   # the 32-bit two's complement pattern as a positive number
    return unsigned >> k


# --- try it ---
rev = reverse_bits(0b00000010100101000001111010011100)
print(rev)                              # -> 964176192
print(format(rev, "032b"))              # -> 00111001011110000010100101000000
print(reverse_bits(1))                  # -> 2147483648
print(reverse_bits(0))                  # -> 0
print(-8 >> 1)                          # -> -4   (arithmetic: the sign stays)
print(logical_right_shift(-8, 1))       # -> 2147483644
print(logical_right_shift(16, 2))       # -> 4
