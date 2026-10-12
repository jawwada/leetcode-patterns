# Graphs

A graph is a set of nodes and a set of edges between them. Almost every graph algorithm in interviews is one of two things: a **traversal** that visits nodes in some order (BFS, DFS, topological sort) or a **greedy selection** that repeatedly takes the cheapest option from a priority queue or a sorted list (Dijkstra, Prim, Kruskal). The data structure that drives the order is the whole algorithm: a queue gives layers, a stack gives depth, a heap gives cheapest-first, and union-find answers "are these two already connected?" in near constant time.

Represent the graph as an **adjacency list**: `adj[u]` is the list of neighbors of `u` (with the weight when edges are weighted). An undirected edge is stored twice, once in each direction. Building it is O(n + m) for n nodes and m edges, and every traversal below is linear in the same n + m before any log factor from a heap.

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| build adjacency list | O(n + m) | undirected edge stored in both directions |
| queue push / popleft | O(1) | `collections.deque` |
| stack push / pop | O(1) | a Python list |
| heap push / pop | O(log k) | `heapq`, k entries; a node may have several stale entries |
| union-find `find` / `union` | near O(1) amortized | path compression + union by size |
| sort m edges | O(m log m) | Kruskal's only expensive step |

## Which algorithm?

| Algorithm | Driving structure | Use it when | Complexity | Caught by |
|---|---|---|---|---|
| BFS | queue, mark on enqueue | shortest path in HOPS, layers, nearest X in an unweighted graph | O(n + m) | marking on pop (nodes enqueued twice) |
| DFS | stack or recursion, mark on pop | reachability, connected components, cycle detection, anything needing the full path | O(n + m) | forgetting that a node may already be visited when popped |
| Kahn (topological sort) | queue of indegree-0 nodes | ordering tasks with prerequisites; detects a cycle when some node is never freed | O(n + m) | checking `not order` instead of `len(order) < n` |
| Dijkstra | heap of (dist, node) | shortest path with NON-NEGATIVE weights | O((n + m) log m) | not skipping stale entries, or skipping with `>=` |
| Prim | heap of (weight, node) crossing edges | minimum spanning tree, dense graph, one start node | O(m log m) | adding a node already in the tree |
| Kruskal | sorted edges + union-find | minimum spanning tree, sparse graph, edges given as a list | O(m log m) | comparing endpoints instead of roots |

BFS and Dijkstra are the same algorithm with a different structure: a queue works for BFS because every edge costs 1, so the queue is already sorted by distance. The heap restores that sorted order when weights differ. Prim is Dijkstra with "weight of this edge" in the heap instead of "distance from the source".

## Drawn example: Dijkstra from 0

```
edges: 0->1 (4)  0->2 (1)  2->1 (2)  1->3 (1)  2->3 (5)  3->4 (3)

pop (0, 0)  final    relax 0->1: dist[1]=4 push (4,1)       heap [(1,2), (4,1)]
                     relax 0->2: dist[2]=1 push (1,2)
pop (1, 2)  final    relax 2->1: dist[1]=3 push (3,1)       heap [(3,1), (4,1), (6,3)]
                     relax 2->3: dist[3]=6 push (6,3)
pop (3, 1)  final    relax 1->3: dist[3]=4 push (4,3)       heap [(4,1), (4,3), (6,3)]
pop (4, 1)  STALE    4 > dist[1]=3, skip                     heap [(4,3), (6,3)]
pop (4, 3)  final    relax 3->4: dist[4]=7 push (7,4)       heap [(6,3), (7,4)]
pop (6, 3)  STALE    6 > dist[3]=4, skip                     heap [(7,4)]
pop (7, 4)  final                                            heap []
dist {0: 0, 2: 1, 1: 3, 3: 4, 4: 7}
```

The same graph as an undirected weighted graph gives the spanning tree 0-2 (1), 1-2 (2), 3-4 (3), 1-3 (5), total 11, whether you grow it from a node (Prim) or pick edges globally (Kruskal); edge 0-1 (4) is the one both reject.

## The invariants to say out loud

- BFS: "Everything in the queue is at distance d or d+1, and the d's come first."
- DFS: "The stack holds the frontier of the current path; a node may sit on it twice, so check visited on pop."
- Kahn: "A node enters the queue exactly when its last prerequisite is removed; if fewer than n nodes come out, the rest form a cycle."
- Dijkstra: "A node is final when popped. Its distance can never improve because every other entry in the heap is at least as far."
- Prim: "The heap holds every edge crossing from the tree to the outside; the cheapest crossing edge is always safe."
- Kruskal: "An edge is safe iff its endpoints have different roots; union-find keeps the roots."

## Exercises

| File | Drills |
|---|---|
| `01_adjacency_list_bfs_dfs.py` | build the adjacency list; BFS with a queue (mark on enqueue); DFS with a stack (push in reverse, mark on pop) |
| `02_topological_sort_kahn_and_dfs.py` | indegree counting, queue of free nodes, cycle detection by count; DFS post-order reversed as the cross-check |
| `03_union_find.py` | find with path compression, union by size, component count, connected queries |
| `04_kruskal_mst.py` | sort edges, accept iff roots differ, stop at n-1 edges; Prim as the cross-check |
| `05_prim_mst.py` | heap of crossing edges, skip a popped node already in the tree; Kruskal as the cross-check |
| `06_dijkstra.py` | heap of (dist, node), stale-entry skip with a strict `>`, relax out-edges; Bellman-Ford as the cross-check |
