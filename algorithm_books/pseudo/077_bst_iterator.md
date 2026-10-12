---
rank: 77
slug: bst_iterator
---

Design an iterator over a binary search tree that hands out its values in ascending order: `next()` returns the next smallest value and `has_next()` says whether any are left. For `[7, 3, 15, null, null, 9, 20]`, five calls to `next()` return `3`, `7`, `9`, `15` and `20`, and `has_next()` turns false after the last one.

The easy answer runs an inorder traversal up front and stores all `n` values in a list, paying `O(n)` memory before the first call. A real iterator does the traversal lazily, one step per call, which means pausing an inorder walk in the middle. A recursive walk knows where it is through the ancestors whose values are still owed, the ones it left by going down into their left subtrees; keep exactly those on an explicit stack and pausing is free. Start by pushing the root and its whole left spine, so the top of the stack is the leftmost node, the smallest value. Each `next()` pops the top, the smallest value not yet returned, and before handing it out pushes the left spine of the popped node's right child, because the values just above the popped one live in that right subtree, smallest first along its spine.

The stack always holds a chain of nodes, each in the left subtree of the one below it. Everything inside the right subtree being explored is smaller than every ancestor still waiting underneath, which is why the order never breaks.

```text
       7          call         returns   stack after (top on the right)
      / \         init                   [7, 3]
     3   15       next()          3      [7]
        /  \      next()          7      [15, 9]
       9    20    has_next()     true    [15, 9]
                  next()          9      [15]
                  next()         15      [20]
                  next()         20      []
                  has_next()     false   []
```

```pseudo
CLASS BSTIterator
    FUNCTION Init(root)
        self.stack ← empty stack
        self.PushLeft(root)

    FUNCTION PushLeft(node)
        WHILE node ≠ null                  // walk down the left spine
            self.stack.push(node)
            node ← node.left

    FUNCTION Next()
        node ← self.stack.pop()            // the smallest value still waiting
        self.PushLeft(node.right)          // its successors live on the right
        RETURN node.val

    FUNCTION HasNext()
        RETURN len(self.stack) > 0

FUNCTION KthSmallest(root, k)
    iterator ← new BSTIterator(root)
    value ← null
    FOR i FROM 0 TO k - 1
        value ← iterator.Next()
    RETURN value
```

A single `next()` can push a long spine, but over the whole iteration every node is pushed once and popped once, so `n` calls cost `O(n)` in total, `O(1)` amortized each, and `has_next()` is always `O(1)`. The stack holds at most one node per level, `O(h)` space instead of `O(n)`. The `k`-th smallest value is just `k` calls to `next()`, `O(h + k)` time. Reach for this whenever a tree must be consumed in sorted order one value at a time: merging two BSTs by advancing two iterators like two sorted lists, finding a pair with a given sum with one ascending and one descending iterator, or finding an in-order successor. The classic mistake is pushing only the popped node's right child instead of its whole left spine; on this tree the iterator then returns `3, 7, 15, 20` and never sees `9`.

*Practice:* LC 173 Binary Search Tree Iterator · LC 230 Kth Smallest Element in a BST · LC 285 Inorder Successor in BST · LC 1305 All Elements in Two Binary Search Trees
