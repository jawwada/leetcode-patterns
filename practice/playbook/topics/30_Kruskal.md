## Kruskal's Minimum Spanning Tree Algorithm

Sort edges by weight. Accept an edge if its endpoints belong to different components, then union those components. An edge inside one component would create a cycle. A disconnected graph produces a minimum spanning forest.

<!-- cell -->

Kruskal builds the same kind of tree from an edge list: sort all edges once, cheapest first, and let union-find, from [Graphs II](00_Topic_Index.ipynb#s18), say whether an edge would close a loop, `find(u) == find(v)`. On the picture's graph it keeps four edges of total weight 11, and it stops as soon as it has n − 1.

<!-- cell -->

```python
def kruskal(n, edges):
    """edges = [(u, v, w)]. Returns (total weight, edges kept)."""
    parent = list(range(n))                       # STATE + INIT: everyone is their own group

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]         # path halving
            x = parent[x]
        return x

    total, kept = 0, []                           # STATE + INIT: the forest built so far
    edges = sorted(edges, key=lambda e: e[2])     # INIT: cheapest edge first
    for u, v, w in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            continue                              # both ends already connected: it would close a loop
        parent[ru] = rv                           # STEP: the edge merges two groups
        total += w                                # RECORD
        kept.append((u, v, w))
        if len(kept) == n - 1:
            break                                 # a spanning tree has exactly n - 1 edges
    return total, kept                            # RETURN: fewer than n - 1 edges = disconnected


print(kruskal(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3)]))
# (11, [(0, 2, 1), (1, 2, 2), (3, 4, 3), (1, 3, 5)])
```

<!-- cell -->

**Try it**
- Delete the `if ru == rv: continue` lines: you get `(10, [(0, 2, 1), (1, 2, 2), (3, 4, 3), (0, 1, 4)])`, four edges that contain the loop 0-1-2 and leave 3 and 4 cut off from the rest.
- Sort by `-e[2]` (heaviest first): a *maximum* spanning tree, weight 20.
- `kruskal(4, [(0, 1, 1), (2, 3, 1)])` keeps only 2 edges: fewer than `n - 1` means the graph is disconnected.

<!-- cell -->

```python
assert kruskal(3, [(0, 1, 1)]) == (1, [(0, 1, 1)])                      # disconnected: fewer than n - 1 edges
```

<!-- cell -->

Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree asks which edges every minimum spanning tree uses, the critical ones, and which only some of them use, the pseudo-critical ones. Kruskal is cheap, so run it once per question about one edge.

An edge is critical when skipping it makes the tree heavier, or impossible, where a run that cannot span counts as infinitely heavy. An edge that is not critical is pseudo-critical when forcing it in first still gives the best weight. Sort a list of indexes, not the edges themselves, so that the answer keeps the input's numbering (trap 11).
