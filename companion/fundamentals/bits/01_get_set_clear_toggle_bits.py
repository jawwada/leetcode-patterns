"""
Get, Set, Clear and Toggle a Bit - Fundamentals
Chapter: fundamentals/bits
Key operations: mask = 1 << i, n | mask sets, n & ~mask clears, n ^ mask toggles, n >> i & 1 reads

Every single-bit operation starts from the mask 1 << i: a lone 1 in position i, counting from the
right, 0-based. OR with the mask forces the bit to 1, AND with the complement forces it to 0, XOR
flips it, and shifting the bit down to position 0 then AND 1 reads it. Writing a value v into bit
i is clear-then-OR.
Example: n = 00101010; set bit 0 -> 00101011; clear bit 3 -> 00100011; toggle bit 7 -> 10100011
"""


# --- algorithm ---
def get_bit(n, i):
    """Shift bit i down to position 0 and keep only that bit. O(1)."""
    return (n >> i) & 1


def set_bit(n, i):
    """OR with the mask: bit i becomes 1, the other bits are unchanged. O(1)."""
    mask = 1 << i
    return n | mask


def clear_bit(n, i):
    """AND with the complement of the mask: bit i becomes 0, the other bits are unchanged. O(1)."""
    mask = 1 << i
    return n & ~mask   # ~mask has a 0 at position i and 1 everywhere else


def toggle_bit(n, i):
    """XOR with the mask: bit i flips, the other bits are unchanged. O(1)."""
    mask = 1 << i
    return n ^ mask


def update_bit(n, i, v):
    """Clear bit i, then OR in v shifted into place. O(1)."""
    cleared = clear_bit(n, i)   # clear first, or OR-ing a 0 would leave an old 1 in place
    return cleared | (v << i)


# --- try it ---
n = 0b00101010
n = set_bit(n, 0)
print(format(n, "08b"))    # -> 00101011
n = clear_bit(n, 3)
print(format(n, "08b"))    # -> 00100011
n = toggle_bit(n, 7)
print(format(n, "08b"))    # -> 10100011
n = update_bit(n, 5, 0)
print(format(n, "08b"))    # -> 10000011
print(get_bit(n, 7))       # -> 1
print(get_bit(n, 2))       # -> 0
