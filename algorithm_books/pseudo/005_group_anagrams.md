---
rank: 5
slug: group_anagrams
---

Given a list of lowercase words, group together the words that are anagrams of each other, words that use the same letters the same number of times. `["eat", "tea", "tan", "ate", "nat", "bat"]` becomes `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`, with the groups in the order they first appear.

The brute force tests every pair of words for being anagrams, `O(n²)` tests at `O(L)` each for words of length `L`. The insight is to stop comparing words with one another and give each word a canonical key: a value that comes out identical for two words exactly when they are anagrams. Grouping then becomes a single pass that files each word in a hash map under its key. Two keys work. The sorted letters, `"aet"` for eat, tea and ate, cost `O(L log L)` per word. The 26 letter counts cost `O(L)`, and that is the key the code uses, frozen into a tuple because a map key must be immutable to be hashed.

Picture each key as a barcode of 26 slots, one per letter from `a` to `z`. Shuffling a word's letters never changes its barcode, so anagrams print the same stripes and the map only has to drop equal barcodes into the same bucket. The order of the letters is forgotten; how many of each letter there are survives.

```text
          abcdefghijklmnopqrstuvwxyz    (letter counts, "." for zero)
"eat"  →  1...1..............1......    new key: group 0
"tea"  →  1...1..............1......    same key: group 0
"tan"  →  1............1.....1......    new key: group 1
"ate"  →  1...1..............1......    same key: group 0
"nat"  →  1............1.....1......    same key: group 1
"bat"  →  11.................1......    new key: group 2
result: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

```pseudo
FUNCTION LetterCounts(word)
    counts ← array of 26 zeros
    FOR EACH ch IN word
        slot ← ord(ch) - ord('a')          // 'a' → 0, 'b' → 1, ..., 'z' → 25
        counts[slot] ← counts[slot] + 1
    RETURN tuple(counts)                   // immutable, so it can be a map key

FUNCTION GroupAnagrams(words)
    groups ← empty map                     // count key → words with that key
    FOR EACH word IN words
        key ← LetterCounts(word)
        IF key NOT IN groups
            groups[key] ← empty list       // first word of a new group
        groups[key].append(word)
    RETURN groups.values()                 // one list per key, first-seen order
```

Each word costs `O(L)` to count plus a constant 26 to hash its key, so grouping `n` words takes `O(n · L)` time, and the groups take `O(n · L)` space. Reach for a canonical key whenever a problem says group, or treats two inputs as equal up to some rearrangement. The same count array decides Valid Anagram with one comparison and, slid along a string as a fixed-width window, finds every anagram of a pattern. The classic mistake is a key that throws information away: `set(word)` forgets multiplicity and merges `"aab"` with `"abb"`, and the sum of the character codes collides on `"ad"` and `"bc"`. A plain list as the key fails outright, because a list cannot be hashed.

*Practice:* LC 49 Group Anagrams · LC 242 Valid Anagram · LC 438 Find All Anagrams in a String
