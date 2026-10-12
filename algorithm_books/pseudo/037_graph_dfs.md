---
rank: 37
slug: graph_dfs
---

Given an undirected graph with nodes `0` to `n - 1` and a list of edges, list the nodes in the order a depth-first search from `start` first reaches them, trying each node's neighbors in the order its edges appear. With `n = 5`, edges `[[0, 1], [0, 4], [0, 2], [1, 3], [3, 2]]` and `start = 0` the order is `[0, 1, 3, 2, 4]`.

Depth-first search is the maze walker's rule: always step to an unvisited neighbor of the node you stand on, and only when there is none, back up to the previous junction and try its next corridor. The recursion is that rule written down. Entering a node marks it visited, records it, and calls itself on every neighbor not yet visited; the call stack is the trail back to the start, and returning from a call is the step back. Marking on entry is what makes cycles harmless: the square `0, 1, 3, 2` leads back to `0`, but `0` is already marked, so the walk turns away instead of circling forever.

The iterative version swaps the call stack for an explicit one, and where it marks decides whether it is still depth-first. Marking a node when it is popped, and skipping the stale copies of nodes pushed twice, reproduces the recursion exactly, as long as the neighbors go on in reverse so the first one ends on top. Marking a node when it is pushed looks tidier, since nothing is pushed twice, but it is a different search: whoever sees a node first claims it, even when a deeper node would have stepped into it sooner. Here `0` claims `2`, so `3` cannot step to it and the walk retreats to `4`, giving `[0, 1, 3, 4, 2]`, an order no depth-first search can produce.

```text
  4 ─── 0 ─── 1      pop   action                stack after   order
        │     │       0    visit, push 2, 4, 1   [2, 4, 1]     [0]
        2 ─── 3       1    visit, push 3         [2, 4, 3]     [0, 1]
                      3    visit, push 2         [2, 4, 2]     [0, 1, 3]
  the top of the      2    visit, push nothing   [2, 4]        [0, 1, 3, 2]
  stack is on the     4    visit, push nothing   [2]           [0, 1, 3, 2, 4]
  right               2    stale copy: skip      []
marking on push instead: [0, 1, 3, 4, 2], since 2 was already claimed by 0
```

```pseudo
FUNCTION BuildGraph(n, edges)
    graph ← empty list
    FOR i FROM 0 TO n - 1
        graph.append(empty list)
    FOR EACH (u, v) IN edges
        graph[u].append(v)
        graph[v].append(u)                 // undirected: both directions
    RETURN graph

FUNCTION DfsRecursive(n, edges, start)
    graph ← BuildGraph(n, edges)
    visited ← empty set
    order ← empty list
    Visit(graph, start, visited, order)
    RETURN order

FUNCTION Visit(graph, node, visited, order)
    visited.add(node)                      // mark first: cycles cannot re-enter
    order.append(node)
    FOR EACH neighbor IN graph[node]
        IF neighbor NOT IN visited
            Visit(graph, neighbor, visited, order)

FUNCTION DfsIterative(n, edges, start)
    graph ← BuildGraph(n, edges)
    visited ← empty set
    order ← empty list
    stack ← empty stack
    stack.push(start)
    WHILE stack is not empty
        node ← stack.pop()
        IF node IN visited
            CONTINUE                       // a stale copy, reached another way
        visited.add(node)                  // mark when popped
        order.append(node)
        FOR EACH neighbor IN reversed(graph[node])   // first one ends on top
            IF neighbor NOT IN visited
                stack.push(neighbor)
    RETURN order
```

Every node is entered once and every edge is examined from both ends, so both versions run in `O(V + E)` time; the recursion can be `V` frames deep, and the explicit stack can hold one entry per edge end, `O(E)`. Reach for it whenever the question is about reachability, connectivity or exploring paths: counting components (#84), flood fill on a grid (#38), cycle detection (#81) and topological order (#82) are all this walk with something recorded on the way in or out. A directed graph drops the second `append`. In Python the recursive form dies on deep graphs, because the default recursion limit is 1000 frames and a path of a thousand nodes raises `RecursionError`, so the iterative version is the safe default. The classic mistake is marking a node only after its neighbors are explored, which lets a cycle walk back into it until the stack overflows.

*Practice:* LC 547 Number of Provinces · LC 841 Keys and Rooms · LC 797 All Paths From Source to Target · LC 133 Clone Graph
