"""
Longest Happy Prefix (LeetCode 1392)  — Hard
Pattern: KMP failure function (longest border)

Problem
-------
A "happy prefix" is a non-empty proper prefix of s that is also a suffix of s. Return the
longest one, or "" if none exists.
Example: "level" -> "l"; "ababab" -> "abab"; "leetcodeleet" -> "leet"; "a" -> "".

Brute force
-----------
For L = n-1 down to 1 compare s[:L] with s[n-L:]; the first match is the answer.
O(n^2) time, O(n) space for the slices. The wasted work: each L is tested independently, so a
mismatch deep inside the comparison for L is forgotten and the comparison for L-1 starts again
at character 0, re-reading the same prefix characters up to n times.

From brute force to optimal
---------------------------
The redundancy is restarting the prefix/suffix comparison for every candidate length.
Observation: let fail[i] be the length of the longest proper border (prefix == suffix) of
s[:i+1]. The borders of s[:i+1] are nested: the second-longest border of s[:i+1] is the longest
border of its longest border. So fail[i] can be computed from fail[i-1]: take k = fail[i-1]; if
s[i] == s[k] the border extends to k+1; otherwise shrink k to fail[k-1] and retry. The
while loop looks expensive but k only increases by at most 1 per character, so the total number
of decreases is at most n: amortised O(n). fail[n-1] is the answer's length; the whole array
is the KMP failure function.

Intuition
---------
A border is a self-overlap: the string laid over a shifted copy of itself with the overlap
matching. The longest overlap at position i is at most one longer than the longest overlap at
position i-1, and if that extension fails the next candidate is "the longest border of the
border", which we have already computed. Nothing is recomputed, nothing is sliced.

Geometric view
--------------
   s:  a b a b a b
   s:        a b a b a b     <- shift by 2: overlap "abab" matches -> border 4
   s:            a b a b a b <- shift by 4: overlap "ab" (the border of the border)
fail[] records, for every prefix, how far the string can be slid under itself and still match.

Steps
-----
1. fail = [0] * n.
2. For i in 1..n-1: k = fail[i-1]; while k and s[i] != s[k]: k = fail[k-1];
   if s[i] == s[k]: k += 1; fail[i] = k.
3. Return s[:fail[-1]].

Complexity: O(n) time, O(n) space — amortised: k rises at most n times in total, so it can fall
at most n times.
Pitfalls: using fail[k] instead of fail[k-1] when backing up; allowing the whole string as its
own border (border must be PROPER, which the recurrence guarantees); n == 1 -> "".
"""


class Solution:
    def longestPrefix(self, s: str) -> str:
        fail = [0] * len(s)                          # fail[i] = longest proper border of s[:i+1]
        for i in range(1, len(s)):
            k = fail[i - 1]
            while k and s[i] != s[k]:                # shrink to the border of the border
                k = fail[k - 1]
            if s[i] == s[k]:
                k += 1
            fail[i] = k
        return s[:fail[-1]]


def brute_force(s: str) -> str:
    for length in range(len(s) - 1, 0, -1):          # longest candidate first
        if s[:length] == s[-length:]:                # fresh O(length) comparison each time
            return s[:length]
    return ""


if __name__ == "__main__":
    s = Solution()
    assert s.longestPrefix("level") == "l"
    assert s.longestPrefix("ababab") == "abab"
    assert s.longestPrefix("leetcodeleet") == "leet"
    assert s.longestPrefix("a") == ""
    assert s.longestPrefix("aaaa") == "aaa"
    assert s.longestPrefix("abcab") == "ab"
    import random
    random.seed(3)
    for _ in range(300):
        w = "".join(random.choice("ab") for _ in range(random.randint(1, 12)))
        assert s.longestPrefix(w) == brute_force(w), w
    print("ok")
