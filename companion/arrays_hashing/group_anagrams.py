"""
Group Anagrams (LeetCode 49) - Medium
Chapter: arrays_hashing
Pattern: Canonical key bucketing

Given a list of lowercase strings, group the anagrams together in any order. Two
strings are anagrams if they contain the same letters with the same counts.
Example: ["eat", "tea", "tan", "ate", "nat", "bat"]
      -> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]].
"""


# --- helpers ---
def tidy(groups):
    """Sort inside each group and then sort the groups, so any valid answer prints the same."""
    tidied = []
    for group in groups:
        tidied.append(sorted(group))
    return sorted(tidied)


# --- brute force ---
def brute_force(strs):
    """Compare each word with one member of every group. O(n^2 * k log k) time."""
    groups = []
    for word in strs:
        placed = False
        for group in groups:
            if sorted(group[0]) == sorted(word):  # anagram test: same letters once sorted
                group.append(word)
                placed = True
                break
        if not placed:
            groups.append([word])
    return groups


# --- optimal ---
def group_anagrams(strs):
    """Bucket words by their letter-count signature. O(n * k) time, O(n * k) space."""
    buckets = {}  # 26-count signature -> list of words with that signature
    for word in strs:
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - ord("a")] += 1
        key = tuple(counts)  # a tuple can be a dict key, a list cannot
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(word)
    return list(buckets.values())


# --- try the brute force ---
print(tidy(brute_force(["eat", "tea", "tan", "ate", "nat", "bat"])))
# -> [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
print(tidy(brute_force([""])))                  # -> [['']]
print(tidy(brute_force(["a"])))                 # -> [['a']]
print(tidy(brute_force(["ab", "ba", "abc"])))   # -> [['ab', 'ba'], ['abc']]


# --- try the optimal ---
print(tidy(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])))
# -> [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
print(tidy(group_anagrams([""])))                  # -> [['']]
print(tidy(group_anagrams(["a"])))                 # -> [['a']]
print(tidy(group_anagrams(["ab", "ba", "abc"])))   # -> [['ab', 'ba'], ['abc']]
