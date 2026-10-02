# Evaluate Reverse Polish Notation

*LeetCode 150 · Medium · Pattern: Stack evaluation · Reading time ~6 min*

## What the problem is really asking

You get an arithmetic expression as a list of tokens written in postfix order: operands come first, the operator comes
after them. `3 + 4` is written `3 4 +`, and `(6 - (2 + 3)) * 4` is written `6 2 3 + - 4 *`. Compute its integer value.
Division truncates toward zero, and the input is guaranteed to be valid.

The answer is one integer. The interesting thing is that postfix needs no parentheses and no precedence rules at all. The
order of the tokens already says exactly which operation happens when. The question is how to read that order without
looking ahead or backtracking.

```text
tokens:  6  2  3  +  -  4  *

as a tree:          *
                  /   \
                 -     4
               /   \
              6     +
                  /   \
                 2     3
postfix = left subtree, right subtree, then the operator
```

## Do it by hand first

Read `6 2 3 + - 4 *` with a pencil. Numbers you cannot use yet, so you write them down in a row. When you meet `+`, you
look at the row: which two numbers does it apply to? The last two you wrote, 2 and 3. Cross them out, write 5.

```text
written so far       next token
6                    2
6 2                  3
6 2 3                +   -> uses 2, 3 -> 6 5
6 5                  -   -> uses 6, 5 -> 1
1                    4
1 4                  *   -> uses 1, 4 -> 4
answer 4
```

Every operator used the two rightmost surviving numbers and left one number in their place. The row of surviving numbers
grew and shrank only at its right end. Your hand was running a stack.

## The first honest attempt

Without that insight, the direct approach is reduction by rescanning: find the first operator in the list, apply it to
the two tokens just before it, splice the result in as one token, and start over from the beginning.

```text
pass 1: 6 2 3 + - 4 *   scan from 0, first operator at 3
        -> 6 5 - 4 *
pass 2: 6 5 - 4 *       scan from 0 AGAIN, operator at 2
        -> 1 4 *
pass 3: 1 4 *           scan from 0 AGAIN
        -> 4
        ^
        "6" was re-read on every pass, and every splice
        shifted the whole tail of the list
```

With about n/2 operators, each pass costs O(n) to scan and rebuild, so O(n^2) in total. The waste is the prefix: numbers
that are already sitting there, untouched, waiting for their operator, get re-read every pass.

## The turning point

**Claim: when an operator is read, its two operands are the two most recent values that have not been consumed yet.**

Why is that true for every valid postfix expression? Look at the tree. The operator's right operand is the value of its
right subtree, which is the token sequence written immediately before the operator. Its left operand is the value of the
left subtree, written immediately before that. Every operator inside those subtrees has already been applied and has
collapsed its own subtree into a single value. So, reading left to right, the last two unconsumed values are exactly the
left and right operands, in that order.

"The most recent unconsumed values" is the top of a stack. So:

- a number is pushed;
- an operator pops `b` (the right operand), then pops `a` (the left operand), and pushes `a op b`;
- at the end, exactly one value remains: the answer.

The splice from the brute force becomes a push, and the rescan disappears, because the stack keeps the unconsumed values
in place and in order.

The order of the two pops matters for `-` and `/`. The value on top arrived later, so it is the right-hand operand:

```text
tokens: 6 5 -          stack     first pop  = b = 5
                       | 5 |     second pop = a = 6
                       | 6 |     push a - b = 1   (not 5 - 6)
```

And "truncate toward zero" is not Python's `//`, which floors: `-7 // 2` is -4, while the expected answer is -3. Use
`int(a / b)`.

## Watch it work

Tokens `6 2 3 + - 4 *`. The cursor `^` marks the token just processed; the stack column is drawn top at the top.

```text
Frame 1:  6 2 3 + - 4 *      stack
              ^              | 3 | <- top
          three numbers      | 2 |
          pushed             | 6 |
```

No operator yet, so all three numbers wait on the stack in reading order.

```text
Frame 2:  6 2 3 + - 4 *      stack
                ^            | 5 | <- top
          pop b=3, a=2       | 6 |
          push 2+3 = 5
```

`+` consumes the top two and leaves their sum in their place. The stack shrank by one.

```text
Frame 3:  6 2 3 + - 4 *      stack
                  ^          | 1 | <- top
          pop b=5, a=6
          push 6-5 = 1
```

`-` takes the two most recent unconsumed values. The second pop, 6, is the left operand, so the result is 1, not -1.

```text
Frame 4:  6 2 3 + - 4 *      stack
                    ^        | 4 | <- top
                             | 1 |
```

4 is a number and waits.

```text
Frame 5:  6 2 3 + - 4 *      stack
                      ^      | 4 | <- top
          pop b=4, a=1       end: one value left
          push 1*4 = 4       answer 4
```

`*` combines 1 and 4. The input is exhausted and one value remains: 4. In every frame the stack held exactly the values
of the complete subtrees read so far whose parent operator had not arrived yet, oldest at the bottom.

## Why it is correct

Invariant: after processing a prefix of the tokens, the stack contains, bottom to top, the values of the maximal
complete subexpressions in that prefix, in left-to-right order. Initially both are empty. Pushing a number adds a new
one-token subexpression on the right. When an operator arrives, the rule of postfix says its operands are the two
rightmost complete subexpressions; by the invariant those are the top two values, so popping them, combining, and pushing
the result replaces two subexpressions with their parent, which keeps the invariant. When the input ends, a valid
expression is one complete subexpression, so the stack holds one value, and it is the value of the whole expression.

## Cost

Time O(n): every token causes one push, and every operator two pops; each is O(1).
Space O(n): a run of numbers before the first operator (for example `1 2 3 4 + + +`) puts about n/2 values on the stack.

## Variations you will meet

- **Infix with precedence (Basic Calculator II).** There are no explicit postfix operators, but `*` and `/` still grab the
  previous term from the stack top. That is two problems ahead.
- **Infix to postfix (shunting-yard).** Use a stack of *operators*: pop higher-precedence operators to the output before
  pushing a new one. Feeding the result to this algorithm evaluates any infix expression.
- **Prefix (Polish) notation.** Read the tokens right to left and the same stack works, except the first pop is now the
  left operand.
- **Build the expression tree.** Push tree nodes instead of numbers; an operator pops two nodes and pushes a new node with
  them as children.

## What to carry forward

In postfix, the operands of an operator are the two most recent unconsumed values; push numbers, and let operators eat
the top two (second pop on the left). The next problem pushes not values but whole unfinished contexts, the text built so
far and a repeat count, every time a bracket opens.
