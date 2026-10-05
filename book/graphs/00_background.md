# Graphs

*45 problems · Reading time ~25 min*

## The chapter

A graph is a set of nodes and the edges that connect them, explicit as an adjacency list or implicit in a grid, a word
list or a board state. This chapter teaches depth-first and breadth-first traversal, multi-source and state-augmented
BFS, topological order, union-find, shortest paths with Dijkstra and its 0-1 and bidirectional variants, minimum
spanning trees, and bridges.

Problems, in reading order:

1. [Flood Fill](flood_fill.md) · Easy
2. [Number of Islands](number_of_islands.md) · Medium
3. [Max Area of Island](max_area_of_island.md) · Medium
4. [Number of Enclaves](number_of_enclaves.md) · Medium
5. [Surrounded Regions](surrounded_regions.md) · Medium
6. [Pacific Atlantic Water Flow](pacific_atlantic_water_flow.md) · Medium
7. [Rotting Oranges](rotting_oranges.md) · Medium
8. [01 Matrix](zero_one_matrix.md) · Medium
9. [Walls and Gates](walls_and_gates.md) · Medium
10. [Clone Graph](clone_graph.md) · Medium
11. [Word Ladder](word_ladder.md) · Hard
12. [Word Ladder II](word_ladder_ii.md) · Hard
13. [Sliding Puzzle](sliding_puzzle.md) · Hard
14. [Bus Routes](bus_routes.md) · Hard
15. [Jump Game IV](jump_game_iv.md) · Hard
16. [K-Similar Strings](k_similar_strings.md) · Hard
17. [Shortest Path in a Grid with Obstacles Elimination](shortest_path_in_a_grid_with_obstacles_elimination.md) · Hard
18. [Shortest Path to Get All Keys](shortest_path_to_get_all_keys.md) · Hard
19. [Shortest Path Visiting All Nodes](shortest_path_visiting_all_nodes.md) · Hard
20. [Minimum Moves to Move a Box to Their Target Location](minimum_moves_to_move_a_box_to_their_target_location.md) · Hard
21. [Find the Town Judge](find_the_town_judge.md) · Easy
22. [Course Schedule](course_schedule.md) · Medium
23. [Course Schedule II](course_schedule_ii.md) · Medium
24. [Alien Dictionary](alien_dictionary.md) · Hard
25. [Parallel Courses III](parallel_courses_iii.md) · Hard
26. [Sort Items by Groups Respecting Dependencies](sort_items_by_groups_respecting_dependencies.md) · Hard
27. [Reconstruct Itinerary](reconstruct_itinerary.md) · Hard
28. [Number of Connected Components in an Undirected Graph](number_of_connected_components.md) · Medium
29. [Graph Valid Tree](graph_valid_tree.md) · Medium
30. [Redundant Connection](redundant_connection.md) · Medium
31. [Redundant Connection II](redundant_connection_ii.md) · Hard
32. [Accounts Merge](accounts_merge.md) · Medium
33. [Number of Islands II](number_of_islands_ii.md) · Hard
34. [Minimize Malware Spread](minimize_malware_spread.md) · Hard
35. [Largest Component Size by Common Factor](largest_component_size_by_common_factor.md) · Hard
36. [Find All People With Secret](find_all_people_with_secret.md) · Hard
37. [Checking Existence of Edge Length Limited Paths](checking_existence_of_edge_length_limited_paths.md) · Hard
38. [Remove Max Number of Edges to Keep Graph Fully Traversable](remove_max_number_of_edges_to_keep_graph_fully_traversable.md) · Hard
39. [Network Delay Time](network_delay_time.md) · Medium
40. [Minimum Cost to Make at Least One Valid Path in a Grid](minimum_cost_to_make_at_least_one_valid_path_in_a_grid.md) · Hard
41. [Swim in Rising Water](swim_in_rising_water.md) · Hard
42. [Minimum Weighted Subgraph With the Required Paths](minimum_weighted_subgraph_with_the_required_paths.md) · Hard
43. [Min Cost to Connect All Points](min_cost_to_connect_all_points.md) · Medium
44. [Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree](find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree.md) · Hard
45. [Critical Connections in a Network](critical_connections_in_a_network.md) · Hard

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

## Advanced patterns

The tools above get you through the Mediums. Each Hard adds one twist: the node is redefined, the edges are thinned,
the queries are reordered, or the cost is computed differently. These seven twists cover every Hard here.

### 1. The node is "where I am plus what I carry"

**When it shows up.** A shortest-path question on a grid or small graph, plus something that changes what is possible
later: walls you may still break, keys on your ring, which nodes you have already seen, where the box sits. The
constraints give it away: k <= 40, at most 6 keys, n <= 12.

**The intuition.** BFS is correct only if two visits to the same node have the same future. A cell reached with a key
and the same cell reached without one do not have the same future: one can pass the door, the other cannot. So the cell
is the wrong node. Put the extra into the node, `(cell, keys)`, and the futures match again, so BFS works unchanged. The
price is the state count: cells times the number of possible extras (times 2^6 for keys, times k + 1 for a budget).
Picture one copy of the grid per value of the extra,
stacked like floors; picking up a key takes the stairs.

```text
  corridor:  $   A   @   .   a     $ goal, A door, a key
  index:     0   1   2   3   4     start at @ (index 2)

  visited keyed on cell only:
    2 -> 3 -> 4 (key!) -> 3? already seen. stuck.

  visited keyed on (cell, keys):    numbers = BFS distance
  floor keys={}  :  .   x   0   1   2   x = door blocks
                                    |   pick up a: stairs
  floor keys={a} :  6   5   4   3   2
  goal reached on the {a} floor at distance 6
```

**Where you'll use it.** Shortest Path in a Grid with Obstacles Elimination (budget), Shortest Path to Get All Keys
(key mask), Shortest Path Visiting All Nodes (visited mask, every node a source), Minimum Moves to Move a Box (box plus
player), and in spirit Sliding Puzzle, where the whole board is the state. Beyond the chapter: Minimum Cost to Reach
Destination in Time (LeetCode 1928).

### 2. Keep every parent: the shortest-path DAG

**When it shows up.** "Return all shortest sequences", or "count the shortest paths".

**The intuition.** BFS normally keeps one parent per node, the first one to discover it, so it can rebuild one path.
Every shortest path, though, steps from layer d to layer d+1 at each move; nothing else can be on a shortest path. So
keep every parent that sits one layer up, and the shortest paths are exactly the routes through this layered DAG. The
trap is the visited mark: if you delete a word the moment one node of layer d finds it, a sibling in layer d that also
links to it never gets recorded as a parent. Expand the whole layer into a "next" map first, then retire all of its
words together. Then backtrack
from the target.

```text
  layer  0     1      2          3          4
         hit - hot - dot ------ dog ------ cog
                  \                       /
                   - lot ------ log ------

  parents:  hot{hit}  dot{hot}  lot{hot}
            dog{dot}  log{lot}  cog{dog, log}  <- two parents
  backtrack from cog: cog-dog-dot-hot-hit, cog-log-lot-hot-hit
```

**Where you'll use it.** Word Ladder II. Beyond the chapter: Number of Ways to Arrive at Destination (LeetCode 1976),
the same DAG idea with Dijkstra and counts instead of lists.

### 3. Replace a clique with a hub, and consume the hub once

**When it shows up.** One rule connects whole groups to each other: every stop on a bus route, every index holding the
same value, every word matching `h*t`, every number sharing a prime factor.

**The intuition.** A group of m mutually connected nodes is m(m-1)/2 edges if you draw them all, and a BFS that walks
them all is quadratic. Add one extra node for the group (the route, the value, the wildcard pattern, the prime) and join
each member to it: m edges. Now a second idea: in BFS, the first time you reach any member, you reach every member at
the same distance + 1. After that the hub is useless, so delete or mark it, and no later member walks the group again.
Each hub is opened once, so the total work is the sum of group sizes. In union-find the same hub trick appears without
the "once": union each number with its primes, and numbers sharing a prime land under one root.

```text
  clique (value 6 at indices 1, 3, 5, 7)   hub
     1 ----- 3                   1   3   5   7
     | \   / |                    \  |   |  /
     |   X   |                     [ value 6 ]
     | /   \ |                 4 edges, and after the first
     5 ----- 7                 visit the bucket is cleared:
  6 edges; m(m-1)/2 grows fast  bucket[6] = []
```

**Where you'll use it.** Word Ladder (wildcard buckets), Bus Routes (routes as nodes), Jump Game IV (value buckets
cleared after use), Largest Component Size by Common Factor (primes as hubs in union-find).

### 4. Topological order carries a DP

**When it shows up.** Dependencies plus a number to optimise along them: earliest finish time, longest chain, count of
ways, or an ordering that must hold at two levels at once.

**The intuition.** A topological order is exactly the order in which a DP over a DAG can be filled: when Kahn pops a
node, every predecessor has already been popped, so every value the node depends on is final. Each pop pushes its value
along its out-edges (`start[v] = max(start[v], finish[u])`), and when a node's in-degree hits 0 its value is complete.
That is how a "longest path", NP-hard in general graphs, becomes linear on a DAG. For two-level orderings (items inside
groups), build two graphs: one between groups from cross-group edges, one between items from same-group edges, sort
both, then lay the item order out group by group.

```text
  courses 1..5, time = [1,2,3,4,5]
  edges 1->5  2->5  3->5  3->4  4->5

     1 (t=1) -----------------------.
     2 (t=2) ---------------------. |
     3 (t=3) -------------------. | |
        |                       v v v
        +-----> 4 (t=4) -----> 5 (t=5)

  node    start (max finish of prereqs)    finish
  1 2 3   0                                1 2 3
  4       3                                7
  5       max(1, 2, 3, 7) = 7              12
  Kahn pops 1 2 3 4 5; answer = max finish = 12
```

**Where you'll use it.** Parallel Courses III (finish times), Sort Items by Groups Respecting Dependencies (two-level
sort), Alien Dictionary (building the edges is the hard part). Beyond the chapter: Longest Increasing Path in a Matrix
(LeetCode 329), a DAG hiding in a grid.

### 5. Union-find on a sorted sweep

**When it shows up.** Many questions about connectivity under a threshold ("paths using only edges shorter than
limit"), meetings that happen at timestamps, or a greedy that must take some edges before others.

**The intuition.** Union-find can merge but never split. That sounds like a weakness, but it is perfect for any process
in which the graph only grows. If you are given all the queries up front, sort them along the axis on which the graph
grows (the weight limit), sort the edges the same way, and sweep: before answering a query, union every edge to the
left of it. Each edge is unioned once in the whole run. When the graph has to forget (a meeting at time 5 must not
connect people at time 8), process one time group at a time and, afterwards, reset the participants who did not end up
connected to the source. The same "sort, then grow" shape is Kruskal, and running Kruskal again with one edge excluded or
forced answers whether that edge is critical.

```text
  edges sorted by length:  0-1:2   1-2:4   2-0:8   1-0:16
  queries sorted by limit: (0,1,<2)   (0,2,<5)

  weight axis  0    2    4    5    8         16
               |----e----e----|----e----------e
                    ^ q0 asks here (nothing < 2 glued)
                              ^ q1 (0-1, 1-2 glued)

  q0: find(0) != find(1)          -> false
  q1: union 0-1, union 1-2;
      find(0) == find(2)          -> true
```

**Where you'll use it.** Checking Existence of Edge Length Limited Paths (offline queries), Find All People With Secret
(time groups with resets), Number of Islands II (online growth), Remove Max Number of Edges (two union-finds, shared
edges first), Find Critical and Pseudo-Critical Edges (Kruskal with an edge excluded or forced). Beyond the chapter:
Number of Good Paths (LeetCode 2421).

### 6. Change the cost, keep the frontier

**When it shows up.** The path's cost is not a plain sum of unit steps: some moves are free and some cost 1; the cost of
a path is its highest cell; or you need distances *into* one target from every node.

**The intuition.** Dijkstra needs only one thing: when you extend a path, its cost never goes down. Sum of non-negative
weights satisfies that, and so does `max(cost so far, next cell)`, so a bottleneck path is Dijkstra with `+` replaced by
`max`. If the weights are only 0 and 1, the heap is overkill: a deque stays sorted if free moves go to the front and
paid moves to the back. And if you need distance from every node to one target, reverse every edge: a column of the
distance matrix becomes a row, which one Dijkstra computes. With rows from two sources and the reversed row into the
destination, a "meeting node" problem is a minimum over x of three table lookups.

```text
  relax rule          container      problem
  d + w               min-heap       Network Delay Time
  max(d, h[cell])     min-heap       Swim in Rising Water
  d + 0 or d + 1      deque          Valid Path, Box Pushing

  swim on      0 6 2      pops in order of path height:
               1 8 3      0, 1, 5, 6, then 2 3 4 all at 6
               5 7 4      answer 6 (path 0 6 2 3 4)

  meeting node: src1=0, src2=1, dest=5 (example graph)
    x   : 0  1  2  3  4  5
    d1  : 0  3  2  5  7  6    Dijkstra from src1
    d2  : 3  0  5  8  5  6    Dijkstra from src2
    dd  : 6  6  6  3  1  0    Dijkstra from dest, reversed
    sum : 9  9 13 16 13 12    answer = min = 9
```

**Where you'll use it.** Minimum Cost to Make at Least One Valid Path (0-1 BFS on arrows), Minimum Moves to Move a Box
(0-1 BFS over states), Swim in Rising Water (bottleneck), Minimum Weighted Subgraph With the Required Paths (two
forward runs and one reversed). Beyond the chapter: Path With Minimum Effort (LeetCode 1631).

### 7. Decide a node on the way back: post-order DFS

**When it shows up.** "Use every edge exactly once" (Euler path), or "which edges are single points of failure"
(bridges).

**The intuition.** Some facts about a node are only known once everything below it has been explored. In Hierholzer's
algorithm you walk edges greedily, deleting each as you use it, and append a node to the route only when it has no
unused edges left. A greedy walk can wander into a dead end too early, but the dead end is appended first, so after the
final reversal it lands at the end of the route, where a dead end belongs. Tarjan's bridges have the same shape:
`low[u]` is complete only after all of u's children return, so the bridge test runs on the way back.

```text
  tickets JFK->KUL  JFK->NRT  NRT->JFK  (smallest name first)

  dfs(JFK) takes KUL           dfs(KUL): no edges, out=[KUL]
  back at JFK, takes NRT
  dfs(NRT) takes JFK           dfs(JFK): no edges left,
                               out=[KUL, JFK]
  NRT done                     out=[KUL, JFK, NRT]
  JFK done                     out=[KUL, JFK, NRT, JFK]
  reversed route: JFK NRT JFK KUL   (KUL, the dead end, last)
```

**Where you'll use it.** Reconstruct Itinerary (Hierholzer), Critical Connections in a Network (low-link). Beyond the
chapter: Valid Arrangement of Pairs (LeetCode 2097).

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

Each problem keeps most of the previous one and changes one thing: what a node is, what an edge is, what the
traversal returns, or what a path costs.

### Stage 1: flood a grid

**Flood Fill.** The smallest traversal: one start pixel, one region. Recolouring *is* the visited set, which also
explains the one trap: if the new colour equals the old, nothing gets marked and the walk never ends.

**Number of Islands.** Now there are many regions and nobody says where they start. Scan every cell and launch a flood
from each unvisited land cell; each launch sinks one whole island, so count the launches.

**Max Area of Island.** Same scan, but each flood now returns how many cells it sank. The traversal produces a value
instead of only a side effect.

**Number of Enclaves.** Asking "can this cell reach the border?" once per cell repeats the same flood over and over.
Turn it around: flood once from all border land together and count what stays dry. Asking from the target side is one
of the chapter's most reusable moves.

**Surrounded Regions.** The same border flood, but the board is rewritten in place, so the flood needs a temporary
third mark. A final sweep flips unmarked `O`s to `X` and restores the marked ones.

**Pacific Atlantic Water Flow.** Flooding downhill from each cell is expensive, so flood from each ocean, climbing
uphill: the edge rule is reversed. Two floods, two visited sets, and the answer is their intersection.

### Stage 2: waves of distance

**Rotting Oranges.** Every rotten orange spreads at once, so one BFS per orange is wrong as well as slow. Seed them all
at minute 0 and count layers: multi-source BFS.

**01 Matrix.** BFS from each one-cell is quadratic. One wave from all zeros writes every cell's distance in a single
pass; the traversal now fills a table.

**Walls and Gates.** The same wave from the gates, with distances written into the grid itself. A cell is visited
exactly when it is no longer infinity, so the grid is both visited set and answer.

### Stage 3: graphs you build or imagine

**Clone Graph.** The first real adjacency list, with cycles. The old-to-new map answers "have I copied this node yet?",
so it is the visited set and also how a copied edge finds its far end.

**Word Ladder.** Nobody gives you the edges: words differing by one letter are joined. Comparing all pairs is too slow,
so bucket words by patterns like `h*t` and find neighbours through the buckets, the first hub (advanced pattern 3).

**Word Ladder II.** Now return every shortest chain. One parent per word loses chains, and marking words too early
loses parents within a layer; build a parents DAG a full layer at a time, then backtrack (advanced pattern 2).

**Sliding Puzzle.** The node is a whole board written as a string, and an edge is one slide of the blank. Only 720
boards exist, so plain BFS suffices; the leap is accepting that a configuration can be a node.

**Bus Routes.** BFS over stops counts stops, but the question counts buses. Make routes the nodes, and one BFS step is
one ride; choosing the node right is the whole problem.

**Jump Game IV.** A value that appears m times creates m(m-1)/2 jump edges. Visit a value's whole bucket the first time
any of its indices is reached, then clear it, and the BFS stays linear.

**K-Similar Strings.** BFS over strings where an edge is a swap, with explosive branching. Only try swaps that fix the
first mismatch; the lesson is why pruning the neighbour function this hard loses no shortest path.

### Stage 4: the node is a state

**Shortest Path in a Grid with Obstacles Elimination.** Reaching a cell with more walls left to break beats reaching it
with fewer, so the node is `(row, col, eliminations left)` (advanced pattern 1). If k covers the Manhattan path, return
its length at once.

**Shortest Path to Get All Keys.** The extra is a key bitmask, and doors test it. The same cell is a different node on
each key ring; the goal is any state with a full mask.

**Shortest Path Visiting All Nodes.** The state is `(node, visited mask)` and the walk may start anywhere, so all n
starts are seeded at distance 0. That is Stage 2's multi-source BFS over n times 2^n states, which is why n <= 12.

**Minimum Moves to Move a Box to Their Target Location.** The state is box plus player, and only pushes count. Walks
cost 0 and pushes cost 1, so a deque replaces the queue: the first 0-1 BFS.

### Stage 5: direction and order

**Find the Town Judge.** Directed edges, no traversal: the judge has in-degree minus out-degree equal to n-1. Degrees
are the bookkeeping Kahn's algorithm runs on.

**Course Schedule.** Repeatedly take a course with in-degree 0 and delete its out-edges. Courses that never reach 0 sit
on a cycle, so the pop count is the answer.

**Course Schedule II.** The same loop, recording the pop order. Kahn does not just say yes; it hands you the schedule.

**Alien Dictionary.** You build the edges: the first differing letter of each adjacent word pair is one edge, then
topo-sort the letters. The trap is a word before its own prefix (`abc` before `ab`), which makes the input invalid.

**Parallel Courses III.** Courses take time and run in parallel, so the answer is the longest weighted path in the DAG.
Carry finish times along Kahn's order (advanced pattern 4).

**Sort Items by Groups Respecting Dependencies.** Groups must stay contiguous. Topo-sort the groups, topo-sort items
within groups, and lay them out group by group, giving each ungrouped item a group of its own.

**Reconstruct Itinerary.** Use every ticket once, smallest route first. A greedy walk can strand you; Hierholzer
appends a node only when it has no unused edges, then reverses, so dead ends land last (advanced pattern 7).

### Stage 6: union-find

**Number of Connected Components in an Undirected Graph.** Easy with DFS, which makes it the right place to meet
union-find: start at n components and subtract one per successful union.

**Graph Valid Tree.** A tree has n-1 edges and no cycle, and a union that finds both ends under one root has just
closed a loop. Union-find gets the cycle test for free.

**Redundant Connection.** One extra edge made exactly one cycle. The edge that closed it is the first union that fails.

**Redundant Connection II.** Directed edges add a second fault, a node with two parents, and the two faults can
interact. One in-degree scan finds at most two candidates; one union-find pass with the later one left out decides.

**Accounts Merge.** Accounts sharing an email are one person. Union through an email-to-first-account map, then group
emails by root: union-find over string keys that must output groups.

**Number of Islands II.** Land appears cell by cell and the count is wanted after each. Each new cell tries at most four
unions, and every successful one merges two islands into one.

**Minimize Malware Spread.** Removing an infected node saves its component only if it is that component's sole infected
node. So keep component sizes and infected counts per root, and compare.

**Largest Component Size by Common Factor.** Comparing all pairs is quadratic; union each number with its prime
factors instead, so primes act as hubs inside union-find.

**Find All People With Secret.** Links from a meeting that missed the secret must not leak into later meetings. Union
one timestamp at a time, then reset everyone who met but did not join person 0: the first union-find that forgets.

**Checking Existence of Edge Length Limited Paths.** Sort queries and edges by weight, sweep the limit upward, and grow
one union-find as you go. The query order is now yours to choose (advanced pattern 5).

**Remove Max Number of Edges to Keep Graph Fully Traversable.** Two players, two union-finds, shared edges first,
because a shared edge does the work of two private ones. Every edge that merges nothing is removable.

### Stage 7: weights, spanning trees and bridges

**Network Delay Time.** Weighted edges mean BFS layers are no longer distances. A min-heap orders the frontier and stale
entries are skipped on pop: Dijkstra.

**Minimum Cost to Make at Least One Valid Path in a Grid.** Following a cell's arrow is free, any other move costs one.
Box Pushing's 0-1 BFS, now on a plain grid.

**Swim in Rising Water.** A path costs its highest cell, not its sum. Dijkstra still works with `max` in place of `+`,
since extending a path never lowers its maximum (advanced pattern 6).

**Minimum Weighted Subgraph With the Required Paths.** Two sources reach one destination and their paths may merge.
Guess the merge node x and add three distances; two forward Dijkstras and one on the reversed graph fill all three
tables.

**Min Cost to Connect All Points.** Not a path but the cheapest way to connect everything: an MST. Every pair is an
edge, so Prim's heap beats sorting n^2 edges for Kruskal.

**Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree.** For each edge, run Kruskal once without it
(heavier means critical) and once with it forced in (same weight means it can belong).

**Critical Connections in a Network.** Removing each edge and re-testing is quadratic. One DFS with discovery times and
low-links finds every bridge: the subtree below it has no back edge reaching above it.
