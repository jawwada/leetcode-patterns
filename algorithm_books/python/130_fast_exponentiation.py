"""
Fast Exponentiation - Square and Multiply

Compute x to the power n with O(log n) multiplications, for a negative n as
well, and the same power modulo m: 3^13 -> 1594323, 2^-2 -> 0.25.
"""


# --- algorithm ---
def power(x, n):
    """Square x once per bit of n; multiply it in where the bit is 1.
    O(log |n|) multiplications."""
    if n < 0:
        x = 1 / x                       # x^-n = (1 / x)^n
        n = -n
    result = 1
    while n > 0:
        if n % 2 == 1:                  # lowest bit is 1: this square counts
            result = result * x
        x = x * x                       # x, x^2, x^4, x^8, ...
        n = n // 2                      # drop the lowest bit
    return result


def mod_power(x, n, m):
    """The same loop with every product reduced mod m. O(log n)."""
    result = 1 % m                      # 0 when m is 1
    x = x % m
    while n > 0:
        if n % 2 == 1:
            result = result * x % m
        x = x * x % m                   # numbers stay below m * m
        n = n // 2
    return result


# --- try it ---
print(power(3, 13))                     # -> 1594323
print(power(2, -2))                     # -> 0.25
print(power(7, 0))                      # -> 1
print(mod_power(3, 13, 1000))           # -> 323
print(mod_power(2, 100, 1000000007))    # -> 976371285
