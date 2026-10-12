---
rank: 32
slug: level_order_traversal
---

Given the root of a binary tree, return its values level by level, each level read from left to right. Writing the tree in level order with `null` for a missing child, `[3, 9, 20, null, null, 15, 7]` is a root `3` with children `9` and `20`, and `20` has children `15` and `7`; the answer is `[[3], [9, 20], [15, 7]]`.

A queue already visits a tree in level order. The root goes in, and every node that comes out sends its children to the back, so all of depth `d` leaves the queue before anything of depth `d + 1`. What a plain breadth-first search loses is the boundary: it produces one flat stream and forgets where one level ends and the next begins. The fix is a snapshot. At the top of each round the queue holds exactly one complete level, nothing more and nothing less, so `size ← len(queue)` freezes that count and the inner loop pops exactly `size` nodes. The children those pops enqueue pile up behind them and become the next level, untouched until the next round takes its own snapshot.

Picture the tree peeled from the top, one horizontal layer per round: the front of the queue is the layer being stripped off, the back is the layer being laid down. Left-to-right order comes for free, because parents leave the queue left to right and each one enqueues its left child before its right.

```text
        3         round   queue at start   size   popped    enqueued
       / \          1     [3]                1    3         9, 20
      9   20        2     [9, 20]            2    9, 20     15, 7
         /  \       3     [15, 7]            2    15, 7     nothing
        15   7            []                      the queue is empty: stop
levels = [[3], [9, 20], [15, 7]]
```

```pseudo
FUNCTION LevelOrder(root)
    levels ← empty list
    IF root = null
        RETURN levels
    queue ← empty queue
    queue.enqueue(root)
    WHILE queue is not empty
        size ← len(queue)                  // snapshot: exactly this level
        level ← empty list
        FOR i FROM 0 TO size - 1
            node ← queue.dequeue()
            level.append(node.val)
            IF node.left ≠ null            // children join the back
                queue.enqueue(node.left)
            IF node.right ≠ null
                queue.enqueue(node.right)
        levels.append(level)               // the level is complete
    RETURN levels
```

Every node is enqueued and dequeued once, so the traversal takes `O(n)` time; the queue never holds more than one level plus part of the next, `O(w)` space for the widest level `w`, which reaches about `n / 2` in a complete tree. Reach for it whenever a problem says level, depth, row, layer or "seen from the side". The variants differ only in what each finished level contributes: the right side view keeps its last value, zigzag order reverses every other `level` before appending it, and the average of each level divides its sum by `size`. On a general graph the same loop needs a visited set and becomes BFS shortest path (#39). The classic mistake is looping against the live queue length instead of the snapshot: the children enqueued during the round grow the queue, and the next level leaks into this one.

*Practice:* LC 102 Binary Tree Level Order Traversal · LC 199 Binary Tree Right Side View · LC 103 Binary Tree Zigzag Level Order Traversal · LC 637 Average of Levels in Binary Tree
