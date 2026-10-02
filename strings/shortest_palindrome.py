"""
Shortest Palindrome (LeetCode 214)  — Hard
Pattern: KMP failure function (longest border)

Problem
-------
You may add characters only in FRONT of s. Return the shortest palindrome you can make.
Example: "aacecaaa" -> "aaacecaaa" (prepend "a"); "abcd" -> "dcbabcd" (prepend "dcb").
Equivalent: find the longest palindromic PREFIX p of s; answer = reverse(s[len(p):]) + s.

Brute force
-----------
For L = n down to 1, test whether s[:L] is a palindrome by comparing it to its reverse; the first
hit is the longest palindromic prefix. O(n^2) time, O(n) space for the reversed copies. The wasted
work: each test re-compares characters from scratch even though the test for L and the test for
L-1 share almost all of their comparisons, and a mismatch at one position tells you nothing you
reuse for the next L.

From brute force to optimal
---------------------------
The redundancy is testing each prefix independently. Observation: "s[:L] is a palindrome" is the
same as "s[:L] equals the last L characters of reverse(s)", i.e. a prefix of s that is also a
suffix of rev(s). Matching a prefix of one string against a suffix of another is exactly what
the KMP failure function computes for the concatenation t = s + '#' + rev(s): fail[-1] is the
length of the longest proper border of t (a prefix that is also a suffix). The '#' separator
(absent from s) caps the border at len(s), so fail[-1] is exactly the longest palindromic
prefix length. The failure array is built in O(n) because the border length only ever drops
along the chain fail[k-1], and the total number of drops is bounded by the total number of
increases (at most one per character).

Intuition
---------
A palindromic prefix of s reads the same forwards (front of s) and backwards (end of rev(s)).
Glue the two strings with a separator and ask the classic KMP question: what is the longest
string that is both a prefix and a suffix of the whole thing? That length is what you can keep;
mirror the rest in front.

Geometric view
--------------
   s = a a c e c a a a            rev(s) = a a a c e c a a
   t = a a c e c a a a # a a a c e c a a
       [ prefix ]                       [ suffix ]   <- same 7 chars: "aacecaa"
The failure function slides the string under itself: fail[i] is how far the prefix overlaps
the text ending at i. At the very end of t the overlap can only be a palindromic prefix of s.

Steps
-----
1. t = s + "#" + s[::-1]; fail = [0] * len(t).
2. For i in 1..len(t)-1: k = fail[i-1]; while k and t[i] != t[k]: k = fail[k-1];
   if t[i] == t[k]: k += 1; fail[i] = k.
3. keep = fail[-1] (longest palindromic prefix of s).
4. Return s[keep:][::-1] + s.

Complexity: O(n) time, O(n) space — amortised KMP over a string of length 2n+1.
Pitfalls: omitting the separator (a border could then run past len(s), e.g. "aaaa");
mirroring the wrong part (prepend reverse of the SUFFIX s[keep:], not of the prefix);
off-by-one in fail[k-1] when backing up.
"""


class Solution:
    def shortestPalindrome(self, s: str) -> str:
        t = s + "#" + s[::-1]                         # '#' stops a border crossing the middle
        fail = [0] * len(t)                           # fail[i] = longest proper border of t[:i+1]
        for i in range(1, len(t)):
            k = fail[i - 1]
            while k and t[i] != t[k]:                 # fall back along shorter borders
                k = fail[k - 1]
            if t[i] == t[k]:
                k += 1
            fail[i] = k
        keep = fail[-1]                               # longest palindromic prefix of s
        return s[keep:][::-1] + s


def brute_force(s: str) -> str:
    for length in range(len(s), 0, -1):               # longest prefix first
        prefix = s[:length]
        if prefix == prefix[::-1]:                    # fresh O(length) check every time
            return s[length:][::-1] + s
    return s


if __name__ == "__main__":
    s = Solution()
    assert s.shortestPalindrome("aacecaaa") == "aaacecaaa"
    assert s.shortestPalindrome("abcd") == "dcbabcd"
    assert s.shortestPalindrome("") == ""
    assert s.shortestPalindrome("a") == "a"
    assert s.shortestPalindrome("aba") == "aba"
    assert s.shortestPalindrome("abab") == "babab"
    assert s.shortestPalindrome("aaaa") == "aaaa"
    import random
    random.seed(1)
    for _ in range(300):
        w = "".join(random.choice("ab") for _ in range(random.randint(0, 10)))
        assert s.shortestPalindrome(w) == brute_force(w), w
    print("ok")
