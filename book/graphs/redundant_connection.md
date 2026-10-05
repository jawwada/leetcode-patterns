# Redundant Connection
*LeetCode 684 · Medium · Pattern: Union-Find (disjoint set union) · Reading time ~9 min*

## The problem

A tree with n nodes labelled 1..n had one extra edge added, so the input has n edges. Return the edge that can be
removed to make it a tree again; if several work, return the one that appears last in the input.

```text
Example: [[1,2],[1,3],[2,3]] -> [2,3];
  [[1,2],[2,3],[3,4],[1,4],[1,5]] -> [1,4].
```

## What the problem is really asking

Someone had a tree on nodes `1..n` and added one extra undirected edge, so now there are `n`
edges and exactly one cycle. Hand back an edge whose removal turns the graph into a tree
again. Several edges will work: any edge on the cycle does. If so, return the one that
appears **last** in the input.

The answer is one edge. The hard part is the tie-break. Finding *a* cycle edge is easy. The
real question is how to land on the last cycle edge in input order without first listing
the whole cycle.

```text
  edges = [[3,4],[1,2],[2,4],[3,5],[2,5]]

      1                     cycle: 2-4-3-5-2
      |                     cycle edges in input order:
      2 ------ 4              [3,4] #0, [2,4] #2,
      |        |              [3,5] #3, [2,5] #4
      5 ------ 3            last one: [2,5]   <- answer
```

## Do it by hand first

Lay the edges down in input order, and keep a pencil mark of which nodes are already joined.

```text
  #  edge   ends already joined?   pieces
  0  3-4    no                     {3,4} {1} {2} {5}
  1  1-2    no                     {3,4} {1,2} {5}
  2  2-4    no                     {1,2,3,4} {5}
  3  3-5    no                     {1,2,3,4,5}
  4  2-5    YES -> this closes the loop
```

The first edge whose ends are already joined is `[2,5]`, and that is the answer. Your hand
kept exactly what it kept in the last two problems: *which piece each node is in*. The new
step is reporting the edge that hits a collision, instead of just reporting that one
happened.

But why is the *first* collision the *last* cycle edge in input order? That is worth
stopping on. It is the turning point.

## The first honest attempt

Process the edges in order. Before adding edge `u-v`, run a DFS over the edges added so far
and ask whether `v` is reachable from `u`. The first time it is, return the edge.

```text
  before #2 (2-4): DFS 2 over {3-4,1-2}   reaches {2,1}
  before #3 (3-5): DFS 3 over {..,2-4}    reaches {3,4,2,1}
  before #4 (2-5): DFS 2 over {..,3-5}    reaches {2,1,4,3,5}
                    ^ each walk re-explores the piece the
                      previous walk already explored
```

Each check is `O(n)` and there are up to `n` checks, so `O(n^2)`. The repeated work is
re-deriving connectivity. Pieces only ever grow, and we keep forgetting what we knew.

## The turning point

**Claim: processing edges in input order, the first edge whose endpoints are already
connected lies on the cycle and comes after every other cycle edge.**

Here is why. The graph is a tree plus one edge, so it has exactly one cycle `C`. Before any
edge of `C` is added, the edges seen so far are a subset of a tree, so none of them can
collide. While edges of `C` are being added, a collision happens only when an edge closes a
loop. The only loop available is `C` itself, and `C` closes only when its *last* edge
arrives. Every earlier edge of `C` joins two pieces that were still separate, because the
rest of the cycle was not there yet. So the single collision is exactly the last cycle edge
in input order. That is also the edge the problem asks for, because removing any cycle edge
leaves a tree, and the tie-break picks the latest.

So the algorithm is the one from Graph Valid Tree, but instead of returning `false` on a
collision, we return the edge that collided. Nodes are labelled `1..n`, so the parent array
has `n + 1` slots and slot 0 is never used.

## Watch it work

`edges = [[3,4],[1,2],[2,4],[3,5],[2,5]]`, `parent[i] = i`, every rank 0. On a rank tie the
root of `u` stays on top.

```text
Frame 1  #0 edge 3-4: roots 3,4, tie -> 4 under 3
  index:  1 2 3 4 5         1   2   3   5
  parent: 1 2 3 3 5                 |
  rank:   0 0 1 0 0                 4
```
Two singletons merge into one tree.

```text
Frame 2  #1 edge 1-2: roots 1,2, tie -> 2 under 1
  index:  1 2 3 4 5         1   3   5
  parent: 1 1 3 3 5         |   |
  rank:   1 0 1 0 0         2   4
```
This is a second pair. Now there are two trees of rank 1, plus node 5.

```text
Frame 3  #2 edge 2-4: find(2)=1, find(4)=3, tie -> 3 under 1
  index:  1 2 3 4 5           1       5
  parent: 1 1 1 3 5          / \
  rank:   2 0 1 0 0         2   3
                                |
                                4
```
The roots differ, so this is a merge. We linked roots 1 and 3, not nodes 2 and 4. The edge
in the graph and the arrow in the forest are different things.

```text
Frame 4  #3 edge 3-5: find(3)=1, find(5)=5 -> 5 under 1
  index:  1 2 3 4 5           1
  parent: 1 1 1 3 1          /|\
  rank:   2 0 1 0 0         2 3 5
                              |
                              4
```
Rank 2 beats rank 0. Every node is now in one tree, after four edges on five nodes. That is
a spanning tree.

```text
Frame 5  #4 edge 2-5: find(2)=1, find(5)=1
  same root -> collision -> return [2,5]
```
Both endpoints already hang under root 1, so this edge adds nothing but a loop.

What stayed invariant: before each edge, every tree in the forest is one connected piece of
the edges so far, and those edges contain no cycle. The first collision is the first moment
that a cycle exists.

## Why it is correct

Invariant: before processing edge `i`, the forest's trees are exactly the components of
edges `0..i-1`, and those edges are acyclic. A differing-root edge merges two components and
cannot form a cycle, so the invariant is kept. A same-root edge has a path between its ends
already, so it closes a cycle. The input has exactly one cycle, and the earlier edges were
acyclic, so this edge is the last-arriving edge of that cycle. Removing any edge of the
unique cycle gives back a tree, so every cycle edge is a valid answer. Among them, the
problem wants the latest in input order, and we just argued that it is this one. We never
need to look at the remaining edges.

## Cost

- Time `O(n * alpha(n))`. There is one pass, with two finds and maybe one link per edge.
- Space `O(n)`, for `parent` and `rank` of size `n + 1`.
- The DFS-per-edge version is `O(n^2)` time, with the same `O(n)` space.

## Variations you will meet

- **Return the first cycle edge, or every cycle edge.** Find the collision edge `u-v`, then
  walk the tree path `u ... v` with a DFS or with parent pointers. The cycle is that path
  plus the edge.
- **More than one extra edge.** Then the first collision is not necessarily the answer to
  any "last" rule. You collect every collision edge, which is exactly the set of non-tree
  edges for this edge order. That is the skeleton of Kruskal's algorithm, which comes later
  in the chapter.
- **Directed edges.** A node can now get two parents without any cycle. Union-find alone can
  no longer tell which edge is wrong. That is the next problem.

## What to carry forward

In input order, the first union that fails is the last edge of the only cycle. Union-find
turns "which edge is redundant?" into "which `find` pair matched first?" The next problem,
Redundant Connection II, gives the edges a direction, so a second kind of fault appears: a
node with two parents.
