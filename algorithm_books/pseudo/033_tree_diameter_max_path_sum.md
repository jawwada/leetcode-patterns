---
rank: 33
slug: tree_diameter_max_path_sum
---

The diameter of a binary tree is the number of edges on its longest path between two nodes, and the maximum path sum is the largest total of node values along any path of at least one node. In `[1, 2, 3, 4, 5]` the diameter is `3`, along `4 → 2 → 1 → 3`; in `[-10, 9, 20, null, null, 15, 7]` the best sum is `42`, along `15 → 20 → 7`.

The brute force takes every pair of endpoints and walks the path between them: `O(n²)` pairs at up to `O(n)` steps each, cubic time in all. The insight is that every path has exactly one highest node, where it bends: it climbs up one arm and comes down the other. So skip the endpoints and ask each node a single question, "what is the best path that bends here?", and answer it from two numbers its children already know, the best downward arm on each side. That makes the recursion postorder, children before parent, and gives it two jobs. It returns the best single arm upward, because a parent can extend only one arm. It writes the bent path, left arm plus right arm, into a shared `best`, because a path that bends here is finished and no ancestor can use it.

For the diameter the arm is a height: `Height(node)` counts the nodes on the longest downward path, so an empty subtree has height `0` and the path bending at a node has exactly `left + right` edges. For the path sum the arm is a gain, the node's value plus its better child gain, and a gain below zero is clipped to `0`: do not take that arm at all. Negatives are also why `best` starts at `root.val` instead of `0`: a path holds at least one node, so when every value is negative the answer is the largest single value.

```text
      1          node  left  right  left + right  best  returns
     / \           4     0     0         0          0      1
    2   3          5     0     0         0          0      1
   / \             2     1     1         2          2      2
  4   5            3     0     0         0          2      1
                   1     2     1         3          3      3    diameter 3

    -10          node  left  right  val + left + right  best  returns
    /  \           9     0     0            9             9      9
   9    20        15     0     0           15            15     15
       /  \        7     0     0            7            15      7
      15   7      20    15     7           42            42     35
                 -10     9    35           34            42     25    sum 42
```

```pseudo
FUNCTION Diameter(root)
    best ← [0]                             // a box every call can update
    Height(root, best)
    RETURN best[0]

FUNCTION Height(node, best)
    IF node = null
        RETURN 0
    left ← Height(node.left, best)
    right ← Height(node.right, best)
    best[0] ← max(best[0], left + right)   // the path that bends at node
    RETURN 1 + max(left, right)            // only one arm continues upward

FUNCTION MaxPathSum(root)
    best ← [root.val]                      // one node alone is a path
    Gain(root, best)
    RETURN best[0]

FUNCTION Gain(node, best)
    IF node = null
        RETURN 0
    left ← max(Gain(node.left, best), 0)   // a negative arm is cut off
    right ← max(Gain(node.right, best), 0)
    best[0] ← max(best[0], node.val + left + right)
    RETURN node.val + max(left, right)
```

Each node is visited once with constant work, so both run in `O(n)` time and `O(h)` space for the recursion stack, where `h` is the tree's height, `O(n)` on a chain. Recognize the pattern when the answer is a path that may lie anywhere in the tree: return what a parent can extend, record what only this node can complete. The same skeleton checks balance by returning the height or `-1` once a subtree is lopsided, and finds the longest univalue path by letting an arm continue only into a child with the same value. The classic mistake is passing the bent path upward, `1 + left + right` instead of `1 + max(left, right)`: the parent then extends something that is no longer a path, and `[1, 2, 3, 4, 5]` reports a diameter of `4`.

*Practice:* LC 543 Diameter of Binary Tree · LC 124 Binary Tree Maximum Path Sum · LC 110 Balanced Binary Tree · LC 687 Longest Univalue Path
