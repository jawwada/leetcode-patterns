# Graphs

*45 problems · Reading time ~25 min*

## Why this chapter exists

A graph is the shape of any question about *things and the connections between them*. Cells of a map that touch, words
one letter apart, courses that require other courses, people who met, airports joined by tickets, servers joined by
cables. Once you see the things as nodes and the connections as edges, a surprisingly small set of algorithms answers
almost everything you will be asked.

The forty-five problems fall into families, and the chapter walks them in this order:

- **Grid flood fill.** The grid is the graph; a traversal paints one connected region (flood fill, islands, island area).
- **Flood from the border.** Reverse the question and start from the edge of the map instead of from each cell
  (enclaves, surrounded regions, Pacific/Atlantic).
- **Multi-source BFS.** Many starting points expand at once and each wave is one unit of distance (rotting oranges,
  0-1 matrix, walls and gates).
- **Traversal with a map.** Copy a graph while walking it (clone graph).
- **BFS on implicit graphs.** Nodes are words, boards, routes or indices that you generate on the fly (word ladder I
  and II, sliding puzzle, bus routes, jump game IV, k-similar strings).
- **BFS on augmented states.** A node is "position plus what I carry": eliminations left, keys held, nodes seen, where
  the box is (obstacle elimination, all keys, visiting all nodes, box pushing).
- **Directed graphs and ordering.** Degrees, topological sort, cycle detection, longest path in a DAG, Euler paths (town
  judge, course schedule I and II, alien dictionary, parallel courses III, sort items by groups, itinerary).
- **Union-find.** Merge components as edges arrive and ask "same component?" in near constant time (components, valid
  tree, redundant connection I and II, accounts merge, islands II, malware, common factor, secret, limited paths,
  removable edges).
- **Weighted shortest paths.** Dijkstra, 0-1 BFS and bottleneck paths (network delay, valid path in a grid, swim in
  rising water, weighted subgraph).
- **Spanning trees and bridges.** Cheapest way to connect everything, which edges every cheapest way needs, and which
  cables cannot fail (connect all points, critical MST edges, critical connections).

## What it is

A **graph** is a set of nodes (vertices) and a set of edges, each edge joining two nodes. Edges may be **undirected**
(friendship: works both ways) or **directed** (prerequisite: A before B). They may carry a **weight** (distance, cost,
time) or not. That is the whole definition. Everything else is about how you store it and how you walk it.

Here is one small undirected graph that the rest of this section reuses, drawn as a picture:

```text
     0 ------- 1
     |         |
     |         |
     2 ------- 3 ------- 4
     |
     5

  6 nodes, 6 edges: 0-1 0-2 1-3 2-3 3-4 2-5
```

### Four ways to store it

**1. Grid (implicit).** Many problems never hand you edges at all. They hand you a 2D array, and the rule "a cell is
joined to its up/down/left/right neighbour" defines the edges. You never build anything; you compute neighbours with
four offsets and a bounds check.

```text
  grid (3 x 3)            the graph hiding in it
  +---+---+---+
  | 1 | 1 | 0 |           (0,0)--(0,1)
  +---+---+---+                    |
  | 0 | 1 | 0 |                  (1,1)
  +---+---+---+
  | 1 | 0 | 1 |           (2,0)        (2,2)  alone
  +---+---+---+
  neighbours of (r,c): (r-1,c) (r+1,c) (r,c-1) (r,c+1)
  keep one only if inside the grid and land
```

Use it when the input is a board, map, image or maze. Cost: zero extra memory; m*n nodes, at most 4 edges each.

**2. Adjacency list.** For each node, a list of its neighbours. In Python, a list of lists or a `defaultdict(list)`.

```text
  adj[0] -> [1, 2]
  adj[1] -> [0, 3]
  adj[2] -> [0, 3, 5]
  adj[3] -> [1, 2, 4]
  adj[4] -> [3]
  adj[5] -> [2]
  memory: V slots + 2E entries (each undirected edge twice)
```

This is the default. Traversals ask "who are my neighbours?" and the list answers in time proportional to the answer.
Use it for anything sparse, which is nearly every interview graph.

**3. Adjacency matrix.** A V x V table, `M[u][v] = 1` (or the weight) when the edge exists.

```text
        0  1  2  3  4  5
    0   .  1  1  .  .  .
    1   1  .  .  1  .  .
    2   1  .  .  1  .  1
    3   .  1  1  .  1  .
    4   .  .  .  1  .  .
    5   .  .  1  .  .  .
  memory: V*V cells, mostly empty; symmetric if undirected
```

Use it when V is small (a few hundred), when the input already is one (some problems give `isConnected[i][j]`), or
when you need "is u joined to v?" in O(1). Listing neighbours costs O(V) per node even if there are none.

**4. Edge list.** Just the edges, often with weights: `[(0,1), (0,2), (1,3), (2,3), (3,4), (2,5)]`.

```text
  i :  0     1     2     3     4     5
      (0,1) (0,2) (1,3) (2,3) (3,4) (2,5)
  no way to ask "neighbours of 3" without scanning all E
```

This is how most problems *give* you the graph. Keep it as-is when the algorithm consumes edges one at a time:
union-find, Kruskal (sort the list by weight), offline queries. Otherwise convert it to an adjacency list in one pass.

### Walking it: DFS and BFS

Every traversal keeps two things: a **container** of discovered-but-not-yet-expanded nodes (the frontier), and a
**visited set** of nodes already discovered. The only difference between depth-first and breadth-first search is the
container. A stack takes the newest node next; a queue takes the oldest.

Both runs below start at node 0, mark a node visited when it is pushed, and push neighbours in list order.

```text
  BFS (queue, popleft)            DFS (stack, pop)
  pop  queue after                pop  stack after
  0    [1, 2]                     0    [1, 2]
  1    [2, 3]                     2    [1, 3, 5]
  2    [3, 5]                     5    [1, 3]
  3    [5, 4]                     3    [1, 4]
  5    [4]                        4    [1]
  4    []                         1    []
  order 0 1 2 3 5 4               order 0 2 5 3 4 1
```

BFS spreads out in rings. DFS dives down one branch (0, 2, 5), backs up, and dives again. Both see every reachable node
exactly once. DFS is the natural fit for "explore everything and summarise" (sizes, cycles, post-order). BFS is the fit
for anything that says "fewest" or "nearest", because of the next property.

### BFS layers are distances

BFS pops nodes in order of their distance from the start. Draw the same run as rings:

```text
  layer 0:  0
  layer 1:  1   2            (one edge from 0)
  layer 2:  3   5            (two edges)
  layer 3:  4                (three edges)

        0          queue at any moment holds at most
       / \         two adjacent layers: [ ...d..., ...d+1... ]
      1   2
       \ / \
        3   5
        |
        4
```

When node 3 is first discovered it is from node 1, at layer 2. No later discovery could be shorter, because everything
in the queue behind it is at least as far. So **the first time BFS touches a node, it has found a shortest path to it**
(unweighted edges). Most shortest-path problems in this chapter are that sentence.

### Why the visited set

Without it, 0 pushes 1, 1 pushes 0, 0 pushes 1 again, forever. Undirected graphs always have these two-way edges, and
any cycle traps an unmarked walk. The visited set guarantees each node enters the container once, which is what makes
the cost O(V + E).

Mark on **push**, not on pop. If you mark on pop, node 3 can be pushed by both 1 and 2 before either copy is popped,
and in a dense graph the queue swells with duplicates. On grids you often skip the set entirely and mark the grid
itself (sink `'1'` to `'0'`, paint the pixel, write the distance). The grid is the visited set.

### Multi-source BFS

Put several starts in the queue at layer 0. BFS then computes, for every node, the distance to the *nearest* start, in
one pass. It is as if a single invisible super-node were joined to every start by an edge.

```text
  S = sources (rotten oranges, zeros, gates)
  . . . S        2 2 1 0        each number = layer at
  . . . .   ->   1 2 2 1        which the wave arrived
  S . . .        0 1 2 2        = distance to nearest S
```

### Implicit graphs

Sometimes nobody gives you the graph because it is too big to list. You get a rule instead. Nodes are words and edges
join words differing by one letter; nodes are board configurations and edges are legal moves; nodes are
`(row, col, keys_held)` and edges are steps. You never build the adjacency list. You write a function `neighbours(state)`
and run BFS with a visited set of states.

```text
  "hit" -> "hot" -> "dot" -> "dog" -> "cog"
            |                  ^
            +----> "lot" ---> "log"
  state = a string; neighbours = all one-letter edits
  that are in the dictionary
```

The skill is choosing what a node *is*. If "the same cell" can behave differently depending on what you carry (keys,
budget, which nodes you have seen), then the cell is not the node; the cell plus what you carry is.

### Directed graphs

Edges now have direction. The **in-degree** of a node is how many edges point into it; the **out-degree** is how many
leave it. A directed graph with no cycle is a DAG, and every DAG has a **topological order**: a line-up of the nodes in
which every edge points rightward.

## Operations and what they cost

V nodes, E edges.

| Operation | Time | Why |
|---|---|---|
| Build adjacency list from edge list | O(V + E) | one append per edge end |
| DFS / BFS of whole graph | O(V + E) | each node pushed once, each edge looked at once or twice |
| Grid flood fill | O(m n) | each cell pushed once, 4 neighbour checks |
| Multi-source BFS | O(V + E) | still one push per node, sources just start in layer 0 |
| Topological sort (Kahn) | O(V + E) | each node dequeued once, each edge decrements once |
| Union-find `find` / `union` | ~O(1) amortised | path compression + union by size: inverse-Ackermann |
| Dijkstra with binary heap | O((V + E) log V) | each edge may push one heap entry |
| 0-1 BFS with deque | O(V + E) | deque front/back pushes are O(1) |
| Kruskal MST | O(E log E) | sorting edges dominates |
| Prim MST (heap) | O(E log V) | like Dijkstra, keyed on single edge weight |
| Bridges (Tarjan low-link) | O(V + E) | one DFS |

### Kahn's algorithm: topological sort and cycle detection

Repeatedly take a node with in-degree 0 (nothing left must come before it), output it, and delete its outgoing edges,
which lowers its neighbours' in-degrees.

```text
  DAG:  0 -> 1 -> 3 -> 4         edges 0->1 0->2 1->3
        0 -> 2 -> 3                    2->3 3->4

  Frame  pop  indeg [0 1 2 3 4]   queue
  start   -    [0,1,1,2,1]        [0]
  1       0    [0,0,0,2,1]        [1,2]
  2       1    [0,0,0,1,1]        [2]
  3       2    [0,0,0,0,1]        [3]
  4       3    [0,0,0,0,0]        [4]
  5       4    [0,0,0,0,0]        []
  order: 0 1 2 3 4   (5 of 5 output -> no cycle)
```

Add one edge `4 -> 1` and the run stalls:

```text
  indeg start [0,2,1,2,1]   queue [0]
  pop 0 ->    [0,1,0,2,1]   queue [2]
  pop 2 ->    [0,1,0,1,1]   queue []      stuck
  output 2 of 5. Nodes 1,3,4 sit on the cycle 1->3->4->1:
  each waits for another, so none ever reaches in-degree 0.
```

If fewer than V nodes come out, there is a cycle. That single count answers "can all courses be finished?".

### Union-find: a parent forest

Union-find (disjoint set union, DSU) keeps one array, `parent`. Each component is a tree; its root is its name.
`find(x)` walks up to the root. `union(a, b)` hangs one root under the other. Path compression makes every node on a
`find` path point straight at the root afterwards.

```text
  start      parent = [0,1,2,3,4,5]   six one-node trees
  union(0,1) parent = [1,1,2,3,4,5]   0 -> 1
  union(2,3) parent = [1,1,3,3,4,5]   2 -> 3
  union(1,3) parent = [1,3,3,3,4,5]   1 -> 3
  union(4,5) parent = [1,3,3,3,5,5]   4 -> 5

  forest now:           3            5
                       / \           |
                      1   2          4
                      |
                      0
  find(0): 0 -> 1 -> 3   root 3; compress: parent[0] = 3
  parent = [3,3,3,3,5,5]
                        3            5
                      / | \          |
                     1  2  0         4
```

`union` returns False when both ends already share a root. That is the cycle detector for undirected graphs: the edge
that fails to union is the edge that closes a loop.

### Dijkstra: the heap replaces the queue

With weights, the node popped next must be the one with the smallest tentative distance, so a min-heap replaces the
queue. Push `(dist, node)`; when you pop, skip it if it is stale (a better distance was recorded since).

```text
  A --4--> B --1--> D
  A --1--> C --2--> B
           C --5--> D

  pop     heap after                 dist A B C D
  (0,A)   [(1,C),(4,B)]                   0 4 1 -
  (1,C)   [(3,B),(4,B),(6,D)]             0 3 1 6
  (3,B)   [(4,B),(6,D),(4,D)]             0 3 1 4
  (4,B)   stale (4 > 3), skip
  (4,D)   [(6,D)]                         0 3 1 4
  (6,D)   stale, skip.  final: A0 B3 C1 D4
```

When a node is popped (not stale) its distance is final: every other path to it would have to leave the settled region
through an edge to something already at least as far, and weights are non-negative. Negative weights break this.

### 0-1 BFS: a deque when weights are only 0 or 1

If every edge costs 0 or 1, keep a deque. A 0-edge leads to a node at the *same* distance: push it on the front. A
1-edge leads one further: push on the back. The deque stays sorted by distance without a heap.

```text
  popped u at distance d
  0-edge to v:  appendleft  ->  [ v(d) | ...d... | ...d+1... ]
  1-edge to w:  append      ->  [ ...d... | ...d+1... | w(d+1) ]
```

### Minimum spanning tree: Kruskal and Prim

A spanning tree connects all V nodes with V-1 edges. The minimum one has the least total weight. **Kruskal**: sort the
edges, take each one unless its ends are already connected (a union-find check). **Prim**: grow one tree from any node,
always adding the cheapest edge leaving it (a heap, like Dijkstra keyed on the edge alone).

```text
  edges sorted: A-B 1, B-C 2, A-C 3, C-D 4, B-D 5
  A-B 1  take   {A,B} {C} {D}
  B-C 2  take   {A,B,C} {D}
  A-C 3  skip   A and C share a root: would close a cycle
  C-D 4  take   {A,B,C,D}   3 edges = V-1, stop. cost 7
```

Both rest on the **cut property**: the cheapest edge crossing any split of the nodes into two sides belongs to some
MST.

### Bridges: the low-link

A bridge is an edge whose removal disconnects the graph. Run DFS, give each node a discovery time `disc`, and compute
`low[u]`: the smallest `disc` reachable from u's subtree using at most one edge that goes back up (not the edge to the
parent). Tree edge `u - v` is a bridge exactly when `low[v] > disc[u]`: v's subtree has no way back to u or above.

```text
  0 --- 1 --- 3 --- 4        edges 0-1 1-2 2-0 1-3 3-4
   \   /
    \ /
     2
  DFS 0 -> 1 -> 2, then back edge 2-0
  node : 0 1 2 3 4
  disc : 0 1 2 3 4
  low  : 0 0 0 3 4
  1-3: low[3]=3 > disc[1]=1  bridge
  3-4: low[4]=4 > disc[3]=3  bridge
  1-2: low[2]=0 <= disc[1]   not (triangle gives a way back)
```

## The invariant

Every algorithm in this chapter protects one sentence: **a node is discovered at most once, and when it is
discovered (BFS) or settled (Dijkstra, 0-1 BFS), the answer recorded for it is already final.**

For flood fill, "final" means "belongs to this component". For BFS it means "this is the shortest distance". For
Dijkstra, "popped and not stale" is final. For Kahn, a node is output only once nothing can still come before it. For
union-find the parallel invariant is that two nodes have the same root exactly when they are connected by the edges
seen so far.

A legal and an illegal BFS state, start S, unit edges:

```text
  legal: queue holds layers d and d+1 only, in that order
     visited/dist:  S=0  a=1  b=1  c=2
     queue:         [ b(1), c(2) ]

  illegal: a node was enqueued twice (marked on pop)
     queue:         [ b(1), c(2), c(2) ]
     c will be expanded twice: work doubles, and a
     counter like "area += 1" on pop counts c twice.

  illegal: queue out of order (a 1-edge pushed to front)
     queue:         [ d(3), b(1) ]
     d is popped and "finalised" before b, so a path
     through b that reaches d in 2 is never recorded.
```

## How to picture it

Picture BFS as a **wave front**: a ring of water spreading from the sources, one ring per time step. The queue is the
wet edge of the wave; everything behind it is soaked (visited), everything ahead is dry. Multi-source BFS is several
pebbles dropped into a pond at once, and each cell is claimed by whichever ripple arrives first.

Picture DFS as **a person in a maze with chalk**: walk forward as long as you can, chalk each junction, and when every
way forward is chalked, back up. The stack is the path back to the entrance.

Picture topological sort as **peeling layers off an onion from the outside**: whatever has nothing in front of it peels
off now. Picture union-find as **a forest of short trees** whose roots are the component names; merging plants one tree
under another's root. Picture Dijkstra as the same wave as BFS, except that the ground is uneven and the wave moves
slower over expensive edges; the heap tells you which part of the shore gets wet next.

## Signals in a problem statement

- A **grid** of land/water, colours, walls; "connected 4-directionally" -> flood fill (DFS or BFS, either works).
- "Can reach the border / escape / drain to the ocean" -> flood from the border instead of from every cell.
- "Minimum number of steps / moves / minutes / transformations", unit cost -> BFS. "All of them spread at once" ->
  multi-source BFS.
- "Return all shortest sequences" -> BFS that records parents per layer, then backtrack.
- A state that is not a cell (a string, a board, a set of keys) and a small state count -> BFS over states.
- "Prerequisites", "must come before", "order of letters", "dependencies" -> directed graph, Kahn's algorithm.
- "Is it possible to finish / is there a cycle" -> Kahn count, or three-colour DFS.
- "Use every ticket / edge exactly once" -> Eulerian path (Hierholzer).
- "Groups", "merge", "same set", edges arriving one at a time, "after each addition" -> union-find.
- "Which edge to remove so that it becomes a tree" -> union-find, first failing union.
- Weights, "cheapest", "minimum time", "delay" -> Dijkstra. Weights only 0/1 -> 0-1 BFS.
- "Minimise the maximum along the path" -> bottleneck Dijkstra, or binary search plus BFS.
- "Connect all points at minimum cost" -> MST (Prim for dense, Kruskal for an edge list).
- "Critical connection", "single point of failure" -> bridges / articulation points.

Counter-signals: a strict left-to-right dependency on an array often wants DP, not a graph. Negative edge weights rule
out Dijkstra (Bellman-Ford). "Longest simple path" in a general graph is NP-hard; only on a DAG is it a DP over the
topological order. With n <= 12 or so and "visit all", expect a bitmask in the state.

**Which traversal for which question:**

| Question | Tool |
|---|---|
| Which cells/nodes are connected to X? | DFS or BFS, either |
| How many components? How big? | scan + flood, or union-find |
| Fewest unit steps from one source | BFS |
| Distance from the nearest of many sources | multi-source BFS |
| Fewest steps when state includes extras | BFS over (position, extras) |
| Order respecting "before" constraints | Kahn topological sort |
| Does a directed graph have a cycle? | Kahn count < V, or DFS colours |
| Connectivity as edges arrive / merge groups | union-find |
| Cheapest path, non-negative weights | Dijkstra |
| Cheapest path, weights 0 or 1 | 0-1 BFS |
| Path minimising its largest edge | bottleneck Dijkstra / Kruskal |
| Connect everything cheapest | MST (Kruskal / Prim) |
| Edges whose loss disconnects | Tarjan bridges (low-link) |

## Python toolbox

`collections.deque` is the queue: `popleft()` is O(1). A list's `pop(0)` is O(n) and quietly turns BFS quadratic.

```python
from collections import deque, defaultdict
import heapq

adj = defaultdict(list)
for u, v in edges:                 # undirected
    adj[u].append(v); adj[v].append(u)

q, seen = deque([src]), {src}      # BFS, mark on push
while q:
    for _ in range(len(q)):        # one layer per outer loop
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
```

`heapq` is a min-heap on a plain list. Push tuples `(dist, node)` so ordering is by distance. There is no decrease-key:
push a new entry and skip stale ones on pop.

```python
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path halving
        x = parent[x]
    return x
```

For grids, keep the four offsets in a tuple: `((1,0),(-1,0),(0,1),(0,-1))`. Python's default recursion limit is 1000,
so a recursive DFS over a 300 x 300 grid of land crashes; use an explicit stack or `sys.setrecursionlimit` with care.

## Mistakes people make

1. **Marking visited on pop.** Nodes get queued many times and counters double-count. Mark when you push.
2. **`list.pop(0)` as a queue.** O(n) per pop. Use `deque.popleft()`.
3. **Recursive DFS on a big grid.** RecursionError at depth 1000. Use an explicit stack.
4. **Forgetting the bounds check before indexing.** `grid[-1][c]` silently reads the last row in Python. Check
   `0 <= r < rows` first.
5. **Flood fill when old colour equals new colour.** Painting marks nothing, so it loops forever. Return early.
6. **Counting BFS layers wrong.** Snapshot `len(q)` before the inner loop, or store distance with each node.
7. **Dijkstra without the stale check.** An old, larger entry relaxes neighbours again. `if d > dist[u]: continue`.
8. **Building a directed edge the wrong way round.** `[a, b]` meaning "b before a" must become `b -> a`. Read the
   statement twice.
9. **Union-find without compression on long chains.** `find` becomes O(n). Compress, and union by size when it matters.
10. **Treating a cell as the node when extras matter.** If keys or budget change what is possible, visited must be
    keyed on `(cell, extras)`, or you will prune paths that were actually different.

## The journey ahead

1. **Flood fill**: the bare traversal; recolouring is the visited set.
2. **Number of islands**: scan plus flood; count how many floods you launch.
3. **Max area of island**: each flood returns a size.
4. **Number of enclaves**: flood from the border instead of from each cell.
5. **Surrounded regions**: border flood with a temporary sentinel, then a rewrite sweep.
6. **Pacific Atlantic water flow**: two border floods with a directed edge rule; intersect.
7. **Rotting oranges**: multi-source BFS counted layer by layer.
8. **0-1 matrix**: multi-source BFS writes distances.
9. **Walls and gates**: the same wave, written in place.
10. **Clone graph**: a real adjacency list and an old-to-new map.
11. **Word ladder**: an implicit graph of words with wildcard buckets.
12. **Word ladder II**: record a parents DAG during BFS, backtrack all shortest paths.
13. **Sliding puzzle**: board configurations as nodes.
14. **Bus routes**: choose routes, not stops, as nodes.
15. **Jump game IV**: clique edges consumed once.
16. **K-similar strings**: BFS with branching pruned to useful swaps.
17. **Obstacle elimination**: a budget joins the state.
18. **All keys**: a key bitmask joins the state.
19. **Visiting all nodes**: a visited bitmask joins the state, multi-source start.
20. **Box pushing**: free and paid moves, a first 0-1 BFS.
21. **Town judge**: in-degree minus out-degree, no traversal.
22. **Course schedule**: Kahn's algorithm detects cycles.
23. **Course schedule II**: Kahn's pop order is the answer.
24. **Alien dictionary**: build the edges yourself, then topo sort.
25. **Parallel courses III**: DP along the topological order.
26. **Sort items by groups**: topo sort at two levels.
27. **Reconstruct itinerary**: every edge once, Hierholzer.
28. **Connected components**: union-find counts merges.
29. **Graph valid tree**: n-1 edges and no failed union.
30. **Redundant connection**: the first failing union.
31. **Redundant connection II**: directed, two parents versus a cycle.
32. **Accounts merge**: union-find on string keys.
33. **Number of islands II**: union-find online, one cell at a time.
34. **Minimize malware spread**: component sizes and infected counts.
35. **Common factor**: union through prime hub nodes.
36. **People with secret**: union-find per timestamp with resets.
37. **Limited paths**: offline queries over a growing union-find.
38. **Removable edges**: two union-finds sharing edges.
39. **Network delay time**: Dijkstra with a heap.
40. **Valid path in a grid**: 0-1 BFS on arrows.
41. **Swim in rising water**: bottleneck path with a heap.
42. **Weighted subgraph**: three Dijkstras, one on the reversed graph.
43. **Connect all points**: Prim's MST.
44. **Critical MST edges**: Kruskal with an edge excluded or forced.
45. **Critical connections**: Tarjan's bridges, the final boss.
