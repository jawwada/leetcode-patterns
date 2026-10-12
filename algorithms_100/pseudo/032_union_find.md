---
rank: 32
slug: union_find
---

Keep `n` nodes in disjoint groups under two operations: `union(a, b)` merges the groups of `a` and `b`, and `find(x)` returns the representative of the group of `x`, so two nodes are connected exactly when they share a representative. Feed it the edges `[0, 1]`, `[2, 3]`, `[0, 2]`, `[3, 1]` on five nodes. The first three each merge two groups; the fourth joins two nodes that are already connected, closing the cycle `0-1-3-2-0`, so it is redundant, and two groups remain, `{0, 1, 2, 3}` and `{4}`.

The brute force stores a group label per node and relabels a whole group on every merge, `O(n)` per union. Union-find stores each group as a tree of parent pointers instead. Every node points toward its root, and the root points at itself and names the group; `find` climbs to the root, and `union` hangs one root under the other with a single pointer write. Two rules keep the trees flat. Union by size hangs the smaller tree under the root of the bigger one, so a node sinks one level deeper only when its tree at least doubles, and no tree grows taller than `log2 n`. Path compression makes `find` repoint every node it climbs past straight at the root, so the next climb takes one step.

Picture a forest of small trees that only ever merge. In the trace, the last union finds `3` two levels below root `0`, and the recursion flattens that path on its way back. The union then returns `false`, because both ends already share root `0`: that `false` is the redundant edge of LC 684, and `count`, which drops by one on every successful union, is the number of components.

```text
edge     roots   what happens                      parent            count
 -                                                 [0, 1, 2, 3, 4]     5
[0, 1]   0, 1    1 hangs under 0, size[0] = 2      [0, 0, 2, 3, 4]     4
[2, 3]   2, 3    3 hangs under 2, size[2] = 2      [0, 0, 2, 2, 4]     3
[0, 2]   0, 2    tie: 2 hangs under 0, size 4      [0, 0, 0, 2, 4]     2
[3, 1]   0, 0    same root: false, redundant       [0, 0, 0, 0, 4]     2

the find(3) inside the last union:
       0                       0
      / \                    / | \
     1   2        ──→       1  2  3         4 stays alone
         |
         3
```

```pseudo
CLASS UnionFind
    FUNCTION Init(n)
        self.parent ← [0, 1, …, n - 1]     // every node starts as its own root
        self.size ← array of n copies of 1 // tree sizes, read only at roots
        self.count ← n                     // number of separate groups

    FUNCTION Find(x)
        IF self.parent[x] ≠ x
            self.parent[x] ← self.Find(self.parent[x])    // path compression
        RETURN self.parent[x]

    FUNCTION Union(a, b)
        root_a ← self.Find(a)
        root_b ← self.Find(b)
        IF root_a = root_b
            RETURN false                   // already connected: a cycle edge
        IF self.size[root_a] < self.size[root_b]
            swap(root_a, root_b)           // root_a is the bigger tree
        self.parent[root_b] ← root_a
        self.size[root_a] ← self.size[root_a] + self.size[root_b]
        self.count ← self.count - 1
        RETURN true

FUNCTION CountComponents(n, edges)
    uf ← UnionFind(n)
    FOR EACH (a, b) IN edges
        uf.Union(a, b)
    RETURN uf.count

FUNCTION FindRedundantConnection(edges)
    uf ← UnionFind(len(edges) + 1)         // nodes are 1..n; slot 0 unused
    FOR EACH (a, b) IN edges
        IF NOT uf.Union(a, b)              // first edge inside one group
            RETURN [a, b]
    RETURN empty list
```

With both rules, `m` operations on `n` nodes cost `O(m · alpha(n))`, where `alpha` is the inverse Ackermann function, at most 4 for any `n` a computer can hold: constant time in practice, and `O(n)` space. Reach for union-find when edges or equivalences arrive one at a time and the questions are "are these two connected?" and "how many groups are there now?": redundant connections, accounts that share an email, islands that appear one cell at a time, and the cycle test inside Kruskal's minimum spanning tree (#83). A flood fill (#62) answers the same questions for a graph given all at once but must search again after every new edge; union-find absorbs each edge in near-constant time, though it can never split a group. The classic mistake is comparing parents instead of roots: before the last union `parent[3]` is `2` and `parent[1]` is `0`, so the redundant edge `[3, 1]` would pass for a new connection.

*Practice:* LC 684 Redundant Connection · LC 547 Number of Provinces · LC 323 Number of Connected Components in an Undirected Graph · LC 721 Accounts Merge
