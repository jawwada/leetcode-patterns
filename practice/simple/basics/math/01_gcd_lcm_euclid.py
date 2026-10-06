"""
GCD and LCM with Euclid's Algorithm (basics: math)
Return the greatest common divisor and the least common multiple of two integers.
  252, 105  ->  gcd 21, lcm 1260

Idea: any number that divides both a and b also divides a % b, so gcd(a, b) = gcd(b, a % b).
      The pair shrinks fast, and when b reaches 0 the gcd is a. Then lcm = |a * b| / gcd.

Pseudocode:
  gcd(a, b):
      a, b = |a|, |b|
      while b != 0: a, b = b, a % b     # (252, 105) -> (105, 42) -> (42, 21) -> (21, 0)
      return a
  lcm(a, b):
      if a == 0 or b == 0: return 0
      return |a| // gcd(a, b) * |b|     # divide first so the product stays small

Time O(log min(a, b)), space O(1).
"""


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:                             # stop when the remainder is 0
        a, b = b, a % b                  # common divisors stay the same
    return a


def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)  # divide first, then multiply


if __name__ == "__main__":
    print(gcd(252, 105), lcm(252, 105))  # 21 1260
    print(gcd(-12, 18), lcm(-12, 18))    # 6 36
    print(gcd(0, 5), lcm(0, 5))          # 5 0
