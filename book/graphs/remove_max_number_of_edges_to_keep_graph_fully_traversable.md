# Remove Max Number of Edges to Keep Graph Fully Traversable
*LeetCode 1579 · Hard · Pattern: Union-Find (disjoint set union) · Reading time ~10 min*

## What the problem is really asking

There are `n` nodes, `1` to `n`, and a list of undirected edges `[type, u, v]`. Alice can
walk on edges of type 1, Bob on edges of type 2, and both of them on type 3. You want to
delete as many edges as possible while keeping two promises: from any node Alice can still
reach every other node using only her edges, and the same for Bob. Return the number of
deleted edges, or `-1` if even the full graph breaks a promise.

Flip it around: deleting the most edges is keeping the fewest. So the real question is
"what is the smallest set of edges that keeps both players' graphs connected?" The answer
is a count. What makes it hard is that one edge (type 3) can serve two masters, so the two
connectivity requirements are coupled.

The example we will trace:

```text
   edges (input order)     legend
   e0 [3, 1, 2]            === type 3 (both)
   e1 [3, 2, 3]            --- type 1 (Alice only)
   e2 [1, 1, 3]            ... type 2 (Bob only)
   e3 [1, 2, 4]
   e4 [1, 1, 2]            n = 4 nodes, E = 6 edges
   e5 [2, 3, 4]

   answer: 2   (delete e2 and e4)
```

Drawn as two separate sheets, one per player, over the same four dots:

```text
   Alice's sheet (types 1, 3)       Bob's sheet (types 2, 3)
   1 === 2 === 3                    1 === 2 === 3
   1 --- 3   (e2)                               :
   2 --- 4   (e3)                               4   (e5 3...4)
   1 --- 2   (e4)
```

## Do it by hand first

A person would start with the shared edges, because they are the bargains: one edge, two
players served. Draw `1 === 2` and `2 === 3` on both sheets. Now both players have
`{1, 2, 3}` connected and `4` alone.

Then patch each sheet separately. Alice: `1 - 3` is useless, she already has it.
`2 - 4` brings in node 4, keep it. `1 - 2` is useless. Bob: `3 ... 4` brings in 4, keep it.

```text
   kept: e0 e1 (shared), e3 (Alice), e5 (Bob)  = 4 edges
   deleted: e2, e4                             = 2 edges
```

What did your hand keep track of? Two separate notions of "who is connected to whom": one
for Alice, one for Bob. For every edge it asked, "does this join two blobs that were apart,
on the sheet(s) this edge can be drawn on?" That is two union-finds.

## The first honest attempt

Try every subset of edges to keep, smallest first; for each, run a BFS on Alice's edges and
a BFS on Bob's edges and check both reach all `n` nodes. The first subset that passes gives
the answer `E - size`.

There are `2^E` subsets, each checked in `O(n + E)`. With `E` up to `10^5`, this is not an
algorithm, it is a thought experiment.

Where is the waste? Most subsets are either clearly disconnected or clearly bloated. Look
at what the enumeration does with a redundant edge:

```text
   subsets containing {e0, e1, e3, e5}:
     {e0,e1,e3,e5}          valid, size 4
     {e0,e1,e3,e5,e2}       valid, size 5  <- e2 adds nothing
     {e0,e1,e3,e5,e4}       valid, size 5  <- e4 adds nothing
     {e0,e1,e3,e5,e2,e4}    valid, size 6
   each is checked with two full BFS runs, yet whether an
   edge is "needed" depends only on whether it joins two
   different blobs -- a local, one-edge question.
```

That local question is exactly what Kruskal's idea from Redundant Connection exploited: an
edge whose endpoints are already connected is redundant; an edge that joins two components
is needed.

## The turning point

**Claim: process all type-3 edges first, keeping each one that joins two components;
then, separately for each player, keep each type-1 or type-2 edge that still joins two
components. The kept edges are a minimum set.**

Two ideas hide in that claim.

**Idea 1: one player alone is a spanning-tree question.** A connected graph on `n` nodes
needs exactly `n - 1` edges to stay connected, and union-find picks them greedily: walk
the edges, keep an edge iff its endpoints have different roots. That is Redundant
Connection run to completion.

**Idea 2: shared edges first.** Count the kept edges. Alice keeps a tree `T_A` of `n - 1`
edges, Bob keeps a tree `T_B` of `n - 1` edges, and the total kept is

```text
   |T_A  union  T_B| = (n - 1) + (n - 1) - |T_A  inter  T_B|
                                            ^^^^^^^^^^^^^^^^
                         shared edges: type 3, counted once
```

So minimising what we keep is the same as **maximising the number of type-3 edges that
both trees use**. The shared edges form a forest inside the type-3 graph (they belong to a
tree, so they cannot contain a cycle). If the type-3 edges alone split the nodes into `c3`
components, no forest of type-3 edges has more than `n - c3` edges. Processing type-3
edges first, keeping those that join components, reaches exactly `n - c3`. Then each
player's tree is completed with their own edges, which is always possible if that player's
full graph is connected (any forest inside a connected graph extends to a spanning tree).

If instead you took a type-1 edge first, it might connect the same two nodes a type-3 edge
would have connected later; then that type-3 edge becomes redundant for Alice and you would
have to keep it only for Bob, paying two edges where one would do:

```text
   order 1-then-3 on pair 1-2:     order 3-then-1:
   [1,1,2] kept (Alice)            [3,1,2] kept (both)
   [3,1,2] Alice: redundant        [1,1,2] Alice: redundant
           Bob: needs it, kept
   cost: 2 edges                   cost: 1 edge
```

**Turning it into an algorithm.** Two parent arrays, `alice` and `bob`. For each type-3
edge, try the union in `alice`; if it succeeds, also union in `bob` and count one kept edge.
The `bob` union is guaranteed to succeed too, because up to this point both forests have
seen exactly the same edges (only type 3), so they have the same components. Then a second
pass: a type-1 edge is kept if it unions in `alice`, a type-2 edge if it unions in `bob`.
Finally, if either forest has more than one root among `1..n`, return `-1`; otherwise return
`E - kept`.

## Watch it work

The solution's union sets `parent[root_b] = root_a`, so the first endpoint's root wins.
Both arrays are indexed `1..4` (index 0 unused).

```text
Frame 1   pass 1, e0 [3,1,2]
   node    1  2  3  4
   alice   1  1  3  4         union ok -> also bob
   bob     1  1  3  4         kept = 1
```
The first shared edge joins 1 and 2 on both sheets.

```text
Frame 2   pass 1, e1 [3,2,3]
   node    1  2  3  4
   alice   1  1  1  4         find(2)=1, 3 -> under 1
   bob     1  1  1  4         kept = 2
```
Type-3 edges are done; both forests are `{1,2,3}` and `{4}`, identical as promised.

```text
Frame 3   pass 2, e2 [1,1,3]   e3 [1,2,4]
   e2: find(1)=1 find(3)=1   redundant, not kept
   e3: find(2)=1 find(4)=4   union ok
   node    1  2  3  4
   alice   1  1  1  1         kept = 3
   bob     1  1  1  4
```
Alice reaches 4 through her own edge; Bob is untouched.

```text
Frame 4   pass 2, e4 [1,1,2]   e5 [2,3,4]
   e4: alice find(1)=find(2)=1   redundant
   e5: bob find(3)=1 find(4)=4   union ok
   node    1  2  3  4
   alice   1  1  1  1
   bob     1  1  1  1         kept = 4
```
Bob reaches 4 with his only private edge.

```text
Frame 5   final check
   alice roots over 1..4: {1}   connected
   bob   roots over 1..4: {1}   connected
   answer = E - kept = 6 - 4 = 2
```
Both sheets are single trees with `n - 1 = 3` edges each, sharing 2.

Invariant across the frames: each forest's components are exactly the components of the
kept edges that player can use, and every kept edge reduced at least one forest's
component count by one. Nothing was kept that did not earn its place.

## Why it is correct

**Feasibility.** If a player's full graph is connected, the greedy pass for that player
ends with one root: an edge between two different components is always taken, so the
forest's components match the components of all that player's edges. If either forest has
two roots at the end, that player's full graph is disconnected and no deletion can help,
so `-1` is right.

**Optimality.** Any valid kept set contains a spanning tree for each player, and a minimum
kept set is exactly `T_A union T_B`. Its size is `2(n - 1) - s`, where `s` counts edges in
both trees; those are type 3 and acyclic, so `s <= n - c3`. The greedy keeps exactly
`n - c3` type-3 edges (pass 1 is Kruskal on the type-3 graph), all used by both players,
and then each player adds exactly the edges needed to reach `n - 1`. So the greedy keeps
`2(n - 1) - (n - c3)` edges, matching the lower bound. Fewer is impossible, so `E - kept`
is the maximum number of deletions.

## Cost

- **Time `O(E * alpha(n))`**: two passes over the edges, each edge doing at most two unions,
  and the final root check is `O(n)`.
- **Space `O(n)`**: two parent arrays of size `n + 1`.
- **Brute force** was `O(2^E * (n + E))`; the greedy replaces enumeration with a local
  "does this edge join two blobs?" test.

## Variations you will meet

- **Three or more players with overlapping edge types.** The neat `n - c3` bound relies on
  one fully shared type; with arbitrary subsets of players per edge, process edges in
  decreasing number of players served, but optimality is no longer guaranteed in general
  (it becomes a matroid intersection problem).
- **Weighted edges, minimise total kept weight.** Run Kruskal per player but sort by
  weight; shared edges are no longer automatically first, since a cheap private edge can
  beat an expensive shared one. Comparing costs `w3` against `w1 + w2` becomes the core.
- **Only Alice matters.** It collapses to "number of redundant edges in a connected graph",
  which is `E - (n - 1)`, or Redundant Connection extended to count all extras.
- **Return which edges to delete.** Record the indices that failed to union; those are the
  deletions.

## What to carry forward

Two union-finds can share one edge stream; give the edges that serve both first pick,
because each one saves an edge on both sheets. The next problem leaves union-find behind:
edges now have travel times, and "connected" becomes "how long until the signal arrives",
which needs Dijkstra and a min-heap.
