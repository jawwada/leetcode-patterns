# Balanced Binary Tree

*LeetCode 110 · Easy · Pattern: Post-order height with side-channel answer · Reading time ~5 min*

## What the problem is really asking

A tree is height-balanced when, at **every** node, the heights of its left and right subtrees differ by at most 1.
Return whether the tree is balanced. The answer is yes or no, but computing it needs heights, so the real object is a
height at every node.

```text
        1           heights (nodes):
       / \            left of root:  2-3-4 chain -> 3
      2   2           right of root: 2-3-4 chain -> 3
     /     \        root: |3 - 3| = 0, looks fine
    3       3
   /         \      but look lower: the left 2 has
  4           4     heights 2 and 0 -> NOT balanced
```

What makes it subtle: it is not enough to check the root. A tree can look even at the top and be lopsided lower down.

## Do it by hand first

Label every node with its height, bottom-up, as in Maximum Depth. Next to each label, write the difference between the
two children's labels. Any difference of 2 or more means "no".

```text
node   L height   R height   diff   height
4(L)   0          0          0      1
3(L)   1          0          1      2
2(L)   2          0          2      BROKEN -> stop
```

You kept track of **two numbers at each node: its height, and whether everything below it was fine**. The first is what
the parent needs to compute its own height; the second is the answer.

## The first honest attempt

Write a standalone `height()` function. At each node, call `height(left)` and `height(right)`, check the difference, then
recurse into both children to check them too.

```text
skewed chain of 4 nodes, height() calls:

  at a:  height(b) walks b c d    (3 nodes)
  at b:  height(c) walks   c d    (2 nodes, again)
  at c:  height(d) walks     d    (1 node, again)
         d's height computed 3 times
```

Each subtree's height is recomputed once per ancestor: O(n²) on a skewed tree, O(n log n) on a balanced one. The heights
are computed bottom-up inside `height()` anyway, and then thrown away.

## The turning point

**Claim: the balance check at a node needs exactly the two numbers `height()` already computes there, so one post-order
pass can return the height and do the check at the same time.**

Fold the check into `height()`. To carry the yes/no without a second return value, use a sentinel: return `-1` to mean
"something in my subtree is unbalanced". Real heights are never negative, so `-1` cannot be confused with one.

```text
height(node):
  None             -> 0
  left is -1       -> -1         (stop, do not even look right)
  right is -1      -> -1
  |left - right|>1 -> -1         (this node breaks it)
  otherwise        -> 1 + max(left, right)
```

This is the first appearance of the chapter's template: the function **returns** a value the parent can extend (a height)
and, on the side, decides the answer. Here the side channel is folded into the return value itself; in the next problem
it lives in a separate variable. Once any node returns `-1`, every ancestor returns `-1` immediately: the answer is
already known.

## Watch it work

Tree `[1,2,2,3,null,null,3,4,null,null,4]` (the picture above). Brackets show returned values; `*` marks the running
call.

```text
Frame 1: descend left to 4; 4's children return 0, 0
          1            stack: h(1), h(2L), h(3L)
         / \
        2   2
       /     \
      3       3
     /         \
   *4           4      4 returns 1
```

The leaf is height 1 and trivially balanced.

```text
Frame 2: h(3L): left 1, right 0, diff 1 -> returns 2
          1            stack: h(1), h(2L)
         / \
        2   2
       /     \
   *3[2]      3
     /         \
  [1]4          4
```

Diff of 1 is allowed; 3 reports its height.

```text
Frame 3: h(2L): left 2, right 0, diff 2 -> returns -1
          1            stack: h(1)
         / \
 *2[-1]     2
       /     \
   [2]3       3
     /         \
  [1]4          4
```

The first broken node is found and converted into the sentinel.

```text
Frame 4: h(1): left is -1 -> returns -1 at once
     *1[-1]            answer: -1 -> False
         / \
   [-1]2    2   <- never visited
             \
              3 -> 4  (whole right side skipped)
```

The root does not even call into its right subtree. Across frames, every returned non-negative number is a true height
of a balanced subtree, and `-1` travels straight up.

## Why it is correct

Invariant: `h(node)` returns the height of node's subtree if that subtree is balanced at every node, and `-1` otherwise.
`None` returns 0: correct. For a node, if either child returned `-1`, some node below is unbalanced, so `-1` is correct.
Otherwise both children are balanced with true heights; this node is balanced iff their difference is at most 1, and then
its height is 1 + max. The tree is balanced iff `h(root) != -1`.

## Cost

Time O(n): each node is visited at most once, often fewer thanks to the early exit. Space O(h) for the recursion stack.
The brute force is O(n²) worst case.

## Variations you will meet

- **Return a pair** `(balanced, height)` instead of a sentinel; clearer, same cost, no short-circuit unless you add one.
- **Balance a BST (LeetCode 1382).** In-order to a sorted list, then rebuild by always picking the middle as root.
- **AVL trees.** The same ±1 rule maintained during insertion with rotations; this problem is the checker.

## What to carry forward

Compute the height bottom-up and make every node judge itself with the two numbers it already has; a sentinel carries the
verdict upward for free. The next problem keeps returning heights but records the answer in a separate variable, because
the best path may bend at any node.
