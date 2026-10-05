"""
Union-Find (Disjoint Set Union) - Basics
Area: graphs
Key operations: find with path compression, union by size, connected query, component count

Maintain n elements 0..n-1 in disjoint sets. union(a, b) merges the sets of a and b, connected(a, b)
says whether they share a set, and count is the number of sets. solve applies the unions in order
and answers each query.
Example: n=6, unions [(0,1),(1,2),(3,4),(0,2)], queries [(0,2),(2,3),(4,3),(5,5)]
         -> [True, False, True, True], 3 components {0,1,2} {3,4} {5}
"""
from collections import deque


# --- brute force ---
def brute_force(n, unions, queries):
    """BFS over the union edges for every query. O(q * (n + m)); union-find answers each query in near O(1)."""
    adj = [[] for _ in range(n)]
    for a, b in unions:
        adj[a].append(b)
        adj[b].append(a)

    def reach(s):
        seen, q = {s}, deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        return seen

    return [b in reach(a) for a, b in queries]


# --- optimal ---
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression: point x straight at the root
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra  # ra is the bigger root; the smaller tree hangs under it
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)


def solve(n, unions, queries):
    """Apply the unions, then answer every query with two finds. Near O(1) amortized per operation."""
    dsu = DSU(n)
    for a, b in unions:
        merged = dsu.union(a, b)
    ans = [dsu.connected(a, b) for a, b in queries]
    return ans


# --- demo ---
def demo():
    return solve(6, [(0, 1), (1, 2), (3, 4), (0, 2)], [(0, 2), (2, 3), (4, 3), (5, 5)])


# --- bugs ---
BUGS = [
    {
        "replace": "        self.parent[rb] = ra",
        "with":    "        self.parent[b] = ra",
        "fix": "hang the ROOT rb under ra; re-pointing the element b leaves its old root as a separate set",
        "why": "When b is not a root, its root keeps parent == itself, so the two sets stay apart: unions (0,1),(2,3),(1,3) leave 0 and 2 disconnected.",
        "decoys": [
            {"line": "        if self.size[ra] < self.size[rb]:", "change": "should be <="},
            {"line": "        self.size[ra] += self.size[rb]", "change": "should add 1"},
            {"line": "        self.count -= 1", "change": "should move before the if ra == rb check"},
        ],
    },
    {
        "replace": "        return self.parent[x]",
        "with":    "        return x",
        "fix": "find returns the ROOT, which after compression is self.parent[x], not x itself",
        "why": "Every find returns its argument, so union compares elements instead of roots and connected(0, 2) is False after union(0, 1), union(1, 2).",
        "decoys": [
            {"line": "        if self.parent[x] != x:", "change": "should be == x"},
            {"line": "            return False", "change": "should return True"},
            {"line": "        return self.find(a) == self.find(b)", "change": "should compare parent[a] == parent[b]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
