"""
Character Counting and Anagrams - Basics
Area: strings
Key operations: 26-slot count array, compare count vectors, group by a count tuple key

Two lowercase words are anagrams when they use the same letters the same number of times. Build a
26-slot count array in one pass instead of sorting; the tuple of counts is a hashable key that puts
every anagram of a word in the same group. Groups and their words are returned sorted.
Example: ["eat", "tea", "tan", "ate", "nat", "bat"] -> [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
def letters(c: List[int]) -> str:
    """Compact view of a count array: [1,0,0,0,1,...] -> 'a1 e1'."""
    return " ".join(f"{chr(ord('a') + i)}{k}" for i, k in enumerate(c) if k)


# --- brute force ---
def brute_is_anagram(s: str, t: str) -> bool:
    """Sort both strings and compare. O(L log L)."""
    return sorted(s) == sorted(t)


def brute_force(words: List[str]) -> List[List[str]]:
    """Key every word by its sorted letters. O(total letters * log L); sorting each word is the waste."""
    groups = {}
    for w in words:
        groups.setdefault("".join(sorted(w)), []).append(w)
    return sorted(sorted(g) for g in groups.values())


# --- optimal ---
def counts(word: str) -> List[int]:
    """26 letter counts in one pass. O(L)."""
    c = [0] * 26
    for ch in word:
        c[ord(ch) - ord("a")] += 1
    return c


def is_anagram(s: str, t: str) -> bool:
    """Equal length and equal count vectors. O(|s| + |t|)."""
    if len(s) != len(t):
        return False
    cs, ct = counts(s), counts(t)
    log(f"counts {s!r}: {letters(cs)} | {t!r}: {letters(ct)} -> equal? {cs == ct}")
    return cs == ct


def solve(words: List[str]) -> List[List[str]]:
    """Group words by the tuple of their counts. O(total letters)."""
    groups = {}
    for w in words:
        key = tuple(counts(w))
        groups.setdefault(key, []).append(w)
        log(f"{w!r} -> key {letters(key)!r}; group now {groups[key]}")
    return sorted(sorted(g) for g in groups.values())


# --- demo ---
def demo():
    return solve(["eat", "tea", "tan", "ate", "nat", "bat"])


# --- tests ---
def tests():
    assert solve(["eat", "tea", "tan", "ate", "nat", "bat"]) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert solve([]) == []
    assert solve([""]) == [[""]]
    assert solve(["a", "a"]) == [["a", "a"]]
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False
    assert is_anagram("aab", "abb") is False  # same letters, different counts
    assert is_anagram("zebra", "braze") is True
    assert is_anagram("", "") is True
    import random
    rng = random.Random(0)
    for _ in range(200):
        words = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 4))) for _ in range(rng.randint(0, 8))]
        assert solve(words) == brute_force(words), words
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 4)))
        t = "".join(rng.choice("ab") for _ in range(rng.randint(0, 4)))
        assert is_anagram(s, t) == brute_is_anagram(s, t), (s, t)


# --- bugs ---
BUGS = [
    {
        "replace": "        c[ord(ch) - ord(\"a\")] += 1",
        "with":    "        c[ord(ch) - ord(\"a\")] = 1",
        "fix": "count the letter (+= 1); a presence flag loses how many times it occurs",
        "why": "'aab' and 'abb' get the same key {a, b}, so they are reported as anagrams and grouped together.",
        "decoys": [
            {"line": "    c = [0] * 26", "change": "should be [0] * 25"},
            {"line": "    if len(s) != len(t):", "change": "should be len(s) < len(t)"},
            {"line": "        key = tuple(counts(w))", "change": "should be key = counts(w)"},
        ],
    },
    {
        "replace": "    return sorted(sorted(g) for g in groups.values())",
        "with":    "    return sorted(groups.values())",
        "fix": "sort the words inside each group too; insertion order is the input order, not a canonical one",
        "why": "The group of 'eat' comes back as ['eat', 'tea', 'ate'] instead of ['ate', 'eat', 'tea'], so the result depends on input order.",
        "decoys": [
            {"line": "        groups.setdefault(key, []).append(w)", "change": "should be groups[key] = [w]"},
            {"line": "    cs, ct = counts(s), counts(t)", "change": "should compare sorted(s) and sorted(t)"},
            {"line": "    return cs == ct", "change": "should be cs is ct"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
