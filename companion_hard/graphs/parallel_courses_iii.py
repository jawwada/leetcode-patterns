"""
Parallel Courses III (LeetCode 2050) - Hard
Chapter: graphs
Pattern: Topological order + longest-path relaxation (Kahn)

There are n courses labelled 1..n. relations[i] = [prev, next] means prev must finish before next
can start, and time[c - 1] is how many months course c takes. Any number of courses may run in
parallel once their prerequisites are done. Return the minimum months to finish every course.
Example: n = 3, relations = [[1,3],[2,3]], time = [3,2,5] -> 8 (1 and 2 run together; 3 runs 3..8).
"""
from collections import deque      # popleft is O(1)


# --- brute force ---
def brute_force(n, relations, time):
    """Sweep every relation again and again until nothing improves (Bellman-Ford style). O(n*E)."""
    finish = time[:]                               # a course with no prerequisite ends at time[c]
    changed = True
    while changed:                                 # at most n sweeps, each over every edge
        changed = False
        for prev, nxt in relations:
            candidate = finish[prev - 1] + time[nxt - 1]
            if candidate > finish[nxt - 1]:        # a later prerequisite pushes nxt later
                finish[nxt - 1] = candidate
                changed = True
    return max(finish)


# --- optimal ---
def minimum_time(n, relations, time):
    """Kahn's order: a course's finish is final when its in-degree hits 0. O(n + E) time."""
    unlocks = []                                   # unlocks[c] = courses that need c first
    in_degree = [0] * n                            # how many prerequisites each course has
    for course in range(n):
        unlocks.append([])
    for prev, nxt in relations:
        unlocks[prev - 1].append(nxt - 1)
        in_degree[nxt - 1] += 1
    finish = time[:]                               # no prerequisites -> ends at time[c]
    queue = deque()
    for course in range(n):
        if in_degree[course] == 0:
            queue.append(course)
    while queue:
        course = queue.popleft()                   # finish[course] is final: all prereqs popped
        for nxt in unlocks[course]:
            finish[nxt] = max(finish[nxt], finish[course] + time[nxt])
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
    return max(finish)


# --- try the brute force ---
print(brute_force(3, [[1, 3], [2, 3]], [3, 2, 5]))                                   # -> 8
print(brute_force(5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]))     # -> 12
print(brute_force(1, [], [7]))                                                       # -> 7
print(brute_force(3, [], [4, 9, 2]))                                                 # -> 9


# --- try the optimal ---
print(minimum_time(3, [[1, 3], [2, 3]], [3, 2, 5]))                                   # -> 8
print(minimum_time(5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]))     # -> 12
print(minimum_time(1, [], [7]))                                                       # -> 7
print(minimum_time(3, [], [4, 9, 2]))                                                 # -> 9
