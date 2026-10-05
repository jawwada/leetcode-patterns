"""
Count Set Bits and the Lowest Set Bit - Fundamentals
Chapter: fundamentals/bits
Key operations: n & (n-1) drops lowest set bit, n & -n isolates it, power of two iff that leaves 0

Subtracting 1 flips the lowest set bit to 0 and every 0 below it to 1, so n & (n - 1) clears
exactly that bit (Kernighan's count loops once per set bit). -n is ~n + 1: it keeps the lowest set
bit and everything below it and flips everything above, so n & -n keeps only the lowest set bit. A
positive number is a power of two exactly when dropping its lowest set bit leaves 0.
Example: n = 180 = 10110100 -> 4 set bits; lowest set bit 00000100 = 4; not a power of two
"""


# --- algorithm ---
def count_bits(n):
    """Kernighan: n & (n - 1) drops the lowest set bit; count the drops until 0. O(set bits)."""
    count = 0
    while n:
        n = n & (n - 1)   # one set bit disappears per round
        count += 1
    return count


def lowest_set_bit(n):
    """n & -n keeps only the lowest set bit (0 for n == 0). O(1)."""
    return n & -n


def is_power_of_two(n):
    """Exactly one set bit: positive, and dropping the lowest set bit leaves 0. O(1)."""
    if n <= 0:   # 0 has no set bit at all; the trick alone would say yes for 0
        return False
    return n & (n - 1) == 0


# --- try it ---
print(count_bits(0b10110100))        # -> 4
print(lowest_set_bit(0b10110100))    # -> 4
print(is_power_of_two(0b10110100))   # -> False
print(is_power_of_two(64))           # -> True
print(count_bits(0))                 # -> 0
print(is_power_of_two(0))            # -> False
