# Basic Calculator II

*LeetCode 227 · Medium · Pattern: Stack evaluation · Reading time ~7 min*

## What the problem is really asking

Evaluate an ordinary infix expression made of non-negative integers, `+ - * /` and spaces, with the usual precedence:
`*` and `/` bind tighter than `+` and `-`. Integer division truncates toward zero. No parentheses, no `eval`.

The answer is one integer. In Reverse Polish Notation the token order told you exactly when to apply each operator. In
infix it does not: when you read `3 + 5`, you cannot add yet, because a `* 4` might follow and steal the 5.

```text
"3+5/2*4-6"

terms:   3   +   (5 / 2 * 4)   -   6
             ^ precedence groups * and / into one term
value:   3   +       8         -   6   =  5
```

## Do it by hand first

Look at `3+5/2*4-6` the way you were taught at school. You split it at the `+` and `-` signs into terms, `3`, `5/2*4`
and `6`, work out each term, then add them with their signs.

```text
term 1: +3
term 2: +5 -> /2 -> 2 -> *4 -> 8      (left to right inside)
term 3: -6
sum: 3 + 8 - 6 = 5
```

Notice what your hand did while reading. On `+` or `-` it started a new term and could forget the old one, except for
its value. On `*` or `/` it went back and changed the term it was building, the most recent one. Only one term was ever
being edited: the last one. That is a stack whose top is "the term under construction", and whose answer is the sum of
everything on it.

## The first honest attempt

Tokenise, then do two passes like a textbook. Pass one: find each `*` or `/`, replace `a op b` by its result in the list,
splice, continue. Pass two: do the same for `+` and `-`.

```text
tokens: 3 + 5 / 2 * 4 - 6
pass 1: 3 + 2 * 4 - 6        splice: tail shifted left
        3 + 8 - 6            splice: tail shifted left again
pass 2: 11 - 6               splice
        5
        ^^^^^^^^^
        every splice moves the whole tail; pass 2
        re-reads tokens pass 1 already walked over
```

Each splice is O(n) and there can be n/2 of them: O(n^2). The waste is moving data around to make results adjacent,
and reading the list twice.

## The turning point

**Claim: precedence only ever reaches back one term; `*` and `/` combine with the term immediately before, while `+` and
`-` can be postponed until the very end by storing signed terms.**

Why one term? Without parentheses, an expression is a sum of signed terms, and each term is a left-to-right chain of
`*` and `/`. A `*` or `/` always applies to the term currently being built, never to anything earlier. A `+` or `-`
closes the current term and opens a new one, and addition is associative and commutative, so all those terms can simply
be summed at the end. Subtraction is just adding a negated term.

So keep a stack of resolved terms:

- after `+`, the next number is pushed as `num`;
- after `-`, it is pushed as `-num`;
- after `*`, pop the top term and push `top * num`;
- after `/`, pop the top term and push `int(top / num)`, truncating toward zero.

The answer is `sum(stack)`.

The one subtle point is *when* to apply an operator. You cannot apply `*` when you see it, because its right operand has
not been read yet (it may have several digits). So remember the operator that came *before* the current number, call it
`op`, starting as `+`. When the number ends, which happens when the next operator arrives or the string ends, apply the
pending `op` to it, then store the new operator as the next `op`.

```text
"3 + 5 / 2"
 op='+' num=3 | sees '+': apply '+' -> push 3, op='+'
 op='+' num=5 | sees '/': apply '+' -> push 5, op='/'
 op='/' num=2 | end:      apply '/' -> pop 5, push 2
                                       ^ operator applied one
                                         step late, on purpose
```

A one-line statement of the rule, since it is the whole algorithm:

```text
if op == '*': stack.append(stack.pop() * num)
```

The stack is a flattened version of the RPN stack from two problems ago: `+` and `-` defer work by pushing, and `*` and
`/` do their work immediately on the top.

## Watch it work

Input `3+5/2*4-6`. The cursor marks the character that completes a number (an operator, or the last character). The stack
of terms is drawn as a column, top at the top; `op` is the pending operator before the number.

```text
Frame 1:  3 + 5 / 2 * 4 - 6     stack     pending
            ^                   | 3 |     op '+' -> '+'
          num 3 ends; op '+': push 3
```

The first number has an implicit `+` in front of it, so it is pushed as a term. The new pending operator is the `+` just
read.

```text
Frame 2:  3 + 5 / 2 * 4 - 6     stack     pending
                ^               | 5 |     op '+' -> '/'
          num 5 ends; op '+':   | 3 |
          push 5
```

5 starts a new term. The `/` is only remembered, because its right operand is not read yet.

```text
Frame 3:  3 + 5 / 2 * 4 - 6     stack     pending
                    ^           | 2 |     op '/' -> '*'
          num 2 ends; op '/':   | 3 |
          pop 5, push int(5/2) = 2
```

Division edits the top term in place: 5 became 2.

```text
Frame 4:  3 + 5 / 2 * 4 - 6     stack     pending
                        ^       | 8 |     op '*' -> '-'
          num 4 ends; op '*':   | 3 |
          pop 2, push 2*4 = 8
```

Multiplication edits the same top term again. The term `5/2*4` is complete with value 8.

```text
Frame 5:  3 + 5 / 2 * 4 - 6     stack     sum
                          ^     | -6 |    3 + 8 - 6 = 5
          last char; op '-':    |  8 |
          push -6               |  3 |
```

The end of the string flushes the last number with the pending `-`, so -6 is pushed. The answer is the sum, 5. In every
frame the stack held finished terms below and the term under construction on top, and summing the stack would give the
value of the expression read so far.

## Why it is correct

Invariant: each time a number is flushed, the stack contains the signed values of the terms read so far, with the last
entry being the current term evaluated up to that number. A flush with `op` of `+` or `-` starts a new term, correctly
signed. A flush with `*` or `/` extends the current term by one more factor; since `*` and `/` associate left to right
inside a term, applying them to the top in reading order gives the right value. Because the subtraction sign was folded
into the term when it was pushed, `-` is never applied across terms, which avoids the trap `8 - 6 * 2` being read as
`(8 - 6) * 2`. When the string ends and the last number is flushed, every term is complete and the expression's value is
their sum.

Division sign care: a term can be negative, for example `14-3/2` pushes 14 then -3, and then `int(-3 / 2)` must be -1, not
-2. Python's `//` would floor to -2. `int(a / b)` truncates toward zero as required.

## Cost

Time O(n): one pass over the characters, O(1) work per character; the final sum is O(number of terms).
Space O(n) for the stack of terms. It can be cut to O(1): keep `total` (the sum of finished terms) and `last` (the term
under construction) as two variables instead of a stack, because only the top is ever touched besides the final sum.

## Variations you will meet

- **Parentheses with only `+` and `-` (Basic Calculator, LeetCode 224).** No precedence, but groups can be negated; the
  stack now holds signs. That is the next problem.
- **All four operators plus parentheses (Basic Calculator III, LeetCode 772).** Combine both ideas: at `(` push the
  current `(stack, op)` context and start fresh, as in Decode String; at `)` collapse the inner stack to its sum and treat
  it as a number.
- **Unary minus.** `-3*2` or `2*-3`: treat a `-` that follows an operator or starts the expression as part of the number.
- **Shunting-yard.** Convert to RPN with an operator stack, then evaluate as in Evaluate Reverse Polish Notation; more
  general, more code.

## What to carry forward

Infix without parentheses is a sum of terms: `+` and `-` push signed terms, `*` and `/` rewrite the top term, and each
operator is applied when the number after it ends. The next problem drops `*` and `/` but adds parentheses, and the
stack changes from holding terms to holding the sign each group passes down.
