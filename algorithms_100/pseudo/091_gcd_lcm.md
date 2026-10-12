---
rank: 91
slug: gcd_lcm
---

The greatest common divisor of two integers is the largest number that divides both, and the least common multiple is the smallest positive number that both divide. For `48` and `18` the gcd is `6` and the lcm is `144`.

The brute force tries every candidate from `min(a, b)` down to `1`, which costs `O(min(a, b))` divisions. Euclid's insight is that the remainder keeps every common divisor. Since `a mod b = a - q · b`, any number that divides `a` and `b` also divides `a mod b`, and any number that divides `b` and `a mod b` divides `a` back. So `gcd(a, b) = gcd(b, a mod b)`: the pair shrinks at every step while its common divisors stay exactly the same, and when the second number reaches `0` the first one is the answer, because `gcd(a, 0) = a`.

Picture an `a × b` rectangle. Taking `a mod b` cuts as many `b × b` squares as fit off its long side and leaves a thinner rectangle, and Euclid repeats the cut on the leftover until the squares tile it exactly. The side of that last square is the gcd: the largest square that tiles the original rectangle with no gap. The lcm then follows from `gcd · lcm = a · b`. Dividing before multiplying, `a / gcd · b`, keeps every intermediate value no larger than the answer, which matters in languages where `a · b` overflows. The gcd of a whole list folds the pair version across it, starting from `0` because `gcd(0, x) = x`, and stops early once it reaches `1`.

```text
  a    b    a = q × b + r      cut q squares of side b off the a × b block
 48   18   48 = 2 × 18 + 12    two 18 × 18, leaving 12 × 18
 18   12   18 = 1 × 12 + 6     one 12 × 12, leaving 12 × 6
 12    6   12 = 2 × 6  + 0     two 6 × 6, nothing left
  6    0   b = 0: gcd = 6      lcm = 48 / 6 × 18 = 144

┌─────────────────┬─────────────────┬───────────┐
│                 │                 │           │
│                 │                 │  12 × 12  │
│     18 × 18     │     18 × 18     │           │
│                 │                 ├─────┬─────┤
│                 │                 │ 6×6 │ 6×6 │
└─────────────────┴─────────────────┴─────┴─────┘
```

```pseudo
FUNCTION Gcd(a, b)
    a ← abs(a)
    b ← abs(b)
    WHILE b ≠ 0
        remainder ← a mod b             // every common divisor survives the mod
        a ← b
        b ← remainder
    RETURN a                            // gcd(a, 0) = a

FUNCTION Lcm(a, b)
    IF a = 0 OR b = 0
        RETURN 0
    RETURN (abs(a) / Gcd(a, b)) * abs(b)  // exact division first

FUNCTION GcdList(nums)
    result ← 0
    FOR EACH x IN nums
        result ← Gcd(result, x)
        IF result = 1
            BREAK                       // it can never go below 1
    RETURN result
```

Every two steps at least halve the larger number: if `b ≤ a / 2` the remainder is below `b`, and otherwise it is `a - b < a / 2`. Within two steps the larger number is at most `min(a, b)`, so Euclid runs in `O(log min(a, b))` steps, and the slowest inputs are consecutive Fibonacci numbers (#67), where almost every step cuts off a single square. Reach for the gcd when a problem asks for a common period or block size, for equal groups that must divide every count, or for a canonical key for a fraction: dividing `(dy, dx)` by their gcd is how Max Points on a Line (#97) compares slopes exactly. Strings follow the same logic: two strings are built from a common repeating block exactly when `s + t = t + s`, and then the longest such block has length `gcd(len(s), len(t))`. The classic mistake is overwriting `a` before taking the remainder, `a ← b` then `b ← a mod b`, which computes `b mod b = 0` and returns `b` after a single step.

*Practice:* LC 1979 Find Greatest Common Divisor of Array · LC 1071 Greatest Common Divisor of Strings · LC 914 X of a Kind in a Deck of Cards · LC 2413 Smallest Even Multiple
