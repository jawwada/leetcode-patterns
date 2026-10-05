# Reverse Linked List

*LeetCode 206 · Easy · Pattern: In-place pointer reversal · Reading time ~6 min*

## The problem

Given the head of a singly linked list, reverse it and return the new head.

```text
Example: 1 -> 2 -> 3 -> 4 -> 5 becomes 5 -> 4 -> 3 -> 2 -> 1.
```

## What the problem is really asking

You get the first node of a chain. Make the chain run the other way and hand back the node that is now first. The answer
is a node reference, the old last node, and every arrow in the list must have turned around.

The hard part is not knowing what the result looks like. It is that you can only see one node at a time, and the arrow you
want to flip is the only thing that tells you where the rest of the list is.

```text
before:  head
          v
         [1] -> [2] -> [3] -> [4] -> None

after:                         new head
                                  v
None <- [1] <- [2] <- [3] <- [4]
```

## Do it by hand first

Lay four index cards on a table, each with an arrow to the next. By hand you go card by card: redraw card 1's arrow to
point at nothing, card 2's to point at card 1, and so on.

But notice what your eyes were doing. When you erased card 2's arrow, you still knew where card 3 was because you could
see the table. A program cannot. So your hand was secretly tracking three things: the card you just finished (so the
current card can point back at it), the card you are on, and the card that comes next (so you can get there after
erasing). Those three are the whole state: `prev`, `cur`, `nxt`.

```text
 finished    on it    still to do
   [1]  <-    [2]      [3] -> [4]
   prev       cur      nxt
```

## The first honest attempt

Walk the list and copy every value into a Python list. Reverse that list, then build a new chain from it. Two passes,
O(n) time, O(n) extra space.

It works, but look at what it does with the memory it already had:

```text
original:  [1] -> [2] -> [3] -> [4]     (n nodes, thrown away)
array:      1      2      3      4      (n slots)
new chain: [4] -> [3] -> [2] -> [1]     (n more nodes)
```

The order of a linked list lives in the arrows, not the values. The waste is the copy itself: every node is duplicated
even though each one only needed its `next` field rewritten.

## The turning point

**Claim: reversing a list is exactly "make each node's `next` point to its predecessor", and you can do that in one left
to right walk if you carry the predecessor with you.**

When you stand at node `cur`, its predecessor is the node you visited just before, so you have it in `prev`. The flip is
one write: `cur.next = prev`. The danger is that `cur.next` was your only link to the rest of the list. So the order of
operations is forced:

1. Save the rest: `nxt = cur.next`.
2. Flip: `cur.next = prev`.
3. Advance both tags: `prev = cur`, `cur = nxt`.

Think of a seam moving right. Left of it, everything is reversed and hangs off `prev`; right of it, everything is untouched
and hangs off `cur`. Each step moves one node across. When `cur` falls off the end, `prev` heads the reversed list.

Starting `prev` at `None` is not a detail: it is what makes the old head end up pointing at `None`, which it must, since
it becomes the tail.

## Watch it work

List `1 -> 2 -> 3 -> 4`. Each frame shows the state after one full loop iteration.

```text
Frame 1: start
 prev   cur
 None   [1] -> [2] -> [3] -> [4] -> None
```

Nothing reversed yet; the left chain is empty and `cur` is on the head.

```text
Frame 2: nxt=[2]; [1].next=None; prev=[1]; cur=[2]
 None <- [1]    [2] -> [3] -> [4] -> None
         prev   cur
```

Node 1 crossed the seam. It points at `None`, and `nxt` kept 2, 3, 4 reachable.

```text
Frame 3: nxt=[3]; [2].next=[1]; prev=[2]; cur=[3]
 None <- [1] <- [2]    [3] -> [4] -> None
                prev   cur
```

Node 2 now points back at 1. The left chain reads 2, 1.

```text
Frame 4: nxt=[4]; [3].next=[2]; prev=[3]; cur=[4]
 None <- [1] <- [2] <- [3]    [4] -> None
                       prev   cur
```

Left chain reads 3, 2, 1; only node 4 remains on the right.

```text
Frame 5: nxt=None; [4].next=[3]; prev=[4]; cur=None
 None <- [1] <- [2] <- [3] <- [4]    None
                              prev   cur
```

`cur` is `None`, the loop stops, and we return `prev`, which reads 4, 3, 2, 1.

In every frame, every node was reachable from either `prev` or `cur`, and the chain hanging off `prev` was exactly the
visited nodes in reverse order.

## Why it is correct

Invariant at the top of each iteration: `prev` heads a correctly reversed copy of the nodes visited so far (ending in
`None`), and `cur` heads the untouched remainder in its original order. Together they hold every node exactly once.

Initially nothing is visited, `prev` is `None`, `cur` is the head. One iteration moves the first node of the remainder
onto the front of the reversed part; `nxt` keeps the shortened remainder reachable. So the invariant holds again. Each iteration shrinks the remainder by one, so the loop ends after n
iterations, with an empty remainder and `prev` heading the whole list reversed.

## Cost

- Time: O(n), one constant-work iteration per node.
- Space: O(1), three references regardless of length.

## Variations you will meet

- **Recursive reversal.** Reverse the rest, then make `head.next.next = head` and `head.next = None`. Same idea, but stack
  depth n; in Python it fails on long lists.
- **Reverse between positions m and n** (LeetCode 92). Walk to the node before position m, run the same loop for n-m+1
  steps, then reconnect both ends. The new part is the reconnection.
- **Reverse in groups of k** (the last problem in this chapter). The same loop, bounded to k nodes, repeated with careful
  stitching.
- **Palindrome and reorder.** Reverse only the second half so it can be walked backwards.

## What to carry forward

Save `next`, flip, advance: a seam moving right with the reversed part on the left. The next problem keeps the habit of
rewiring existing nodes, but instead of flipping arrows it builds a new chain behind a dummy head.
