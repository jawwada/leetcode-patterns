# Minimum Add to Make Parentheses Valid

*LeetCode 921 · Medium · Pattern: Balance counter (stack collapsed to a count) · Reading time ~6 min*

## The problem

s contains only '(' and ')'. In one move you may insert a single parenthesis anywhere. Return the minimum number of
insertions that make s valid.

```text
Example: s = "())" -> 1; s = "(((" -> 3; s = "()))((" -> 4.
```

## What the problem is really asking

The string holds only `(` and `)`. You may insert parentheses anywhere, one per move. What is the fewest insertions that
make the string balanced?

The answer is a count. It is not "how far apart are the numbers of `(` and `)`", and seeing why is the whole problem.
Take `)(`: one of each, yet it needs two insertions, because the `)` comes before anything that could open it and the `(`
comes after anything that could close it. Position matters, not just totals.

```text
s = "())(("
       ^ this ) has no ( before it that is still open
        ^^ these ( have no ) after them

fix:  ( ) ( ) ( ( ) )         +1 "(" before the stray ")"
          ^         ^ ^       +2 ")" at the end
answer 3
```

## Do it by hand first

Take `()))((`, length six. Read left to right, match each `)` with an open `(` before it if there is one, and circle any
character that cannot be matched.

```text
index:  0 1 2 3 4 5
char:   ( ) ) ) ( (
        `-'          0 and 1 match
            x x      2 and 3: no open "(" left -> stray
                x x  4 and 5: never closed     -> stray
4 strays -> each needs one partner -> answer 4
```

Each circled character needs exactly one inserted partner: a stray `)` gets a `(` right before it, a leftover `(` gets a
`)` at the end. While reading, your hand tracked only one fact: how many `(` were currently open. It did not matter which
`(` they were, since they are all identical.

## The first honest attempt

Use the deletion trick from Valid Parentheses: repeatedly remove every adjacent `()` until none remains. What survives has
the shape `)))...(((`, every character in it is unmatched, and the answer is its length.

```text
round 1:  ( ) ) ) ( (   -> remove "()"  -> ) ) ( (
round 2:  ) ) ( (       -> no "()"      -> stop
leftover length 4 -> answer 4

worse case "((((()))))":
round 1 rebuilds 8 chars, round 2 rebuilds 6, ... the
outer characters are copied again on every round
```

Each round costs O(n) to rebuild the string and there can be up to n/2 rounds, so O(n^2) time. The cancellations it
performs are exactly the ones a single left-to-right stack pass would perform, only spread over many slow rounds.

## The turning point

**Claim: the stack from Valid Parentheses would only ever hold `(` characters, so its height is all you need.**

With one bracket type, the type check on a closer disappears: any open `(` matches any `)`. The stack then becomes a
column of identical `(` symbols, and a column of identical symbols carries no information except its height. So replace it
with an integer `open`: push becomes `open += 1`, pop becomes `open -= 1`, and "stack is empty" becomes `open == 0`.

The second half of the insight is what to do on a failure. In Valid Parentheses a `)` arriving at an empty stack ended the
game. Here it costs one insertion, and it is safe to pay that cost right away. A `)` that arrives when `open == 0` can
never be matched by anything to its right, because a `(` that comes later cannot close something earlier. Its partner
must be inserted before it. So add one to a second counter, `adds`, and leave `open` at zero.

At the end, `open` counts the `(` that were never closed. Each needs one `)` appended. The answer is `adds + open`.

Picture the balance as a mountain path. `(` steps up, `)` steps down. A valid string never goes below sea level and ends
at sea level. Each time the path would dip below sea level we clip it (one insertion) and keep walking at zero; whatever
height remains at the end is the number of `)` to append.

```text
s = "()))(("     open after each step, clipped at 0

2 |                 *
1 |  *           *
0 +-----*--x--x--------- sea level
     (  )  )  )  (  (
           ^  ^ would go below 0: clip, adds += 1
end: height 2 -> append 2 ")"; adds 2 -> total 4
```

## Watch it work

Input `()))((`. The would-be stack of open `(` is drawn as a column whose height is `open`; `adds` counts stray `)`.

```text
Frame 1:  ( ) ) ) ( (       would-be stack    open adds
          ^                 | ( | <- top      1    0
```

The first `(` opens; height 1.

```text
Frame 2:  ( ) ) ) ( (       would-be stack    open adds
            ^               (empty)           0    0
```

`)` finds an open `(` and cancels it; we are back at sea level.

```text
Frame 3:  ( ) ) ) ( (       would-be stack    open adds
              ^             (empty)           0    1
          ) with open == 0: stray, insert "(" before it
```

Nothing is open, so this `)` can never be matched from the right. Count one insertion and stay at zero.

```text
Frame 4:  ( ) ) ) ( (       would-be stack    open adds
                ^           (empty)           0    2
```

Same situation again: another stray `)`, another insertion.

```text
Frame 5:  ( ) ) ) ( (       would-be stack    open adds
                  ^         | ( | <- top      1    2
```

A new `(` opens. It cannot rescue the earlier strays, because they lie to its left.

```text
Frame 6:  ( ) ) ) ( (       would-be stack    open adds
                    ^       | ( | <- top      2    2
                            | ( |
          end: answer = adds + open = 2 + 2 = 4
```

The scan ends with two unclosed `(`, so two `)` must be appended. The answer is 4. Throughout, `open` stayed equal to the
height the explicit stack would have had, and `adds` never decreased: a stray `)` is a permanent cost.

## Why it is correct

Two facts give a lower bound. Every `)` that finds `open == 0` has no unmatched `(` to its left, so any valid completion
must insert a `(` somewhere before it, and different strays need different insertions since one `(` closes only one `)`.
Likewise every `(` still open at the end needs a distinct `)` inserted after it. So at least `adds + open` insertions are
required.

The bound is also achievable: insert one `(` immediately before each stray `)` and append `open` copies of `)` at the
end. Now the running balance never goes negative and ends at zero, which is exactly the condition for a balanced string
with one bracket type. Greedy matching (always cancel when something is open) never hurts, because matching a `)` with an
open `(` now leaves fewer unmatched characters than leaving both for later.

## Cost

Time O(n): a single pass, constant work per character.
Space O(1): two integers replace the O(n) stack. Compared with Valid Parentheses, the time is the same and the space
dropped from O(n) to O(1), purely because one bracket type makes the stack contents redundant.

## Variations you will meet

- **Several bracket types.** The counter is no longer enough because type matters. Go back to a real stack; but note
  that "minimum insertions" with mixed types is a harder interval-DP problem, since a mismatch is no longer fixed by a
  single insertion.
- **Minimum remove to make valid (LeetCode 1249).** Same scan, but you must output the string. Keep a stack of *indices*
  of open `(`; the stray `)` and the leftover indices are the characters to delete.
- **Minimum insertions to balance with "))" as the closer (LeetCode 1541).** Each `(` needs two `)`. The counter now
  counts needed `)` characters, and an odd count at a `(` forces an extra insertion.
- **Check if a string with `*` wildcards can be valid (LeetCode 678).** Track a range `[low, high]` of possible open
  counts instead of a single number.

## What to carry forward

When every item on a stack is identical, keep only its height; a stray closer is paid for immediately, leftover openers
at the end. The next problem keeps a real stack but asks it a new question: what is the smallest value on it, in O(1).
