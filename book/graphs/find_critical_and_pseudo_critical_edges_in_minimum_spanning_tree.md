# Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree
*LeetCode 1489 · Hard · Pattern: Kruskal MST (sorted edges + union-find) · Reading time ~12 min*

## What the problem is really asking

A connected, undirected, weighted graph can have several minimum spanning trees when
weights tie. Sort every edge into one of three bins:

- **critical**: in **every** MST. Deleting it makes the best spanning tree heavier (or
  impossible).
- **pseudo-critical**: in **some** MSTs but not all.
- **neither**: in no MST at all.

Return the indices of the first two bins. Here is the graph we will trace (edge `eI:w` is
index `I`, weight `w`):

```text
      0 ------ e0:1 ------ 1
      | \                / |
      |  e4:3        e6:6  |
      |     \        /     |
    e3:2      \    /     e1:1
      |         4          |
      |       /            |
      |   e5:3             |
      | /                  |
      3 ------ e2:2 ------ 2

  edge list  e0 [0,1,1]  e1 [1,2,1]  e2 [2,3,2]  e3 [0,3,2]
             e4 [0,4,3]  e5 [3,4,3]  e6 [1,4,6]
  MST weight 7.   answer: critical [0,1], pseudo [2,3,4,5]
```

The answer is two lists of indices. What makes it hard: "every MST" and "some MST" are
statements about a family of trees that can be exponentially large, and we cannot list it.

## Do it by hand first

Think of Kruskal (from the previous problem): take edges lightest first, keep an edge if it
joins two separate clumps. Do it by hand and pay attention to the **ties**.

```text
  weight 1: e0 (0-1), e1 (1-2)   both needed, no rival
            clumps {0,1,2} {3} {4}
  weight 2: e2 (2-3), e3 (0-3)   both join {3} to {0,1,2}
            only ONE can be taken: a choice
            clumps {0,1,2,3} {4}
  weight 3: e4 (0-4), e5 (3-4)   both join {4} to the rest
            only ONE can be taken: a choice
  weight 6: e6 (1-4)             everything already joined
```

The tie groups tell the story. e0 and e1 had no rival at their weight, so every MST takes
them. e2/e3 and e4/e5 were interchangeable pairs, so each sits in some MSTs. e6 never had a
chance. Your hand tracked **clumps** (union-find) and **which edges compete for the same
merge at the same weight**. That second notion is what we need to make precise.

## The first honest attempt

Enumerate every set of `n - 1` edges, keep those that are spanning trees, find the minimum
weight `W`, then check each edge against all trees of weight `W`.

```text
  C(7,4) = 35 subsets for this tiny graph
  {e0,e1,e2,e4} tree, 7     {e0,e1,e3,e5} tree, 7
  {e0,e1,e2,e3} cycle 0-1-2-3, rejected
  {e0,e2,e3,e6} tree, 11    ... 31 more ...
  every subset re-checks connectivity from nothing
```

`C(E, n-1)` subsets is exponential. The waste: almost every subset is either not a tree or
nowhere near minimal, while Kruskal builds a minimum tree directly in `O(E log E)`.

## The turning point

**Claim: one question about one edge needs one Kruskal run. "Is edge `i` critical?" is
"does Kruskal without `i` get heavier than `W`?", and "is edge `i` in some MST?" is "does
Kruskal with `i` forced in first still reach `W`?"**

Start with the cut property from the previous problem: for any split of the nodes into two
groups, a cheapest edge crossing the split belongs to some MST. Kruskal applies it every
time it accepts an edge.

**Exclude test.** Run Kruskal on the graph with edge `i` deleted. If some MST avoids `i`,
that tree is still available, so the result is `W`. If the result is larger than `W` (or the
graph falls apart), no MST avoids `i`: every MST contains it. So:

`critical  <=>  mst(skip = i) > W`

**Force test.** Union edge `i`'s endpoints before anything else, add its weight, then run
Kruskal normally. This builds the cheapest spanning tree **among those containing `i`**
(collapse `i` into one node; Kruskal on the collapsed graph is optimal there). If that equals
`W`, some MST contains `i`. So:

`in some MST  <=>  mst(force = i) == W`

Combine: critical edges are found by the exclude test; among the rest, the force test picks
out pseudo-critical edges; anything left over is in no MST. The order matters: a critical
edge also passes the force test, so check exclusion first.

One helper does both runs; the solution file calls it `mst(skip, force)`:

```python
def mst(skip=-1, force=-1):
    parent = list(range(n)); total = used = 0
    if force >= 0: union the forced edge; total, used = w, 1
    for i in order:              # indices sorted by weight
        if i != skip and union(u_i, v_i):
            total += w_i; used += 1
    return total if used == n - 1 else inf
```

Why is this a good trade? Each Kruskal run reuses the same sorted index list, so it costs a
single linear pass with union-find, nearly `O(E)`. Two runs per edge gives about `2E` passes:
for the problem's limits (`E <= 200`) that is tiny, and it replaces an exponential
enumeration with a polynomial one. The idea generalises far beyond MSTs: whenever you need
to know whether an element is in **every** optimal solution or in **some** optimal solution,
re-solve once with the element banned and once with it forced, and compare each result with
the unconstrained optimum.

Note how forcing is done. The fresh union-find has every node as its own root, so writing
`parent[u] = v` directly is a valid union. Later, when Kruskal reaches edge `i` itself in
the sorted order, its endpoints already share a root and it is skipped, so it is never
counted twice.

Two details. `order` is a sorted list of **indices**, not a sorted copy of the edges, so the
answer can report original indices. And a run that ends with fewer than `n - 1` edges means
the graph came apart; it must return infinity, not its partial (small) total.

## Watch it work

Union-find `parent` arrays are exact, including the path-halving rewrites done by `find`.

```text
Frame 1  base run, weight-1 edges
  e0 0-1: roots 0,1 differ -> take   parent [1,1,2,3,4]
  e1 1-2: roots 1,2 differ -> take   parent [1,2,2,3,4]
  total 2, clumps {0,1,2} {3} {4}
```
Both lightest edges are accepted; node 0's chain is now 0 -> 1 -> 2.

```text
Frame 2  base run, weight-2 edges
  e2 2-3: roots 2,3 differ -> take   parent [1,2,3,3,4]
  e3 0-3: find(0) halves path        parent [2,2,3,3,4]
          roots 3,3 equal  -> skip
  total 4, clumps {0,1,2,3} {4}
```
e3 lost the tie only because e2 came first in the sorted order.

```text
Frame 3  base run, the rest
  e4 0-4: roots 3,4 -> take          parent [3,2,3,4,4]
  e5 3-4: roots 4,4 -> skip
  e6 1-4: roots 4,4 -> skip
  W = 1+1+2+3 = 7
```
The baseline is fixed: every later run is compared with 7.

```text
Frame 4  exclude e0
  take e1, e2, e3, e4  ->  1+2+2+3 = 8
  8 > 7  =>  e0 is CRITICAL
  (exclude e1 also gives 8 => e1 CRITICAL)
```
Without e0, node 0 must be reached by e3 (weight 2) instead of weight 1.

```text
Frame 5  exclude e2, then force e2
  skip e2:  takes e0 e1 e3 e4 -> 7   not critical
  force e2: parent [0,1,3,3,4], total 2
            takes e0 e1 e4    -> 7   == W
  => e2 PSEUDO-CRITICAL
```
e3 stands in for e2 at no extra cost, yet e2 can be in an optimal tree.

```text
Frame 6  exclude e4 (shows the e4/e5 tie)
  takes e0 e1 e2 e5 -> 7   not critical
  force e4 -> 7            => e4 PSEUDO
  (e3 and e5 behave the same way)
```
Each member of a tied pair can replace the other.

```text
Frame 7  exclude e6, then force e6
  skip e6:  7  not critical
  force e6: parent [0,4,2,3,4], total 6
            takes e0 e1 e2 -> 6+1+1+2 = 10 != 7
  => e6 in no MST
```
Forcing the heavy edge costs 3 more than the best tree, so it is never optimal.

```text
Frame 8  result
   edge   skip   force   bin
   e0       8      7     critical
   e1       8      7     critical
   e2       7      7     pseudo
   e3       7      7     pseudo
   e4       7      7     pseudo
   e5       7      7     pseudo
   e6       7     10     neither
```
Critical `[0,1]`, pseudo-critical `[2,3,4,5]`, matching the expected output.

Across frames, union-find held the clumps of one run only (a fresh `parent` every run), and
the sorted index order never changed; only `skip` and `force` did.

## Why it is correct

Three facts.

1. **Kruskal returns an MST.** Each accepted edge is the lightest edge crossing the cut
   around one of its endpoint clumps (lighter edges were all seen already and are inside
   clumps), so by the cut property the accepted set stays inside some MST.
2. **Exclusion.** The MST weight of `G - i` is `W` exactly when some MST of `G` avoids `i`;
   otherwise it is larger or the graph is disconnected. That is the definition of
   critical.
3. **Forcing.** Spanning trees containing `i` correspond one-to-one with spanning trees of
   the graph where `i`'s endpoints are merged, plus `w(i)`. Kruskal after the forced union
   is exactly Kruskal on that merged graph, so it returns the minimum weight of a spanning
   tree containing `i`. It equals `W` exactly when some MST contains `i`.

An edge in some MST but not critical is, by definition, in some but not all MSTs:
pseudo-critical. Checking critical first keeps the bins disjoint.

## Cost

- **Time `O(E^2 · α(n))` plus one `O(E log E)` sort**: up to two Kruskal runs per edge,
  each a linear pass over the pre-sorted indices with near-constant union-find operations.
  The solution file's docstring states it loosely as `O(E^2 log E)`.
- **Space `O(n + E)`**: the parent array and the sorted index list.

The faster `O(E log E)` method works tie group by tie group: within one weight, an edge is
in some MST if it joins two different clumps, and critical if it is also a bridge of the
small graph formed by that group on the clumps. That needs Tarjan's bridge-finding, which is
the next problem.

## Variations you will meet

- **Is a given edge in some MST?** One force run (or: is it among the cheapest edges
  crossing the cut its weight induces). Same reasoning, one edge only.
- **Second-best MST.** Try excluding each edge of the base MST; the best of those runs is the
  second-best tree. Same exclude idea.
- **Remove Max Number of Edges to Keep Graph Fully Traversable.** Also Kruskal with
  priority, but the priority is edge type, not weight.
- **Unique MST check.** The MST is unique exactly when every MST edge is critical.

## What to carry forward

To ask "every optimum or some optimum?" about an element, re-solve with the element banned
and with it forced; for MSTs each re-solve is one cheap Kruskal pass over pre-sorted
indices. The final problem asks the same "is this edge indispensable?" question without
weights, for connectivity itself, and answers it for every edge in a single DFS.
