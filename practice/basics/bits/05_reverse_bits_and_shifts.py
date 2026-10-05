"""
Reverse Bits and Shifts (LeetCode 190) - Basics
Area: bits
Key operations: n & 1 peels the lowest bit, result = result << 1 | bit pushes it in from the right, n >>= 1, mask & 0xFFFFFFFF for logical shifts

LeetCode 190: reverse the 32 bits of an unsigned integer. Thirty-two rounds: take the lowest bit of
n, shift the result left and OR the bit in, shift n right. Python's >> is arithmetic (it keeps the
sign: -8 >> 1 == -4, it floors); a logical right shift of a 32-bit value is (n & 0xFFFFFFFF) >> k.
Example: reverse_bits(0b00000010100101000001111010011100) -> 964176192 (0b00111001011110000010100101000000)
"""


# --- brute force ---
def brute_force(n: int) -> int:
    """Format as a 32-character binary string, reverse it, parse it back. O(32) with string building."""
    return int(format(n, "032b")[::-1], 2)


# --- optimal ---
def reverse_bits(n: int) -> int:
    """Peel the lowest bit of n and push it into the result from the right, 32 times. O(32)."""
    result = 0
    for i in range(32):
        bit = n & 1
        result = (result << 1) | bit
        n >>= 1
    return result


def logical_right_shift(n: int, k: int) -> int:
    """Python's >> keeps the sign (arithmetic); mask to 32 bits first to shift in zeros (logical). O(1)."""
    unsigned = n & 0xFFFFFFFF
    return unsigned >> k


# --- demo ---
def demo():
    return reverse_bits(0b00000010100101000001111010011100), logical_right_shift(-8, 1)


# --- bugs ---
BUGS = [
    {
        "replace": "    for i in range(32):",
        "with":    "    for i in range(31):",
        "fix": "a 32-bit word needs exactly 32 rounds, one per bit",
        "why": "One round short leaves the result shifted one place too few: reverse_bits(1) returns 2^30 instead of 2^31.",
        "decoys": [
            {"line": "        n >>= 1", "change": "should be n <<= 1"},
            {"line": "        bit = n & 1", "change": "should be n & i"},
            {"line": "    result = 0", "change": "should start at 1"},
        ],
    },
    {
        "replace": "        result = (result << 1) | bit",
        "with":    "        result = result | (bit << i)",
        "fix": "shift the result left and bring the new bit in at the bottom; placing bit i at position i just rebuilds n",
        "why": "Setting bit i at position i copies n instead of reversing it: reverse_bits(1) returns 1 instead of 2^31.",
        "decoys": [
            {"line": "    for i in range(32):", "change": "should be range(1, 33)"},
            {"line": "    unsigned = n & 0xFFFFFFFF", "change": "should be n & 0x7FFFFFFF"},
            {"line": "    return result", "change": "should return result >> 1"},
        ],
    },
    {
        "replace": "    unsigned = n & 0xFFFFFFFF",
        "with":    "    unsigned = n",
        "fix": "mask to 32 bits first so a negative number becomes its two's-complement pattern and zeros shift in",
        "why": "Without the mask Python's >> stays arithmetic: logical_right_shift(-8, 1) returns -4 instead of 0x7FFFFFFC.",
        "decoys": [
            {"line": "    return unsigned >> k", "change": "should be unsigned << k"},
            {"line": "        bit = n & 1", "change": "should be n | 1"},
            {"line": "        n >>= 1", "change": "should be n >>= i"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
