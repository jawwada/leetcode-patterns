"""
Encode and Decode Strings (LeetCode 271) - Basics
Area: strings
Key operations: length-prefix each string, collect parts in a list and join once, read length then slice

Encode a list of strings into one string and decode it back; the strings may contain any character,
including the delimiter. Each part is written as "<length>#<string>", so the decoder reads a number,
skips the '#', and slices exactly that many characters. Building the output with a list and one
join copies every character once; appending with += in a loop copies the whole accumulator again on
every step (quadratic). The trace counts both.
Example: ["lint", "code", "love", "you"] -> "4#lint4#code4#love3#you" -> ["lint", "code", "love", "you"]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(strs: List[str]) -> str:
    """Same encoding built with += in a loop: step k copies everything built so far. O(total^2) characters copied in the worst case."""
    out = ""
    for s in strs:
        out += f"{len(s)}#{s}"
    return out


# --- optimal ---
def solve(strs: List[str]) -> str:
    """Length-prefix each string, append the parts to a list, join once. O(total length)."""
    parts = []
    joined, plus = 0, 0  # characters copied by one join vs by += in a loop
    for s in strs:
        parts.append(f"{len(s)}#{s}")
        joined += len(parts[-1])
        plus += joined  # += copies the whole accumulator again
        log(f"append {parts[-1]!r}: join cost so far {joined}, += cost so far {plus}")
    log(f"join copies {joined} chars once; += in a loop would copy {plus}")
    return "".join(parts)


def decode(s: str) -> List[str]:
    """Read the length up to '#', slice that many characters, jump past them. O(n)."""
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)
        length = int(s[i:j])
        out.append(s[j + 1:j + 1 + length])
        log(f"i={i}: length {length} -> {out[-1]!r}; next i={j + 1 + length}")
        i = j + 1 + length
    return out


# --- demo ---
def demo():
    encoded = solve(["lint", "code", "love", "you"])
    return encoded, decode(encoded)


# --- tests ---
def tests():
    assert solve(["lint", "code", "love", "you"]) == "4#lint4#code4#love3#you"
    assert decode("4#lint4#code4#love3#you") == ["lint", "code", "love", "you"]
    assert solve([]) == ""
    assert decode("") == []
    assert decode(solve([""])) == [""]
    assert decode(solve(["", ""])) == ["", ""]
    assert decode(solve(["1#", "#", "12#34"])) == ["1#", "#", "12#34"]  # delimiter and digits inside
    import random
    rng = random.Random(0)
    for _ in range(200):
        strs = ["".join(rng.choice("a#1 ") for _ in range(rng.randint(0, 4))) for _ in range(rng.randint(0, 5))]
        assert solve(strs) == brute_force(strs), strs
        assert decode(solve(strs)) == strs, strs


# --- bugs ---
BUGS = [
    {
        "replace": "        i = j + 1 + length",
        "with":    "        i = j + length",
        "fix": "the next part starts after the '#' and the payload: j + 1 + length",
        "why": "Off by one: the next read starts on the last payload character, so '4#lint...' tries int('t4') and raises ValueError.",
        "decoys": [
            {"line": "        j = s.index(\"#\", i)", "change": "should be s.index(\"#\")"},
            {"line": "        length = int(s[i:j])", "change": "should be int(s[i:j + 1])"},
            {"line": "    while i < len(s):", "change": "should be i <= len(s)"},
        ],
    },
    {
        "replace": "        out.append(s[j + 1:j + 1 + length])",
        "with":    "        out.append(s[j + 1:j + length])",
        "fix": "the payload runs from j + 1 for exactly length characters: s[j + 1:j + 1 + length]",
        "why": "Every decoded string loses its last character: 'lint' comes back as 'lin'.",
        "decoys": [
            {"line": "        parts.append(f\"{len(s)}#{s}\")", "change": "should be f\"{s}#{len(s)}\""},
            {"line": "        plus += joined  # += copies the whole accumulator again", "change": "should be plus += len(parts[-1])"},
            {"line": "    return \"\".join(parts)", "change": "should be \"#\".join(parts)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
