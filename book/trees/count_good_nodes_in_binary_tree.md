# Count Good Nodes in Binary Tree

*LeetCode 1448 · Medium · Pattern: DFS carrying path state · Reading time ~7 min*

## The problem

A node is good if no node on the path from the root to it has a value greater than it (the root is always good). Count
the good nodes.

```text
Example: [3,1,4,3,null,1,5] -> 4 (the root 3, the 4, the 5, and
  the deeper 3).
```

## What the problem is really asking

Walk from the root down to some node X. If nothing you stepped on along the way is strictly bigger than X, then X is "good". Count how many nodes are good. The root is always good, since the path to it contains only itself. The answer is one integer between 1 and n.

```text
 tree [3,1,4,3,null,1,5]

            3          path to each node   max above   good?
          /   \        3                    -          yes
         1     4       3,1                  3          no
        /     / \      3,1,3                3          yes (tie)
       3     1   5     3,4                  3          yes
                       3,4,1                4          no
                       3,4,5                4          yes
                                            answer = 4
```

Two details hide in the definition. First, it is about the path from the root, not about the whole tree: the 3 at the bottom left is good even though 4 exists elsewhere, because 4 is not on its path. Second, "no node is greater" means ties are fine: the deeper 3 sits below another 3 and is still good.

## Do it by hand first

By hand you would trace each path and keep a running "highest so far" in your head, the way a hiker tracks the highest altitude reached on a trail:

```text
 trail    3  1  3      3  4  1      3  4  5
 record   3  3  3      3  4  4      3  4  5
 good?    Y  n  Y      Y  Y  n      Y  Y  Y
```

You never looked back along the trail to recompute the record; you updated it when you passed a new high. And when you started the second trail, you did not erase the record back to zero; you went back to the record at the fork, which was 3. Your hand kept exactly one number per position on the path: the highest value above it.

## The first honest attempt

The direct translation of the definition: walk the tree carrying the whole root-to-node path as a list, and at each node compare its value against `max(path)`.

```text
 node   path            max(path) scans
 3      [3]             3
 1      [3,1]           3, 1
 3      [3,1,3]         3, 1, 3        <- rescans 3, 1
 4      [3,4]           3, 4           <- rescans 3
 1      [3,4,1]         3, 4, 1        <- rescans 3, 4
 5      [3,4,5]         3, 4, 5        <- rescans 3, 4
```

Each `max(path)` costs O(depth), and building `path + [val]` at every node costs O(depth) too, so the total is O(n·h), quadratic on a chain. The repeated work is in the scans: the maximum of `[3,4]` was already known at node 4, yet each child of 4 scans `3, 4` again from scratch.

## The turning point

**Claim: the decision at a node needs only one number about its path, the maximum so far, and that number updates in O(1): `max(path + [v]) = max(max(path), v)`.**

Maximum is a running quantity, like a sum. You can compute it one step at a time without ever looking at the whole list again. So instead of carrying the path down, carry its maximum:

```text
 dfs(node, path_max):
   good     = 1 if node.val >= path_max else 0
   path_max = max(path_max, node.val)
   return good + dfs(left, path_max) + dfs(right, path_max)
```

Read the order carefully. Compare first, update second. If you update before comparing, every node compares against a maximum that already includes itself, and `node.val >= max(..., node.val)` is always true. And the comparison is `>=`, because ties count as good.

Two points about how the state flows, compared with the last problem:

1. **No undo is needed.** In Path Sum II there was one shared list, and every call had to pop what it pushed so the sibling saw the right prefix. Here `path_max` is a plain integer passed by value. When node 4 hands `path_max = 4` to its children, node 3's local `path_max` (still 3) is unaffected. Each call has its own copy, so returning restores the old value automatically.
2. **The answer flows back up as a count.** Each call returns "number of good nodes in my subtree". That is the "state down, totals up" shape from Sum of Left Leaves, just with a richer piece of state.

Start the root with `path_max = root.val` (or negative infinity); either way the root compares equal or greater and counts as good.

## Watch it work

Tree `[3,1,4,3,null,1,5]`. `in` is the `path_max` a call receives; `out` is what it passes to its children. `G` marks good nodes, `x` not good.

**Frame 1.** Root.

```text
         [3]G  in=3 out=3       count so far 1
         /   \
        1     4
       /     / \
      3     1   5
```

3 >= 3, good; the maximum stays 3.

**Frame 2.** Left child 1.

```text
          3G                    stack: 3(in 3)
         /                             1(in 3)
       [1]x  in=3 out=3         count so far 1
       /
      3
```

1 < 3, not good. It passes 3 down unchanged.

**Frame 3.** The deeper 3.

```text
          3G                    stack: 3(in 3)
         /                             1(in 3)
        1x                             3(in 3)
       /
     [3]G  in=3 out=3           count so far 2
```

3 >= 3: a tie, so good. Left subtree of the root returns 0 + 1 = 1.

**Frame 4.** Right child 4, with the root's own `path_max` of 3.

```text
          3G                    stack: 3(in 3)
            \                          4(in 3)
            [4]G  in=3 out=4    count so far 3
            / \
           1   5
```

The 3 inside node 1's call never leaked here: node 4 got a fresh 3 from the root. 4 >= 3, good, and it raises the maximum to 4.

**Frame 5.** Children of 4.

```text
            4G  out=4
           /  \
        [1]x  [5]G              1: in=4, 1 < 4
                                5: in=4, 5 >= 4
                                count so far 4
```

Right subtree returns 1 + 0 + 1 = 2; root returns 1 + 1 + 2 = 4.

Across the frames, the number a call received was always the largest value strictly above it on its own root path, never contaminated by a sibling's branch.

## Why it is correct

Invariant: `path_max` passed into `dfs(node)` equals the maximum value over the nodes strictly above `node` on its root path (for the root, its own value, which does not change the verdict). It holds at the root, and each child receives `max(path_max, node.val)`, which is exactly the maximum over the path extended by `node`. Given the invariant, `node.val >= path_max` is precisely the definition of good. Every node is visited exactly once, so summing the 0 or 1 verdicts over all calls counts the good nodes exactly.

## Cost

- Time O(n): one visit per node, O(1) work each, versus O(n·h) for rescanning the path.
- Space O(h): the recursion stack. No path list is stored.

## Variations you will meet

- **Iterative BFS or DFS.** Put `(node, path_max)` pairs into a queue or stack. The state still rides with the node; BFS works because the verdict depends only on the node's own root path, not on visit order.
- **Maximum Difference Between Node and Ancestor** (LeetCode 1026). Carry both the running minimum and maximum down; at each node the best difference is against one of them.
- **Validate Binary Search Tree** (later in this chapter). Carry an allowed `(low, high)` interval down instead of one maximum; a node is valid if it fits, and it narrows the interval for each child differently.
- **Pseudo-Palindromic Paths** (LeetCode 1457). Carry a bitmask of digit parities; at a leaf, check that at most one bit is set.

## What to carry forward

If the condition at a node depends on a summary of its root path, and that summary updates in O(1) per step (sum, max, min, parity), pass the summary down as an integer and you never need undo. Binary Tree Maximum Path Sum next reverses the flow: the useful number travels *up* from the children, and the answer is recorded on the side at every node.
