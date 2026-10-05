"""
Fast Power and Modular Arithmetic - Fundamentals
Chapter: fundamentals/math
Key operations: exp & 1 reads the current bit, base = base * base, exp >>= 1, reduce products mod m

Compute base^exp by walking the bits of exp from the lowest: when the bit is 1 multiply the current
base into the result; then square the base and shift exp right. Reducing every product mod m gives
modular exponentiation with numbers that never exceed m^2 (Python's % is never negative for m > 0).
Example: 3^13 with 13 = 1101b -> bits 1, 0, 1, 1 -> 3 * 81 * 6561 = 1594323; 3^13 mod 1000 -> 323
"""


# --- algorithm ---
def power(base, exp):
    """Binary exponentiation: square the base once per bit, multiply it in when the bit is 1."""
    result = 1                    # the empty product; starting at base gives one factor too many
    while exp > 0:
        if exp & 1 == 1:          # lowest bit set: this power of base belongs in the answer
            result = result * base
        base = base * base
        exp = exp >> 1
    return result


def mod_power(base, exp, mod):
    """The same loop with every product reduced mod m, so numbers never grow past m^2. O(log)."""
    result = 1
    base = base % mod
    while exp > 0:                # run while exp is nonzero: the top bit is handled when exp == 1
        if exp & 1 == 1:
            result = result * base % mod
        base = base * base % mod
        exp = exp >> 1
    return result % mod


# --- try it ---
print(power(3, 13))              # -> 1594323
print(mod_power(3, 13, 1000))    # -> 323
print(power(2, 0))               # -> 1
print(mod_power(2, 10, 7))       # -> 2
print(mod_power(-7, 1, 3))       # -> 2
