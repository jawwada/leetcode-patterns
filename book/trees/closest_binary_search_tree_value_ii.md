# Closest Binary Search Tree Value II

*LeetCode 272 · Hard · Pattern: Two lazy inorder iterators (predecessor / successor stacks) · Reading time ~11 min*

## The problem

Given a BST, a float target and an integer k (at most the number of nodes), return the k values closest to target in
any order.

```text
Example: root=[4,2,5,1,3], target=3.714286, k=2 returns [4,3].
```

## What the problem is really asking

You are given a binary search tree, a real-number `target` and an integer `k`. Return the `k` values in the tree that sit closest to `target` on the number line. Any order is fine, and `k` never exceeds the number of nodes.

The answer is a small set of `k` values. The tree is a BST, so its inorder walk lists the values in sorted order. Once the values are on a sorted line, "the `k` closest to a point" is not a scattered set. It is a contiguous run of `k` neighbours around the point. The hard part is getting that run without listing the whole tree. If the tree has a million nodes and `k = 3`, touching every node is a waste, and the follow-up the interviewer is waiting for is "can you do it in roughly `O(h + k)`?"

```text
tree:          4            target = 3.6, k = 4
             /   \
            2     6
           / \   / \
          1   3 5   7

inorder line:
   1     2     3  t  4     5     6     7
                  ^ 3.6
distance: 2.6  1.6  0.6  0.4  1.4  2.4  3.4

answer: {4, 3, 5, 2}   (a window of 4 around t)
```

## Do it by hand first

Put your finger on `3.6` on the number line. The two nearest values are the one just left of you (`3`) and the one just right of you (`4`). Take the closer, `4`. Now the right finger moves one step right to `5`, and the left finger stays at `3`. Compare `3` (distance 0.6) with `5` (distance 1.4) and take `3`. The left finger steps left to `2`. Compare `2` (1.6) with `5` (1.4) and take `5`. Compare `2` (1.6) with `6` (2.4) and take `2`. You have four values.

```text
        left finger          right finger
             <-  2  3  t  4  5  ->
step 1:          [3]     [4]       take 4 (0.4 < 0.6)
step 2:          [3]        [5]    take 3 (0.6 < 1.4)
step 3:       [2]           [5]    take 5 (1.4 < 1.6)
step 4:       [2]              [6] take 2 (1.6 < 2.4)
```

Your hand kept track of two things: the next unused value on the left of the target, and the next unused value on the right. Each step you compared just those two and moved one finger outward. This is the merge step from merge sort, run on two sorted lists that both start at the target and walk away from it. The question is how to get "the next value to the left" and "the next value to the right" out of a tree cheaply. The answer is the inorder iterator from Binary Tree Inorder Traversal and Kth Smallest Element in a BST, built twice, once facing each way.

## The first honest attempt

Walk the whole tree inorder into a list of `n` values, sort it by `|value - target|`, and return the first `k`. That is `O(n log n)` time and `O(n)` space.

There are two kinds of waste. The sort throws away order that inorder already gave us for free. And the walk touches every node, even though only the `k` around the target can matter.

```text
inorder list: 1  2  3  4  5  6  7  ... 999 1000
                 \________/
                 the only part the answer uses
              everything else is visited, stored
              and sorted for nothing
```

A better middle step is to keep the inorder walk but stop sorting. Hold a sliding window of the last `k` values. When a new value is closer than the window's leftmost, slide. When it is farther, stop, because every later value is farther still. That is `O(n)` in the worst case, when the target sits near the largest value and the walk has to cross the whole tree to get there. The real target is to avoid walking the part of the tree far from `target` at all.

## The turning point

**Claim: the `k` closest values are produced by merging two sorted streams that both start at the target: predecessors read right-to-left, and successors read left-to-right. Each stream can be generated lazily by an inorder stack in amortised `O(1)` per value.**

Why merging works: on the left side, values get farther from target as you walk left, and on the right side they get farther as you walk right. So each stream is already sorted by distance. The closest unused value overall is always at the head of one of the two streams. Merging is just "compare the two heads and take the smaller distance", `k` times.

Now the structure. Remember how the iterative inorder walk works. A stack holds the "left spine" still to visit, the top is the next smallest node, and after popping a node you push its right child and that child's whole left chain. That machine produces the successor stream if it starts at the right place. The trick is where the stacks start. Do one ordinary BST search for `target` from the root:

- At a node with `val <= target`, the node is a predecessor candidate. Push it on `pred` and go right, since anything closer from below is in the right subtree.
- At a node with `val > target`, it is a successor candidate. Push it on `succ` and go left.

When the search falls off the tree, the top of `pred` is the largest value `<= target`, and the top of `succ` is the smallest value `> target`. Each stack is exactly the state an inorder iterator would have at that point in the walk.

```text
search path for 3.6:   4 (>t, succ)  -> go left
                       2 (<=t, pred) -> go right
                       3 (<=t, pred) -> go right -> None

pred = [2, 3]  top 3 = largest <= t
succ = [4]     top 4 = smallest > t
```

Advancing them mirrors each other:

- `next_succ`: pop the top. Its right subtree holds the next larger values, so push its right child and then that child's left chain. The new top is the next successor.
- `next_pred`: pop the top. Its left subtree holds the next smaller values, so push its left child and then that child's right chain. The new top is the next predecessor.

A node equal to the target goes on `pred` only, so no value appears in both streams. When distances tie, the code takes from `pred`. Either choice is correct, since the problem accepts any order and either value belongs in the answer.

This turns the brute force's "list everything and sort" into "start in the middle and walk outward", which is the whole point of having a BST.

## Watch it work

Tree `[4,2,6,1,3,5,7]`, `target = 3.6`, `k = 4`. Stacks are written bottom to top, so the rightmost entry is the top.

Frame 1. The search path splits into the two stacks.

```text
          4  -> succ
        /   \
pred <- 2     6
       / \   / \
      1   3 5   7
          ^ pred
pred = [2, 3]    top 3  (dist 0.6)
succ = [4]       top 4  (dist 0.4)
out  = []
```

Nothing has been output yet. The only nodes touched so far are the three on the search path.

Frame 2. Compare heads: `3` is 0.6 away and `4` is 0.4 away, so take `4` from `succ`. Refill: push `4.right = 6`, then its left chain, `5`.

```text
pred = [2, 3]    top 3  (0.6)
succ = [6, 5]    top 5  (1.4)
out  = [4]
```

The successor stream now points at `5`, the next value right of `4`.

Frame 3. Compare `3` (0.6) with `5` (1.4) and take `3` from `pred`. Refill: `3.left` is empty, so nothing is pushed.

```text
pred = [2]       top 2  (1.6)
succ = [6, 5]    top 5  (1.4)
out  = [4, 3]
```

The predecessor stream falls back to `2`, which was already on the stack from the search.

Frame 4. Compare `2` (1.6) with `5` (1.4) and take `5`. Refill: `5.right` is empty.

```text
pred = [2]       top 2  (1.6)
succ = [6]       top 6  (2.4)
out  = [4, 3, 5]
```

Frame 5. Compare `2` (1.6) with `6` (2.4) and take `2`. Refill: push `2.left = 1`, then its right chain, which is empty.

```text
pred = [1]       top 1  (2.6)
succ = [6]       top 6  (2.4)
out  = [4, 3, 5, 2]   k reached, stop
```

Node `7` was never touched, and node `1` was pushed but never output. In a large tree, whole subtrees far from the target are never visited.

Across all frames, `pred`'s top is the largest unused value `<= target` and `succ`'s top is the smallest unused value `> target`. Each stack holds at most one root-to-leaf path. The output is always a contiguous window of the inorder line that contains the target's gap.

## Why it is correct

There are two invariants, one per stack. For `succ`: the stack holds the nodes whose values are the unread successors, arranged so that the top is the smallest unread one and every other unread successor is either on the stack or in the right subtree of a node on the stack, above it in value. This is the standard inorder-iterator invariant. The initial search sets it up, because every node where we turned left is a successor whose left part we are about to explore. `next_succ` keeps it, because popping a node and pushing its right child's left chain is exactly how inorder advances. The same argument, mirrored, holds for `pred`.

With both invariants in place, the merge is correct by the same reasoning as merging two sorted lists. Let `L` be the unread predecessors in decreasing order and `R` the unread successors in increasing order. Distances along `L` increase and distances along `R` increase. So the minimum distance among all unread values is at the head of `L` or the head of `R`. Taking the smaller of the two heads each step outputs values in non-decreasing order of distance. After `k` steps we have the `k` smallest distances.

The empty-stack checks cover targets outside the range. If the target is below every value, `pred` starts empty and every pick comes from `succ`. That is exactly the first `k` values in inorder.

## Cost

- **Time `O(h + k)`.** The initial search is `O(h)`. Each `next_*` call pushes nodes that will each be popped at most once. Across `k` calls, the total pushes are bounded by `k` plus at most `h` per stack of refill chain, so the cost is amortised `O(1)` per output plus `O(h)` overall. For a balanced tree that is `O(log n + k)`.
- **Space `O(h)`.** Each stack holds at most one root-to-leaf path. The output takes `O(k)`.
- The simpler inorder-with-sliding-window version is `O(n)` time and `O(k)` space. It is worth saying out loud first, then improving to the two-stack version.

## Variations you will meet

- **Closest Binary Search Tree Value (LeetCode 270), `k = 1`.** Only the search path is needed. Track the closest value seen while descending. No stacks at all.
- **Find K Closest Elements (LeetCode 658) on a sorted array.** The same "window around target" idea, but random access lets you binary search the window's left edge directly in `O(log(n - k))`. The tree version has no random access, so it walks outward instead.
- **BST Iterator with `prev()` and `next()` (LeetCode 1586-style).** This is one of the two stacks made bidirectional. Keeping a cache of already-visited values makes moving backwards cheap.
- **K closest in a plain binary tree (not a BST).** Sortedness is gone, so there is no window. You fall back to a size-`k` max-heap keyed by distance over all `n` nodes, `O(n log k)`. This is the K Closest Points to Origin pattern.

## What to carry forward

A BST's inorder sequence is a sorted line, and an inorder stack is a cursor on it. Put two cursors at the target, one facing each way, and merge outward. The next problem keeps the inorder line but looks at it for a different reason: a place where it goes downhill when it should not, a "dip" that betrays two swapped values.
