"""
Course Schedule (LeetCode 207) - Medium
Area: graphs
Key operations: adjacency prereq -> course plus indegrees, queue the indegree-0 courses, pop and release dependents, cycle iff taken < n

There are n courses 0..n-1 and prerequisites [a, b] meaning b must be taken before a. Return True
iff every course can be taken, i.e. the prerequisite graph has no directed cycle.
Example: n = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]] -> True (0, then 1 and 2, then 3)
         n = 2, prerequisites = [[1, 0], [0, 1]] -> False
"""
from collections import deque
from typing import List


# --- brute force ---
def brute_force(n: int, prerequisites: List[List[int]]) -> bool:
    """DFS with three colours: white = unvisited, gray = on the current path, black = finished. An edge
    into a gray node closes a cycle. Also O(V + E), but a different method: recursive, path based, and it
    yields no order to take the courses in; Kahn's queue needs no recursion and reads the order off."""
    adj = [[] for _ in range(n)]
    for course, pre in prerequisites:
        adj[pre].append(course)
    color = [0] * n

    def has_cycle(u: int) -> bool:
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1 or (color[v] == 0 and has_cycle(v)):
                return True
        color[u] = 2
        return False

    return not any(color[u] == 0 and has_cycle(u) for u in range(n))


# --- optimal ---
def solve(n: int, prerequisites: List[List[int]]) -> bool:
    """Kahn: take any course with indegree 0, then lower the indegree of everything it unlocks; a course
    that hits 0 joins the queue. If fewer than n courses get taken, the rest sit on a cycle. O(V + E)."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for course, pre in prerequisites:
        adj[pre].append(course)
        indeg[course] += 1
    queue = deque(c for c in range(n) if indeg[c] == 0)
    taken = 0
    while queue:
        cur = queue.popleft()
        taken += 1
        for nxt in adj[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return taken == n


# --- demo ---
def demo():
    return solve(4, [[1, 0], [2, 0], [3, 1], [3, 2]])


# --- bugs ---
BUGS = [
    {
        "replace": "        adj[pre].append(course)",
        "with":    "        adj[course].append(pre)",
        "fix": "edges point prereq -> course: finishing pre is what releases course",
        "why": "The adjacency is reversed while the indegrees are not, so taking a course releases the wrong side and n = 2, [[1, 0]] returns False.",
        "decoys": [
            {"line": "    queue = deque(c for c in range(n) if indeg[c] == 0)", "change": "should start with every course"},
            {"line": "            if indeg[nxt] == 0:", "change": "should be indeg[nxt] <= 0"},
            {"line": "    return taken == n", "change": "should be return not queue"},
        ],
    },
    {
        "replace": "            indeg[nxt] -= 1",
        "with":    "            indeg[cur] -= 1",
        "fix": "decrement the dependent course nxt, the one that just lost a prerequisite",
        "why": "The popped course is decremented instead of its dependents, so nothing new ever reaches 0 and any graph with an edge reports a cycle.",
        "decoys": [
            {"line": "        taken += 1", "change": "should move inside the for loop"},
            {"line": "        cur = queue.popleft()", "change": "should be queue.pop()"},
            {"line": "    indeg = [0] * n", "change": "should be [1] * n"},
        ],
    },
    {
        "replace": "        indeg[course] += 1",
        "with":    "        indeg[pre] += 1",
        "fix": "the course that has the prerequisite gains the indegree, not the prerequisite",
        "why": "Indegrees now count outgoing edges, so courses with prerequisites start free and real prerequisites never do: n = 2, [[1, 0]] returns False.",
        "decoys": [
            {"line": "    adj = [[] for _ in range(n)]", "change": "should have n + 1 lists"},
            {"line": "                queue.append(nxt)", "change": "should append cur"},
            {"line": "    return taken == n", "change": "should be taken >= n - 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
