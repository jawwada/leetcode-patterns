"""
Shortest Palindrome (LeetCode 214) - Hard
Chapter: strings
Pattern: KMP failure function (longest border)

You may add characters only in front of s; return the shortest palindrome you can form.
Equivalently: find the longest palindromic prefix of s and mirror the rest in front.
Example: "aacecaaa" -> "aaacecaaa" (prepend "a"); "abcd" -> "dcbabcd" (prepend "dcb").
"""


# --- brute force ---
def brute_force(s):
    """Test each prefix, longest first, against its reverse. O(n^2) time, O(n) space."""
    n = len(s)
    for length in range(n, 0, -1):                 # longest prefix first
        prefix = s[:length]
        if prefix == prefix[::-1]:                 # a fresh O(length) check every time
            rest = s[length:]
            return rest[::-1] + s                  # mirror what is left in front
    return s


# --- optimal ---
def shortest_palindrome(s):
    """KMP failure array of s + '#' + reverse(s): its last entry is the longest one. O(n) time."""
    text = s + "#" + s[::-1]                       # '#' stops a border from crossing the middle
    m = len(text)
    fail = [0] * m                                 # fail[i] = longest proper border of text[:i+1]
    for i in range(1, m):
        k = fail[i - 1]
        while k > 0 and text[i] != text[k]:
            k = fail[k - 1]                        # fall back to a shorter border
        if text[i] == text[k]:
            k += 1
        fail[i] = k
    keep = fail[m - 1]                             # a prefix of s equal to a suffix of reverse(s)
    rest = s[keep:]
    return rest[::-1] + s


# --- try the brute force ---
print(brute_force("aacecaaa"))                     # -> aaacecaaa
print(brute_force("abcd"))                         # -> dcbabcd
print(brute_force("abab"))                         # -> babab
print(brute_force("aba"))                          # -> aba


# --- try the optimal ---
print(shortest_palindrome("aacecaaa"))             # -> aaacecaaa
print(shortest_palindrome("abcd"))                 # -> dcbabcd
print(shortest_palindrome("abab"))                 # -> babab
print(shortest_palindrome("aba"))                  # -> aba
