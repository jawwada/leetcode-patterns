"""
Longest Duplicate Substring (LeetCode 1044)  — Hard
Pattern: Binary search on length + rolling hash (Rabin-Karp)

Problem
-------
Given a string s of lowercase letters, return any duplicated substring of maximum length
(a substring that occurs two or more times, occurrences may overlap). Return "" if there is
none.
Example: s = "banana" -> "ana" (occurs at 1 and 3). s = "abcd" -> "".

Brute force
-----------
For each length L from n - 1 down to 1, put every substring of length L into a set and stop
at the first repeat. There are O(n) lengths, O(n) substrings each, and each substring costs
O(L) to slice and hash: O(n^3) time, O(n^2) space in the worst case. Two things are wasted:
we try every length although the answer's length can be found by search, and we hash each
substring from scratch although neighbouring substrings share L - 1 characters.

From brute force to optimal
---------------------------
Observation 1 (O(n) lengths -> O(log n)): if some substring of length L is duplicated, then
so is every shorter length (take any prefix of the two occurrences). "Has a duplicate of
length L" is therefore monotone in L, and binary search finds the largest feasible L in
log n probes. Observation 2 (O(nL) per probe -> O(n)): hash the window of length L with a
polynomial rolling hash, h = sum(code[i] * B^(L-1-i)) mod M; sliding one step right is
h = (h * B - code[out] * B^L + code[in]) mod M, an O(1) update. Store hashes in a dict and,
on a hash hit, compare the actual substrings so a collision can never produce a wrong answer
(with a 61-bit modulus collisions are astronomically rare, so the check is almost free).
Total O(n log n) expected time. A suffix array gives a deterministic O(n log n), but the
hash version is what fits in an interview.

Intuition
---------
Two ideas stack: binary search converts "find the longest" into "check a fixed length" using
monotonicity, and Rabin-Karp makes "check a fixed length" linear by treating each window as
a base-B number whose value is updated arithmetically as it slides. Equal strings have equal
hashes, so a repeated hash is a candidate repeat; verifying the characters makes it exact.

Geometric view
--------------
Picture a window of width L gliding along the string; above it a single number (the hash)
is being rolled: multiply by the base, drop the leftmost digit's weight, add the new digit.
Each number is dropped into a bag; a bag that already holds the same number marks a repeat.
Outside this inner loop, a binary search dial sets L: a repeat found turns the dial up, none
found turns it down.

Steps
-----
1. codes = [ord(c) - 96 for c in s]; MOD = 2^61 - 1; BASE = 257 (or random).
2. search(L): hash the first L codes; seen = {hash: [0]}; power = BASE^L mod MOD.
3.   For i in 1..n-L: roll the hash; if it is in seen and some stored start matches
     s[j:j+L] == s[i:i+L], return i; else record i.
4.   Return -1.
5. Binary search lo = 1, hi = n - 1; if search(mid) >= 0 record (start, mid) and go right,
   else go left.
6. Return the recorded substring or "".

Complexity: O(n log n) expected time, O(n) space — log n probes, each a linear rolling-hash scan over a dict of at most n hashes.
Pitfalls: recomputing each window hash from scratch (O(nL) per probe); subtracting the
outgoing character without multiplying by BASE^L; forgetting the modulus can make the
subtraction negative in other languages; not verifying on a hash hit; lengths from n - 1
only (a length-n substring can never repeat).
"""


class Solution:
    def longestDupSubstring(self, s: str) -> str:
        n = len(s)
        codes = [ord(c) - 96 for c in s]
        MOD, BASE = (1 << 61) - 1, 257

        def search(L: int) -> int:       # start of some repeated length-L window, or -1
            h = 0
            for c in codes[:L]:
                h = (h * BASE + c) % MOD
            seen = {h: [0]}
            power = pow(BASE, L, MOD)    # weight of the character leaving the window
            for i in range(1, n - L + 1):
                h = (h * BASE - codes[i - 1] * power + codes[i + L - 1]) % MOD
                if h in seen:
                    if any(s[j:j + L] == s[i:i + L] for j in seen[h]):   # rule out collisions
                        return i
                    seen[h].append(i)
                else:
                    seen[h] = [i]
            return -1

        lo, hi = 1, n - 1
        start, best = -1, 0
        while lo <= hi:                  # feasibility is monotone in L
            mid = (lo + hi) // 2
            i = search(mid)
            if i >= 0:
                start, best = i, mid
                lo = mid + 1
            else:
                hi = mid - 1
        return s[start:start + best] if start >= 0 else ""


def brute_force(s: str) -> str:
    n = len(s)
    for L in range(n - 1, 0, -1):
        seen = set()
        for i in range(n - L + 1):
            sub = s[i:i + L]
            if sub in seen:
                return sub
            seen.add(sub)
    return ""


if __name__ == "__main__":
    s = Solution()
    assert s.longestDupSubstring("banana") == "ana"
    assert s.longestDupSubstring("abcd") == ""
    assert s.longestDupSubstring("aaaaa") == "aaaa"
    assert s.longestDupSubstring("a") == ""
    assert s.longestDupSubstring("abcabcabc") in ("abcabc",)
    import random
    random.seed(1044)
    for _ in range(300):
        text = "".join(random.choice("ab") for _ in range(random.randint(1, 14)))
        got, want = s.longestDupSubstring(text), brute_force(text)
        assert len(got) == len(want)
        assert got == "" or text.find(got, text.find(got) + 1) != -1
    print("ok")
