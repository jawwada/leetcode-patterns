"""
Clone Graph - The Old-to-New Map Doubles as Visited

Given one node of a connected undirected graph, where every node has a value
and a list of neighbors, return a deep copy of the whole graph. Row i of the
adjacency list holds the neighbors of node i + 1:
[[2, 4], [1, 3], [2, 4], [1, 3]] -> the same list, built from all-new nodes.
"""
from collections import deque      # popleft is O(1)


# --- helpers ---
class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []


def build_graph(adjacency):
    """Make node i + 1 for row i, link the listed neighbors, return node 1."""
    if not adjacency:
        return None
    nodes = []
    for i in range(len(adjacency)):
        nodes.append(Node(i + 1))
    for i in range(len(adjacency)):
        for value in adjacency[i]:
            nodes[i].neighbors.append(nodes[value - 1])
    return nodes[0]


def collect_nodes(node):
    """Every node reachable from node, in BFS order. O(V + E)."""
    if node is None:
        return []
    seen = set()
    seen.add(node)
    order = [node]
    queue = deque([node])
    while queue:
        current = queue.popleft()
        for neighbor in current.neighbors:
            if neighbor not in seen:
                seen.add(neighbor)
                order.append(neighbor)
                queue.append(neighbor)
    return order


def graph_to_list(node):
    """Adjacency list of the graph: row i lists node i + 1's neighbors."""
    nodes = collect_nodes(node)
    rows = []
    for i in range(len(nodes)):
        rows.append([])
    for current in nodes:
        for neighbor in current.neighbors:
            rows[current.val - 1].append(neighbor.val)
    return rows


def shares_a_node(first, second):
    """True if the two graphs have any node object in common."""
    originals = set(collect_nodes(first))
    for node in collect_nodes(second):
        if node in originals:
            return True
    return False


# --- algorithm ---
def clone_graph(node):
    """BFS; the map old -> copy makes each copy once and is the visited set.
    O(V + E) time, O(V) extra space."""
    if node is None:
        return None
    copies = {}                             # old node -> its copy
    copies[node] = Node(node.val)
    queue = deque([node])
    while queue:
        current = queue.popleft()
        for neighbor in current.neighbors:
            if neighbor not in copies:      # first sighting: copy, visit later
                copies[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            copies[current].neighbors.append(copies[neighbor])  # copy to copy
    return copies[node]


# --- try it ---
original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
clone = clone_graph(original)
print(graph_to_list(clone))                # -> [[2, 4], [1, 3], [2, 4], [1, 3]]
print(shares_a_node(original, clone))      # -> False
path = build_graph([[2], [1, 3], [2]])
print(graph_to_list(clone_graph(path)))    # -> [[2], [1, 3], [2]]
print(graph_to_list(clone_graph(build_graph([[]]))))    # -> [[]]
print(clone_graph(None))                   # -> None
