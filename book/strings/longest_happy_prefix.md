# Longest Happy Prefix

*LeetCode 1392 · Hard · Pattern: KMP failure function (longest border) · Reading time ~10 min*

## The problem

A happy prefix is a non-empty proper prefix of s that is also a suffix of s. Return the longest one, or "" if none
exists.

```text
Example: "level" -> "l"; "ababab" -> "abab"; "leetcodeleet" ->
  "leet"; "a" -> "".
```

## What the problem is really asking

A "happy prefix" of `s` is a non-empty prefix that is also a suffix, and that is not the whole string. Return the longest one, or `""` if none exists. `"level"` gives `"l"`. `"ababab"` gives `"abab"`, because the first four characters `abab` are also the last four; the two copies overlap in the middle, which is allowed.

The standard name for such a thing is a **border**: a proper prefix that equals a suffix. So the question is: what is the longest border of `s`?

The answer is a substring, fully described by one number, its length `b`, with `0 <= b < n`. What makes it hard is the input size (up to `10^5`) combined with the fact that the obvious check, comparing a prefix of length `b` with a suffix of length `b`, is `O(b)` per candidate and there are `n - 1` candidates.

```text
 s = a a b a a a b        n = 7
     0 1 2 3 4 5 6
     [a a b]              prefix of length 3
             [a a b]      suffix of length 3   equal!

 longest border = 3 -> "aab"
 (length 4: "aaba" vs "aaab" differ;
  length 5: "aabaa" vs "baaab" differ; ...)
```

## Do it by hand first

To find the longest border by hand, slide a second copy of the string underneath the first, shifted right, and look for the smallest shift where the overlapping parts agree completely. The overlap at that shift is the longest border.

```text
 shift 1:  a a b a a a b
             a a b a a a b      overlap: a b a a a b
                                      vs a a b a a a  (b != a)
 shift 2:  a a b a a a b
               a a b a a a b    overlap: b a a a b vs a a b a a
 shift 3:  a a b a a a b
                 a a b a a a b  overlap: a a a b vs a a b a
 shift 4:  a a b a a a b
                   a a b a a a b
                                overlap: a a b  vs  a a b  YES
```

The thing your hand kept track of is the overlap: how much of the string's beginning lines up with its end. That overlap is exactly the border, and the natural question it leads to is not just "what is the overlap of the whole string" but "what is the overlap for every prefix of the string", because those are the pieces you keep re-reading.

## The first honest attempt

Try each candidate length from the largest down: for `b = n-1, n-2, ..., 1`, compare `s[:b]` with `s[n-b:]`. Return the first match.

```text
 b=6: aabaaa vs abaaab   fail at char 1
 b=5: aabaa  vs baaab    fail at char 0
 b=4: aaba   vs aaab     fail at char 2
 b=3: aab    vs aab      match
       ^^^ each test re-reads the prefix from s[0]
```

Worst case `O(n^2)`: on a string like `"aaaa...ab"` most tests run almost to the end before failing. The waste is that each candidate length is tested independently. When the test for `b = 4` failed at its third character, we had learned that `s[0..1]` matches `s[3..4]`, but the test for `b = 3` throws that away and starts again at `s[0]`.

## The turning point

**Claim: if you know the longest border of every prefix of `s`, you can compute the longest border of the next prefix with only the comparisons "does the next character extend some border?", and the borders of a string are nested, so the candidates to try are a chain you have already computed.**

This is the Knuth-Morris-Pratt **failure function**. Since you have not met it before, build it slowly.

**Definition.** Let `fail[i]` be the length of the longest proper border of the prefix `s[0..i]` (the first `i+1` characters). For `s = "aabaaab"`:

```text
 i       0  1  2  3  4  5  6
 s[i]    a  a  b  a  a  a  b
 fail[i] 0  1  0  1  2  2  3

 fail[4] = 2: prefix "aabaa", border "aa"
              [a a] b [a a]
 fail[6] = 3: prefix "aabaaab", border "aab"
              [a a b] a [a a b]
```

The answer to the problem is `fail[n-1]`. The whole question is how to fill the table in `O(n)`.

**Fact 1: a border can grow by at most one character per step.** If `s[0..i]` has a border of length `b`, then removing the last character of both the prefix copy and the suffix copy gives a border of `s[0..i-1]` of length `b - 1`. So `fail[i] <= fail[i-1] + 1`. And the only way to get `fail[i] = fail[i-1] + 1` is to extend the previous longest border: with `k = fail[i-1]`, the prefix copy `s[0..k-1]` is followed by `s[k]`, the suffix copy is followed by `s[i]`, so if `s[i] == s[k]` the border grows to `k + 1`.

```text
 extending the border of s[0..i-1] by one:

  s[0..k-1]  s[k]              ...   s[i-k..i-1]  s[i]
  [ border ]  ?                      [ border ]    ?
             \___________ equal? ___________/
                 yes -> fail[i] = k + 1
```

**Fact 2: if the extension fails, the next candidate is the border of the border.** Suppose `s[i] != s[k]`. We need the next shorter border of `s[0..i-1]` and try to extend that instead. Here is the key picture. Any border of `s[0..i-1]` shorter than `k` is a prefix of the string and a suffix of the string; since it is shorter than `k`, it is also a prefix of the prefix copy `s[0..k-1]` and a suffix of the suffix copy, which is identical to `s[0..k-1]`. So it is a border of `s[0..k-1]`. The longest such thing is `fail[k-1]`, which we already computed.

```text
 the borders are nested:

 s[0..i-1]:  [ x x ] . . . . . . [ x x ]   k = fail[i-1]
             [ y ]x               x[ y ]
              ^ border of the border = fail[k-1]
 every border of s[0..i-1] shorter than k
 is a border of s[0..k-1]
```

So the next candidate is `k = fail[k-1]`. Try to extend it with `s[i] == s[k]`. If that fails too, fall again to `fail[k-1]`, and so on until either a match extends some border or `k` reaches 0. At `k = 0`, compare `s[i]` with `s[0]` once: if equal the border is 1, otherwise 0.

```text
 fail = [0] * n
 for i in 1..n-1:
     k = fail[i-1]
     while k > 0 and s[i] != s[k]:  k = fail[k-1]
     if s[i] == s[k]:  k += 1
     fail[i] = k
```

**Why this is linear, even with a loop inside a loop.** Watch `k` as a single quantity carried from step to step. Each outer step raises it by at most 1 (the `k += 1`). Each inner iteration lowers it by at least 1 (a border of the border is strictly shorter). It never goes below 0. Over the whole run it rises at most `n - 1` times in total, so it can fall at most `n - 1` times in total. Total work is `O(n)`, regardless of how the falls are distributed.

The border is automatically proper: `fail[0] = 0`, and growth by one per step from a proper border of the previous prefix stays proper.

## Watch it work

`s = "aabaaab"`. State: `i`, the candidate chain for `k`, and the table.

Frame 1. `i = 1`: `k = fail[0] = 0`; `s[1] = a`, `s[0] = a`, match.

```text
 i   0 1 2 3 4 5 6
 s   a a b a a a b
 f   0 1 . . . . .
       ^ k: 0 -> 1
```

Frame 2. `i = 2`: `k = fail[1] = 1`; `s[2] = b` vs `s[1] = a`, no. Fall: `k = fail[0] = 0`; `b` vs `s[0] = a`, no.

```text
 i   0 1 2 3 4 5 6
 s   a a b a a a b
 f   0 1 0 . . . .
         ^ chain: 1 -> 0, no match
```

The `b` breaks every border; the overlap resets.

Frame 3. `i = 3`: `k = 0`, `a == s[0]`, border 1. `i = 4`: `k = 1`, `s[4] = a == s[1] = a`, border 2.

```text
 i   0 1 2 3 4 5 6
 s   a a b a a a b
 f   0 1 0 1 2 . .
             ^ "aabaa": [aa]b[aa]
```

Frame 4. `i = 5`: `k = fail[4] = 2`; `s[5] = a` vs `s[2] = b`, no. Fall: `k = fail[1] = 1`; `s[5] = a` vs `s[1] = a`, yes: border 2.

```text
 try k=2: [a a b] needs s[5]=b  -> a, fail
 fall to fail[1] = 1
 try k=1: [a a]   needs s[5]=a  -> a, ok
 f   0 1 0 1 2 2 .
```

This is the border-of-the-border step: the overlap `aa` could not grow into `aab`, so we fell to the overlap of `aa`, which is `a`, and grew that.

Frame 5. `i = 6`: `k = fail[5] = 2`; `s[6] = b == s[2] = b`, border 3.

```text
 i   0 1 2 3 4 5 6
 s   a a b a a a b
 f   0 1 0 1 2 2 3
 answer = s[:fail[6]] = s[:3] = "aab"
```

At every frame the invariant held: `fail[0..i]` was correct for every prefix so far, and the only data consulted were entries already filled.

## Why it is correct

By induction on `i`. Assume `fail[0..i-1]` is correct. The candidates for `fail[i]` are `c + 1` where `c` is a border length of `s[0..i-1]` (or 0) and `s[i] == s[c]` (Fact 1). The border lengths of `s[0..i-1]` in decreasing order are exactly `fail[i-1]`, `fail[fail[i-1]-1]`, ... down to 0 (Fact 2, applied repeatedly). The loop tries them in decreasing order and stops at the first that extends, so it finds the largest valid one. If none extends, it ends with `k = 0` and the value is 1 or 0 depending on `s[i] == s[0]`. Thus `fail[i]` is correct, and `fail[n-1]` is the longest border of `s`.

## Cost

- Time `O(n)`: amortised, since `k` rises at most `n - 1` times in total and each fall costs one unit of a previous rise.
- Space `O(n)`: the table.

The brute force was `O(n^2)` in the worst case.

## Variations you will meet

- **Find a pattern in a text (LeetCode 28, KMP search).** Build `fail` for the pattern, then scan the text with the same "extend or fall back along `fail`" loop; a match is when `k` reaches the pattern's length.
- **Repeated Substring Pattern (LeetCode 459).** `s` is a repetition of a block iff `n % (n - fail[n-1]) == 0` and `fail[n-1] > 0`. The smallest period is `n - fail[n-1]`.
- **Count all borders.** Walk the chain `fail[n-1]`, `fail[fail[n-1]-1]`, ... Every border appears once.
- **Z-function or hashing.** The Z-array answers the same question (largest `z[i]` with `i + z[i] == n`); a rolling hash compares each prefix with its suffix in `O(1)`, but needs collision care.

## What to carry forward

The failure function stores, for every prefix, the longest overlap of the string with itself, and on a mismatch it falls to "the border of the border" instead of starting over; that fall is what makes it linear. The next problem reuses this exact table on a cleverly glued string to find the longest palindromic prefix.
