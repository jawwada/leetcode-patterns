"""
Find All People With Secret (LeetCode 2092)  — Hard
Pattern: Time-grouped union-find with reset of non-informed components

Problem
-------
n people (0..n-1). Person 0 shares a secret with firstPerson at time 0. meetings[i] = [x, y, t]
means x and y meet at time t; if either knows the secret then, both do, and within the same
time t the secret keeps spreading along chains of meetings instantly. Return everyone who knows
the secret after all meetings (any order).
Example: n=6, meetings=[[1,2,5],[2,3,8],[1,5,10]], firstPerson=1 -> [0,1,2,3,5].

Brute force
-----------
Sort meetings by time and process each time group. Inside a group, sweep the group's meetings
again and again, marking both people known whenever exactly one of them knows, until a whole
sweep changes nothing. A group of g meetings may need g sweeps: O(g^2) per group, O(m^2) total
in the worst case, O(n) space. The wasted work is re-sweeping meetings between two people whose
status already settled, just to carry the secret one hop further per sweep.

From brute force to optimal
---------------------------
The redundancy is propagating one hop per sweep. Within one time group the question is purely
"which people are connected (through this group's meetings) to someone who already knows?", a
connectivity question that union-find answers in near-O(1) per edge. So union the pairs of the
group, then every person whose root equals root(0) knows. The catch: connections made at time t
must NOT persist to later times (an uninformed pair that met at t=5 does not share a secret
learnt at t=8). The invariant that fixes it: after each group, reset every participant who is
not in 0's component back to a singleton (parent[p] = p). People in 0's component stay merged
forever, which is exactly right because knowing is permanent. Each meeting costs two finds and
a union, so the total is O(m log m) for the sort plus O((n + m) alpha(n)).

Intuition
---------
Treat person 0 as the permanent "knows" root. At one timestamp, everyone linked to that root
by the meetings of that timestamp learns the secret, no matter how long the chain. Links that
never touched the root carry no information and must be forgotten before the next timestamp.

Geometric view
--------------
Picture the people as dots and each time group as a temporary set of ropes between dots. Pull
on dot 0: every dot that moves is informed and gets glued to 0 permanently. Then cut all ropes
that are not attached to the glued blob; the loose dots fall back to being separate.

Steps
-----
1. parent = identity; union(firstPerson, 0).
2. Sort meetings by time and iterate over the groups of equal time.
3. For each meeting in the group, union(x, y).
4. For each participant p of the group, if find(p) != find(0): parent[p] = p (forget the link).
5. Answer: every p with find(p) == find(0).

Complexity: O(m log m + (n + m) alpha(n)) time, O(n + m) space — sort dominates; DSU arrays.
Pitfalls: forgetting to reset uninformed participants (secret leaks across time); resetting
          BEFORE checking the whole group (a chain through a not-yet-checked person is lost);
          treating firstPerson as the only seed and forgetting person 0.
"""
import random
from itertools import groupby
from typing import List


class Solution:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]        # path halving
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        union(firstPerson, 0)
        by_time = sorted(meetings, key=lambda m: m[2])
        for _, grp in groupby(by_time, key=lambda m: m[2]):
            group = list(grp)
            for x, y, _ in group:
                union(x, y)
            for x, y, _ in group:                     # links that never reached 0 are forgotten
                if find(x) != find(0):
                    parent[x] = x
                if find(y) != find(0):
                    parent[y] = y
        return [p for p in range(n) if find(p) == find(0)]


def brute_force(n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
    # Per time group, re-sweep that group's meetings until nobody new learns the secret.
    known = [False] * n
    known[0] = known[firstPerson] = True
    by_time = sorted(meetings, key=lambda m: m[2])
    for _, grp in groupby(by_time, key=lambda m: m[2]):
        group = list(grp)
        changed = True
        while changed:
            changed = False
            for x, y, _ in group:
                if known[x] != known[y]:              # one hop of spreading per sweep
                    known[x] = known[y] = True
                    changed = True
    return [p for p in range(n) if known[p]]


if __name__ == "__main__":
    s = Solution()
    assert s.findAllPeople(6, [[1, 2, 5], [2, 3, 8], [1, 5, 10]], 1) == [0, 1, 2, 3, 5]
    assert s.findAllPeople(4, [[3, 1, 3], [1, 2, 2], [0, 3, 3]], 3) == [0, 1, 3]
    assert s.findAllPeople(5, [[3, 4, 2], [1, 2, 1], [2, 3, 1]], 1) == [0, 1, 2, 3, 4]
    # 3-4 met before anyone of them knew; 4-5 met with no knower -> both links forgotten
    assert s.findAllPeople(6, [[1, 2, 5], [3, 4, 5], [2, 3, 8], [4, 5, 10]], 1) == [0, 1, 2, 3]
    assert s.findAllPeople(2, [], 1) == [0, 1]                    # no meetings at all

    random.seed(7)
    for _ in range(300):
        n = random.randint(2, 9)
        m = random.randint(0, 12)
        meet = []
        for _ in range(m):
            x, y = random.sample(range(n), 2)
            meet.append([x, y, random.randint(1, 4)])
        first = random.randrange(n)
        assert s.findAllPeople(n, meet, first) == brute_force(n, meet, first)
    print("ok")
