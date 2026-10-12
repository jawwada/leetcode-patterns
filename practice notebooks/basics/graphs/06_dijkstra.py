"""
Dijkstra's Shortest Paths - Basics
Area: graphs
Key operations: heap of (dist, node), skip stale entries, relax out-edges, a node is final when popped

Given n nodes, directed edges (u, v, w) with w >= 0 and a source, return {node: shortest distance}
for every node reachable from the source. The heap always yields the closest unsettled node; an entry
whose distance is larger than the recorded one is stale and skipped.
Example: n=5, edges [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3)], source 0
         -> {0: 0, 2: 1, 1: 3, 3: 4, 4: 7}
"""
import heapq


# --- brute force ---
def brute_force(n, edges, src):
    """Bellman-Ford: relax every edge n - 1 times. O(n * m); Dijkstra relaxes each edge once, in the right order."""
    dist = {src: 0}
    for _ in range(n - 1):
        for u, v, w in edges:
            if u in dist and dist[u] + w < dist.get(v, float("inf")):
                dist[v] = dist[u] + w
    return dist


# --- optimal ---
def solve(n, edges, src):
    """Pop the closest unsettled node: its distance is final; relax its out-edges and push improvements. O((n + m) log m)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = {src: 0}
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


# --- demo ---
def demo():
    return solve(5, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)], 0)


# --- bugs ---
BUGS = [
    {
        "replace": "        if d > dist[u]:",
        "with":    "        if d >= dist[u]:",
        "fix": "an entry is stale only when it is STRICTLY worse than the recorded distance; the genuine entry has d == dist[u]",
        "why": "The first pop of every node has d == dist[u], so everything is skipped and nothing is relaxed: the result is just {src: 0}.",
        "decoys": [
            {"line": "    dist = {src: 0}", "change": "should start empty"},
            {"line": "                dist[v] = d + w", "change": "should be dist[u] + w"},
            {"line": "    heap = [(0, src)]", "change": "should be [(src, 0)]"},
        ],
    },
    {
        "replace": "                heapq.heappush(heap, (dist[v], v))",
        "with":    "                heapq.heappush(heap, (w, v))",
        "fix": "push the TOTAL distance to v, not the weight of the last edge; the heap orders by distance from the source",
        "why": "Ordering by edge weight pops nodes too early and relaxes from a d that is not the real distance: the example sets dist[3] = 3 instead of 4.",
        "decoys": [
            {"line": "        adj[u].append((v, w))", "change": "should append (w, v)"},
            {"line": "            continue", "change": "should be break"},
            {"line": "        d, u = heapq.heappop(heap)", "change": "should be heap.pop(0)"},
        ],
    },
    {
        "replace": "            if d + w < dist.get(v, float(\"inf\")):",
        "with":    "            if w < dist.get(v, float(\"inf\")):",
        "fix": "compare the full path length d + w with the best known distance to v",
        "why": "A cheap edge from a far-away node overwrites a shorter distance that was already final: with dist[v] = 4 and an edge of weight 3 from a node at distance 10, v becomes 13.",
        "decoys": [
            {"line": "    while heap:", "change": "should be while heap and len(dist) < n"},
            {"line": "    for u, v, w in edges:", "change": "should also add the reverse edge"},
            {"line": "    return dist", "change": "should return sorted(dist)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
