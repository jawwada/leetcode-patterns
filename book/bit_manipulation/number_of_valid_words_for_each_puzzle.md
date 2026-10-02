# Number of Valid Words for Each Puzzle

*LeetCode 1178 · Hard · Pattern: Bitmask counting + submask enumeration · Reading time ~10 min*

## What the problem is really asking

You get a list of words and a list of puzzles. Each puzzle is exactly 7 distinct letters. A word is valid for a puzzle when two things hold:

1. every letter of the word appears in the puzzle, and
2. the word contains the puzzle's **first** letter.

For each puzzle, report how many words are valid. The answer is a list of counts, one per puzzle.

The hardness is scale: up to 10^5 words and 10^4 puzzles. Checking every pair is 10^9 checks before you even look at letters.

Notice what does **not** matter. Repeated letters ("aaaa" is the same as "a") and letter order ("able" vs "bale") make no difference. Only the *set* of letters in a word counts. That is the first hint that a word is really a bitmask.

```text
puzzle "actresz"  first letter 'a'

word     letters      inside puzzle?  has 'a'?  valid
aaaa     {a}          yes             yes       yes
asas     {a,s}        yes             yes       yes
able     {a,b,l,e}    no (b,l)        yes       no
actt     {a,c,t}      yes             yes       yes
actor    {a,c,t,o,r}  no (o)          yes       no
access   {a,c,e,s}    yes             yes       yes
                                         count = 4
```

## Do it by hand first

Shrink it to something you can fully enumerate. Use the puzzle "abc" with first letter 'a'. The code does not care that a real puzzle has 7 letters, so this toy keeps every step visible. Take the words `aa, ab, ba, bc, cab, d`.

By hand you would first reduce each word to its letter set, and notice duplicates: "ab" and "ba" are the same set.

```text
word   set      as bits (c b a)
aa     {a}      0 0 1
ab     {a,b}    0 1 1
ba     {a,b}    0 1 1   same set as "ab"
bc     {b,c}    1 1 0
cab    {a,b,c}  1 1 1
d      {d}      d is bit 3: 1 0 0 0
```

Then for the puzzle you would ask: which of these sets fit inside {a, b, c} and include a? The answers are {a}, {a,b} (twice) and {a,b,c}, for a count of 4.

What your hand kept track of was a **tally of letter sets**, "how many words have exactly this set", and then a question asked of the puzzle: "which sets am I willing to accept?" The puzzle accepts only subsets of its own letters. A 7-letter puzzle has 2^7 = 128 subsets, and only half of them contain the first letter. So the puzzle accepts just 64 possible sets.

## The first honest attempt

For each puzzle, for each word, test `set(word) <= set(puzzle)` and `puzzle[0] in word`.

```text
             w1   w2   w3  ...  w100000
puzzle 1    chk  chk  chk  ...   chk
puzzle 2    chk  chk  chk  ...   chk
  ...
puzzle 10^4 chk  chk  chk  ...   chk
            10^9 checks, each touching up to 50 letters
```

The repeated work has two layers.

- Every word is rebuilt into a set and re-examined for every puzzle, although its letter set never changes.
- Thousands of words share a letter set ("aaaa", "aa", "a" are all {a}), yet each copy is tested on its own.

Turning words into 26-bit masks first and testing `w & ~p == 0` makes each check O(1), but there are still 10^9 of them. Masks alone do not save us. The loop is pointed the wrong way.

## The turning point

**Claim: count words by their letter-set mask once, then let each puzzle enumerate the at most 64 masks it would accept and add up their counts.**

There are two moves here, and each kills one layer of waste.

**Move 1: collapse words to masks.** Map each word to a 26-bit integer, with bit `ord(c) - 97` set for each letter `c`. Put those in a counter `cnt[mask] = number of words with that exact letter set`. After this, the words are never read again. The 10^5 words become at most 10^5 distinct keys, usually far fewer.

**Move 2: enumerate from the small side.** Validity is a subset relation: word mask `w` fits puzzle mask `p` when `w` is a submask of `p`. There are two ways to find all pairs (word, puzzle) with `w ⊆ p`.

- From the word side: for each word mask, find all puzzles that are supersets. Supersets of a small set inside 26 letters are huge in number.
- From the puzzle side: for each puzzle, list its submasks. That is only 2^7 = 128, and 64 once we insist on the first letter.

The puzzle side is tiny, so we flip the loop. For each puzzle we generate its 64 acceptable masks and look each one up in the counter in O(1).

```text
puzzle mask p with 7 set bits, first-letter bit F

  26 columns:  . . 1 . . 1 . 1 . . 1 . 1 . . 1 . . F . . . . .
                   ^     ^   ^     ^   ^     ^     ^
  submasks = all on/off choices of those 7 columns
  F forced on -> 2^6 = 64 lookups in cnt
```

The tool for listing submasks is the step `sub = (sub - 1) & p`. Subtracting 1 counts down in binary. AND-ing with `p` throws away any bit outside the puzzle, so the count jumps straight to the next smaller number that uses only the puzzle's columns. Starting from `sub = p`, it visits every submask exactly once in decreasing order and reaches 0 last.

You could instead loop over the 7 letters and build all 128 subsets recursively. That is the same set of masks; the `(sub - 1) & p` walk is just the compact way to write it.

Why not use the arithmetic trick on the word side? Because a word can use up to 26 letters, and a word mask with 20 bits has a million submasks. The asymmetry, 7 letters against 26, is the whole problem.

## Watch it work

Toy instance: words `aa, ab, ba, bc, cab, d`; puzzle `"abc"`, first letter 'a' = bit 0. Bits are written `d c b a`.

```text
Frame 1   build cnt from words
  aa ->0001  ab ->0011  ba ->0011
  bc ->0110  cab->0111  d  ->1000
  cnt = {0001:1, 0011:2, 0110:1, 0111:1, 1000:1}
```
Six words became five keys; "ab" and "ba" merged. Words are never read again.

```text
Frame 2   puzzle p = 0111, first F = 0001
  sub = 0111   has F? yes   cnt[0111] = 1
  total = 1
```
The full puzzle set itself is the first submask; "cab" counts.

```text
Frame 3   sub = (0111-1) & 0111 = 0110
  has F? no -> skip                total = 1
  sub = (0110-1) & 0111 = 0101
  has F? yes  cnt[0101] = 0        total = 1
```
{b,c} is skipped because it lacks 'a'; {a,c} is acceptable but no word has it.

```text
Frame 4   sub = (0101-1) & 0111 = 0100
  has F? no -> skip                total = 1
  sub = (0100-1) & 0111 = 0011
  has F? yes  cnt[0011] = 2        total = 3
```
Both "ab" and "ba" arrive in one lookup; that is the payoff of the counter.

```text
Frame 5   sub = (0011-1) & 0111 = 0010
  has F? no -> skip                total = 3
  sub = (0010-1) & 0111 = 0001
  has F? yes  cnt[0001] = 1        total = 4
```
{a} is accepted: "aa" counts.

```text
Frame 6   sub = (0001-1) & 0111 = 0000
  has F? no -> skip; sub == 0 -> stop
  answer for "abc" = 4
  never visited: 1000 ("d") - not a submask
```
The walk ended after exactly 2^3 = 8 submasks. The mask for "d", outside the puzzle, was never looked at.

Across the frames, `sub` always stayed inside `p`, never repeated, and decreased strictly. `total` was the number of words whose mask was among the submasks already visited that contain F. The counter itself never changed after Frame 1.

## Why it is correct

**Counter correctness.** A word's validity depends only on its letter set, so two words with equal masks are valid for exactly the same puzzles. Summing `cnt[m]` over valid masks `m` therefore counts valid words with their multiplicity.

**Enumeration covers exactly the valid masks.** A word mask `w` is valid for `p` exactly when `w ⊆ p` and `F ⊆ w`. The walk visits every submask of `p` exactly once. Here is why. Think of the 7 bits of `p` as a 7-bit counter whose digits are spread across 26 columns. `sub - 1` decrements the number. Bits that land outside `p` can only be the borrowed 1s below the lowest set bit of `sub`, and AND-ing with `p` clears them. The result is the largest submask of `p` that is strictly smaller than `sub`. Starting at `p` and stopping after 0, the walk lists all 2^7 submasks in decreasing order. We add `cnt[sub]` exactly when `sub` contains F. So the total is the sum over all valid masks, and masks never seen in any word contribute 0.

**Termination edge.** The loop processes `sub` before testing `sub == 0`, so the empty mask is visited once. It never contains F, so it adds nothing, but the shape of the loop matters for problems where the empty set counts.

## Cost

- Building the counter: O(W · L), where L is the word length (one OR per letter).
- Each puzzle: 7 letters to build its mask plus 128 steps of the walk with O(1) lookups. O(P · 2^7) overall.
- Total: O(W · L + P · 128), around 5 · 10^6 + 1.3 · 10^6 operations. Space O(W) for the counter.

For comparison, the brute force is O(P · W · L), and masks alone bring it to O(P · W), still 10^9.

A small speed-up: skip any word with more than 7 distinct letters while building the counter, since it can never fit a puzzle.

## Variations you will meet

- **Enumerate only with F fixed**: walk the submasks of `p ^ F`, which has 6 bits and 64 submasks, and look up `cnt[sub | F]`. This halves the loop and removes the `if`.
- **Superset counting for many queries** (count words whose mask contains a given set): use SOS DP (sum over subsets) across all 2^k masks when the alphabet is small enough, which is O(k · 2^k) for all queries at once.
- **Maximum Product of Word Lengths** (LeetCode 318): the same word-to-mask step; two words share no letters exactly when `m1 & m2 == 0`.
- **Iterating all submasks of all masks** of a k-bit universe costs 3^k in total. Remember it when a DP over subsets needs every (mask, submask) pair.

## What to carry forward

Collapse items to a mask of what they contain and tally the masks. Then enumerate submasks from the small side with `sub = (sub - 1) & p`. Here a mask said which letters were present. In the next problem a mask says which digit counts are odd, and XOR keeps it up to date as a prefix moves along a string.
