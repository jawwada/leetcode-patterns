"""
Course Schedule (LeetCode 207)
Can you finish all n courses, given pairs [course, prerequisite]?
  n = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]  ->  True   (0, then 1 and 2, then 3)

Idea: a course is ready when it has no unfinished prerequisites (indegree 0).
      Take ready courses one by one (Kahn's topological sort); courses on a cycle never become ready.

Pseudocode:
  build adj (pre -> course) and indegree counts
  queue = all courses with indegree 0
  while queue:
      cur = pop; taken += 1
      for nxt in adj[cur]:
          indegree[nxt] -= 1
          if indegree[nxt] == 0: push nxt
  return taken == n

Time O(V + E), space O(V + E).
"""
from collections import deque


def can_finish(n, prerequisites):
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    for course, pre in prerequisites:            # edge pre -> course
        adj[pre].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(n) if indegree[c] == 0)
    taken = 0
    while queue:
        cur = queue.popleft()
        taken += 1
        for nxt in adj[cur]:
            indegree[nxt] -= 1                   # one prerequisite done
            if indegree[nxt] == 0:               # now ready
                queue.append(nxt)
    return taken == n                            # leftovers sit on a cycle


if __name__ == "__main__":
    print(can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))  # True
    print(can_finish(2, [[1, 0], [0, 1]]))                  # False
