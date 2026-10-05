"""
Prim's Minimum Spanning Tree - Fundamentals
Chapter: fundamentals/graphs
Key operations: heap of (weight, node, parent), skip a popped node already in the tree, push edges

Given n nodes, weighted undirected edges (u, v, w) and a start node, grow one tree from the start:
the heap holds the edges leaving the tree, always take the cheapest, ignore it if its far end is
already inside. Return the total weight and the tree edges (parent, node, w) in the order added.
Example: n=5, edges [(0,1,4),(0,2,1),(1,2,2),(1,3,5),(2,3,8),(3,4,3)], start 0
         -> (11, [(0,2,1), (2,1,2), (1,3,5), (3,4,3)])
"""
import heapq                       # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def build_adjacency(n, edges):
    """adj[u] lists (weight, neighbour) pairs; an undirected edge goes both ways. O(n + m)."""
    adj = []
    for _ in range(n):
        adj.append([])
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    return adj


def prim(n, edges, start):
    """Pop the cheapest crossing edge; skip it if it leads into the tree, else add. O(m log m)."""
    adj = build_adjacency(n, edges)
    in_tree = set()
    total = 0
    tree = []
    heap = [(0, start, start)]         # (weight, node, parent); the start has no real parent
    while heap and len(in_tree) < n:
        w, node, parent = heapq.heappop(heap)
        if node in in_tree:
            continue                   # stale entry: node joined the tree through a cheaper edge
        in_tree.add(node)
        if node != start:
            total += w
            tree.append((parent, node, w))
        for next_w, neighbour in adj[node]:
            if neighbour not in in_tree:
                heapq.heappush(heap, (next_w, neighbour, node))
    return total, tree


# --- try it ---
print(prim(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3)], 0))
# -> (11, [(0, 2, 1), (2, 1, 2), (1, 3, 5), (3, 4, 3)])
print(prim(4, [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4)], 0))
# -> (7, [(0, 1, 1), (1, 2, 2), (2, 3, 4)])
print(prim(3, [(0, 1, 2), (1, 2, 1), (0, 2, 3)], 2))              # -> (3, [(2, 1, 1), (1, 0, 2)])
