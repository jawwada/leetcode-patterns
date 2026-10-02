# Compare Version Numbers
*LeetCode 165 · Medium · Pattern: Two-pointer chunk parsing · Reading time ~7 min*

## What the problem is really asking

A version string is a list of numbers ("revisions") joined by dots, like `1.01` or `7.5.2.4`. To compare two versions, compare their revisions left to right **as integers**, so leading zeros mean nothing and `01` equals `1`. A version that runs out of revisions is treated as if it continued with zeros, so `1.0` equals `1.0.0`. Return −1, 0 or 1.

The answer is a three-way comparison result. The hard part is not the comparison. It is getting both quiet rules right: integers, not strings, and missing revisions count as zero.

```text
 v1:  1 . 0 1                   revisions: [1, 1]   (+0, +0 ...)
 v2:  1 . 0 0 1 . 1             revisions: [1, 1, 1]
            field 1   field 2   field 3
 v1:          1         1         0 (missing)
 v2:          1         1         1
                                  ^ first diff: v1 < v2 -> -1
```

## Do it by hand first

Compare `1.01` with `1.001.1` on paper. You line the fields up under each other. You do not write the whole field list down first. You read the first field of each ("1" and "1"), see they are equal, and move on. Second field: "01" and "001", and you mentally drop the zeros: 1 and 1, equal. Third field: the left version has nothing left, so you read a blank as 0, against 1. Stop, left is smaller.

```text
 field:     #1      #2       #3
 v1:        1   .   01       (blank = 0)
 v2:        1   .   001  .   1
 compare:   1=1     1=1      0<1  -> stop, answer -1
```

Your hand kept track of **where you were in each string** and **the number of the current field**, built digit by digit. That is two positions and two small integers.

## The first honest attempt

Split both on `.`, convert every piece to `int`, pad the shorter list with zeros, and compare the lists element by element (Python can compare lists directly).

```text
 "1.01"    -> ["1", "01"]       -> [1, 1]    -> pad [1, 1, 0]
 "1.001.1" -> ["1", "001", "1"] -> [1, 1, 1]
 compare lists [1, 1, 0] < [1, 1, 1]          -> -1
```

This is O(n + m) time and it is fine, so say it first. The waste is in materialising everything. You build two lists of substrings and two lists of ints, and pad one with zeros, all before the first comparison. Then the comparison often decides on the very first field. With versions like `2.<ten thousand fields>` against `1.<ten thousand fields>`, you parse twenty thousand fields to use one.

```text
 v1:  [2][x][x][x] ... [x]      <- all parsed
 v2:  [1][x][x][x] ... [x]      <- all parsed
       ^ decided here; everything right of it was wasted
```

## The turning point

**Each revision can be parsed, compared, and forgotten before the next one is read, and an exhausted string naturally parses as 0.**

The comparison is lexicographic over fields: the first unequal field decides, and later fields never matter once one has. So there is no reason to hold more than one field from each string at a time. Keep an index `i` into `v1` and `j` into `v2`. To read a field, accumulate `x = x*10 + digit` while the character is not a dot and the index is in range. Then compare the two numbers. If they differ, return. If they are equal, step both indices past the dot and repeat while either string still has characters.

The "missing revision is 0" rule comes for free. When `v1` is exhausted, `i ≥ len(v1)`, the inner digit loop does not run, and `x` stays at its starting value of 0. Stepping `i += 1` past the end does no harm, because the loop guard `i < n` keeps failing. Leading zeros vanish because `0*10 + 0 + … + 1` is just 1.

This is the lockstep two-pointer pattern: two pointers on two different strings that advance in rounds (one field each per round), rather than one per character.

## Watch it work

`v1 = "1.01"` (n = 4), `v2 = "1.001.1"` (m = 7).

**Frame 1.** Round 1. `i` parses "1" and stops at the dot (index 1). `j` does the same. x = 1, y = 1, equal.
```text
 v1:  1 . 0 1          v2:  1 . 0 0 1 . 1
        ^ i=1                 ^ j=1
 x = 1                  y = 1        equal -> skip dots
```

**Frame 2.** Round 2. `i` reads "01" (x: 0 → 1) and runs off the end at i = 4. `j` reads "001" (y: 0 → 0 → 1) and stops at the dot at j = 5.
```text
 v1:  1 . 0 1          v2:  1 . 0 0 1 . 1
              ^ i=4                   ^ j=5
 x = 1                  y = 1        equal -> i=5, j=6
```

**Frame 3.** Round 3. `i = 5 ≥ n`, so v1 contributes x = 0. `j` reads "1", so y = 1.
```text
 v1:  1 . 0 1  (empty)  v2:  1 . 0 0 1 . 1
                 ^ i=5                     ^ j=7
 x = 0                  y = 1        0 < 1 -> return -1
```

Before every round, both pointers sat at the start of a field (or past the end), and every earlier field pair had compared equal. Within a round, `x` and `y` were the integer value of the digits consumed so far in the current field.

## Why it is correct

Invariant at the top of each round: all previous field pairs, with missing fields read as 0, were equal, and `i` and `j` point at the first character of the next field in each string, or beyond the end. The digit loops consume exactly one field each and leave the pointer on the dot or at the end. `x` is then that field's integer value, or 0 if the string is exhausted, which is the problem's padding rule. If `x ≠ y`, this is the first differing field, and lexicographic comparison says it decides. If they are equal, the `+= 1` steps past the dot and restores the invariant. The loop ends when both strings are exhausted, at which point every field pair was equal and the answer is 0.

## Cost

- **Time O(n + m)**: each character is read once by its digit loop. The comparison may stop much earlier.
- **Space O(1)**: two indices and two accumulators, with no substrings or lists.
- The split-and-pad version is O(n + m) time and O(n + m) space.

## Variations you will meet

- **Revisions too large for a machine integer** (other languages). Do not accumulate. Skip leading zeros, then compare the remaining digit runs by length first and lexicographically second. A longer run of significant digits is the bigger number.
- **Semantic Versioning with pre-release tags** (`1.0.0-alpha.1`). Fields become mixed numeric and alphanumeric, with special ordering rules. It is the same lockstep walk with a richer field comparator.
- **Sorting a list of versions.** Turn each version into a key: a tuple of ints with trailing zeros stripped, so that `1.0` and `1` give equal keys. This is a canonical-form idea from Valid Anagram, applied here.
- **"Return how far apart they are."** You need the first differing index and both values, which is exactly where the loop exits.

## What to carry forward

Lockstep pointers over two strings, parsing one field at a time, with "exhausted means zero" falling out of the loop guards. Compare as numbers, not text. The next problem parses a single number but adds phases (spaces, sign, digits) and a hard 32-bit wall that must be checked while the number is still being built.
