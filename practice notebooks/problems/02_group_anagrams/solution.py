"""
Group Anagrams (LeetCode 49) - Medium
Area: arrays & hashing
Key operations: build a 26-count key per word, append the word to the bucket for that key, return the buckets

Given a list of lowercase words, group the anagrams together (any order of groups and of words
inside a group). Two words are anagrams if they contain the same letters with the same counts.
Example: ["eat", "tea", "tan", "ate", "nat", "bat"] -> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
"""
from collections import defaultdict
from typing import List


# --- brute force ---
def brute_force(strs: List[str]) -> List[List[str]]:
    """Compare each word against the first word of every existing group with an anagram test
    (sort both). O(n^2 * k log k): a word is tested against every group, although its own letters
    alone already decide where it belongs."""
    groups = []
    for word in strs:
        for g in groups:
            if sorted(g[0]) == sorted(word):
                g.append(word)
                break
        else:
            groups.append([word])
    return groups


# --- optimal ---
def solve(strs: List[str]) -> List[List[str]]:
    """Give every word a key that depends only on its letter multiset, a tuple of 26 counts, and
    drop it into the dict bucket for that key. O(n * k) for n words of length k."""
    buckets = defaultdict(list)  # 26-count key -> words with exactly those letters
    for word in strs:
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - ord("a")] += 1
        key = tuple(counts)
        buckets[key].append(word)
    return list(buckets.values())


# --- demo ---
def demo():
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    return solve(words)


# --- bugs ---
BUGS = [
    {
        "replace": "            counts[ord(ch) - ord(\"a\")] += 1",
        "with":    "            counts[ord(ch) - ord(\"a\")] = 1",
        "fix": "count with += 1, not a presence flag",
        "why": "With a 0/1 flag 'aab' and 'abb' get the same key and land in one group, although they are not anagrams.",
        "decoys": [
            {"line": "        counts = [0] * 26", "change": "should be 25 slots, [0] * 25"},
            {"line": "        key = tuple(counts)", "change": "should be key = counts"},
            {"line": "    return list(buckets.values())", "change": "should return list(buckets)"},
        ],
    },
    {
        "replace": "        buckets[key].append(word)",
        "with":    "        buckets[key] = [word]",
        "fix": "append to the bucket, do not replace it",
        "why": "Every word overwrites its group, so each group keeps only its last word: the example returns [['ate'], ['nat'], ['bat']].",
        "decoys": [
            {"line": "        for ch in word:", "change": "should iterate set(word)"},
            {"line": "    buckets = defaultdict(list)  # 26-count key -> words with exactly those letters", "change": "should be defaultdict(set)"},
            {"line": "        key = tuple(counts)", "change": "should be tuple(sorted(word))"},
        ],
    },
    {
        "replace": "        key = tuple(counts)",
        "with":    "        key = tuple(sorted(counts))",
        "fix": "keep counts in letter order, do not sort them",
        "why": "After sorting, 'ab' and 'cd' both become (0, ..., 0, 1, 1) and are grouped together although they share no letters.",
        "decoys": [
            {"line": "            counts[ord(ch) - ord(\"a\")] += 1", "change": "should index with ord(ch) - 97 - 1"},
            {"line": "        buckets[key].append(word)", "change": "should append only when the bucket exists"},
            {"line": "    for word in strs:", "change": "should iterate sorted(strs)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
