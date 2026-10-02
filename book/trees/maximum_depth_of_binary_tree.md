# Maximum Depth of Binary Tree

*LeetCode 104 · Easy · Pattern: Tree recursion (post-order) · Reading time ~5 min*

## What the problem is really asking

Count the nodes on the longest path that starts at the root and ends at a leaf. The answer is one integer. It is not
hard to compute; it is hard to compute *without thinking about every path*. This is the warm-up for the habit the whole
chapter depends on: write the answer for a node in terms of the answers for its children.

```text
        3            longest root-to-leaf paths:
       / \             3 -> 20 -> 15   (3 nodes)
      9   20           3 -> 20 -> 7    (3 nodes)
         /  \        short one:
        15   7         3 -> 9          (2 nodes)
                     answer = 3
```

Note the unit: nodes, not edges. A single node has depth 1; an empty tree has depth 0.

## Do it by hand first

Most people answer by staring at the picture and finding the lowest leaf. Do it more slowly, from the bottom. Write a
number next to each node: "how tall is the tree hanging from here?". A leaf gets 1. A node gets one more than its taller
child.

```text
        3 [3]          9:  leaf               -> 1
       / \             15: leaf               -> 1
  [1] 9   20 [2]       7:  leaf               -> 1
         /  \          20: 1 + max(1, 1)      -> 2
   [1] 15    7 [1]     3:  1 + max(1, 2)      -> 3
```

Your hand kept track of **one number per node**, and each number was made from the two numbers just below it. You never
looked at a whole path. That bottom-up label is the algorithm.

## The first honest attempt

List every root-to-leaf path explicitly, then return the length of the longest. A walk that copies the current path into
each child does it.

```text
path list after the walk:
  [3, 9]
  [3, 20, 15]
  [3, 20, 7]
   ^^^^^  copied twice: once for 15, once for 7
```

This is O(n·h): up to n/2 leaves, each holding a copy of a path up to h long. The repeated work is the shared prefix.
Every leaf below 20 re-stores `3, 20`. In a big balanced tree, the root's value is copied once per leaf. And the
contents of the paths are never used; only their lengths are.

## The turning point

**Claim: the depth of a tree is 1 + the larger of its two subtrees' depths, and the depth of an empty tree is 0.**

Justify it by looking at the longest path from the node. It starts at the node (that is the 1), then must go into either
the left subtree or the right subtree, and from there it is a root-to-leaf path of that subtree. The longest such path in
the left subtree has length depth(left); same on the right. Pick the better side. Nothing about the parent or the
siblings matters.

That is the first use of **trust the call on the child**. You do not ask how `depth(left)` figures out its answer. You
assume it is right, add one, and take a max. The empty tree returns 0 so that a leaf comes out as `1 + max(0, 0) = 1`.

The recursion is post-order: a node can only answer after both children have answered. Each node is entered exactly once
and returns a single integer. No path is ever stored.

## Watch it work

Tree `[3,9,20,null,null,15,7]`. Brackets show values already returned; `*` marks the call that is running; the stack
column lists paused callers.

```text
Frame 1: depth(9) runs; both children None -> 0, 0
        3              stack: depth(3)
       / \
     *9   20           9 returns 1 + max(0,0) = 1
```

The left child of the root answers first, because the left call is made first.

```text
Frame 2: depth(20) called, descends into 15
        3              stack: depth(3), depth(20)
       / \
   [1]9   20
         /  \
      *15    7         15 returns 1
```

The root is paused waiting on its right side; 20 is paused waiting on its left side.

```text
Frame 3: depth(7) runs
        3              stack: depth(3), depth(20)
       / \
   [1]9   20
         /  \
    [1]15   *7         7 returns 1
```

Both children of 20 have answered.

```text
Frame 4: 20 combines: 1 + max(1, 1)
        3              stack: depth(3)
       / \
   [1]9  *20 -> 2
         /  \
    [1]15   [1]7
```

20's label is now fixed at 2 and its frame is gone from the stack.

```text
Frame 5: 3 combines: 1 + max(1, 2)
       *3 -> 3         stack: empty
       / \
   [1]9  [2]20
         /  \
    [1]15   [1]7       answer 3
```

The root returns 3. Across every frame, a returned label equals the true height of that node's subtree, and the stack
holds exactly the path from the root to the running node.

## Why it is correct

Induction on the shape. An empty tree has depth 0: correct. For a node, assume the two calls return the true depths of
its subtrees. Every root-to-leaf path from this node is the node plus a root-to-leaf path in one of the subtrees, so the
longest one has length 1 + max of the two. The function returns exactly that. Since every call is correct when its
children's calls are, the root's call is correct.

## Cost

Time O(n): each node is entered once and does O(1) work beyond its two calls. Space O(h) for the call stack: O(log n)
when balanced, O(n) for a skewed stick.

## Variations you will meet

- **Minimum depth (LeetCode 111).** Not just `min` instead of `max`: a node with one missing child is not a leaf, so the
  missing side must be ignored, not counted as 0. BFS that stops at the first leaf is often simpler.
- **Iterative BFS.** Count levels with a queue; the number of rows processed is the depth. Avoids recursion limits.
- **N-ary tree depth (LeetCode 559).** Same formula, `1 + max` over all children.
- **Depth in edges.** Return -1 for an empty tree, or subtract 1 at the end. Diameter later uses edges.

## What to carry forward

A node's answer is built from its children's answers plus one local step; trust the child, handle `None`. The next
problem keeps the same one-visit walk but, instead of returning a number, it rewires each node it visits.
