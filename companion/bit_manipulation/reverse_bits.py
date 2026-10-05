"""
Reverse Bits (LeetCode 190) - Easy
Chapter: bit_manipulation
Pattern: Bit-by-bit shift and accumulate

Reverse the bits of a 32-bit unsigned integer: bit 0 becomes bit 31, bit 1 becomes bit 30,
and so on.
Example: 43261596 (00000010100101000001111010011100)
      -> 964176192 (00111001011110000010100101000000).
"""


# --- brute force ---
def brute_force(n):
    """Detour through a 32-character binary string and reverse it. O(32) time, O(32) space."""
    bits = format(n, "032b")                 # e.g. 1 -> "00000000000000000000000000000001"
    reversed_bits = bits[::-1]
    return int(reversed_bits, 2)             # parse the reversed text back into a number


# --- optimal ---
def reverse_bits(n):
    """Peel the lowest bit off n and push it onto the result, 32 times. O(1) time and space."""
    result = 0
    for step in range(32):                   # all 32 columns, including the leading zeros
        lowest = n & 1
        result = (result << 1) | lowest      # make room at the bottom, drop the bit in
        n = n >> 1
    return result


# --- try the brute force ---
print(brute_force(43261596))     # -> 964176192
print(brute_force(4294967293))   # -> 3221225471
print(brute_force(0))            # -> 0
print(brute_force(1))            # -> 2147483648


# --- try the optimal ---
print(reverse_bits(43261596))     # -> 964176192
print(reverse_bits(4294967293))   # -> 3221225471
print(reverse_bits(0))            # -> 0
print(reverse_bits(1))            # -> 2147483648
