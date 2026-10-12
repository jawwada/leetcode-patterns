---
rank: 13
slug: minimum_window_substring
---

Given strings `s` and `t`, return the shortest substring of `s` that contains every character of `t`, repeats included, or `""` if there is none. For `s = "ADOBECODEBANC"` and `t = "ABC"` the answer is `"BANC"`.

The brute force tests every substring against the counts of `t`, `O(n²)` windows before any checking. The insight is that the windows worth testing form a chain. For each right end only the shortest covering window that ends there matters, and as the right end moves forward, the left end of that window never moves back. So one window slides with two edges: `right` expands until the window covers `t`, then `left` shrinks it for as long as it still covers `t`, recording each covering window on the way. The first character whose loss breaks the cover hands control back to `right`. Unlike the jumping left edge of #11, `left` here advances one step at a time, because coverage depends on counts rather than positions.

Re-checking the cover at every step would cost a loop over the characters of `t`, so the window keeps two pieces of bookkeeping. `need[ch]` is how many more copies of `ch` the window lacks, and it goes negative when the window holds spares. `missing` counts the characters of `t` still uncovered, repeats included, and drops only when an arriving character fills a real gap, that is, when its `need` was positive. The window covers `t` exactly when `missing = 0`, a constant-time test.

```text
                 A D O B E C O D E B A N C     t = "ABC"
right  5 covers  └─────────┘                 ADOBEC
        shrinks  └─────────┘                 ADOBEC  best ADOBEC
right 10 covers    └─────────────────┘       DOBECODEBA
        shrinks            └─────────┘       CODEBA  best ADOBEC
right 12 covers              └───────────┘   ODEBANC
        shrinks                    └─────┘   BANC    best BANC
```

```pseudo
FUNCTION CharCounts(text)
    counts ← empty map
    FOR EACH ch IN text
        counts[ch] ← counts.get(ch, 0) + 1
    RETURN counts

FUNCTION MinWindow(s, t)
    IF len(t) = 0
        RETURN ""                          // nothing to cover
    need ← CharCounts(t)                   // char → copies the window lacks
    missing ← len(t)                       // chars of t not yet covered
    left ← 0
    best_start ← 0
    best_len ← len(s) + 1                  // longer than any real window
    FOR right FROM 0 TO len(s) - 1
        ch ← s[right]
        IF need.get(ch, 0) > 0
            missing ← missing - 1          // this copy fills a real gap
        need[ch] ← need.get(ch, 0) - 1     // below zero: a spare copy
        WHILE missing = 0                  // covers t: record, then shrink
            IF right - left + 1 < best_len
                best_start ← left
                best_len ← right - left + 1
            drop ← s[left]
            need[drop] ← need[drop] + 1
            IF need[drop] > 0
                missing ← missing + 1      // dropped a copy the window needed
            left ← left + 1
    IF best_len > len(s)
        RETURN ""                          // no window ever covered t
    RETURN s[best_start..best_start + best_len - 1]
```

Each index enters the window once and leaves it at most once, so the work is `O(len(s) + len(t))` time, and the map holds one count per distinct character. Reach for expand-right, shrink-left whenever a problem asks for the shortest window that contains something; with the width pinned to `len(t)`, the same counts find every permutation or anagram of a pattern inside a string. The classic mistake is decrementing `missing` for every arriving character of `t`, spares included: with `s = "AAB"` and `t = "AB"`, the second `A` claims the slot meant for `B`, `missing` reaches 0 on `"AA"`, and the answer comes back without a `B`.

*Practice:* LC 76 Minimum Window Substring · LC 567 Permutation in String · LC 438 Find All Anagrams in a String · LC 30 Substring with Concatenation of All Words
