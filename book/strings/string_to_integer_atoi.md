# String to Integer (atoi)
*LeetCode 8 · Medium · Pattern: Single-pass state machine with early clamp · Reading time ~8 min*

## What the problem is really asking

Implement C's `atoi`. Skip leading spaces, accept at most one `+` or `-`, read as many digits as follow, and ignore everything after the first non-digit. If the value falls outside the 32-bit signed range [−2³¹, 2³¹ − 1], clamp it to the nearest end. If no digits were read, the answer is 0. The answer is a single integer.

What makes it hard is that the rules are positional. A space is fine at the start and fatal after the sign. A sign is fine once, before any digit. Letters are fine after the digits, where they just stop the read, and fatal before them, where the result is 0. The overflow rule also says something about *when* to check.

```text
 "   -0412x9"
  ___            spaces: skip
     -           sign: negative
      0412       digits: 412
          x9     stop at 'x'; the 9 is never read
 answer: -412
```

## Do it by hand first

Read `"   -0412x9"` aloud like a machine. "Space, skip. Space, skip. Space, skip. Minus, so remember negative. Zero: number is 0. Four: 4. One: 41. Two: 412. x: not a digit, done." You never went back, and at every moment you could have said which **phase** you were in: still skipping spaces, just read the sign, or reading digits.

```text
 char:   _   _   _   -   0   4   1   2   x
 phase:  SP  SP  SP  SG  DG  DG  DG  DG  STOP
 num:    .   .   .   .   0   4   41  412
```

Your hand tracked **a phase**, **a sign**, and **a running number**. That is a state machine with one accumulator.

## The first honest attempt

Use Python's tools: `lstrip(" ")`, peel off a sign character, collect the leading digits into a substring, call `int()` on it, multiply by the sign, and clamp with `max(INT_MIN, min(INT_MAX, value))`.

It is correct in Python and runs in O(n) time with O(n) extra space for the slices. The waste is subtle and becomes a bug in any other language. For an input like `"-91283472332"` it builds the full eleven-digit integer and only then discovers that most of it was never representable. In C or Java, `int` arithmetic overflows before the clamp line runs. Python's big integers just postpone the problem. Given a million-digit input, you build a million-digit number to return `2147483647`.

```text
 digits:  9 1 2 8 3 4 7 2 3 | 3 2
                            ^ already past 2^31 here
 brute:   keep multiplying anyway, clamp at the very end
```

## The turning point

**Parsing needs only the current phase and one accumulator, and the overflow decision can be made the moment the magnitude crosses the bound, because more digits can only make it larger.**

First claim: every rule in the spec is "in phase P, character class C sends you to phase Q". Drawn out, it is a small automaton:

```text
        ' '                                   digit
       +---+                                  +---+
       v   |                                  v   |
   +-------+  '+'/'-'  +------+   digit   +--------+
-->| SPACE |---------->| SIGN |---------->| DIGITS |
   +-------+           +------+           +--------+
       |                  |                ^    |
       | digit            |                |    | other
       +------------------|----------------+    | or end
       | other            | other               v
       +------------------+------> [ STOP: return sign*num ]
```

In code the phases are implicit in three consecutive loops on one index: a `while` that skips spaces, an `if` that takes at most one sign, and a `while` over digits. Any character that does not fit the current phase ends the scan.

Second claim: with a positive accumulator, `num = num*10 + d` never decreases. Once `sign * num` reaches `INT_MAX` or goes at or beyond `INT_MIN`, the final answer is the clamp, whatever comes next. So check after **every** digit and return immediately. The accumulator then never exceeds about 10 × 2³¹, which is how real C implementations stay in range. (Their check is `num > (INT_MAX − d) / 10`, done *before* multiplying.)

The comparison uses `>=` on the positive side. Reaching exactly 2147483647 already returns `INT_MAX`, which is the correct value anyway. On the negative side `<=` lets −2147483648 return `INT_MIN`, which is exact as well.

## Watch it work

First `"   -0412x9"`, then a quick look at the clamp on `"-91283472332"`.

**Frame 1.** SPACE phase. `i` skips indices 0–2.
```text
 _ _ _ - 0 4 1 2 x 9
       ^ i=3          phase SPACE -> SIGN
```

**Frame 2.** SIGN phase. `-` sets sign = −1, and `i` moves to 4.
```text
 _ _ _ - 0 4 1 2 x 9
         ^ i=4        sign=-1, num=0
```

**Frame 3.** DIGITS phase. 0 → 4 → 41 → 412, and the bound is checked after each.
```text
 _ _ _ - 0 4 1 2 x 9
                 ^ i=8
 num: 0, 4, 41, 412      -412 > INT_MIN: keep going
```

**Frame 4.** `x` is not a digit, so STOP. Return sign × num.
```text
 _ _ _ - 0 4 1 2 x 9
                 ^ stop     return -412   ('9' never read)
```

**Frame 5.** Clamp case `"-91283472332"`. After the 9th digit, num = 912834723, which is still inside the range.
```text
 - 9 1 2 8 3 4 7 2 3 3 2
                   ^ num=912834723   -num > -2147483648
```

**Frame 6.** The 10th digit gives num = 9128347233, and −9128347233 ≤ INT_MIN, so it returns −2147483648 at once. The last digit is never read.
```text
 - 9 1 2 8 3 4 7 2 3 3 2
                     ^ clamp -> return -2147483648
```

The pointer only moved right, and each phase handed off to the next and never back. In the DIGITS phase `num` always held the value of the digits read so far and was never more than one digit past the bound.

## Why it is correct

Invariant in the DIGITS phase: `num` is the integer value of `s[start:i]`, the digits read so far, and `sign * num` lies strictly inside (INT_MIN, INT_MAX). The update `num*10 + d` is exactly appending a digit. If the new value hits or crosses a bound, then every possible continuation also lies at or beyond it, since appending digits to a positive magnitude never shrinks it. So the clamped value is the final answer, and returning early matches what the full parse followed by a clamp would produce. When a non-digit or the end of the string arrives, the spec says to ignore the rest, so `sign * num` is the answer. The answer is 0 if no digit was read, because `num` started at 0.

The phases are correct by construction. Spaces are consumed only before any sign or digit. At most one sign is consumed, and only immediately after the spaces. So `"+-12"` reads `+` and then sees `-` in the DIGITS phase, stops, and gives 0. `"  + 413"` sees a space in the DIGITS phase and gives 0.

## Cost

- **Time O(n)** in the worst case, though it stops at the first non-digit or as soon as it clamps, so it reads at most about 10 digits.
- **Space O(1)**: one index, one sign and one accumulator.
- The slicing version is O(n) time and O(n) space, and it builds an arbitrarily large integer before clamping.

## Variations you will meet

- **Valid Number (LeetCode 65).** The next problem. Instead of extracting a value you must *accept or reject* the whole string, and the grammar adds a decimal point and an exponent. The automaton grows, and flags replace the linear phases.
- **"Implement it without 64-bit integers."** Check before multiplying: if `num > INT_MAX // 10`, or `num == INT_MAX // 10` and `d > 7`, then clamp. Negative numbers have one more unit of room (8), so handle the sign carefully.
- **Parse in a different base, or with underscores (`1_000`).** Change the digit class and the multiplier. The state machine stays the same.
- **Reverse Integer (LeetCode 7).** The same overflow-before-it-happens check, applied while building the reversed number.

## What to carry forward

Draw the phases as an automaton, implement each phase as a loop on one index, and clamp the moment the bound is crossed, because a monotone accumulator never comes back. The next problem keeps the one-pass automaton but must judge the *whole* string, so a few booleans replace the linear phase list.
