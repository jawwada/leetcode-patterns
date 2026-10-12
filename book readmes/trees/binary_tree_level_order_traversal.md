# Binary Tree Level Order Traversal

*LeetCode 102 · Medium · Pattern: BFS by level (queue snapshot) · Reading time ~8 min*

## The problem

Return the node values level by level, left to right, as a list of lists.

```text
Example: [3,9,20,null,null,15,7] -> [[3],[9,20],[15,7]].
```

## What the problem is really asking

Read the tree the way you read a page: top row first, left to right, then the next row. Return the rows as separate lists. The answer is a list of lists, one inner list per depth, and an empty tree gives an empty list.

```text
 tree [3,9,20,null,null,15,7]

   depth 0          3              -> [3]
                  /   \
   depth 1       9     20          -> [9, 20]
                      /  \
   depth 2          15    7        -> [15, 7]

 answer: [[3], [9, 20], [15, 7]]
```

Every problem so far in this chapter went deep first: follow one path to the bottom, come back, try the next. That order is natural for recursion but wrong for this question. In depth-first order you finish all of 9's side before ever seeing 20, and on a bigger tree you would touch depth 3 on the left long before depth 1 on the right. What makes this problem worth studying is not difficulty but the new tool it forces: visiting by distance from the root, and knowing where one row ends and the next begins.

## Do it by hand first

On paper you would point at the top row, read it, then look just below it for the next row. Crucially, you find the next row by looking at the children of the row you just read, left to right:

```text
 row being read     children found, in order
 [3]                9, 20
 [9, 20]            (9 has none), 15, 7
 [15, 7]            (none)       -> stop
```

You kept a "current row" and, while reading it, built up a "next row" behind it. The next row was formed in left-to-right order automatically, because you scanned the current row left to right and listed each node's left child before its right. That waiting line of nodes is a queue: first in, first out.

## The first honest attempt

A candidate who only knows recursion can still do it. Compute the height h. Then for each depth d from 0 to h - 1, run a fresh depth-first walk that carries the current depth and collects the nodes where depth equals d.

```text
 pass d=0: visit 3                          keep 3
 pass d=1: visit 3, 9, 20                   keep 9, 20
 pass d=2: visit 3, 9, 20, 15, 7            keep 15, 7
           ^^^^^^^^^ top of the tree walked again in every pass
```

Each pass walks the tree down to depth d, and there are h passes, so the cost is O(n·h): O(n log n) for a balanced tree, O(n^2) for a chain. The repeated work is clear in the drawing. Pass d=2 re-walks 3, 9, 20 to rediscover the nodes it needs, but pass d=1 was literally standing on 9 and 20, with their children one pointer away.

## The turning point

**Claim: the nodes of level d + 1 are exactly the children of the nodes of level d, taken in order; so if you keep the current level in a FIFO queue and append children at the back as you remove parents from the front, the queue always holds the rest of one level followed by the start of the next, in left-to-right order.**

That is breadth-first search. But plain BFS only produces one long sequence `3, 9, 20, 15, 7`; we also need the row breaks. Here is the one extra trick that turns BFS into a level-by-level BFS:

**The snapshot.** At the start of a round, before removing anything, the queue contains exactly one whole level and nothing else. So `len(queue)` at that moment is the size of the level. Remove exactly that many nodes; their children pile up at the back but are not touched this round. When the count runs out, the level is complete, and the queue again holds exactly one whole level.

```text
 start of round:   front [ 9 | 20 ] back       size = 2
 pop 9, push none: front [ 20 ] back
 pop 20, push 15,7 front [ 15 | 7 ] back       popped 2: stop
                         \______/
                         next level, untouched this round
```

The snapshot must be taken once, before the inner loop. If you re-read `len(queue)` while popping, the children you just added make the queue longer, and the round runs into the next level.

In Python the queue is `collections.deque`, whose `popleft` is O(1). A plain list with `pop(0)` shifts every element and silently makes the whole traversal quadratic.

## Watch it work

Tree `[3,9,20,null,null,15,7]`. Each frame shows the tree with `*` on the node just popped, the queue from front to back, the level being built, and the result.

**Frame 1.** Initialise.

```text
           3            queue  front [ 3 ] back
          / \
         9   20         result []
            /  \
          15    7
```

The queue holds the root, which is all of level 0.

**Frame 2.** Round 1, snapshot size = 1. Pop 3, push 9 and 20.

```text
          *3*           queue  front [ 9 | 20 ] back
          / \
         9   20         level  [3]   (1 of 1 popped)
            /  \        result [[3]]
          15    7
```

Size reached, so `[3]` is closed. The queue now holds exactly level 1.

**Frame 3.** Round 2, snapshot size = 2. Pop 9; it has no children.

```text
           3            queue  front [ 20 ] back
          / \
        *9*  20         level  [9]   (1 of 2 popped)
            /  \        result [[3]]
          15    7
```

**Frame 4.** Pop 20, push 15 and 7.

```text
           3            queue  front [ 15 | 7 ] back
          / \
         9  *20*        level  [9, 20]  (2 of 2 popped)
            /  \        result [[3], [9, 20]]
          15    7
```

The round stops at 2 even though the queue is non-empty: 15 and 7 belong to the next row.

**Frame 5.** Round 3, snapshot size = 2. Pop 15, then pop 7; neither has children.

```text
           3            queue  front [ ] back
          / \
         9   20         level  [15, 7]  (2 of 2 popped)
            /  \        result [[3], [9, 20], [15, 7]]
         *15*  *7*
```

The queue is empty, so the outer loop ends.

Across the frames, at the start of every round the queue held exactly one complete level in left-to-right order, and during a round, nodes of the current level sat in front of nodes of the next.

## Why it is correct

The layer property, proved by induction on rounds. Suppose round k starts with the queue equal to level k, left to right. During the round we pop those nodes in that order and append each one's left child then right child. The children of level k, listed by parent order and then left before right, are exactly level k + 1 in left-to-right order. So after `size` pops, the queue is precisely level k + 1, ordered. The base case is the root alone, which is level 0. Each round records the popped values in order, so result[k] is level k. The loop ends when a level has no children, which is when the tree is exhausted. Every node is enqueued exactly once, by its unique parent.

## Cost

- Time O(n): each node is pushed and popped once, O(1) each with a deque.
- Space O(w), where w is the maximum width of the tree: the queue holds at most one level plus part of the next. For a complete tree the last level is about n/2 nodes, so worst case O(n). Compare depth-first's O(h): BFS is cheap on tall thin trees and expensive on wide ones; DFS is the opposite.
- The brute force, by contrast, was O(n·h) time.

## Variations you will meet

- **Level Order Bottom-Up** (LeetCode 107). Same rounds, reverse the result at the end.
- **Zigzag Level Order** (LeetCode 103). Same rounds; reverse every other level, or fill each level into a deque from alternating ends. The queue order itself does not change.
- **Averages, maximums, or sums per level** (LeetCode 637, 515, 1161). Replace "append value to level" with an accumulator; the snapshot still marks the boundary.
- **DFS with a depth parameter.** Pass `depth` down and append to `result[depth]`, creating the list when `depth == len(result)`. Same output, O(h) space instead of O(w). The next problem leans on exactly this "first time I reach a depth" test.
- **Minimum depth, or nearest anything.** BFS reaches nodes in distance order, so the first leaf popped is the shallowest; you can stop early, which DFS cannot.

## What to carry forward

A FIFO queue plus a size snapshot taken at the start of each round turns BFS into clean row-by-row processing. Binary Tree Right Side View next asks for just one node per row, the last one; you can read it off these same rounds, or get it with a right-first DFS that keeps only the first node it reaches at each depth.
