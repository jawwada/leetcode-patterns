"""
Fast Power and Modular Arithmetic (basics: math)
Compute base ** exp with O(log exp) multiplications, and base ** exp % mod without huge numbers.
  power(3, 13)  ->  1594323;  mod_power(3, 13, 1000)  ->  323

Idea: write exp in binary: 13 = 1101b, so 3^13 = 3^8 * 3^4 * 3^1. Square the base once per bit
      (3, 3^2, 3^4, 3^8, ...) and multiply it into the result when that bit is 1.
      For mod, reduce after every product: (a * b) % m == ((a % m) * (b % m)) % m.

Pseudocode:
  power(base, exp):
      result = 1
      while exp > 0:
          if exp & 1: result = result * base     # lowest bit is 1
          base = base * base                     # the next bit is worth base^2
          exp = exp >> 1                         # drop the lowest bit
      return result
  mod_power(base, exp, mod): the same loop, with % mod after every product

Time O(log exp) multiplications, space O(1).
"""


def power(base, exp):
    result = 1
    while exp > 0:
        if exp & 1:                      # lowest bit is 1: multiply it in
            result *= base
        base *= base                     # base, base^2, base^4, base^8, ...
        exp >>= 1                        # move on to the next bit
    return result


def mod_power(base, exp, mod):
    result, base = 1, base % mod         # Python: -2 % 5 == 3, never negative
    while exp > 0:
        if exp & 1:
            result = result * base % mod  # reduce after every product
        base = base * base % mod
        exp >>= 1
    return result % mod                  # exp == 0 with mod == 1 gives 0


if __name__ == "__main__":
    print(power(3, 13), power(2, 0))     # 1594323 1
    print(mod_power(3, 13, 1000))        # 323
    print(mod_power(-2, 3, 5))           # 2
