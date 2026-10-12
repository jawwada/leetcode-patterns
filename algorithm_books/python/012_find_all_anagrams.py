"""
Find All Anagrams in a String - Fixed-Size Window with Letter Counts

Given lowercase strings s and p, return the start index of every substring of
s that is an anagram of p (the same letters, the same counts):
s "cbaebabacd", p "abc" -> [0, 6].
"""


# --- algorithm ---
def letter_counts(text):
    """The 26 letter counts of a lowercase string. O(len(text))."""
    counts = [0] * 26
    for ch in text:
        slot = ord(ch) - ord('a')   # 'a' -> 0, 'b' -> 1, ..., 'z' -> 25
        counts[slot] += 1
    return counts


def find_anagrams(s, p):
    """Slide a window of len(p) one letter in, one letter out; record a start
    whenever its 26 letter counts equal p's. O(26 n) time, O(26) space."""
    m = len(p)
    starts = []
    if m > len(s):
        return starts               # no window fits
    need = letter_counts(p)
    window = letter_counts(s[0:m])  # the first window, s[0..m-1]
    if window == need:
        starts.append(0)            # the first window counts too
    for right in range(m, len(s)):
        entering = ord(s[right]) - ord('a')
        leaving = ord(s[right - m]) - ord('a')
        window[entering] += 1       # s[right] slides in
        window[leaving] -= 1        # s[right - m] slides out
        if window == need:          # 26 slot comparisons
            starts.append(right - m + 1)
    return starts


# --- try it ---
print(find_anagrams("cbaebabacd", "abc"))   # -> [0, 6]
print(find_anagrams("abab", "ab"))          # -> [0, 1, 2]
print(find_anagrams("baa", "aa"))           # -> [1]
print(find_anagrams("ab", "abc"))           # -> []
