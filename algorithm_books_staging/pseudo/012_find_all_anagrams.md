---
rank: 12
slug: find_all_anagrams
---

Given lowercase strings `s` and `p`, return the start index of every substring of `s` that is an anagram of `p`: the same letters, each the same number of times, in any order. For `s = "cbaebabacd"` and `p = "abc"` the answer is `[0, 6]`, the windows `"cba"` and `"bac"`.

An anagram of `p` has exactly `len(p)` letters, so only windows of that one width can qualify. The brute force rebuilds the letter counts of each such window from scratch, `O(n · m)` for `n = len(s)` and `m = len(p)`, and more if it sorts each one instead. But neighboring windows differ only at their ends. Slide the window one step and at most two counts change: the letter entering on the right goes up by one, and the letter leaving on the left goes down by one. The 26 counts are the canonical key of Group Anagrams (#5), kept current instead of recomputed, and a window is an anagram exactly when its counts equal those of `p`.

Picture a frame of fixed width riding along the string with a tally of 26 slots attached. Both edges move in lockstep, which is what sets this window apart from the variable windows of #11 and #13, where the right edge runs ahead and the left edge follows its own rule: it jumps past a repeat in #11, and in #13 it shrinks the window for as long as the window still covers every needed letter. Each step compares two arrays of 26 counts, a constant amount of work. A counter of how many of the 26 slots currently agree removes even that: a slide touches two slots, so the counter moves by at most two per step, and the window is an anagram when all 26 agree.

```text
p = "abc", need = a1 b1 c1
start  c b a e b a b a c d    in   out   window counts   anagram?
0      └───┘                  -    -     a1 b1 c1        ✓
1        └───┘                e    c     a1 b1 e1        ✗
2          └───┘              b    b     a1 b1 e1        ✗
3            └───┘            a    a     a1 b1 e1        ✗
4              └───┘          b    e     a1 b2           ✗
5                └───┘        a    b     a2 b1           ✗
6                  └───┘      c    a     a1 b1 c1        ✓
7                    └───┘    d    b     a1 c1 d1        ✗
answer [0, 6]
```

```pseudo
FUNCTION LetterCounts(text)
    counts ← array of 26 zeros
    FOR EACH ch IN text
        slot ← ord(ch) - ord('a')          // 'a' → 0, 'b' → 1, ..., 'z' → 25
        counts[slot] ← counts[slot] + 1
    RETURN counts

FUNCTION FindAnagrams(s, p)
    m ← len(p)
    starts ← empty list
    IF m > len(s)
        RETURN starts                      // no window fits
    need ← LetterCounts(p)
    window ← LetterCounts(s[0..m-1])       // the first window
    IF window = need
        starts.append(0)                   // the first window counts too
    FOR right FROM m TO len(s) - 1
        entering ← ord(s[right]) - ord('a')
        leaving ← ord(s[right - m]) - ord('a')
        window[entering] ← window[entering] + 1      // s[right] slides in
        window[leaving] ← window[leaving] - 1        // s[right - m] slides out
        IF window = need                   // 26 slot comparisons
            starts.append(right - m + 1)
    RETURN starts
```

Building the first window costs `O(m)`, and each of the `n - m` slides costs two updates and a 26-slot comparison, so the scan is `O(26 · n)` time, linear for a fixed alphabet, with two arrays of 26 counts for space. Reach for a fixed-size window whenever a problem asks about every substring or subarray of one given length: anagrams and permutations of a pattern, or the best sum or average of `k` consecutive values. Permutation in String is the yes-or-no version of this problem and returns `true` at the first match. The classic mistake is comparing only inside the sliding loop and forgetting the very first window: on the example that loses index 0 and returns `[6]`.

*Practice:* LC 438 Find All Anagrams in a String · LC 567 Permutation in String · LC 643 Maximum Average Subarray I · LC 30 Substring with Concatenation of All Words
