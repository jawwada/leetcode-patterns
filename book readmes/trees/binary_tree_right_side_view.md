# Binary Tree Right Side View

*LeetCode 199 · Medium · Pattern: DFS with depth (first-visit per level) · Reading time ~8 min*

## The problem

Standing to the right of a binary tree, return the values visible from top to bottom: the rightmost node of every
level.

```text
Example: [1,2,3,null,5,null,4] -> [1,3,4]; [1,null,3] -> [1,3].
```

## What the problem is really asking

Stand to the right of the tree and look left. On each row you see exactly one node, the one furthest to the right on that row; everything else on the row is hidden behind it. Return those visible values from top to bottom. The answer is a list with one value per level, so its length is the height of the tree.

```text
 tree [1,2,3,4,5]                       eye
                                         |
   depth 0          1        ---------> 1
                  /   \
   depth 1       2     3     ---------> 3
                / \
   depth 2     4   5         ---------> 5

 answer: [1, 3, 5]
```

The trap is in depth 2. The tempting answer is "walk down the right edge: 1, 3, stop", which returns `[1, 3]`. But 3 has no children, and row 2 still exists, made of nodes hanging under the left child 2. From the right you see 5 there, because nothing on row 2 stands to its right. The rightmost node of a row can come from anywhere in the tree, not only from the right spine. That is what makes it a level question and not a path question.

## Do it by hand first

By hand you would do what you did in the last problem: read the tree row by row, left to right, and keep the last node of each row.

```text
 row      nodes, left to right    last
 0        1                       1
 1        2, 3                    3
 2        4, 5                    5
```

Or, more lazily, you would read each row from the right and just take the first node you meet. Either way your hand kept, for each depth, "have I already picked this row's node?" Once a row had its answer you ignored the rest of it. That per-depth "already claimed" mark is the seed.

## The first honest attempt

You already own a tool that produces rows: the level-order BFS with a size snapshot. The plainest use of it builds every row as a full list, the whole `[[1],[2,3],[4,5]]`, then keeps the last element of each. That stores all n values to use h of them.

A tighter BFS keeps nothing but the last node popped in each round. Here is the queue, front on the left:

```text
 round  size  pops (queue after each pop)     last popped
 0      1     1 -> [2 | 3]                   1
 1      2     2 -> [3 | 4 | 5]
              3 -> [4 | 5]                   3
 2      2     4 -> [5]
              5 -> [ ]                       5
                                   view = [1, 3, 5]
```

This is correct and O(n) time. Its cost is space: the queue holds a whole row, O(w), which is about n/2 on the bottom row of a complete tree. Every node of every row passes through the queue even though only one per row matters. On a wide tree, that is a lot of memory spent on nodes whose only job is to be hidden.

## The turning point

**Claim: in a depth-first walk that visits the right child before the left child, the first node reached at each depth is the rightmost node of that depth.**

Why? Take any depth d and two nodes on it, A to the right of B. Follow both paths up until they meet at their lowest common ancestor X. Below X, A is in X's right subtree and B in X's left subtree (that is what "A is to the right of B" means in a tree drawing). A right-first walk finishes X's entire right subtree before it enters X's left subtree. So A is visited before B. This holds for every pair, so the rightmost node at depth d beats all others on that row.

```text
            X                  right-first order at X:
          /   \                  1) all of right subtree
         .     .                 2) then all of left subtree
        /       \
       B  ...    A    depth d    A is reached first
```

So we do not need the whole row. We need a way to recognise "this is the first node I have reached at this depth". The answer list itself gives it for free: if the walk is at depth d and `len(view) == d`, then depths 0 to d-1 are claimed and depth d is not. Record the value. If `len(view) > d`, someone to the right already claimed this row; do nothing, but keep walking, because deeper rows might still be unclaimed.

```text
 if depth == len(view): view.append(node.val)
 dfs(node.right, depth + 1)
 dfs(node.left,  depth + 1)
```

That last point is the fix for the trap. When the walk has finished 3's (empty) subtree and comes back into 2, depth 1 is already claimed, so 2 is skipped. But the walk continues into 2's children at depth 2, which no one has claimed, and 5 becomes the visible node. The DFS hugs the right edge first, then back-fills the rows the right edge did not reach.

Notice the state flowing down: `depth` is passed as a parameter, exactly like `path_max` in Count Good Nodes. It is an integer per call, so siblings cannot corrupt it. The shared state is `view`, which only ever grows.

## Watch it work

Tree `[1,2,3,4,5]`. Each frame shows the node being visited `*`, its depth, `len(view)` before the check, the decision, the call stack, and `view`.

**Frame 1.** Visit 1 at depth 0.

```text
          *1*  d=0           len(view)=0 -> claim
          /  \               stack: 1
         2    3              view = [1]
        / \
       4   5
```

**Frame 2.** Right first: visit 3 at depth 1.

```text
           1                 len(view)=1 -> claim
          /  \               stack: 1, 3
         2   *3*  d=1        view = [1, 3]
        / \
       4   5
```

3 has no children, so its call returns.

**Frame 3.** Back to 1, now its left child: visit 2 at depth 1.

```text
           1                 len(view)=2 > 1 -> skip
          /  \               stack: 1, 2
        *2*   3   d=1        view = [1, 3]
        / \
       4   5
```

Row 1 already belongs to 3. The walk does not stop here; it continues into 2's children.

**Frame 4.** Right first: visit 5 at depth 2.

```text
           1                 len(view)=2 -> claim
          /  \               stack: 1, 2, 5
         2    3              view = [1, 3, 5]
        / \
       4  *5*  d=2
```

The back-fill: row 2 is claimed by a node under the left child.

**Frame 5.** Visit 4 at depth 2.

```text
           1                 len(view)=3 > 2 -> skip
          /  \               stack: 1, 2, 4
         2    3              view = [1, 3, 5]
        / \
      *4*  5   d=2
```

Every node visited; the answer is `[1, 3, 5]`.

Across the frames, `len(view)` always equalled the number of depths already claimed, and each claim was made by the first node reached at that depth, which right-first order guarantees is the rightmost.

## Why it is correct

Invariant: whenever `dfs(node, d)` is entered, `view` holds, for every depth less than `len(view)`, the rightmost node of that depth, and no node at depth `len(view)` or deeper has been visited yet. Preorder reaches depth d only by passing through every depth above it, so when the first node at depth d appears, `len(view)` is exactly d; it is appended. By the turning-point argument, that first node is the rightmost at depth d. Later nodes at depth d see `len(view) > d` and are skipped. Every node is visited, so every non-empty depth gets claimed once.

## Cost

- Time O(n) for both the DFS and the BFS versions: every node is visited once.
- Space: DFS uses O(h) for the recursion stack plus h answers. BFS uses O(w) for the queue. For a complete tree that is O(log n) against O(n); for a long chain it flips, O(n) stack against O(1) queue width.

## Variations you will meet

- **Left side view.** Swap the two recursive calls (left first), or take the first node of each BFS round instead of the last.
- **BFS keeping the last of each round.** The version from the first attempt. Perfectly acceptable in an interview; mention the O(w) versus O(h) trade-off and you have shown both views.
- **Largest value in each row** (LeetCode 515). Here every node on a row matters, so "first to arrive" is not enough. With DFS, compare instead of append when `depth < len(view)`; with BFS, keep a running max per round.
- **Bottom view or top view.** These group by horizontal column instead of depth and need (column, depth) bookkeeping, the idea behind Vertical Order Traversal later in this chapter.

## What to carry forward

Right-first DFS with a depth parameter, and `depth == len(answer)` as the test for "first time on this row". Cousins in Binary Tree next also cares about depth, but it compares two specific nodes: same depth, different parents, so the walk must carry the parent down along with the depth.
