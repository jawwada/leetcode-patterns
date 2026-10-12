"""
Base Conversion and Excel Column Titles (basics: math)
Convert to and from base b (2..36), and between Excel column numbers and titles (28 = AB).
  to_base(255, 16)  ->  'ff';  from_base('ff', 16)  ->  255;  column_title(701)  ->  'ZY'

Idea: divmod(n, b) peels off the lowest digit, so digits come out backwards: reverse at the end.
      Reading back is Horner's rule, n = n * b + digit, left to right.
      Excel is base 26 with digits A..Z = 1..26 and no zero: subtract 1 before each divmod.

Pseudocode:
  to_base(n, b):      while n > 0: n, d = divmod(n, b); collect digit d; return them reversed
  from_base(s, b):    n = 0; for ch in s: n = n * b + value(ch)
  column_title(n):    while n > 0: n, r = divmod(n - 1, 26); collect letter r (0 = A); reverse
  column_number(s):   n = 0; for ch in s: n = n * 26 + (position of ch, A = 1)

Time O(number of digits) for each, space O(number of digits).
"""
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, b):
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n, digits = abs(n), []
    while n > 0:
        n, d = divmod(n, b)              # d is the lowest digit
        digits.append(DIGITS[d])
    return sign + "".join(reversed(digits))  # lowest digit came out first


def from_base(s, b):
    n = 0
    for ch in s:                         # Horner: shift one digit left, add ch
        n = n * b + DIGITS.index(ch)
    return n


def column_title(n):
    letters = []
    while n > 0:
        n, r = divmod(n - 1, 26)         # -1: digits run 1..26, not 0..25
        letters.append(chr(ord("A") + r))
    return "".join(reversed(letters))


def column_number(s):
    n = 0
    for ch in s:                         # A = 1, B = 2, ..., Z = 26
        n = n * 26 + ord(ch) - ord("A") + 1
    return n


if __name__ == "__main__":
    print(to_base(2026, 2), to_base(255, 16))                     # 11111101010 ff
    print(from_base("11111101010", 2), from_base("ff", 16))       # 2026 255
    print(column_title(26), column_title(27), column_title(701))  # Z AA ZY
    print(column_number("AB"), column_number("ZY"))               # 28 701
