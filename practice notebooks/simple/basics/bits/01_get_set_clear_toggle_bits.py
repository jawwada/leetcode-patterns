"""
Get, Set, Clear and Toggle a Bit (basics: bits)
Read or change bit i of an integer n (bit 0 is the rightmost) using the mask 1 << i.
  n = 00101010:  set bit 0 -> 00101011,  clear bit 3 -> 00100010,  get bit 5 -> 1

Idea: 1 << i is a lone 1 at position i. OR with it forces bit i to 1, AND with its
      complement ~(1 << i) (all ones except position i) forces it to 0, XOR flips it.
      To read bit i, shift it down to position 0 and keep only that bit with & 1.

Pseudocode:
  mask = 1 << i
  get_bit(n, i):        (n >> i) & 1
  set_bit(n, i):        n | mask
  clear_bit(n, i):      n & ~mask
  toggle_bit(n, i):     n ^ mask
  update_bit(n, i, v):  (n & ~mask) | (v << i)    # clear first, then OR in v (0 or 1)

Time O(1) per operation, space O(1).
"""


def get_bit(n, i):
    return (n >> i) & 1                  # bit i down to position 0, keep only it


def set_bit(n, i):
    return n | (1 << i)                  # OR: bit i becomes 1, the rest unchanged


def clear_bit(n, i):
    return n & ~(1 << i)                 # AND with all ones except bit i: bit i becomes 0


def toggle_bit(n, i):
    return n ^ (1 << i)                  # XOR: bit i flips, the rest unchanged


def update_bit(n, i, v):
    return (n & ~(1 << i)) | (v << i)    # clear bit i, then OR in v


if __name__ == "__main__":
    n = 0b00101010
    print(get_bit(n, 5), get_bit(n, 4))                                  # 1 0
    print(format(set_bit(n, 0), "08b"), format(clear_bit(n, 3), "08b"))  # 00101011 00100010
    print(format(toggle_bit(n, 7), "08b"))                               # 10101010
    print(format(update_bit(n, 5, 0), "08b"))                            # 00001010
