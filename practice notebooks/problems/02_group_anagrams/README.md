# Group Anagrams (LeetCode 49)

**Area:** arrays & hashing · **Difficulty:** Medium · **Key operations:** build a 26-count key per word, append the word to the bucket for that key, return the buckets

## Problem

Given a list of lowercase words, group the anagrams together. Two words are anagrams if they contain the same letters with the same counts. Groups may be returned in any order, and the words inside a group in any order.

## Example

```
words  = ["eat", "tea", "tan", "ate", "nat", "bat"]
groups = [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

## Brute force

Keep a list of groups. For each word, compare it with the first word of every existing group using an anagram test (sort both strings and compare). Join the first group that matches, or open a new one.

O(n² · k log k) time for n words of length k. The wasted work is the pairwise test itself: a word is compared with *every* group, although its own letters alone already determine where it belongs.

## From brute force to optimal

"Is an anagram of" is an equivalence relation, so instead of comparing word against group, compute a **canonical key** for each word once and let equal keys meet in the same dict bucket. The key only has to depend on the multiset of letters, not their order. Two choices:

- the sorted string `"".join(sorted(word))`, O(k log k) per word;
- a tuple of 26 letter counts, O(k) per word, which is the true optimum for lowercase input.

n² comparisons become n dict insertions.

## Intuition

Think of 26 counters as a fingerprint for a word. Anagrams have identical fingerprints because reordering letters does not change how many of each there are, and non-anagrams differ in at least one counter. A dict is a wall of labelled bins; each word is dropped into the bin labelled with its fingerprint, and the bins are the answer. The list must be turned into a tuple first, because a list is not hashable.

## Walkthrough

Keys are shown compactly (`a1e1t1` means one a, one e, one t; all other counts are 0).

```
word 'eat'  key a1e1t1    buckets  a1e1t1: [eat]
word 'tea'  key a1e1t1    buckets  a1e1t1: [eat, tea]
word 'tan'  key a1n1t1    buckets  a1e1t1: [eat, tea] | a1n1t1: [tan]
word 'ate'  key a1e1t1    buckets  a1e1t1: [eat, tea, ate] | a1n1t1: [tan]
word 'nat'  key a1n1t1    buckets  a1e1t1: [eat, tea, ate] | a1n1t1: [tan, nat]
word 'bat'  key a1b1t1    buckets  a1e1t1: [eat, tea, ate] | a1n1t1: [tan, nat] | a1b1t1: [bat]

return the bucket values: [[eat, tea, ate], [tan, nat], [bat]]
```

## Steps

1. `buckets = defaultdict(list)`.
2. For each word: `counts = [0] * 26`; for each letter `counts[ord(ch) - ord('a')] += 1`.
3. `key = tuple(counts)` (hashable); `buckets[key].append(word)`.
4. Return `list(buckets.values())`.

## Complexity

O(n · k) time: one pass over the letters of every word to build its key, one O(1) dict insert per word. O(n · k) space to hold the words plus O(26 · n) for the keys.

## Pitfalls

- **Presence instead of count.** `counts[...] = 1` turns the key into a set of letters, so `"aab"` and `"abb"` collide. Use `+= 1`.
- **Assigning instead of appending.** `buckets[key] = [word]` overwrites the group each time, keeping only its last word: the example returns `[['ate'], ['nat'], ['bat']]`.
- **Sorting the counts.** `tuple(sorted(counts))` forgets which letter each count belongs to, so `"ab"` and `"cd"` get the same key.
- **Using a list as the key.** `buckets[counts]` raises `TypeError: unhashable type`. Convert to a tuple (or use the sorted string).
- **Off-by-one alphabet.** `[0] * 25` raises `IndexError` on the letter z.
