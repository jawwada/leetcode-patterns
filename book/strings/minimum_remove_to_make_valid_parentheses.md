# Minimum Remove to Make Valid Parentheses
*LeetCode 1249 · Medium · Pattern: Stack matching · Reading time ~8 min*

## The problem

Given a string of lowercase letters and parentheses, remove the minimum number of parentheses so the result is valid,
and return any such result.

```text
Example: "lee(t(c)o)de)" -> "lee(t(c)o)de"; "a)b(c)d" ->
  "ab(c)d"; "))((" -> "".
```

## What the problem is really asking

The string has lowercase letters and the characters `(` and `)`. Delete as few parentheses as possible so that the rest is balanced: every `)` closes an earlier `(`, and every `(` is eventually closed. Letters stay. Return any one valid result. The answer is a string, a subsequence of the input that keeps every letter.

The interesting part is "minimum". You might worry that you have to choose cleverly which parentheses to cut. It turns out there is no choice to make. Some characters are unmatchable no matter what, and deleting exactly those is both necessary and sufficient.

```text
 s:      a  )  b  (  c  (  d  )
 index:  0  1  2  3  4  5  6  7
 pairs:                 [5----7]
 orphans:   ^        ^              ) at 1 has no opener
                                    ( at 3 is never closed
 answer: a b c ( d )  = "abc(d)"
```

## Do it by hand first

Read `"a)b(c(d)"` left to right and count open parentheses on your fingers. `a`: nothing. `)`: you have zero fingers up, so nothing can match it and it is doomed. Cross it out. `b`: nothing. `(`: one finger. `c`: nothing. `(`: two fingers. `d`. `)`: put a finger down, matched. End of string: one finger still up, so one `(` was never closed. Which one? The one whose partner never came. In this string that is the earlier `(` at index 3, because the `(` at 5 was taken by the `)` at 7.

```text
 char:    a  )  b  (  c  (  d  )
 open:    0  X  0  1  1  2  2  1     X = would go negative: cut
 end: 1 opener left over -> cut it (index 3)
```

Counting fingers tells you *how many* openers are left. To know *which* ones to cut, your hand also had to remember **where each open `(` was**. A list of positions that you add to and take from at the end is a stack of indices.

## The first honest attempt

Scan with a depth counter. When depth would go negative, that `)` is bad, so delete it from the string and restart the scan from the beginning. Repeat until no `)` drives the depth negative. Then do the mirror image from the right to remove unclosed `(`.

```text
 "a)b(c(d)"   scan: ')' at 1 drives depth to -1 -> delete
 "ab(c(d)"    rescan from 0 ... no negative depth
 reverse & mirror: ")d(c(ba"  treat ')' as opener
              '(' at index 4 (orig 3) goes negative -> delete
 result "abc(d)"
```

Each deletion rebuilds the string in O(n) and restarts a scan of O(n), so with many bad characters it is O(n²). The repeated work is the restart. After deleting the bad `)` at position 1, the prefix `a` is rescanned, although its depth profile has not changed. With a string like `")))))…((((("`, every deletion re-walks the same prefix again.

## The turning point

**A `)` is unmatchable exactly when no `(` is open at that moment, and a `(` is unmatchable exactly when it is still open at the end. Both facts can be read off one left-to-right pass that keeps a stack of open `(` indices.**

Justification for the first half: if a `)` arrives while the stack is empty, every `(` to its left is already paired with a later `)` that came before this one, so in any balanced subsequence this `)` has no partner and must go. If the stack is non-empty, pairing it with the most recent open `(` is always safe. Nesting guarantees that the most recent opener is the one a valid matching uses.

Second half: whatever indices remain on the stack at the end are openers that no `)` after them could take. Each must be deleted, and deleting them leaves the matched pairs intact.

Minimality: every deleted character was individually unmatchable, so any valid result must delete at least that many. We delete exactly that many.

Implementation detail that matters: **do not delete during the scan**. Deleting shifts every later index and breaks the indices stored on the stack. Instead, work on `chars = list(s)` and *mark* a character for deletion by overwriting it with `""`. At the end, `"".join(chars)` drops the marks in one O(n) step.

```text
 chars:  [a][)][b][(][c][(][d][)]
 mark:      ""       ""
 join:   a  b  c  (  d  )
```

## Watch it work

`s = "a)b(c(d)"`, indices 0–7.

**Frame 1.** `a` is a letter, so it is ignored. `)` at 1 arrives with an empty stack, so it is unmatched. Mark it.
```text
 a  )  b  (  c  (  d  )
    ^ i=1
 chars: a "" b ( c ( d )
 stack: []
```

**Frame 2.** `b` is ignored. `(` at 3 is pushed.
```text
 a  )  b  (  c  (  d  )
          ^ i=3
 stack: [3]
```

**Frame 3.** `c` is ignored. `(` at 5 is pushed.
```text
 a  )  b  (  c  (  d  )
                ^ i=5
 stack: [3, 5]
```

**Frame 4.** `d` is ignored. `)` at 7 pops 5, so the pair is (5, 7).
```text
 a  )  b  (  c  (  d  )
                [-----]
 stack: [3]
```

**Frame 5.** The scan is over. Index 3 is still open, so mark it. Join.
```text
 chars: a "" b "" c ( d )
 join -> "abc(d)"
```

At every frame, the stack held exactly the indices of the `(` characters in the prefix that had not yet been closed, in increasing order. Every `)` was settled the moment it was read: matched, or marked.

## Why it is correct

Invariant after processing `s[0..i]`: (a) the stack contains, in order, the indices of every `(` in the prefix that is not matched to a `)` in the prefix, and (b) every `)` in the prefix is either matched to a `(` that was popped or marked as deleted. Pushing on `(` keeps (a). On `)` with a non-empty stack, popping matches it to the nearest open `(`, keeping (a) and (b). On `)` with an empty stack, marking it keeps (b).

After the whole string, the unmarked `)` are all matched to earlier `(`, and the stack lists the unmatched `(`. Marking them leaves a string in which every remaining `(` and `)` is in a matched pair, and the pairs, taken by most-recent-open, nest properly. So the result is balanced. As argued above, each marked character was unmatchable in *every* valid subsequence, so no smaller deletion set exists.

## Cost

- **Time O(n)**: one pass with O(1) stack work per character, plus one join.
- **Space O(n)**: the `chars` list and, in the worst case (`"((((("`), a stack of n indices.
- **O(1) extra variant**: two passes with a counter. Left to right, drop `)` when the count is 0. Then right to left over the result, drop `(` when the closing count is 0. The output buffer is still O(n), but there is no stack.
- The rescan approach is O(n²).

## Variations you will meet

- **Valid Parentheses (LeetCode 20).** Several bracket types, and you only answer yes or no. The stack holds bracket *types*, not indices, and a mismatch fails immediately.
- **Minimum Add to Make Parentheses Valid (LeetCode 921).** Count instead of mark. The answer is the number of unmatched `)` plus the number of `(` left on the stack. That is exactly how many characters this problem would delete.
- **Remove Invalid Parentheses (LeetCode 301).** Return *all* minimum-removal results. The counts from this problem give you how many of each to remove, then you backtrack over which ones, so the search is exponential in the worst case.
- **Longest Valid Parentheses (LeetCode 32).** Push indices, and when a pop empties the stack, the distance to the last unmatched index is a valid run. It is the same index stack, read differently.

## What to carry forward

Push **indices**, not characters, when you need to act on the original string later, and mark rather than delete while scanning. Anything still on the stack at the end is exactly what never got matched. The next problem leaves matching behind and returns to a plain scan, where the only state is a row pointer that bounces between two walls.
