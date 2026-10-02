"""
Find the Town Judge (LeetCode 997)  — Easy
Pattern: Degree counting (in-degree minus out-degree)

Problem
-------
n people are labelled 1..n; trust[i] = [a, b] means a trusts b. The town judge trusts
nobody and is trusted by everybody else. Return the judge's label, or -1 if none exists.
Example: n=3, trust=[[1,3],[2,3]] -> 3.  n=3, trust=[[1,3],[2,3],[3,1]] -> -1.

Brute force
-----------
For each candidate j, scan the whole trust list twice: does j trust anybody, and how many
distinct people trust j? O(n * len(trust)) time, O(n) space. The waste: every candidate
re-reads every edge, although each edge only ever affects two people's counts.

From brute force to optimal
---------------------------
The redundancy is re-scanning all edges per candidate. Observation: the judge is exactly
the vertex with in-degree n-1 and out-degree 0 in the trust graph, and both degrees can
be tallied for every vertex in one pass over the edges. Fold them into one number:
score = in - out. Since in <= n-1 (no duplicate edges, no self-trust), score == n-1 forces
in == n-1 and out == 0. One pass + one scan: O(n + len(trust)). The user's original
two-dict version is the same idea; this keeps it as a single array.

Intuition
---------
A judge is a sink that every other vertex points to. Every edge gives +1 to its head and
-1 to its tail; only a perfect sink can accumulate the maximum possible n-1.

Geometric view
--------------
Draw n dots and the trust arrows. The judge is the dot with an arrow arriving from every
other dot and no arrow leaving it: a star with all spokes pointing inward.

Steps
-----
1. score = [0] * (n + 1).
2. For each (a, b): score[a] -= 1, score[b] += 1.
3. Return the first i in 1..n with score[i] == n - 1, else -1.

Complexity: O(n + t) time, O(n) space — one pass over edges, one over people.
Pitfalls: n == 1 with no edges (answer 1, handled since score[1] == 0 == n-1); checking
only in-degree (a person trusted by all may also trust someone).
"""
from typing import List


class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        score = [0] * (n + 1)
        for a, b in trust:
            score[a] -= 1  # out-edge disqualifies
            score[b] += 1
        for person in range(1, n + 1):
            if score[person] == n - 1:
                return person
        return -1


def brute_force(n: int, trust: List[List[int]]) -> int:
    # For each candidate, rescan every edge: O(n * len(trust)).
    for j in range(1, n + 1):
        trusts_someone = any(a == j for a, _ in trust)
        trusted_by = {a for a, b in trust if b == j}
        if not trusts_someone and len(trusted_by) == n - 1:
            return j
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = [(2, [[1, 2]], 2),
             (3, [[1, 3], [2, 3]], 3),
             (3, [[1, 3], [2, 3], [3, 1]], -1),
             (1, [], 1),
             (4, [[1, 3], [1, 4], [2, 3], [2, 4], [4, 3]], 3)]
    for n, t, want in cases:
        assert s.findJudge(n, t) == want
        assert brute_force(n, t) == want
    print("ok")
