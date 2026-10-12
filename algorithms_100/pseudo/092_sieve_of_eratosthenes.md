---
rank: 92
slug: sieve_of_eratosthenes
---

List every prime below `n`, and decide whether a single number is prime. For `n = 30` the primes are `2, 3, 5, 7, 11, 13, 17, 19, 23, 29`, and `91` is not prime because `91 = 7 × 13`.

Testing each number on its own with trial division costs `O(√k)` for the number `k`, so `O(n√n)` for the whole range. The sieve turns the question around: instead of every number searching for a divisor, every prime announces its multiples. Lay out the numbers `2` to `n - 1` and walk upward. The first number that is not yet crossed out has no smaller prime factor, so it is prime, and it crosses out its multiples. Whatever survives the walk is prime.

Two bounds make the walk short. A prime `p` starts crossing at `p²`, not at `2p`: every multiple `k · p` with `2 ≤ k < p` has the smaller factor `k`, so a smaller prime has already crossed it out, which is why `5` finds `10`, `15` and `20` gone and starts at `25`. And the outer loop stops once `p² ≥ n`, because a composite below `n` always has a prime factor of at most `√n`; by then every composite is crossed out and the survivors need no more work. Trial division for a single number rests on the same square root: divisors come in pairs `d` and `n / d`, and one of the two is at most `√n`, so testing `d` while `d · d ≤ n` is enough.

```text
n = 30: p runs 2, 3, 4, 5 and the loop stops at p = 6, since 6 × 6 ≥ 30
p = 2  crosses 4 6 8 10 12 14 16 18 20 22 24 26 28
p = 3  crosses 9 (12) 15 (18) 21 (24) 27       (12) = crossed again
p = 4  skipped: already crossed, its multiples are multiples of 2
p = 5  crosses 25                  10, 15, 20 fell to 2 and 3 earlier

       +0  +1  +2  +3  +4  +5  +6  +7  +8  +9     ×p = first crossed by p
   0    ·   ·   2   3  ×2   5  ×2   7  ×2  ×3      · = 0 and 1, never prime
  10   ×2  11  ×2  13  ×2  ×3  ×2  17  ×2  19
  20   ×2  ×3  ×2  23  ×2  ×5  ×2  ×3  ×2  29
survivors: 2 3 5 7 11 13 17 19 23 29, the ten primes below 30
```

```pseudo
FUNCTION Sieve(n)
    crossed ← array of n copies of false  // true once a smaller prime divides i
    p ← 2
    WHILE p * p < n
        IF NOT crossed[p]                 // p is prime: nothing crossed it out
            multiple ← p * p              // below p * p: already crossed
            WHILE multiple < n
                crossed[multiple] ← true
                multiple ← multiple + p
        p ← p + 1
    primes ← empty list
    FOR i FROM 2 TO n - 1
        IF NOT crossed[i]
            primes.append(i)
    RETURN primes

FUNCTION IsPrime(n)
    IF n < 2
        RETURN false
    d ← 2
    WHILE d * d ≤ n                       // d and n / d: one is at most √n
        IF n mod d = 0
            RETURN false
        d ← d + 1
    RETURN true
```

The sieve runs in `O(n log log n)` time, because the prime `p` crosses out at most `n / p` numbers and the sum of `1 / p` over the primes grows only like `log log n`; the array costs `O(n)` space. Trial division is `O(√n)` for one number. Reach for the sieve when a problem asks about many numbers in a range, such as counting the primes below `n` or finding the closest pair of primes in `[left, right]`, and store the smallest prime factor instead of a boolean when every value in an array must be factored. Reach for trial division when the question is about one number. The classic mistake is `d · d < n` in trial division, which declares `49` prime because its only small factor is exactly `√49 = 7`; the sieve's version of the slip is counting up to `n` inclusive when Count Primes asks for the primes strictly below `n`.

*Practice:* LC 204 Count Primes · LC 2523 Closest Prime Numbers in Range · LC 952 Largest Component Size by Common Factor
