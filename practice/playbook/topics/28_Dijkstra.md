## Dijkstra's Algorithm

For nonnegative edge weights, repeatedly pop the smallest tentative distance from a min-heap. Skip obsolete heap entries and relax outgoing edges. A cheaper route discovered later can replace a tentative distance, so do not finalize a node when it is first pushed.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Add `print(d, u)` right after the `heappop` and run the second example: node 2 comes out twice, at 2 (real) and at 4 (stale, skipped).
- The BFS habit: keep a `seen` set, add `v` when you push it, and skip neighbours already seen. The second example answers 6 instead of 4: node 2 was locked in at 4 by the direct edge before 1 → 3 → 2 (cost 2) was found. A Dijkstra node is final when it is popped.
- Change `d > dist[u]` to `d >= dist[u]`: all three examples answer -1. Even the very first entry, `(0, src)`, now looks stale.
- Give `dijkstra` a `target` and return at discovery (`if v == target: return d + w` right after `dist[v] = d + w`): from 1 to 2 in the second example you get 4 instead of 2. Discovery-time checks are safe in BFS, where every edge costs 1, not here.

<!-- cell -->

### Watch it work

The trace runs Dijkstra on the picture's graph and prints one line per pop: a pop either settles its node and offers the neighbours, or is skipped as stale. Watch C come out twice, once at its old price and once at its real one.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Make the road A-C cost 3 instead of 5 (in both directions): no stale entry this time, because C's first price is already its best.
- Add `last = max(last, d)` right after the pop, *before* the stale check (start with `last = 0`), and print it at the end: 5, although the farthest node is only 4 away. Anything recorded per pop belongs after the stale check.
- Run `trace_dijkstra({"A": [("B", 1), ("C", 2)], "B": [("D", 1)], "C": [("B", -2)], "D": []}, "A")`: B is settled twice, first at 1 and later at 0. A negative edge broke "popped means final".

<!-- cell -->

```python
assert dijkstra({0: []}, 0) == {0: 0}                                  # the source alone

assert dijkstra({0: [(1, 0)], 1: []}, 0) == {0: 0, 1: 0}               # zero-weight edges are fine

assert dijkstra({0: [(1, 5), (1, 2)], 1: []}, 0)[1] == 2               # parallel edges: the cheaper one wins

assert network_delay_time([], 1, 1) == 0                                # one node hears it at time 0

assert network_delay_time([[1, 2, 1]], 3, 1) == -1                      # node 3 never hears it
```

<!-- cell -->

The second pattern changes the key instead of the container. Path With Minimum Effort asks for the route between the top-left and bottom-right cells whose steepest step, the largest height difference between neighbours, is as small as possible: 2 for the first grid below. Swim in Rising Water asks for the lowest water level at which you can swim between the same corners, a cell being open once the water reaches its height: 16 for the 5 × 5 grid.

Dijkstra still works, because `max` never decreases along a path, just as `+` never does with non-negative weights. "A path is as bad as its worst step" is `max(t, step)` in place of `d + w`, and only that key changes, so one helper serves both problems.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Push the step alone (`nt = step_key(...)`, no `max`): the 5×5 Swim in Rising Water grid answers 6 instead of 16. The key forgot the worst step on the way.
- Use `t + step_key(...)` instead: the 5×5 grid gives 57, the cheapest *total* climb, which is a different problem.
- `swim_in_water([[3, 2], [0, 1]])` is 3: the start's own height counts, so you cannot leave before the water reaches it. `minimum_effort([[5]])` is 0: one cell, no step at all.

<!-- cell -->

Path With Minimum Effort has two other accepted answers. One is binary search on the answer t, with one BFS or DFS per guess asking "can I reach the corner using steps ≤ t?" ([Binary Search](11_Binary_Search.ipynb#topic-binary-search)). The other is a Kruskal-style sweep that adds edges by weight until the start and the corner share a root.

Path With Maximum Probability (1514) asks for the most likely path between two nodes when each edge succeeds with its own probability, and it is Dijkstra too. A product of probabilities ≤ 1 never grows along a path, so push `-p` and pop the most likely node first.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Minimum Weighted Subgraph With the Required Paths gives a weighted directed graph and asks for the lightest set of edges through which both `src1` and `src2` can reach `dest`, or -1: 9 for the graph below. The two paths meet at some node x and share the rest, so the cost is `d1[x] + d2[x] + (x → dest)`. Distances from the sources are two ordinary Dijkstras, and "from every x to dest" sounds like n searches, but on the reversed graph it is a single Dijkstra *from* `dest`.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Run the third Dijkstra on `forward` instead of `backward`: 12. Nothing can be reached *from* node 5, so the only meeting point left is 5 itself.
- Print `d1[x]`, `d2[x]` and `to_dest[x]` for every x: meeting at 0 or at 1 both cost 9 (`0 + 3 + 6` and `3 + 0 + 6`).
- `minimum_weight(3, [[0, 2, 5], [1, 2, 5], [0, 1, 1]], 0, 1, 2)` is 6: src1 rides to src2 for 1, then they share 1 → 2. The meeting point can be one of the sources.
