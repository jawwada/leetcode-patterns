"""
Count Set Bits and the Lowest Set Bit - Basics
Area: bits
Key operations: n & (n - 1) drops the lowest set bit, n & -n isolates it, power of two is n > 0 and n & (n - 1) == 0

Subtracting 1 flips the lowest set bit to 0 and every 0 below it to 1, so n & (n - 1) clears exactly
that bit (Kernighan's count loops once per set bit). -n is ~n + 1: it keeps the lowest set bit and
everything below it, and flips everything above, so n & -n keeps only the lowest set bit. A positive
number is a power of two exactly when dropping its lowest set bit leaves 0.
Example: n = 180 = 10110100 -> 4 set bits; lowest set bit 00000100 = 4; not a power of two
"""
from typing import Tuple


# --- brute force ---
def brute_force(n: int) -> Tuple[int, int, bool]:
    """Walk every bit position of the binary string. O(bit length) instead of O(set bits) or O(1)."""
    count = bin(n).count("1")
    lowest = next((1 << i for i in range(n.bit_length()) if n >> i & 1), 0)
    return count, lowest, n > 0 and count == 1


# --- optimal ---
def count_bits(n: int) -> int:
    """Kernighan: n &= n - 1 drops the lowest set bit; count how many drops reach 0. O(set bits)."""
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def lowest_set_bit(n: int) -> int:
    """n & -n keeps only the lowest set bit (0 for n == 0). O(1)."""
    return n & -n


def is_power_of_two(n: int) -> bool:
    """Exactly one set bit: positive, and dropping the lowest set bit leaves 0. O(1)."""
    return n > 0 and n & (n - 1) == 0


def solve(n: int) -> Tuple[int, int, bool]:
    """Return (set bit count, lowest set bit, is power of two)."""
    return count_bits(n), lowest_set_bit(n), is_power_of_two(n)


# --- demo ---
def demo():
    return solve(0b10110100)


# --- bugs ---
BUGS = [
    {
        "replace": "    return n > 0 and n & (n - 1) == 0",
        "with":    "    return n & (n - 1) == 0",
        "fix": "require n > 0 as well: 0 & -1 == 0 but zero is not a power of two",
        "why": "For n = 0, n - 1 is -1 (all ones) and 0 & -1 == 0, so is_power_of_two(0) returns True.",
        "decoys": [
            {"line": "        n &= n - 1", "change": "should be n &= n + 1"},
            {"line": "    return n & -n", "change": "should be n & ~n"},
            {"line": "        count += 1", "change": "should add the dropped bit's value"},
        ],
    },
    {
        "replace": "    while n:",
        "with":    "    while n > 1:",
        "fix": "loop while n is nonzero; the final 1 is a set bit that still has to be counted",
        "why": "Stopping at n == 1 misses the last set bit of every nonzero number: count_bits(1) returns 0 and count_bits(0b10110100) returns 3.",
        "decoys": [
            {"line": "    return n > 0 and n & (n - 1) == 0", "change": "should be n >= 0"},
            {"line": "    count = 0", "change": "should start at 1"},
            {"line": "    return count_bits(n), lowest_set_bit(n), is_power_of_two(n)", "change": "wrong order of the three results"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
