"""
Course Schedule (LeetCode 207) - Medium
Chapter: graphs
Pattern: Topological sort (Kahn's BFS) / cycle detection

There are numCourses courses labelled 0..n-1, and prerequisites [a, b] means course b must be
taken before course a. Return true if it is possible to finish every course, i.e. the
prerequisite graph has no directed cycle.
Example: numCourses=2, [[1,0]] -> true; numCourses=2, [[1,0],[0,1]] -> false.
"""
from collections import deque      # popleft is O(1)


# --- brute force ---
def brute_force(num_courses, prerequisites):
    """Walk forward from every course; getting back to the start means a cycle. O(V(V+E)) time."""
    unlocks = []                     # unlocks[pre] = the courses that need pre first
    for _ in range(num_courses):
        unlocks.append([])
    for course, pre in prerequisites:
        unlocks[pre].append(course)
    for start in range(num_courses):
        seen = set()
        stack = unlocks[start][:]
        while stack:
            cur = stack.pop()
            if cur == start:         # walked back to where we began: a cycle
                return False
            if cur not in seen:
                seen.add(cur)
                for nxt in unlocks[cur]:
                    stack.append(nxt)
    return True


# --- optimal ---
def course_schedule(num_courses, prerequisites):
    """Kahn's algorithm: keep taking a course that has no prerequisites left. O(V+E) time."""
    unlocks = []                     # unlocks[pre] = the courses that need pre first
    for _ in range(num_courses):
        unlocks.append([])
    waiting_on = [0] * num_courses   # how many prerequisites each course still waits on
    for course, pre in prerequisites:
        unlocks[pre].append(course)
        waiting_on[course] += 1
    queue = deque()
    for course in range(num_courses):
        if waiting_on[course] == 0:
            queue.append(course)
    taken = 0
    while queue:
        cur = queue.popleft()
        taken += 1
        for nxt in unlocks[cur]:
            waiting_on[nxt] -= 1
            if waiting_on[nxt] == 0:     # its last prerequisite is done: it can be taken now
                queue.append(nxt)
    return taken == num_courses      # anything left over is stuck on a cycle


# --- try the brute force ---
print(brute_force(2, [[1, 0]]))                    # -> True
print(brute_force(2, [[1, 0], [0, 1]]))            # -> False
print(brute_force(4, [[1, 0], [2, 1], [3, 2]]))    # -> True
print(brute_force(3, [[0, 1], [1, 2], [2, 0]]))    # -> False


# --- try the optimal ---
print(course_schedule(2, [[1, 0]]))                    # -> True
print(course_schedule(2, [[1, 0], [0, 1]]))            # -> False
print(course_schedule(4, [[1, 0], [2, 1], [3, 2]]))    # -> True
print(course_schedule(3, [[0, 1], [1, 2], [2, 0]]))    # -> False
