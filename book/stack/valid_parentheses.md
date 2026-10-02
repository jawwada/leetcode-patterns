# Valid Parentheses

*LeetCode 20 · Easy · Pattern: Stack matching · Reading time ~5 min*

## What the problem is really asking

You get a string made only of the six characters `( ) [ ] { }`. Decide whether it is well formed: every opener is
eventually closed by a bracket of the same type, and closings happen in the reverse order of openings, so groups nest
inside each other instead of overlapping.

The answer is a single yes or no. What makes it more than counting is the word "order". `([)]` has one of each opener
and one of each closer, yet it is invalid because the `)` tries to close the `(` while the `[` opened after it is still
open. The groups cross instead of nesting.

```text
"{[]()}"   valid          "([)]"   invalid
 {      }                  (   )
  [ ]( )                    [   ]
 groups nest               groups cross
```

## Do it by hand first

Take `{[]()}` and read it left to right with a pencil. When you see an opener you cannot judge it yet, so you remember it.
When you see a closer, you look back for the opener it should match. Which one? Not the first one you wrote down, but the
latest one that has not been crossed off yet. You cross both off and move on.

```text
{ [ ] ( ) }
{ [ ]          ] closes the latest open: [   cross off
{       ( )    ) closes the latest open: (   cross off
{           }  } closes the latest open: {   cross off
nothing left open -> valid
```

What your hand kept track of was a list of openers still waiting, and you only ever touched its newest end. That is a
stack, and the "latest open opener" is its top.

## The first honest attempt

A natural first idea: an innermost pair like `()` or `[]` is always adjacent, so delete adjacent matched pairs until
nothing changes. If the string becomes empty, it was valid.

Each deletion costs an O(n) scan and rebuild, and there are n/2 of them: O(n^2) time.

```text
pass 1: { [ ] ( ) }   scan from start, find [], delete
pass 2: { ( ) }       scan from start AGAIN, find (), delete
pass 3: { }           scan from start AGAIN, find {}, delete
pass 4: ""            empty -> valid
        ^
        the leading "{" was re-read on every pass
```

After a deletion, the only place a new adjacent pair can appear is right where the deletion happened: the character just
before the gap now touches the character just after it; the prefix before it was already checked,
yet every pass re-reads it.

## The turning point

**Claim: a closer is legal exactly when it matches the most recently opened bracket that is still open.**

Why? Suppose the most recent still-open opener is `[` and a `)` arrives. If that `)` closed some earlier `(`, the `[` would
be left open inside a group that has already ended, which is the crossing picture above. So the only legal partner for any
closer is the newest unclosed opener.

"Newest first, and once it is gone the previous newest is next" is the definition of last in, first out. So keep the open
openers on a stack. Push each opener. On a closer, the stack must be non-empty and its top must be the matching opener;
pop it. At the end the stack must be empty, or some opener was never closed.

## Watch it work

Input `{[]()}`. The cursor `^` marks the character being read; the stack is drawn as a column with the top at the top.

```text
Frame 1:  { [ ] ( ) }        stack
          ^                  | { | <- top
```

`{` is an opener; it cannot be judged yet, so it is pushed.

```text
Frame 2:  { [ ] ( ) }        stack
            ^                | [ | <- top
                             | { |
```

`[` is pushed on top. It is now the nearest unresolved opener.

```text
Frame 3:  { [ ] ( ) }        stack
              ^              | { | <- top
          ] matches top [ -> pop
```

The closer `]` meets `[` at the top, so both are resolved and `{` is exposed again.

```text
Frame 4:  { [ ] ( ) }        stack
                ^            | ( | <- top
                             | { |
```

`(` is pushed; the stack grows back to two waiting openers.

```text
Frame 5:  { [ ] ( ) }        stack
                  ^          | { | <- top
          ) matches top ( -> pop
```

`)` matches `(` and pops it.

```text
Frame 6:  { [ ] ( ) }        stack
                    ^        (empty)
          } matches top { -> pop; end, empty -> True
```

The final `}` closes `{`, the scan ends with an empty stack, so the answer is True. Across every frame the stack held
exactly the openers seen so far that had not yet been closed, oldest at the bottom.

## Why it is correct

The invariant: after reading any prefix, the stack holds the unmatched openers of that prefix, in the order they were
opened. It is true at the start (empty prefix, empty stack). A push keeps it true, since a new opener is unmatched and
newest. On a closer, the problem's nesting rule says it must close the newest unmatched opener, which is the top; if the
top is the wrong type or missing, no valid completion of the string can fix the problem, so returning False at once is
safe. If it matches, popping keeps the invariant.

At the end, the string is valid exactly when no closer failed and no opener is left unmatched, which by the invariant is
"the stack is empty".

## Cost

Time O(n): each character is pushed at most once and popped at most once.
Space O(n): a string of only openers puts all of them on the stack.

## Variations you will meet

- **Only one bracket type.** All stack entries are identical, so the stack collapses into a counter of open brackets.
  That is the next problem.
- **Minimum remove to make valid (LeetCode 1249).** Push the *indices* of openers; stray closers and leftover openers
  are the characters to delete.
- **Longest valid parentheses (LeetCode 32).** Store indices instead of characters, and the distance between the current
  index and the new top measures a valid run. It returns later in this chapter.

## What to carry forward

A closer can only meet the newest unclosed opener, so openers wait on a stack and the top is the only candidate. The
next problem has only `(` and `)`, so every entry on the stack is the same and the whole stack shrinks to a number.
