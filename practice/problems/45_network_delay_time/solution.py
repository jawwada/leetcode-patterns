"""
Network Delay Time (LeetCode 743) - Medium
Area: graphs
Key operations: heap pop the closest node, skip stale entries, relax out-edges, push improved arrival times

There are n nodes labelled 1..n and directed edges times[i] = [u, v, w]: a signal sent from u
reaches v after w units. A signal is sent from node k. Return the time at which ALL nodes have
received it, or -1 if some node never does.
Example: times = [[1,2,4],[1,3,1],[3,2,1],[2,4,2]], n = 4, k = 1 -> 4
"""
import heapq
from collections import defaultdict
from typing import List


# --- brute force ---
def brute_force(times: List[List[int]], n: int, k: int) -> int:
    """Bellman-Ford: n - 1 rounds, each relaxing EVERY edge. O(V * E). The waste: every round
    rescans all edges, including those leaving nodes whose distance did not change."""
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    worst = max(dist[1:])
    return -1 if worst == INF else worst


# --- optimal ---
def solve(times: List[List[int]], n: int, k: int) -> int:
    """Dijkstra: pop the unsettled node with the smallest arrival time (it is final), relax its
    out-edges, skip stale heap entries. O((V + E) log V)."""
    INF = float("inf")
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
    dist = {k: 0}  # best arrival time found so far
    heap = [(0, k)]  # (arrival time, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist.get(v, INF):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1


# --- demo ---
def demo():
    return solve([[1, 2, 4], [1, 3, 1], [3, 2, 1], [2, 4, 2]], 4, 1)


# --- bugs ---
BUGS = [
    {
        "replace": "        if d > dist[u]:",
        "with":    "        if d >= dist[u]:",
        "fix": "an entry is stale only when it is strictly worse: if d > dist[u]",
        "why": "Every entry is popped with d == dist[u] the first time, so >= skips every node including the source; nothing is relaxed and the example returns -1.",
        "decoys": [
            {"line": "    dist = {k: 0}  # best arrival time found so far", "change": "should start empty: dist = {}"},
            {"line": "    heap = [(0, k)]  # (arrival time, node)", "change": "should be [(k, 0)]"},
            {"line": "        adj[u].append((v, w))", "change": "should append (w, v)"},
        ],
    },
    {
        "replace": "            if d + w < dist.get(v, INF):",
        "with":    "            if v not in dist:",
        "fix": "relax whenever the new time improves: if d + w < dist.get(v, INF)",
        "why": "Recording only the FIRST time a node is seen keeps a long direct edge over a shorter two-hop path: [[1,2,1],[2,3,1],[1,3,5]] from 1 returns 5 instead of 2.",
        "decoys": [
            {"line": "        d, u = heapq.heappop(heap)", "change": "should be u, d = heapq.heappop(heap)"},
            {"line": "        if d > dist[u]:", "change": "should be if u in dist"},
            {"line": "    return max(dist.values()) if len(dist) == n else -1", "change": "should return sum(dist.values())"},
        ],
    },
    {
        "replace": "                heapq.heappush(heap, (d + w, v))",
        "with":    "                heapq.heappush(heap, (w, v))",
        "fix": "push the total arrival time d + w, not the edge weight",
        "why": "The heap then orders nodes by their last edge instead of by arrival time, so nodes are settled in the wrong order and the recorded times are wrong on chains like [[2,1,1],[2,3,1],[3,4,1]].",
        "decoys": [
            {"line": "                dist[v] = d + w", "change": "should be dist[u] = d + w"},
            {"line": "        for v, w in adj[u]:", "change": "should iterate adj[v]"},
            {"line": "    while heap:", "change": "should be while heap and len(dist) < n"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
