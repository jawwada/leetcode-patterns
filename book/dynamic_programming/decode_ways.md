# Decode Ways

*LeetCode 91 · Medium · Pattern: 1-D DP over prefixes (Fibonacci-style) · Reading time ~6 min*

## What the problem is really asking

Letters were encoded as numbers, `A = 1` through `Z = 26`, and the numbers were glued together with no separators. Given the digit string, count how many letter strings could have produced it. A code may not have a leading zero: `"06"` is not 6, it is invalid.

The answer is a count, not a list. What makes it hard is twofold: the number of ways can grow like Fibonacci (ten 1s already give 89), and zeros punch holes in the rules, because a `0` cannot stand alone and can only finish a `10` or `20`.

```text
 s = " 1  1  1  0  6 "

 cut A:  1 | 1 | 10 | 6      ->  A A J F
 cut B:  11 | 10 | 6         ->  K J F
 cut C:  1 | 11 | 0 | 6      ->  "0" alone: invalid
 cut D:  1 | 1 | 1 | 0 | 6   ->  invalid
                               answer: 2
```

## Do it by hand first

Treat the string as stepping stones and count paths across. Write under each boundary "how many ways to decode everything to my left". The empty prefix has exactly one decoding (decode nothing). Then for each new boundary ask two questions: can the last single digit be a letter, and can the last two digits be a letter?

```text
 prefix:   ""   "1"  "11"  "111"  "1110"  "11106"
 ways:      1    1     2     3       2       2
                                     ^
          "1110": the single "0" is no letter -> 0
                  the pair "10" is J -> ways("11") = 2
```

Your hand kept one count per boundary and, to fill a box, looked at the two boxes behind it, admitting each only if its digits formed a legal code. That is Fibonacci with gates.

## The first honest attempt

Recursion on where the remaining string starts. `ways(i)` counts decodings of the suffix `s[i:]`:

- If `s[i]` is `0`, nothing can start here: 0.
- Otherwise take one digit: `ways(i+1)`.
- And if `s[i:i+2]` is between 10 and 26, also take two digits: `ways(i+2)`.
- At the end of the string: 1 (one completed decoding).

```text
                     ways(0) "11106"
               1 /                 \ 11
          ways(1) "1106"          ways(2) "106"   <-- here
          1 /        \ 11          1 /     \ 10
   ways(2) "106"   ways(3) "06"  ...       ways(4) "6"
     ^                     |
     solved again          0 (starts with '0')
```

Each call can branch twice, so on a string of 1s the tree has Fibonacci-many leaves: about 1.6^n. The repeated work is visible: the suffix `"106"` is decoded from scratch once under "take 1, take 1" and again under "take 11". How you consumed the prefix has no effect on how many ways the suffix can be finished.

## The turning point

**Claim: every decoding of a prefix ends with a letter made of either its last one digit or its last two digits, so the count for the prefix is the sum of the counts for the two shorter prefixes, each admitted only if that last code is legal.**

Take any valid decoding of `s[:i]`. Its last letter covers either `s[i-1]` alone or `s[i-2:i]`. These two groups do not overlap (the last letter has a different length) and together cover everything. Removing the last letter leaves a valid decoding of `s[:i-1]` or `s[:i-2]`, and every decoding of those shorter prefixes extends by that letter. So the groups have exactly `dp[i-1]` and `dp[i-2]` members, when the gate is open.

- **State:** `dp[i]` = number of decodings of the prefix `s[:i]`.
- **Recurrence:** `dp[i] = (dp[i-1] if s[i-1] != '0') + (dp[i-2] if 10 <= int(s[i-2:i]) <= 26)`.
- **Base:** `dp[0] = 1` (the empty prefix), `dp[1] = 1` if `s[0] != '0'` else 0.
- **Order:** `i = 2..n`, left to right.
- **Space:** two rolling counts, `prev2 = dp[i-2]` and `prev1 = dp[i-1]`.

The two gates carry all the zero handling:

```text
 last digit  last pair   one-digit gate   two-digit gate
     '6'        "06"         open          closed (6 < 10)
     '0'        "10"        closed         open
     '0'        "30"        closed        closed  -> dp = 0
     '7'        "27"         open         closed (27 > 26)
```

A zero closes the one-digit gate; a leading zero or a value above 26 closes the two-digit gate. When both close, the count drops to 0, and it stays 0: the next cell's two-digit look-back would start with that same zero, so both of its inputs are 0 too. That is why `"100"` and `"30"` return 0.

Why does `dp[0] = 1` make sense? Because "the number of ways to decode the empty string" is the number of ways to finish when nothing is left, and finishing is one way. It is the same `1` the brute force returned at the end of the string. Setting it to 0 would zero out every count that reaches back to the start through a two-digit code.

## Watch it work

`s = "11106"`. Start with `(prev2, prev1) = (dp[0], dp[1]) = (1, 1)`.

**Frame 1.** i = 2, last digit `1`, pair `"11"`: both gates open, `1 + 1 = 2`.

```text
 s:        1   1   1   0   6
 dp:   1   1   2
               p2  p1
```

"11" decodes as AA or K.

**Frame 2.** i = 3, last digit `1`, pair `"11"`: `2 + 1 = 3`.

```text
 s:        1   1   1   0   6
 dp:   1   1   2   3
                   p2  p1
```

Plain Fibonacci so far: AAA, AK, KA.

**Frame 3.** i = 4, last digit `0` (gate closed), pair `"10"` (gate open): `0 + 2 = 2`.

```text
 s:        1   1   1   0   6
 dp:   1   1   2   3   2
                       p2  p1
```

The zero kills every decoding that ended with a lone "1": only those finishing in J survive.

**Frame 4.** i = 5, last digit `6` (open), pair `"06"` (closed, leading zero): `2 + 0 = 2`.

```text
 s:        1   1   1   0   6
 dp:   1   1   2   3   2   2  <- answer
                           p2  p1
```

The 6 extends both survivors: AAJF and KJF.

Invariant across frames: `prev1` always held the exact number of decodings of the prefix read so far and `prev2` that of the prefix one shorter, and each new count added only counts whose last code was legal.

## Why it is correct

Before step `i`, `prev2 = dp[i-2]` and `prev1 = dp[i-1]` are exact. The decodings of `s[:i]` split by the length of their last letter into two disjoint groups, which are in bijection with the decodings of `s[:i-1]` (when the last digit is 1..9) and of `s[:i-2]` (when the last two digits are 10..26). So the sum of the admitted terms is exactly `dp[i]`. The shift restores the invariant; after `i = n`, `prev1` is the answer. Disjointness matters for counting: if the groups could overlap, adding them would double count.

## Cost

- **Brute force:** O(1.6^n) time in the worst case, O(n) stack.
- **Table:** O(n) time, O(n) space.
- **Rolling pair:** O(n) time, O(1) space.

## Variations you will meet

- **Decode Ways II (LC 639):** `*` stands for any digit 1-9. The gates become multiplicities: `*` alone opens 9 one-digit codes, `1*` opens 9 pairs, `2*` opens 6. Same recurrence, weighted, taken modulo 10^9+7.
- **List all decodings:** the output is exponential, so it is backtracking over the same two choices, possibly pruned by the DP count.
- **Climbing Stairs (LC 70):** the same recurrence with both gates always open.
- **Word Break (LC 139):** the "last piece" can be any dictionary word, so each cell checks many look-backs instead of two.

## What to carry forward

Counting DP: split by the last piece, make sure the cases are disjoint, add the admitted ones, and give the empty prefix the count 1. The next problem looks back not by one or two cells but by every coin value, and asks for a minimum over all of them.
