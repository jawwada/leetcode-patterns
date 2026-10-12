# Binary Tree Level Order Traversal (LeetCode 102)

**Area:** trees · **Difficulty:** Medium · **Key operations:** queue of the current level, snapshot len(q), popleft and push children, append the level

## Problem

Given the root of a binary tree, return its node values level by level, left to right, as a list of lists. Trees are given in LeetCode's level-order list form with `None` for a missing child.

## Example

```
[3, 9, 20, None, None, 15, 7]

        3
       / \
      9   20
         /  \
        15   7

-> [[3], [9, 20], [15, 7]]
```

## Brute force

Compute the height `h`, then for each depth `d = 0 .. h-1` run a fresh DFS over the whole tree collecting the nodes whose depth is exactly `d`, left to right.

O(n · h) time (O(n²) on a chain), O(h) stack space. The wasted work: each DFS pass walks all `n` nodes but keeps only the ones on a single level, so every node is visited `h` times.

## From brute force to optimal

While the brute force is collecting level `d`, it is standing right next to the nodes of level `d + 1`: they are the children of what it just collected. Keep them instead of rediscovering them. A FIFO queue holds the current frontier in left-to-right order. Record `len(q)` at the start of a round: that many nodes are exactly the current level, because all of them are already queued and none of their children have been added yet. Pop that many, pushing each node's children behind, and the queue now holds exactly the next level, again in order. Every node is enqueued and dequeued once.

## Intuition

Picture a horizontal line sweeping down the drawing of the tree one row at a time. The queue is the set of nodes currently on the line. Each round replaces the line's nodes by their children, left to right, so the next row arrives already in order. The only extra trick beyond plain BFS is the snapshot: `len(q)` at the top of the round is the width of the row, and it must be read before the row's children start arriving.

## Walkthrough

The queue is shown front to back; `level` is the row being built.

```
        3
       / \
      9   20
         /  \
        15   7

round 0   queue [3]         snapshot 1
          pop 3   push 9, 20          queue [9, 20]      level [3]
          -> levels [[3]]

round 1   queue [9, 20]     snapshot 2
          pop 9   no children         queue [20]         level [9]
          pop 20  push 15, 7          queue [15, 7]      level [9, 20]
          -> levels [[3], [9, 20]]

round 2   queue [15, 7]     snapshot 2
          pop 15  no children         queue [7]          level [15]
          pop 7   no children         queue []           level [15, 7]
          -> levels [[3], [9, 20], [15, 7]]

queue empty -> return [[3], [9, 20], [15, 7]]
```

In round 1 the queue grows to `[20, 15, 7]` in the middle of the round; the snapshot of 2 is what stops the round after popping 20, leaving 15 and 7 for the next row.

## Steps

1. If the root is `None`, return `[]`. `q = deque([root])`, `levels = []`.
2. While the queue is not empty: `level = []`, then repeat `len(q)` times (read once, before the loop):
3. Pop the front node, append its value to `level`, push its left child then its right child if they exist.
4. Append `level` to `levels`.
5. Return `levels`.

## Complexity

O(n) time: each node is pushed and popped once. O(w) space for the queue, where `w` is the widest level (up to about n/2).

## Pitfalls

- **Draining the queue instead of popping the snapshot.** `while q:` as the inner loop keeps popping the children that were just pushed, so every node lands in one level: the example gives `[[3, 9, 20, 15, 7]]`. Read `len(q)` once at the top of the round.
- **Popping from the right.** `q.pop()` turns the queue into a stack: children of the last node come out before the earlier nodes, so levels mix and reverse (`[[3], [20, 7], [15, 9]]`). Use `popleft`.
- **Copy-paste guard.** Guarding the right push with `if node.left:` skips a right child whose sibling is missing, and pushes `None` when a left child exists without a right one; `[1, None, 2]` loses the 2 and `[1, 2]` crashes on `None.val`.
- **Enqueueing `None` children.** Every push must be guarded; otherwise the next pop reads `.val` of `None`.
- **Empty tree.** `deque([None])` is non-empty, so check the root before starting.
