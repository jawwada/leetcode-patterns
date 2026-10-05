# Invert Binary Tree

*LeetCode 226 · Easy · Pattern: Tree recursion (post-order) · Reading time ~5 min*

## The problem

Given the root of a binary tree, mirror it so that every node's left and right children are swapped, all the way down,
and return the root.

```text
Example: [4,2,7,1,3,6,9] becomes [4,7,2,9,6,3,1].
```

## What the problem is really asking

Turn the tree into its mirror image: what was on the left of every node is now on the right, at every level, all the way
down. Return the same root. The answer is a tree, and you are allowed (expected) to change the one you were given.

```text
   before              after (fold along the centre line)
        4                     4
      /   \                 /   \
     2     7               7     2
    / \   / \             / \   / \
   1   3 6   9           9   6 3   1
```

What makes it slightly tricky is that "mirror" is not only "swap the root's two children". After swapping 2 and 7, the
subtree under 7 still has 6 on its left. Every node has to be flipped.

## Do it by hand first

With the drawing in front of you, you would go node by node and cross the two arms of each: at 4 swap 2 and 7; at 7 swap
6 and 9; at 2 swap 1 and 3. Leaves have nothing to swap.

```text
node   left  right   after swap
4      2     7       7 2
7      6     9       9 6
2      1     3       3 1
1,3,6,9  (leaves)    nothing
```

You kept track of **which nodes you had already flipped**. One swap per node, each node once, and the order did not
matter. That is the whole algorithm: a walk that visits every node and swaps its two pointers.

## The first honest attempt

Build a brand-new tree. For each original node allocate a copy whose left child is the mirrored copy of the original
right subtree, and whose right child is the mirrored copy of the original left.

```text
original 4 ----copy----> new 4'
         2 ----copy----> new 2'     n allocations, and
         7 ----copy----> new 7'     n values copied that
         ...                        never change
```

It is O(n) time, which is already optimal, but O(n) extra memory. The waste is the allocation itself: values never
change, only which pointer is called "left". A new node for every old node just to re-label two pointers.

## The turning point

**Claim: a tree is mirrored exactly when every node has had its two children swapped once, and each swap is a local O(1)
operation on that node.**

Why: mirror(T) is the node with left = mirror(T.right) and right = mirror(T.left). Unroll that definition and every node
appears once, with its two child pointers exchanged; values and depths do not move. So nothing needs copying. Walk the
tree, at each node exchange the two pointers.

Trust the child: assume `invert(child)` returns that child's subtree already mirrored. Then the node's job is one line,
the left pointer gets the inverted right subtree and the right pointer gets the inverted left. Do both assignments in a
single tuple assignment so neither original pointer is lost before it is read.

Pre-order (swap, then recurse) and post-order (recurse, then swap) both work. The solution evaluates
`invert(root.right)` first, then `invert(root.left)`, and only then assigns both pointers.

## Watch it work

Tree `[4,2,7,1,3,6,9]`. `*` marks the running call; `done` marks subtrees whose call has returned (already mirrored).

```text
Frame 1: invert(4) evaluates invert(right) first -> enters 7
          4            stack: invert(4)
        /   \
       2    *7
      / \   / \
     1   3 6   9
```

Because the tuple's first item is `invert(root.right)`, the right side is processed first.

```text
Frame 2: 7 inverts 9 then 6 (leaves return as is), then swaps
          4            stack: invert(4)
        /   \
       2     7 done
      / \   / \
     1   3 9   6       7.left=9, 7.right=6
```

The leaves return themselves; 7 now holds 9 on the left.

```text
Frame 3: invert(4) now evaluates invert(left) -> enters 2
          4            stack: invert(4)
        /   \
      *2     7 done
      / \   / \
     1   3 9   6
```

Pointers of 4 are still untouched: both tuple items must be computed before assignment.

```text
Frame 4: 2 inverts 3 then 1, then swaps
          4            stack: invert(4)
        /   \
       2     7 done
      / \   / \
     3   1 9   6       2.left=3, 2.right=1
```

Both subtrees are mirrored internally but still on the original sides.

```text
Frame 5: 4 assigns left = (mirrored 7), right = (mirrored 2)
          4 done       stack: empty
        /   \
       7     2         result [4,7,2,9,6,3,1]
      / \   / \
     9   6 3   1
```

Invariant across frames: when a call returns, its whole subtree is mirrored, and nodes outside it are untouched.

## Why it is correct

Induction on the shape. An empty tree mirrored is empty: return `None`. For a node, assume both calls return their
subtrees mirrored. Placing the mirrored right subtree on the left and the mirrored left on the right is exactly the
definition of the mirror. The tuple assignment guarantees both originals were read before either pointer changed.

## Cost

Time O(n): one visit and one swap per node. Space O(h) for the recursion stack; an explicit stack or queue version has the
same worst case (O(n) on a stick or a wide last level).

## Variations you will meet

- **Iterative with a queue or stack.** Pop a node, swap its children, push the non-null children. Order does not matter
  since each swap is independent; avoids recursion limits.
- **Return a new mirrored tree, leave the original intact.** Then the copying brute force is the right answer.
- **Flip equivalence (LeetCode 951).** Two trees are equivalent if some set of swaps makes them equal: at each node try
  "children match straight" or "children match crossed". That is a two-tree recursion, which is where we go next.

## What to carry forward

One swap per node, done by a walk; the tuple swap reads both pointers before writing either. The next problem walks two
trees at once instead of one, comparing them position by position.
