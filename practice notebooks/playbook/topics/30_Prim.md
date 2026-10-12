## Prim's Minimum Spanning Tree Algorithm

Grow one connected tree by repeatedly taking the cheapest edge from the tree to an outside node. The heap key is the cost of that joining edge, rather than a path distance. The first vertex joins for cost zero. A dense graph can use a scan instead of a heap.

<!-- cell -->

Min Cost to Connect All Points asks for the cheapest way to connect points on a plane, where joining two points costs their Manhattan distance, `|x1 − x2| + |y1 − y2|`: the five points below cost 20. It is a minimum spanning tree of the complete graph, so there is no edge list; the "edges" from a point are its distances to every point still outside the tree. "The cheapest edge leaving the tree" is a pop that skips any point already in.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Delete the `if in_tree[i]: continue` lines: the first example answers 18. Point 3 is popped a second time and counted as a fifth join, so the loop stops before point 2 ever joins.
- Start the heap with `(5, 0)` instead of `(0, 0)`: 25. The start must join for free.
- Print `i, cost` when a point joins: 0 (0), 1 (4), 3 (3), 4 (4), 2 (9). The costs are not sorted: Prim takes the cheapest edge leaving the *current* tree, not the cheapest edge overall.

<!-- cell -->

```python
assert min_cost_connect_points([[1, 1]]) == 0                           # one point: nothing to connect

assert min_cost_connect_points([[0, 0], [0, 0]]) == 0                   # duplicate points cost 0
```

<!-- cell -->

On a complete graph the heap can go. There are n² edges anyway, so a heap only adds a log factor: keep `best[j]`, the cheapest edge from the tree to point j, and pick the next point with a plain scan. The five points of Min Cost to Connect All Points cost 20 again, and the three points `[[3, 12], [-2, 5], [-4, 1]]` cost 18.

<!-- cell -->

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

<!-- cell -->

**Try it**
- Forget `best[0] = 0`: the answer becomes `inf`. The first scan still picks point 0, but it joins at an infinite price.
- Print `best` each time a point joins on the 3-point example: `[0, inf, inf]`, `[0, 12, 18]`, `[0, 12, 6]`. An entry only ever goes down: point 2's price drops from 18 to 6 once point 1 is in.
- Compare both versions on random point sets: they always agree. The array version does n² simple steps and keeps no stale entries.
