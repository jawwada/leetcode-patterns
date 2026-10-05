# Longest Palindromic Substring

*LeetCode 5 · Medium · Pattern: Expand around center · Reading time ~7 min*

## The problem

Given a string s, return the longest substring that reads the same forwards and backwards; if several tie, any one is
accepted.

```text
Example: 'babad' -> 'bab' (or 'aba'); 'cbbd' -> 'bb'.
```

## What the problem is really asking

Given a string `s`, find the longest contiguous piece of it that reads the same forwards and backwards. If several have the maximum length, any one is fine.

The answer is a substring, which you can describe by two numbers: a start index and a length. "Contiguous" matters; this is not the longest palindromic subsequence, where you may skip characters. What makes it hard is the count: a string of length `n` has about `n^2 / 2` substrings, and checking whether one is a palindrome costs up to its length. Naively that is cubic.

```text
 s = c a b b a d
     0 1 2 3 4 5
       [-----]       "abba", indices 1..4, length 4

 other palindromes: every single letter, "bb" (2..3)
 nothing longer: "cabbac" would need s[5] == 'c'
```

## Do it by hand first

Look at `"cabbad"` and find the longest palindrome by eye. You probably did not test substrings one by one. Your eye spotted the doubled `bb` in the middle and then checked outward: is the letter left of `bb` the same as the letter right of it? `a` and `a`, yes. One more step out: `c` and `d`, no. Stop. The palindrome is `abba`.

```text
       c  a  b  b  a  d
             ^  ^            start: "bb" (equal pair)
          ^        ^         a == a  -> "abba"
       ^              ^      c != d  -> stop
```

What your eye tracked was a center and two pointers walking away from it in lockstep. A palindrome is a mirror image around its middle, so you grew it from the middle.

Also notice the middle was between two letters, not on a letter. `"aba"` has a letter in the middle; `"abba"` has a gap. Both kinds of middle exist.

## The first honest attempt

Enumerate every pair `(i, j)` with `i <= j`, take `s[i..j]`, and test it by comparing it to its reverse. Keep the longest that passes.

There are `n(n+1)/2` pairs and each test is `O(n)`, so `O(n^3)` time, `O(1)` extra space if you compare in place.

Where is the waste? Look at two substrings with the same middle:

```text
 test s[1..4] = a b b a :  compare a/a, then b/b
 test s[2..3] =   b b   :  compare b/b             <- again
 test s[0..5] = c a b b a d : compare c/d          (fails)
     but if it had passed, next it would compare
     a/a and b/b again, which we already know
```

`s[i..j]` is a palindrome exactly when `s[i] == s[j]` and `s[i+1..j-1]` is a palindrome. The brute force asks about the inner substring from scratch inside every outer test. It is solving the same nested question again and again, once for every pair of ends wrapped around it.

## The turning point

**Claim: every palindrome is determined by its center, and the longest palindrome around a fixed center is found by expanding outward until the first mismatch.**

Justify the stopping rule. Fix a center. Suppose the radius-`r` extension fails, meaning `s[lo] != s[hi]` at the pointers. Every wider candidate around the same center contains those two positions as a mirrored pair, so every wider candidate is also not a palindrome. So the first mismatch tells you the maximum radius for that center, and stopping there loses nothing.

How many centers are there? A palindrome of odd length has a middle character: `n` choices. One of even length has a middle gap between two adjacent characters: `n - 1` choices. So `2n - 1` centers in total. In code, an odd center at `i` starts with `lo = hi = i`, and an even center between `i` and `i + 1` starts with `lo = i`, `hi = i + 1`. Both use the same expansion:

```text
 expand(lo, hi):
   while lo >= 0 and hi < n and s[lo] == s[hi]:
       lo -= 1;  hi += 1
   palindrome is s[lo+1 .. hi-1], length hi - lo - 1

  c  a  b  b  a  d       exit state for center (2,3):
  ^              ^       lo=0, hi=5 (mismatch c/d)
  lo             hi      palindrome = s[1..4], len 4
```

The exit point needs care. The loop stops with `lo` and `hi` pointing one step past the palindrome on each side (either at a mismatch or outside the string), so the palindrome is `s[lo+1 : hi]` in Python slicing, of length `hi - lo - 1`. For an even center whose two starting characters differ, the loop runs zero times and the length is `(i+1) - i - 1 = 0`, an empty palindrome, which is harmless.

Why is this better? Every comparison now either extends a palindrome (and that knowledge is used immediately for the next step out) or ends a center. Nothing is ever re-checked for the same center. The nested question "is the inside a palindrome?" is answered by the fact that we only reached this radius because the inside already matched.

## Watch it work

`s = "cabbad"`. State: the current center, the pointers at exit, and the best `(start, length)` so far.

Frame 1. Centers on `c` (index 0) and on the gap 0|1.

```text
 c a b b a d
 ^            odd (0,0): lo=-1 out of bounds -> "c", len 1
 ^ ^          even (0,1): c != a -> len 0
 best = (0, 1)  "c"
```

The first single letter becomes the best so far.

Frame 2. Centers on `a` (index 1) and on the gap 1|2.

```text
 c a b b a d
 ^   ^        odd (1,1): grow to lo=0,hi=2: c != b -> "a"
   ^ ^        even (1,2): a != b -> len 0
 best = (0, 1)  unchanged (ties do not replace)
```

Frame 3. Center on `b` (index 2), then the gap 2|3.

```text
 c a b b a d
   ^   ^      odd (2,2): a != b at lo=1,hi=3 -> "b"
     ^ ^      even (2,3): b == b, step out
   ^     ^              a == a, step out
 ^         ^            c != d, stop: lo=0, hi=5
 palindrome s[1:5] = "abba", len 4
 best = (1, 4)
```

The even center found the answer; an odd-only solution would have missed it.

Frame 4. The remaining centers: on `b`(3), gap 3|4, on `a`(4), gap 4|5, on `d`(5).

```text
 odd (3,3): "b"   even (3,4): b != a
 odd (4,4): "a"   even (4,5): a != d
 odd (5,5): "d"   even (5,6): hi out of bounds
 best = (1, 4) -> return "abba"
```

Each later center found something of length 1 or 0, never beating 4.

Across the frames, the invariant was: `best` is the longest palindrome among all centers processed so far, and within one center, `s[lo+1 .. hi-1]` was always a palindrome.

## Why it is correct

Every palindromic substring has exactly one center among the `2n - 1` we try. For that center, the expansion finds the maximum radius by the stopping argument above, so it finds a palindrome at least as long as the one we are thinking of. The global maximum is the maximum over centers, and we track it with `best`. Therefore the returned substring has the maximum length.

The per-center loop invariant: whenever the loop condition is about to be checked, `s[lo+1 .. hi-1]` is a palindrome. Initially that is a single character or the empty string; each successful iteration wraps it in a matching pair.

## Cost

- Time `O(n^2)` in the worst case: `2n - 1` centers, each expanding at most `n/2` steps. The worst case is a string of one repeated letter, like `"aaaa..."`, where every center expands to the string's edge. On typical text, most centers stop after one or two comparisons.
- Space `O(1)`: two pointers and the best pair.

A dynamic-programming table `dp[i][j]` also gives `O(n^2)` time but uses `O(n^2)` space. Manacher's algorithm reaches `O(n)` by reusing mirror information from a palindrome that already covers the current center; it is rarely expected in interviews.

## Variations you will meet

- **Palindromic Substrings (LeetCode 647).** Count all palindromic substrings instead of finding the longest. Same expansion; add one to the count on every successful step, including the radius-0 odd step.
- **Longest Palindromic Subsequence (LeetCode 516).** Characters may be skipped, so centers no longer work; use the interval DP on `(i, j)`.
- **Valid Palindrome II (LeetCode 680).** Two pointers from the outside inward, allowing one skip; it is expansion run in reverse.
- **Return all longest palindromes, or the leftmost.** Ties: the code replaces only on strictly longer, so it returns the first maximum found by center order.

## What to carry forward

A palindrome is a mirror around a center: grow it outward from all `2n - 1` centers and stop at the first mismatch. The next problem trades mirrors for overlaps: instead of a string matching its own reverse, it asks where a string's beginning reappears at its own end.
