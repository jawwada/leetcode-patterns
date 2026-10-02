# Reverse Nodes in k-Group
*LeetCode 25 · Hard · Pattern: In-place pointer reversal · Reading time ~12 min*

## What the problem is really asking

Cut the list into consecutive blocks of k nodes. Reverse each full block. If the last block has fewer than k nodes, leave it alone. Return the new head. You must change links, not values, and the follow-up asks for O(1) extra memory.

```text
  k = 2:   [1 -> 2] [3 -> 4] [5]
       ->  [2 -> 1] [4 -> 3] [5]       5 is a short block: kept

  k = 3:   [1 -> 2 -> 3] [4 -> 5]
       ->  [3 -> 2 -> 1] [4 -> 5]
```

The answer is a rewired list. Reversing one block is the very first problem of this chapter. What makes this one Hard is everything around the reversal: knowing *before* you start a block whether it is full, keeping the block attached to what comes before and after it while its insides are being flipped, and moving cleanly from one block to the next. Every one of these is a place to lose half the list or create a cycle.

## Do it by hand first

With cards on a table, k = 2: pick up the first two cards, flip their order, put them back. Move on to the next two. When fewer than two remain, stop.

```text
  table:   1  2  3  4  5
          [1  2]            count 2 cards: full -> flip
  table:   2  1  3  4  5
                [3  4]      count 2 cards: full -> flip
  table:   2  1  4  3  5
                      [5]   count: only 1 -> leave it
```

Notice what your hands did between flips. Before flipping, you *counted ahead* to check there were k cards. While flipping, your left hand held the boundary "the card before this block" (nothing, then 1) and your eyes held "the card after this block" (3, then 5). After flipping, the boundary moved to the last card of the block you just flipped, which was the *first* card before the flip (1, then 3).

Those three things are the state of the algorithm: a lookahead to the k-th node, the node before the block, and the node after the block.

## The first honest attempt

Copy the nodes into an array. Reverse each full chunk of k entries in the array. Relink `nodes[i].next = nodes[i+1]` in the new order and end with None. O(n) time, O(n) space.

```text
  array:   [n1, n2, n3, n4, n5]
  chunks:  [n1, n2] [n3, n4] [n5]
  reverse: [n2, n1] [n4, n3] [n5]
  relink:  n2 -> n1 -> n4 -> n3 -> n5 -> None
```

It is honest and easy to get right. The array serves two purposes: telling us how many nodes remain (so we skip the short tail), and letting us visit a chunk backwards. But the first can be done by walking k steps ahead, and the second is exactly what in-place reversal provides. So the O(n) buffer is paying for things we already know how to do in O(1) memory.

An alternative wasteful attempt: reverse every block, including the last, and then if the last block was short, reverse it again. It works but does extra passes and requires knowing which block was last; counting ahead is cleaner.

## The turning point

**Claim: each block is an ordinary list reversal stopped after k nodes; if you start the reversal with `prev` set to the node after the block, the reversed block comes out already attached on its right, and only one link on its left needs fixing.**

Let us build the per-block procedure from the three things the hands tracked.

*A dummy node.* The first block's reversal changes the list's head. To avoid a special case, put a dummy node D in front: `D -> 1 -> 2 -> ...`. Then "the node before the block" always exists. We call it `group_prev`, and it starts as D. The answer at the end is `D.next`.

*Lookahead.* From `group_prev`, step k times to find `kth`, the last node of the block. If you hit None before k steps, the block is short: stop and return. Nothing has been modified for that block, so the short tail stays in order for free.

*Remember the right boundary.* `nxt = kth.next`, the first node after the block (possibly None).

*Reverse with a pre-attached tail.* In plain list reversal you start with `prev = None`, because the old head becomes the new tail and must point to None. Here, the old head of the block becomes the block's tail and must point to `nxt`. So start with `prev = nxt`, `cur = group_prev.next`, and do the usual flip `cur.next, prev, cur = prev, cur, cur.next` until `cur` reaches `nxt`. After k flips, `prev` is `kth`, the new head of the block, and the old head points to `nxt`.

```text
  before:  gp -> a -> b -> c -> nxt
  after:   gp -> a           a -> nxt     (a was flipped first)
                c -> b -> a -> nxt        (c is the new head)
           gp still points to a!
```

*Fix the left link and move on.* `group_prev.next` still points to the old head `a`, which is now the block's tail. Save it: `tmp = group_prev.next`. Then `group_prev.next = kth` hooks the reversed block on the left. Finally `group_prev = tmp`: the old head, now the tail, is the node before the next block.

That is the whole algorithm. Each block costs a k-step lookahead and k flips, and there is exactly one link (`group_prev.next`) that gets rewired outside the reversal loop.

The two choices that make it short are worth naming as principles, because they recur in every pointer-surgery problem. First, a dummy head removes the "is this the first block?" branch. Second, initialising `prev` to the right neighbour, rather than None, removes a separate "connect the tail" step. Get these two right and the bugs that remain are only about saving a pointer before overwriting it.

## Watch it work

List `1 -> 2 -> 3 -> 4 -> 5`, k = 2. D is the dummy, gp is `group_prev`.

Frame 1 — setup and first lookahead.

```text
  D -> 1 -> 2 -> 3 -> 4 -> 5 -> None
  gp        kth  nxt
  lookahead from D: 1, 2   -> full block [1, 2]
```

Two steps from D reach node 2, so the block is full; `nxt` is 3.

Frame 2 — reverse, first flip.

```text
  prev = nxt = 3, cur = 1
  flip: 1.next = 3

  D -> 1 -> 3 -> 4 -> 5        2 -> 3 (unchanged so far)
  gp   prev                    cur
```

Node 1 now points right past its block to 3, already in its final position as the block tail.

Frame 3 — reverse, second flip.

```text
  flip: 2.next = 1, prev = 2, cur = 3 == nxt -> stop

  2 -> 1 -> 3 -> 4 -> 5
  prev
  D -> 1 -> 3 ...              (D still points to 1)
```

The block is reversed and attached to 3 on the right, but D still points to the old head 1, so node 2 is unreachable from D at this instant.

Frame 4 — stitch the left side.

```text
  tmp = D.next = 1
  D.next = kth = 2
  gp = tmp = 1

  D -> 2 -> 1 -> 3 -> 4 -> 5 -> None
            gp
```

The block is hooked in, and gp moves to node 1, the new tail of the finished block.

Frame 5 — second block, lookahead and reverse.

```text
  lookahead from 1: 3, 4  -> kth = 4, nxt = 5
  prev = 5, cur = 3
  flip: 3.next = 5          flip: 4.next = 3, cur = 5 -> stop

  4 -> 3 -> 5               1 -> 3 (gp still points to 3)
```

Same two flips as before, with the right boundary 5 attached from the first flip.

Frame 6 — stitch the second block.

```text
  tmp = 1.next = 3;  1.next = 4;  gp = 3

  D -> 2 -> 1 -> 4 -> 3 -> 5 -> None
                      gp
```

The second block is hooked between 1 and 5; gp moves to its tail, node 3.

Frame 7 — lookahead fails.

```text
  lookahead from 3: 5, then None   -> short block
  return D.next

  2 -> 1 -> 4 -> 3 -> 5 -> None
```

Only one node remains after gp, so the loop returns without touching it.

What stayed true at the top of each round: everything from D up to gp is finished and correctly linked, gp.next is the first unprocessed node, and the unprocessed part is still the original list in its original order. Within a round, the only temporarily broken link was `gp.next` (Frames 3 and 5), and it was repaired before gp moved.

## Why it is correct

Invariant at the top of each loop iteration: the list from D to gp is the correct output for the blocks processed so far; gp.next is the head of the remaining, untouched suffix of the original list.

Initially gp = D and the suffix is the whole list, so it holds.

*Short block.* If the lookahead finds fewer than k nodes, the remaining suffix must be left in order. It is untouched by the invariant, and gp.next already points to it, so returning D.next produces the correct full answer.

*Full block.* The block is the nodes gp.next through kth, and nxt is the suffix after them. The reversal loop starting at cur = gp.next with prev = nxt performs exactly k flips (it stops when cur reaches nxt, which is k nodes later), the same as standard reversal with the initial prev replaced by nxt. Its effect: the block's links are reversed, the old head points to nxt, and prev ends at kth. No node outside the block has its `next` changed. Then gp.next = kth attaches the reversed block after the finished prefix, and gp = old head moves to the new end of the finished prefix, whose next is nxt, the untouched suffix. The invariant holds again.

Each full block advances gp by k nodes, so the loop ends after floor(n/k) full blocks plus one failed lookahead.

## Cost

- **Time: O(n).** Each node is visited twice: once in a lookahead and once in a reversal. The final failed lookahead visits fewer than k nodes.
- **Space: O(1).** A dummy node and a handful of pointers. The array approach is O(n) time and O(n) space; a recursive solution (reverse the first block, recurse on the rest) is O(n) time but O(n/k) stack.

## Variations you will meet

- **Swap Nodes in Pairs (LeetCode 24).** Exactly this problem with k = 2. The same code works; many people write a special-cased pair swap, but the general version is no longer.
- **Reverse Linked List II (LeetCode 92).** Reverse only positions left..right. It is one block: walk to the node before `left` (with a dummy), then reverse right - left + 1 nodes with `prev` initialised to the node after the range.
- **Reverse the last short block too.** Drop the "stop if fewer than k" check and reverse whatever remains; the lookahead just limits the block length instead of guarding it.
- **Reverse alternate k-blocks (reverse k, skip k, reverse k...).** After stitching, advance gp k extra nodes before the next lookahead. The invariant is unchanged; "finished prefix" simply includes skipped blocks.

## What to carry forward

A hard pointer problem is usually an easy one repeated, plus glue: a dummy head, a lookahead to check the block exists, `prev` initialised to the right neighbour so the reversed block is born attached, and one saved pointer to stitch the left side. That closes the chapter: across these twelve problems you have built, reversed, merged, split, raced, aligned, folded, woven and cloned linked lists, and every technique came down to the same discipline of naming the few pointers you must hold and saving each one before you overwrite it.
