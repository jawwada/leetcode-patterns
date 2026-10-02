"""
Course Schedule (LeetCode 207)  — Medium
Pattern: Topological sort (Kahn's BFS) / cycle detection

Problem
-------
There are numCourses courses 0..n-1 and prerequisites [a, b] meaning "take b before a".
Return True iff it is possible to finish all courses, i.e. the prerequisite graph has no
directed cycle.
Example: numCourses=2, [[1,0]] -> True.  numCourses=2, [[1,0],[0,1]] -> False.

Brute force
-----------
For each course, run a DFS from it and check whether it can reach itself again (a cycle
through that node). Each DFS is O(V + E) and we run it V times -> O(V*(V+E)) time,
O(V) space. The waste: the same edges are re-walked for every start node, and the
sub-paths explored from a node that was already proven cycle-free are explored again.

From brute force to optimal
---------------------------
The redundancy is re-exploring nodes whose "cycle-free" status is already known.
Observation: a node with in-degree 0 cannot be part of any cycle, and removing it can
only lower other in-degrees, never create a cycle. So repeatedly peel off in-degree-0
nodes (Kahn's algorithm): keep a queue of them, pop one, decrement its out-neighbours'
in-degrees, enqueue any that hit 0. Each edge is decremented once -> O(V + E). If the
number of peeled nodes is less than V, the leftovers all have in-degree >= 1, which is
only possible inside a cycle.

Intuition
---------
A course with no outstanding prerequisites can be taken now. Taking it may unlock others.
Keep taking what is unlocked; if you manage to take all n courses, no cycle exists. If you
get stuck with courses remaining, each of them is waiting on another one of them -- a
cycle.

Geometric view
--------------
Draw the courses as nodes with arrows prereq -> course and write each node's in-degree
beside it. The queue holds the nodes labelled 0. Each pop deletes a node and all its
outgoing arrows, decrementing the labels at the arrow tips; new 0s join the queue. A cycle
is a ring of nodes whose labels never fall to 0 because each is held up by the one before.

Steps
-----
1. Build adjacency list prereq -> [courses] and in-degree array.
2. Enqueue all courses with in-degree 0.
3. Pop a course, count it as taken, decrement each dependent's in-degree, enqueue on 0.
4. Return taken == numCourses.

Complexity: O(V + E) time, O(V + E) space — each node is enqueued once and each edge decremented once.
Pitfalls: reversing the edge direction ([a, b] means b -> a); forgetting isolated courses
(they start at in-degree 0 and must be counted); duplicate edges in input (Kahn handles
them because in-degree counts duplicates).
"""
from collections import deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for course, pre in prerequisites:
            adj[pre].append(course)
            indeg[course] += 1
        queue = deque(c for c in range(numCourses) if indeg[c] == 0)
        taken = 0
        while queue:
            cur = queue.popleft()
            taken += 1
            for nxt in adj[cur]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
        return taken == numCourses


def brute_force(numCourses: int, prerequisites: List[List[int]]) -> bool:
    # From every course, DFS along prereq -> course edges and see if we come back to it.
    adj = [[] for _ in range(numCourses)]
    for course, pre in prerequisites:
        adj[pre].append(course)
    for start in range(numCourses):
        seen, stack = set(), list(adj[start])
        while stack:
            cur = stack.pop()
            if cur == start:
                return False
            if cur not in seen:
                seen.add(cur)
                stack.extend(adj[cur])
    return True


if __name__ == "__main__":
    s = Solution()
    cases = (
        (2, [[1, 0]], True),
        (2, [[1, 0], [0, 1]], False),
        (1, [], True),
        (4, [[1, 0], [2, 1], [3, 2]], True),
        (3, [[0, 1], [1, 2], [2, 0]], False),
        (5, [[1, 4], [2, 4], [3, 1], [3, 2]], True),
    )
    for n, pre, want in cases:
        assert brute_force(n, pre) == want
        assert s.canFinish(n, pre) == want
    print("ok")
