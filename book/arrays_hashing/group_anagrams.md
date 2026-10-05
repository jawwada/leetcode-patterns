# Group Anagrams

*LeetCode 49 · Medium · Pattern: Canonical key bucketing · Reading time ~6 min*

## The problem

Given a list of lowercase strings, group the anagrams together in any order. Two strings are anagrams if they contain
the same letters with the same counts.

```text
Example: ["eat","tea","tan","ate","nat","bat"] ->
  [["eat","tea","ate"],["tan","nat"],["bat"]].
```

## What the problem is really asking

You get a list of lowercase words. Put words that are anagrams of each other (same letters, same counts, any order) into
the same group, and return the groups in any order.

The answer is a partition of the input: a list of lists, where every word lands in exactly one list. The hard part is
that "is an anagram of" is a relation between two words, and checking a relation between every pair of words is
quadratic. We want each word to find its group on its own, without meeting the others.

```text
input:  eat  tea  tan  ate  nat  bat

groups: [eat, tea, ate]   [tan, nat]   [bat]
         a e t letters     a n t        a b t
```

## Do it by hand first

Given these six words on cards, you might rearrange each card's letters alphabetically and write that on the back:
`eat` becomes `aet`, `tan` becomes `ant`. Then you sort the cards into piles by what is written on the back.

```text
card  back
eat   aet  \
tea   aet   >--- pile "aet"
ate   aet  /
tan   ant  \____ pile "ant"
nat   ant  /
bat   abt  ----- pile "abt"
```

You never compared two words with each other. Each card got a label computed from itself alone, and labels did the
grouping. The thing you kept track of was "label to pile". That is a dict from key to list.

## The first honest attempt

Keep a list of groups. For each word, walk the groups and test it against each group's first word (sort both and compare).
Join the first group that matches, or start a new group.

With `n` words of length up to `k`, the worst case (no anagrams at all) compares every word with every earlier group:
O(n^2) tests, each O(k log k) for the sorting. Time O(n^2 k log k).

The waste is doubled. First, each test re-sorts the group representative, which never changes. Second, and more
fundamental, comparing a word against groups is pointless when the answer depends only on the word's own letters.

```text
word "bat":
  vs "eat"?  sort "eat"="aet", "bat"="abt"  no
  vs "tan"?  sort "tan"="ant", "bat"="abt"  no
  -> new group
"abt" was computed twice and "aet" is re-sorted for every word
```

## The turning point

Claim: "is an anagram of" is an equivalence relation, so every word can be mapped to a canonical key that is equal for
two words exactly when they are anagrams. Then grouping is just hashing by that key.

Justification: anagrams are words with the same multiset of letters. Any function of a word that depends only on its
letter multiset, and fully captures that multiset, assigns the same key to anagrams and different keys to non-anagrams.
Two such functions:

1. **Sorted letters.** `"tea"` becomes `"aet"`. Sorting throws away order and keeps the multiset. Cost O(k log k) per word.
2. **Letter-count vector.** 26 counters, one per letter, as a tuple. `"tea"` becomes `(1,0,0,0,1,0,...,1,...)` with 1s at
   `a`, `e`, `t`. Cost O(k) per word plus 26 to build the tuple.

```text
"tea"  ->  counts[ord(ch) - ord('a')] += 1

index:  0  1  2  3  4  ...  19  ...  25
letter: a  b  c  d  e  ...  t   ...  z
count:  1  0  0  0  1  ...  1   ...  0
key = tuple(count)   (a list is unhashable)
```

Then the algorithm is: `buckets = defaultdict(list)`, and for each word, `buckets[key(word)].append(word)`. Return the
dict's values. No word is ever compared with another word.

This is the background chapter's canonical-key idea in its purest form. Whenever a problem says "group things that are
the same up to X" (rotation, shift, reordering, scaling), ask: what function erases X and keeps everything else? That
function's output is your dict key.

Why must the key be a tuple? A dict finds a key by its hash, and the hash must not change while the key is stored. Lists
are mutable, so Python refuses to hash them. A tuple is frozen and hashes fine. A string like `"#1#0#0..."` also works.

## Watch it work

`strs = ["eat", "tea", "tan", "ate", "nat", "bat"]`. Keys shown in short form: only the nonzero letters.

Frame 1

```text
word  "eat"   key {a:1 e:1 t:1}
buckets:
  {a1 e1 t1} -> [eat]
```

First word, new key, new list.

Frame 2

```text
word  "tea"   key {a:1 e:1 t:1}   same key as eat
buckets:
  {a1 e1 t1} -> [eat, tea]
```

The count vector ignored the letter order, so `tea` hashes to the same bucket.

Frame 3

```text
word  "tan"   key {a:1 n:1 t:1}   new key
buckets:
  {a1 e1 t1} -> [eat, tea]
  {a1 n1 t1} -> [tan]
```

`n` replaces `e`, so the 26-tuple differs in two positions: a different bucket.

Frame 4

```text
words "ate", "nat"
buckets:
  {a1 e1 t1} -> [eat, tea, ate]
  {a1 n1 t1} -> [tan, nat]
```

Each finds its existing bucket with one O(1) average lookup.

Frame 5

```text
word  "bat"   key {a:1 b:1 t:1}   new key
buckets:
  {a1 e1 t1} -> [eat, tea, ate]
  {a1 n1 t1} -> [tan, nat]
  {a1 b1 t1} -> [bat]
return list(buckets.values())
```

The dict's values are the answer, in first-seen order of keys.

Across frames, each bucket held exactly the words seen so far that share its key, and no word was ever compared with
another.

## Why it is correct

Two words are anagrams if and only if their letter-count vectors are equal: same count for every letter is the
definition of the same multiset. So the key function is "perfect" for this relation: equal keys means same group, and
different keys means different groups.

The dict maintains the invariant that, after processing a prefix of the input, `buckets[key]` lists exactly the words in
that prefix whose key is `key`. Appending each word to its key's list keeps it true. At the end, every word is in the
list of its key, the lists are disjoint, and each list is one anagram class. That is the required partition.

## Cost

- Count key: O(n * k) time (each letter once, plus 26 per word to build the tuple), O(n * k) space for the stored words
  and keys.
- Sorted key: O(n * k log k) time, same space. Usually fine in practice, and simpler to write: `tuple(sorted(w))` or
  `"".join(sorted(w))`.

Interviewers often accept the sorted key first and then ask, "can you avoid the sort?" The count tuple is that answer,
and it relies on the alphabet being small and fixed.

## Variations you will meet

- **Valid Anagram (two words).** The same key comparison for one pair: compare two count arrays, or one array with `+1`
  for the first word and `-1` for the second, checking all zeros.
- **Group Shifted Strings.** `"abc"`, `"bcd"`, `"xyz"` belong together. The key erases the shift: the tuple of differences
  between consecutive letters, mod 26.
- **Find All Anagrams in a String.** The key now slides: a window of fixed length whose count vector is updated by one
  letter in and one letter out, compared against the pattern's counts.
- **Unicode or huge alphabets.** The 26-slot tuple no longer works; use `frozenset(Counter(w).items())` or the sorted
  string as the key.

## What to carry forward

To group by "same up to X", design a key that erases X and keeps everything else, then let a dict of lists do the
grouping. The next problem counts instead of groups, and then turns those counts into array indices to avoid sorting.
