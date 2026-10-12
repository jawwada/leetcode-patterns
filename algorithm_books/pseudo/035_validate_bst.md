---
rank: 35
slug: validate_bst
---

Given the root of a binary tree, decide whether it is a valid binary search tree: for every node, all values in its left subtree are strictly smaller than the node's value and all values in its right subtree are strictly larger. `[2, 1, 3]` is valid. `[5, 4, 6, null, null, 3, 7]` is not, even though every child sits on the correct side of its own parent, because `3` lives in the right subtree of `5`.

The tempting check compares each node only with its children, and that second tree is exactly why it fails: `3 < 6` is fine locally, yet the root promised that everything on its right exceeds `5`. The BST rule is a promise about whole subtrees, and promises pile up on the way down. Each time the path turns left at a node, everything below is capped by that node's value; each time it turns right, everything below is floored by it. So carry the promises as one open interval `(low, high)`. The root may hold anything, `(-∞, ∞)`; a left child keeps its parent's `low` and takes the parent's value as its `high`; a right child keeps `high` and takes the parent's value as its `low`. A node passes when its value lies strictly inside its interval, and the tree is valid when every node passes.

Geometrically, each node cuts the number line at its value, and stepping into a subtree keeps only one side of the cut. The window at a node is the gap between two ancestors: the nearest one it hangs to the right of and the nearest one it hangs to the left of. The search stops at the first node outside its window, so `7` below is never looked at.

```text
           5                 node   allowed range   verdict
         /   \                 5      (-∞, ∞)         inside
        4     6                4      (-∞, 5)         inside
             / \               6      (5, ∞)          inside
            3   7              3      (5, 6)          3 ≤ 5: outside → false
                               7      never checked
each parent-child pair looks fine (4 < 5, 6 > 5, 3 < 6, 7 > 6), yet 3 < 5
```

```pseudo
FUNCTION IsValidBST(root)
    RETURN Fits(root, -∞, ∞)

FUNCTION Fits(node, low, high)
    IF node = null
        RETURN true
    IF node.val ≤ low OR node.val ≥ high
        RETURN false                       // breaks a promise made higher up
    IF NOT Fits(node.left, low, node.val)  // left side: below node.val
        RETURN false
    RETURN Fits(node.right, node.val, high)    // right side: above node.val
```

Each node is checked once, so validation costs `O(n)` time and `O(h)` space for the recursion. The equivalent test is an inorder traversal: a tree is a BST exactly when its inorder sequence is strictly increasing, so walk it while remembering the previous value and fail on the first value that is not larger. The same inorder walk, stopped at the `k`-th value, finds the `k`-th smallest element. Strict inequalities make duplicates invalid, as the definition demands. Reach for the interval whenever a constraint flows from ancestors to descendants rather than from parent to child. The classic mistake is the parent-versus-child check; the runner-up is seeding the bounds with the smallest and largest 32-bit integers, which rejects a lone root holding exactly one of those values, a trap that `-∞` and `∞` avoid.

*Practice:* LC 98 Validate Binary Search Tree · LC 230 Kth Smallest Element in a BST · LC 99 Recover Binary Search Tree
