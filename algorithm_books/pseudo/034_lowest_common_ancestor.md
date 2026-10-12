---
rank: 34
slug: lowest_common_ancestor
---

Given a binary tree and two of its nodes `p` and `q`, both present, return their lowest common ancestor: the deepest node that has both of them in its subtree, where a node counts as an ancestor of itself. In `[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4]` the LCA of `7` and `8` is the root `3`, the LCA of `6` and `4` is `5`, and the LCA of `5` and `4` is `5` itself.

One way is to record the path from the root to `p` and the path to `q` and keep the last node they share, which costs two searches and two stored paths. The postorder search does it in a single pass by letting every subtree send up one report: `null` if it holds neither target, the target itself if it holds one, and the meeting point once it holds both. A call that lands on `p` or `q` returns at once without looking below, and that is safe: if the other target sits underneath, this node is the answer anyway, and if it does not, the other target lives elsewhere and an ancestor will collect both reports. The first node that hears a report from its left subtree and another from its right is where the two root paths split, so it is the lowest common ancestor. From there up, every ancestor hears from one side only and simply forwards it.

Picture two flares fired from `p` and `q`. Each climbs toward the root through its ancestors, and the first node lit from both sides is the answer; it swallows both flares and sends up a single one, itself.

```text
              3                 node   left   right   returns
            /   \                 6    null   null    null
          5       1               7    is p, stops    7
         / \     / \              4    null   null    null
        6   2   0   8             2    7      null    7
           / \                    5    null   7       7
          7   4                   0    null   null    null
                                  8    is q, stops    8
     p = 7, q = 8                 1    null   8       8
                                  3    7      8       3   both sides: the LCA
```

```pseudo
FUNCTION LowestCommonAncestor(root, p, q)
    IF root = null OR root = p OR root = q
        RETURN root                    // nothing here, or a target itself
    left ← LowestCommonAncestor(root.left, p, q)
    right ← LowestCommonAncestor(root.right, p, q)
    IF left ≠ null AND right ≠ null
        RETURN root                    // one target on each side: the LCA
    IF left ≠ null
        RETURN left                    // pass the single report upward
    RETURN right
```

Every node is visited at most once, so the search costs `O(n)` time and `O(h)` space for the recursion. Reach for it whenever a question involves two nodes and where their paths to the root meet; the distance between two nodes, for instance, is `depth(p) + depth(q) - 2 * depth(lca)`. In a binary search tree the values do the steering: walk down from the root, going left while both values are smaller and right while both are larger, and the first node that separates them, or equals one of them, is the LCA, in `O(h)`. With parent pointers it turns into the intersection of two linked lists: climb from both nodes, restart each pointer at the other node when it passes the root, and the two meet at the LCA after equal distances. The classic mistake is forgetting the promise that both nodes exist: when only `p` is in the tree, the search still returns `p`, so a version without that promise must confirm that both targets were seen.

*Practice:* LC 236 Lowest Common Ancestor of a Binary Tree · LC 235 Lowest Common Ancestor of a Binary Search Tree · LC 1650 Lowest Common Ancestor of a Binary Tree III
