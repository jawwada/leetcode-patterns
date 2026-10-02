# Validate Binary Search Tree

*LeetCode 98 · Medium · Pattern: DFS with (low, high) bounds · Reading time ~8 min*

## What the problem is really asking

A binary search tree (BST) promises one thing: for every node, **all** values in its left subtree are strictly smaller than it, and **all** values in its right subtree are strictly larger. Given a binary tree, return whether it keeps that promise.

The answer is a boolean. The word that makes it hard is *all*. It is not enough that each child is on the correct side of its parent; every descendant must be on the correct side of every ancestor.

Running example, the classic trap: `[5,4,6,null,null,3,7]`.

```text
          5
        /   \
       4     6
            / \
           3   7
           ^
  3 < 6, fine for its parent
  but 3 is in 5's RIGHT subtree, so it must be > 5. Invalid.
```

Every parent-child pair looks correct: 4 < 5, 6 > 5, 3 < 6, 7 > 6. The tree is still not a BST.

## Do it by hand first

Put your finger on 3 and ask: "which ancestors constrain me, and how?" Walk from the root:

```text
 at 5, I turned RIGHT  -> I must be > 5
 at 6, I turned LEFT   -> I must be < 6
 so 3 must live in the open interval (5, 6)
       number line:   ...  4    5 ( . . . ) 6    7 ...
                                 ^ allowed ^
       3 is outside -> invalid
```

Your hand did not need to remember every ancestor. For "greater than" it only needed the *largest* value you turned right at, and for "less than" the *smallest* value you turned left at. Two numbers: a window `(low, high)`. That window is the seed of the algorithm.

## The first honest attempt

Check the definition literally. At each node, collect every value in its left subtree and check they are all smaller; collect every value in its right subtree and check they are all larger. Then recurse into both children.

That is correct, and it costs `O(n²)` on a skewed tree, because a deep node is collected once by each of its ancestors:

```text
 chain 1 -> 2 -> 3 -> 4 (each a right child)

 at 1: scan {2,3,4}
 at 2: scan   {3,4}
 at 3: scan     {4}
           node 4 was scanned 3 times,
           node 3 twice: n + (n-1) + ... = O(n^2)
```

The repeated work: every ancestor re-reads the whole subtree below it. But all those comparisons for one node ask the same kind of question, "are you above this ancestor, below that one?", and their answers can be folded into two numbers.

## The turning point

**Claim: a node satisfies the BST rule with respect to every ancestor if and only if `low < node.val < high`, where `low` is the largest ancestor value at which the path turned right and `high` the smallest ancestor value at which it turned left.**

Justification. Each ancestor `a` gives one constraint on a descendant `d`: if `d` is in `a`'s left subtree then `d < a`, else `d > a`. All the "less than" constraints together are equivalent to "less than the smallest of them"; all the "greater than" constraints are equivalent to "greater than the largest of them". So the full set of ancestor constraints collapses into one open interval.

And the interval is cheap to maintain as we descend:

- Going **left** from `node`: every value below must also be `< node.val`. The new `high` is `node.val`. (It is automatically the smallest, because `node.val` already passed `< high`.)
- Going **right**: the new `low` is `node.val`.

So the interval flows *down* as two arguments, the same pattern as depth in the cousins problem. The whole check is:

```text
 valid(node, low, high):
     if node is None: return True
     if not (low < node.val < high): return False
     return valid(node.left,  low, node.val) and \
            valid(node.right, node.val, high)
```

Start with `(-inf, +inf)`. Use real infinities (or `None` for "no bound"), not a large sentinel like `2**31 - 1`: LeetCode's tests include nodes holding exactly those values. The inequalities are strict because duplicates are not allowed.

**A second view of the same fact.** In the previous problem we saw that inorder reads a tree left to right. A tree is a BST exactly when that reading is strictly increasing. For the trap tree, inorder gives `4 5 3 6 7`, and `5 > 3` is the violation. An iterative inorder that remembers the previous value and fails on `prev >= val` is an equally good solution. The window version is the one shown here; the inorder version is the one the next problem builds on.

## Watch it work

Tree `[5,4,6,null,null,3,7]`. Each frame shows the node, its window, and the recursion path.

Frame 1. The root gets the whole number line.

```text
 node 5   window (-inf, +inf)   -inf < 5 < +inf  ok
 path: 5
 children get:  4 -> (-inf, 5)    6 -> (5, +inf)
```

Frame 2. Left child 4.

```text
 node 4   window (-inf, 5)      4 < 5  ok
 path: 5 -> 4 (left)
 both children None -> True
```

The whole left subtree is valid; the `and` moves on to the right.

Frame 3. Right child 6.

```text
 node 6   window (5, +inf)      5 < 6  ok
 path: 5 -> 6 (right)
 children get:  3 -> (5, 6)    7 -> (6, +inf)
```

Going left from 6 slides the right wall in to 6; the left wall 5 stays from the root.

Frame 4. Node 3 is checked against both walls.

```text
 node 3   window (5, 6)         5 < 3 ?  NO -> False
 path: 5 -> 6 -> 3
          (5 ......... 6)
     3 is here, outside the window
```

`False` propagates up through the `and`s; node 7 is never visited.

Across frames, the window only ever shrank on the way down, and at each node it was exactly the intersection of all its ancestors' constraints.

## Why it is correct

Invariant: when `valid(node, low, high)` is called, `(low, high)` is exactly the set of values that the BST rule allows at `node`'s position, given all its ancestors. True at the root (no ancestors, whole line). If true at `node`, then for its left child the allowed set adds one constraint, `< node.val`, giving `(low, node.val)`; similarly `(node.val, high)` on the right. So it holds everywhere.

If the function returns `True`, every node was inside its window, so every node satisfies every ancestor constraint: that is the definition of a BST. If the tree is a BST, every node is inside its window, so no check fails and the function returns `True`.

## Cost

- Time `O(n)`: each node is checked once against two numbers. The `O(n²)` scanning is gone because each ancestor's constraint is applied in `O(1)` by narrowing the window.
- Space `O(h)`: the recursion depth. The iterative inorder version also uses `O(h)` for its stack.

## Variations you will meet

- **Inorder with a `prev` value.** Same `O(n)`, and it stops at the first descent. It is the natural form when the tree is huge and you want an iterative walk.
- **Duplicates allowed on one side.** If the rule were "left `<=` node `<` right", change one inequality per side. Windows handle any mix of strict and non-strict bounds.
- **Largest BST subtree (LeetCode 333).** Validating from the top cannot reuse work for every subtree. Flip the direction: each subtree returns `(is_bst, min, max, size)` upward, and the parent checks `left.max < node.val < right.min`. Same constraint, carried up instead of down.
- **Range Sum of BST (LeetCode 938).** Compare each node with a query window `[L, R]`: if `node.val < L`, its whole left subtree is too small and can be skipped; symmetrically on the right.

## What to carry forward

A BST's rule is a window that narrows on the way down, and equivalently a strictly increasing inorder line. The next problem walks that sorted line on purpose, stopping after `k` steps.
