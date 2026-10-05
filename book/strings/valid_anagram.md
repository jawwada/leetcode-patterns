# Valid Anagram
*LeetCode 242 · Easy · Pattern: Fixed-alphabet frequency count · Reading time ~5 min*

## The problem

Given two lowercase strings s and t, return True if t is an anagram of s: the same letters with the same
multiplicities, in any order.

```text
Example: s = 'anagram', t = 'nagaram' -> True; s = 'rat', t =
  'car' -> False.
```

## What the problem is really asking

Given two lowercase strings `s` and `t`, decide whether `t` is a rearrangement of `s`: the same letters, each used the same number of times, in any order. The answer is a single boolean. The interesting part is how much information you may throw away.

```text
 s = a a b c          t = c a b a
     \ \ \ \              / / / /
      same bag of letters?
      a:2  b:1  c:1      a:2  b:1  c:1     -> True
```

An anagram check is a **multiset** comparison. Positions do not matter. Only the count of each symbol does.

## Do it by hand first

Take `s = "aabc"` and `t = "caba"`. A person with a pencil does not sort anything. They make a tally: for each letter in the first word, put a stroke under that letter. For each letter in the second word, cross one out. If everything cancels, the words match.

```text
           a     b     c
 from s:  | |    |     |        +1 per letter
 from t:  x x    x     x        -1 per letter
 left:     0     0     0        all zero -> anagram
```

What your hand kept track of is a **row of tallies indexed by letter**. With only 26 possible letters, that row is a 26-cell array.

## The first honest attempt

`sorted(s) == sorted(t)` is correct, short, and what most people say first. It costs O(n log n) time and O(n) space for the two sorted copies.

Where is the waste? Sorting computes a full **order** on the letters: which `a` comes before which other `a`, and where `b` sits relative to `c`. The question never asks about order. Sorting works hard to build information that you then reduce to "equal or not".

```text
 sorted(s):  a a b c        work spent placing every letter
 sorted(t):  a a b c        in its exact final slot...
             = = = =        ...only to compare slot by slot,
                            = comparing counts
```

Sorted letters are still a legitimate **canonical form**: every anagram of a word sorts to the same string. Group Anagrams uses it as a dict key. For a single yes/no comparison, though, the counts are enough.

## The turning point

**Two strings are anagrams exactly when their letter histograms are equal, and one histogram built as a difference answers that in a single pass.**

A multiset over a fixed alphabet is completely described by its 26 counts, so comparing histograms is not an approximation of the question. It is the question.

You could build two histograms and compare them. It is neater to build one: walk both strings together, **add** one for the letter from `s` and **subtract** one for the letter from `t`. Cell `k` then holds `count_s(k) − count_t(k)`, and the strings are anagrams iff every cell is zero.

Put a length check first. Different lengths can never be anagrams, and `zip` silently stops at the shorter string, so without the check `"a"` vs `"ab"` would wrongly pass.

The structure is a plain list of 26 integers indexed by `ord(ch) - 97`. A dict or `Counter` works too, and is needed for arbitrary Unicode.

## Watch it work

`s = "aabc"`, `t = "caba"`. The lengths match (4 = 4). Only the cells a, b, c are shown, because the others stay at 0.

**Frame 1.** Pair (`a`, `c`): a goes up, c goes down.
```text
 s: [a] a  b  c      t: [c] a  b  a
 count   a: +1   b:  0   c: -1
```

**Frame 2.** Pair (`a`, `a`): a goes up and down, so it is unchanged.
```text
 s:  a [a] b  c      t:  c [a] b  a
 count   a: +1   b:  0   c: -1
```

**Frame 3.** Pair (`b`, `b`) cancels in the same way.
```text
 s:  a  a [b] c      t:  c  a [b] a
 count   a: +1   b:  0   c: -1
```

**Frame 4.** Pair (`c`, `a`): c comes back to 0, and a comes back to 0.
```text
 s:  a  a  b [c]     t:  c  a  b [a]
 count   a:  0   b:  0   c:  0     -> not any(count) -> True
```

Across the frames the array was always `histogram(prefix of s) − histogram(prefix of t)` for the prefixes read so far. Cells may go negative midway (c in frames 1–3); only the end state matters.

## Why it is correct

Invariant: after processing the first k pairs, `count[x] = (#x in s[:k]) − (#x in t[:k])` for every letter x. Each step adds one to the cell of `s[k]` and subtracts one from the cell of `t[k]`, which keeps the invariant. With the lengths equal, after n steps the prefixes are the whole strings, so `count[x] = 0` for every x iff every letter appears equally often in both. That is the definition of an anagram. If the lengths differ, at least one letter's count must differ, so returning False early is safe.

## Cost

- **Time O(n)**: one pass over the pairs, O(1) per step, plus a 26-cell `any` at the end.
- **Space O(1)**: 26 integers regardless of n. With a dict for Unicode input it is O(k) for k distinct symbols.
- The sorting version is O(n log n) time and O(n) space.

## Variations you will meet

- **Unicode input.** Use `Counter` or a dict. Mention normalisation: `"é"` can be one code point or `e` plus a combining accent, and the counts differ unless you normalise both strings first.
- **Group Anagrams (LeetCode 49).** Many words, bucket the anagrams together. Now you need a hashable key per word: `tuple(count)` or `"".join(sorted(w))`. The histogram is now a canonical form rather than a one-off comparison.
- **Find All Anagrams in a String (LeetCode 438).** The same difference-histogram, slid as a fixed-width window across a longer string, tracking how many cells are non-zero. That belongs to the sliding-window chapter.
- **Ransom Note (LeetCode 383).** Containment, not equality: check no cell is negative.

## What to carry forward

Throw away what the question does not ask about. Here that is order, which leaves a 26-cell histogram, and "add for one, subtract for the other" turns equality into "is everything zero". The next problem goes back to caring about order: it rearranges whole words in place using two pointers and a pair of reversals.
