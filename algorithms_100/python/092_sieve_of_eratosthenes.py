"""
Sieve of Eratosthenes - Cross Out Multiples Starting at p squared

List every prime below n, and test a single number for primality:
n = 30 -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]; 91 -> not prime (7 * 13).
"""


# --- algorithm ---
def sieve(n):
    """Primes below n: each surviving p crosses out p*p, p*p + p, ...
    O(n log log n) time, O(n) space."""
    crossed = [False] * n           # True once a smaller prime divides i
    p = 2
    while p * p < n:
        if not crossed[p]:          # p is prime: nothing crossed it out
            multiple = p * p        # below p * p: already crossed
            while multiple < n:
                crossed[multiple] = True
                multiple += p
        p += 1
    primes = []
    for i in range(2, n):
        if not crossed[i]:
            primes.append(i)
    return primes


def is_prime(n):
    """Trial division by 2, 3, 4, ... while d * d <= n. O(sqrt(n))."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:               # d and n / d: one is at most sqrt(n)
        if n % d == 0:
            return False
        d += 1
    return True


# --- try it ---
print(sieve(30))                # -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print(len(sieve(10)))           # -> 4
print(is_prime(91))             # -> False
print(is_prime(97))             # -> True
