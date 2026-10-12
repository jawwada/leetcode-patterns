"""
Count Set Bits - Brian Kernighan's n & (n - 1)

Count the 1 bits in the binary form of a non-negative integer, test for a
power of two, and count the 1 bits of every number from 0 to n:
44 = 101100 -> 3 set bits.
"""


# --- algorithm ---
def count_set_bits(n):
    """Kernighan: n & (n - 1) clears the lowest set bit. O(set bits)."""
    count = 0
    while n > 0:
        n = n & (n - 1)                 # the lowest 1 becomes 0
        count += 1
    return count


def is_power_of_two(n):
    """A power of two has exactly one set bit. O(1)."""
    return n > 0 and (n & (n - 1)) == 0


def count_bits_up_to(n):
    """bits[i] = bits[i >> 1] + (i & 1) for every i in 0..n. O(n)."""
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)    # i >> 1 drops i's last bit
    return bits


# --- try it ---
print(count_set_bits(44))           # -> 3
print(count_set_bits(0))            # -> 0
print(is_power_of_two(64))          # -> True
print(is_power_of_two(0))           # -> False
print(count_bits_up_to(5))          # -> [0, 1, 1, 2, 1, 2]
