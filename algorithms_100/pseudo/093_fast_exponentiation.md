---
rank: 93
slug: fast_exponentiation
---

Compute `x` raised to the power `n`, where `n` may be negative, and compute `x^n mod m` for a huge `n` without ever building the full number. For example `3^13 = 1594323`, `2^-2 = 0.25`, and `3^13 mod 1000 = 323`.

Multiplying `x` into the result `n` times costs `O(n)` multiplications, hopeless when `n` is in the billions. Squaring is the shortcut: `x · x = x^2`, `x^2 · x^2 = x^4`, and `k` squarings climb to `x^(2^k)`. Every exponent is a sum of powers of two, which are its binary digits, so `x^n` is the product of the rungs of that ladder where `n` has a 1 bit: `13 = 8 + 4 + 1` gives `3^13 = 3^8 · 3^4 · 3^1`. The loop reads the bits of `n` from the lowest. While `x` climbs `x, x^2, x^4, x^8, …`, the test `n mod 2 = 1` asks whether the current rung belongs in the product, and halving `n` throws away the bit just read.

A negative exponent flips the base once at the start, since `x^-n = (1 / x)^n`, and from then on the loop sees only a non-negative `n`. The modular version is the same loop with `mod m` after every product. That is legal because remainders multiply like the numbers they came from, `(a · b) mod m = ((a mod m) · (b mod m)) mod m`, and it keeps every intermediate value below `m²`: `3^1000000 mod 1000000007` takes 20 squarings of small numbers instead of building a number with 477,122 digits.

```text
13 = 8 + 4 + 1 = 1101 in binary, so 3^13 = 3^1 · 3^4 · 3^8
  n   n mod 2   result after the step     x after squaring
 13      1      1 · 3 = 3                 3^2  = 9
  6      0      3          (bit 0: skip)  3^4  = 81
  3      1      3 · 81 = 243              3^8  = 6561
  1      1      243 · 6561 = 1594323      3^16 = 43046721
  0             stop: 4 squarings and 3 multiplies instead of 12 multiplies

mod 1000, the same walk on remainders:
  result 3 → 3 → 243 → 243 · 561 mod 1000 = 323     x 9 → 81 → 561 → 721
```

```pseudo
FUNCTION Power(x, n)
    IF n < 0
        x ← 1 / x                       // x^-n = (1 / x)^n
        n ← -n
    result ← 1
    WHILE n > 0
        IF n mod 2 = 1                  // lowest bit is 1: this square counts
            result ← result * x
        x ← x * x                       // x, x^2, x^4, x^8, …
        n ← floor(n / 2)                // drop the lowest bit
    RETURN result

FUNCTION ModPower(x, n, m)
    result ← 1 mod m                    // 0 when m is 1
    x ← x mod m
    WHILE n > 0
        IF n mod 2 = 1
            result ← (result * x) mod m
        x ← (x * x) mod m               // numbers stay below m * m
        n ← floor(n / 2)
    RETURN result
```

The loop runs once per bit of `n`, one squaring each time plus one multiply per 1 bit, so it costs `O(log n)` multiplications and `O(1)` space. Reach for it when an exponent is huge, when an answer is requested modulo `10^9 + 7`, or when independent choices multiply: Count Good Numbers is `5^ceil(n / 2) · 4^floor(n / 2)`, and Super Pow feeds in an exponent given as a digit array through `a^(10k + d) = (a^k)^10 · a^d`. Replacing the product of numbers by a product of matrices gives matrix powers, the source of fast Fibonacci (#67). The classic mistake is negating `n` in a language with 32-bit integers, where `-(-2^31)` overflows back to `-2^31`; widen to 64 bits before negating. Its modular twin is reducing only the result and not the squared base, which lets `x` grow without bound.

*Practice:* LC 50 Pow(x, n) · LC 372 Super Pow · LC 1922 Count Good Numbers
