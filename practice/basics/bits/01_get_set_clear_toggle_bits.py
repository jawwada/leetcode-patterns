"""
Get, Set, Clear and Toggle a Bit - Basics
Area: bits
Key operations: mask = 1 << i, n | mask sets, n & ~mask clears, n ^ mask toggles, n >> i & 1 reads

Every single-bit operation starts from the mask 1 << i: a lone 1 in position i, counting from the
right, 0-based. OR with the mask forces the bit to 1, AND with the complement forces it to 0, XOR
flips it, and shifting the bit down to position 0 then AND 1 reads it. Writing a given value v into
bit i is clear-then-OR.
Example: n = 00101010; set bit 0 -> 00101011; clear bit 3 -> 00100011; toggle bit 7 -> 10100011; get bit 7 -> 1
"""


# --- brute force ---
def brute_force(n: int, i: int, op: str, v: int = 0) -> int:
    """Edit character i (from the right) of the binary string and parse it back. O(bits) and allocates strings."""
    bits = list(format(n, "b").rjust(max(n.bit_length(), i + 1), "0"))
    pos = len(bits) - 1 - i
    if op == "get":
        return int(bits[pos])
    if op == "set":
        bits[pos] = "1"
    elif op == "clear":
        bits[pos] = "0"
    elif op == "toggle":
        bits[pos] = "0" if bits[pos] == "1" else "1"
    else:
        bits[pos] = str(v)
    return int("".join(bits), 2)


# --- optimal ---
def get_bit(n: int, i: int) -> int:
    """Shift bit i down to position 0 and keep only that bit. O(1)."""
    return n >> i & 1


def set_bit(n: int, i: int) -> int:
    """OR with the mask: bit i becomes 1, the other bits are unchanged. O(1)."""
    return n | (1 << i)


def clear_bit(n: int, i: int) -> int:
    """AND with the complement of the mask: bit i becomes 0, the other bits are unchanged. O(1)."""
    return n & ~(1 << i)


def toggle_bit(n: int, i: int) -> int:
    """XOR with the mask: bit i flips, the other bits are unchanged. O(1)."""
    return n ^ (1 << i)


def update_bit(n: int, i: int, v: int) -> int:
    """Clear bit i, then OR in v shifted into place. O(1)."""
    return (n & ~(1 << i)) | (v << i)


# --- demo ---
def demo():
    n = 0b00101010
    n = set_bit(n, 0)
    n = clear_bit(n, 3)
    n = toggle_bit(n, 7)
    n = update_bit(n, 5, 0)
    return format(n, "08b"), get_bit(n, 7)


# --- bugs ---
BUGS = [
    {
        "replace": "    return n & ~(1 << i)",
        "with":    "    return n & (1 << i)",
        "fix": "AND with the COMPLEMENT of the mask: ~(1 << i) is all ones except position i",
        "why": "Without the ~ this keeps only bit i and throws the rest away: clear_bit(0b111, 1) returns 0b010 instead of 0b101.",
        "decoys": [
            {"line": "    return n >> i & 1", "change": "should be n >> i & i"},
            {"line": "    return n ^ (1 << i)", "change": "should be n ^ i"},
            {"line": "    return (n & ~(1 << i)) | (v << i)", "change": "should be (n & (1 << i)) | v"},
        ],
    },
    {
        "replace": "    return n >> i & 1",
        "with":    "    return n & 1 << i",
        "fix": "shift the bit down to position 0 before the & 1, so the answer is 0 or 1",
        "why": "n & (1 << i) isolates the bit in place and returns 0 or 2^i: get_bit(0b1000, 3) returns 8 instead of 1.",
        "decoys": [
            {"line": "    return n | (1 << i)", "change": "should be n | i"},
            {"line": "    return n & ~(1 << i)", "change": "should be n & ~i"},
            {"line": "    return format(n, \"08b\"), get_bit(n, 7)", "change": "should be format(n, \"8b\")"},
        ],
    },
    {
        "replace": "    return (n & ~(1 << i)) | (v << i)",
        "with":    "    return n | (v << i)",
        "fix": "clear the bit first, then OR the new value in; OR alone can never turn a 1 into a 0",
        "why": "Writing v = 0 into a set bit leaves it set: update_bit(0b111, 1, 0) returns 0b111 instead of 0b101.",
        "decoys": [
            {"line": "    return n ^ (1 << i)", "change": "should be n ^ ~(1 << i)"},
            {"line": "    return n | (1 << i)", "change": "should be n | (1 >> i)"},
            {"line": "    n = 0b00101010", "change": "should be 0b00101011"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
