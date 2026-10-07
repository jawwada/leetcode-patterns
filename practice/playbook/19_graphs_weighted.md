## Graphs III: Weighted Paths & MST

> Once edges have prices, "fewest edges" is no longer "cheapest". **Dijkstra** is BFS with a priority queue: always settle the closest unsettled node, because with no negative edges nobody can reach it more cheaply later. **A minimum spanning tree** connects everything for the least total price: keep taking the cheapest edge that does not close a loop.

**Reach for it when** edges have weights and the problem asks for the minimum cost / time / effort to get somewhere (Dijkstra); every weight is 0 or 1, like "free move or paid move" (0-1 BFS with a deque); "minimise the *highest* step on the route" (Dijkstra with `max` instead of `+`); "connect all points / cities as cheaply as possible" (MST: Prim or Kruskal); "at most k stops" or negative weights (Bellman-Ford rounds).

**In this repo:** `graphs/` (7 of its 45 problems) · bank: `practice/simple/45_network_delay_time.py`, `practice/simple/46_min_cost_to_connect_all_points.py` · basics: `practice/simple/basics/graphs/06_dijkstra.py`, `practice/simple/basics/graphs/05_prim_mst.py`, `practice/simple/basics/graphs/04_kruskal_mst.py`, `practice/simple/basics/graphs/03_union_find.py`

### The picture

```text
         1
   A ---------- B          pop (0,A)  settle A  push B=1 C=5   heap (1,B) (5,C)
   |            |          pop (1,B)  settle B  push D=3       heap (3,D) (5,C)
 5 |            | 2        pop (3,D)  settle D  push C=4       heap (4,C) (5,C)   C got cheaper
   |            |          pop (4,C)  settle C                 heap (5,C)
   C ---------- D          pop (5,C)  stale: 5 > dist[C] = 4, skip it
         1
```

The heap always hands out the closest node nobody has settled yet. C was first priced at 5 (straight from A), then found again at 4 (A, B, D, C); the old entry is not removed, it is simply skipped when it surfaces. That skip is the **stale check**.

Why is a popped node final?

```text
   settled (popped)                    in the heap (priced, not final yet)
( src ... x ) --w-->  y  [price(y) >= d]  ... -->  u

u is popped with d = the smallest price in the heap. Any other route to u leaves the
settled blob through some edge x -> y; at y it already costs >= price(y) >= d, and the
rest of the route adds >= 0 (no negative edges). Nothing can beat d.
```

```text
    0 ---4--- 1                 Kruskal: cheapest edge first; skip it if its ends are already connected
    |       / |
    1     2   5                 0-2 (1)  take   {0,2} {1} {3} {4}
    |   /     |                 1-2 (2)  take   {0,1,2} {3} {4}
    2 ---8--- 3 ---3--- 4       3-4 (3)  take   {0,1,2} {3,4}
                                0-1 (4)  SKIP   0 and 1 are already connected: it would close a loop
                                1-3 (5)  take   {0,1,2,3,4}: n - 1 = 4 edges, done, total 11

    Prim grows one blob from 0 instead, always adding the cheapest edge that leaves it:
    0-2 (1), 2-1 (2), 1-3 (5), 3-4 (3): the same total, 11
```

**Why the greedy edge is safe (the cut property).** Split the nodes into two sides and let e be the cheapest edge crossing the split. Take any best tree that does not use e: adding e closes a loop, and that loop must cross the split a second time through some edge f with w(f) ≥ w(e). Swap f for e: the tree still spans everything and is never heavier, so some best tree uses e. Prim uses the split "tree so far | the rest". Kruskal, at an edge (u, v) whose ends have different roots, uses the split "u's group | the rest": every cheaper edge has already been processed, and none of them can still leave u's group (it would have been taken), so (u, v) is the cheapest edge leaving it.

**Why it is fast:** Bellman-Ford relaxes every edge in V − 1 rounds, O(V · E), because it does not know which distances are final. Dijkstra settles nodes in order of distance, so each node's edges are relaxed once, and the heap hands out the next node in O(log V): O((V + E) log V). For the MST, the brute force tries spanning trees (exponentially many); the cut property makes the greedy choice safe, so one sorted pass (Kruskal) or one heap-driven growth (Prim) is enough.

### From idea to code

**The idea in one sentence:** *pop the cheapest entry from a min-heap; if it is out of date, skip it; otherwise it is final, so offer its neighbours at their new prices.* Dijkstra prices a node by the whole path `d + w`; Prim prices it by the single edge `w` that would attach it to the tree. That is the one real difference between the two loops: both pop the cheapest entry, skip the out-of-date ones, and offer the neighbours.

| Decision | Dijkstra | Prim (MST) |
|---|---|---|
| **State**: what must I remember? | `dist[v]` and a min-heap of `(dist, node)` | `in_tree` and a min-heap of `(edge cost, node)` |
| **Definition**: what exactly does each variable mean? | `dist[v]` = the cheapest path from `src` to `v` found so far; final once `v` is popped with `d == dist[v]` | an entry `(w, v)` = "v could join the tree through an edge of cost w" |
| **Invariant**: what is true at the end of every step? | nodes are settled in nondecreasing distance, and a settled distance never changes | the tree built so far is part of some minimum spanning tree |
| **Step**: how does one item change the state? | pop `(d, u)`; skip if `d > dist[u]`; for each edge `(v, w)`: if `d + w < dist[v]`, update and push | pop `(w, v)`; skip if `v` is in the tree; add it; push `(w', x)` for every edge to an outside `x` |
| **Record**: when is the answer updated? | `dist[u]` is final at its (non-stale) pop | `total += w` when `v` joins |
| **Init**: starting values | `dist = {src: 0}`, heap `[(0, src)]` | heap `[(0, start)]`: the start joins for free |
| **Return**: what comes back, and for "not found"? | `dist`, `dist[target]` or `max(dist.values())`; −1 if a node never appears | `total` once all n have joined; fewer means the graph is disconnected |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "the closest node not settled yet" | `d, u = heapq.heappop(heap)` |
| "an out-of-date copy of u" | `if d > dist[u]: continue` |
| "going through u is cheaper" | `if d + w < dist.get(v, math.inf):` |
| "remember it and offer it" | `dist[v] = d + w` then `heapq.heappush(heap, (d + w, v))` |
| "a path is as bad as its worst step" | `max(d, w)` in place of `d + w` |
| "a free move / a paid move" (0-1 BFS) | `dq.appendleft(...)` / `dq.append(...)` |
| "the cheapest edge leaving the tree" (Prim) | `w, v = heapq.heappop(heap)`, skip if `in_tree[v]` |
| "this edge would close a loop" (Kruskal) | `find(u) == find(v)` |

Dijkstra, then Network Delay Time on top of it. The order is the whole point: a node is final when it is *popped* (after the stale check), never when it is pushed.

```python
def dijkstra(graph, src):
    """graph[u] = [(v, w), ...] with every w >= 0, and every node is a key (use defaultdict(list)).
    Returns {node: shortest distance from src} for every node src can reach."""
    dist = {src: 0}                               # STATE + INIT: dist[v] = cheapest way to v found so far
    heap = [(0, src)]                             # STATE + INIT: (price, node) entries, cheapest on top
    while heap:
        d, u = heapq.heappop(heap)                # the cheapest entry left
        if d > dist[u]:
            continue                              # stale: u was already settled closer
        # RECORD: d == dist[u] is final now; a single target is checked here: if u == target: return d
        for v, w in graph[u]:
            if d + w < dist.get(v, math.inf):     # relax: going through u is cheaper
                dist[v] = d + w                   # STEP: v's best price so far...
                heapq.heappush(heap, (d + w, v))  # ...offered to the heap
    return dist                                   # RETURN: unreachable nodes are simply missing


def network_delay_time(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist = dijkstra(graph, k)
    return max(dist.values()) if len(dist) == n else -1     # the last node to hear it, or -1


print(network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))             # 2
print(network_delay_time([[1, 2, 4], [1, 3, 1], [3, 2, 1], [2, 4, 2]], 4, 1))  # 4  (1 -> 3 -> 2 beats 1 -> 2)
print(network_delay_time([[1, 2, 1]], 2, 2))                                   # -1 (nothing leaves node 2)
```

**Try it**
- Add `print(d, u)` right after the `heappop` and run the second example: node 2 comes out twice, at 2 (real) and at 4 (stale, skipped).
- The BFS habit: keep a `seen` set, add `v` when you push it, and skip neighbours already seen. The second example answers 6 instead of 4: node 2 was locked in at 4 by the direct edge before 1 → 3 → 2 (cost 2) was found. A Dijkstra node is final when it is popped.
- Change `d > dist[u]` to `d >= dist[u]`: all three examples answer -1. Even the very first entry, `(0, src)`, now looks stale.
- Give `dijkstra` a `target` and return at discovery (`if v == target: return d + w` right after `dist[v] = d + w`): from 1 to 2 in the second example you get 4 instead of 2. Discovery-time checks are safe in BFS, where every edge costs 1, not here.

Prim on the complete graph of points. There is no edge list: the "edges" from a point are its distances to every point still outside the tree.

```python
def min_cost_connect_points(points):
    n = len(points)
    in_tree = [False] * n                         # STATE + INIT: who has joined the tree
    heap = [(0, 0)]                               # STATE + INIT: (cost to join, point); point 0 joins free
    total = joined = 0
    while joined < n:                             # all points connect to all, so the heap never runs dry
        cost, i = heapq.heappop(heap)             # the cheapest edge leaving the tree
        if in_tree[i]:
            continue                              # stale: i joined earlier through a cheaper edge
        in_tree[i] = True                         # STEP: i joins the tree...
        total += cost                             # RECORD: ...through the cheapest crossing edge, a safe one
        joined += 1
        for j in range(n):                        # offer i's edges to every point still outside
            if not in_tree[j]:
                manhattan = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                heapq.heappush(heap, (manhattan, j))
    return total                                  # RETURN


print(min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))   # 20
print(min_cost_connect_points([[3, 12], [-2, 5], [-4, 1]]))                # 18
```

**Try it**
- Delete the `if in_tree[i]: continue` lines: the first example answers 18. Point 3 is popped a second time and counted as a fifth join, so the loop stops before point 2 ever joins.
- Start the heap with `(5, 0)` instead of `(0, 0)`: 25. The start must join for free.
- Print `i, cost` when a point joins: 0 (0), 1 (4), 3 (3), 4 (4), 2 (9). The costs are not sorted: Prim takes the cheapest edge leaving the *current* tree, not the cheapest edge overall.

Kruskal: sort all edges once, then let union-find say whether an edge would close a loop.

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
    for u, v, w in sorted(edges, key=lambda e: e[2]):   # cheapest edge first
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

**Try it**
- Delete the `if ru == rv: continue` lines: you get `(10, [(0, 2, 1), (1, 2, 2), (3, 4, 3), (0, 1, 4)])`, four edges that contain the loop 0-1-2 and leave 3 and 4 cut off from the rest.
- Sort by `-e[2]` (heaviest first): a *maximum* spanning tree, weight 20.
- `kruskal(4, [(0, 1, 1), (2, 3, 1)])` keeps only 2 edges: fewer than `n - 1` means the graph is disconnected.

### Watch it work

The picture's graph, step by step. Every pop is either settled or skipped as stale:

```python
def trace_dijkstra(graph, src):
    dist, heap = {src: 0}, [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            print(f"pop ({d}, {u})  stale: dist[{u}] is already {dist[u]}, skip")
            continue
        pushed = []
        for v, w in graph[u]:
            if d + w < dist.get(v, math.inf):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
                pushed.append(f"{v}={d + w}")
        print(f"pop ({d}, {u})  settle {u}  push {pushed}  heap={sorted(heap)}")


roads = {"A": [("B", 1), ("C", 5)], "B": [("A", 1), ("D", 2)],
         "C": [("A", 5), ("D", 1)], "D": [("B", 2), ("C", 1)]}
trace_dijkstra(roads, "A")
```

**Try it**
- Make the road A-C cost 3 instead of 5 (in both directions): no stale entry this time, because C's first price is already its best.
- Add `last = max(last, d)` right after the pop, *before* the stale check (start with `last = 0`), and print it at the end: 5, although the farthest node is only 4 away. Anything recorded per pop belongs after the stale check.
- Run `trace_dijkstra({"A": [("B", 1), ("C", 2)], "B": [("D", 1)], "C": [("B", -2)], "D": []}, "A")`: B is settled twice, first at 1 and later at 0. A negative edge broke "popped means final".

### Where it goes wrong

1. **Marking a node when it is pushed (the BFS habit).** A cheaper route can still arrive through a node popped later. With `seen` on push, the second delay example answers 6 instead of 4 (plain BFS gives the same 6).
2. **Stopping when the target is discovered.** Its first price may not be its best: from 1 to 2 in the second delay example you get 4 instead of 2. Return when the target is *popped*.
3. **No stale check while recording at pop time.** Distances still come out right (an out-of-date `d` cannot improve anything), but whatever you record per pop is wrong: the max over pops in the trace graph is 5 instead of 4, and Prim counts a point twice (18 instead of 20).
4. **Negative edges.** "Popped means final" needs `w >= 0`. With `A->B 1, A->C 2, C->B -2, B->D 1`, B is popped at 1 before the cheaper route through C (0) is found. A version that never re-expands a node (a `done` set) leaves D at 2 instead of 1; this lazy version re-pushes B and recovers here, but can take exponential time in general. Negative weights need Bellman-Ford.
5. **0-1 BFS with a plain FIFO.** A free move must go to the *front*; appending it lets a cost-1 entry come out first, and `[[1, 1, 3], [3, 2, 2], [1, 1, 4]]` answers 1 instead of 0.
6. **Bottleneck with the wrong key.** Pushing the step alone instead of `max(t, step)` forgets the worst step so far (the 5×5 Swim in Rising Water grid answers 6 instead of 16).
7. **Unreachable nodes.** They never get a `dist`. Check `len(dist) == n` before taking a max, and return −1 otherwise.
8. **Nodes missing from the graph dict.** `dijkstra({0: [(1, 1)]}, 0)` raises `KeyError: 1`, because node 1 has no entry. Build the graph as a `defaultdict(list)`.
9. **Prim's start with a cost.** Pushing `(5, 0)` instead of `(0, 0)` adds 5 to the total (25 instead of 20). The start joins for free.
10. **Prim on a disconnected edge list.** `while joined < n` pops from an empty heap (`IndexError`) once the reachable part is used up. Loop `while heap and joined < n`, and return −1 if `joined < n`.
11. **Losing edge indexes.** Sorting `edges` in place loses the original numbering that Critical and Pseudo-Critical Edges must return. Sort a list of indexes.
12. **Unorderable heap entries.** On a tie in distance, Python compares the next item of the tuple: pushing `(1, obj)` twice with plain objects raises `TypeError`. Push `(dist, index)` or `(dist, counter, obj)`.

### Edge cases to say out loud

The source alone · an unreachable node (−1) · zero-weight edges · parallel edges (the cheaper one wins) · self-loops (harmless) · one point (MST cost 0) · duplicate points (cost 0) · a disconnected graph for an MST (fewer than n − 1 edges) · equal weights (several MSTs, one total).

```python
assert dijkstra({0: []}, 0) == {0: 0}                                  # the source alone
assert dijkstra({0: [(1, 0)], 1: []}, 0) == {0: 0, 1: 0}               # zero-weight edges are fine
assert dijkstra({0: [(1, 5), (1, 2)], 1: []}, 0)[1] == 2               # parallel edges: the cheaper one wins
assert network_delay_time([], 1, 1) == 0                                # one node hears it at time 0
assert network_delay_time([[1, 2, 1]], 3, 1) == -1                      # node 3 never hears it
assert min_cost_connect_points([[1, 1]]) == 0                           # one point: nothing to connect
assert min_cost_connect_points([[0, 0], [0, 0]]) == 0                   # duplicate points cost 0
assert kruskal(3, [(0, 1, 1)]) == (1, [(0, 1, 1)])                      # disconnected: fewer than n - 1 edges
print("edge cases pass")
```

**Try it**
- Predict `dijkstra({0: [(1, 3)], 1: [(0, 3)]}, 1)` before running it: `{1: 0, 0: 3}`.
- `dijkstra({0: [(0, 5)]}, 0)` is still `{0: 0}`: a loop can never make a path cheaper.
- `min_cost_connect_points([[0, 0], [1, 0], [2, 0]])` is 2: three points on a line, and the tree is the line.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **All distances, then a max** | run to the end; answer = `max(dist.values())`, −1 if a node is missing | 743 |
| **Weights are only 0 or 1** | a deque instead of a heap: weight 0 → `appendleft`, weight 1 → `append` | 1368, 1263 |
| **Dijkstra on a grid or on states** | a node is `(r, c)` or a whole state like `(box, player)`; the loop is unchanged | 1631, 778, 1263 |
| **Minimise the worst step** | key = `max(so_far, step)` instead of a sum | 1631, 778 |
| **Most likely path** | push `-p`: a product of probabilities ≤ 1 never grows along a path | 1514 |
| **At most k edges, or negative weights** | Bellman-Ford: k + 1 rounds, each relaxing every edge from a copy of last round's prices | 787 |
| **MST on a set of points** | Prim with a heap, or the O(n²) array version on a complete graph | 1584 |
| **MST from an edge list** | Kruskal: sort + union-find | 1489 |
| **Hard extras** | several fixed endpoints · which edges matter to the MST | 2203, 1489 |

**Weights are only 0 or 1: 0-1 BFS.** With two possible weights the heap only ever holds two distances, `d` and `d + 1`. A deque keeps that order for free: a free move joins the *front* of the line, a paid move the back. In Minimum Cost to Make a Valid Path, following a cell's arrow is free and turning it costs 1.

```python
ARROWS = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}   # sign in the cell -> direction it points


def min_cost_valid_path(grid):
    rows, cols = len(grid), len(grid[0])
    dist = {(0, 0): 0}
    dq = deque([(0, 0, 0)])                         # (cost, r, c): only two cost values live in here, d and d + 1
    while dq:
        d, r, c = dq.popleft()
        if d > dist[(r, c)]:
            continue                                # stale, exactly like Dijkstra
        if (r, c) == (rows - 1, cols - 1):
            return d
        for sign, (dr, dc) in ARROWS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                w = 0 if grid[r][c] == sign else 1  # follow the arrow for free, turn it for 1
                if d + w < dist.get((nr, nc), math.inf):
                    dist[(nr, nc)] = d + w
                    if w == 0:
                        dq.appendleft((d, nr, nc))  # same cost: jump the line
                    else:
                        dq.append((d + 1, nr, nc))  # one more: back of the line


print(min_cost_valid_path([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]))   # 3
print(min_cost_valid_path([[1, 1, 3], [3, 2, 2], [1, 1, 4]]))                           # 0
print(min_cost_valid_path([[1, 2], [4, 3]]))                                            # 1
```

**Try it**
- Change `dq.appendleft(...)` to `dq.append(...)`, a plain FIFO: `[[1, 1, 3], [3, 2, 2], [1, 1, 4]]` now answers 1 instead of 0. A cost-1 entry got out before the free path arrived.
- Print `[x[0] for x in dq]` just before each `popleft()` on the first grid: only two values ever, `d` and `d + 1`, in order. That is why a deque can replace the heap.
- Swap the deque for `heapq` (push `(d + w, nr, nc)`, pop the smallest): plain Dijkstra, the same three answers, with an extra log factor.

The same deque works on states. In Minimum Moves to Move a Box (1263) a node is `(box, player)`: a player step that does not touch the box costs 0, and walking into the box pushes it one cell for a cost of 1 (if the cell beyond is free). The answer is the cost of the first popped state whose box sits on the target.

**Minimise the worst step: bottleneck Dijkstra.** In Path With Minimum Effort a route is as hard as its *steepest* step; in Swim in Rising Water, as its *highest* cell. Dijkstra still works, because `max` never decreases along a path, just as `+` never decreases with non-negative weights. Only the key changes, so one helper serves both:

```python
def bottleneck_path(rows, cols, start_key, step_key):
    """Smallest possible worst step on a path from (0, 0) to (rows - 1, cols - 1)."""
    best = {(0, 0): start_key}                    # best[cell] = lowest "worst step so far" on a path to it
    heap = [(start_key, 0, 0)]
    while heap:
        t, r, c = heapq.heappop(heap)
        if t > best[(r, c)]:
            continue                              # stale
        if (r, c) == (rows - 1, cols - 1):
            return t                              # popped = final, as in Dijkstra
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nt = max(t, step_key((r, c), (nr, nc)))   # a path is as hard as its worst step: max, not +
                if nt < best.get((nr, nc), math.inf):
                    best[(nr, nc)] = nt
                    heapq.heappush(heap, (nt, nr, nc))


def minimum_effort(h):                            # 1631: a step costs the height difference
    return bottleneck_path(len(h), len(h[0]), 0, lambda a, b: abs(h[b[0]][b[1]] - h[a[0]][a[1]]))


def swim_in_water(g):                             # 778: a step costs the height of the cell you enter
    return bottleneck_path(len(g), len(g), g[0][0], lambda a, b: g[b[0]][b[1]])


print(minimum_effort([[1, 2, 2], [3, 8, 2], [5, 3, 5]]), minimum_effort([[1, 2, 3], [3, 8, 4], [5, 3, 5]]))   # 2 1
print(swim_in_water([[0, 2], [1, 3]]), swim_in_water([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16],
                                                      [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]))                  # 3 16
```

**Try it**
- Push the step alone (`nt = step_key(...)`, no `max`): the 5×5 Swim in Rising Water grid answers 6 instead of 16. The key forgot the worst step on the way.
- Use `t + step_key(...)` instead: the 5×5 grid gives 57, the cheapest *total* climb, which is a different problem.
- `swim_in_water([[3, 2], [0, 1]])` is 3: the start's own height counts, so you cannot leave before the water reaches it. `minimum_effort([[5]])` is 0: one cell, no step at all.

Two other accepted answers for Path With Minimum Effort: binary search on the answer t, with one BFS or DFS per guess asking "can I reach the corner using steps ≤ t?" ([Binary Search](#s09)); or a Kruskal-style sweep that adds edges by weight until the start and the corner share a root. Path With Maximum Probability (1514) is Dijkstra too: a product of probabilities ≤ 1 never grows along a path, so push `-p` and pop the most likely node first.

**At most k edges: Bellman-Ford in rounds (Cheapest Flights Within K Stops).** Plain Dijkstra keeps one price per node, so it cannot also cap the number of edges unless the node becomes (node, edges used). Bellman-Ford counts edges for free: each round relaxes *every* edge once, reading last round's prices, so after round i every node knows its cheapest route with at most i edges. It also tolerates negative weights (V − 1 rounds for plain shortest paths, O(V · E)).

```python
def find_cheapest_price(n, flights, src, dst, k):
    dist = [math.inf] * n
    dist[src] = 0
    for _ in range(k + 1):                 # at most k stops = at most k + 1 flights
        new = dist[:]                      # read last round's prices, write this round's
        for u, v, w in flights:
            if dist[u] + w < new[v]:
                new[v] = dist[u] + w
        dist = new
    return -1 if dist[dst] == math.inf else dist[dst]


print(find_cheapest_price(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1))   # 700
print(find_cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1),
      find_cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0))                             # 200 500
```

**Try it**
- Relax in place (`new = dist` instead of `dist[:]`): with k = 0 the second network answers 200 instead of 500. The flights 0 → 1 and 1 → 2 both slipped into one round, which means two flights for a "zero stops" ticket.
- Allow k = 2 on the first network: 400, along 0 → 1 → 2 → 3.
- `find_cheapest_price(3, [[0, 1, 100]], 0, 2, 1)` is -1: nothing ever flies into 2.

**MST on a set of points, in O(n²).** On a complete graph there are n² edges anyway, so a heap only adds a log factor. Keep `best[j]` = the cheapest edge from the tree to point j, and pick the next point with a plain scan:

```python
def min_cost_connect_points_dense(points):
    n = len(points)
    best = [math.inf] * n                         # best[j] = cheapest edge from the tree to j so far
    best[0] = 0
    in_tree = [False] * n
    total = 0
    for _ in range(n):
        i = min((j for j in range(n) if not in_tree[j]), key=lambda j: best[j])   # an O(n) scan replaces the heap
        in_tree[i] = True
        total += best[i]
        for j in range(n):
            if not in_tree[j]:
                best[j] = min(best[j], abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]))
    return total


print(min_cost_connect_points_dense([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]),
      min_cost_connect_points_dense([[3, 12], [-2, 5], [-4, 1]]))                # 20 18
```

**Try it**
- Forget `best[0] = 0`: the answer becomes `inf`. The first scan still picks point 0, but it joins at an infinite price.
- Print `best` each time a point joins on the 3-point example: `[0, inf, inf]`, `[0, 12, 18]`, `[0, 12, 6]`. An entry only ever goes down: point 2's price drops from 18 to 6 once point 1 is in.
- Compare both versions on random point sets: they always agree. The array version does n² simple steps and keeps no stale entries.

#### Hard extras

**Several fixed endpoints (Minimum Weighted Subgraph).** Two paths, from `src1` and `src2`, must both reach `dest`. Somewhere they meet at a node `x` and share the rest, so the cost is `d1[x] + d2[x] + (x → dest)`. Distances from the sources are two ordinary Dijkstras. "From every x to dest" sounds like n searches, but on the reversed graph it is a single Dijkstra *from* `dest`.

```python
def minimum_weight(n, edges, src1, src2, dest):
    forward, backward = defaultdict(list), defaultdict(list)
    for u, v, w in edges:
        forward[u].append((v, w))
        backward[v].append((u, w))                  # reversed: Dijkstra from dest measures every "x -> dest"
    d1, d2, to_dest = dijkstra(forward, src1), dijkstra(forward, src2), dijkstra(backward, dest)
    best = min((d1[x] + d2[x] + to_dest[x] for x in range(n) if x in d1 and x in d2 and x in to_dest),
               default=math.inf)                    # the two paths meet at x, then share x -> dest
    return -1 if best == math.inf else best


print(minimum_weight(6, [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3], [2, 3, 4],
                         [3, 4, 2], [4, 5, 1]], 0, 1, 5))   # 9
print(minimum_weight(3, [[0, 1, 1], [2, 1, 1]], 0, 1, 2))  # -1
```

**Try it**
- Run the third Dijkstra on `forward` instead of `backward`: 12. Nothing can be reached *from* node 5, so the only meeting point left is 5 itself.
- Print `d1[x]`, `d2[x]` and `to_dest[x]` for every x: meeting at 0 or at 1 both cost 9 (`0 + 3 + 6` and `3 + 0 + 6`).
- `minimum_weight(3, [[0, 2, 5], [1, 2, 5], [0, 1, 1]], 0, 1, 2)` is 6: src1 rides to src2 for 1, then they share 1 → 2. The meeting point can be one of the sources.

**Which edges matter to the MST?** An edge is *critical* if the MST without it is heavier (or impossible), and *pseudo-critical* if it is not critical but some MST uses it: forcing it in first still gives the best weight. Kruskal is cheap, so run it once per question.

```python
def critical_edges(n, edges):
    order = sorted(range(len(edges)), key=lambda i: edges[i][2])   # sort INDEXES: keep the original numbering

    def mst_weight(skip=None, force=None):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        total, used = 0, 0
        for i in ([force] if force is not None else []) + order:   # a forced edge goes in first
            u, v, w = edges[i]
            if i == skip or find(u) == find(v):
                continue
            parent[find(u)] = find(v)
            total, used = total + w, used + 1
        return total if used == n - 1 else math.inf  # not spanning counts as infinitely bad

    best = mst_weight()
    critical = [i for i in range(len(edges)) if mst_weight(skip=i) > best]
    pseudo = [i for i in range(len(edges)) if i not in critical and mst_weight(force=i) == best]
    return [critical, pseudo]


print(critical_edges(5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]]))   # [[0, 1], [2, 3, 4, 5]]
print(critical_edges(4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]]))                                  # [[], [0, 1, 2, 3]]
```

**Try it**
- Let a run that does not span count as a normal weight (`return total`): the path `critical_edges(3, [[0, 1, 1], [1, 2, 1]])` gives `[[], [0, 1]]` instead of `[[0, 1], []]`. Removing a bridge made the "tree" cheaper instead of impossible.
- Drop `i not in critical` from the pseudo-critical test: the critical edges 0 and 1 show up in both lists.
- A triangle with weights 1, 2, 3: `critical_edges(3, [[0, 1, 1], [1, 2, 2], [0, 2, 3]])` is `[[0, 1], []]`. Make all three weights 1 and every edge becomes pseudo-critical: any two of them form an MST.

### Say it in the interview

> "The edges have different costs, so 'fewest edges' isn't 'cheapest' and plain BFS is out. Bellman-Ford would relax every edge V − 1 times, O(V · E). The weights are non-negative, so I'll use Dijkstra: a min-heap of (distance, node). When I pop a node with distance d, any other route to it must leave the settled nodes through something still in the heap, which already costs at least d, and edges can't subtract, so d is final and I relax its edges once. Entries that went out of date are skipped when they surface. With lazy deletion the heap holds up to E entries: O(E log E) = O(E log V)."

> "We need every point connected at minimum total cost, which is a minimum spanning tree. The cheapest edge leaving the tree built so far is always safe, so Prim's grows the tree with a heap of (edge cost, point): O(n² log n) on the complete graph of n points, or O(n²) with the array version."

Point at the stale check, the relax condition, and the line where the answer is read. If the weights are only 0 and 1, say "0-1 BFS" and show the two `append` calls. Follow-ups to expect: negative weights (Bellman-Ford), at most k stops (rounds with a copy), the path itself (`parent[v] = u` on every successful relax, then walk back), a single target (return at its first non-stale pop), and a complete graph (the O(V²) array version).

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree | `graphs/find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree.py` | critical: the MST without it is heavier; pseudo: forcing it in first keeps the MST weight |
| Min Cost to Connect All Points | `graphs/min_cost_to_connect_all_points.py` · `practice/simple/46_min_cost_to_connect_all_points.py` | Prim on the complete graph: heap of (distance, point), skip points already in; or O(n²) with an array |
| Minimum Cost to Make at Least One Valid Path in a Grid | `graphs/minimum_cost_to_make_at_least_one_valid_path_in_a_grid.py` | 0-1 BFS: following the arrow costs 0 (front), turning it costs 1 (back) |
| Minimum Moves to Move a Box to Their Target Location | `graphs/minimum_moves_to_move_a_box_to_their_target_location.py` | 0-1 BFS over (box, player) states: walking costs 0, a push costs 1 |
| Minimum Weighted Subgraph With the Required Paths | `graphs/minimum_weighted_subgraph_with_the_required_paths.py` | Dijkstra from src1, src2, and from dest on reversed edges; minimise over the meeting node |
| Network Delay Time | `graphs/network_delay_time.py` · `practice/simple/45_network_delay_time.py` | Dijkstra from k; answer = the largest distance, −1 if a node is never reached |
| Swim in Rising Water | `graphs/swim_in_rising_water.py` | bottleneck Dijkstra: key = the highest elevation so far; the first pop of the corner wins |

### Self-check

1. Why is a node's distance final when it is popped (and not stale)? What breaks with a negative edge?
<details><summary>Answer</summary>Every other route to that node has to leave the settled region through some node still in the heap, and that node is already at least as far away. Non-negative edges can only add to that, so no other route can be cheaper. A negative edge can subtract, so a route through a node popped <em>later</em> can still undercut a settled distance.</details>

2. In 0-1 BFS, why must a free move go to the front of the deque?
<details><summary>Answer</summary>The deque must stay sorted by cost, like a heap. A free move has the same cost <code>d</code> as the node being expanded, which is the smallest cost in the deque, so it belongs in front of every <code>d + 1</code> entry. Put at the back, it waits behind more expensive entries, and the target can be popped with a cost that is too high.</details>

3. Prim and Dijkstra look almost identical. What is the one real difference?
<details><summary>Answer</summary>The key in the heap. Dijkstra orders nodes by the whole path cost <code>d + w</code> from the source; Prim orders them by the single edge <code>w</code> that would attach them to the tree.</details>

4. Why can't Dijkstra mark a node when it is pushed, as BFS does?
<details><summary>Answer</summary>In BFS every edge costs 1, so the first discovery comes from the closest ring and is already final. With weights, a node first discovered through an expensive edge can still be reached more cheaply through a node that is popped later. Marking it at push time blocks that cheaper route: the second delay example then answers 6 instead of 4.</details>
