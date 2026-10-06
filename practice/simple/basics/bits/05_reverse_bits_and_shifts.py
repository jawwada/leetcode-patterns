"""
Reverse Bits and Shifts (basics: bits)
Reverse the 32 bits of an unsigned integer, and shift right with zeros coming in (logical shift).
  00000010100101000001111010011100  ->  00111001011110000010100101000000

Idea: 32 rounds: peel the lowest bit off n, push it into the result from the right, drop it
      from n. The first bit peeled gets pushed furthest left, so the order flips.
      Python's >> keeps the sign (-8 >> 1 == -4); mask to 32 bits first to shift in zeros.

Pseudocode:
  reverse_bits(n):
      result = 0
      repeat 32 times:
          bit = n & 1
          result = (result << 1) | bit
          n = n >> 1
      return result
  logical_right_shift(n, k):  return (n & 0xFFFFFFFF) >> k

Time O(32) = O(1), space O(1).
"""


def reverse_bits(n):
    result = 0
    for _ in range(32):                  # one round per bit
        bit = n & 1                      # peel the lowest bit of n
        result = (result << 1) | bit     # push it into the result from the right
        n >>= 1                          # drop it from n
    return result


def logical_right_shift(n, k):
    unsigned = n & 0xFFFFFFFF            # the 32-bit pattern of n, never negative
    return unsigned >> k                 # so zeros shift in from the left


if __name__ == "__main__":
    n = 0b00000010100101000001111010011100      # 43261596
    print(format(reverse_bits(n), "032b"))      # 00111001011110000010100101000000
    print(reverse_bits(n))                      # 964176192
    print(reverse_bits(1))                      # 2147483648
    print(-8 >> 1, logical_right_shift(-8, 1))  # -4 2147483644
