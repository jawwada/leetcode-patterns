# Path Sum

*LeetCode 112 · Easy · Pattern: DFS carrying path state · Reading time ~6 min*

## What the problem is really asking

Is there a way to walk from the root straight down to a leaf so that the values you step on add up to `targetSum`? The answer is a yes or no. The path must start at the root and must end at a leaf, a node with no children. Stopping halfway at an internal node whose running total happens to match does not count, and an empty tree has no paths at all, even when the target is 0.

```text
 root = [5,4,8,11,null,13,4,7,2,null,null,null,1]
 targetSum = 22

               5
             /   \
            4     8
           /     / \
         11    13   4
        /  \         \
       7    2         1

 root-to-leaf paths and their sums:
   5-4-11-7 = 27     5-4-11-2 = 22  <- yes
   5-8-13   = 26     5-8-4-1  = 18
```

The difficulty is resisting two shortcuts: checking at internal nodes, and pruning when the sum "gets too big" (values can be negative).

## Do it by hand first

By hand you would put a finger on the root and keep one number in your head, subtracting as you go: "need 22. Take 5, need 17. Take 4, need 13. Take 11, need 2." Leaf 7 overshoots; back up and try 2, which leaves exactly 0 at a leaf.

```text
 need 22
   5   -> need 17
   4   -> need 13
   11  -> need 2
     7 -> need -5   leaf, not 0: fail
     2 -> need 0    leaf, is 0:  found
```

The thing you kept track of was one number, "how much is still needed", and it only changed by one subtraction per step down. That is the seed: carry the remainder down, check it at leaves.

## The first honest attempt

The obvious brute force lists every root-to-leaf path as a list of values and sums each list. Recursively, each call builds `path + [node.val]` and hands the new list to both children; at each leaf the list is stored, and at the end every stored list is summed.

The repeated work shows up as shared prefixes being copied and re-added:

```text
 stored paths            prefix copied and re-summed
 [5, 4, 11, 7]           5 + 4 + 11  ...
 [5, 4, 11, 2]           5 + 4 + 11  ... again
 [5, 8, 13]              5           ... again
 [5, 8, 4, 1]            5 + 8       ... again
```

Each of up to n/2 leaves pays O(h) to copy and O(h) to sum: O(n·h) time and space. And it never stops early.

## The turning point

**Claim: a leaf needs only one number from its path, the sum so far (or equivalently the amount still needed), and that number for a child is the parent's number minus one value.**

This is Sum of Left Leaves again with a richer piece of state. There the parent passed down one bit. Here it passes down an integer, the remainder:

```text
 remaining(child) = remaining(parent) - parent.val
 in code: each call subtracts its own value first
```

So a call `hasPathSum(node, remaining)` does three things: subtract `node.val`; if `node` is a leaf, answer `remaining == 0`; otherwise ask the left subtree, and only if that fails, the right subtree. The `or` gives the early exit for free: once any leaf says yes, every call above it returns immediately without visiting the rest.

Two details carry the correctness:

1. Only leaves report a match. An internal node with remainder 0 still has to continue down, because the path is not finished.
2. An empty child returns False. That is what makes "node with one child" behave: the missing side cannot pretend to be a leaf.

## Watch it work

Same tree, target 22. The stack column lists calls with the remainder *after* subtracting that node.

**Frame 1.** Enter the root.

```text
          (5)               stack: 5 rem 17
         /   \
        4     8
```

17 still needed; 5 has children, go left.

**Frame 2.** Down the left spine to 11.

```text
          (5)               stack: 5  rem 17
         /                         4  rem 13
       (4)                         11 rem 2
       /
     (11)
     /  \
    7    2
```

Each step did one subtraction. 11 is not a leaf.

**Frame 3.** Try leaf 7.

```text
     (11) rem 2             stack: ... 11 rem 2
     /                                 7  rem -5
   [7]  rem -5  leaf, -5 != 0 -> False
```

7 returns False, so the `or` at node 11 tries the right child.

**Frame 4.** Try leaf 2.

```text
     (11) rem 2             stack: ... 11 rem 2
         \                             2  rem 0
         [2] rem 0  leaf, 0 == 0 -> True
```

The leaf reports a hit.

**Frame 5.** True bubbles up and short-circuits everything.

```text
          (5) True
         /   \
      (4)T    8   <- never visited
       /
    (11)T
```

The whole right subtree of 5 is skipped.

Throughout, each call's remainder was `22 - (sum from root to here)`, and only leaves turned it into an answer.

## Why it is correct

Invariant: inside the call for `node`, after its subtraction, `remaining` equals targetSum minus the sum of values on the root-to-`node` path. True at the root, and preserved because each child starts from its parent's value of `remaining`. A leaf therefore returns True exactly when its root-to-leaf path sums to the target. An internal node returns True exactly when one of its subtrees contains such a leaf, which by induction is what its children's calls report. So the root returns True exactly when some root-to-leaf path matches.

## Cost

- Time O(n): each node is visited at most once with O(1) work; the early exit can only make it faster.
- Space O(h): the recursion stack; no path lists are stored.

## Variations you will meet

- **Path Sum II** (next). Return every matching path, not just yes or no. Now you need the path itself, and the trick is to keep one shared list and undo changes on the way back up.
- **Path Sum III** (LeetCode 437). Paths may start and end anywhere going downward. The carried state becomes a prefix-sum count map, the same idea as subarray sum equals k, applied to the root-to-node path.
- **Iterative DFS or BFS.** Store `(node, remaining)` pairs in the container.
- **Sum Root to Leaf Numbers** (LeetCode 129). The carried state is `10 * value + digit` instead of a subtraction.

## What to carry forward

Carry the remainder down, decide only at leaves, and let `or` stop the search. The next problem, Path Sum II, keeps the remainder but must also remember the path itself, so it adds a shared list with push on entry and pop on exit.
