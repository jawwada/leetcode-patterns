# Minimum Window Substring (LeetCode 76)

**Area:** sliding window · **Difficulty:** Medium-Hard · **Key operations:** count what is needed, expand right and bump formed, shrink left while every count is met, record the shortest

## Problem

Given strings `s` and `t`, return the shortest substring of `s` that contains every character of `t`, with multiplicity. Return `""` if there is none.

## Example

```
s = "ADOBECODEBANC", t = "ABC"  ->  "BANC"
```

`"ADOBEC"` also covers `ABC` but is longer; `"BANC"` is the shortest window that holds one `A`, one `B` and one `C`.

## Brute force

For every start `i`, extend `j` to the right, counting letters, until the window covers `t`; record it and move to the next start.

O(n² · |t|) time, O(alphabet) space. The wasted work: start `i + 1` recounts letters that start `i` already counted, and every step rechecks the whole histogram of `t`.

## From brute force to optimal

Two observations make both edges move only forward. Once `s[left..right]` covers `t`, growing `right` keeps it covered, so a longer window with the same `left` is never worth recording: shrink `left` instead. And once shrinking `left` breaks the cover, only growing `right` can restore it. So: expand `right`; while the window covers `t`, record it and drop `s[left]`.

To make "covers `t`" an O(1) check, keep `have` (counts inside the window) and `formed`, the number of distinct letters of `t` whose count is met. `formed` goes up exactly when `have[ch]` reaches `need[ch]` and goes down exactly when `have[out]` drops below `need[out]`. The window covers `t` iff `formed == required`, the number of distinct letters in `t`.

## Intuition

The right edge races ahead until the window holds everything `t` asks for. The left edge then creeps forward, throwing out surplus letters, until it rests on a letter the window cannot spare. That is a candidate window, so record it. Then throw that letter out too, which breaks the cover, and let the right edge run again. Each candidate is the tightest window for its right edge, and the shortest of them is the answer.

## Walkthrough

`^` marks the window; `have` lists only the letters of `t`; `formed` counts letters whose need is met (required 3).

```
    ADOBECODEBANC
r=0 'A'  have {A:1 B:0 C:0} formed 1/3   window [0..0]
    ^
r=3 'B'  have {A:1 B:1 C:0} formed 2/3   window [0..3]
    ^^^^
r=5 'C'  have {A:1 B:1 C:1} formed 3/3   window [0..5] 'ADOBEC' covers t
         record 'ADOBEC' len 6 -> best
         out 'A': have A 0 < 1 -> formed 2/3   window [1..5]
     ^^^^^
r=9 'B'  have {A:0 B:2 C:1} formed 2/3   window [1..9]
     ^^^^^^^^^
r=10 'A' have {A:1 B:2 C:1} formed 3/3   window [1..10] 'DOBECODEBA' len 10, not shorter
         out 'D', 'O' (not needed)            window [3..10] still 3/3
         out 'B': have B 1, still >= 1        window [4..10] still 3/3
         out 'E'                              window [5..10] 'CODEBA' len 6, not shorter
         out 'C': have C 0 < 1 -> formed 2/3  window [6..10]
          ^^^^^
r=12 'C' have {A:1 B:1 C:1} formed 3/3   window [6..12] 'ODEBANC' len 7
         out 'O', 'D'                         window [8..12] 'EBANC' len 5 -> best
         out 'E'                              window [9..12] 'BANC'  len 4 -> best
         out 'B': have B 0 < 1 -> formed 2/3  window [10..12]
              ^^^
end: best 'BANC'
```

Between `r=5` and `r=10` the window is not a cover (formed 2/3), so `right` just grows. The two shrink runs are where the surplus `D O B E` and then `O D E` get trimmed.

## Steps

1. `need = Counter(t)`, `have = Counter()`, `formed = 0`, `required = len(need)`, `left = 0`, best = none.
2. For each `right`, `ch`: `have[ch] += 1`; if `ch` is needed and `have[ch] == need[ch]`, `formed += 1`.
3. While `formed == required`: record the window if it is shorter; drop `out = s[left]` (`have[out] -= 1`; if `out` is needed and `have[out] < need[out]`, `formed -= 1`); `left += 1`.
4. Return the best window, or `""`.

## Complexity

O(|s| + |t|) time: each pointer crosses `s` once and the cover check is O(1). O(alphabet) space for the two counters.

## Pitfalls

- **`have[ch] >= need[ch]` when bumping `formed`.** Every surplus copy bumps `formed` again, so it overshoots and the shrink loop runs past a needed letter: `s = "aab", t = "ab"` returns `"a"`. Bump only at the moment of equality.
- **`have[out] <= need[out]` when dropping.** Removing a surplus copy is treated as breaking the cover, so the surplus is never trimmed: `"aab"` / `"ab"` returns `"aab"`. Drop `formed` only when the count falls *below* the need.
- **`if` instead of `while` for the shrink.** One shrink step per expansion never tightens the window: the example returns `"ADOBEC"`.
- **Recording after the eviction.** The window must be recorded while it still covers `t`, before `s[left]` is dropped.
- **`required = len(t)`.** `formed` counts distinct letters, so `required` must be the number of distinct letters, `len(need)`.
