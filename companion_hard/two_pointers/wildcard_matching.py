"""
Wildcard Matching (LeetCode 44) - Hard
Chapter: two_pointers
Pattern: Greedy two pointers with last-star backtrack

Given a string s and a pattern p where '?' matches any one character and '*' matches any
sequence of characters (including none), decide whether p matches all of s.
Example: s = "adceb", p = "*a*b" -> True ("" a "dce" b).   s = "acdcb", p = "a*c?b" -> False.
"""


# --- brute force ---
def brute_force(s, p):
    """Recursion: a star takes zero or one more character, try both. Exponential time."""
    if p == "":
        return s == ""
    if p[0] == "*":
        if brute_force(s, p[1:]):  # star matches nothing
            return True
        if s != "" and brute_force(s[1:], p):  # star swallows one more character
            return True
        return False
    if s == "":
        return False
    if p[0] != s[0] and p[0] != "?":
        return False
    return brute_force(s[1:], p[1:])


# --- optimal ---
def is_match(s, p):
    """Walk both strings; on a mismatch the LAST star eats one more char. O(n m) worst case."""
    i = 0  # position in s
    j = 0  # position in p
    star = -1  # index of the last '*' seen in p
    match = 0  # the index in s where that star started matching
    while i < len(s):
        if j < len(p) and (p[j] == s[i] or p[j] == "?"):
            i += 1
            j += 1
        elif j < len(p) and p[j] == "*":
            star = j
            match = i
            j += 1  # the star matches nothing for now
        elif star != -1:
            # mismatch after a star: that star swallows one more character and we retry
            match += 1
            i = match
            j = star + 1
        else:
            return False
    while j < len(p) and p[j] == "*":  # leftover stars can match the empty string
        j += 1
    return j == len(p)


# --- try the brute force ---
print(brute_force("aa", "*"))          # -> True
print(brute_force("cb", "?a"))         # -> False
print(brute_force("adceb", "*a*b"))    # -> True
print(brute_force("acdcb", "a*c?b"))   # -> False


# --- try the optimal ---
print(is_match("aa", "*"))          # -> True
print(is_match("cb", "?a"))         # -> False
print(is_match("adceb", "*a*b"))    # -> True
print(is_match("acdcb", "a*c?b"))   # -> False
