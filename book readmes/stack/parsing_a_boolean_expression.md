# Parsing a Boolean Expression

*LeetCode 1106 · Hard · Pattern: Stack-based expression evaluation · Reading time ~9 min*

## The problem

Evaluate a boolean expression built from 't', 'f', !(expr), &(expr,expr,...) and |(expr,expr,...).

```text
Example: "&(|(f))" -> False; "|(f,f,f,t)" -> True; "!(&(f,t))"
  -> True.
```

## What the problem is really asking

You get a string written in a tiny prefix language. The atoms are `t` and `f`. There are three operators, and each one is written in front of a parenthesised list of operands: `!(x)` negates one operand, `&(x,y,...)` is true when every operand is true, `|(x,y,...)` is true when at least one operand is true. Operands may themselves be whole expressions, nested as deep as you like. Return the boolean the whole string evaluates to.

The answer is a single bit. What makes it hard is not the logic, which is a one-liner per operator, but the shape of the input: the value of an outer operator is not knowable until every one of its operands, at every depth, has been reduced to a letter. You read left to right, but the evaluation has to happen inside out.

```text
expression:   & ( | ( f , t ) , ! ( f ) )
index:        0 1 2 3 4 5 6 7 8 9 0 1 2 3

as a tree:            &
                    /   \
                  |       !
                 / \      |
                f   t     f
```

The tree on the right is what the string means. The string on the left is how it is stored: a flattened, parenthesised walk of that tree. Every `)` in the string marks the moment a subtree is complete.

## Do it by hand first

Take `&(|(f,t),!(f))` and evaluate it on paper. Nobody starts with the `&`. Your eye slides right until it finds the first group that has no parentheses inside it, `|(f,t)`, and you write `t` over it. Then you find the next innermost group, `!(f)`, and write `t` over that. Now the outer group reads `&(t,t)`, which is `t`.

```text
&(|(f,t),!(f))
  '--+--'
     t
&(  t   ,!(f))
         '-+'
           t
&(  t   ,  t )   ->   t
```

What did your hand keep track of? Two things. First, the stuff to the left of the group you were working on, which you deliberately ignored and left exactly as it was. Second, the moment the group closed: a `)` told you "everything you need for this operator is now in view". You never revisited text to the left once you had walked past it, except to collapse the group you had just finished. Untouched text on the left, plus "collapse the most recent open group" on `)`, is exactly the description of a stack.

## The first honest attempt

The strong candidate's first idea copies the hand method literally: find the first `)`, walk back to its matching `(`, read the operator in front of it, split the inside on commas, evaluate, then splice the single result letter back into the string. Repeat until no `(` remains.

It is correct, and it is easy to write. Its cost is the problem. Each reduction builds a brand-new string by concatenating the prefix, the letter, and the suffix. With `d` groups the loop runs `d` times, and each time it copies and re-scans nearly the whole string. A deeply nested input like `!(!(!(!(...f...))))` has about `n/3` groups, so the total is O(n^2).

```text
round 1: &(|(f,t),!(f))     scan to first ')', rebuild
           ~~~~~~
round 2: &(t,!(f))          rebuild again; "&(t," was
             ~~~~~          copied a second time
round 3: &(t,t)             rebuild again; "&(" copied
         ~~~~~~             a third time
```

The squiggles mark the only part each round actually needed. Everything else, especially the prefix `&(`, is copied over and over even though nothing about it changes until the very last round. That repeated copying of untouched outer text is the waste.

## The turning point

**Claim: the text to the left of the innermost open group is never inspected until that group has collapsed to one letter, so it can sit on a stack untouched instead of being re-copied.**

Why is it never inspected? An operator only needs its own operands, and its operands lie to its right. The `&` at index 0 has nothing to do while `|(f,t)` is still unfinished; it is waiting. Waiting things that are resumed in reverse order of arrival — the most recently opened group finishes first — are the textbook use of a stack.

So we turn the observation into a single pass:

- Skip commas; they carry no information once each operand is its own stack entry.
- Any other character except `)` is pushed: operators, `(`, `t`, `f`.
- On `)`, pop letters until a `(` is on top. Those letters are exactly the operands of the group that just closed, because anything pushed after that `(` belongs to it, and every nested group inside it has already been collapsed to a single letter by its own `)`.
- Pop the `(`, pop the operator under it, compute one letter, and push that letter back. It now sits where the whole group used to be, ready to serve as an operand of the enclosing group.

There is a second, smaller insight that makes the operator step trivial. `&`, `|` and `!` only care about which values appear among the operands, not how many or in what order. `&` is false exactly when an `f` appears. `|` is true exactly when a `t` appears. `!` has one operand, so it is true exactly when the operand set is `{f}`. Collecting the popped letters into a set reduces each operator to a membership test.

```text
before ')':   ... op  (  x  y  z        <- top
on ')':       pop z, y, x into a set
              pop '(' , pop op
after:        ... r                     r = op(set)
```

One push per character, at most one pop per character. The stack height at any moment is the nesting depth of the reader's position, plus the operands collected at each level.

## Watch it work

Expression `&(|(f,t),!(f))`, indices 0 to 13. The stack is drawn bottom on the left, top on the right. The final answer from running the solution is `True`.

Frame 1 — read indices 0 to 3, all pushed.

```text
& ( | ( f , t ) , ! ( f ) )
      ^ i=3
stack: [ &  (  |  ( ]
depth:       1     2
```

Two operators are now waiting, the outer `&` and the inner `|`, each sitting on top of nothing yet.

Frame 2 — read `f`, skip `,`, read `t`.

```text
& ( | ( f , t ) , ! ( f ) )
            ^ i=6
stack: [ &  (  |  (  f  t ]
```

The inner group's operands are piled on its ledge; the comma at index 5 never touched the stack.

Frame 3 — `)` at index 7 closes `|(f,t)`.

```text
& ( | ( f , t ) , ! ( f ) )
              ^ i=7
pop t, f -> set {f,t};  pop '(' ;  pop '|'
'|' with t in set -> t
stack: [ &  (  t ]
```

The whole subtree `|(f,t)` is now the single letter `t`, sitting as the first operand of `&`.

Frame 4 — skip `,`, push `!`, `(`, `f`.

```text
& ( | ( f , t ) , ! ( f ) )
                      ^ i=11
stack: [ &  (  t  !  (  f ]
```

A second group opened on top of the first operand; the `t` underneath is untouched.

Frame 5 — `)` at index 12 closes `!(f)`.

```text
& ( | ( f , t ) , ! ( f ) )
                        ^ i=12
pop f -> set {f};  pop '(' ;  pop '!'
'!' with set == {f} -> t
stack: [ &  (  t  t ]
```

Frame 6 — `)` at index 13 closes the outer group.

```text
& ( | ( f , t ) , ! ( f ) )
                          ^ i=13
pop t, t -> set {t};  pop '(' ;  pop '&'
'&' with no f in set -> t
stack: [ t ]      answer: stack[0] == 't' -> True
```

Across every frame, each `(` on the stack had above it only letters (finished operands) and possibly one more open group. Whenever a `)` arrived, the run of letters directly above the nearest `(` was the complete operand list of the group being closed. The stack never held a half-evaluated group below a finished one.

## Why it is correct

The invariant, checked after every character: **reading the stack from bottom to top, each `(` is immediately preceded by its operator, and the letters between a `(` and the next `(` (or the top) are exactly the values of the operands of that group seen so far, each fully evaluated.**

It holds at the start trivially (empty stack). Pushing an operator or a `(` opens a new level with no operands yet, which keeps it. Pushing `t` or `f` adds an atomic operand, already fully evaluated, to the current top level. Skipping a comma changes nothing.

The interesting step is `)`. The grammar guarantees this `)` closes the most recently opened group, which is the topmost `(` on the stack. By the invariant, the letters above it are the fully evaluated values of all its operands, and since the `)` has arrived there are no more operands coming. So the set we collect is the true operand set, the operator under the `(` is the right operator, and the letter we compute is the true value of the group. We push that letter onto the level below, where it is precisely the next operand of the enclosing group. The invariant holds again.

When the string ends, every group has been closed, so the stack holds one letter: the value of the whole expression. A bare `t` or `f` input never opens a group and is returned as is.

## Cost

Time O(n): every character is pushed at most once and popped at most once; the set work for a group is proportional to the letters popped for it.

Space O(n): in the worst case (deep nesting) the stack holds a constant number of entries per level.

The brute force is O(n^2) time because of the repeated string rebuilds, O(n) space for the current string.

## Variations you will meet

- **Recursive descent.** Write `eval(i)` that reads an operator at `i`, recursively evaluates each operand, and returns the value and the next index. Same O(n), but the call stack does what our explicit stack did. Python's recursion limit bites on very deep inputs, which is why the explicit stack is safer.
- **Short-circuit evaluation.** With `&` you can stop caring after the first `f`. On a stack you cannot skip the remaining characters cheaply because you still must find the matching `)`, so the saving is constant-factor only.
- **Infix boolean expressions with precedence** (`t & f | !t`). Now you need the two-stack operator-precedence method from the calculator problems: an operand stack plus an operator stack, reducing while the operator on top binds tighter.
- **Return the expression tree instead of the value.** Push nodes instead of letters; on `)` pop children into a list and push a new node. The control flow is identical.

## What to carry forward

A `)` means "the top of the stack is now a finished sub-problem: collapse it to one value and hand it to the level below". Stacks evaluate nested things because the thing you opened last is the thing you finish first.

The next problem keeps the "push now, resolve later" stack but changes what triggers resolution: not a closing bracket, but a warmer day arriving — and the stack it builds is sorted.
