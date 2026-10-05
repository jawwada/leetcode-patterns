# Implement Queue using Stacks

*LeetCode 232 · Easy · Pattern: Two stacks make a queue (lazy transfer) · Reading time ~6 min*

## The problem

Build a FIFO queue with push, pop, peek and empty using only stack operations (push to top, pop/peek from top, size,
is-empty).

```text
Example: push(1); push(2); peek() -> 1; pop() -> 1; empty() ->
  False.
```

## What the problem is really asking

Build a first-in, first-out queue with `push(x)` (join the back), `pop()` (remove and return the front), `peek()` (read
the front) and `empty()`, using only stack operations: push to the top, pop or peek the top, size, is-empty.

The awkward part: a stack hands you the *newest* item, and a queue must hand you the *oldest*, buried at the bottom.

```text
push 1, 2, 3 onto one stack       queue wants:
   | 3 | <- top: what a stack       pop -> 1
   | 2 |    gives you              the oldest, at
   | 1 | <- bottom                 the bottom
```

## Do it by hand first

Put three plates on a table, labelled 1, 2, 3, stacked in that order. Someone asks for "the plate that arrived first".
You cannot slide it out from the bottom, so you lift plates off one by one and set them down in a second pile: 3, then
2, then 1. The second pile now has 1 on top.

```text
pile A    pile B            pile A    pile B
| 3 |                                 | 1 | <- top
| 2 |              lift ->            | 2 |
| 1 |                                 | 3 |
```

Hand over plate 1. Plate 4 arrives: on pile B it would be served before 2 and 3, so it goes on pile A. Requests are
served from B, and only when B is empty do you lift A over again.

Your hands kept two piles: one for arrivals, one already flipped into serving order.

## The first honest attempt

Keep one stack with the *oldest item on top*, so pop and peek are trivial. To push `x`, you must slide it underneath
everything: pour the whole stack into a helper, push `x`, pour everything back.

```text
push 4 into main = [3, 2, 1] (1 on top)

main      helper            main      helper     main
| 1 |                                 | 3 |      | 1 |
| 2 |  -> pour ->           | 4 |     | 2 |  ->  | 2 |
| 3 |                                 | 1 |      | 3 |
                                                 | 4 |
 items 1, 2, 3 moved twice; their order did not change
```

Each push costs O(n), so n pushes cost O(n^2). Pouring reverses a stack and pouring back reverses it again: every
push does a full reversal and then undoes it.

## The turning point

**Claim: each item needs to be reversed exactly once in its life, and that one reversal can wait until the item is
actually needed.**

Pouring turns newest-on-top into oldest-on-top, the queue order we want, and once flipped an item never needs flipping
back. So give the two stacks fixed jobs:

- **inbox** takes every push. Newest on top.
- **outbox** serves every pop and peek. Oldest on top.

When a pop or peek finds the outbox empty, pour the entire inbox into it. Never pour while the outbox still has items:
those items are older than everything in the inbox, and they must leave first.

The invariant that makes this a queue: **every item in the outbox is older than every item in the inbox, and the outbox
has its oldest item on top.** Then the outbox top, when it exists, is the oldest item in the whole structure. When the
outbox is empty, the oldest item is at the bottom of the inbox, and one pour brings it to the top.

```text
inbox (newest on top)   outbox (oldest on top)
      | 5 |                  | 2 | <- front of the queue
      | 4 |                  | 3 |
 all of {4, 5} arrived after all of {2, 3}
```

The cost argument is per item, not per operation: an item is pushed to the inbox, popped from it, pushed to the outbox,
popped from it. Four stack operations for its whole life.

## Watch it work

Operations: `push 1, push 2, push 3, pop, push 4, pop, pop, pop`. Stacks are drawn as lists with the top on the
right.

```text
Frame 1: push 1, push 2, push 3
  inbox  [1, 2, 3]   <- top 3
  outbox []
```

Pushes only touch the inbox.

```text
Frame 2: pop
  outbox empty -> pour:  inbox [] , outbox [3, 2, 1]
  pop outbox top -> 1
  inbox  []
  outbox [3, 2]      <- top 2
```

The pour puts 1 on top; it leaves.

```text
Frame 3: push 4
  inbox  [4]
  outbox [3, 2]      <- top 2
```

4 waits in the inbox. It must not go onto the outbox, where it would jump ahead of 2 and 3.

```text
Frame 4: pop -> 2, then pop -> 3
  outbox was not empty: no pour either time
  inbox  [4]
  outbox []
```

Both pops come straight from the outbox; 4 waits behind them.

```text
Frame 5: pop
  outbox empty -> pour:  outbox [4]
  pop -> 4
  inbox [] , outbox []   empty() -> True
```

The second pour moves only the one item that arrived after the first pour.

The outbox always held only items older than everything in the inbox, items left in the order 1, 2, 3, 4, and each
crossed from inbox to outbox exactly once.

## Why it is correct

The invariant above holds at the start (both empty). A push adds the newest item to the inbox, so it is younger than
everything in the outbox: still true. A pop from a non-empty outbox removes its top, the oldest item overall, which is
exactly the queue's front. A pour happens only when the outbox is empty; it moves the inbox over in reversed order, so
the oldest inbox item lands on top and the inbox becomes empty, which makes "outbox older than inbox" trivially true.
So every pop returns the oldest remaining item: FIFO. `empty()` must check both stacks.

## Cost

Time: push O(1); pop and peek O(1) amortised and O(n) in the worst case (a single pour), because each item is moved by
at most four stack operations in its life, so any sequence of m operations costs O(m).
Space: O(n), each item lives in exactly one of the two stacks.


## Variations you will meet

- **Worst-case O(1) follow-up.** For a real-time system amortised is not enough; in an interview, name the difference
  and point at the O(n) pour as the spike.
- **Min queue / sliding window aggregate.** Make both stacks min stacks (store the minimum below each entry). The queue's
  minimum is the smaller of the two stacks' top minimums: O(1) amortised, and it works for any associative summary.
- **Implement Stack using Queues (225).** The reverse construction, and it does not mirror nicely: see the next problem.

## What to carry forward

One reversal turns LIFO into FIFO: do it once per item, as late as possible, and charge its cost to the item's lifetime.
The next problem tries the opposite construction and finds that a queue cannot reverse, only rotate.
