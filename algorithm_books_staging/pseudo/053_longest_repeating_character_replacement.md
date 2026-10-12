---
rank: 53
slug: longest_repeating_character_replacement
---

Given a string of uppercase letters and an integer `k`, return the length of the longest substring that can be turned into one repeated letter by replacing at most `k` of its characters. For `"AABABBA"` with `k = 1` the answer is `4`: replacing the `B` in `"AABA"` gives `"AAAA"`.

The cheapest way to make a window uniform keeps its most frequent letter and replaces all the others, so a window needs exactly `length - top count` replacements, and it qualifies when that is at most `k`. The brute force tries every start with every end, `O(n²)` windows. The condition survives shrinking, since a window inside a fixable window is fixable, so the variable window of #11 applies: extend `right` one letter at a time, and while the window needs more than `k` replacements, drop `s[left]` and advance `left`. The 26 letter counts of the window update in `O(1)` per step.

The subtle part is `max_count`, the largest count any letter has reached in any window so far. When `left` moves, the true top count of the window can fall, yet `max_count` is never lowered, and it never needs to be. Once the window has slid for the first time, its length is exactly `max_count + k`, so it can grow again only when the entering letter pushes `max_count` higher, and that higher count is real, inside the current window. A stale `max_count` therefore never inflates the answer; at worst it keeps the frame sliding at its current width, as at `right = 4` and `right = 6` below, where `"ABAB"` and `"ABBA"` would really need two replacements. And because `max_count` never drops, the `while` runs at most once per step: the window either grows by one or slides by one, and its final length is the answer.

```text
k = 1; the test runs as s[right] arrives, the window is drawn after the step
right  in  max_count  length - max_count  action  window after     counts  best
  0    A       1      1 - 1 = 0           grow   [A]A B A B B A    A1       1
  1    A       2      2 - 2 = 0           grow   [A A]B A B B A    A2       2
  2    B       2      3 - 2 = 1           grow   [A A B]A B B A    A2 B1    3
  3    A       3      4 - 3 = 1           grow   [A A B A]B B A    A3 B1    4
  4    B       3      5 - 3 = 2 > 1       slide   A[A B A B]B A    A2 B2    4
  5    B       3      5 - 3 = 2 > 1       slide   A A[B A B B]A    A1 B3    4
  6    A       3      5 - 3 = 2 > 1       slide   A A B[A B B A]   A2 B2    4
right 4 and 6: ABAB and ABBA need 2 replacements; max_count 3 is stale
```

```pseudo
FUNCTION CharacterReplacement(s, k)
    count ← array of 26 zeros              // letter counts inside the window
    max_count ← 0                          // top single-letter count so far
    left ← 0
    best ← 0
    FOR right FROM 0 TO len(s) - 1
        slot ← ord(s[right]) - ord('A')
        count[slot] ← count[slot] + 1
        max_count ← max(max_count, count[slot])
        WHILE right - left + 1 - max_count > k     // too many to replace
            drop ← ord(s[left]) - ord('A')
            count[drop] ← count[drop] - 1
            left ← left + 1                // runs at most once per step
        best ← max(best, right - left + 1)
    RETURN best
```

Each index enters the window once and leaves it at most once, so the scan is `O(n)` time with 26 counts of space. Reach for this window whenever a problem asks for the longest stretch that a budget of `k` changes can make uniform: Max Consecutive Ones III is the same loop with the zeros as the letters to replace, and Maximize the Confusion of an Exam is this problem over the two letters `T` and `F`. The classic mistake is measuring the window against the count of the letter that just entered instead of the top count: on `"AAAB"` with `k = 1`, the arriving `B` shrinks the window to `"AB"`, and the answer comes out `3` instead of `4`.

*Practice:* LC 424 Longest Repeating Character Replacement · LC 1004 Max Consecutive Ones III · LC 2024 Maximize the Confusion of an Exam
