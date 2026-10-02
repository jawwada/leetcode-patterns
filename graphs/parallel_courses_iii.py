"""
Parallel Courses III (LeetCode 2050)  — Hard
Pattern: Topological order + longest-path relaxation (Kahn)

Problem
-------
n courses labelled 1..n, relations [prev, next] meaning prev must be finished before next can
start, and time[i] is how many months course i+1 takes. Unlimited courses may run in parallel
once their prerequisites are done. Return the minimum number of months to finish every course.
Example: n=3, relations=[[1,3],[2,3]], time=[3,2,5] -> 8  (1 and 2 run together; 3 starts at
month 3 and ends at month 8).

Brute force
-----------
finish(c) = time[c] + max(finish(p) for every prerequisite p). Without a fixed visiting order
we can only sweep ALL edges repeatedly, Bellman-Ford style, raising finish[next] whenever
finish[prev] + time[next] beats it, until a full sweep changes nothing. Up to n sweeps of E
edges: O(V*E) time, O(V) space. The wasted work is re-relaxing every edge in every sweep,
although an edge can only change its target after its source has changed.

From brute force to optimal
---------------------------
The redundancy is re-checking edges whose source finish time is still provisional. The
observation: finish(c) depends only on courses that precede c in a topological order, so if we
visit courses in Kahn's order (pop a course only when its in-degree is 0), every prerequisite is
FINAL at the moment c is popped. The structure is the in-degree queue plus one array finish[c].
Instead of each course pulling the max from its prerequisites, each popped course pushes into
its dependants: finish[nxt] = max(finish[nxt], finish[cur] + time[nxt]); when nxt's in-degree
drops to 0 its value is complete and it joins the queue. Every edge is relaxed exactly once, so
the longest node-weighted path in the DAG costs O(V + E) instead of O(V*E).

Intuition
---------
Courses with no prerequisites start at month 0 and end at time[c]. Any other course starts the
instant its slowest prerequisite ends, so its finish is time[c] + max over prerequisites. The
answer is the longest path in the DAG with weights on the nodes, and Kahn's order guarantees
that when a node leaves the queue all of its incoming edges have already delivered their max.

Geometric view
--------------
Draw the DAG left to right in layers; each node carries a bar of length time[c], like a Gantt
chart. A bar starts at the right end of the longest chain of bars ending at any prerequisite.
The answer is the rightmost end over all bars: the critical path.

Steps
-----
1. Build adjacency prev -> [next] and the in-degree array (convert to 0-indexed).
2. finish[c] = time[c] for every c; enqueue all in-degree-0 courses.
3. Pop cur (its finish is final). For each dependant nxt:
   finish[nxt] = max(finish[nxt], finish[cur] + time[nxt]); decrement in-degree; enqueue at 0.
4. Return max(finish).

Complexity: O(V + E) time, O(V + E) space — each edge relaxed once; adjacency list plus arrays.
Pitfalls: the input is 1-indexed; adding time[cur] again (finish[cur] already contains it);
          reading finish[c] before c has been popped (its max is not final yet).
"""
import random
from collections import deque
from typing import List


class Solution:
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        adj = [[] for _ in range(n)]
        indeg = [0] * n
        for prev, nxt in relations:
            adj[prev - 1].append(nxt - 1)
            indeg[nxt - 1] += 1
        finish = time[:]                        # no prerequisites -> ends at time[c]
        queue = deque(c for c in range(n) if indeg[c] == 0)
        while queue:
            cur = queue.popleft()               # finish[cur] is final: every prerequisite popped
            for nxt in adj[cur]:
                finish[nxt] = max(finish[nxt], finish[cur] + time[nxt])
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
        return max(finish)


def brute_force(n: int, relations: List[List[int]], time: List[int]) -> int:
    # Bellman-Ford style: sweep EVERY edge until a whole sweep changes nothing (<= n sweeps).
    finish = time[:]
    changed = True
    while changed:
        changed = False
        for prev, nxt in relations:
            cand = finish[prev - 1] + time[nxt - 1]
            if cand > finish[nxt - 1]:
                finish[nxt - 1] = cand
                changed = True
    return max(finish)


if __name__ == "__main__":
    s = Solution()
    assert s.minimumTime(3, [[1, 3], [2, 3]], [3, 2, 5]) == 8
    assert s.minimumTime(5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]) == 12
    assert s.minimumTime(1, [], [7]) == 7                         # single course, no edges
    assert s.minimumTime(3, [], [4, 9, 2]) == 9                   # all parallel -> slowest

    random.seed(1)
    for _ in range(300):
        n = random.randint(1, 8)
        label = list(range(1, n + 1))
        random.shuffle(label)                                     # hide the DAG order
        rel = [[label[i], label[j]] for i in range(n) for j in range(i + 1, n)
               if random.random() < 0.4]
        t = [random.randint(1, 9) for _ in range(n)]
        assert s.minimumTime(n, rel, t) == brute_force(n, rel, t)
    print("ok")
