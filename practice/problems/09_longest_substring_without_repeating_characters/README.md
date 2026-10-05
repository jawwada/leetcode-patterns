# Longest Substring Without Repeating Characters (LeetCode 3)

**Area:** sliding window · **Difficulty:** Medium · **Key operations:** expand right, look up the last index of the new char, jump left past it, record the window length

## Problem

Given a string `s`, return the length of the longest substring in which no character appears twice.

## Example

```
s = "abcabcbb"  ->  3   ("abc")
s = "pwwkew"    ->  3   ("wke")
s = "bbbbb"     ->  1
```

## Brute force

For every start index `i`, extend `j` to the right while the characters stay distinct (tracked in a set), and record the longest run.

O(n²) time, O(min(n, alphabet)) space. The wasted work: when start `i` fails at position `j`, start `i + 1` rebuilds its set from scratch over `s[i+1..j-1]`, a stretch already known to be distinct.

## From brute force to optimal

Keep one window `s[left..right]` that is always duplicate-free. When the new character `s[right]` already occurs inside the window at position `p`, every window that starts at or before `p` and includes `right` is doomed, so `left` can jump straight to `p + 1`. Finding `p` must be instant, so store `last[ch]`, the most recent index of every character. The guard `last[ch] >= left` matters: an occurrence to the left of the window is stale and must not pull `left` backwards. Both edges only move right, so the whole pass is O(n).

## Intuition

Slide a window along the string. The right edge advances one character per step; the left edge only ever jumps forward, landing just past the earlier copy of the character that just arrived. Because the window never shrinks except to cut off a duplicate, at every step it is the longest duplicate-free substring ending at `right`, and the answer is the biggest window seen.

## Walkthrough

`^` marks the window `s[left..right]`; `last` is the most recent index of each character.

```
    abcabcbb
r=0 'a'                            window [0..0] 'a'    len 1 best 1   last {a:0}
    ^
r=1 'b'                            window [0..1] 'ab'   len 2 best 2   last {a:0, b:1}
    ^^
r=2 'c'                            window [0..2] 'abc'  len 3 best 3   last {a:0, b:1, c:2}
    ^^^
r=3 'a' repeats at 0 >= left 0  -> left = 1
                                   window [1..3] 'bca'  len 3 best 3   last {a:3, b:1, c:2}
     ^^^
r=4 'b' repeats at 1 >= left 1  -> left = 2
                                   window [2..4] 'cab'  len 3 best 3   last {a:3, b:4, c:2}
      ^^^
r=5 'c' repeats at 2 >= left 2  -> left = 3
                                   window [3..5] 'abc'  len 3 best 3   last {a:3, b:4, c:5}
       ^^^
r=6 'b' repeats at 4 >= left 3  -> left = 5
                                   window [5..6] 'cb'   len 2 best 3   last {a:3, b:6, c:5}
         ^^
r=7 'b' repeats at 6 >= left 5  -> left = 7
                                   window [7..7] 'b'    len 1 best 3   last {a:3, b:7, c:5}
           ^
result 3
```

The guard in action on `"abba"`: at `r=3` the `'a'` was last seen at 0, but `left` is already 2, so `0 >= 2` is false and the window stays `[2..3]`. Without the guard `left` would jump back to 1 and `"bba"` would be miscounted as length 3.

## Steps

1. `last = {}`, `left = 0`, `best = 0`.
2. For each `right`, `ch`: if `ch` is in `last` and `last[ch] >= left`, set `left = last[ch] + 1`.
3. Set `last[ch] = right`, then `best = max(best, right - left + 1)`.
4. Return `best`.

## Complexity

O(n) time: `right` moves n times and `left` only moves forward, so at most n moves in total. O(min(n, alphabet)) space for `last`.

## Pitfalls

- **Dropping the `last[ch] >= left` guard.** A stale occurrence left of the window pulls `left` backwards and re-admits duplicates: `"abba"` returns 3 instead of 2.
- **`left = last[ch]` instead of `last[ch] + 1`.** The earlier copy stays inside the window, so `"abcabcbb"` counts `"abca"` as 4.
- **Window length off by one.** `s[left..right]` has `right - left + 1` characters; `right - left` reports 0 for a one-character string.
- **Set-based shrinking that forgets to remove.** The `while s[right] in seen` variant must `seen.remove(s[left])` as `left` advances, or it never terminates.
- **Updating `last[ch]` before the check.** Then `last[ch]` is `right` itself and the window is cut to one character on every repeat.
