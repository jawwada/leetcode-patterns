# Longest Valid Parentheses

*LeetCode 32 · Hard · Pattern: Stack of indices with a barrier · Reading time ~10 min*

## The problem

Given a string of '(' and ')', return the length of the longest well-formed contiguous substring.

```text
Example: "(()" -> 2; ")()())" -> 4 ("()()"); "" -> 0.
```

## What the problem is really asking

You get a string of `(` and `)` only. Find the longest contiguous substring that is a well-formed bracket sequence, and return its length.

In Valid Parentheses, the first problem of this chapter, the question was yes or no for the whole string. Here the answer is a length, and the string is allowed to be broken in places; you have to find the longest unbroken stretch. Two things make it hard. Valid stretches can be *nested* (`(())`) or *chained* (`()()`), and a chain can be glued together across what looked like separate matches. And the stretch must be contiguous, so a single stray `)` cuts everything in two.

```text
i:   0 1 2 3 4 5 6
s:   ( ) ) ( ( ) )
     '-'   '-----'
     len 2   len 4      answer: 4
         ^
         stray ')' at i=2 splits the string
```

The `)` at index 2 has nothing to match. Nothing on its left can join anything on its right. On the right, `(())` is a nested valid run of length 4.

## Do it by hand first

Read `())(())` left to right with a pencil. When you see a `(`, mark it as open. When you see a `)`, connect it to the most recent unconnected `(`. If there is none, draw a wall.

```text
i:   0 1 2 3 4 5 6
s:   ( ) ) ( ( ) )
     |_|   | |_| |
           |_____|
         ||
         wall at 2
run ending at i=1: from 0 to 1   -> 2
run ending at i=5: from 4 to 5   -> 2
run ending at i=6: from 3 to 6   -> 4
```

Now the key question: when you close a pair at index `i`, how far back does the valid run go? It goes back past the `(` you just matched, and past any complete pairs immediately before it, until it hits either an `(` that is still open (it cannot be part of a valid run that has already ended) or a wall. Your hand, without noticing, was looking at *the most recent thing that is not yet matched*. Open `(` still waiting and walls are exactly the unmatched positions. The run ending at `i` starts right after the latest unmatched position. That latest unmatched position is what a stack of indices will hold on top.

## The first honest attempt

For every start index `i`, scan right with a balance counter: `(` adds 1, `)` subtracts 1. Each time the balance returns to 0, `s[i..j]` is valid; record its length. If the balance goes negative, a stray `)` has appeared and no longer substring from `i` can be valid, so stop.

That is O(n^2) time, O(1) space. On a string like `()()()()` every start index rescans most of the string.

```text
s:      ( ) ( ) ( ) ( )
from 0: ( ) ( ) ( ) ( )   finds pairs at 1,3,5,7
from 2:     ( ) ( ) ( )   finds pairs at 3,5,7 AGAIN
from 4:         ( ) ( )   finds pairs at 5,7 AGAIN
                ~~~~~~~
every scan re-matches the same pairs
```

Each pair `(i, j)` is a fact about the string that does not depend on where you started reading, yet each scan re-derives it. The waste is re-matching pairs.

## The turning point

**Claim: in a single left-to-right pass, a `)` matches the most recent unmatched `(`, and after that match the valid run ending here extends back exactly to the most recent position that is still unmatched.**

The first half is the classic bracket stack: push the index of every `(`, pop on `)`. Every pair is matched exactly once.

The second half is what turns matching into measuring. After popping the partner, look at the new top of the stack. It is the most recent index that has not been matched. Every index between it and `i` is matched, and matched *within* that range (a pair cannot straddle an unmatched `(`, because that `(` would have been matched first). So `s[top+1 .. i]` is valid, and it cannot extend further left because `top` itself is unmatched. The length is `i - top`.

What if the stack is empty after the pop? Then the run goes back to the start of the string, or to the last stray `)`. To make "the most recent unmatched position" always exist, put a barrier at the bottom of the stack:

- Start with `stack = [-1]`. The `-1` is a virtual wall just before the string.
- On `(`: push its index.
- On `)` with an open `(` above the wall: pop it, then `best = max(best, i - stack[-1])`.
- On `)` with only the wall left: this `)` is unmatched; it becomes the new wall, `stack[0] = i`.

The barrier is never popped. It slides right only when a stray `)` makes everything before it irrelevant.

Notice the stack holds indices in increasing order, a rising staircase of positions. When a `)` arrives it knocks off the top step, and the step below tells it where its run starts. That is the same picture as the histogram problems coming next.

## Watch it work

`s = "())(())"`. Each frame shows the string, `i`, and the stack as a staircase: each step's `*` sits under the index it stores (the wall at -1 sits just left of index 0). Running the solution returns 4.

Frame 1 — `i = 0` is `(`: push 0.

```text
i:        0 1 2 3 4 5 6
s:        ( ) ) ( ( ) )
          ^ i=0
stack, bottom first (* = index):
  wall  *                 -1
  open  ==*               0  <- top
best = 0
```

Frame 2 — `i = 1` is `)`: pop 0; the new top is the wall -1.

```text
i:        0 1 2 3 4 5 6
s:        ( ) ) ( ( ) )
            ^ i=1
stack, bottom first (* = index):
  wall  *                 -1  <- top
pop 0, len = 1 - (-1) = 2, best = 2
```

The run `()` reaches all the way back to the wall.

Frame 3 — `i = 2` is `)` with only the wall left.

```text
i:        0 1 2 3 4 5 6
s:        ( ) ) ( ( ) )
              ^ i=2
stack, bottom first (* = index):
  wall  ======*           2  <- top
only the wall left: wall := 2
best = 2
```

The stray `)` replaces the wall. Nothing to its left can ever join a run again.

Frame 4 — `i = 3, 4` are both `(`: push.

```text
i:        0 1 2 3 4 5 6
s:        ( ) ) ( ( ) )
                  ^ i=4
stack, bottom first (* = index):
  wall  ======*           2
  open  ========*         3
  open  ==========*       4  <- top
best = 2
```

A rising staircase: two opens waiting on top of the wall.

Frame 5 — `i = 5` is `)`: pop 4; the new top is the open `(` at 3.

```text
i:        0 1 2 3 4 5 6
s:        ( ) ) ( ( ) )
                    ^ i=5
stack, bottom first (* = index):
  wall  ======*           2
  open  ========*         3  <- top
pop 4, len = 5 - 3 = 2, best = 2
```

The run `()` at 4..5 stops at index 3, because that `(` is still waiting.

Frame 6 — `i = 6` is `)`: pop 3; the new top is the wall at 2.

```text
i:        0 1 2 3 4 5 6
s:        ( ) ) ( ( ) )
                      ^ i=6
stack, bottom first (* = index):
  wall  ======*           2  <- top
pop 3, len = 6 - 2 = 4, best = 4
```

Now the run swallows the inner pair and reaches back to the wall: `(())`, length 4.

Across all frames the stack was a strictly rising staircase of indices with exactly one wall at the bottom. Every index between the top step and `i` was matched, and every pop measured a run from the step below to `i`.

## Why it is correct

**Invariant.** After processing `s[0..i]`: the stack bottom is the index of the last unmatched `)` (or -1), the entries above it are the indices of the `(` that are still unmatched, in increasing order, and every other index in `s[0..i]` after the wall is matched to a partner inside `s[0..i]`.

It holds initially (wall -1, nothing else). A `(` is unmatched when read, so pushing it keeps the invariant. A `)` with an open `(` above the wall matches the most recent open one, the top; popping it marks both as matched. A `)` with no open `(` is unmatched forever, and since nothing to its left can pair with anything to its right across an unmatched `)`, moving the wall to it is exactly right.

**The popped element's answer is fixed at pop time.** When `(` at index `p` is popped by `)` at `i`, its partner is `i`, permanently: brackets matched by the "most recent open" rule are the only legal pairing. And at that same moment we measure the run ending at `i`. Every index strictly between the new top `t` and `i` is matched with a partner in that range (by the invariant, unmatched indices are only on the stack, and `t` is the latest of them), so `s[t+1..i]` is balanced, hence valid. It cannot extend to include `t`: `t` is either a wall or an open `(` that is unmatched at least up to `i`. So `i - t` is the longest valid substring ending at `i`, and that value never needs revising.

Every valid substring ends at some `)` that was matched, so taking the maximum over all pops covers the true answer. A `)` that hits the wall ends no valid substring, so skipping it loses nothing.

## Cost

Time O(n): each index is pushed at most once and popped at most once; the wall is overwritten in O(1).

Space O(n): a string of all `(` puts every index on the stack.

The brute force is O(n^2) time, O(1) space. There is also an O(1)-space method with two counter sweeps (left to right, then right to left), at the same O(n) time.

## Variations you will meet

- **Two-counter sweep, O(1) space.** Scan left to right with `open` and `close` counts: equal means a valid run of `2*close`; `close > open` resets both. That misses runs like `(()` where opens never fall back to equal, so sweep right to left as well with the roles swapped.
- **DP on ends.** `dp[i]` = longest valid substring ending at `i`. For `s[i] == ')'`, look at `s[i-1]`: if `(`, `dp[i] = dp[i-2] + 2`; if `)`, check the character before the run ending at `i-1`. The stack version computes the same `dp[i]` as `i - top`.
- **Return the substring itself.** Record `(top + 1, i)` whenever `best` improves.
- **Multiple bracket types.** On `)` check that the top is the matching opener; a mismatch is a wall, and everything on the stack is cleared down to it.

## What to carry forward

Stack *indices*, not characters, and keep a barrier at the bottom; then "pop, then look at the new top" measures how far back the current structure reaches. The span from the step below to the current index is the answer for the popped item.

The next problem uses exactly that measurement: in a histogram, popping a bar and reading the new top gives the bar's left wall, while the current index is its right wall.
