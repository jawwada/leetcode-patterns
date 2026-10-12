"""
Kahn's Algorithm - Topological Sort by Peeling Indegree-Zero Nodes

Courses are 0..n-1, and a pair [a, b] means course b must come before course
a. Return an order that takes every course, or [] if the pairs form a cycle:
n = 6, [[3, 0], [3, 1], [4, 3], [2, 3], [5, 4], [5, 2]] -> [0, 1, 3, 4, 2, 5].
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def find_order(num_courses, prerequisites):
    """Take courses whose prerequisites are all done; a cycle never frees up.
    O(V + E) time and space."""
    graph = []
    for _ in range(num_courses):
        graph.append([])
    indegree = [0] * num_courses        # prerequisites not yet taken
    for course, before in prerequisites:
        graph[before].append(course)    # [a, b] is the edge b -> a
        indegree[course] += 1
    queue = deque()
    for course in range(num_courses):
        if indegree[course] == 0:       # free to take right away
            queue.append(course)
    order = []
    while queue:
        course = queue.popleft()
        order.append(course)
        for next_course in graph[course]:
            indegree[next_course] -= 1  # one prerequisite of it is done
            if indegree[next_course] == 0:
                queue.append(next_course)
    if len(order) < num_courses:
        return []                       # the rest wait on each other: a cycle
    return order


# --- try it ---
pairs = [[3, 0], [3, 1], [4, 3], [2, 3], [5, 4], [5, 2]]
print(find_order(6, pairs))                             # -> [0, 1, 3, 4, 2, 5]
print(find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))  # -> [0, 1, 2, 3]
print(find_order(3, [[1, 0], [2, 1], [1, 2]]))          # -> []
print(find_order(2, []))                                # -> [0, 1]
