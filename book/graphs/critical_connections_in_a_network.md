# Critical Connections in a Network
*LeetCode 1192 · Hard · Pattern: Tarjan bridges (DFS low-link) · Reading time ~13 min*

## The problem

n servers 0..n-1 are joined by undirected connections forming a connected graph. A connection is critical if removing
it disconnects some pair of servers. Return all critical connections in any order.

```text
Example: n=4, connections=[[0,1],[1,2],[2,0],[1,3]] -> [[1,3]].
```

## What the problem is really asking

`n` servers are joined by undirected cables, and the whole network is connected. A cable is
**critical** if cutting it splits the network in two. Return every critical cable. In graph
terms these are the **bridges**: edges that lie on no cycle.

```text
  n = 6, connections:
  [0,1] [1,2] [2,0] [2,3] [3,4] [4,5] [5,3]

        0                     4
       / \                   / \
      1---2 --------------- 3---5

  stored as adjacency lists (order matters for the DFS)
    0: 1 2        3: 2 4 5
    1: 0 2        4: 3 5
    2: 1 0 3      5: 4 3

  answer: [[2,3]]  (each triangle survives any single cut;
                    the cable between them does not)
```

The answer is a list of edges. The test "does removing this edge disconnect the graph?" is
easy for one edge. What makes it hard is doing it for up to 10^5 edges without paying a full
traversal per edge.

## Do it by hand first

Look at a cable and ask: **is there another way around?** Cable `0-1`: yes, `0-2-1`. Cable
`3-4`: yes, `3-5-4`. Cable `2-3`: every route from the left triangle to the right one uses
it. An edge is safe exactly when it sits on a cycle.

```text
  0-1  on cycle 0-1-2       safe
  1-2  on cycle 0-1-2       safe
  2-0  on cycle 0-1-2       safe
  2-3  no cycle through it  CRITICAL
  3-4, 4-5, 5-3 on cycle 3-4-5  safe
```

By hand you spotted cycles by eye. The hand "kept track" of **loops that close back on
themselves**. To make a machine see loops cheaply, we need an order of exploration in which
every loop announces itself. Depth-first search provides exactly that.

## The first honest attempt

For each edge: delete it, run a BFS from node 0, and if fewer than `n` nodes are reached the
edge was a bridge.

```text
  delete 0-1: BFS visits 0 2 1 3 4 5   all 6, safe
  delete 1-2: BFS visits 0 1 2 3 4 5   all 6, safe
  delete 2-0: BFS visits 0 1 2 3 4 5   all 6, safe
  delete 2-3: BFS visits 0 1 2         only 3 -> bridge
  ...
  each BFS re-walks nearly the same graph, 7 times over
```

`E` traversals of `O(V + E)` each is `O(E(V + E))`, around 10^10 at the limits. The waste:
the answer to "is there a way around this edge?" is recomputed from nothing for each edge,
when a single exploration could record, for every region, how far back it can loop.

## The turning point

**Claim: run one DFS and number nodes by discovery time `disc`. For each node `v`, let
`low[v]` be the smallest `disc` reachable from `v`'s DFS subtree using tree edges downward
plus one back edge. Then the tree edge `u -> v` (u the parent) is a bridge exactly when
`low[v] > disc[u]`.**

That needs three ideas, built up from zero.

**1. The DFS tree.** Run DFS from node 0. The edges it walks to reach new nodes form a tree,
the **DFS tree**. Every other edge is a **back edge**. In an undirected graph a back edge
always joins a node to one of its **ancestors** in that tree: DFS finishes everything
reachable from a node before backing out, so an edge to an unrelated branch would have been
walked as a tree edge instead. No "cross edges" exist.

```text
  DFS tree (top-down by discovery), back edges as ropes

    0  disc 0  <---------.
    |                    |
    1  disc 1            |  back edge 2-0
    |                    |
    2  disc 2  ----------'
    |
    3  disc 3  <---------.
    |                    |
    4  disc 4            |  back edge 5-3
    |                    |
    5  disc 5  ----------'
```

**2. Cycles are back edges.** A back edge from a node up to an ancestor plus the tree path
between them is a cycle. So a tree edge lies on a cycle exactly when some back edge
**jumps over** it: starts inside the subtree below the edge and lands above it. Back edges
are never bridges themselves, because each one closes a cycle.

**3. `low` measures how high a subtree can jump.** Picture `low[v]` as the highest rope
anywhere in `v`'s subtree. Cut the tree edge `u - v`. The subtree of `v` stays attached only
if some rope from inside it lands at `u` or above, that is `low[v] <= disc[u]`. If
`low[v] > disc[u]`, nothing escapes, and `u - v` is a bridge.

`low` is computed bottom-up during the same DFS, as the recursion unwinds:

```python
disc[u] = low[u] = timer; timer += 1
for v in adj[u]:
    if v == parent: continue                  # not a back edge
    if disc[v] == -1:                         # tree edge
        dfs(v, u); low[u] = min(low[u], low[v])
        if low[v] > disc[u]: bridges.append([u, v])
    else: low[u] = min(low[u], disc[v])       # back edge
```

Two rules deserve a word. Skipping `parent` matters: the edge we just came down is in the
adjacency list too, and treating it as a back edge would let every subtree "reach" its
parent, so nothing would ever look like a bridge. And for a back edge we take `disc[v]`, not
`low[v]`: one rope lands at `v`, and that is all the edge itself proves.

## Watch it work

`disc` and `low` arrays are shown as `node:disc/low`; `-` means unvisited.

```text
Frame 1  dfs(0) -> dfs(1) -> dfs(2)
  0:0/0  1:1/1  2:2/2  3:-  4:-  5:-
  call stack: 0 > 1 > 2
```
Each new node gets the next timer value as both `disc` and its starting `low`.

```text
Frame 2  at 2: neighbour 1 is the parent, skip;
         neighbour 0 is visited -> back edge
  low[2] = min(2, disc[0]=0) = 0
  0:0/0  1:1/1  2:2/0
```
Node 2 holds a rope to the very top of the tree.

```text
Frame 3  at 2: neighbour 3 unvisited -> dfs(3)
         -> dfs(4) -> dfs(5)
  0:0/0  1:1/1  2:2/0  3:3/3  4:4/4  5:5/5
  call stack: 0 > 1 > 2 > 3 > 4 > 5
```
The DFS dives into the second triangle along tree edges.

```text
Frame 4  at 5: neighbour 4 is the parent, skip;
         neighbour 3 visited -> back edge
  low[5] = min(5, disc[3]=3) = 3
  return to 4: low[4] = min(4, low[5]=3) = 3
  test low[5]=3 > disc[4]=4 ?  no -> 4-5 safe
  3:3/3  4:4/3  5:5/3
```
The rope from 5 to 3 jumps over edge 4-5, and `low` carries that news up to 4.

```text
Frame 5  return to 3: low[3] = min(3, low[4]=3) = 3
  test low[4]=3 > disc[3]=3 ?  no -> 3-4 safe
  3 sees 5 again (already visited):
  low[3] = min(3, disc[5]=5) = 3, unchanged
```
The same back edge seen from the ancestor's end changes nothing, as it should.

```text
Frame 6  return to 2:
  test low[3]=3 > disc[2]=2 ?  YES -> bridge [2,3]
  low[2] = min(0, 3) = 0
  0:0/0  1:1/1  2:2/0  3:3/3  4:4/3  5:5/3
```
The best rope in 3's whole subtree reaches only 3 itself, below node 2, so nothing jumps over 2-3.

```text
Frame 7  return to 1, then 0
  at 1: low[1] = min(1, 0) = 0; 0 > 1? no -> safe
  at 0: low[1]=0 > disc[0]=0? no -> safe
        0 sees 2 again: min(0, 2) = 0
  final low: [0, 0, 0, 3, 3, 3]   bridges [[2,3]]
```
The left triangle's rope from 2 to 0 covers both 0-1 and 1-2.

Invariant across frames: when `dfs(v)` returns, `low[v]` is final, the highest any rope from
`v`'s subtree can reach. Every bridge test happened exactly then, at the parent, once per
tree edge.

## Why it is correct

**`low` is right.** By induction on the recursion: when `dfs(v)` returns, every node in
`v`'s subtree has been visited and every back edge leaving the subtree has been looked at
from its lower end, where it lowered that node's `low` to the ancestor's `disc`. Each child
passes its own minimum upward. So `low[v]` is the smallest `disc` hit by any back edge from
the subtree (or `disc[v]` if none).

**The test is right.** Removing tree edge `u - v` separates `v`'s subtree from the rest
unless some other edge connects them. Tree edges cannot (the subtree's only tree link
upward is `u - v`), and there are no cross edges, so only a back edge from the subtree to a
proper ancestor of `v`, which means `u` or above, can. Such a back edge exists iff
`low[v] <= disc[u]`. Non-tree edges are never bridges because each lies on a cycle.

The graph is connected, so a single `dfs(0)` reaches every edge.

## Cost

- **Time `O(V + E)`**: one DFS; each adjacency entry is looked at once, with `O(1)` work.
- **Space `O(V + E)`**: adjacency lists, `disc` and `low`, and recursion depth up to `V`.

On a long chain the recursion is `10^5` deep; the solution raises Python's limit. An
iterative DFS with an explicit stack of `(node, parent, next-neighbour index)` avoids it.

## Variations you will meet

- **Articulation points (cut vertices).** Same `disc`/`low`. A non-root `u` is a cut vertex
  if some child has `low[v] >= disc[u]` (`>=`, since reaching `u` itself is not enough to
  survive losing `u`); the root is one if it has two or more DFS children.
- **Parallel edges.** Two cables between the same pair form a cycle, so neither is a bridge.
  Skipping by parent **node** would wrongly skip both; skip by the **edge id** you came down.
- **2-edge-connected components.** Delete the bridges; what remains splits into the
  components, and they form a tree joined by the bridges.
- **Strongly connected components (Tarjan's SCC).** The directed cousin: the same
  `disc`/`low` plus a stack of active nodes; a node with `low == disc` roots a component.

## What to carry forward

A DFS tree has only tree edges and back edges, and `low[v]` records how high `v`'s subtree
can reach by a back edge; a tree edge is a bridge exactly when its child cannot reach above
it, all in one `O(V + E)` pass.

This problem closes the chapter. You can now flood a grid and count or measure its regions;
run BFS from one source or from many at once and read distances off the layers; search over
implicit graphs whose nodes are words, boards, bitmasks or (position, keys) states; order
tasks with topological sort and detect cycles with colours or in-degrees; merge sets with
union-find, online and offline; find shortest paths with Dijkstra, with 0-1 BFS when weights
are 0 or 1, with a `max` instead of a `+` for bottlenecks, and on a reversed graph when many
sources share one target; build minimum spanning trees with Prim or Kruskal and argue them
with the cut property; and find every indispensable edge with one low-link DFS. Faced with a
new graph problem, ask what the nodes are, what an edge costs, and whether the question is
about reaching, ordering, grouping, cheapest routes, cheapest connection or fragility, and
one of these tools will fit.
