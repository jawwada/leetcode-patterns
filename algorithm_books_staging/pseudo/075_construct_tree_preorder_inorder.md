---
rank: 75
slug: construct_tree_preorder_inorder
---

Given the preorder and inorder traversals of a binary tree whose values are all different, rebuild the tree. Preorder `[3, 9, 20, 15, 7]` and inorder `[9, 3, 15, 20, 7]` describe a root `3` with a left child `9` and a right child `20`, whose own children are `15` and `7`; in level order the tree is `[3, 9, 20, null, null, 15, 7]`.

Neither traversal pins the tree down alone, but together they do, because they answer different questions. Preorder lists every root before everything below it, so its first value is the root of the whole tree. Inorder lists the left subtree, then the root, then the right subtree, so the root's position there splits everything else into the two subtrees. The direct recursion finds the root with a linear scan of inorder and slices both arrays for the two recursive calls, which costs `O(n²)` on a chain-shaped tree. Two changes make it linear: a map from value to inorder index finds the root in `O(1)`, and each call receives the bounds `lo..hi` of its inorder range instead of copied slices.

The preorder side needs no bounds at all. `Build` creates a root, then finishes the entire left subtree, then the right one, so it asks for roots in exactly the order preorder lists them: root, left block, right block. One index moving left to right through preorder, kept in a one-element box that every call shares, hands each call its root. The left call consumes exactly the `mid - lo` values of the left block and stops, leaving the index on the first value of the right block, which is why the left subtree must be built first.

```text
preorder   3 │ 9 │ 20 15 7        root │ left block │ right block
inorder    9 │ 3 │ 15 20 7        left block │ root │ right block
position   {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}

call          pre_index   root   mid   left range    right range
Build(0, 4)       0         3     1    0..0          2..4
Build(0, 0)       1         9     0    0..-1 empty   1..0 empty
Build(2, 4)       2        20     3    2..2          4..4
Build(2, 2)       3        15     2    2..1 empty    3..2 empty
Build(4, 4)       4         7     4    4..3 empty    5..4 empty

      3           level order: [3, 9, 20, null, null, 15, 7]
     / \
    9   20
       /  \
      15   7
```

```pseudo
FUNCTION ConstructTree(preorder, inorder)
    position ← empty map                   // value → index in inorder
    FOR i FROM 0 TO len(inorder) - 1
        position[inorder[i]] ← i
    pre_index ← [0]                        // one box every call shares
    RETURN Build(preorder, position, pre_index, 0, len(inorder) - 1)

FUNCTION Build(preorder, position, pre_index, lo, hi)
    IF lo > hi
        RETURN null                        // empty range: no subtree here
    value ← preorder[pre_index[0]]         // roots come in preorder
    pre_index[0] ← pre_index[0] + 1
    root ← new TreeNode(value)
    mid ← position[value]                  // the root splits inorder[lo..hi]
    root.left ← Build(preorder, position, pre_index, lo, mid - 1)
    root.right ← Build(preorder, position, pre_index, mid + 1, hi)
    RETURN root
```

Every node is created once after an `O(1)` lookup, so the build runs in `O(n)` time, with `O(n)` space for the map and recursion as deep as the tree is tall; a chain of more than about a thousand nodes passes Python's default recursion limit. Reach for this whenever two traversals must become a tree again. Inorder with postorder is the mirror image: walk postorder from its end, where the root sits, and build the right subtree before the left. Preorder with postorder fixes the tree only when no node has a single child, since a lone child could hang on either side. A binary search tree needs its preorder alone, because its inorder is the sorted order, and null markers make a single preorder enough for any tree (#36). The classic mistake is building the right subtree first: the right range `2..4` then receives `9`, the root of the left block, and from there every range is wrong until the build reads past the end of preorder.

*Practice:* LC 105 Construct Binary Tree from Preorder and Inorder Traversal · LC 106 Construct Binary Tree from Inorder and Postorder Traversal · LC 889 Construct Binary Tree from Preorder and Postorder Traversal · LC 1008 Construct Binary Search Tree from Preorder Traversal
