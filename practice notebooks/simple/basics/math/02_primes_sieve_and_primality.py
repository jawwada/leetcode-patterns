"""
Primes: Trial Division and the Sieve of Eratosthenes (basics: math)
Test whether one number is prime, and list every prime up to n.
  is_prime(91)  ->  False (7 * 13);  sieve(30)  ->  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

Idea: is_prime: divisors come in pairs d * (n / d), one of them <= sqrt(n), so stop at d * d > n.
      sieve: each prime p crosses off its multiples starting at p * p
      (the smaller multiples were already crossed off by a smaller prime).

Pseudocode:
  is_prime(n):
      if n < 2: return False
      for d = 2, 3, 4, ... while d * d <= n:
          if n % d == 0: return False
      return True
  sieve(n):
      is_p[0..n] = all True, except is_p[0] = is_p[1] = False
      for p = 2 .. sqrt(n):
          if is_p[p]: cross off p*p, p*p + p, p*p + 2p, ... up to n
      return every i with is_p[i] still True

Time is_prime O(sqrt n); sieve O(n log log n) time, O(n) space.
"""
from math import isqrt


def is_prime(n):
    if n < 2:                            # 0, 1 and negatives are not prime
        return False
    d = 2
    while d * d <= n:                    # only divisors up to sqrt(n)
        if n % d == 0:
            return False
        d += 1
    return True


def sieve(n):
    is_p = [False, False] + [True] * (n - 1)  # index i: is i still prime?
    for p in range(2, isqrt(n) + 1):     # p up to sqrt(n)
        if is_p[p]:                      # p survived, so it is prime
            for m in range(p * p, n + 1, p):
                is_p[m] = False          # cross off multiples of p
    return [i for i in range(n + 1) if is_p[i]]


if __name__ == "__main__":
    print(is_prime(91), is_prime(97))    # False True
    print(sieve(30))                     # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    print(sieve(1))                      # []
