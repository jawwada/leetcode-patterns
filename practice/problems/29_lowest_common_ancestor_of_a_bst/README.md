# Lowest Common Ancestor of a BST (LeetCode 235)

**Area:** trees · **Difficulty:** Medium · **Key operations:** compare both targets with the node, go left if both smaller, go right if both larger, stop at the split

## Problem

Given a binary search tree and two values `p` and `q` that occur in it, return the value of their lowest common ancestor: the deepest node that has both `p` and `q` as descendants, where a node counts as a descendant of itself.

## Example

```
[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]

            6
          /   \
         2     8
        / \   / \
       0   4 7   9
          / \
         3   5

p = 3, q = 5  ->  4     (walk 6 -> 2 -> 4)
p = 2, q = 8  ->  6
p = 2, q = 4  ->  2     (2 is an ancestor of 4, so it is its own LCA)
```

## Brute force

Descend from the root to `p` recording the path, descend again to `q` recording that path, then walk both lists in parallel and return the last node they share.

O(h) time and O(h) space. The wasted work: the two paths are identical up to the split point, so that prefix is walked twice and stored twice, only for its last element to be read.

## From brute force to optimal

The two paths agree exactly as long as `p` and `q` fall on the same side of the current node, and in a BST "which side" is decided by a comparison with the node's value. If both targets are smaller, both paths turn left; if both are larger, both turn right; otherwise one is on each side (or the node is one of them), which is precisely the split, and the split is the LCA. So a single descent from the root that stops at the first split finds the answer with no path storage. The invariant: the current node is an ancestor of both targets.

## Intuition

Every node of a BST cuts the number line at its value: left means smaller, right means larger. Take the interval `[min(p, q), max(p, q)]`. Walking down, as long as the node's value lies entirely outside that interval, both targets are on the same side and you step toward them. The first node whose value falls inside the interval (ends included) separates the two, and that node is the lowest common ancestor. Above it the targets travel together; below it they are apart.

## Walkthrough

`p = 3`, `q = 5`, so the target interval is `[3, 5]`.

```
            6        at 6: 5 < 6, both targets are smaller   -> go left
          /   \
         2     8     at 2: 3 > 2, both targets are larger    -> go right
        / \   / \
       0   4 7   9   at 4: 3 <= 4 <= 5, the paths split here -> LCA 4
          / \
         3   5

p = 2, q = 8:  at 6: 2 <= 6 <= 8  -> LCA 6 in one step
p = 2, q = 4:  at 6: both < 6, go left; at 2: 2 <= 2 <= 4 -> LCA 2 (2 is p itself)
```

## Steps

1. `lo, hi = min(p, q), max(p, q)`; `node = root`.
2. While `node` exists: if `hi < node.val`, go left; else if `lo > node.val`, go right; else return `node.val`.

## Complexity

O(h) time: one pointer walks a single root-to-LCA path, `h` being the height (log n balanced, n skewed). O(1) extra space.

## Pitfalls

- **`<=` when turning.** `if hi <= node.val` steps past a node that *is* `q`: `p = 0`, `q = 2` returns 0 instead of 2. Equality means the node is a target and therefore the LCA; turn only on strict comparisons.
- **Assuming `p < q`.** Using `lo, hi = p, q` without `min`/`max` gives an empty interval when `p > q`; `p = 8`, `q = 2` walks left from 6 and off the tree.
- **Turning the wrong way.** Going right when both targets are smaller leaves the subtree that holds them: `p = 3`, `q = 5` walks `6 -> 8 -> 9 -> None`.
- **Applying this to a non-BST.** The value comparison is only meaningful with the BST ordering; a general binary tree needs the recursive LCA (LeetCode 236).
- **Forgetting that a node is its own descendant.** The LCA of 2 and 4 is 2, not 6; the "else" branch covers this because `lo == node.val` is neither strictly smaller nor strictly larger.
