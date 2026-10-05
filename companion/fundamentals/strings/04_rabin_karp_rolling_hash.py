"""
Rabin-Karp Rolling Hash - Fundamentals
Chapter: fundamentals/strings
Key operations: polynomial hash of a window, roll it by dropping the left char, adding the right

Hash the pattern and the first window of the text with a base-BASE polynomial modulo MOD. Sliding
the window one step costs O(1): subtract the leftmost character times BASE^(m-1), multiply by BASE,
add the new character. Equal hashes may be collisions, so a hit is confirmed by a direct compare.
Example: text "abracadabra", pattern "abra" -> [0, 7]
"""


# --- algorithm ---
BASE = 256
MOD = 101                             # tiny on purpose: collisions happen, verify catches them


def poly_hash(s):
    """Hash of a whole string: h = (h * BASE + ord(ch)) % MOD over its characters. O(len)."""
    h = 0
    for ch in s:
        h = (h * BASE + ord(ch)) % MOD
    return h


def rabin_karp(text, pattern):
    """Roll one hash across the text; compare characters only when the hashes agree. O(n + m)."""
    n = len(text)
    m = len(pattern)
    if m > n:
        return []
    high = pow(BASE, m - 1, MOD)          # weight of the window's leftmost character
    target = poly_hash(pattern)
    h = poly_hash(text[:m])
    hits = []
    for i in range(n - m + 1):
        if h == target and text[i:i + m] == pattern:    # a hash hit is a candidate, not a proof
            hits.append(i)
        if i + m < n:
            h = (h - ord(text[i]) * high) * BASE + ord(text[i + m])   # drop left char, add right
            h = h % MOD
    return hits


# --- try it ---
print(rabin_karp("abracadabra", "abra"))     # -> [0, 7]
print(rabin_karp("aaaa", "aa"))              # -> [0, 1, 2]
print(rabin_karp("abccabra", "abra"))        # -> [4]
print(rabin_karp("abc", "abcd"))             # -> []
