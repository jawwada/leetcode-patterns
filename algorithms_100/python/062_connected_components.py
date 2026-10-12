"""
Connected Components - Count and Label by Flood Fill

Given n nodes 0..n-1 and an undirected edge list, count the connected
components and label every node with the number of its component:
n = 7, [[0, 1], [1, 2], [3, 4], [3, 5]] -> (3, [0, 0, 0, 1, 1, 1, 2]).
"""


# --- algorithm ---
def connected_components(n, edges):
    """Each unlabeled node floods its whole component with a new label.
    O(V + E) time."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)              # undirected: store both directions
        graph[v].append(u)
    label = [-1] * n                    # -1 means not reached yet
    count = 0
    for start in range(n):
        if label[start] == -1:          # not reached by any earlier flood
            flood(graph, start, count, label)
            count += 1
    return count, label


def flood(graph, start, mark, label):
    """Paint every node reachable from start with mark, using a stack.
    O(nodes + edges) of that component."""
    label[start] = mark
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if label[neighbor] == -1:
                label[neighbor] = mark  # label when pushed: pushed only once
                stack.append(neighbor)


# --- try it ---
edges = [[0, 1], [1, 2], [3, 4], [3, 5]]
print(connected_components(7, edges))       # -> (3, [0, 0, 0, 1, 1, 1, 2])
print(connected_components(3, []))          # -> (3, [0, 1, 2])
chain = [[3, 2], [1, 0], [2, 1]]
print(connected_components(4, chain))       # -> (1, [0, 0, 0, 0])
