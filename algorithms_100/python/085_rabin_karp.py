"""
Rabin-Karp - Rolling Hash Pattern Matching

Return every index where the pattern starts in the text, comparing window
hashes first and confirming each hash hit character by character:
text "abracadabra", pattern "abra" -> [0, 7].
"""


# --- algorithm ---
BASE = 256                              # one digit per character code
MOD = 1000000007                        # a large prime keeps collisions rare


def poly_hash(s):
    """s read as a number in base BASE, kept mod MOD. O(len(s))."""
    value = 0
    for ch in s:
        value = (value * BASE + ord(ch)) % MOD  # shift left, add a digit
    return value


def rabin_karp(text, pattern):
    """Roll one window hash across the text; compare characters only on a
    hash hit. Expected O(n + m) time when matches are few."""
    n = len(text)
    m = len(pattern)
    if m == 0 or m > n:
        return []
    high = pow(BASE, m - 1, MOD)        # leading digit weight: BASE^(m-1) % MOD
    pattern_hash = poly_hash(pattern)
    window_hash = poly_hash(text[0:m])
    matches = []
    for start in range(n - m + 1):
        if window_hash == pattern_hash and text[start:start + m] == pattern:
            matches.append(start)       # a hash hit, confirmed
        if start + m < n:               # roll the window one step right
            window_hash = (window_hash - ord(text[start]) * high) % MOD
            window_hash = (window_hash * BASE + ord(text[start + m])) % MOD
    return matches


# --- try it ---
print(rabin_karp("abracadabra", "abra"))                # -> [0, 7]
print(rabin_karp("aaaaa", "aa"))                        # -> [0, 1, 2, 3]
print(poly_hash("neonatus") == poly_hash("plumular"))   # -> True
print(rabin_karp("neonatus", "plumular"))               # -> []
print(rabin_karp("abc", "abcd"))                        # -> []
