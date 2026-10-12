"""
Graph DFS, Recursive and Iterative (basics: searches)
Return the order in which DFS visits the nodes reachable from start in a directed graph.
  graph = {0: [1, 2], 1: [3], 2: [3], 3: []}, start = 0  ->  [0, 1, 3, 2]

Idea: go deep along the first unvisited neighbour, back up when stuck, then try the next one.
      An explicit stack gives the same order only if neighbours are pushed in REVERSE
      (first neighbour on top) and a node is marked when POPPED (stale copies get skipped).

Pseudocode:
  dfs_recursive(u):
      mark u, record u
      for v in graph[u]: if v not seen: dfs_recursive(v)

  dfs_iterative(start):
      stack = [start]
      while stack:
          u = pop
          if u seen: continue            # stale copy, already visited
          mark u, record u
          push graph[u] in reverse order

Time O(V + E), space O(V + E) (the stack may hold stale copies).
"""


def dfs_recursive(graph, start):
    order, seen = [], set()

    def visit(u):
        seen.add(u)
        order.append(u)
        for v in graph[u]:
            if v not in seen:
                visit(v)                 # go deeper before the next neighbour

    visit(start)
    return order


def dfs_iterative(graph, start):
    order, seen, stack = [], set(), [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue                     # stale copy, already visited
        seen.add(u)                      # mark when popped, not when pushed
        order.append(u)
        stack.extend(reversed(graph[u]))  # first neighbour ends on top
    return order


if __name__ == "__main__":
    graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
    print(dfs_recursive(graph, 0))                        # [0, 1, 3, 2]
    print(dfs_iterative(graph, 0))                        # [0, 1, 3, 2]
    print(dfs_iterative({0: [1, 2], 1: [2], 2: [0]}, 0))  # [0, 1, 2]
