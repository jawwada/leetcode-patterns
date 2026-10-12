"""
KMP String Matching - The Prefix Function Never Re-Reads the Text

Return every index where the pattern starts in the text, overlapping matches
included: text "abababc", pattern "ababc" -> [2].
"""


# --- algorithm ---
def build_lps(pattern):
    """lps[i] = length of the longest proper prefix of pattern[0..i] that is
    also its suffix; the search loop run on the pattern itself. O(m)."""
    lps = [0] * len(pattern)
    j = 0                               # length of the border being extended
    for i in range(1, len(pattern)):    # lps[0] = 0: a proper prefix is shorter
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]              # fall back to the next shorter border
        if pattern[i] == pattern[j]:
            j += 1
        lps[i] = j
    return lps


def kmp_search(text, pattern):
    """i never moves back; a mismatch slides the pattern by lps. O(n + m)."""
    if len(pattern) == 0:
        return []
    lps = build_lps(pattern)
    matches = []
    j = 0                               # pattern characters matched so far
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]              # slide the pattern; text[i] is retried
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)   # the match ends at i
            j = lps[j - 1]              # keep the border: overlaps are found
    return matches


# --- try it ---
print(build_lps("ababc"))               # -> [0, 0, 1, 2, 0]
print(kmp_search("abababc", "ababc"))   # -> [2]
print(build_lps("aabaaab"))             # -> [0, 1, 0, 1, 2, 2, 3]
print(kmp_search("aaaaa", "aa"))        # -> [0, 1, 2, 3]
print(kmp_search("abc", "abd"))         # -> []
