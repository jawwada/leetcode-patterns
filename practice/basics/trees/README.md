# Trees

A binary tree is a node with a value and two optional children, `left` and `right`; every child is itself a tree. That recursive shape is the whole trick: almost every tree algorithm is "do something at this node, then do the same thing to the left subtree and to the right subtree". The only decisions are the **order** (visit before, between or after the children) and **what each call returns upward** (a height, a found node, a serialized token stream). When recursion is not allowed, an explicit stack reproduces the depth-first orders and a queue gives the level order.

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| visit every node (any traversal) | O(n) | each node is entered and left once |
| recursion depth / explicit stack size | O(h) | h = height; n for a chain, log n for a balanced tree |
| level-order queue | O(w) extra | w = widest level, up to n/2 |
| BST insert / search / delete | O(h) | one root-to-leaf path, O(log n) only if the tree is balanced |
| post-order aggregate (height, balance, LCA) | O(n) | one pass, the answer for a node is computed from its children's answers |

## The three depth-first orders

```
          1
        /   \          preorder   1 2 4 5 3 6   visit, then children        (copy / serialize a tree)
       2     3         inorder    4 2 5 1 3 6   left, visit, right          (sorted order of a BST)
      / \     \        postorder  4 5 2 6 3 1   children, then visit        (height, delete, anything bottom-up)
     4   5     6
```

The recursion is the same function three times; only the position of `visit` moves. With an explicit stack:

```
preorder                                   inorder
stack [1]        pop 1 visit, push 3 then 2  node=1 push, go left     stack [1]
stack [2, 3]     pop 2 visit, push 5 then 4  node=2 push, go left     stack [2, 1]
stack [4, 5, 3]  pop 4 visit                 node=4 push, go left     stack [4, 2, 1]
stack [5, 3]     pop 5 visit                 node=None: pop 4 visit, go right (None)
stack [3]        pop 3 visit, push 6         pop 2 visit, go right -> node=5
stack [6]        pop 6 visit                 push 5, pop 5 visit, pop 1 visit, go right -> 3 ...
```

Preorder pushes the **right** child first so the left child is on top and pops next. Inorder walks left pushing everything, pops, visits, then steps right.

## Level order

```
queue [1]        drain 1 node:  level [1]       push 2, 3
queue [2, 3]     drain 2 nodes: level [2, 3]    push 4, 5, 6
queue [4, 5, 6]  drain 3 nodes: level [4, 5, 6]
height = 3 levels
```

`for _ in range(len(q))` freezes the level size before the children are pushed; that one line is what separates "level order" from "just BFS".

## Post-order returns

The height, the balance check, the lowest common ancestor and serialization are all "ask both children, combine, hand the result up":

```
height(node)   = 1 + max(height(left), height(right)), with -1 as an "unbalanced" signal that short-circuits
lca(node)      = node if both children report a find, else whichever side found something
serialize(node)= str(node) + serialize(left) + serialize(right), with '#' standing in for None
```

## The invariants to say out loud

- Traversals: "Every node is visited exactly once; the stack holds the path from the root to where I am."
- Level order: "The queue holds exactly one level when the `for` starts; what I push during the loop is the next level."
- BST: "Everything in the left subtree is smaller, everything in the right subtree is bigger, at every node." Deleting a node with two children keeps that true by copying the inorder successor (smallest in the right subtree) into the node and deleting the successor.
- Post-order: "By the time I am at a node, both children already answered."

## Exercises

| File | Drills |
|---|---|
| `01_traversals_recursive_and_iterative.py` | the three recursive orders in one walk; preorder and inorder with an explicit stack, pushing right before left |
| `02_bfs_level_order_and_height.py` | level order with `for _ in range(len(q))`, height = number of levels |
| `03_bst_insert_search_delete.py` | descend by comparison; delete with 0/1 children by splicing, 2 children via the inorder successor |
| `04_balanced_and_depth.py` | LeetCode 110: post-order height that returns -1 to short-circuit the unbalanced case |
| `05_lowest_common_ancestor_binary_tree.py` | LeetCode 236: return the found node upward; both sides non-None marks the LCA |
| `06_serialize_and_deserialize.py` | LeetCode 297: preorder with '#' for None, decoding with one shared iterator |
