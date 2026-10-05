# Graph Valid Tree
*LeetCode 261 · Medium · Pattern: Union-Find (disjoint set union) · Reading time ~9 min*

## The problem

Given n nodes labelled 0..n-1 and a list of undirected edges, return true iff the edges form a valid tree: the graph
is connected and has no cycle.

```text
Example: n=5, [[0,1],[0,2],[0,3],[1,4]] -> true; n=5,
  [[0,1],[1,2],[2,3],[1,3],[1,4]] -> false because 1-2-3-1 is a
  cycle.
```

## What the problem is really asking

You get `n` nodes `0..n-1` and a list of undirected edges. Say yes if the edges form a tree.
A tree here means one connected piece with no cycle. There is no root and no direction.

The answer is a boolean, but it hides two separate checks. **Connected**: every node can
reach every other node. **Acyclic**: no edge is wasted on a loop. A graph can fail either
check alone, so the hard part is checking both without walking the graph over and over.

```text
  n = 5, edges = [[0,1],[2,3],[1,3],[3,4]]     -> true

     0 --- 1          drawn as a shape:   0
           |                              |
     2 --- 3 --- 4                        1
                                          |
  4 edges, 5 nodes, no loop               3
                                         / \
                                        2   4
```

## Do it by hand first

Draw five dots. Add the edges one by one, and before each one ask: "can I already get from
one end to the other?"

```text
  edge   already connected?   pieces after
  0-1    no                   {0,1} {2} {3} {4}
  2-3    no                   {0,1} {2,3} {4}
  1-3    no                   {0,1,2,3} {4}
  3-4    no                   {0,1,2,3,4}       one piece
```

Every edge joined two different pieces, and we ended with one piece. Now try
`[[0,1],[1,2],[2,0],[3,4]]`. When you reach `2-0`, the answer to "already connected?" is
**yes**, because `2-1-0` already joins them. Adding the edge closes a triangle. Your hand
tracked the same thing as in the last problem, *which piece each node is in*. But now the
event that matters is the failed merge.

There is a second thing you can see by just counting. Each successful merge lowers the
number of pieces by one. Going from `n` pieces to 1 takes exactly `n - 1` successful merges.

## The first honest attempt

Build adjacency lists. Check connectivity with one DFS from node 0 and ask whether all `n`
nodes were reached. Then check acyclicity edge by edge: delete edge `u-v`, and test whether
`v` is still reachable from `u`. If it is, some other path joins them, so the edge sits on a
cycle.

```text
  test edge 0-1: remove it, DFS 0 ... walks the graph
  test edge 2-3: remove it, DFS 2 ... walks the graph
  test edge 1-3: remove it, DFS 1 ... walks the graph
  test edge 3-4: remove it, DFS 3 ... walks the graph
               ^ E full traversals, each O(V + E)
```

That is `O(E * (V + E))`. Each test re-walks nearly the same graph to rediscover
connectivity that the previous test already knew.

## The turning point

**Claim: a graph on `n` nodes is a tree exactly when it has `n - 1` edges and no edge joins
two nodes that are already connected.**

Here is the justification, as a counting argument. Start with `n` isolated nodes, which is
`n` pieces, and add the edges in any order. An edge either merges two pieces, so the count
drops by one, or it lands inside a piece and closes a cycle. A tree has no cycle, so every
one of its edges must be a merging edge. Ending at one piece takes exactly `n - 1` merges.
So a tree has exactly `n - 1` edges, all of them merges.

Now run it in reverse. If there are exactly `n - 1` edges and none of them fails to merge,
we did `n - 1` merges starting from `n` pieces, which leaves one piece. That is connected
and acyclic, so it is a tree. With `n - 1` edges, the two conditions are the **same
condition**, so we only need to check one of them.

That gives a two-line plan:

1. If `len(edges) != n - 1`, answer `false` straight away. Too few edges cannot connect
   everything. Too many must contain a cycle.
2. Feed the edges to the union-find from the previous problem. The moment `find(u) ==
   find(v)`, the edge closes a cycle, so answer `false`. If all the edges merge, answer
   `true`.

The union-find question "are these already in the same piece?" is *exactly* the cycle test.
It costs near-constant time instead of a full DFS.

## Watch it work

`n = 5`, `edges = [[0,1],[2,3],[1,3],[3,4]]`. There are 4 edges, which equals `n - 1`, so
we continue. The rank rules are the same as last time: on a tie the first endpoint's root
stays on top.

```text
Frame 1  edge 0-1: roots 0,1 differ -> 1 under 0
  index:  0 1 2 3 4        0   2   3   4
  parent: 0 0 2 3 4        |
  rank:   1 0 0 0 0        1
```
This is a real merge, so it is not a cycle. Four trees remain.

```text
Frame 2  edge 2-3: roots 2,3 differ -> 3 under 2
  index:  0 1 2 3 4        0   2   4
  parent: 0 0 2 2 4        |   |
  rank:   1 0 1 0 0        1   3
```
This is another merge. Two trees have height 1.

```text
Frame 3  edge 1-3: find(1)=0, find(3)=2, tie -> 2 under 0
  index:  0 1 2 3 4          0     4
  parent: 0 0 0 2 4         / \
  rank:   2 0 1 0 0        1   2
                               |
                               3
```
The roots differ, so this is a merge. Only node 4 is still outside.

```text
Frame 4  edge 3-4: find(3) halves 3->0, find(4)=4 -> 4 under 0
  index:  0 1 2 3 4          0
  parent: 0 0 0 0 0      / /   \ \
  rank:   2 0 1 0 0     1 2     3 4
  4 merges, 0 collisions  -> true
```
Path halving re-pointed 3 straight at 0. Rank 2 beats rank 0, so 4 hangs under 0. Everyone
now points at root 0.

Now compare the failing case, `n = 5`, `edges = [[0,1],[1,2],[2,0],[3,4]]`:

```text
Frame 5  after 0-1 and 1-2; now edge 2-0
  index:  0 1 2 3 4          0     3   4
  parent: 0 0 0 3 4         / \
  rank:   1 0 0 0 0        1   2
  find(2)=0 == find(0)=0  -> collision -> false
```
The edge `2-0` lands inside the tree rooted at 0, which closes the triangle `0-1-2`. We stop
immediately.

What stayed invariant: each tree in the forest is one connected piece of the edges read so
far, and no piece contains a cycle yet. A collision is the first moment that second fact
would break.

## Why it is correct

The edge-count gate is safe. A tree on `n` nodes always has `n - 1` edges, so rejecting any
other count never rejects a tree.

After the gate, we keep this invariant: before each edge, the forest's trees are the
components of the edges read so far, and those edges form a forest, meaning no cycle. If
the next edge's endpoints have different roots, adding it cannot create a cycle, because a
cycle needs a second path between `u` and `v`, and no path exists at all. So the invariant
holds after the union. If they share a root, a path `u ... v` already exists, and the edge
completes a cycle. A tree has no cycles, so `false` is correct. If we reach the end, we did
`n - 1` merges from `n` pieces, so there is one component with no cycle: a tree.

## Cost

- Time `O(n * alpha(n))`. The gate guarantees at most `n - 1` edges, and each costs two
  finds and maybe one link.
- Space `O(n)`, for the `parent` and `rank` arrays.
- Without the gate you would need a final check that `count == 1` to catch a forest with
  too few edges. The asymptotic cost is the same, but there is more to get wrong.

## Variations you will meet

- **DFS version.** Do a DFS from node 0 and track the parent you came from. Meeting a visited
  node that is not your parent means a cycle. Then check that all `n` nodes were seen. This
  is the same cost, with adjacency lists.
- **Is this a forest?** Drop the `n - 1` gate and only reject on a collision. The number of
  trees is `n - len(edges)`.
- **Directed "is this a rooted tree?"** Here you also need in-degrees: exactly one node with
  in-degree 0, every other node with exactly 1. Redundant Connection II, two problems ahead,
  lives here.
- **Edge cases.** `n = 1` with no edges is a tree. A self-loop `[a, a]` shows up as a
  collision on its own.

## What to carry forward

A tree is `n - 1` edges and zero collisions. In union-find, a failed union *is* a cycle. The
next problem, Redundant Connection, stops asking yes or no and asks *which* edge collided.
