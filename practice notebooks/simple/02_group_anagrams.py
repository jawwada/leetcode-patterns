"""
Group Anagrams (LeetCode 49)
Group together words that are made of exactly the same letters.
  ["eat", "tea", "tan", "ate", "nat", "bat"]  ->  [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

Idea: anagrams have identical letter counts. Turn each word's 26 letter counts
      into a key, and drop the word into the dict bucket for that key.

Pseudocode:
  buckets = {}                    # letter-count key -> words
  for word in words:
      counts = 26 zeros; count each letter
      buckets[tuple(counts)].append(word)
  return all buckets

Time O(n * k) for n words of length k, space O(n * k).
"""
from collections import defaultdict


def group_anagrams(words):
    buckets = defaultdict(list)          # letter-count key -> words
    for word in words:
        counts = [0] * 26
        for ch in word:                  # count each letter
            counts[ord(ch) - ord("a")] += 1
        buckets[tuple(counts)].append(word)   # same counts -> same bucket
    return list(buckets.values())


if __name__ == "__main__":
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    print(group_anagrams(["a"]))         # [['a']]
