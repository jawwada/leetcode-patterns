---
rank: 119
slug: prim_mst
---

Given `n` nodes and weighted undirected edges, return the total weight of a minimum spanning tree, the cheapest set of edges that connects every node, or nothing if the graph is disconnected. For the edges `0-1 (4)`, `0-2 (1)`, `1-2 (2)`, `1-3 (5)`, `2-3 (8)`, `3-4 (3)` the answer is `11`.

Kruskal (#118) grows a forest whose pieces slowly merge; Prim grows a single tree from node 0 and never lets go of it. At every moment the tree and the rest of the graph form a cut, and by the cut property the cheapest edge crossing it is safe to add. So the whole algorithm is one repeated question: what is the cheapest edge from the tree to a node outside it? A min-heap answers it. Whenever a node joins the tree, push each of its edges to an outside node as `(weight, neighbor)`. Pop the smallest entry. If its node is already in the tree, the entry is stale, left over from before a cheaper edge pulled that node in, so skip it; otherwise the node joins the tree at that cost.

Picture an ink blot spreading over the graph, always seeping along the cheapest edge on its rim. The heap is the rim: every edge that leaves the blot, plus a few old ones that now point back inside, which the in-tree check throws away as they surface. This lazy deletion spares the heap any removal from its middle. The popped costs are not sorted, either: edge `3-4 (3)` comes after `1-3 (5)`, because it only touches the rim once node 3 is in.

```text
popped    action                     total   heap after the step
(0, 0)    add 0, push (4,1) (1,2)       0    (1,2) (4,1)
(1, 2)    add 2, push (2,1) (8,3)       1    (2,1) (4,1) (8,3)
(2, 1)    add 1, push (5,3)             3    (4,1) (5,3) (8,3)
(4, 1)    skip: 1 is already in         3    (5,3) (8,3)
(5, 3)    add 3, push (3,4)             8    (3,4) (8,3)
(3, 4)    add 4: all 5 nodes in        11    (8,3) is never popped

entries are (weight, node); the heap is listed smallest first
```

```pseudo
FUNCTION Prim(n, edges)
    graph ← array of n empty lists
    FOR EACH [u, v, w] IN edges
        graph[u].append((w, v))
        graph[v].append((w, u))               // undirected: both directions
    in_tree ← array of n copies of false
    heap ← empty min-heap
    heap.push((0, 0))                         // (cost to attach, node)
    total ← 0
    count ← 0
    WHILE heap is not empty AND count < n
        (cost, node) ← heap.pop()
        IF in_tree[node]
            CONTINUE                          // stale: joined by a cheaper edge
        in_tree[node] ← true                  // mark when popped, not pushed
        total ← total + cost
        count ← count + 1
        FOR EACH (weight, neighbor) IN graph[node]
            IF NOT in_tree[neighbor]
                heap.push((weight, neighbor))
    IF count < n
        RETURN null                           // some node was never reached
    RETURN total
```

Each edge enters the heap at most once, from whichever end joins the tree first, and a push or pop costs `O(log E) = O(log V)`, so Prim runs in `O(E log V)` time and `O(V + E)` space. It has the shape of Dijkstra's loop (#42), but the heap key is the weight of the single edge into the node, not a distance summed from the start, so negative weights do no harm. On a dense graph, such as points on a plane where every pair is an edge, drop the heap: keep an array `best[v]` of the cheapest edge from the tree to each outside node, pick the next node by an `O(V)` scan, refresh `best` from it in `O(V)`, and finish in `O(V²)` without ever listing the edges, the standard answer to Min Cost to Connect All Points. The classic mistake is marking a node as in the tree when it is pushed rather than popped, which freezes the first edge found to it instead of the cheapest.

*Practice:* LC 1584 Min Cost to Connect All Points · LC 1135 Connecting Cities With Minimum Cost · LC 1168 Optimize Water Distribution in a Village
