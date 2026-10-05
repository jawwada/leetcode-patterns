"""
Clone Graph (LeetCode 133) - Medium
Chapter: graphs
Pattern: Graph traversal with old->new node map

Given a reference to one node of a connected undirected graph, where each node has an integer
val (1..n, unique) and a list of neighbors, return a deep copy of the whole graph.
Example: the 4-cycle with adjacency [[2,4],[1,3],[2,4],[1,3]] must come back as an identical
graph made of brand-new Node objects.
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []


def build_graph(adj):
    """adj[i] lists the 1-based neighbours of node i + 1; return node 1 (None if adj is empty)."""
    if not adj:
        return None
    nodes = []
    for i in range(len(adj)):
        nodes.append(Node(i + 1))
    for i in range(len(adj)):
        for j in adj[i]:
            nodes[i].neighbors.append(nodes[j - 1])
    return nodes[0]


def graph_to_list(node):
    """Walk the graph from node and return [neighbour values of node 1, of node 2, ...]."""
    if node is None:
        return []
    values_of = {}                   # node value -> sorted list of neighbour values
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.val in values_of:
            continue
        values = []
        for nb in cur.neighbors:
            values.append(nb.val)
            stack.append(nb)
        values_of[cur.val] = sorted(values)
    result = []
    for val in sorted(values_of):
        result.append(values_of[val])
    return result


# --- brute force ---
def brute_force(node):
    """Collect all nodes, copy each, then find every neighbour's copy by a linear scan. O(V*E)."""
    if node is None:
        return None
    originals = []
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur in originals:
            continue
        originals.append(cur)
        for nb in cur.neighbors:
            stack.append(nb)
    copies = []
    for original in originals:
        copies.append(Node(original.val))
    for i in range(len(originals)):
        for nb in originals[i].neighbors:
            for copy in copies:      # linear search: which copy has this neighbour's value?
                if copy.val == nb.val:
                    copies[i].neighbors.append(copy)
                    break
    return copies[0]


# --- optimal ---
def clone_graph(node):
    """BFS once; a dict original -> copy creates each copy once and doubles as visited. O(V+E)."""
    if node is None:
        return None
    clones = {node: Node(node.val)}
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb not in clones:     # first sight of nb: make its copy and plan to visit it
                clones[nb] = Node(nb.val)
                queue.append(nb)
            clones[cur].neighbors.append(clones[nb])   # link copy to copy, never to an original
    return clones[node]


# --- try the brute force ---
print(graph_to_list(brute_force(build_graph([[2, 4], [1, 3], [2, 4], [1, 3]]))))  # -> same 4-cycle
print(graph_to_list(brute_force(build_graph([[2], [1, 3], [2]]))))      # -> [[2], [1, 3], [2]]
print(graph_to_list(brute_force(build_graph([[]]))))                              # -> [[]]
print(graph_to_list(brute_force(build_graph([]))))                                # -> []


# --- try the optimal ---
print(graph_to_list(clone_graph(build_graph([[2, 4], [1, 3], [2, 4], [1, 3]]))))  # -> same 4-cycle
print(graph_to_list(clone_graph(build_graph([[2], [1, 3], [2]]))))      # -> [[2], [1, 3], [2]]
print(graph_to_list(clone_graph(build_graph([[]]))))                              # -> [[]]
print(graph_to_list(clone_graph(build_graph([]))))                                # -> []
