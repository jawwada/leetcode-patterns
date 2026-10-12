---
rank: 118
slug: kruskal_mst
---

Given `n` nodes and weighted undirected edges, choose `n - 1` edges that connect every node with the smallest possible total weight: a minimum spanning tree. Return its weight and its edges, or nothing if the graph is disconnected. With edges `0-1 (4)`, `0-2 (1)`, `1-2 (2)`, `1-3 (5)`, `2-3 (8)`, `3-4 (3)` the tree is `0-2, 1-2, 3-4, 1-3` with weight `11`.

The cut property makes greed safe. Split the nodes into any two groups: the cheapest edge crossing between them belongs to some minimum spanning tree. If a tree left it out, adding it would close a cycle, that cycle would cross the split a second time through another edge that is no cheaper, and swapping the two gives a tree that is no heavier. Kruskal applies this one edge at a time. Sort the edges by weight and scan them cheapest first. An edge whose ends already lie in the same component would close a cycle, so it is rejected. An edge that joins two different components is the cheapest edge leaving either of them, because every cheaper edge has already been scanned and either merged its ends or found them together; by the cut property it is safe, so take it.

Picture the nodes as islands and the sorted edges as bridges offered cheapest first. Union-find (#41) remembers which islands are already linked, so each offer costs two near-constant finds: the same root means reject, different roots means build the bridge and merge. Once `n - 1` bridges stand, every island is linked and the scan stops; if the offers run out first, the graph is disconnected.

```text
sorted   edge   w   components before       action                 total
  1      0-2    1   {0} {1} {2} {3} {4}     take                     1
  2      1-2    2   {0,2} {1} {3} {4}       take                     3
  3      3-4    3   {0,1,2} {3} {4}         take                     6
  4      0-1    4   {0,1,2} {3,4}           skip: same component     6
  5      1-3    5   {0,1,2} {3,4}           take                    11
  6      2-3    8   never examined: n - 1 = 4 edges already taken

tree    0 ─(1)─ 2 ─(2)─ 1 ─(5)─ 3 ─(3)─ 4          total 11
```

```pseudo
FUNCTION Find(parent, x)
    IF parent[x] ≠ x
        parent[x] ← Find(parent, parent[x])   // path compression
    RETURN parent[x]

FUNCTION Union(parent, size, a, b)
    root_a ← Find(parent, a)
    root_b ← Find(parent, b)
    IF root_a = root_b
        RETURN false                          // already one component
    IF size[root_a] < size[root_b]
        swap(root_a, root_b)                  // hang the smaller tree below
    parent[root_b] ← root_a
    size[root_a] ← size[root_a] + size[root_b]
    RETURN true

FUNCTION Kruskal(n, edges)
    order ← empty list
    FOR EACH [u, v, w] IN edges
        order.append((w, u, v))               // weight first: sort by weight
    order.sort()                              // cheapest edge first
    parent ← [0, 1, …, n - 1]                 // every node is its own root
    size ← array of n copies of 1
    total ← 0
    tree ← empty list
    FOR EACH (w, u, v) IN order
        IF Union(parent, size, u, v)          // two components: edge is safe
            total ← total + w
            tree.append([u, v, w])
            IF len(tree) = n - 1
                BREAK                         // n - 1 edges span all n nodes
    IF len(tree) < n - 1
        RETURN null                           // the graph is disconnected
    RETURN (total, tree)
```

Sorting dominates: `O(E log E)` time, the same as `O(E log V)`, plus near-constant union-find work per edge and `O(V)` space beyond the edges. Reach for Kruskal when the graph arrives as an edge list, when the question is the cheapest way to connect everything (cities, points, network links), or when single edges must be forced in or kept out: finding the critical edges of a minimum spanning tree means rerunning Kruskal with one edge banned or taken first. On a dense graph given as points, the array version of Prim (#119) avoids building and sorting all `O(n²)` edges. The classic mistakes are sorting `[u, v, w]` triples as they come, which orders them by `u` instead of by weight, and returning the weight of a forest without checking that `n - 1` edges were taken.

*Practice:* LC 1584 Min Cost to Connect All Points · LC 1135 Connecting Cities With Minimum Cost · LC 1489 Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree
