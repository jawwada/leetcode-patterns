# Longest Palindromic Substring (LeetCode 5)

**Area:** strings · **Difficulty:** Medium · **Key operations:** pick a center (odd and even), expand l and r while the ends match, record the best span

## Problem

Given a string `s`, return the longest substring of `s` that reads the same forwards and backwards. If several palindromic substrings share the maximum length, return the leftmost one (LeetCode accepts any; this script is deterministic).

## Example

```
s = "babad" -> "bab"

index  0 1 2 3 4
       b a b a d
       [---]        "bab"  centered on index 1
         [---]      "aba"  centered on index 2, same length, further right
```

`"cbbd"` gives `"bb"`, an even-length palindrome centred on the gap between indices 1 and 2.

## Brute force

Enumerate every substring `s[i:j+1]` and test whether it equals its reverse, keeping the first one longer than the best so far.

O(n³) time: O(n²) substrings, O(n) to check each. O(1) extra space. The wasted work: when `s[i:j+1]` is tested, its inner part `s[i+1:j]` was already tested earlier and the outer result only needs one extra comparison, yet the whole check starts from scratch.

## From brute force to optimal

Instead of fixing the two endpoints and checking inward, fix the *middle* and grow outward. A palindrome is determined by its center and its radius: from a center, extend one step on each side as long as the two outer characters match. The moment they differ, no wider palindrome with that center exists, so stop. There are only `2n - 1` centers: `n` single characters (odd lengths) and `n - 1` gaps between neighbours (even lengths). Each comparison either grows a palindrome or ends a center, so the total is O(n²) in the worst case with O(1) extra space, and far less on typical input. No table is filled.

## Intuition

Picture two fingers starting together on one character (odd case) or on two adjacent characters (even case), then walking apart one step at a time. As long as the two fingers see the same letter, the span between them is a palindrome; the first disagreement ends the walk, and the palindrome is the span *just inside* the fingers, `s[l+1:r]`. Since the length of a palindrome and its center position fix where it starts, scanning centers left to right and replacing the best only when strictly longer always keeps the leftmost of the longest.

## Walkthrough

`l` and `r` are the fingers after the walk stops; the palindrome is `s[l+1:r]`. Best is replaced only when strictly longer.

```
s = b a b a d
    0 1 2 3 4

center 0 odd   l=0 r=0  s[0]==s[0] -> l=-1 r=1   stop (l<0)      "b"    best "b" (1)
center 0 even  l=0 r=1  b != a                   stop            ""
center 1 odd   l=1 r=1  s[1]==s[1] -> l=0 r=2
                        s[0]==s[2] -> l=-1 r=3   stop (l<0)      "bab"  best "bab" (3)
center 1 even  l=1 r=2  a != b                   stop            ""
center 2 odd   l=2 r=2  s[2]==s[2] -> l=1 r=3
                        s[1]==s[3] -> l=0 r=4
                        s[0]=b != s[4]=d         stop            "aba"  3 is not > 3, keep "bab"
center 2 even  l=2 r=3  b != a                   stop            ""
center 3 odd   l=3 r=3  -> l=2 r=4   b != d      stop            "a"
center 3 even  l=3 r=4  a != d                   stop            ""
center 4 odd   l=4 r=4  -> l=3 r=5   stop (r==n)                 "d"
center 4 even  l=4 r=5  stop (r==n)                              ""
return s[0:3] = "bab"
```

## Steps

1. `best_lo, best_len = 0, 0`.
2. For each index `center`, try two starting pairs: `(center, center)` for odd lengths and `(center, center + 1)` for even lengths.
3. While `l >= 0`, `r < n` and `s[l] == s[r]`: `l -= 1`, `r += 1`.
4. The palindrome is `s[l+1:r]`, of length `r - l - 1`. If that is strictly longer than `best_len`, record `best_lo = l + 1` and the length.
5. Return `s[best_lo : best_lo + best_len]`.

## Complexity

O(n²) time in the worst case (a string of one repeated letter expands every center to the edge); O(1) extra space. Typical strings stop most expansions after one comparison.

## Pitfalls

- **`>=` instead of `>` when updating the best.** An equal-length palindrome found later overwrites the earlier one, so `"babad"` returns `"aba"` and `"ac"` returns `"c"`; the leftmost answer needs a strict comparison.
- **Recording `l` instead of `l + 1`.** When the loop stops, `l` and `r` sit on the first mismatch (or just outside the string); the palindrome is `s[l+1:r]`, so `"cbbd"` would wrongly give `"cb"`.
- **`l > 0` instead of `l >= 0`.** Index 0 is a valid left end; `"abba"` would give `"bb"` and `"a"` would give `""`.
- **Forgetting the even centers.** `"cbbd"` has no odd-length palindrome longer than 1; without the gap centers the answer is `"c"`.
- **`r <= n` in the bound check.** `s[n]` raises `IndexError`.
