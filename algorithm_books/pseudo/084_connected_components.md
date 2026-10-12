---
rank: 84
slug: connected_components
---

Given `n` nodes `0` to `n - 1` and a list of undirected edges, count the connected components, the groups of nodes that can reach one another, and label each node with the number of its component. With seven nodes and the edges `0-1`, `1-2`, `3-4` and `3-5` there are 3 components, `{0, 1, 2}`, `{3, 4, 5}` and the lone `{6}`, so the labels are `[0, 0, 0, 1, 1, 1, 2]`.

The brute force asks for every pair of nodes whether a path joins them, a search per pair, `O(V² · (V + E))`. The insight is that one search from a node reaches exactly its own component, all of it and nothing else. So scan the nodes in order: each node that is still unlabeled starts a flood fill that paints its entire component with a fresh label, and every node the flood paints is skipped when the scan reaches it. The number of floods is the number of components. The flood keeps an explicit stack, like the iterative DFS of #37, but paints each node the moment it is pushed, so no node enters the stack twice. As #37 points out, that order is no longer strictly depth-first, and here it does not matter: BFS would serve equally well, because all that counts is that every reachable node gets painted. `label` doubles as the visited mark, with `-1` for unpainted.

Picture paint poured on a node. It runs along the edges and stops at the border of the component, because no edge leaves it. The scan then walks past the painted nodes until it finds a dry one and pours the next color. On a grid the same loop counts islands (#38), with the four neighboring land cells as the edges.

```text
  0 ── 1 ── 2        3 ── 4        6
                     │
                     5

start   label[start]   action                     label after
  0         -1         flood with 0: 0, 1, 2      [0, 0, 0, -1, -1, -1, -1]
  1, 2     0, 0        already painted: skip
  3         -1         flood with 1: 3, 4, 5      [0, 0, 0, 1, 1, 1, -1]
  4, 5     1, 1        already painted: skip
  6         -1         flood with 2: 6            [0, 0, 0, 1, 1, 1, 2]
count = 3
```

```pseudo
FUNCTION ConnectedComponents(n, edges)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)                 // undirected: both directions
        graph[v].append(u)
    label ← array of n copies of -1        // -1 means not reached yet
    count ← 0
    FOR start FROM 0 TO n - 1
        IF label[start] = -1               // not reached by any earlier flood
            Flood(graph, start, count, label)
            count ← count + 1
    RETURN (count, label)

FUNCTION Flood(graph, start, mark, label)
    label[start] ← mark
    stack ← empty stack
    stack.push(start)
    WHILE stack is not empty
        node ← stack.pop()
        FOR EACH neighbor IN graph[node]
            IF label[neighbor] = -1
                label[neighbor] ← mark     // label when pushed: pushed once
                stack.push(neighbor)
```

Each node is painted once and each edge is examined from both ends, so the whole labeling costs `O(V + E)` time and space. Reach for it when a problem asks how many groups, networks, provinces or islands there are, whether two nodes are connected, or how big each group is; Count Unreachable Pairs needs only the component sizes, adding `size × (n - size)` over the components and halving the total. When the edges arrive one at a time and the count must stay current, union-find (#41) absorbs each new edge in near-constant time instead of flooding again. The classic mistake is storing each edge in one direction only: a flood from `0` can then never cross an edge written `[1, 0]`, and two nodes joined by that edge are counted as two components.

*Practice:* LC 323 Number of Connected Components in an Undirected Graph · LC 547 Number of Provinces · LC 1971 Find if Path Exists in Graph · LC 2316 Count Unreachable Pairs of Nodes in an Undirected Graph
