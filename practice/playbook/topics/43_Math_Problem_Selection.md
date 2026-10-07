## Choosing a Mathematical Representation

This reference compares the integer, bit, digit, and geometry representations. Follow the topic index to the corresponding runnable lesson before trying a referenced function.

<!-- cell -->

### Where it goes wrong

Most bit bugs come from Python ints having no width, and most math bugs from floats or from numbering that starts at 1.

1. **Operator precedence.** In Python `&`, `|` and `^` bind tighter than `==`, so `x & 1 == 0` works, unlike in C and Java. But `<<` and `>>` bind *looser* than `+` and `-`: `1 << k - 1` is `1 << (k - 1)`, and `x & mask + 1` is `x & (mask + 1)`. Parenthesise every bit expression.
2. **`~x` is negative in Python.** Ints have no fixed width, so `~0b1010 == -11`, not `0b0101`. For a k-bit complement use `x ^ ((1 << k) - 1)`.
3. **Negative numbers never run out of bits.** `-1 >> 1 == -1`, so `while x: x >>= 1` never ends for a negative x, and neither does the `x &= x - 1` loop. Mask first: `x & 0xFFFFFFFF` is the 32-bit pattern, and `to_signed32` turns it back.
4. **Digits of a negative number.** `divmod(-123, 10) == (-13, 7)`, so the last digit comes out as 7; and `divmod(-1, 10) == (-1, 9)`, so `while n:` never ends. Work on `abs(x)` and restore the sign; [Python Toolkit](03_Python_Toolkit.ipynb#topic-python-toolkit) has more on `%` and `//` with negatives.
5. **Stopping a fixed-width loop early.** Reverse Bits must run exactly 32 rounds; stopping when `x == 0` loses the leading zeros that should become trailing zeros, so `reverse_bits(1)` comes back as 1 instead of 2147483648.
6. **Zero passes the power-of-two test.** `0 & (0 - 1) == 0`, so write `x > 0 and (x & (x - 1)) == 0`.
7. **Floats for exact questions.** `math.log(243, 3) == 4.999999999999999`, and `int(math.sqrt(100000001**2 - 1))` is 100000001 while `math.isqrt` gives the true 100000000. Use integers: reduced `(dx, dy)` pairs, cross products, `math.isqrt`, repeated multiplication instead of logs.
8. **Reducing mod at the wrong moment.** Reduce after every multiply (`ans = ans * x % MOD`), but never before comparing: with `a = 10**9 + 8` and `b = 5`, `max(a % MOD, b % MOD)` picks `b`.
9. **Off by one in 1-indexed systems.** Excel columns need `n - 1` before the divmod, or `column_title(26)` gives `"BA"`; the k-th permutation needs the rank `k - 1`; and "primes less than n" is not "primes up to n".
10. **Testing after adding.** In the bit-array template, test bit v *before* you set it, or every value looks like a repeat: `[1, 2, 2, 4]` answers `[4, 3]`.
11. **Duplicate points.** `slope_key(0, 0)` divides by `gcd(0, 0) == 0`: count copies of the anchor separately.

### Edge cases to say out loud

Say these before coding, because each one lands on a guard above. 0 and 1 (no set bits, `is_prime(1)`) · negative numbers (infinite sign bits in Python) · the 32-bit limits (2³¹ − 1 and −2³¹) · the missing value is 0 or n · duplicate points and vertical lines · `mod = 1` · an empty input.

<!-- cell -->

**Try it**
- Run `all(column_number(column_title(n)) == n for n in range(1, 1000))`: True. Two inverse functions test each other.
- What should `missing_number([])` return? Write the assert before running it (0: the range 0..0 lost its only value).
- Predict `find_error_nums([1, 2, 3, 3])` before running: `[3, 4]`, where the missing value is n itself, the top bit of `full`. Build `full` as `(1 << n) - 2` instead and that bit is lost: the answer becomes `[3, -1]`.
