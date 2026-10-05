# Basic Calculator

*LeetCode 224 · Hard · Pattern: Sign stack for parentheses · Reading time ~9 min*

## The problem

Evaluate a string containing non-negative integers, '+', '-', '(', ')' and spaces, including unary minus such as
"-(2-3)". No eval().

```text
Example: "(1+(4+5+2)-3)+(6+8)" -> 23; " 2-1 + 2 " -> 3; "-(2-3)"
  -> 1.
```

## What the problem is really asking

Evaluate a string containing non-negative integers, `+`, `-`, parentheses and spaces. There is no `*` or `/`. A minus may
be unary, as in `-(2-3)` or `-5`. You may not call `eval`.

The answer is one integer. With only `+` and `-`, the arithmetic itself is trivial; all the difficulty is in the
parentheses, and in particular in a minus sign standing in front of a parenthesised group. `1 - (2 - (3 + 4))` is not
`1 - 2 - 3 + 4`. The minus in front of each group reaches inside and changes how every term in it counts.

```text
1 - ( 2 - ( 3 + 4 ) )

depth 0:  1  -  [ ............... ]
depth 1:          2  -  [ ....... ]
depth 2:                  3  +  4

value: 1 - (2 - 7) = 1 - (-5) = 6
```

## Do it by hand first

Here is how most people simplify `1 - (2 - (3 + 4))` on paper without computing the inner groups first: they distribute
the minus signs. "Minus a group" flips every sign inside it.

```text
1 - (2 - (3 + 4))
= 1 - 2 + (3 + 4)     outer "-" flipped the sign of 2 and
                      the "-" in front of the inner group
= 1 - 2 + 3 + 4       inner group now preceded by "+"
= 6
```

Look at each number and ask "what sign does it finally carry?" The 1 is `+`. The 2 is written with `+` (implicitly, as
the first thing in its group), but the group is under one minus, so it ends up `-`. The 3 and 4 are written with `+`,
but sit under two minuses, which cancel, so they end up `+`.

```text
number   own sign   enclosing groups' signs   final
  1         +        (none)                     +
  2         +        -                          -
  3         +        -, -                       +
  4         +        -, -                       +
```

So every number's final sign is its own sign times the product of the signs in front of the groups it sits inside. Your
hand kept track of one thing as it went deeper: "am I currently inside an odd or an even number of negated groups?" It
pushed a fact on entering a group and dropped it on leaving. That is a stack of signs.

## The first honest attempt

Recursive evaluation. Scan left to right, adding signed numbers into a total. When you meet `(`, find its matching `)`
by walking forward and counting depth, recursively evaluate the substring between them, and add the result with the
current sign.

```text
"(1+(4+5+2)-3)+(6+8)"

top: "(" at 0, scan to its ")" at 12     12 chars
  recurse on "1+(4+5+2)-3":
    "(" at 2, scan to ")" at 8            7 chars
      recurse on "4+5+2"                  5 chars

"4+5+2" was read three times: by each enclosing scan
for ")" and then by its own evaluation
```

Finding the matching parenthesis reads the whole inside, and then the recursive call reads it again. A character at
depth d is read about d+1 times, so deeply nested input such as `((((...1...))))` costs O(n^2). Slicing substrings for
the recursive calls also copies O(n) characters per level. And on adversarial depth the recursion itself can blow Python's
stack. The waste is the look-ahead: we read ahead to find a `)`, only to read all of the same characters again.

## The turning point

**Claim: with only `+` and `-`, a parenthesised group changes nothing but the sign of each term inside it, so each
number can be added to one running total the moment it is read, as long as we know the effective sign of the group we
are in.**

Justification: addition and subtraction distribute over a group. `a - (b - c + d)` equals `a - b + c - d` for any
values. Applying this rule from the outside in, every number in the expression ends up as plus or minus itself in one
flat sum. The flat sign of a number is (its own operator's sign) times (the flat sign of the group it lives in), and the
flat sign of a group is (the operator in front of the group) times (the flat sign of the group around it). This is a
recursive definition, but it only ever needs the sign of the *innermost open group*, and groups open and close in LIFO
order. So it is a stack.

The algorithm keeps:

- `res`, the running total of everything flushed so far;
- `num`, the number currently being read (digits accumulate as `num * 10 + d`);
- `sign`, the flat sign that `num` will be added with;
- `signs`, a stack whose top is the flat sign of the innermost open group, starting as `[1]` for the whole expression.

The transitions, which are short enough to state completely:

- digit: extend `num`;
- `+` or `-`: flush `res += sign * num`, reset `num = 0`, and set the next sign `sign = signs[-1] * (+1 or -1)`;
- `(`: the current `sign` is the sign in front of this group, which is the flat sign of the new group, so push it;
- `)`: the group ends, pop.

To flush the very last number, scan `s + "+"` so a sentinel operator triggers one final flush.

```text
c in "+-":  res += sign * num
            num = 0
            sign = signs[-1] * (1 if c == "+" else -1)
c == "(":   signs.append(sign)
c == ")":   signs.pop()
```

Why push `sign` and not `+1` at `(`? Because at the moment `(` is read, `sign` already equals "the operator before this
group times the enclosing group's sign", which is exactly the definition of the new group's flat sign. Unary minus falls
out for free: `-(2-3)` reads `-` first, sets `sign = -1`, and the `(` pushes -1.

Picture each parenthesis pair as a lens. A `-` lens flips every term seen through it; two stacked `-` lenses cancel. The
stack is the pile of lenses the cursor is currently looking through, and its top is their combined effect.

```text
1 - ( 2 - ( 3 + 4 ) )
      |-------------|  lens -1
            |-----|    lens -1 * -1 = +1 (combined)
cursor at 3: looking through combined lens +1
```

The contrast with the previous problem is instructive. Basic Calculator II stored *terms* because `*` needs the previous
term. Here there is no `*`, so terms never need to be revisited, and the only thing worth remembering about an open group
is one bit: its sign.

## Watch it work

Input `1-(2-(3+4))`, scanned with a sentinel `+` at the end. The cursor marks the character just processed; the sign
stack is drawn as a column with its top at the top. `res` is the running total, `sign` the flat sign the next number
will be added with.

```text
Frame 1:  1 - ( 2 - ( 3 + 4 ) ) +      signs
            ^                          | +1 | <- top
          flush 1 with sign +1: res = 1
          sign = top(+1) * (-1) = -1
```

The `-` flushes 1 into the total and sets the sign for whatever comes next: minus, under a positive context.

```text
Frame 2:  1 - ( 2 - ( 3 + 4 ) ) +      signs
              ^                        | -1 | <- top
          push current sign -1         | +1 |
          res = 1, sign = -1
```

Entering the group: the sign in front of it, -1, becomes the context for everything inside.

```text
Frame 3:  1 - ( 2 - ( 3 + 4 ) ) +      signs
                  ^                    | -1 | <- top
          flush 2 with sign -1:        | +1 |
          res = 1 - 2 = -1
          sign = top(-1) * (-1) = +1
```

2 is added as -2 because it sits inside the negated group. The `-` after it, seen through the -1 lens, becomes `+`.

```text
Frame 4:  1 - ( 2 - ( 3 + 4 ) ) +      signs
                    ^                  | +1 | <- top
          push current sign +1         | -1 |
          res = -1, sign = +1          | +1 |
```

The inner group is preceded by a minus inside a negated group, so its flat sign is +1, and that is what is pushed.

```text
Frame 5:  1 - ( 2 - ( 3 + 4 ) ) +      signs
                        ^              | +1 | <- top
          flush 3 with sign +1:        | -1 |
          res = -1 + 3 = 2             | +1 |
          sign = top(+1) * (+1) = +1
```

3 is added positively, exactly as the hand-distributed version said.

```text
Frame 6:  1 - ( 2 - ( 3 + 4 ) ) +      signs
                            ^ ^        | +1 | <- top
          num = 4 (not flushed yet)
          ")" pop, ")" pop
          res = 2, sign = +1
```

Two `)` close both groups. The pending 4 keeps the sign it was given when `+` was read, which already accounts for both
lenses; popping only affects operators read later.

```text
Frame 7:  1 - ( 2 - ( 3 + 4 ) ) +      signs
                                ^      | +1 | <- top
          sentinel "+": flush 4 with sign +1
          res = 2 + 4 = 6   -> answer 6
```

The sentinel flushes the last number. The total is 6, matching `1 - (2 - 7)`. Across the frames, the stack depth always
equalled the number of open parentheses plus one, its top was the combined sign of all enclosing groups, and `res` was
always the flat sum of every number already completed.

## Why it is correct

Define the flat sign of a number as the sign it carries when every group is distributed away. Claim: when a number is
flushed, `sign` equals its flat sign, so `res` is always the flat sum of the flushed numbers, which is the value of the
expression once all are flushed.

Invariant 1: `signs[-1]` is the flat sign of the innermost open group (the whole expression counts as a group with sign
+1). It holds at the start with `[1]`. On `(`, the new group's flat sign is (the operator before it) times (the
enclosing group's flat sign); that product is precisely what `sign` was set to when that operator was read. If no operator
precedes the `(` inside its group, as in `((`, then `sign` still holds the enclosing group's flat sign, which is also
correct. So pushing `sign` maintains the invariant. On `)`, the innermost group closes and its entry is popped, exposing the
enclosing group's entry, still correct because nothing below the top ever changes.

Invariant 2: after reading an operator, `sign` is the flat sign of the number or group that follows it. That is true by
construction: the operator's own sign times the enclosing group's flat sign, which by invariant 1 is the stack top.

A number following an operator is flushed with that `sign`, which is its flat sign. A number at the start of a group
follows the `(`, and `sign` still equals the group's flat sign, which is the right flat sign for a number with an
implicit `+`. Hence every flush adds the right signed value, and the sentinel guarantees the last one is flushed.

## Cost

Time O(n): one pass, constant work per character, no look-ahead and no re-reading.
Space O(d), where d is the maximum nesting depth: one sign per open parenthesis. The recursive brute force is O(n * d)
time, which is O(n^2) on deeply nested input, plus O(n) space for slices and recursion frames.

An equivalent version keeps a stack of `(res, sign)` pairs: on `(` push the total so far and the sign in front of the
group, reset `res = 0`; on `)` compute the group's value and fold it into the popped total. That is the Decode String
pattern, saving the outer context and resuming it, and it is the version that generalises once `*` and `/` come back.

## Variations you will meet

- **Basic Calculator III (LeetCode 772).** All four operators plus parentheses. The sign trick no longer works, since
  `2 * (3 + 4)` cannot be distributed term by term into a flat sum cheaply. Push the whole context at `(` (the term stack
  and pending operator from Basic Calculator II), evaluate the group to a number at `)`, and continue as if it were a
  number.
- **Unary minus inside a group, like `2-(-3)`.** Already handled: the inner `-` is read as an operator with `num = 0`
  flushed before it, which adds 0, harmless.
- **Recursion instead of a stack.** A recursive descent parser with a shared index (not slices) is O(n) as well. The
  explicit stack is preferred when nesting can be 10^5 deep.
- **Expression with variables, simplify to a polynomial (LeetCode 770).** The stack holds whole polynomials instead of
  signs, but the shape of the parser is the same.

## What to carry forward

With only `+` and `-`, a parenthesis is just a sign lens: push the sign in front of each group, multiply every operator
by the top, and add each number straight into one total. The next problem keeps nesting but makes each group an operator
over many operands, so on `)` you collapse everything back to the matching `(` into one value.
