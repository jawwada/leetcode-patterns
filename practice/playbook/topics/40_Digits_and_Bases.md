## Digits and Number Bases

Modulo extracts the last digit; integer division removes it. Keep the base and digit range explicit, especially when digits are numbered from one.

<!-- cell -->

Digits come next. `n % 10` is the last digit and `n // 10` drops it, so digits come out lowest first, and `rev * 10 + d` pushes a digit onto the right end of `rev`. Work on `abs(x)` and put the sign back at the end. Every base works the same way with `divmod(n, b)`, and reading digits back is Horner's rule, `n = n * b + d`. Excel columns are base 26 with digits 1..26 and *no zero*, so shift each digit down by one before the divmod.

Reverse Integer asks for the digits of a 32-bit integer in reverse order, or 0 when the result leaves 32 bits: −123 gives −321, and 1534236469 gives 0. A 32-bit language cannot compute `rev * 10 + d` and look afterwards, so test *before* pushing, `rev > (LIMIT - d) // 10`. One limit, 2³¹ − 1, serves both signs: −2³¹ could only come from reversing 8463847412, which is not a 32-bit input.

Palindrome Number asks whether an integer reads the same backwards, without turning it into a string: 12321 does, 10 does not. Reverse only the lower half of the digits and compare it with the upper half. Excel Sheet Column Title turns a column number into its letters, 28 into `AB`, and `column_number` goes back, `ZY` to 701.

<!-- cell -->

```python
def reverse_int(x):                            # Reverse Integer: 0 if the result leaves 32 bits
    LIMIT = 2**31 - 1
    n, rev = abs(x), 0
    while n:
        n, d = divmod(n, 10)                   # peel off the last digit
        if rev > (LIMIT - d) // 10:            # rev * 10 + d would pass the limit: stop BEFORE
            return 0
        rev = rev * 10 + d                     # push d onto the right of rev
    return rev if x >= 0 else -rev


def is_palindrome_number(x):                   # Palindrome Number, without strings
    if x < 0 or (x % 10 == 0 and x != 0):      # a minus sign, or a trailing 0 that cannot lead
        return False
    rev = 0
    while x > rev:                             # move digits until rev holds the lower half
        x, d = divmod(x, 10)
        rev = rev * 10 + d
    return x == rev or x == rev // 10          # even length, or odd (the middle digit is in rev)


def column_title(n):                           # 1 -> A, 26 -> Z, 27 -> AA
    out = []
    while n:
        n, r = divmod(n - 1, 26)               # shift 1..26 down to 0..25 first
        out.append(chr(ord("A") + r))
    return "".join(reversed(out))


def column_number(title):
    n = 0
    for ch in title:
        n = n * 26 + (ord(ch) - ord("A") + 1)  # Horner: shift one digit left, add this one
    return n


print(reverse_int(-123), reverse_int(1534236469), reverse_int(120))     # -321 0 21
print(is_palindrome_number(12321), is_palindrome_number(1221), is_palindrome_number(10))   # True True False
print(column_title(28), column_title(701), column_number("ZY"))         # AB ZY 701
```

<!-- cell -->

**Try it**
- Remove the `- 1` in `column_title` and run `column_title(26)`: `"BA"` instead of `"Z"`. Plain base 26 writes 26 as "10"; Excel has no zero digit, so 26 is the single digit Z.
- `reverse_int(1463847412)` is 2147483641, which fits; `reverse_int(1563847412)` would be 2147483651, which does not, so it returns 0.
- Drop the `x % 10 == 0 and x != 0` test and run `is_palindrome_number(10)`: `True`. Its trailing 0 becomes the leading digit of `rev`, and the comparison cannot see it.

<!-- cell -->

```python
assert reverse_int(-2**31) == 0 and reverse_int(0) == 0 and reverse_int(120) == 21

assert is_palindrome_number(0) and not is_palindrome_number(-121)

assert column_title(1) == "A" and column_title(52) == "AZ" and column_number("AAA") == 703
```
