---
rank: 7
slug: longest_substring_without_repeating
---

Given a string, return the length of its longest substring in which no character appears twice. In `"abcbad"` the answer is `4`, the window `"cbad"`.

The brute force starts a scan at every index and extends it until a character repeats, `O(n²)` work. The insight is that neighboring answers overlap: when the window `s[left..right]` meets a repeat, the next valid window only has to drop the stretch up to the earlier copy, never start over. So keep one window and slide both of its edges forward. `right` advances one character per step; `left` moves only when the new character already sits inside the window, and then it jumps straight past the earlier copy, because no window that still holds both copies can be valid. A map from each character to the index of its latest occurrence makes that jump a single lookup.

Picture the window as an elastic band on the string: the right edge moves steadily, the left edge waits and then leaps. The one subtlety is a stale entry. The map still remembers characters that have already left the window, so the jump happens only when `last_seen[ch] ≥ left`; otherwise `left` would move backward and readmit a repeat. Below, the `a` at index 4 was last seen at index 0, already outside the window, so `left` stays at 2.

```text
          a b c b a d     last_seen[ch]          left  best
right 0   a               -                        0    1
right 1   a b             -                        0    2
right 2   a b c           -                        0    3
right 3       c b         1, inside: left = 2      2    3
right 4       c b a       0, left of window        2    3
right 5       c b a d     -                        2    4
```

```pseudo
FUNCTION LengthOfLongestSubstring(s)
    last_seen ← empty map                  // char → index of latest occurrence
    left ← 0
    best ← 0
    FOR right FROM 0 TO len(s) - 1
        ch ← s[right]
        IF ch IN last_seen AND last_seen[ch] ≥ left
            left ← last_seen[ch] + 1       // jump past the copy in the window
        last_seen[ch] ← right
        best ← max(best, right - left + 1)
    RETURN best
```

Each index enters the window once and `left` only moves forward, so the scan is `O(n)` time, and the map holds one entry per distinct character. Reach for a variable window whenever a problem asks for the longest contiguous stretch whose condition survives shrinking: no repeats, at most `k` distinct characters, at most `k` replacements. When the condition depends on counts rather than positions, keep a count map and advance `left` one step at a time instead of jumping, as Minimum Window Substring (#8) does. The classic mistake is dropping the `last_seen[ch] ≥ left` test: on `"abba"` the final `a` drags `left` back to index 1 and the answer comes out 3 instead of 2.

*Practice:* LC 3 Longest Substring Without Repeating Characters · LC 159 Longest Substring with At Most Two Distinct Characters · LC 340 Longest Substring with At Most K Distinct Characters · LC 424 Longest Repeating Character Replacement
