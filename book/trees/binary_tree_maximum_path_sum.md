# Binary Tree Maximum Path Sum

*LeetCode 124 · Hard · Pattern: Post-order height with side-channel answer · Reading time ~11 min*

## The problem

A path is any sequence of nodes connected by parent-child edges, each node used at most once; it need not pass through
the root or end at a leaf. Return the maximum sum of node values over all non-empty paths.

```text
Example: [-10,9,20,null,null,15,7] -> 42 via 15 -> 20 -> 7.
```

## What the problem is really asking

A path here is any chain of nodes linked by parent-child edges, using each node at most once. It can start anywhere and end anywhere. It does not have to touch the root and does not have to reach a leaf. It must contain at least one node. Among all such paths, return the largest sum of values.

```text
 tree [-10,9,20,null,null,15,-7]

            -10
            /  \
           9    20
               /  \
             15    -7

 some paths and their sums
   9                    =  9
   15 - 20              = 35   <- best
   15 - 20 - -7         = 28
   9 - -10 - 20 - 15    = 34
   15 - 20 - -10 - 9    = 34   (same path, read backwards)
```

The answer is one integer. Three things make it hard, and each one breaks a simpler problem you already know:

1. Values can be negative, so "longer" does not mean "bigger". The best path above avoids -7 and avoids the root.
2. A path can bend: go up from 15 to 20 and down the other side. So it is not a root-to-leaf path like Path Sum.
3. The path cannot fork. At any node it uses at most two of the three edges (parent, left, right). A shape like "20 with both children and its parent" is a tree, not a path.

## Do it by hand first

Look at any path drawn on the tree. It has exactly one highest node, the one closest to the root. Call it the top. From the top, the path goes down on at most two sides: some chain into the left subtree and some chain into the right subtree.

```text
 path 15 - 20 - -7         path 9 - -10 - 20 - 15

        20  <- top                  -10  <- top
       /  \                         /  \
     15    -7                      9    20
                                         \.. 15
  left arm: 15                  left arm: 9
  right arm: -7                 right arm: 20 -> 15
```

So by hand you would go node by node, imagine it as the top, and ask: what is the best downward chain I can hang on the left, and the best on the right? If the best chain on a side is negative, you would not hang anything there. Take the top's value plus both arms, and remember the biggest total you have seen.

For top = 20: best left arm is 15, best right arm is -7 so use nothing, total 35. For top = -10: best left arm 9, best right arm is 20 + 15 = 35, total -10 + 9 + 35 = 34. Biggest is 35.

What your hand tracked for each node was "the best chain starting here and going down". That number is the seed.

## The first honest attempt

Turn the hand method into code directly. Write a helper `gain(node)` meaning "the best sum of a chain that starts at `node` and goes straight down", which is `node.val + max(gain(left), gain(right), 0)`. Then for every node as the top, compute `node.val + max(gain(left),0) + max(gain(right),0)` and take the maximum.

It is correct, but each `gain` call walks the entire subtree below it, and it is called fresh for every ancestor that plays top:

```text
 who calls gain(15)?
   top = 20   -> gain(15)         (left arm of 20)
   top = -10  -> gain(20)
                   -> gain(15)    again
 on a chain of n nodes, the bottom node is re-measured
 by every one of its n-1 ancestors

   1
    \           top=1  measures 2,3,4,5
     2          top=2  measures   3,4,5
      \         top=3  measures     4,5
       3        ...
        \
         4      total ~ n^2 / 2 visits
          \
           5
```

O(n^2) time on a skewed tree. The waste: `gain(node)` is a fixed number for each node, and the brute force recomputes it once per ancestor.

## The turning point

**Claim: a single post-order pass can compute `gain` for every node exactly once, and at the moment `gain(node)` has both child gains in hand, it already has everything needed to score `node` as the top, so it can update the answer right there and return only the one-armed value upward.**

Let's take that slowly, because it contains two separate ideas.

*Idea 1: compute gains bottom up.* `gain(node)` depends only on `gain(left)` and `gain(right)`. A post-order recursion computes children before parents, so every gain is computed once and reused by the parent immediately. This is the same move as Maximum Depth: the height of a node is one plus the heights of its children, computed once.

*Idea 2: the function returns one thing and records another.* At node X with clipped child gains `L` and `R`, there are two different quantities:

```text
 bend at X (candidate answer)     extend through X (returned)

         X                                parent
        / \                                 |
      L     R                               X
                                           /
   X.val + L + R                         L  (or R, the better)

   uses both arms, so nothing        uses one arm, so the parent
   above X can join this path        can attach it as ITS arm
```

The bending path is a complete candidate: it is the best path whose top is X. Nothing above can extend it, because X has already used both of its downward edges and a third edge (to the parent) would create a fork. So we score it on the spot, `best = max(best, X.val + L + R)`, and never pass it anywhere.

The extendable path is what the parent needs: a chain starting at X and going down one side. That is `X.val + max(L, R)`, and it is the return value.

This split between "what I return" and "what I record on the side" is exactly the pattern from Diameter of Binary Tree, where the function returned height but recorded `left_height + right_height` as a candidate diameter. Here the "heights" are weighted by values and can be negative.

*Clipping.* A child's gain can be negative, as with -7. Including a negative arm only lowers the sum, and arms are optional (a path can stop at X). So the parent uses `max(gain(child), 0)`: a negative arm counts as "take nothing on this side". Note that the returned value `X.val + max(L, R)` itself is not clipped; X.val may be negative. The parent does the clipping when it reads it.

*Initialising best.* The path must contain at least one node. If every value is negative, say a single node -3, the answer is -3. Starting `best` at 0 would wrongly return 0, the sum of an empty path. Start at negative infinity; the first node scored replaces it.

## Watch it work

Tree `[-10,9,20,null,null,15,-7]`. Post-order visits 9, 15, -7, 20, -10. Each frame shows the node being finished, its clipped arms `L` and `R`, the bend candidate, `best`, and the value returned to the parent. Finished nodes show their return value in brackets.

**Frame 1.** Leaf 9.

```text
            -10
            /  \
         *9*    20          L=0  R=0
               /  \         bend = 9 + 0 + 0 = 9
             15    -7       best = max(-inf, 9) = 9
                            return 9
```

Empty children contribute 0. The single node 9 is the first candidate.

**Frame 2.** Leaf 15.

```text
            -10
            /  \
         [9]    20          L=0  R=0
               /  \         bend = 15
            *15*   -7       best = 15
                            return 15
```

**Frame 3.** Leaf -7.

```text
            -10
            /  \
         [9]    20          L=0  R=0
               /  \         bend = -7
           [15]   *-7*      best = max(15, -7) = 15
                            return -7
```

It returns -7 honestly; deciding to ignore it is the parent's job.

**Frame 4.** Node 20 sees its children's returns, 15 and -7.

```text
            -10
            /  \
         [9]   *20*         L = max(15, 0) = 15
               /  \         R = max(-7, 0) = 0   clipped
           [15]   [-7]      bend = 20 + 15 + 0 = 35
                            best = 35
                            return 20 + max(15,0) = 35
```

The best path so far is 15 - 20. Clipping removed -7 from both the candidate and the return.

**Frame 5.** Root -10 sees 9 and 35.

```text
           *-10*            L = 9   R = 35
            /  \            bend = -10 + 9 + 35 = 34
         [9]   [35]         best = max(35, 34) = 35
                            return -10 + 35 = 25
```

The path through the root, 9 - -10 - 20 - 15, scores 34 and loses. The returned 25 goes nowhere, since the root has no parent.

**Frame 6.** Done.

```text
   best = 35      path: 15 - 20  (top = 20)
```

Across the frames, the value returned by a node was always "best downward chain starting here", and `best` was always the maximum bend score over finished nodes. The returned value never included both arms.

## Why it is correct

Two facts, both by induction on the post-order.

*Fact 1: `gain(X)` returns the maximum sum of a chain that starts at X and goes downward (possibly just X).* Such a chain is either X alone, X followed by a chain starting at the left child, or X followed by one starting at the right child. By induction the children's calls return the best of their chains, so the best for X is `X.val + max(0, gain(left), gain(right))`, which is what the code returns, since clipping each child at 0 first gives the same maximum.

*Fact 2: every path is scored at its top, and is scored no higher than its true best.* Any path has a unique top T. Remove T and the path splits into at most a left chain starting at T.left and a right chain starting at T.right, each going downward (or absent). The sum is `T.val + left_part + right_part`. Each part is at most the best chain on that side and an absent part counts as 0, so the sum is at most `T.val + max(gain(T.left),0) + max(gain(T.right),0)`, which is exactly T's bend score. Conversely that bend score is the sum of a real path: T plus its best non-negative arms. So the bend score at T is the maximum over all paths with top T.

Every node is scored once, every path has a top, so the maximum of all bend scores is the maximum over all paths.

## Cost

- Brute force: O(n^2) time on a skewed tree, O(h) space.
- Optimal: O(n) time, one post-order visit per node with O(1) work; O(h) space for the recursion stack (n for a chain, so very deep trees in Python may need an iterative post-order or a raised recursion limit).

## Variations you will meet

- **Diameter of Binary Tree** (earlier). Same shape with every node weighing 1 on edges and no negatives, so no clipping. If you can derive one from the other, you own the pattern.
- **Longest Univalue Path** (LeetCode 687). An arm only counts if the child has the same value as the node; otherwise the arm is 0. Same return-one-arm, record-two-arms split.
- **Return the path itself.** Store, alongside `best`, which node was the top and which arms were used; rebuild by following the better child at each step. Or return `(gain, chain)` pairs, paying for list copies.
- **Maximum path sum in a general tree or graph.** In an N-ary tree a node keeps its two largest child gains. In a graph with cycles, paths become a much harder problem; the tree's "unique top" is what made this one linear.

## What to carry forward

Return what the parent can extend (one arm), record what is complete (both arms), and clip negative arms to zero. That closes the depth-first part of the chapter. Next, Binary Tree Level Order Traversal changes the visiting order entirely: instead of diving down one path, it sweeps the tree row by row with a queue.
