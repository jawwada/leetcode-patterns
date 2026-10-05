"""
Number of 1 Bits (LeetCode 191) - Easy
Chapter: bit_manipulation
Pattern: Clear lowest set bit (n & (n - 1))

Given a 32-bit unsigned integer n, return how many 1 bits its binary form has (the Hamming
weight).
Example: 11 (binary 1011) -> 3; 128 (binary 10000000) -> 1.
"""


# --- brute force ---
def brute_force(n):
    """Test each of the 32 bit positions one by one. O(32) time, O(1) space."""
    count = 0
    for i in range(32):                      # every column is inspected, even when it is 0
        bit = (n >> i) & 1                   # shift bit i down to the bottom, then look at it
        if bit == 1:
            count = count + 1
    return count


# --- optimal ---
def number_of_1_bits(n):
    """Clear the lowest set bit until nothing is left. O(k) time for k set bits, O(1) space."""
    count = 0
    while n != 0:
        n = n & (n - 1)                      # n - 1 flips the lowest 1 and the zeros below it
        count = count + 1
    return count


# --- try the brute force ---
print(brute_force(11))           # -> 3
print(brute_force(128))          # -> 1
print(brute_force(0))            # -> 0
print(brute_force(4294967295))   # -> 32


# --- try the optimal ---
print(number_of_1_bits(11))           # -> 3
print(number_of_1_bits(128))          # -> 1
print(number_of_1_bits(0))            # -> 0
print(number_of_1_bits(4294967295))   # -> 32
