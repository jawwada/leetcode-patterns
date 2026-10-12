# Stamping The Sequence

*LeetCode 936 · Hard · Pattern: Reverse greedy (undo the last move first) · Reading time ~10 min*

## The problem

Starting from a string of len(target) '?' characters, repeatedly place stamp anywhere, overwriting the characters
beneath it. Return any sequence of at most 10 * len(target) stamp positions that produces target, or [] if impossible.

```text
Example: stamp = 'abc', target = 'ababc' -> [0, 2] (stamp at 0
  gives 'abc??', at 2 gives 'ababc'); [1, 0, 2] is also
  accepted.
```

## What the problem is really asking

You have a rubber `stamp` (a short string) and a `target` string. You begin with a blank strip of `len(target)` cells, shown as `?`. One move presses the stamp fully inside the strip at some offset, overwriting whatever was under it. Return any sequence of offsets, at most `10 * len(target)` long, that turns the blank strip into `target`, or an empty list if it cannot be done.

The answer is a sequence, not a number, which already sets this problem apart. What makes it hard is overwriting. A stamp you press early may be mostly hidden by later stamps; only a few of its letters survive into the target. Looking at the target, you cannot directly see the early stamps. You can only see the last ones.

```text
stamp = "abca", target = "aabcaca"   (n = 7, m = 4)

offset 0:  a b c a ? ? ?
offset 3:  a b c a b c a
offset 1:  a a b c a c a   = target
           ^   ^-------^ last stamp, fully visible
           only cell 0 survives from stamp 1
answer [0, 3, 1]
```

The first stamp at offset 0 left only its first letter in the final string. Nobody looking at `aabcaca` would see a stamp there.

## Do it by hand first

Try to build `"ababc"` with stamp `"abc"` by hand, forwards. Where does the first stamp go? You do not know. Instead, look at the finished target and ask a question you can answer: which stamp was pressed last? The last one is never overwritten, so it appears intact somewhere.

```text
target:  a b a b c
             [a b c]  window 2 equals the stamp exactly
             -> this was the last press
peel it:  a b ? ? ?
          [a b ?]     window 0: letters a,b match,
                      ? matches anything
             -> this was the press before
peel it:  ? ? ? ? ?   blank: done
peeled order: 2, 0  -> forward order: 0, 2
```

Your hand kept track of the current partly blanked strip and, for each window, whether every remaining letter under it agrees with the stamp. Blanks act as wildcards, because whatever was under a later stamp no longer matters. That strip of letters and wildcards is the whole state.

## The first honest attempt

Forward breadth-first search: start from `?????`, try every offset, then every offset again, until the target appears.

```text
"?????" -> "abc??" "?abc?" "??abc"
"abc??" -> "abc??" "aabc?" "ababc" <- found
            ^ each level multiplies by n-m+1
state space: every mix of letters and ? -> exponential
```

Exponential in `n`. The waste is structural: going forwards you cannot tell which presses will be overwritten later, so you must explore every order, and most orders are equivalent once overwriting is taken into account.

The tempting forward greedy is: "find every window where the target equals the stamp exactly, press those, and declare the rest impossible." On `"ababc"` the only exact window is offset 2. Cells 0 and 1 (`a b`) are not inside any exact window, so this greedy says impossible. But `[0, 2]` works: the first press at 0 is partly hidden by the press at 2. The forward greedy fails exactly because it looks for complete stamps, and early stamps are never complete in the final string.

## The turning point

**Claim: run time backwards. The last press is visible intact; replace it with wildcards and repeat. Erasing a matching window never hurts, so you can peel any matching window in any order.**

Reverse thinking turns an invisible question into a visible one. Forwards: "which press will survive?" is unknowable. Backwards: "which window, right now, matches the stamp, treating `?` as anything?" is a direct check.

Why greedy peeling is safe, in one sentence: peeling only ever turns letters into `?`, and a `?` matches every stamp letter, so a window that matched before still matches after, and new windows may start to match. The set of peelable windows only grows. You never lose an option by peeling early, so there is no order to regret.

```text
before peel:   a [a b c a] c a      window 1 matches
after peel:    a [? ? ? ?] c a
window 3:            [? ? c a]  now matches too
(? ? matched by a b, c a by c a)
```

Two practical rules follow. A window counts as progress only if it erases at least one real letter, or the loop could spin forever on an already blank window. And a window that has been peeled is fully blank, so it is marked done and never examined again. If a full pass over all windows erases nothing while letters remain, no stamp could have been the last one on those letters, so it is impossible.

At the end, reverse the list of peeled offsets to get a forward pressing order.

## Watch it work

Example: `stamp = "abca"`, `target = "aabcaca"`. Windows are offsets 0..3. The solution returns `[0, 3, 1]`.

Frame 1. Start of pass 1. Nothing erased.

```text
idx:    0 1 2 3 4 5 6
t:      a a b c a c a       stars 0
win 0: [a a b c] vs a b c a -> a!=b at idx1: no
moves []
```

Window 0 has a live letter that disagrees with the stamp.

Frame 2. Pass 1, window 1: `a b c a` equals the stamp. Peel it.

```text
idx:    0 1 2 3 4 5 6
t:      a ? ? ? ? c a       stars 4
          [-------] win 1 erased 4
moves [1]   done[1] = True
```

This is the last press in forward time.

Frame 3. Pass 1, window 2: cells `? ? ? c` against `a b c a`. The live `c` sits under stamp letter `a`.

```text
idx:    0 1 2 3 4 5 6
t:      a ? ? ? ? c a
             [? ? ? c]  c vs a -> no
moves [1]
```

Frame 4. Pass 1, window 3: cells `? ? c a` against `a b c a`. Both live letters agree. Peel.

```text
idx:    0 1 2 3 4 5 6
t:      a ? ? ? ? ? ?       stars 6
              [? ? c a] win 3 erased 2
moves [1, 3]   done[3] = True
```

Window 3 only became peelable because window 1's blanks now act as wildcards.

Frame 5. Pass 2 (pass 1 made progress, so loop again). Window 0: only the `a` at idx 0 is live, and it matches stamp letter `a`. Peel.

```text
idx:    0 1 2 3 4 5 6
t:      ? ? ? ? ? ? ?       stars 7 = n
       [a ? ? ?] win 0 erased 1
moves [1, 3, 0]
```

Window 2 is then checked, has no live letters, and is skipped without counting as progress.

Frame 6. All cells are blank. Reverse the peel order.

```text
peeled:  [1, 3, 0]
forward: [0, 3, 1]
```

Frame 7. Replay forwards to confirm.

```text
start      ? ? ? ? ? ? ?
press 0    a b c a ? ? ?
press 3    a b c a b c a
press 1    a a b c a c a   = target
```

Across the frames the strip only gained `?`s, and every peeled window had all its live letters equal to the stamp. Each pass that continued erased at least one letter.

## Why it is correct

There are three things to show: the output, when returned, really builds the target; the greedy never gets stuck on a solvable input; and the length limit holds.

**Replay is right.** Reverse the peel order to get the forward order. In forward time, each cell's final letter is set by the last press covering it. In backward time, that is the first peel that covered it while it was still a live letter, and a peel only happens when every live letter in the window equals the stamp letter above it. So each cell ends with its target letter. Every cell gets erased eventually (stars reaches `n`), so every cell is covered by some press, and no `?` survives.

**Never stuck on a solvable input.** This is the invariant argument, and it is where the greedy is justified. Suppose some valid forward sequence `p1, ..., pk` builds the target, and at some point our strip still has live letters. Look at the latest press `pj` in that valid sequence whose window still contains a live letter. Any live letter in its window was not covered by a later press, because every later press's window is already fully blank (otherwise a later press would have been chosen). So each live letter in `pj`'s window is exactly what `pj` wrote: the stamp letter. That window matches and has a live letter, so the pass will peel something. Erasing only adds wildcards, so this argument holds again after any peel, in any order. This is the exchange idea in disguise: any peel we choose can be swapped into the valid sequence's reverse without breaking it, because peeling never removes an option.

**Contrapositive.** If a full pass erases nothing while letters remain, then no valid sequence exists, and returning `[]` is right.

**Length.** Each window is peeled at most once (it is marked done), so the answer has at most `n - m + 1 <= n` offsets, well under `10 * n`.

## Cost

Time O(n * (n - m) * m) in the worst case. Each productive pass erases at least one letter, so there are at most `n` passes, and each pass checks up to `n - m + 1` windows at `m` cells each. In practice most windows are marked done quickly.

Space O(n) for the mutable strip, the done flags and the move list.

A faster O(n * m) version precomputes, for each window, which of its cells still mismatch, and keeps a queue of cells that just became `?`; when a cell blanks, only the at most `m` windows containing it are rechecked. Same reverse greedy, event-driven instead of pass-driven.

## Variations you will meet

- **Minimum number of presses.** The reverse greedy finds a valid sequence but not necessarily the shortest one; minimising presses is a much harder search problem and is not what the interviewer usually wants.
- **Strange Printer.** Also overwriting, but each print is a run of a single character of any length, and you minimise the count; that one needs interval DP rather than reverse greedy.
- **Undo-based reasoning elsewhere.** "Reverse the process" shows up in Broken Calculator and Reaching Points (work backwards from the target, where the previous step is forced), and in Burst Balloons (choose the last balloon, not the first); whenever the last step is easiest to identify, run time backwards.
- **Multiple different stamps.** The same peel works with a choice of stamp per window, since any matching window can still be peeled safely; the check per window grows by the number of stamps.

## What to carry forward

When the forward choice is hidden by later moves, run the process backwards: the last move is visible, undoing it only makes the rest easier, so the greedy can never paint itself into a corner. That closes the Greedy chapter. Across all fourteen problems the recurring move was the same: find the quantity a greedy step can never make worse (a reach, a staircase, a boundary flow, a rightmost pin, a cycle count, a growing set of wildcards), prove it with an exchange or an invariant, and let one pass do the rest.
