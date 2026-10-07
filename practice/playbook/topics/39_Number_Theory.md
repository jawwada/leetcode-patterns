## Number Theory

Use divisibility, the Euclidean algorithm, sieves, and repeated squaring to avoid enumerating much larger sets of candidates.

<!-- cell -->

### Math recipes

The math recipes count instead of listing too. Four of them cover what medium interviews ask: number theory, digits and bases, random sampling and exact slopes.

Euclid's rule is that every common divisor of `a` and `b` also divides `a % b`, so `gcd(a, b) = gcd(b, a % b)`, and the pair shrinks fast; then `lcm(a, b) = a // gcd(a, b) * b`. Trial division stops at √n, because divisors come in pairs `d · (n / d)` and one of the two is at most √n. The sieve lists the primes up to n by crossing off the multiples of each prime p from `p * p` on; the smaller multiples have a smaller prime factor and are gone already.

Fast power writes the exponent in binary, `3^13 = 3^8 · 3^4 · 3^1`: square the base once per bit and multiply it in when the bit is 1. Reduce after every multiply, because `(a * b) % m == ((a % m) * (b % m)) % m`: reducing early never changes the answer and keeps every number below m², under 2⁶³ for m = 10⁹ + 7, which fixed-width languages need. Python never overflows, but `3 ** 10**6` has 477 122 digits, and multiplying giants is slow.

Python has most of this built in: `math.gcd`, `math.lcm`, `pow(b, e, m)`, `pow(x, -1, m)` for the inverse of x modulo m, `math.isqrt` and `math.comb`. Write each one once by hand so that you can explain it: gcd(252, 105) is 21, ten primes lie below 30, and 3¹³ mod 1000 is 323.

<!-- cell -->

```python
def gcd(a, b):
    while b:
        a, b = b, a % b                        # (252, 105) -> (105, 42) -> (42, 21) -> (21, 0)
    return abs(a)


def lcm(a, b):
    return abs(a) // gcd(a, b) * abs(b) if a and b else 0     # divide first: smaller numbers


def is_prime(n):                               # trial division up to sqrt(n): a pair has one side there
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def primes_upto(n):                            # sieve of Eratosthenes
    alive = [False, False] + [True] * (n - 1)  # alive[i]: is i still possibly prime?
    for p in range(2, math.isqrt(n) + 1):
        if alive[p]:
            for multiple in range(p * p, n + 1, p):   # smaller multiples are crossed off already
                alive[multiple] = False
    return [i for i in range(n + 1) if alive[i]]


def power_mod(base, exp, mod):
    result, base = 1 % mod, base % mod
    while exp:
        if exp & 1:                            # this bit of exp is 1: multiply its power in
            result = result * base % mod       # reduce after EVERY multiply
        base = base * base % mod               # base, base^2, base^4, base^8, ...
        exp >>= 1
    return result


print(gcd(252, 105), lcm(4, 6), is_prime(91), primes_upto(30))   # 21 12 False [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print(power_mod(3, 13, 1000), pow(3, 13, 1000))                  # 323 323
```

<!-- cell -->

**Try it**
- Print `(a, b)` at the top of the `gcd` loop for `gcd(55, 34)`: 8 rounds. Neighbouring Fibonacci numbers are the slowest case for Euclid, and even they finish in O(log) steps.
- Remove the `1 % mod` (start with `result = 1`) and run `power_mod(5, 0, 1)`: 1 instead of 0. Everything is 0 modulo 1, even an empty product.
- Compare `power_mod(3, 10**6, 10**9 + 7)` with `3 ** 10**6 % (10**9 + 7)`: the same answer, but the second first builds a 1.6-million-bit number. The built-in `pow(3, 10**6, 10**9 + 7)` does the fast version for you.

<!-- cell -->

```python
assert gcd(0, 5) == 5 and lcm(0, 5) == 0 and gcd(-12, 18) == 6

assert not is_prime(1) and is_prime(2) and primes_upto(1) == []

assert power_mod(5, 0, 1) == 0 and power_mod(-2, 3, 5) == 2  # with a positive modulus, % lands in [0, mod)
```
