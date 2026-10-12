"""
Count Set Bits and the Lowest Set Bit (basics: bits)
For n >= 0: count its 1 bits, keep only its lowest 1 bit, and test whether it is a power of two.
  n = 180 = 10110100  ->  4 set bits, lowest set bit 00000100 = 4, not a power of two

Idea: n - 1 turns the lowest 1 into 0 and the 0s below it into 1s, so n & (n - 1) drops it.
      -n is ~n + 1: the only 1 it shares with n is n's lowest 1, so n & -n keeps just that bit.
      A power of two has exactly one 1 bit: n > 0 and dropping that bit leaves 0.

Pseudocode:
  count_bits(n):
      count = 0
      while n != 0: n = n & (n - 1); count += 1    # one round per set bit
      return count
  lowest_set_bit(n):   return n & -n
  is_power_of_two(n):  return n > 0 and (n & (n - 1)) == 0

Time O(set bits) for count_bits, O(1) for the other two; space O(1).
"""


def count_bits(n):
    count = 0
    while n:                             # Kernighan: one round per set bit
        n &= n - 1                       # drop the lowest set bit
        count += 1
    return count


def lowest_set_bit(n):
    return n & -n                        # the only 1 that n and -n share


def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0  # exactly one set bit


if __name__ == "__main__":
    print(count_bits(180), lowest_set_bit(180), is_power_of_two(180))  # 4 4 False
    print(count_bits(64), lowest_set_bit(64), is_power_of_two(64))     # 1 64 True
    print(count_bits(0), lowest_set_bit(0), is_power_of_two(0))        # 0 0 False
