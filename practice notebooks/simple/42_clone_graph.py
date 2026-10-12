"""
Clone Graph (LeetCode 133)
Return a deep copy of a connected undirected graph (every node brand new).
  4-cycle 1-2-3-4-1  ->  a new 4-cycle 1-2-3-4-1 built from fresh nodes

Idea: BFS over the original graph. A dict old -> new does two jobs:
      it is the visited set, and it finds the clone of any neighbour in O(1).

Pseudocode:
  clones = {start: Node(start.val)}
  queue = [start]
  while queue:
      cur = pop
      for nb in cur.neighbors:
          if nb not in clones: clones[nb] = Node(nb.val); push nb   # first sight
          clones[cur].neighbors.append(clones[nb])                  # wire the copy

Time O(V + E), space O(V).
"""
from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []


def clone_graph(start):
    if start is None:
        return None
    clones = {start: Node(start.val)}            # old node -> new node
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb not in clones:                 # first time we see nb
                clones[nb] = Node(nb.val)
                queue.append(nb)
            clones[cur].neighbors.append(clones[nb])   # clone -> clone edge
    return clones[start]


if __name__ == "__main__":
    a, b, c, d = Node(1), Node(2), Node(3), Node(4)
    a.neighbors, b.neighbors, c.neighbors, d.neighbors = [b, d], [a, c], [b, d], [a, c]
    copy = clone_graph(a)
    print(copy.val, [n.val for n in copy.neighbors])   # 1 [2, 4]
    print(copy is a, copy.neighbors[0] is b)           # False False
    print(clone_graph(None))                           # None
