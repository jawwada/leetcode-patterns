"""
Union-Find (basics: graphs)
Keep elements 0..n-1 in disjoint sets: merge two sets, ask if two elements share one, count sets.
  n = 6, unions (0,1) (1,2) (3,4) (0,2), queries (0,2) (2,3) (4,3) (5,5)
    ->  [True, False, True, True], 3 sets: {0,1,2} {3,4} {5}

Idea: each set is a tree named by its root, so "same set?" means "same root?".
      Path compression points nodes straight at the root and union by size hangs the smaller
      tree under the bigger one; the trees stay flat, so every operation is near O(1).

Pseudocode:
  find(x):          if parent[x] != x: parent[x] = find(parent[x])     # compress the path
                    return parent[x]
  union(a, b):      ra, rb = find(a), find(b); if ra == rb: return False
                    hang the smaller root under the bigger; add the sizes; count -= 1
  connected(a, b):  return find(a) == find(b)

Time near O(1) amortized per operation, space O(n).
"""


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))     # everyone starts as its own root
        self.size = [1] * n              # tree sizes (read at roots)
        self.count = n                   # number of sets

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:                     # already in the same set
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra              # make ra the bigger root
        self.parent[rb] = ra             # smaller tree hangs under the bigger
        self.size[ra] += self.size[rb]
        self.count -= 1                  # two sets became one
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)


if __name__ == "__main__":
    uf = UnionFind(6)
    for a, b in [(0, 1), (1, 2), (3, 4), (0, 2)]:    # (0, 2) is already joined
        uf.union(a, b)
    print(uf.connected(0, 2), uf.connected(2, 3), uf.connected(4, 3))  # True False True
    print(uf.count)                                                    # 3
    print(uf.union(2, 3), uf.count)                                    # True 2
