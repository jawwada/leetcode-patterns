# Validate Binary Search Tree (LeetCode 98)

**Area:** trees · **Difficulty:** Medium · **Key operations:** pass down an open window (lo, hi), check lo < val < hi, tighten hi going left and lo going right

## Problem

Given the root of a binary tree, return `True` if it is a valid binary search tree: every node is strictly greater than **all** values in its left subtree and strictly less than **all** values in its right subtree. Duplicates are not allowed.

## Example

```
[5, 1, 4, None, None, 3, 6]          [2, 1, 3]

        5                                2
       / \                              / \
      1   4                            1   3
         / \
        3   6

-> False (4 < 5 sits as the            -> True
   right child; 3 is also < 5)
```

## Brute force

Walk the tree inorder (left, node, right) and collect every value into a list. A tree is a BST exactly when that list is strictly increasing, so check neighbours pairwise.

O(n) time but O(n) extra space, and a second pass over a copy of the data. The wasted work: the whole sequence is materialised before a single comparison happens, so a violation at the root is only noticed after visiting every node, and the method cannot say *which* node broke the rule.

## From brute force to optimal

Checking a node against its parent alone is not enough: in `[5, 4, 6, None, None, 3, 7]` the 3 is smaller than its parent 6 (fine) but it lives in the right subtree of 5, so it must also be greater than 5. An ancestor does not need to inspect every descendant, though; it only needs to hand down a constraint. Every node receives an open window `(lo, hi)` that all values in its subtree must satisfy. Going left, the node becomes the new `hi`; going right, it becomes the new `lo`. A node is valid with respect to all its ancestors exactly when `lo < val < hi`. One traversal, each node checked once, and the first violation stops the recursion immediately.

## Intuition

Picture each node receiving a window on the number line. The root's window is `(-inf, +inf)`. Stepping to a left child slides the right wall in to the parent's value; stepping to a right child slides the left wall in. Windows only ever shrink on the way down, and they accumulate every ancestor's rule at once: the 3 under 6 under 5 receives `(5, 6)` and is caught even though its parent is fine. Strict inequalities enforce "no duplicates", since touching a wall means equalling an ancestor.

## Walkthrough

The docstring example, with the window each node receives.

```
        5          (-inf, inf)
       / \
      1   4        1 gets (-inf, 5)     4 gets (5, inf)
         / \
        3   6

node 5   window (-inf, inf)   -inf < 5 < inf   ok
                              left gets (-inf, 5), right gets (5, inf)
node 1   window (-inf, 5)     -inf < 1 < 5     ok
                              left gets (-inf, 1), right gets (1, 5)
         left None  -> True, right None -> True
node 4   window (5, inf)      5 < 4 ?  no      -> False, stop

result False
```

The grandparent trap, where only the window catches the error:

```
        5          (-inf, inf)
       / \
      4   6        4 gets (-inf, 5)     6 gets (5, inf)
         / \
        3   7      3 gets (5, 6)  ->  5 < 3 ?  no  -> False
```

## Steps

1. `valid(node, lo, hi)`: an empty subtree is valid.
2. If not `lo < node.val < hi`, return `False`.
3. Return `valid(left, lo, node.val) and valid(right, node.val, hi)`.
4. Start with `valid(root, -inf, +inf)`.

## Complexity

O(n) time: each node is compared once against its window. O(h) space for the recursion stack, where `h` is the height.

## Pitfalls

- **`<=` instead of `<`.** The walls are ancestor values, so touching one means a duplicate. With `<=`, `[2, 2, 2]` is accepted.
- **Not tightening `lo` for the right child.** Passing `(lo, hi)` unchanged to the right subtree lets a small value hide there: `[5, 4, 6, None, None, 3, 7]` is accepted although 3 lies to the right of 5. Symmetrically, `hi` must become `node.val` for the left child.
- **`or` instead of `and`.** One valid subtree then hides a broken sibling: `[5, 1, 4, None, None, 3, 6]` passes because the left subtree is fine.
- **Comparing only with the parent.** The classic wrong answer: it accepts the grandparent trap above. The window carries every ancestor's constraint.
- **Finite sentinels.** Using `sys.maxsize` or a fixed large number as the initial walls can collide with real values; use `±inf` or `None`.
