"""
Primes: Trial Division and the Sieve of Eratosthenes - Fundamentals
Chapter: fundamentals/math
Key operations: trial divide while d * d <= n, cross off multiples of p from p * p, keep survivors

is_prime(n): n >= 2 and no d in 2..sqrt(n) divides n (a factor above sqrt(n) pairs with one below).
sieve(n): mark every number 2..n as prime, then for each surviving p with p * p <= n cross off
p*p, p*p + p, p*p + 2p, ... (smaller multiples were already crossed off by a smaller prime).
Example: is_prime(91) -> False (91 = 7 * 13); sieve(30) -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
"""


# --- algorithm ---
def is_prime(n):
    """Trial division by d = 2, 3, 4, ... while d * d <= n. O(sqrt n)."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:             # <= not <: for a perfect square the only small factor is sqrt(n)
        if n % d == 0:
            return False
        d += 1
    return True


def sieve(n):
    """Eratosthenes: each surviving p with p * p <= n crosses off p*p, p*p+p, ... O(n loglog n)."""
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = False
    is_p[1] = False
    p = 2
    while p * p <= n:
        if is_p[p]:
            multiple = p * p      # start at p * p: smaller multiples have a smaller prime factor
            while multiple <= n:
                is_p[multiple] = False
                multiple += p
        p += 1
    primes = []
    for i in range(2, n + 1):
        if is_p[i]:
            primes.append(i)
    return primes


# --- try it ---
print(is_prime(91))      # -> False
print(is_prime(97))      # -> True
print(is_prime(4))       # -> False
print(sieve(30))         # -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print(sieve(10))         # -> [2, 3, 5, 7]
