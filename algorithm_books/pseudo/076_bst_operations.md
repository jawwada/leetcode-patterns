---
rank: 76
slug: bst_operations
---

A binary search tree keeps every value in a node's left subtree smaller than the node and every value in its right subtree larger. Search for a value, insert a new one and delete an existing one, keeping that order intact. Deleting `3` from `[5, 3, 6, 2, 4, null, 7]` gives `[5, 4, 6, 2, null, null, 7]`: the successor `4` moves up into the gap.

All three operations ride on one move. At each node a single comparison throws away an entire subtree, so the walk follows one path from the root toward a leaf. Search loops down that path until it meets the value or falls off the tree. Insert follows the same path to the empty spot where the value would have been and hangs a new leaf there. Written recursively, each call returns the root of its subtree and the parent reattaches whatever comes back, so the one new link is made without any special case, not even for an empty tree.

Delete is the operation with cases, sorted by the number of children the doomed node has. A leaf simply disappears, and its parent receives null. A node with one child is spliced out and the child takes its place; the order survives because that whole subtree already sat on the correct side of the parent. A node with two children cannot leave without orphaning one of them, so it keeps its place and changes its value instead. The standard replacement is the in-order successor, the smallest value of the right subtree, found by stepping right once and then left as far as possible: it is larger than everything on the left and smaller than everything else on the right. Copy it up, then delete it from the right subtree, where it has no left child and so falls into an easy case.

```text
3 < 5: go left, then 3     successor: right once,     copy 4 up; deleting the
is found with 2 children   then left to the end: 4    old 4 is the leaf case
      5                          5                          5
    /   \                      /   \                      /   \
   3     6                    3     6                    4     6
  / \     \                  / \     \                  /       \
 2   4     7                2  (4)    7                2         7
```

```pseudo
FUNCTION Search(root, val)
    node ← root
    WHILE node ≠ null AND node.val ≠ val
        IF val < node.val
            node ← node.left
        ELSE
            node ← node.right
    RETURN node                            // the node holding val, or null

FUNCTION Insert(root, val)
    IF root = null
        RETURN new TreeNode(val)           // the empty spot: a new leaf
    IF val < root.val
        root.left ← Insert(root.left, val)
    ELSE IF val > root.val
        root.right ← Insert(root.right, val)
    RETURN root                            // equal: already present

FUNCTION Delete(root, val)
    IF root = null
        RETURN null                        // val is not in the tree
    IF val < root.val
        root.left ← Delete(root.left, val)
    ELSE IF val > root.val
        root.right ← Delete(root.right, val)
    ELSE
        IF root.left = null                // leaf, or right child only
            RETURN root.right
        IF root.right = null               // left child only
            RETURN root.left
        successor ← root.right             // two children: leftmost node
        WHILE successor.left ≠ null        // of the right subtree
            successor ← successor.left
        root.val ← successor.val           // copy it up...
        root.right ← Delete(root.right, successor.val)   // ...and remove it
    RETURN root
```

Each operation walks a single path, so all three cost `O(h)`: `O(log n)` while the tree stays balanced, `O(n)` once sorted insertions have stretched it into a chain, which is why the ordered maps of standard libraries are self-balancing trees. Reach for a BST when data must stay sorted while it changes: the next larger value, every value in a range, the `k`-th smallest (#77 walks a BST in order). The in-order predecessor, the largest value of the left subtree, works just as well as the replacement. The classic mistake is deleting the original value from the right subtree after copying the successor up, instead of the successor's value: the original is no longer there, nothing is removed, and the tree ends up holding the successor twice.

*Practice:* LC 700 Search in a Binary Search Tree · LC 701 Insert into a Binary Search Tree · LC 450 Delete Node in a BST
