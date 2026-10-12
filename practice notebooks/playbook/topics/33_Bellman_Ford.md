## Bellman–Ford

Relax every edge in rounds. Reading only the previous round's distances enforces an edge budget. The example allows at most k stops, hence k + 1 edges. Without a reachable negative cycle, V − 1 rounds suffice for ordinary shortest paths.

<!-- cell -->

A cap on the number of edges breaks plain Dijkstra, and rounds handle it. Cheapest Flights Within K Stops asks for the cheapest price from `src` to `dst` with at most k stops, or -1: on the first network below, k = 1 allows 0 → 1 → 3 for 700. Dijkstra keeps one price per node, so it cannot also cap the number of edges unless the node becomes (node, edges used).

Bellman-Ford counts edges for free. Each round relaxes *every* edge once, reading last round's prices, so after round i every node knows its cheapest route with at most i edges. It also tolerates negative weights: V − 1 rounds find plain shortest paths in O(V · E).

<!-- cell -->

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

<!-- cell -->

**Try it**
- Relax in place (`new = dist` instead of `dist[:]`): with k = 0 the second network answers 200 instead of 500. The flights 0 → 1 and 1 → 2 both slipped into one round, which means two flights for a "zero stops" ticket.
- Allow k = 2 on the first network: 400, along 0 → 1 → 2 → 3.
- `find_cheapest_price(3, [[0, 1, 100]], 0, 2, 1)` is -1: nothing ever flies into 2.
