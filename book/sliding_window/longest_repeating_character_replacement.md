# Longest Repeating Character Replacement
*LeetCode 424 · Medium · Pattern: Variable-size sliding window · Reading time ~8 min*

## The problem

Given an uppercase string s and an integer k, you may change at most k characters. Return the length of the longest
substring that can be turned into a single repeated letter.

```text
Example: s = "AABABBA", k = 1 -> 4 (change one letter to get
  "AAAA" or "BBBB").
```

## What the problem is really asking

You get a string of uppercase letters and a budget `k`. You may overwrite at most `k` characters with any letters you like. What is the longest substring you can make that consists of one letter repeated?

As in Max Consecutive Ones III, the story about *which* characters to change hides a window question. Take any substring. The cheapest way to make it uniform is to keep its most frequent letter and overwrite everything else. So a substring is achievable exactly when

```text
length - (count of its most frequent letter) <= k
```

The answer is the length of the longest substring passing that test. The new difficulty is that "most frequent letter in the window" is not something a simple counter tracks: it can go down when a letter leaves on the left, and finding the new maximum seems to need a scan.

```text
s = "AABABBA", k = 1
index:  0  1  2  3  4  5  6
        A  A  B  A  B  B  A
       [A  A  B  A]            A x3, B x1: change 1 -> AAAA
                [A  B  B]      B x2, A x1: change 1 -> BBB
             [B  A  B  B]      B x3, A x1: change 1 -> BBBB
answer 4
```

## Do it by hand first

Slide over "AABABBA" with `k = 1`, keeping a tally and asking "how many letters are *not* the majority?"

```text
A        tally A1        len 1  minority 0  ok
AA       tally A2        len 2  minority 0  ok
AAB      tally A2 B1     len 3  minority 1  ok
AABA     tally A3 B1     len 4  minority 1  ok   <- 4
AABAB    tally A3 B2     len 5  minority 2  too many
```

At this point you might shrink until legal again. But stop and think as the hand does: we already own a length-4 answer. Any window of length 4 or less is useless to us. The only thing worth checking from now on is whether some window of length **5** is legal. So instead of shrinking, just slide the length-4 frame forward and keep asking whether it can grow.

Your hand tracked a 26-slot tally and the size of the tallest bar. And it noticed the frame never needs to get smaller.

## The first honest attempt

For every start `i`, extend `j`, update a 26-letter tally, and test `(j - i + 1) - max(tally) <= k`. That is O(26 · n^2) time and O(26) space.

Two kinds of waste:

```text
start 0:  A A B A B ...     tally rebuilt from zero
start 1:    A B A B ...     tally rebuilt from zero
              ^^^^^ same letters counted again

each step: max(tally) scans 26 slots
           A:3 B:2 C:0 D:0 ... Z:0
```

The tally for start `i+1` is the tally for start `i` minus one letter, and the maximum over 26 slots is recomputed although at most one slot changed.

## The turning point

There are two observations here; the second is what makes this problem famous.

**Observation 1: legality is monotone under shrinking, so the usual two-pointer window applies.** Dropping a letter from the left lowers the length by 1 and lowers the max count by at most 1, so `length - max` never increases. Sub-windows of legal windows are legal.

With that alone you can write: expand `R`, and while `length - max(count) > k`, drop `s[L]`. It is correct and O(26 · n). Fine, but there is a cleaner version.

**Observation 2 (the claim): `max_freq` never needs to decrease, and the window never needs to shrink. Keep the record-high count ever seen, and when the window is illegal, slide it one step instead of shrinking it.**

Why is a stale, too-large `max_freq` harmless? Because we only care about beating the best length found so far. The window width only ever increases or stays the same. For the width to *increase* from `W` to `W + 1`, we need `W + 1 - max_freq <= k`, which means `max_freq >= W + 1 - k`. Once the window has had to slide for the first time, its width is exactly `max_freq + k`, so growing again requires `max_freq` itself to go up. And `max_freq` goes up only when the letter just added reaches a new record count, which is a real count inside the current window. So whenever the window grows, it truly is legal. When `max_freq` is stale, the worst that happens is that we keep sliding a window that is temporarily illegal, but its width equals a width we already proved achievable, so it cannot corrupt the answer.

```text
max_freq stale = 3
window "ABBA": true max 2, 2 minority > k=1  (illegal)
but width 4 was already achieved by "AABA" earlier;
the window just slides at width 4 until a letter
reaches count 4, which would justify width 5.
```

So the loop body is:

- Add `s[R]` to `count`; `max_freq = max(max_freq, count[s[R]])`.
- If `(R - L + 1) - max_freq > k`: drop `s[L]`, advance `L` (once, an `if`, not a `while`).
- `best = max(best, R - L + 1)`; in fact `best` is just the final width.

This is the same non-shrinking window you met at the end of Max Consecutive Ones III, now pulling its weight: it avoids ever recomputing a maximum.

## Watch it work

`s = "AABABBA"`, `k = 1`. `mf` is `max_freq`.

Frame 1

```text
 i:   0  1  2  3  4  5  6
     [A  A  B  A] B  B  A
      L        R            A3 B1  mf=3  4-3=1 ok  best=4
```

`R` walks 0 to 3 without any slide; "AABA" needs one change.

Frame 2

```text
 i:   0  1  2  3  4  5  6
      A [A  B  A  B] B  A
         L        R         A2 B2  mf=3  best=4
```

`R = 4` adds B: width 5, `5 - 3 = 2 > 1`, so slide once; the A at index 0 leaves. `mf` stays 3 although no letter now has count 3.

Frame 3

```text
 i:   0  1  2  3  4  5  6
      A  A [B  A  B  B] A
            L        R      A1 B3  mf=3  best=4
```

`R = 5` adds B, giving B a count of 3 (equal to `mf`, not above it). Width 5 still fails, so slide; window "BABB" is legal.

Frame 4

```text
 i:   0  1  2  3  4  5  6
      A  A  B [A  B  B  A]
               L        R   A2 B2  mf=3 (stale)  best=4
```

`R = 6` adds A; width 5 fails, slide. "ABBA" is actually illegal (true max 2), but width 4 was already earned, so the answer stays 4.

Across all frames the window width never decreased, it increased only on steps where the new letter's count set a record, and from frame 2 on the width stayed at `mf + k = 4`.

## Why it is correct

Two directions.

*The answer is never too large.* Before the first slide, the window is a prefix and `max_freq` is its true maximum, so every width recorded is legal. After the first slide, width equals `max_freq + k`, and it grows only when `max_freq` grows, which only happens when `count[s[R]]` in the current window sets a record. At that moment the window has a letter with count `max_freq`, so it is legal. Hence every width that becomes `best` was realised by a legal window.

*The answer is never too small.* Take an optimal window `[a, b]`. Every count in the current window is at most `max_freq`, because each count was at most the record when it was last raised and only decreases afterwards. Suppose `L` were pushed past `a` at some step `R' <= b`. Then the window at that moment was `[a, R']`, a sub-window of the optimal one, hence legal: its length minus its true maximum is at most `k`, and replacing the true maximum by the larger `max_freq` only makes the test easier to pass. So no slide would happen, a contradiction. Thus at step `b` we have `L <= a`, and the width is at least `b - a + 1`.

## Cost

- Time O(n): each step is O(1); there is no 26-slot scan and no inner loop.
- Space O(1): a 26-integer array (O(alphabet) in general).

The shrinking version with `max(count)` per step is O(26 · n) time, also linear for a fixed alphabet. Both are accepted; the non-shrinking one is the version to understand.

## Variations you will meet

- **Max Consecutive Ones III.** The same problem over a two-letter alphabet where only 0s may be changed. There "majority" is fixed to 1, so a zero counter suffices.
- **Return the actual substring.** Record `L` when the width last increased.
- **Lowercase or arbitrary alphabet.** Use a dictionary; the stale-maximum argument does not depend on the alphabet size.
- **Per-letter answer.** If you must say which letter is repeated, run the simple "at most k non-c letters" window once per letter c. That is 26 passes of the Ones III loop, often easier to explain in an interview.

## What to carry forward

Memory hook: when only the maximum length matters, the window may slide instead of shrinking, and a summary that is stale in the "too optimistic" direction cannot spoil the answer.

The next problem, Permutation in String, freezes the window's width from the start: we compare a fixed-length frame's letter counts against a target's, and the new idea is tracking how many letters already match so the comparison costs O(1).
