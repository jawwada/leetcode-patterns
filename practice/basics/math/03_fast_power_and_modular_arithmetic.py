"""
Fast Power and Modular Arithmetic - Basics
Area: math
Key operations: exp & 1 reads the current bit, base = base * base, exp >>= 1, reduce every product mod m

Compute base^exp by walking the bits of exp from the lowest: when the bit is 1 multiply the current
base into the result; then square the base and shift exp right. Reducing every product mod m gives
modular exponentiation with numbers that never exceed m^2. Python's // and % round toward negative
infinity, so -7 // 3 == -3 and -7 % 3 == 2; the tests spell the rules out.
Example: 3^13 with 13 = 1101b -> bits 1, 0, 1, 1 -> result 3 * 81 * 6561 = 1594323; 3^13 mod 1000 -> 323
"""


# --- brute force ---
def brute_force(base: int, exp: int, mod: int = 0) -> int:
    """Multiply base into the result exp times (reducing mod m when given). O(exp) multiplications instead of O(log exp)."""
    result = 1
    for _ in range(exp):
        result = result * base % mod if mod else result * base
    return result % mod if mod else result


# --- optimal ---
def power(base: int, exp: int) -> int:
    """Binary exponentiation: square the base once per bit, multiply it in when the bit is 1. O(log exp)."""
    result = 1
    while exp > 0:
        bit = exp & 1
        if bit:
            result *= base
        base *= base
        exp >>= 1
    return result


def mod_power(base: int, exp: int, mod: int) -> int:
    """The same loop with every product reduced mod m, so numbers never grow past m^2. O(log exp)."""
    result, base = 1, base % mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result % mod


# --- demo ---
def demo():
    return power(3, 13), mod_power(3, 13, 1000)


# --- bugs ---
BUGS = [
    {
        "replace": "    result = 1",
        "with":    "    result = base",
        "fix": "the accumulator starts at 1 (the empty product); the loop multiplies the base in when bit 0 is set",
        "why": "Starting at base multiplies one extra factor in: power(3, 13) returns 3^14 and power(2, 0) returns 2 instead of 1.",
        "decoys": [
            {"line": "        base *= base", "change": "should be base *= 2"},
            {"line": "        bit = exp & 1", "change": "should be exp % 2 == 0"},
            {"line": "        if bit:", "change": "should be if bit == exp"},
        ],
    },
    {
        "replace": "    while exp:",
        "with":    "    while exp > 1:",
        "fix": "loop while exp is nonzero; the highest bit is processed when exp == 1",
        "why": "The last round is skipped, so the highest power of the base is never multiplied in: mod_power(3, 1, 10) returns 1 and 3^13 loses the 3^8 factor.",
        "decoys": [
            {"line": "        base = base * base % mod", "change": "the % mod is unnecessary here"},
            {"line": "    return result % mod", "change": "should return result"},
            {"line": "    result, base = 1, base % mod", "change": "should not reduce base first"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
