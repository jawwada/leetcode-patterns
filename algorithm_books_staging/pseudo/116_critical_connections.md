---
rank: 116
slug: critical_connections
---

A network has `n` nodes joined by undirected connections, none repeated. A connection is critical, a bridge, when removing it cuts some pair of nodes off from each other. Return every bridge, each pair sorted and the list sorted. Seven nodes forming two triangles, `0-1-2` and `3-4-5`, joined by the edge `1-3`, with one more edge `5-6` hanging off node 5, have the bridges `[[1, 3], [5, 6]]`.

The brute force removes each edge in turn and checks whether the graph still hangs together, `O(E · (V + E))`. One depth-first search finds every bridge at once. It stamps `disc[u]`, the time node `u` is first reached, and its tree edges form a spanning tree in which every other edge is a back edge, joining a node to one of its ancestors. A back edge lies on a cycle with the tree path between its ends, so it is never a bridge. Removing a tree edge `u → v` leaves the subtree of `v` attached exactly when some back edge leaves that subtree and lands on `u` or above it, closing a cycle through the edge. So let `low[u]` be the smallest discovery time reachable from `u`'s subtree using one back edge. The tree edge `u → v` is a bridge exactly when `low[v] > disc[u]`: nothing below `v` reaches back to `u` or higher, so cutting the edge strands the whole subtree.

Low-links are settled on the way back up. On entry `low[u]` starts at `disc[u]`; a back edge to an ancestor `v` can lower it to `disc[v]`, and each finished child `v` can lower it to its own `low[v]`. Only the edge to the parent is skipped, because it is the tree edge just walked, seen from below. The same numbers find articulation points, the nodes whose removal disconnects the graph: a non-root `u` is one when some tree child `v` has `low[v] ≥ disc[u]`, and the root is one when it has two or more tree children.

```text
    0               4
   / \             / \
  2 ─ 1 ───────── 3 ─ 5 ───────── 6

node   0  1  2  3  4  5  6
disc   0  1  2  3  4  5  6
low    0  0  0  3  3  3  6

tree edge u → v   low[v] > disc[u]?
0 → 1             0 > 0   no
1 → 2             0 > 1   no     2 reaches 0 by the back edge 2-0
1 → 3             3 > 1   yes    bridge [1, 3]
3 → 4             3 > 3   no
4 → 5             3 > 4   no     5 reaches 3 by the back edge 5-3
5 → 6             6 > 5   yes    bridge [5, 6]
```

```pseudo
FUNCTION CriticalConnections(n, connections)
    graph ← array of n empty lists
    FOR EACH (u, v) IN connections
        graph[u].append(v)
        graph[v].append(u)                 // undirected: both directions
    disc ← array of n copies of -1         // discovery time, -1 = not visited
    low ← array of n zeros                 // lowest disc the subtree reaches
    timer ← [0]                            // next discovery time, one box
    bridges ← empty list
    FOR start FROM 0 TO n - 1              // one DFS per component
        IF disc[start] = -1
            Dfs(graph, start, -1, disc, low, timer, bridges)
    bridges.sort()                         // a deterministic order
    RETURN bridges

FUNCTION Dfs(graph, u, parent, disc, low, timer, bridges)
    disc[u] ← timer[0]
    low[u] ← timer[0]
    timer[0] ← timer[0] + 1
    FOR EACH v IN graph[u]
        IF v = parent
            CONTINUE                       // the tree edge we came down by
        IF disc[v] = -1                    // tree edge: explore v first
            Dfs(graph, v, u, disc, low, timer, bridges)
            low[u] ← min(low[u], low[v])
            IF low[v] > disc[u]            // nothing below v reaches u or above
                bridges.append([min(u, v), max(u, v)])
        ELSE
            low[u] ← min(low[u], disc[v])  // back edge to an ancestor
```

Each node is entered once and each edge is examined from both ends, so the search runs in `O(V + E)` time and space. The recursion is as deep as the longest DFS path, up to `n` frames, so a DFS path longer than about a thousand nodes passes Python's default recursion limit; inputs that large need the same search with an explicit stack of (node, next neighbor) pairs. The outer loop over start nodes handles a disconnected graph at no extra cost. Reach for low-links when a problem asks which single link, road or cable is critical, or which single node is a single point of failure, as in Minimum Number of Days to Disconnect Island, where an island of two or more cells splits after losing one cell exactly when it has an articulation point. The classic mistake is mixing up the two tests: `≥` belongs to articulation points, and using it for bridges here also reports `0-1` and `3-4`, which both lie on triangles. Forgetting to skip the parent is the other: the edge just walked then counts as a back edge, every child reaches its parent, and no bridge is ever reported.

*Practice:* LC 1192 Critical Connections in a Network · LC 1568 Minimum Number of Days to Disconnect Island
