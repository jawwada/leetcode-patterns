"""
Find Longest Awesome Substring (LeetCode 1542)  — Hard
Pattern: Prefix parity mask + first-seen positions

Problem
-------
A string of digits is awesome if some rearrangement of it is a palindrome, i.e. at most one
digit occurs an odd number of times. Given a digit string `s`, return the length of its longest
awesome substring (a single character always qualifies).
Example: s = "3242415" -> 5  ("24241" -> "24142").  s = "12345678" -> 1.  s = "213123" -> 6.

Brute force
-----------
For every start i, extend j to the right keeping ten digit counts; after each extension check
how many counts are odd and record the length when at most one is. O(n^2 * 10) time, O(1) space
— n = 10^5 gives 10^11 steps. The waste: we only ever care about the PARITY of each count, and
the parities of a substring are a function of two prefix states, yet we recompute them from
scratch for every start.

From brute force to optimal
---------------------------
Encode the parities of the ten digit counts in a 10-bit mask; let M[j] be the mask of the
prefix s[:j]. The parity mask of substring s[i:j] is M[j] XOR M[i] (even counts cancel). The
substring is awesome iff that XOR is 0 (all even) or a single bit (one odd digit) — only 11
possible target values. So for each right end j, instead of scanning every i, look up the
EARLIEST i whose prefix mask equals M[j] or M[j] ^ (1 << d) for d in 0..9; a dictionary
first_seen[mask] -> smallest index gives each lookup in O(1), and "earliest" is what maximises
j - i. One pass, 11 lookups per position: O(11 n).

Intuition
---------
"Can be rearranged into a palindrome" is a parity statement, and parities compose by XOR. That
turns a substring question into a two-prefix question: find two prefixes whose masks differ in
at most one bit. Store the first time each of the 1024 masks appears and every later position
asks about its 11 compatible partners.

Geometric view
--------------
Write the running parity as a 10-column binary row that flips one column per character. Lay the
rows out downward; a substring is awesome when its top and bottom rows differ in 0 or 1 column.
At each row j you look up the highest row equal to row j, or equal with one column flipped, and
measure the vertical distance.

Steps
-----
1. first = {0: -1} (the empty prefix has mask 0 at position -1); mask = 0; best = 0.
2. For j, c in enumerate(s): mask ^= 1 << int(c).
3. If mask in first: best = max(best, j - first[mask]) (all counts even).
4. For d in 0..9: if mask ^ (1 << d) in first: best = max(best, j - first[mask ^ (1 << d)]).
5. If mask not in first: first[mask] = j (keep the earliest).
6. Return best.

Complexity: O(11 n) time, O(2^10) space — at most 1024 distinct masks are stored.
Pitfalls: overwriting first[mask] with a later index (destroys the maximum length); forgetting
to seed mask 0 at index -1 (a whole prefix can be awesome); checking only the all-even case and
missing the one-odd-digit case.
"""
import random


class Solution:
    def longestAwesome(self, s: str) -> int:
        first = {0: -1}                               # parity mask -> earliest prefix index
        mask = best = 0
        for j, c in enumerate(s):
            mask ^= 1 << int(c)                       # flip this digit's parity bit
            if mask in first:                         # same parities: all counts even
                best = max(best, j - first[mask])
            for d in range(10):                       # exactly one digit odd
                partner = mask ^ (1 << d)
                if partner in first:
                    best = max(best, j - first[partner])
            if mask not in first:
                first[mask] = j                       # keep the earliest occurrence only
        return best


def brute_force(s: str) -> int:
    best = 0
    for i in range(len(s)):
        counts = [0] * 10
        for j in range(i, len(s)):                    # every substring s[i:j+1]
            counts[int(s[j])] += 1
            if sum(c & 1 for c in counts) <= 1:
                best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    s = Solution()
    assert s.longestAwesome("3242415") == 5
    assert s.longestAwesome("12345678") == 1
    assert s.longestAwesome("213123") == 6
    assert s.longestAwesome("00") == 2
    assert s.longestAwesome("7") == 1                              # single character
    rng = random.Random(1542)
    for _ in range(200):
        t = "".join(rng.choice("0123") for _ in range(rng.randint(1, 14)))
        assert s.longestAwesome(t) == brute_force(t), t
    print("ok")
