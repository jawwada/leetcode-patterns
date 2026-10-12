# Longest Substring Without Repeating Characters
*LeetCode 3 · Medium · Pattern: Variable-size sliding window · Reading time ~7 min*

## The problem

Given a string s, return the length of the longest substring whose characters are all distinct.

```text
Example: s = "abcabcbb" -> 3 ("abc"); s = "pwwkew" -> 3 ("wke");
  s = "bbbbb" -> 1.
```

## What the problem is really asking

Given a string, find the longest contiguous piece in which no character appears twice, and return its length. "Substring" means contiguous; "pwke" inside "pwwkew" does not count because it skips a letter.

The answer is a length. The difficulty is that there are O(n^2) substrings, and checking each for duplicates naively costs O(n) more. We need to visit far fewer of them while still being sure we did not miss the longest.

```text
s:      a   b   c   b   d   a
index:  0   1   2   3   4   5
       [a   b   c]              distinct, length 3
               [c   b   d   a]  distinct, length 4  <- answer
       [a   b   c   b]          has two b's: illegal
```

## Do it by hand first

Read the string left to right, keeping the current duplicate-free run in your head.

```text
read a   run = a        (1)
read b   run = ab       (2)
read c   run = abc      (3)
read b   b is already in the run, at position 1.
         cut everything up to and including that b:
         run = c b      (2)
read d   run = cbd      (3)
read a   is 'a' in the run "cbd"? no (the old a was cut)
         run = cbda     (4)  <- longest
```

Two things were tracked. The current run (its left end), and for each character, *where* it last appeared, so that on a repeat you knew how far to cut. That second piece of information is the seed: a map from character to last index.

## The first honest attempt

For every start `i`, extend `j` rightwards, adding characters to a fresh set, and stop at the first duplicate. Record `j - i`. That is O(n^2) time, since each set operation is O(1), and O(alphabet) space.

The waste is visible when start `i` fails and start `i+1` begins:

```text
start 0:  a b c | b      fails at index 3 (b repeats)
start 1:    b c | b      rebuilds {b, c}, fails at 3 again
start 2:      c b d a    rebuilds {c}, then continues
              ^
   starts 0 and 1 rescanned "b c" which was already
   known to be duplicate-free; start 1 was doomed anyway
```

Start 1 could never succeed past index 3, because it still contains the first `b`. The brute force does not know that and rebuilds the set to find out.

## The turning point

**Claim: if `s[L..R-1]` is duplicate-free and `s[R]` equals `s[p]` for some `p` in `[L, R-1]`, then no window that starts at or before `p` and ends at `R` or later can be legal, so `L` can jump directly to `p + 1`.**

Justification: any such window contains both index `p` and index `R`, which hold the same character. So all of those starts are dead for every future right edge. Meanwhile `s[p+1..R]` is legal: `s[p+1..R-1]` was already distinct, and the only earlier copy of `s[R]` in the old window was at `p`, which we just excluded.

To make the jump O(1) we need `p` instantly. Store `last[ch]` = the most recent index where `ch` appeared. When we read `s[R]`:

- If `s[R]` was seen and `last[s[R]] >= L`, set `L = last[s[R]] + 1`.
- Set `last[s[R]] = R`.
- Record `R - L + 1`.

The guard `last[ch] >= L` is essential. The map remembers *every* character ever seen, including ones that have already fallen out of the window. If you jump to a stale index you would move `L` backwards and reintroduce duplicates. In "abba", when the final `a` arrives, `last['a'] = 0` but `L` is already 2; the guard keeps `L` at 2. (Writing `L = max(L, last[ch] + 1)` expresses the same rule.)

There is a second, equally valid version that keeps a set and shrinks one step at a time: while `s[R]` is in the set, remove `s[L]` and advance `L`. It is still O(n) total because each character is removed at most once. The map version just does the shrink in one jump.

Compare with the previous problem. There we wanted the *shortest* qualifying window, so we recorded inside the shrink. Here we want the *longest legal* window, so we first restore legality, then record.

## Watch it work

`s = "abcbda"`. `last` shows only the characters seen so far.

Frame 1

```text
 i:   0  1  2  3  4  5
     [a  b  c] b  d  a
      L     R           last={a:0,b:1,c:2}  best=3
```

`R` walks 0 to 2 with no repeats; `L` stays at 0 and the window grows to "abc".

Frame 2

```text
 i:   0  1  2  3  4  5
      a  b [c  b] d  a
            L  R        b seen at 1 >= L=0 -> L=2
                        last={a:0,b:3,c:2}  best=3
```

`R = 3` reads `b`, last seen at 1 inside the window; `L` jumps to 2 in one step.

Frame 3

```text
 i:   0  1  2  3  4  5
      a  b [c  b  d] a
            L     R     last={a:0,b:3,c:2,d:4} best=3
```

`R = 4` reads a new `d`; the window "cbd" has length 3, tying the best.

Frame 4

```text
 i:   0  1  2  3  4  5
      a  b [c  b  d  a]
            L        R  a seen at 0 < L=2: stale, ignore
                        last={a:5,...}  best=4
```

`R = 5` reads `a`; its last index 0 is left of `L`, so no jump. Length 4 is the answer.

In every frame, the window `[L, R]` contained no repeats, and `L` was the smallest start for which that was true. `L` never moved left.

## Why it is correct

Invariant after processing `R`: `s[L..R]` is the longest duplicate-free substring that ends at `R`.

Base case: before any character, the window is empty. Step: assume it holds for `R - 1` with left edge `L`. Read `c = s[R]`. If `c` does not occur in `s[L..R-1]` (either never seen, or `last[c] < L`), then `s[L..R]` is duplicate-free, and it cannot extend further left than `L`, because `s[L-1..R-1]` already had a duplicate (or `L = 0`). If `c` does occur, its only occurrence in the window is `last[c]`, and as argued in the claim the longest legal window ending at `R` starts at `last[c] + 1`. Either way the invariant holds.

The global answer is the longest duplicate-free substring, which ends at some `R`, and we took the maximum over all `R`.

## Cost

- Time O(n): one pass; each step does a constant number of map lookups and updates.
- Space O(min(n, alphabet)): the `last` map has one key per distinct character. For ASCII you can use a fixed array of 128 integers.

The set-and-shrink version has the same O(n) bound: `R` adds each index once and `L` removes each index at most once.

## Variations you will meet

- **At most k distinct characters (LeetCode 340) / at most two (159).** The rule changes from "each count is at most 1" to "number of keys is at most k". You need counts, not last positions, because a character leaves the window only when its count hits zero. That is Fruit Into Baskets, two problems ahead.
- **Return the substring, not the length.** Remember the `L` at which `best` last improved and slice at the end.
- **Longest substring with each character at most twice.** Counts again; shrink while the new character's count exceeds 2.
- **Unicode or a huge alphabet.** The dictionary version works unchanged; the array version needs to switch to a dict.

## What to carry forward

Memory hook: for "longest legal window", restore legality first, then record; and a last-seen map lets `L` jump, provided you never let it jump backwards.

The next problem, Max Consecutive Ones III, keeps the "longest legal window" shape but the rule becomes "at most k bad items", so the summary shrinks to a single counter and the real lesson is spotting the window inside a problem about flipping bits.
