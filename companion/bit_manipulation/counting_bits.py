"""
Counting Bits (LeetCode 338) - Easy
Chapter: bit_manipulation
Pattern: Reuse the count of i >> 1

Given n, return a list of length n + 1 whose entry i is the number of 1 bits in the binary form
of i.
Example: 5 -> [0, 1, 1, 2, 1, 2] (for 0, 1, 10, 11, 100, 101).
"""


# --- brute force ---
def brute_force(n):
    """Count the bits of every number separately, 32 tests each. O(32 * n) time."""
    result = []
    for num in range(n + 1):
        count = 0
        for b in range(32):
            if (num >> b) & 1 == 1:          # is bit b of num set?
                count = count + 1
        result.append(count)
    return result


# --- optimal ---
def counting_bits(n):
    """bits[i] = bits[i >> 1] + lowest bit of i. O(n) time, O(1) extra space."""
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        half = i >> 1                        # drop the lowest bit: a smaller number, already done
        bits[i] = bits[half] + (i & 1)
    return bits


# --- try the brute force ---
print(brute_force(2))   # -> [0, 1, 1]
print(brute_force(5))   # -> [0, 1, 1, 2, 1, 2]
print(brute_force(0))   # -> [0]
print(brute_force(7))   # -> [0, 1, 1, 2, 1, 2, 2, 3]


# --- try the optimal ---
print(counting_bits(2))   # -> [0, 1, 1]
print(counting_bits(5))   # -> [0, 1, 1, 2, 1, 2]
print(counting_bits(0))   # -> [0]
print(counting_bits(7))   # -> [0, 1, 1, 2, 1, 2, 2, 3]
