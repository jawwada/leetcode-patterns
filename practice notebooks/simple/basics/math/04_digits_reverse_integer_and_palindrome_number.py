"""
Reverse Integer and Palindrome Number (basics: math)
Reverse a 32-bit integer's digits (0 on overflow) and check palindrome numbers without strings.
  reverse_integer(-123)  ->  -321;  is_palindrome_number(12321)  ->  True

Idea: n % 10 is the last digit and n // 10 drops it; rev = rev * 10 + digit appends it to rev.
      Palindrome: reverse only the lower half of the digits, then compare it with the upper half.

Pseudocode:
  reverse_integer(x):
      sign = -1 if x < 0 else 1; n = |x|; rev = 0
      while n > 0: n, d = divmod(n, 10); rev = rev * 10 + d
      rev = sign * rev
      return rev if -2^31 <= rev <= 2^31 - 1 else 0
  is_palindrome_number(x):
      if x < 0, or (x % 10 == 0 and x != 0): return False
      half = 0
      while x > half: x, d = divmod(x, 10); half = half * 10 + d
      return x == half or x == half // 10      # even / odd digit count

Time O(number of digits), space O(1).
"""
INT_MIN, INT_MAX = -2**31, 2**31 - 1


def reverse_integer(x):
    sign = -1 if x < 0 else 1
    n, rev = abs(x), 0
    while n > 0:
        n, d = divmod(n, 10)             # peel off the last digit
        rev = rev * 10 + d               # append it to rev
    rev *= sign
    return rev if INT_MIN <= rev <= INT_MAX else 0  # outside 32 bits: 0


def is_palindrome_number(x):
    if x < 0 or (x % 10 == 0 and x != 0):  # -121 and 10 cannot be palindromes
        return False
    half = 0
    while x > half:                      # move digits until half catches up
        x, d = divmod(x, 10)
        half = half * 10 + d
    return x == half or x == half // 10  # 1221: 12 == 12; 12321: 12 == 123 // 10


if __name__ == "__main__":
    print(reverse_integer(-123))         # -321
    print(reverse_integer(1534236469))   # 0
    print(is_palindrome_number(12321))   # True
    print(is_palindrome_number(10))      # False
