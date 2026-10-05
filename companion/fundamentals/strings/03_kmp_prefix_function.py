"""
KMP Prefix Function - Fundamentals
Chapter: fundamentals/strings
Key operations: build the failure table, fall back with fail[k - 1] on a mismatch, extend on match

fail[i] is the length of the longest proper prefix of pattern[:i + 1] that is also its suffix. When
text[i] does not match pattern[j], the first j characters already match, so instead of restarting
at i - j + 1 the pattern slides to its longest border: j = fail[j - 1]. Return every start index.
Example: text "aabaaabaab", pattern "aab" -> [0, 4, 7]   (failure table of "aab": [0, 1, 0])
"""


# --- algorithm ---
def build_failure(pattern):
    """fail[i] = length of the longest proper prefix of pattern[:i + 1] that is also a suffix."""
    fail = [0] * len(pattern)
    k = 0                                     # length of the border being extended
    for i in range(1, len(pattern)):          # start at 1: fail[0] is always 0 (PROPER prefix)
        while k > 0 and pattern[i] != pattern[k]:
            k = fail[k - 1]                   # fall back to the next shorter border
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    return fail


def kmp_search(text, pattern):
    """One pass over text; j = matched prefix length, i never moves backwards. O(n + m)."""
    fail = build_failure(pattern)
    hits = []
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = fail[j - 1]                   # while, not if: a fall-back may hit another mismatch
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            hits.append(i - j + 1)
            j = fail[-1]                      # keep the longest border: overlapping hits are found
    return hits


# --- try it ---
print(build_failure("aab"))                  # -> [0, 1, 0]
print(build_failure("abcabd"))               # -> [0, 0, 0, 1, 2, 0]
print(kmp_search("aabaaabaab", "aab"))       # -> [0, 4, 7]
print(kmp_search("aaaa", "aa"))              # -> [0, 1, 2]
print(kmp_search("abc", "d"))                # -> []
