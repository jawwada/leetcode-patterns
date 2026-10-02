# Kth Smallest Element in a BST

*LeetCode 230 · Medium · Pattern: Iterative in-order traversal with early stop · Reading time ~7 min*

## What the problem is really asking

You get a valid BST and an integer `k` (1-indexed). Return the `k`-th smallest value in it.

The answer is one value. The question underneath is: where does the BST keep its sorted order, and how little of it do we need to read? An unsorted tree would force us to look at every value. A BST has already done the sorting; it is just stored as a shape instead of an array.

Running example: `[5,3,6,2,4,null,null,1]`, `k = 3`.

```text
              5
            /   \
           3     6
          / \
         2   4
        /
       1

 inorder line:  1   2   3   4   5   6
                        ^
                     3rd smallest = 3
```

## Do it by hand first

Who is the smallest? Keep going left from the root until you cannot: 5, 3, 2, 1. So 1 is first. The second smallest is the next node on the inorder line: back up to 2. Third: 2 has no right child, so back up again to 3. Stop. You never looked at 4, 5's other side, or 6.

```text
 down-left:   5 -> 3 -> 2 -> 1    (count 1 at the bottom)
 back up:               2         (count 2)
 back up:          3              (count 3, stop)
 untouched:  4, 5 (not yet visited), 6
```

Your hand did the inorder walk from Binary Tree Inorder Traversal, kept a stack of ancestors still owed a visit, and kept one counter. It stopped the moment the counter reached `k`.

## The first honest attempt

Collect every value with any traversal, sort the list, return index `k - 1`. That is `O(n log n)` time and `O(n)` space.

```text
 collect (preorder):  5 3 2 1 4 6
 sort:                1 2 3 4 5 6   <- the BST already
 index k-1 = 2:       3                encoded this order
     work done on 4, 5, 6: wasted
     the sort: wasted (inorder gives sorted order for free)
```

Two kinds of waste. The sort redoes work the BST invariant already did. And all `n` values are gathered when only the first `k` are needed; if `k = 1` in a tree of a million nodes, we touched a million nodes to read one.

A recursive inorder fixes the sort but not the second waste unless you thread a "found it, stop now" flag through every call.

## The turning point

**Claim: in a BST, inorder visits values in increasing order, so the `k`-th node popped by an iterative inorder is the answer, and we can stop right there.**

The first half is the "second view" from Validate BST: a tree is a BST exactly when its inorder reading is strictly increasing. So inorder *is* the sorted array, read lazily.

The second half is why the iterative form from Binary Tree Inorder Traversal is the right tool. Its state is an explicit stack and a pointer. Each pop produces the next sorted value. To stop, just `return`: there is no recursion to unwind and no flag to check. The loop is the same as before with a counter in the visit step:

```text
 while True:
     while node: stack.append(node); node = node.left
     node = stack.pop()
     k -= 1
     if k == 0: return node.val
     node = node.right
```

`while True` is safe because the problem guarantees `1 <= k <= n`, so the `k`-th pop always happens before the tree runs out.

The cost now depends on `k`, not `n`. Reaching the smallest value means sliding down one spine, `O(h)`. Each later pop is amortised `O(1)`, because every node is pushed once and popped once over the whole walk.

## Watch it work

Tree `[5,3,6,2,4,null,null,1]`, `k = 3`. Stack drawn bottom to top.

Frame 1. Slide left from the root to the minimum.

```text
          [5]            stack: 5 3 2 1   (top = 1)
          /              k = 3
        [3]              node: None
        /
      [2]
      /
    [1]
```

The whole left spine is on the stack. Its top is the smallest value.

Frame 2. Pop 1: the 1st smallest.

```text
 pop 1   k: 3 -> 2
 stack: 5 3 2       node: 1.right = None
```

No right child, so the next slide pushes nothing.

Frame 3. Pop 2: the 2nd smallest.

```text
 pop 2   k: 2 -> 1
 stack: 5 3         node: 2.right = None
```

Frame 4. Pop 3: the 3rd smallest. `k` hits 0, return.

```text
 pop 3   k: 1 -> 0   -> return 3
 stack: 5           (never popped)
 never pushed: 4, 6
```

The walk ended with 5 still on the stack and 4 and 6 never touched.

Across frames, the top of the stack was always the smallest value not yet counted, and `k` was always "how many more pops until the answer".

## Why it is correct

The iterative inorder pops nodes in inorder (shown in Binary Tree Inorder Traversal). In a valid BST, inorder order is increasing order (the BST rule says every left-subtree value is smaller than the node and every right-subtree value is larger, applied recursively). So the `i`-th pop is the `i`-th smallest value. The counter starts at `k` and drops by one per pop, so it reaches zero exactly at the `k`-th pop, and that value is returned.

## Cost

- Time `O(h + k)`: one spine of length at most `h` is pushed to reach the minimum, then `k` pops, each amortised `O(1)` including the pushes they trigger.
- Space `O(h)`: the stack never holds more than one root-to-leaf spine.

On a balanced tree with small `k` that is `O(log n)`, against `O(n log n)` for collect-and-sort.

## Variations you will meet

- **Frequent queries with inserts and deletes (the official follow-up).** Store in each node the size of its subtree. At a node, if `k <= size(left)` go left; if `k == size(left) + 1` this is it; else go right with `k -= size(left) + 1`. That is `O(h)` per query with no traversal, and updates adjust sizes along one path.
- **Kth largest.** Run reverse inorder (right spine first) and count down the same way.
- **BST Iterator (LeetCode 173).** The same stack, with the loop body cut into a `next()` method. This problem is the iterator called `k` times.
- **Two Sum IV in a BST (LeetCode 653).** Run one ascending and one descending iterator at the same time, and move them like two pointers on a sorted array.

## What to carry forward

In a BST, "sorted" is free: an iterative inorder is a lazy sorted array that you can stop after `k` steps. The next problem uses the BST order differently: instead of reading the line, it uses comparisons to decide which way to walk down.
