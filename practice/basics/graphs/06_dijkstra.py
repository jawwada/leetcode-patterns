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
import sys
import heapq

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
            log(f"pop ({d}, {u}): STALE, dist[{u}] is already {dist[u]} | heap {heap}")
            continue
        log(f"pop ({d}, {u}): FINAL, dist[{u}] = {d}; relax its out-edges {adj[u]}")
        for v, w in adj[u]:
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
                log(f"    relax {u}->{v} w={w}: dist[{v}] = {d + w}, push ({d + w}, {v})")
        log(f"    heap {heap} dist {dist}")
    return dist


# --- demo ---
def demo():
    return solve(5, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)], 0)


# --- tests ---
def tests():
    E = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]
    assert solve(5, E, 0) == {0: 0, 2: 1, 1: 3, 3: 4, 4: 7}
    assert solve(5, E, 3) == {3: 0, 4: 3}  # unreachable nodes are absent
    assert solve(1, [], 0) == {0: 0}
    assert solve(3, [(0, 1, 2), (0, 1, 1), (1, 0, 5)], 0) == {0: 0, 1: 1}  # parallel edges and a back edge
    assert solve(3, [(0, 1, 0), (1, 2, 0)], 0) == {0: 0, 1: 0, 2: 0}  # zero weights
    assert solve(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 3, 10)], 0) == {0: 0, 1: 1, 2: 2, 3: 3}  # long cheap path beats the direct edge
    import random
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(rng.randint(0, 14))]
        edges = [(u, v, w) for u, v, w in edges if u != v]
        src = rng.randrange(n)
        assert solve(n, edges, src) == brute_force(n, edges, src), (n, edges, src)


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
