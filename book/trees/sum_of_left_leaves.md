# Sum of Left Leaves

*LeetCode 404 · Easy · Pattern: DFS carrying path state · Reading time ~6 min*

## What the problem is really asking

Add up the values of the nodes that satisfy two conditions at once: the node has no children (it is a leaf), and it hangs off its parent's left pointer (it is a left child). The answer is a single integer. A tree that is only a root has no left leaves, because the root has no parent at all.

```text
 tree [1,2,3,4,5,6]

            1
          /   \
         2     3
        / \   /
       4   5 6

 leaves: 4, 5, 6
 left children: 2, 4, 6
 both: 4 and 6       answer = 4 + 6 = 10
```

The catch: the two conditions live in different places. "Leaf" is a fact about the node (both child pointers are empty). "Left" is not; nothing inside node 6 says it is a left child. Only its parent knows.

## Do it by hand first

With a pencil, most people walk the tree from the top and label every edge with the direction it goes:

```text
            1
         L/   \R
         2     3
      L/  \R  L/
      4    5  6

 dead ends (leaves) and the label of the edge into them:
   4  <- L    count it
   5  <- R    skip
   6  <- L    count it
```

Your hand tracked one thing: which way it just turned. That single bit, "did I arrive by going left?", is the whole state of the algorithm.

Node 2 is a left child but not a leaf; node 5 is a leaf but arrived by a right edge. Neither counts.

## The first honest attempt

A natural first plan: collect all leaves, then for each leaf find its parent and check whether `parent.left is leaf`. The tree has no parent pointers, so "find its parent" means searching the whole tree from the root again.

```text
 leaf 4: scan 1, 2  -> parent is 2, 2.left is 4   count
 leaf 5: scan 1, 2  -> parent is 2, 2.left is 4   skip
 leaf 6: scan 1, 2, 4, 5, 3 -> parent is 3         count
         ^^^^^^^^^^^^^^^^^
         the same top of the tree walked again per leaf
```

Each search is O(n), there can be about n/2 leaves, so this is O(n^2). The waste is plain: when the first traversal reached leaf 6, it got there *from* node 3 by following `3.left`. It knew the parent and the direction at that exact moment and threw the knowledge away.

## The turning point

**Claim: whether a node is a left child is decided by the edge you just crossed, so a depth-first walk can pass it down as one boolean parameter instead of ever looking it up.**

This is the first problem in the chapter where information flows *down* the recursion. Maximum Depth and Diameter only returned values up to the parent. Here the parent tells the child something: "you are my left one."

The mechanism is a parameter. Define `dfs(node, is_left)`:

- If `node` is empty, it contributes 0.
- If `node` is a leaf, it contributes `node.val` when `is_left` is true, else 0.
- Otherwise it contributes `dfs(node.left, True) + dfs(node.right, False)`.

Calling the root with `is_left = False` handles the single-node case with no special code. The shape is "state going down, totals coming up", the template for the next several problems.

```text
 what each call receives (down) and returns (up)

        dfs(1,F)            -> 4 + 6 = 10
        /       \
   dfs(2,T)    dfs(3,F)     -> 4      -> 6
    /    \       /
 dfs(4,T) dfs(5,F) dfs(6,T) -> 4   0   6
```

## Watch it work

Example `[1,2,3,4,5,6]`. Each frame shows the call stack (top is the current call) and the running total.

**Frame 1.** Start at the root with `is_left = False`.

```text
          *1*
          /  \             stack: dfs(1,F)
         2    3
        / \  /
       4  5 6
```

Node 1 has children, so it is not a leaf; it calls its left child with True.

**Frame 2.** Node 2, arrived by a left edge.

```text
           1
         /   \             stack: dfs(1,F)
       *2*    3                   dfs(2,T)
       / \   /
      4   5 6
```

`is_left` is True but 2 has children, so nothing is counted here.

**Frame 3.** Leaf 4 with True returns 4; leaf 5 with False returns 0.

```text
           1
         /   \             stack: dfs(1,F)
        2     3                   dfs(2,T) = 4 + 0
       / \   /
     [4] (5) 6             [ ] counted   ( ) skipped
```

Node 2 returns 4 to node 1.

**Frame 4.** Node 3 with False, then its left child 6 with True.

```text
           1
         /   \             stack: dfs(1,F)
        2     3                   dfs(3,F) = 6 + 0
       / \   /
     [4] (5)[6]            right child of 3 is None -> 0
```

Leaf 6 returns 6; node 3 returns 6.

**Frame 5.** Back at the root with both answers.

```text
          *1*  = 4 + 6 = 10     stack: dfs(1,F)
         /   \
     (2)=4  (3)=6
```

The root adds both sides and returns 10.

Across the frames, every call knew one extra bit, always correct for the edge just crossed. No call ever looked upward.

## Why it is correct

Invariant: when `dfs(node, is_left)` is called, `is_left` is true exactly when `node` is the left child of its parent. That holds for the root (False, it has no parent) and is preserved by every step, because the only places a call is made are `dfs(node.left, True)` and `dfs(node.right, False)`. Given that, a leaf adds its value exactly when it is a left leaf, and non-leaves add nothing of their own. The return value of a call is therefore the sum of left leaves inside that subtree, and the root's call covers the whole tree. Each leaf is reached by exactly one path, so none is counted twice.

## Cost

- Time O(n): each node is entered once and does constant work.
- Space O(h): the recursion stack holds one frame per level of the current path; h is n for a chain and log n for a balanced tree.

## Variations you will meet

- **Sum of right leaves.** Flip which call gets True. The structure is identical; only the edge label changes.
- **Iterative version.** Push `(node, is_left)` pairs on a stack or queue; the state rides next to the node.
- **Deepest leaves sum** (LeetCode 1302). The state carried down is depth instead of direction, and you keep the sum for the largest depth seen.
- **Check from the parent instead.** Test `node.left` for leaf-ness while standing on `node`. Same idea: whoever knows the direction decides.

## What to carry forward

When a property depends on how you got to a node, not on the node itself, pass it down as a parameter. Path Sum next carries a number down instead of a boolean, a running remainder of a target, and checks it at the leaves.
