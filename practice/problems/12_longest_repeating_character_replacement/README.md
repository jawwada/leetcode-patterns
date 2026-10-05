# Longest Repeating Character Replacement (LeetCode 424)

**Area:** sliding window · **Difficulty:** Medium · **Key operations:** count the new char, track the max count, shrink while len - max_freq > k, record the window length

## Problem

Given an uppercase string `s` and an integer `k`, you may change at most `k` characters. Return the length of the longest substring that can be turned into a single repeated letter.

## Example

```
s = "AABABBA", k = 1  ->  4

A A B A B B A
      [A B B A]  change the A at index 3 -> "BBBB"
```

## Brute force

For every start `i`, extend `j` to the right keeping a count of the letters in `s[i..j]`. The window can be made uniform iff `(j - i + 1) - max(count) <= k`: keep the majority letter, change the rest.

O(n² · 26) time, O(26) space. The wasted work: every start recounts the stretch the previous start just counted, and every step rescans the 26 bins for the maximum.

## From brute force to optimal

The validity test `len - max_freq <= k` says the non-majority letters are the ones you change. Adding a character can only raise `len - max_freq` by 1 and dropping one can only lower it, so a sliding window works: expand `right`, and while the window needs more than `k` changes, shrink `left`.

The subtle point is `max_freq`. It would be natural to recompute it when `left` moves, but it never needs to decrease. A smaller `max_freq` only makes the test stricter, which can only produce a window *shorter* than one you already recorded with the larger value, and you are after the maximum. So `max_freq` is simply the largest count ever seen, and the window effectively slides at its best size, growing only when a new majority appears.

## Intuition

Inside the window picture a bar chart of letter counts. The tallest bar is the letter you keep; everything else is a change you must spend. Grow the window while the changes fit in `k`. When they do not, slide the window one step instead of shrinking it: a shorter window can never beat a length you have already achieved, so there is no point going back.

## Walkthrough

`^` marks the window; `needs` is `len - max_freq`, the number of changes required.

```
    AABABBA   k=1
r=0 'A'  count {A:1}      max_freq 1  len 1 needs 0        best 1
    ^
r=1 'A'  count {A:2}      max_freq 2  len 2 needs 0        best 2
    ^^
r=2 'B'  count {A:2 B:1}  max_freq 2  len 3 needs 1 <= 1   best 3
    ^^^
r=3 'A'  count {A:3 B:1}  max_freq 3  len 4 needs 1 <= 1   best 4
    ^^^^
r=4 'B'  count {A:3 B:2}  max_freq 3  len 5 needs 2 > 1    -> out 'A', left 1   count {A:2 B:2}
     ^^^^                                                     window 'ABAB' len 4   best 4
r=5 'B'  count {A:2 B:3}  max_freq 3  len 5 needs 2 > 1    -> out 'A', left 2   count {A:1 B:3}
      ^^^^                                                    window 'BABB' len 4   best 4
r=6 'A'  count {A:2 B:3}  max_freq 3  len 5 needs 2 > 1    -> out 'B', left 3   count {A:2 B:2}
       ^^^^                                                   window 'ABBA' len 4   best 4
result 4
```

From `r=4` on the window is stuck at size 4 and slides: `max_freq` stays 3 even at `r=6` where the real maximum inside `"ABBA"` is 2. That stale value cannot hurt, because a window of size 4 was already recorded.

## Steps

1. `count = {}`, `left = max_freq = best = 0`.
2. For each `right`, `ch`: `count[ch] += 1`, `max_freq = max(max_freq, count[ch])`.
3. While `(right - left + 1) - max_freq > k`: `count[s[left]] -= 1`, `left += 1`.
4. `best = max(best, right - left + 1)`.
5. Return `best`.

## Complexity

O(n) time: each index enters the window once and leaves at most once. O(26) space for the counts.

## Pitfalls

- **`>= k` in the shrink condition.** A window that needs exactly `k` changes is valid. With `>=` the window is shrunk as soon as it needs `k`, so the example returns 2.
- **`max_freq = count[ch]`.** Setting it to the newest letter's count forgets the real majority: `"AAAAB"` with `k = 1` shrinks on the `B` and returns 4 instead of 5.
- **Dropping the `+ 1` from the window length.** Under-counting the length lets windows that need `k + 1` changes pass: `"ABCDE"` with `k = 1` returns 3.
- **Recomputing `max_freq` after shrinking.** Correct but needless: a lower `max_freq` can only produce shorter windows than the one already recorded.
- **Counting the wrong letter on shrink.** The letter leaving is `s[left]`, not `ch`.
