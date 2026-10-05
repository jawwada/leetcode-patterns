"""
Number of Islands II (LeetCode 305) - Hard
Chapter: graphs
Pattern: Union-Find (disjoint set union)

An m x n grid starts as all water. Each positions[i] = (r, c) turns that cell into land, one
operation at a time; after each operation report the number of islands (4-directionally
connected land groups). A cell may be added twice; the second add changes nothing.
Example: m = 3, n = 3, positions = [[0,0],[0,1],[1,2],[2,1]] -> [1, 1, 2, 3]
"""


# --- brute force ---
def count_islands(land):
    """Flood-fill from every land cell not yet seen; each flood is one island."""
    seen = set()
    islands = 0
    for cell in land:
        if cell in seen:
            continue
        islands += 1
        seen.add(cell)
        stack = [cell]
        while stack:
            row, col = stack.pop()
            for nb in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
                if nb in land and nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
    return islands


def brute_force(m, n, positions):
    """After every add, recount all the islands from scratch by flood fill. O(k * m * n)."""
    land = set()
    out = []
    for row, col in positions:
        land.add((row, col))
        out.append(count_islands(land))    # rediscovers every island that already existed
    return out


# --- optimal ---
def find(parent, x):
    """Root of x in the union-find, halving the path on the way up."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def number_of_islands_ii(m, n, positions):
    """New land is +1 island; each distinct neighbouring island it touches merges in, -1. O(k)."""
    parent = {}                        # union-find keyed by row * n + col, land cells only
    count = 0
    out = []
    for row, col in positions:
        key = row * n + col
        if key in parent:
            out.append(count)          # duplicate add: nothing changes
            continue
        parent[key] = key
        count += 1
        for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
            if nr < 0 or nr >= m or nc < 0 or nc >= n:
                continue
            nb = nr * n + nc
            if nb not in parent:
                continue               # still water
            root_new = find(parent, key)
            root_nb = find(parent, nb)
            if root_new != root_nb:    # a different island (two neighbours may share one root)
                parent[root_nb] = root_new
                count -= 1
        out.append(count)
    return out


# --- try the brute force ---
print(brute_force(3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]]))    # -> [1, 1, 2, 3]
print(brute_force(1, 1, [[0, 0]]))                            # -> [1]
print(brute_force(3, 3, [[0, 0], [0, 0], [1, 1], [0, 1]]))    # -> [1, 1, 2, 1]
print(brute_force(2, 2, [[0, 0], [1, 1], [0, 1], [1, 0]]))    # -> [1, 2, 1, 1]


# --- try the optimal ---
print(number_of_islands_ii(3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]]))    # -> [1, 1, 2, 3]
print(number_of_islands_ii(1, 1, [[0, 0]]))                            # -> [1]
print(number_of_islands_ii(3, 3, [[0, 0], [0, 0], [1, 1], [0, 1]]))    # -> [1, 1, 2, 1]
print(number_of_islands_ii(2, 2, [[0, 0], [1, 1], [0, 1], [1, 0]]))    # -> [1, 2, 1, 1]
