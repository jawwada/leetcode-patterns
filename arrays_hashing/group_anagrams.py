"""
Group Anagrams (LeetCode 49)  — Medium
Pattern: Canonical key bucketing

Problem
-------
Given a list of strings, group the anagrams together (any order). Two strings are
anagrams if they contain the same letters with the same counts.
Example: ["eat","tea","tan","ate","nat","bat"] -> [["eat","tea","ate"],["tan","nat"],["bat"]].

Brute force
-----------
Keep a list of groups. For each word, compare it against the representative of every
existing group using an anagram test (sort both, or count letters). O(n^2 * k) time
where k is the word length, O(n * k) space. The wasted work is re-running the
pairwise anagram test: a word is compared against every group even though the
test's answer depends only on the word's own letter multiset.

From brute force to optimal
---------------------------
The pairwise comparison is redundant because "is an anagram of" is an equivalence
relation: instead of comparing word-to-group, compute a canonical form of each word
once and let equal canonical forms meet in the same bucket. A hash map keyed by the
canonical form turns n^2 comparisons into n insertions. The key can be the sorted
string (O(k log k)) or, for lowercase letters, a tuple of 26 counts (O(k)), which is
the true optimum.

Intuition
---------
Anagrams are the same multiset of letters, so any function that depends only on
that multiset, not on letter order, assigns identical keys to anagrams and different
keys to non-anagrams. Hashing by that key groups them for free.

Geometric view
--------------
Imagine 26 counters forming a "fingerprint" vector for each word. Words that are
anagrams map to the same point in this 26-dimensional space. A dict is a set of
labelled bins at those points; each word is dropped into the bin at its point.

Steps
-----
1. Create a defaultdict(list) keyed by fingerprint.
2. For each word, build a 26-entry count list, one slot per letter.
3. Convert the list to a tuple (hashable) and append the word to that bucket.
4. Return the list of bucket values.

Complexity: O(n * k) time, O(n * k) space — one linear scan per word to build its
key; every word is stored once.
Pitfalls: using a list as a dict key (unhashable); forgetting non-anagrams can have the
same length; sorting is fine but is O(k log k) per word and the interviewer may ask
you to beat it.
"""
from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        buckets = defaultdict(list)
        for word in strs:
            counts = [0] * 26
            for ch in word:
                counts[ord(ch) - ord("a")] += 1
            buckets[tuple(counts)].append(word)  # tuple is hashable, list is not
        return list(buckets.values())


def brute_force(strs: List[str]) -> List[List[str]]:
    groups: List[List[str]] = []
    for word in strs:
        for g in groups:
            if sorted(g[0]) == sorted(word):
                g.append(word)
                break
        else:
            groups.append([word])
    return groups


def _normalize(groups: List[List[str]]) -> List[List[str]]:
    return sorted(sorted(g) for g in groups)


if __name__ == "__main__":
    s = Solution()
    ex1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    assert _normalize(s.groupAnagrams(ex1)) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert s.groupAnagrams([""]) == [[""]]
    assert s.groupAnagrams(["a"]) == [["a"]]
    assert _normalize(s.groupAnagrams(["ab", "ba", "abc"])) == [["ab", "ba"], ["abc"]]
    for case in (ex1, [""], ["a"], ["ab", "ba", "abc"]):
        assert _normalize(s.groupAnagrams(case)) == _normalize(brute_force(case))
    print("ok")
