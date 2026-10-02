"""
Course Schedule II (LeetCode 210)  — Medium
Pattern: Topological sort (Kahn's BFS) / cycle detection

Problem
-------
Same setup as Course Schedule: numCourses courses, prerequisites [a, b] = "b before a".
Return ANY valid ordering of all courses, or [] if none exists.
Example: numCourses=4, [[1,0],[2,0],[3,1],[3,2]] -> [0,1,2,3] (or [0,2,1,3]).

Brute force
-----------
Repeatedly scan the full prerequisite list to find a course all of whose prerequisites
are already in the output; append it; repeat until n courses are placed or a full scan
finds nothing (cycle). Each scan is O(V + E) and up to V scans are needed -> O(V*(V+E))
time, O(V) space. The waste is rescanning every edge each round even though only the
edges leaving the course just placed could have changed anyone's readiness.

From brute force to optimal
---------------------------
The redundancy is recomputing "is this course ready?" for all courses after each
placement. Observation: readiness only changes for the direct dependents of the course
just placed, and it is a simple counter (remaining prerequisites == in-degree). Maintain
in-degrees, keep a queue of ready (in-degree 0) courses, and when a course is placed
decrement only its dependents. Each edge is touched exactly once -> O(V + E). The order
in which courses leave the queue IS a topological order.

Intuition
---------
Kahn's algorithm with the pop order recorded. A course leaves the queue only after every
prerequisite has already left, so writing courses in pop order guarantees prerequisites
come first. If the output is shorter than n, a cycle blocked the rest -- return [].

Geometric view
--------------
Nodes with in-degree labels; a conveyor belt (the queue) on the left. Nodes labelled 0
fall onto the belt. Each node taken off the belt is appended to the output row and its
outgoing arrows are cut, decrementing labels at the arrow tips; newly-zero nodes fall onto
the belt. The output row grows left to right in dependency order.

Steps
-----
1. Build adjacency prereq -> [courses] and in-degree array.
2. Enqueue all in-degree-0 courses.
3. Pop, append to order, decrement dependents, enqueue those that hit 0.
4. Return order if len(order) == numCourses else [].

Complexity: O(V + E) time, O(V + E) space — each node enqueued once, each edge relaxed once.
Pitfalls: returning a partial order when a cycle exists; edge direction; assuming the
answer is unique (tests accept any valid order, so compare by validating, not by equality).
"""
from collections import deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for course, pre in prerequisites:
            adj[pre].append(course)
            indeg[course] += 1
        queue = deque(c for c in range(numCourses) if indeg[c] == 0)
        order = []
        while queue:
            cur = queue.popleft()
            order.append(cur)
            for nxt in adj[cur]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
        return order if len(order) == numCourses else []


def brute_force(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    # Each round, rescan all courses and all prerequisites to find one that is ready.
    placed, order = set(), []
    while len(order) < numCourses:
        progress = False
        for c in range(numCourses):
            if c in placed:
                continue
            if all(pre in placed for course, pre in prerequisites if course == c):
                placed.add(c)
                order.append(c)
                progress = True
                break
        if not progress:
            return []
    return order


def valid(order: List[int], n: int, prerequisites: List[List[int]]) -> bool:
    if sorted(order) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(order)}
    return all(pos[pre] < pos[course] for course, pre in prerequisites)


if __name__ == "__main__":
    s = Solution()
    cases = (
        (2, [[1, 0]], True),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),
        (1, [], True),
        (2, [[1, 0], [0, 1]], False),
        (3, [[1, 0], [2, 1], [0, 2]], False),
    )
    for n, pre, possible in cases:
        got, bf = s.findOrder(n, pre), brute_force(n, pre)
        if possible:
            assert valid(got, n, pre) and valid(bf, n, pre)
        else:
            assert got == [] and bf == []
    assert s.findOrder(2, [[1, 0]]) == [0, 1]
    print("ok")
