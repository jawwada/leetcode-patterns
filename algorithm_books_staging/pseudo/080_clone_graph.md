---
rank: 80
slug: clone_graph
---

Given one node of a connected undirected graph, where every node holds a value and a list of its neighbors, return a deep copy of the whole graph: new nodes with the same values, wired the same way, without a single pointer into the original. The square `1-2-3-4-1`, written as the adjacency list `[[2, 4], [1, 3], [2, 4], [1, 3]]` where row `i` lists the neighbors of node `i + 1`, must come back as the same list built from four brand-new nodes.

A copy that simply copies every neighbor it meets goes wrong in two ways. It never stops, because every undirected edge is a cycle of pointers: copying `1` copies its neighbor `2`, whose list leads straight back to `1`. And even a copy that somehow stopped would give a node reached along two paths two copies, as `3` is reached from both `2` and `4`, so the clone would not have the original's shape. Both failures come from forgetting what was already copied, and one map from each original node to its copy cures both. The map answers "have I met this node before?" exactly as a visited set would, and it also hands over the copy that a new edge must point at. So the map is the visited set, and a breadth-first search over the original (#39) does the rest.

The search follows one rule. A node's copy is made the moment the node is first seen as somebody's neighbor, and the node is queued then. When a node is popped, every one of its edges is copied by appending the neighbor's copy to the popped node's copy. An edge to a node that already has a copy is appended too, and those edges are what close the cycles in the clone. Each node is popped exactly once, so each copy receives its neighbor list exactly once, in the original's order.

```text
  1 ── 2       the original                1' ── 2'     the clone: four
  │    │                                   │     │      new node objects
  4 ── 3                                   4' ── 3'

pop   neighbors   copies made   neighbors of its copy   queue after
 -        -           1'                  -                [1]
 1      2, 4        2', 4'            [2', 4']             [2, 4]
 2      1, 3        3'                [1', 3']             [4, 3]
 4      1, 3        none              [1', 3']             [3]
 3      2, 4        none              [2', 4']             []
```

```pseudo
CLASS Node
    FUNCTION Init(val)
        self.val ← val
        self.neighbors ← empty list

FUNCTION CloneGraph(node)
    IF node = null
        RETURN null
    copies ← empty map                     // old node → its copy
    copies[node] ← new Node(node.val)
    queue ← empty queue
    queue.enqueue(node)
    WHILE queue is not empty
        current ← queue.dequeue()
        FOR EACH neighbor IN current.neighbors
            IF neighbor NOT IN copies      // first sighting: copy, visit later
                copies[neighbor] ← new Node(neighbor.val)
                queue.enqueue(neighbor)
            copies[current].neighbors.append(copies[neighbor])  // copy to copy
    RETURN copies[node]
```

Every node is copied, queued and popped once, and every neighbor list is walked once, so the clone costs `O(V + E)` time and `O(V)` extra space for the map and the queue, beyond the clone itself. Reach for the old-to-new map whenever a structure with shared or cyclic references must be deep-copied. Copy List with Random Pointer is the same idea on a list: one pass puts a copy of every node in the map, and a second pass wires each copy's `next` and `random` through it. A recursive DFS works just as well, provided a node's copy enters the map before the recursion reaches its neighbors; otherwise a cycle recurses forever. The classic mistake is appending only the neighbors seen for the first time: the edges of the search tree survive, every edge back to an already copied node is lost, and the square comes back as `[[2, 4], [3], [], []]`.

*Practice:* LC 133 Clone Graph · LC 138 Copy List with Random Pointer · LC 1490 Clone N-ary Tree
