"""
Group Anagrams - Canonical-Key Hashing

Given a list of lowercase words, group the words that are anagrams of each
other (same letters, same counts), groups in first-seen order:
["eat", "tea", "tan", "ate", "nat", "bat"]
-> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]].
"""


# --- algorithm ---
def letter_counts(word):
    """The 26 letter counts of a word, as a tuple: anagrams share it. O(L)."""
    counts = [0] * 26
    for ch in word:
        slot = ord(ch) - ord('a')   # 'a' -> 0, 'b' -> 1, ..., 'z' -> 25
        counts[slot] += 1
    return tuple(counts)            # a tuple can be a dict key; a list cannot


def group_anagrams(words):
    """Bucket every word under its count key. O(n * L) time and space."""
    groups = {}                     # count key -> words with that key
    for word in words:
        key = letter_counts(word)
        if key not in groups:
            groups[key] = []        # first word of a new group
        groups[key].append(word)
    return list(groups.values())    # one list per key, in first-seen order


# --- try it ---
groups = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
print(groups)   # -> [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
print(group_anagrams(["", "b", ""]))    # -> [['', ''], ['b']]
print(group_anagrams(["aab", "abb"]))   # -> [['aab'], ['abb']]
print(group_anagrams(["ad", "bc"]))     # -> [['ad'], ['bc']]
