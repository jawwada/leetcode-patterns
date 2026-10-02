"""
Group Shifted Strings (LeetCode 249)  — Medium
Pattern: Canonical key hashing (shift-invariant signature)

Problem
-------
A string can be "shifted" by moving every letter forward by the same amount, wrapping z -> a
("abc" -> "bcd" -> ... -> "xyz" -> "yza"). Given lowercase strings, group together all strings
that belong to the same shifting sequence; return the groups in any order.
Example: ["abc","bcd","acef","xyz","az","ba","a","z"] ->
  [["acef"], ["a","z"], ["az","ba"], ["abc","bcd","xyz"]].

Brute force
-----------
For every string, compare it against every existing group's representative: same length and
there exists one shift k that maps one onto the other (compute k from the first letters, then
verify every position). O(n^2 * L) time for n strings of length L, O(n * L) space. The wasted
work is pairwise comparison: we re-derive the "same shape" relation for each pair instead of
computing a shape once per string and letting a hash map do the grouping.

From brute force to optimal
---------------------------
Two strings are in the same sequence iff the DIFFERENCES between consecutive letters agree
(mod 26): shifting adds the same constant to every letter, so consecutive differences are
untouched. That makes the tuple of (s[i+1] - s[i]) % 26 a shift-invariant canonical key. Strings
with the same key go in the same bucket of a dict; one pass over the input, O(L) per string to
build the key. The mod 26 is what handles wrap-around ("az": z - a = 25; "ba": a - b = -1 = 25).

Intuition
---------
"Same up to a uniform shift" is an equivalence relation; grouping by an equivalence relation is
always "find a canonical representative, hash on it". Here the canonical form is the sequence
of gaps between neighbours, which deletes the absolute offset and keeps only the shape.

Geometric view
--------------
Plot letters as heights: "abc" = 0 1 2, "xyz" = 23 24 25, "bcd" = 1 2 3. All three curves are the
same staircase slid up or down; their step sizes (+1, +1) are identical. "az" = 0 25 and
"ba" = 1 0 look different until you take steps mod 26: 25 and -1 == 25, the same step.

Steps
-----
1. groups = defaultdict(list).
2. For each s: key = tuple((ord(b) - ord(a)) % 26 for consecutive a, b in s).
3. groups[key].append(s).
4. Return list(groups.values()).

Complexity: O(n * L) time, O(n * L) space — one key of length L-1 per string, one dict insert.
Pitfalls: forgetting % 26 (wrap-around pairs split apart); keying on the string itself minus
          its first letter without mod; single-letter strings all share the empty key (correct).
"""
from collections import defaultdict
from typing import List


class Solution:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strings:
            key = tuple((ord(b) - ord(a)) % 26 for a, b in zip(s, s[1:]))   # shift-invariant
            groups[key].append(s)
        return list(groups.values())


def brute_force(strings: List[str]) -> List[List[str]]:
    """Compare each string with every group's representative by trying the implied shift."""
    def same_sequence(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        k = (ord(b[0]) - ord(a[0])) % 26 if a else 0
        return all((ord(y) - ord(x)) % 26 == k for x, y in zip(a, b))

    groups: List[List[str]] = []
    for s in strings:
        for g in groups:
            if same_sequence(g[0], s):
                g.append(s)
                break
        else:
            groups.append([s])
    return groups


def canon(groups: List[List[str]]) -> set:
    return {frozenset(g) for g in groups}


if __name__ == "__main__":
    sol = Solution()
    ex = ["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]
    assert canon(sol.groupStrings(ex)) == {frozenset({"acef"}), frozenset({"a", "z"}),
                                          frozenset({"az", "ba"}), frozenset({"abc", "bcd", "xyz"})}
    assert canon(sol.groupStrings(["a"])) == {frozenset({"a"})}
    assert canon(sol.groupStrings(["az", "ba", "zx"])) == {frozenset({"az", "ba"}), frozenset({"zx"})}   # wrap-around
    assert canon(sol.groupStrings(["abc", "abd"])) == {frozenset({"abc"}), frozenset({"abd"})}
    for case in [ex, ["a"], ["az", "ba", "zx"], ["abc", "abd"], ["zz", "aa", "yz", "za"]]:
        assert canon(sol.groupStrings(case)) == canon(brute_force(case)), case
    print("ok")
