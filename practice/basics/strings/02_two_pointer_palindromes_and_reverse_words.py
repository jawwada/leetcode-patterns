"""
Two Pointer Palindromes and Reverse Words - Basics
Area: strings
Key operations: lo/hi pointers that skip non-alphanumerics, compare lowercase, reverse a range in place, reverse each word back

Two drills on a char list with two pointers. (1) is_palindrome: ignore everything that is not a
letter or digit and compare case-insensitively. (2) reverse the order of the words in a sentence
of single-space separated words in place: reverse the whole list, then reverse every word back.
Example: "A man, a plan, a canal: Panama" -> True; "the sky is blue" -> "blue is sky the"
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_is_palindrome(s: str) -> bool:
    """Build the cleaned string and compare with its slice reversal. O(n) time but O(n) extra space."""
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]


def brute_force(s: str) -> str:
    """Split into words, reverse the list with a slice, join. O(n) time, O(n) extra space; not in place."""
    return " ".join(s.split(" ")[::-1])


# --- optimal ---
def reverse_range(chars: List[str], lo: int, hi: int) -> None:
    """Swap inward until the pointers cross. O(hi - lo)."""
    while lo < hi:
        chars[lo], chars[hi] = chars[hi], chars[lo]
        log(f"      swap {lo}<->{hi}: {''.join(chars)!r}")
        lo += 1
        hi -= 1


def is_palindrome(s: str) -> bool:
    """Two pointers from both ends; skip non-alphanumerics; compare lowercase. O(n), O(1) space."""
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if not s[lo].isalnum():
            log(f"skip s[{lo}]={s[lo]!r}")
            lo += 1
        elif not s[hi].isalnum():
            log(f"skip s[{hi}]={s[hi]!r}")
            hi -= 1
        else:
            log(f"compare s[{lo}]={s[lo]!r} with s[{hi}]={s[hi]!r}")
            if s[lo].lower() != s[hi].lower():
                return False
            lo += 1
            hi -= 1
    return True


def solve(s: str) -> str:
    """Reverse the whole list, then reverse each word back into reading order. O(n), O(1) extra space."""
    chars = list(s)
    reverse_range(chars, 0, len(chars) - 1)
    log(f"whole list reversed: {''.join(chars)!r}")
    start = 0
    for i in range(len(chars) + 1):
        if i == len(chars) or chars[i] == " ":
            reverse_range(chars, start, i - 1)
            log(f"word [{start}..{i - 1}] reversed back: {''.join(chars)!r}")
            start = i + 1
    return "".join(chars)


# --- demo ---
def demo():
    return solve("the sky is blue")


# --- tests ---
def tests():
    assert solve("the sky is blue") == "blue is sky the"
    assert solve("hello") == "hello"
    assert solve("") == ""
    assert solve("a b") == "b a"
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    assert is_palindrome("") is True
    assert is_palindrome(".,") is True  # nothing alphanumeric
    assert is_palindrome("0P") is False
    import random
    rng = random.Random(0)
    for _ in range(200):
        s = "".join(rng.choice("aAb, 1") for _ in range(rng.randint(0, 8)))
        assert is_palindrome(s) == brute_is_palindrome(s), s
        words = ["".join(rng.choice("xyz") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(1, 4))]
        sentence = " ".join(words)
        assert solve(sentence) == brute_force(sentence), sentence


# --- bugs ---
BUGS = [
    {
        "replace": "            reverse_range(chars, start, i - 1)",
        "with":    "            reverse_range(chars, start, i)",
        "fix": "the word ends just before the space at i, so its last index is i - 1",
        "why": "The space is swapped into the word, and for the last word i == len(chars) is out of range: 'the sky is blue' raises IndexError.",
        "decoys": [
            {"line": "    for i in range(len(chars) + 1):", "change": "should be range(len(chars))"},
            {"line": "            start = i + 1", "change": "should be start = i"},
            {"line": "    reverse_range(chars, 0, len(chars) - 1)", "change": "should be reverse_range(chars, 0, len(chars))"},
        ],
    },
    {
        "replace": "            if s[lo].lower() != s[hi].lower():",
        "with":    "            if s[lo] != s[hi]:",
        "fix": "compare case-insensitively: lower() both characters",
        "why": "'A' and 'a' are treated as different, so 'A man, a plan, a canal: Panama' is rejected at its first comparison.",
        "decoys": [
            {"line": "    lo, hi = 0, len(s) - 1", "change": "should be hi = len(s)"},
            {"line": "        if not s[lo].isalnum():", "change": "should be isalpha()"},
            {"line": "                return False", "change": "should return True"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
