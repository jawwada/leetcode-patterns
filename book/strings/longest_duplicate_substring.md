# Longest Duplicate Substring

*LeetCode 1044 · Hard · Pattern: Binary search on the answer + rolling hash · Reading time ~11 min*

## The problem

Given a string s of lowercase letters, return any duplicated substring of maximum length, where a duplicated substring
occurs two or more times and occurrences may overlap; return "" if there is none.

```text
Example: s = "banana" -> "ana" (at indices 1 and 3). s = "abcd"
  -> "".
```

## What the problem is really asking

Given a string `s` of lowercase letters, return a longest substring that occurs at least twice. The two occurrences may overlap. If no substring repeats, return `""`.

The answer is a substring, described by a start and a length. The length is the real unknown; once you know the best length `L`, any repeated window of that length will do. What makes it hard is the size: `n` up to `3 * 10^4`. There are about `n^2 / 2` substrings, and comparing two of them costs up to `L`, so anything that touches substrings character by character, for every length, is far too slow.

```text
 s = b a n a n a
     0 1 2 3 4 5
       [a n a]          start 1
           [a n a]      start 3   (overlap is allowed)

 length 3 repeats ("ana"); no length-4 window repeats
 -> answer "ana"
```

## Do it by hand first

By hand, you would probably pick a length and look for a repeat. Length 1 in `"banana"`: `a` repeats, obviously. Length 2: `an` at 1 and 3. Length 3: `ban`, `ana`, `nan`, `ana`, and there is the repeat. Length 4: `bana`, `anan`, `nana`: all different. Length 5 cannot do better if 4 failed, because a repeated 5-window would contain a repeated 4-window.

```text
 L:      1     2     3     4     5
 repeat? yes   yes   yes   no    no
         T     T     T     F     F    <- monotone
```

Two things your hand tracked. First, a yes/no question per length, and the answers go `T T T F F`, switching only once. Second, for one fixed length, a bag of windows seen so far, checking each new window against the bag. Those two habits are the two halves of the solution.

## The first honest attempt

For `L` from `n - 1` down to 1, slide a window of length `L`, put each window string into a set, and stop at the first window already in the set.

```text
 L=5: "banan" "anana"           set, no repeat
 L=4: "bana" "anan" "nana"      set, no repeat
 L=3: "ban" "ana" "nan" "ana"   repeat!
      each window: slice L chars + hash L chars
```

Cost: up to `n` lengths, `n` windows each, `O(L)` per window to slice and hash. That is `O(n^3)` in the worst case and `O(n^2)` memory for the strings in the set. Two separate wastes:

1. We try lengths one by one, although the yes/no answers are monotone.
2. For a fixed `L`, each window is hashed from scratch, although neighbouring windows share `L - 1` characters.

```text
 b [a n a] n a
   [a n] shared with the next window
 b a [n a n] a
     [n a]  shared again
```

## The turning point

Two observations, one for each waste.

**Claim 1: if some substring of length `L` repeats, then some substring of every shorter length repeats.** Take the two occurrences of the length-`L` string and chop the last character off both: they are still equal, still at two different starts. So the predicate "a repeat of length `L` exists" is monotone: true up to some `L*`, false after. Binary search finds `L*` with `O(log n)` checks instead of `n`. Keep `lo = 1`, `hi = n - 1`; check `mid`; if a repeat exists, record it and search right (`lo = mid + 1`), else search left (`hi = mid - 1`).

**Claim 2: the hash of the next window can be computed from the hash of the current window in `O(1)`.** This is the **rolling hash** (Rabin-Karp). You have not seen it before, so build it from something familiar.

Read a window of digits as a number. In `"31415"`, the length-3 windows are the numbers 314, 141, 415. To move from 314 to 141, you do not reread the digits. You drop the leading 3 (subtract `3 * 100`), shift left (multiply by 10), and append the new digit 1:

```text
 window 314 -> 141:
   314 * 10       = 3140     shift everything left
   - 3 * 1000     = 140      drop the digit that fell off
   + 1            = 141      add the new digit

 window 141 -> 415:
   1410 - 1*1000 + 5 = 415
```

Written as one formula, with base `B` and window length `L`:

```text
 h_next = h * B - out * B^L + in
```

Here `out` is the character leaving on the left and `in` the one entering on the right. Multiplying first and then subtracting `out * B^L` is the same as subtracting `out * B^(L-1)` and then multiplying; the code does the first form. Strings work the same way once each letter is a digit: `a=1, b=2, ..., z=26`, and the base must exceed the largest digit so different strings give different numbers. The solution uses `B = 257`.

Two strings of length `L` are equal exactly when their numbers are equal. But the numbers have `L` digits in base 257, far too big. So we keep them modulo a large prime `M` (the code uses `2^61 - 1`). Equal strings still have equal hashes. Different strings almost always have different hashes, but not always: two different windows may collide. So a hash match is only a candidate, and we confirm it by comparing the actual characters. With a 61-bit modulus collisions are so rare that this check almost never runs on a false candidate, so it costs nearly nothing, but it makes the answer exact.

Now the check for one length `L` is: hash the first window directly; then roll across the string; keep a dictionary from hash to list of start positions; on each new window, if its hash is in the dictionary and one of the stored starts has the same characters, a repeat exists. That is `O(n)` per check, expected.

```text
 check(L):                    binary search over L:
   h = hash(s[0:L])           lo=1 ............ hi=n-1
   seen = {h: [0]}               T T T T F F F F
   for i in 1..n-L:                    ^ find last T
     roll h one step              each probe = check(mid)
     if h in seen and
        a stored start matches:
          return i
     add i under h
   return -1
```

## Watch it work

`s = "banana"`, codes `b=2, a=1, n=14`, `B = 257`. The numbers below stay smaller than the modulus, so they are the exact values the code computes. Useful powers: `257^2 = 66049`, `257^3 = 16974593`.

Frame 1. Binary search starts. `lo = 1`, `hi = 5`, so `mid = 3`.

```text
 lengths   1  2  3  4  5
           lo    ^mid   hi
 check(3)
```

Frame 2. `check(3)`: hash the first window directly.

```text
 b a n a n a
 [b a n]   h = 2*66049 + 1*257 + 14 = 132369
 seen = {132369: [0]}
 power = 257^3 = 16974593
```

Frame 3. Roll to start 1 and start 2.

```text
 i=1 [a n a]: 132369*257 - 2*16974593 + 1 = 69648
 i=2 [n a n]: 69648*257  - 1*16974593 + 14 = 924957
 seen = {132369:[0], 69648:[1], 924957:[2]}
```

Each new hash cost one multiply, one subtract, one add, no matter how long the window is.

Frame 4. Roll to start 3: the hash is already in the bag.

```text
 i=3 [a n a]: 924957*257 - 14*16974593 + 1 = 69648
 69648 in seen -> starts [1]
 verify s[1:4] "ana" == s[3:6] "ana"   yes
 check(3) returns 3   -> record (start 3, len 3)
 lo = 4
```

The character check confirms it is a true repeat, not a collision.

Frame 5. `lo = 4`, `hi = 5`, `mid = 4`: `check(4)`.

```text
 [b a n a]  34018834
 [a n a n]  17899550
 [n a n a]  237713950
 all distinct -> check(4) returns -1
 hi = 3
```

Frame 6. `lo = 4 > hi = 3`: the search ends.

```text
 best = (start 3, len 3)
 return s[3:6] = "ana"
```

Only two lengths were ever checked. Throughout, the invariant held: every length below `lo` was known feasible (with a recorded witness for the largest), every length above `hi` was known infeasible.

## Why it is correct

Binary search: the predicate `P(L)` = "some length-`L` substring occurs twice" is monotone by Claim 1 (true for `L` implies true for `L - 1`), and `P(n)` is false since a string has only one window of length `n`. The loop maintains: `P` is true for every `L < lo` that we have recorded, and false for every `L > hi`. Each probe shrinks `[lo, hi]` while preserving that. When the interval is empty, `lo - 1` is the largest true length, and `best` holds a witness for it (or nothing, if no length was true, so we return `""`).

Each check: rolling preserves the invariant "`h` equals the hash of `s[i:i+L]`", by the shift-drop-add identity applied modulo `M`. If two windows are equal, their hashes are equal, so the second one finds the first in `seen` and the character comparison succeeds: no repeat is missed. If the check returns `i`, the character comparison proved a real repeat: no false positive is possible. Collisions only cost time, never correctness.

## Cost

- Time `O(n log n)` expected: `O(log n)` binary-search probes, each an `O(n)` rolling scan with `O(1)` dictionary operations; the verification slice runs essentially only on true repeats.
- Space `O(n)`: the dictionary holds at most `n` hashes.

The brute force was `O(n^3)` time. A suffix array with an LCP array solves it deterministically in `O(n log n)` (the answer is the maximum LCP of adjacent suffixes), but it is much longer to write.

## Variations you will meet

- **Repeated DNA Sequences (LeetCode 187).** The length is fixed at 10, so there is no binary search, just the rolling hash (or a 20-bit encoding of the window) and a set.
- **Longest Common Substring of two strings.** Same binary search; for a given `L`, put all window hashes of the first string in a set and look up the second string's windows.
- **Longest substring occurring at least `k` times.** Count occurrences per hash instead of stopping at two; monotonicity still holds.
- **Longest repeat without overlap.** Non-overlapping repeats need the stored start to satisfy `i - j >= L`; monotonicity still holds because shortening keeps the starts far enough apart.

## What to carry forward

When the question is "the longest X", check whether "an X of length `L` exists" is monotone, and binary search on `L`; when each check slides a window over a string, roll a hash so each step is `O(1)` and verify matches to stay exact. This closes the strings chapter: you started by splitting and comparing characters one at a time, and you end by treating windows as numbers, the idea behind most fast string matching.
