"""
Shortest Path Visiting All Nodes (LeetCode 847) - Hard
Chapter: graphs
Pattern: BFS over augmented states (position + bitmask/budget)

An undirected connected graph with n <= 12 nodes is given as adjacency lists. Return the length
of the shortest walk that visits every node at least once; you may start anywhere and may
revisit nodes and edges.
Example: [[1,2,3],[0],[0],[0]] -> 4 via 1-0-2-0-3.
"""
from collections import deque            # popleft is O(1)
from itertools import permutations       # every ordering of a sequence, as tuples


# --- brute force ---
def distances_from(graph, source):
    """Plain BFS: the number of edges from source to every node."""
    distance = [-1] * len(graph)
    distance[source] = 0
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if distance[neighbour] == -1:
                distance[neighbour] = distance[node] + 1
                queue.append(neighbour)
    return distance


def brute_force(graph):
    """All-pairs distances, then try every order of first visits. O(n! * n) time."""
    n = len(graph)
    distance = []                                  # distance[a][b] = shortest path a -> b
    for source in range(n):
        distance.append(distances_from(graph, source))
    best = -1
    for order in permutations(range(n)):           # n! orders; shared prefixes are redone
        total = 0
        for i in range(n - 1):
            total += distance[order[i]][order[i + 1]]
        if best == -1 or total < best:
            best = total
    return best


# --- optimal ---
def shortest_path_visiting_all_nodes(graph):
    """BFS over states (node, set of visited nodes as a bitmask). O(n^2 * 2^n) time, O(n * 2^n)."""
    n = len(graph)
    if n == 1:
        return 0
    everyone = (1 << n) - 1                        # bitmask with all n bits set
    queue = deque()
    seen = set()
    for node in range(n):                          # start anywhere, at distance 0
        queue.append((node, 1 << node, 0))
        seen.add((node, 1 << node))
    while queue:
        node, visited, length = queue.popleft()
        for neighbour in graph[node]:
            new_visited = visited | (1 << neighbour)
            if new_visited == everyone:
                return length + 1
            if (neighbour, new_visited) not in seen:      # a node may repeat, a state may not
                seen.add((neighbour, new_visited))
                queue.append((neighbour, new_visited, length + 1))
    return -1


# --- try the brute force ---
print(brute_force([[1, 2, 3], [0], [0], [0]]))                               # -> 4
print(brute_force([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]]))                 # -> 4
print(brute_force([[]]))                                                     # -> 0
print(brute_force([[1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5]]))       # -> 6
print(brute_force([[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]]))                 # -> 5


# --- try the optimal ---
print(shortest_path_visiting_all_nodes([[1, 2, 3], [0], [0], [0]]))                          # -> 4
print(shortest_path_visiting_all_nodes([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]]))            # -> 4
print(shortest_path_visiting_all_nodes([[]]))                                                # -> 0
print(shortest_path_visiting_all_nodes([[1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5]]))  # -> 6
print(shortest_path_visiting_all_nodes([[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]]))            # -> 5
