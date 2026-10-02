# Min Stack

*LeetCode 155 · Medium · Pattern: Stack with auxiliary state · Reading time ~6 min*

## What the problem is really asking

Build a stack with the usual `push`, `pop` and `top`, plus one extra question, `getMin`: what is the smallest value
currently on the stack? All four must run in O(1) time.

The answer is a data structure, not a number. What makes it hard is `pop`. Keeping the minimum while values only arrive
is easy: compare and keep the smaller. But when the current minimum is popped, you need the *previous* minimum, the
smallest of what remains, and you cannot afford to search for it.

```text
push 5, push 3, push 7          pop, pop
+---+                           
| 7 |                           
+---+                           
| 3 | <- min 3                  
+---+                           +---+
| 5 |                           | 5 | <- min must become 5
+---+                           +---+
                                where did "5" come from?
```

## Do it by hand first

Push 5, 3, 7, 3 onto a stack drawn on paper, and next to each plate write down the smallest plate at or below it. That
is easy to compute at push time: it is the smaller of the new value and the note written next to the plate below.

```text
 value | min at or below
-------+----------------
   3   |   3     <- top: getMin reads 3
   7   |   3
   3   |   3
   5   |   5
```

Now pop twice. The top two rows vanish, and the note on the new top row says 3, which is right: the stack is `5 3`, and
its minimum is 3. Pop once more and the note says 5. You never recomputed anything. Your hand kept a second column of
"minimum so far, measured from the floor", one entry per plate.

## The first honest attempt

Use a plain list. `push`, `pop` and `top` are O(1). For `getMin`, call `min()` over the whole list: O(n) per call.

```text
stack: 5 3 7 3 ...            getMin -> scan 5 3 7 3 ...
                               getMin -> scan 5 3 7 3 ... again
push 9                         getMin -> scan 5 3 7 3 ... 9
       ^^^^^^^
       this prefix did not change between calls,
       yet its minimum is recomputed every time
```

The obvious patch, one variable `cur_min`, fixes `getMin` but breaks `pop`: when the popped value equals `cur_min`, the
variable is now wrong and the only way to repair it is a full scan. So the brute force wastes time on a prefix whose
answer never changed, and the single-variable patch loses information that it then has to recompute.

## The turning point

**Claim: while a value sits on the stack, the minimum of everything at or below it never changes.**

Why? A stack is only modified at the top. Everything underneath a value v was there before v was pushed and will still be
there, untouched, until v is popped. So "minimum of v and everything below it" is a fixed number for v's entire life on
the stack. Compute it once, at push time, and store it next to v.

That turns the stack into a stack of pairs `(value, min_so_far)`, where `min_so_far = min(value, previous top's
min_so_far)`. Now:

- `getMin` is the top pair's second field: O(1).
- `pop` removes the top pair. The new top pair's second field is the minimum of what remains, because that is precisely
  what it was computed to be when it was pushed. Nothing to repair.
- `push` is one comparison with the current top's stored minimum.

The second column is non-increasing from floor to ceiling: each entry is the min of the one below and a new value, so it
can only stay the same or drop. Picture two parallel columns that always move together:

```text
  value   min      (rows move as a unit)
  +---+  +---+
  | 3 |  | 3 |  <- top: getMin = 3
  +---+  +---+
  | 7 |  | 3 |
  +---+  +---+
  | 3 |  | 3 |
  +---+  +---+
  | 5 |  | 5 |
  +---+  +---+
```

This is a general pattern, not a trick for minimum: any summary of "everything at or below me" that can be computed from
the summary of the element below plus my own value (min, max, sum, gcd, count of negatives) can ride along on each
entry.

## Watch it work

Operations `push 5, push 3, push 7, push 3, pop, pop, pop` (written `+v` below), with `getMin` after each step. The cursor
marks the operation just executed; the stack is drawn as pairs `| value | min |`, top at the top.

```text
Frame 1: push 5, push 3
ops: +5 +3 +7 +3 pop pop pop
     ^  ^
  value min
  | 3 | 3 | <- top
  | 5 | 5 |
  getMin = 3
```

The first push has nothing below it, so it stores itself as the minimum. Pushing 3 stores min(3, 5) = 3.

```text
Frame 2: push 7
ops: +5 +3 +7 +3 pop pop pop
           ^
  value min
  | 7 | 3 | <- top
  | 3 | 3 |
  | 5 | 5 |
  getMin = 3
```

7 is larger than the minimum below it, so it inherits 3 instead of storing 7.

```text
Frame 3: push 3 (a duplicate)
ops: +5 +3 +7 +3 pop pop pop
              ^
  value min
  | 3 | 3 | <- top
  | 7 | 3 |
  | 3 | 3 |
  | 5 | 5 |
  getMin = 3
```

The second 3 gets its own row with min 3. Duplicates need no special case because every row carries its own note.

```text
Frame 4: pop (removes the top 3)
ops: +5 +3 +7 +3 pop pop pop
                 ^
  value min
  | 7 | 3 | <- top
  | 3 | 3 |
  | 5 | 5 |
  getMin = 3
```

One copy of 3 leaves; the row now on top still says 3, which is right because another 3 is below it.

```text
Frame 5: pop (removes 7)
ops: +5 +3 +7 +3 pop pop pop
                     ^
  value min
  | 3 | 3 | <- top
  | 5 | 5 |
  getMin = 3
```

Popping 7 changes nothing about the minimum; the 3 row is exposed with its note intact.

```text
Frame 6: pop (removes 3)
ops: +5 +3 +7 +3 pop pop pop
                         ^
  value min
  | 5 | 5 | <- top
  getMin = 5
```

The last 3 leaves and the note on the 5 row, written back in Frame 1, is already correct.

Across all frames the right column was non-increasing from floor to top, and its top always equalled the true minimum
of the left column. No frame ever looked below the top row.

## Why it is correct

Invariant: for every row i, `min[i] = min(value[0..i])`. Push establishes it for the new row because `min(value[0..i]) =
min(value[i], min(value[0..i-1])) = min(value[i], min[i-1])`, and rows below are untouched. Pop removes the top row and
touches nothing else, so every remaining row still satisfies it. Therefore `getMin`, which returns `min[top]`, returns
`min(value[0..top])`, the minimum of the entire stack.

The single-variable approach failed exactly because it stored only `min[top]` and threw away `min[top-1]`, which is the
value needed after a pop. Storing one per row keeps every value we might fall back to.

## Cost

Time O(1) for push, pop, top and getMin: each is a constant number of list operations.
Space O(n): one extra integer per element. The common optimisation is a second "min stack" that only pushes when the new
value is less than or equal to the current minimum; that saves space when the minimum rarely changes, at the price of
the classic duplicate bug (pushing on `<` instead of `<=` loses the second copy of a minimum after one pop).

## Variations you will meet

- **Max stack with popMax (LeetCode 716).** A ride-along max gives `peekMax` in O(1), but removing the max from the
  middle breaks the "only the top changes" premise. You need a sorted structure or a heap with lazy deletion beside a
  doubly linked list.
- **Min queue / sliding window minimum.** A queue changes at both ends, so a per-entry summary goes stale. Either build a
  queue from two min stacks (amortised O(1)) or use a monotonic deque.
- **O(1) extra space.** Store `value - min` differences in a single stack and decode the previous minimum on pop. Clever,
  but watch integer overflow in other languages.
- **Any associative summary.** Sum, max, gcd, or "count of negatives" ride along exactly like min.

## What to carry forward

Because a stack only changes at its top, anything computed about the elements below an entry stays true while that entry
lives; store it beside the entry. The next problem keeps the stack of values but lets an operator consume the top two.
