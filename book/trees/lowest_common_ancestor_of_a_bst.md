# Lowest Common Ancestor of a Binary Search Tree

*LeetCode 235 · Medium · Pattern: BST ordered descent · Reading time ~7 min*

## What the problem is really asking

You get a BST and two of its nodes, `p` and `q`. Return their **lowest common ancestor** (LCA): the deepest node that has both `p` and `q` in its subtree. A node counts as being in its own subtree, so if `p` is an ancestor of `q`, the answer is `p` itself.

The answer is a node. Geometrically it is the place where the two root-to-target paths **split**: above it, the paths to `p` and `q` are the same; below it, they go different ways.

Running example: `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 3`, `q = 5`.

```text
               6
            /     \
           2       8
          / \     / \
         0   4   7   9
            / \
           3   5
           p   q

 path to 3:  6 -> 2 -> 4 -> 3
 path to 5:  6 -> 2 -> 4 -> 5
                       ^ last shared node = LCA = 4
```

## Do it by hand first

Trace both paths with two fingers starting at the root. At 6, both targets are smaller, so both fingers go left. At 2, both targets are larger, so both go right. At 4, 3 goes left and 5 goes right: the fingers part. 4 is the answer.

```text
 node   3 vs node   5 vs node   fingers
  6       <           <         both left
  2       >           >         both right
  4       <           >         SPLIT -> answer 4
```

Notice what your hand compared: not the nodes in the tree, only the two target **values** against the current node. In a BST that comparison alone tells you which way a target lies. You never needed to search.

## The first honest attempt

Record the path from the root to `p` and the path to `q` as two lists (each found by a BST descent), then walk the lists in parallel and return the last node they share.

```text
 path_p: [6, 2, 4, 3]
 path_q: [6, 2, 4, 5]
          =  =  =  x
          shared prefix walked twice and stored twice;
          only the point where they differ mattered
```

This is `O(h)` time and `O(h)` space, which is already good. The waste is smaller than in most chapters: the shared prefix is walked twice, and two whole lists are stored just to find the first place they differ. But if we can tell *at each node* whether the paths are about to split, we can walk the prefix once and store nothing.

## The turning point

**Claim: walking down from the root, the LCA is the first node whose value lies between `p.val` and `q.val`, inclusive.**

Let `lo = min(p.val, q.val)` and `hi = max(p.val, q.val)`. At any node on the shared prefix, there are three cases:

- `hi < node.val`: both targets are smaller, so both are in the left subtree. Both paths continue left; this node is a common ancestor but not the lowest.
- `lo > node.val`: both are in the right subtree. Go right.
- Otherwise `lo <= node.val <= hi`. Either the targets are on opposite sides (`lo < node.val < hi`), so the paths split here, or one of them *is* this node (`node.val == lo` or `== hi`), so the other is below it. In both cases this node is the LCA.

On a number line, every BST node cuts its range into "less than me" (left) and "greater than me" (right). We walk down while the whole interval `[lo, hi]` sits on one side of the cut. The first node that falls *inside* the interval cuts it, and that node is the answer.

```text
 number line:   0   2   3   4   5   6   7   8   9
 [lo, hi]:              [=======]
 cut at 6:                          |   interval left of 6
 cut at 2:          |                   interval right of 2
 cut at 4:                  |           inside -> LCA
```

The inequalities must be inclusive. With strict ones, `p = 2, q = 4` would fail: at node 2, `lo = 2` is not `> 2` and `hi = 4` is not `< 2`, so the "otherwise" case correctly returns 2. That is exactly the "a node is its own ancestor" rule.

The invariant that makes this a loop with `O(1)` state: **the current node is always a common ancestor of `p` and `q`**. It holds at the root, and each left or right step is taken only when both targets lie on that side.

## Watch it work

Tree as drawn above, `p = 3`, `q = 5`, so `lo = 3`, `hi = 5`.

Frame 1. Start at the root.

```text
 node = 6        [lo, hi] = [3, 5]
 hi 5 < 6  -> both in left subtree -> go left
 path so far: 6
```

Frame 2. At 2.

```text
 node = 2
 hi 5 < 2 ? no      lo 3 > 2 ? yes -> go right
 path so far: 6 -> 2
```

Frame 3. At 4.

```text
 node = 4
 hi 5 < 4 ? no      lo 3 > 4 ? no
 -> 3 <= 4 <= 5: return node 4
 path so far: 6 -> 2 -> 4      (3 and 5 never visited)
```

Frame 4. Same tree, `p = 2`, `q = 4`: the inclusive case.

```text
 [lo, hi] = [2, 4]
 node 6: hi 4 < 6 -> left
 node 2: 4 < 2 ? no   2 > 2 ? no  -> return node 2
          (p itself; q = 4 is in its right subtree)
```

In every frame the current node was an ancestor of both targets, and the walk only ever moved down one path.

## Why it is correct

Invariant: `node` is a common ancestor of `p` and `q`. At the root it is trivially true. If `hi < node.val`, the BST rule puts both targets in the left subtree, so the left child is still a common ancestor; symmetrically on the right. The loop ends at the first node with `lo <= node.val <= hi`. If `lo < node.val < hi`, the targets are in different subtrees, so no child of `node` contains both, and `node` is the lowest. If `node.val` equals `lo` or `hi`, then `node` is one of the targets (values are unique), and no proper descendant of a node can be an ancestor of that node, so again `node` is the lowest. The loop always ends because each step goes one level down and both targets exist.

## Cost

- Time `O(h)`: one root-to-LCA path. `h` is `log n` for a balanced tree, `n` for a skewed one.
- Space `O(1)`: one pointer and two numbers. A recursive version is `O(h)` stack for no benefit.

## Variations you will meet

- **LCA in a plain binary tree** (the next problem). Values no longer say which side a target is on, so you must search both sides and let the subtrees report back.
- **Targets that may be missing.** The loop happily returns any node whose value falls in `[lo, hi]`, even if `p` or `q` is absent. If presence is not guaranteed, search for both values from the returned node before trusting it.
- **Distance between two nodes in a BST.** Find the LCA with this descent, then add the depths of `p` and `q` measured from it.
- **Many queries on a static tree.** Binary lifting or an Euler tour with a range-minimum structure answers each LCA query in `O(log n)` or `O(1)`, for any tree.

## What to carry forward

In a BST the LCA is where the interval `[lo, hi]` stops sitting on one side: walk down until the node's value falls inside it, inclusive. The next problem removes the ordering, so instead of steering by values, each subtree must report upward what it found.
