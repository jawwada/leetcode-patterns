# Symmetric Tree

*LeetCode 101 · Easy · Pattern: Simultaneous tree recursion · Reading time ~5 min*

## What the problem is really asking

Is the tree its own mirror image? Fold the drawing along the vertical line through the root: every node must land on a
node with the same value, and every empty spot on an empty spot. The answer is yes or no.

```text
   symmetric               not symmetric
        1                        1
      /   \                    /   \
     2     2                  2     2
    / \   / \                  \     \
   3   4 4   3                  3     3
   |-mirror-|              3 is right of both 2s;
                           the mirror needs one on the left
```

The trap is the right-hand tree. Its levels hold the same values (`1`, `2 2`, `3 3`), so a check that ignores empty
spots says "symmetric". Shape matters, just as in Same Tree.

## Do it by hand first

Put one finger on the left 2 and one on the right 2. Compare. Now move them **apart**: the left finger goes left, the
right finger goes right, to the two outermost nodes. Compare. Come back, and move them **inward**: left finger goes right,
right finger goes left, to the two inner nodes. Compare.

```text
          1
        /   \
       2     2          pair (2, 2)   equal
      / \   / \
     3   4 4   3        outer (3, 3)  equal
     ^   ^ ^   ^        inner (4, 4)  equal
     outer inner outer
```

Your hands tracked **a pair of nodes that should be mirror images**, and the next pairs were always outer-with-outer and
inner-with-inner.

## The first honest attempt

Walk the tree level by level, writing out every child slot, including `None` for missing ones, and check each level
reads the same forwards and backwards.

```text
level 1: [2, 2]                     palindrome
level 2: [None, 3, None, 3]         reversed:
         [3, None, 3, None]         not equal -> False
```

That is O(n) time but O(w) memory for the widest level, plus a reversed copy. The waste: whole levels are built, padded
and reversed before any comparison, so a mismatch deep in one corner is noticed only after everything above it is
materialised. And the palindrome check is just pairing slot k from the left with slot k from the right, which could be
done directly.

## The turning point

**Claim: symmetry is a relation between two subtrees, not a property of one. The tree is symmetric exactly when the
root's left subtree is the mirror of its right subtree.**

Then define `mirror(a, b)` the way Same Tree defined `same(p, q)`, but crossing over:

- if either is `None`, the answer is whether both are;
- otherwise `a.val == b.val`, and `mirror(a.left, b.right)` (outer pair), and `mirror(a.right, b.left)` (inner pair).

Why crossing: in a mirror image, the left child of a sits opposite the right child of b. Compare with Same Tree, which
pairs left with left. Change one word and the problem changes from "copy" to "reflection".

```text
  same(a, b):    a.left <-> b.left     a.right <-> b.right
  mirror(a, b):  a.left <-> b.right    a.right <-> b.left
```

The answer is `mirror(root.left, root.right)`, and an empty tree is symmetric. No padding lists, and `and` stops at the
first failing pair.

## Watch it work

First on `[1,2,2,3,4,4,3]`. `*` marks the pair being compared; brackets show returned results.

```text
Frame 1: mirror(2L, 2R): values equal, go to outer pair
          1            stack: mirror(2,2)
        /   \
      *2     2*
      / \   / \
     3   4 4   3
```

The two fingers start on the root's children.

```text
Frame 2: outer pair mirror(3, 3): equal; both (None,None)
          1            stack: mirror(2,2), mirror(3,3)
        /   \
       2     2
      / \   / \
    *3   4 4   3*      returns True
```

Leaves pair up with leaves; their empty children match.

```text
Frame 3: inner pair mirror(4, 4): equal, returns True
          1            stack: mirror(2,2), mirror(4,4)
        /   \
       2     2
      / \   / \
   [T]3 *4 4* 3[T]
```

Both pairs under the 2s matched, so `mirror(2, 2)` returns True: symmetric.

Now the trap, `[1,2,2,null,3,null,3]`:

```text
Frame 4: mirror(2L, 2R): values equal, outer pair next
          1            stack: mirror(2,2)
        /   \
      *2     2*
        \     \
         3     3
```

The outer pair is 2L.left (None) against 2R.right (3).

```text
Frame 5: outer pair mirror(None, 3): one empty -> False
          1            answer False; the inner pair
        /   \          (3, None) is never examined
       2     2
      . \     \
    *    3     3*
  (None)
```

At every frame the two fingers sit at mirror-image positions, which is what makes a single value comparison meaningful.

## Why it is correct

Induction on pairs. Two empty subtrees are mirrors; one empty and one not are not. For two nodes, they are mirrors iff
their values match, a's left mirrors b's right, and a's right mirrors b's left; assuming the two calls answer those
correctly, the expression is correct. The whole tree is symmetric iff its two halves are mirrors.

## Cost

Time O(n): each mirror pair is compared once and each node is in exactly one pair. Space O(h) for the recursion.

## Variations you will meet

- **Iterative.** A queue of pairs: push `(a.left, b.right)` then `(a.right, b.left)`. Same comparisons, no recursion.
- **Invert then compare.** Invert a copy of the left half and run Same Tree against the right half; correct but more work.
- **Mirror two different trees.** Same `mirror(a, b)` function called on two roots.

## What to carry forward

Symmetry is "same tree, crossed": recurse on pairs, outer with outer, inner with inner. The next problem goes back to
Same Tree, but must try it from every node of a big tree, which forces us to find a faster way.
