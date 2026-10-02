"""
Wildcard Matching (LeetCode 44)  — Hard
Pattern: Greedy two pointers with last-star backtrack

Problem
-------
Given a string s and a pattern p where '?' matches any single character and '*' matches any
sequence (including empty), decide whether p matches the whole of s.
Example: s = "adceb", p = "*a*b" -> True ("" a "dce" b). s = "acdcb", p = "a*c?b" -> False.

Brute force
-----------
Recursive backtracking: match the first characters and recurse; on a '*' try matching it to
the empty string (advance p) or to one more character (advance s), and succeed if either
branch does. Exponential time in the number of stars — a pattern with k stars can split s in
O(n^k) ways — and O(n + m) stack space. The waste is that the recursion re-explores
assignments for earlier stars that cannot possibly matter once a later star has been reached.

From brute force to optimal
---------------------------
The key observation is about which star to backtrack to. Suppose we are past some '*' and a
mismatch occurs. Any star earlier than the most recent one could absorb more characters, but
whatever it absorbs, the most recent star could absorb the same characters instead (it sits
later in the pattern and also matches any sequence), so re-trying earlier stars is redundant.
Therefore only the LAST star needs to be remembered: on a mismatch, return to the pattern
position right after it and let it swallow one more character of s. Greedy pointers i (into
s) and j (into p) with two saved positions (star, match) replace the whole recursion. The
pointer i never returns to a position before `match`, and `match` only increases, so the
total work is O(n * m) in the worst case and O(n + m) typically — no DP table.

Intuition
---------
Stars are "safety nets": once a star has been seen, the pattern after it only has to match
some suffix of the remaining text. If matching the suffix fails at some point, the only
useful repair is to let the most recent net catch one more character and try the following
pattern again from the next position. Earlier nets are dominated — anything they could do,
the latest net can do too.

Geometric view
--------------
Two pointers walk in lockstep along s (top rail) and p (bottom rail). When the bottom pointer
passes a '*', a bookmark is dropped at (star position, current s position). A mismatch does
not unwind everything: the bottom pointer snaps back to just after the bookmarked star, the
bookmark on the top rail slides one step right, and the top pointer resumes from there. The
bookmark only ever moves right, so the walk is bounded.

Steps
-----
1. i = j = 0; star = -1 (index of last '*' in p); match = 0 (s index that star currently
   matches up to).
2. While i < n: if p[j] is s[i] or '?': i += 1, j += 1.
3.   elif p[j] == '*': star = j, match = i, j += 1 (star matches empty for now).
4.   elif star != -1: j = star + 1, match += 1, i = match (last star eats one more char).
5.   else return False.
6. Skip trailing '*' in p; return j == len(p).

Complexity: O(n * m) worst-case time, O(1) space — i can be reset to match at most n times and each reset scans at most m pattern characters.
Pitfalls: backtracking to an earlier star (unnecessary and wrong bookkeeping); forgetting to
consume trailing stars in p after s is exhausted; not resetting j to star + 1 (resetting to
star re-reads the '*'); treating '?' as optional rather than exactly one character.
"""


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        i = j = 0
        star, match = -1, 0              # last '*' in p, and the s index it has eaten up to
        while i < len(s):
            if j < len(p) and p[j] in (s[i], "?"):
                i += 1
                j += 1
            elif j < len(p) and p[j] == "*":
                star, match = j, i       # let the star match "" for now
                j += 1
            elif star != -1:
                # mismatch after a star: the LAST star swallows one more character
                # (earlier stars are dominated by it) and we retry the rest of p
                match += 1
                i, j = match, star + 1
            else:
                return False
        while j < len(p) and p[j] == "*":
            j += 1
        return j == len(p)


def brute_force(s: str, p: str) -> bool:
    if not p:
        return not s
    if p[0] == "*":
        return brute_force(s, p[1:]) or (bool(s) and brute_force(s[1:], p))
    return bool(s) and p[0] in (s[0], "?") and brute_force(s[1:], p[1:])


if __name__ == "__main__":
    s = Solution()
    assert s.isMatch("aa", "a") is False
    assert s.isMatch("aa", "*") is True
    assert s.isMatch("cb", "?a") is False
    assert s.isMatch("adceb", "*a*b") is True
    assert s.isMatch("acdcb", "a*c?b") is False
    assert s.isMatch("", "***") is True
    assert s.isMatch("", "?") is False
    assert s.isMatch("abc", "a*b*c*") is True
    import random
    random.seed(44)
    for _ in range(600):
        text = "".join(random.choice("ab") for _ in range(random.randint(0, 8)))
        pat = "".join(random.choice("ab?*") for _ in range(random.randint(0, 6)))
        assert s.isMatch(text, pat) == brute_force(text, pat), (text, pat)
    print("ok")
