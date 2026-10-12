"""
GCD and LCM - Euclid's Algorithm

The greatest common divisor of two integers is the largest number dividing
both; the least common multiple is the smallest positive number both divide:
gcd(48, 18) -> 6, lcm(48, 18) -> 144.
"""


# --- algorithm ---
def gcd(a, b):
    """Euclid: (a, b) becomes (b, a mod b) until b is 0. O(log min(a, b))."""
    a = abs(a)
    b = abs(b)
    while b != 0:
        remainder = a % b               # every common divisor survives the mod
        a = b
        b = remainder
    return a                            # gcd(a, 0) = a


def lcm(a, b):
    """Divide by the gcd before multiplying. O(log min(a, b))."""
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)  # exact division first


def gcd_list(nums):
    """Fold gcd over the list from 0, since gcd(0, x) = x. O(n log max)."""
    result = 0
    for x in nums:
        result = gcd(result, x)
        if result == 1:
            break                       # it can never go below 1
    return result


# --- try it ---
print(gcd(48, 18))                      # -> 6
print(lcm(48, 18))                      # -> 144
print(gcd(7, 0))                        # -> 7
print(gcd_list([12, 18, 30]))           # -> 6
