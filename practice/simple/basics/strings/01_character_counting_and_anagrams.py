"""
Character Counting and Anagrams (basics: strings)
Count letters with a 26-slot array, test two words for anagrams, and group anagrams together.
  ["eat", "tea", "tan", "ate", "nat", "bat"]  ->  [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]

Idea: anagrams use the same letters the same number of times, so their count arrays match.
      Counting is one pass (no sorting needed), and the counts turned into a tuple make a
      dict key that every anagram of a word shares.

Pseudocode:
  letter_counts(word): counts = [0] * 26; for ch in word: counts[ch - 'a'] += 1
  is_anagram(s, t):    len(s) == len(t) and letter_counts(s) == letter_counts(t)
  group_anagrams(words):
      groups = {}                                   # tuple of counts -> words
      for w in words: groups[tuple(letter_counts(w))].append(w)
      return the groups, words sorted inside each group, groups sorted

Time O(total letters) to count and group (plus sorting the output), space O(total letters).
"""
from collections import defaultdict


def letter_counts(word):
    counts = [0] * 26                    # one slot per letter a..z
    for ch in word:
        counts[ord(ch) - ord("a")] += 1
    return counts


def is_anagram(s, t):
    if len(s) != len(t):                 # different lengths: never anagrams
        return False
    return letter_counts(s) == letter_counts(t)


def group_anagrams(words):
    groups = defaultdict(list)           # tuple of counts -> words
    for w in words:
        key = tuple(letter_counts(w))    # a list can't be a dict key, a tuple can
        groups[key].append(w)
    return sorted(sorted(g) for g in groups.values())  # a fixed output order


if __name__ == "__main__":
    print(letter_counts("abca")[:3])     # [2, 1, 1]
    print(is_anagram("listen", "silent"), is_anagram("aab", "abb"))  # True False
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
