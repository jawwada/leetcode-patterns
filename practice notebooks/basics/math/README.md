# Math fundamentals

Interview math is integer arithmetic done carefully: peeling digits with `divmod`, Euclid's gcd, the sieve, squaring your way to a power, writing a number in another base, and sampling from a stream. None of it needs more than `%`, `//`, `*` and a loop; what matters is knowing the one identity each technique rests on and the one edge case that breaks it (zero, negatives, the last step of a loop).

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| `n, d = divmod(n, 10)` peels the lowest digit | O(1) per digit, O(log n) total | digits come out least significant first |
| `rev = rev * 10 + d` rebuilds a number (Horner) | O(1) per digit | the same line reads any base: `n = n * b + digit` |
| `a, b = b, a % b` until `b == 0` (Euclid) | O(log min(a, b)) | the pair at least halves every two steps |
| `lcm = a // gcd * b` | O(log min(a, b)) | divide first, the product stays small; lcm(0, x) = 0 |
| trial division `while d * d <= n` | O(sqrt n) | a divisor above sqrt(n) pairs with one below it |
| sieve of Eratosthenes up to n | O(n log log n) time, O(n) space | start crossing off at p * p; stop at p = sqrt(n) |
| binary exponentiation | O(log exp) multiplications | square the base each round, multiply in on a 1 bit |
| `x = x * y % m` after every product | numbers stay below m^2 | `(a * b) % m == ((a % m) * (b % m)) % m` |
| base conversion to/from base b | O(log_b n) | `divmod(n - 1, 26)` for 1-based digits (Excel) |
| reservoir sampling of k from a stream | O(n) time, O(k) space | item i enters with probability k / (i + 1) |

## Drawn example: Euclid on (252, 105), then 3^13 by squaring

```
gcd:  (252, 105)   252 = 2 * 105 + 42      every common divisor of 252 and 105
      (105,  42)   105 = 2 *  42 + 21      also divides the remainder, so the
      ( 42,  21)    42 = 2 *  21 +  0      set of common divisors never changes
      ( 21,   0)   b == 0 -> gcd = 21      lcm = 252 // 21 * 105 = 1260

3^13, 13 = 1101b, bits read right to left:
      bit 1  result = 1 * 3       = 3        base -> 3^2  = 9
      bit 0  result unchanged     = 3        base -> 3^4  = 81
      bit 1  result = 3 * 81      = 243      base -> 3^8  = 6561
      bit 1  result = 243 * 6561  = 1594323  done: 3^13 = 3^1 * 3^4 * 3^8
```

## Python's `//` and `%`: floor, not truncation

`a // b` rounds toward negative infinity and `a % b` takes the **sign of the divisor**, so `a == (a // b) * b + a % b` always holds:

```
 7 //  3 =  2     7 %  3 =  2
-7 //  3 = -3    -7 %  3 =  2     (C would give -2 and -1)
 7 // -3 = -3     7 % -3 = -2
-7 // -3 =  2    -7 % -3 = -1
```

This is why `(-8) % 5 == 2` and a modular power is never negative for a positive modulus, and why `int(-7 / 3)` (which truncates to -2) is not the same as `-7 // 3`.

## The identities to say out loud

- "gcd(a, b) = gcd(b, a mod b), and gcd times lcm is |a times b|."
- "If n is composite it has a divisor no larger than sqrt(n), so trial division stops at `d * d <= n`."
- "x^e = (x^2)^(e // 2) times x^(e mod 2): one squaring per bit of e."
- "Digits come out backwards: divmod gives the lowest digit first, Horner puts them back."
- "Excel has no zero digit: subtract 1 before the divmod."
- "Reservoir: the i-th item (0-based) replaces a random slot when `randrange(i + 1) < k`, and every item ends up chosen with probability k / n."

## Exercises

| File | Drills |
|---|---|
| `01_gcd_lcm_euclid.py` | Euclid's step `(a, b) -> (b, a % b)` traced pair by pair; lcm via the gcd; gcd(0, n) = n |
| `02_primes_sieve_and_primality.py` | trial division up to sqrt(n); the sieve drawn after each prime's multiples are crossed off |
| `03_fast_power_and_modular_arithmetic.py` | binary exponentiation with the bit, base and result per round; the modular version; Python's floor rules in the tests |
| `04_digits_reverse_integer_and_palindrome_number.py` | LeetCode 7 and 9: digit extraction, sign handling, the 32-bit range check, palindrome by reversing half |
| `05_base_conversion_and_excel_columns.py` | LeetCode 168 and 171: to and from base b, and the subtract-1 trick for 1-based digits |
| `06_random_pick_and_reservoir_sampling.py` | reservoir sampling of k items and Random Pick Index (k = 1), with a seeded frequency test |
