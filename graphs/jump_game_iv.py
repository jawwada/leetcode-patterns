"""
Jump Game IV (LeetCode 1345)  — Hard
Pattern: BFS on implicit graph with value buckets consumed once

Problem
-------
From index i of arr you may jump to i+1, i-1, or to any j with arr[j] == arr[i]. Return the
minimum number of jumps from index 0 to the last index.
Example: arr=[100,-23,-23,404,100,23,23,23,3,404] -> 3  (0 -> 4 -> 3 -> 9).

Brute force
-----------
Plain BFS where the neighbours of index i are found by scanning the whole array for every j
with arr[j] == arr[i], plus i-1 and i+1. Each pop costs O(n), there are up to n pops: O(n^2)
time, O(n) space. The wasted work is rescanning for the same value again and again: once the
first index holding value v is popped, EVERY index with value v is already visited, yet each of
those indices rescans the full array when it is popped in turn.

From brute force to optimal
---------------------------
First redundancy: scanning for equal values. Pre-bucket indices by value (dict value -> list) so
the same-value neighbours are a lookup, not a scan. That alone is not enough: an array of n
equal values makes every pop iterate a bucket of size n, still O(n^2). Second observation: the
first time any index of value v is popped, BFS marks all of v's indices visited, so the bucket
can never contribute again. Clear (or pop) the bucket after its first use. The invariant is
that each bucket is iterated at most once over the whole run, so the total work over all pops
is O(n) for buckets plus O(n) for the +-1 edges, and BFS gives the shortest jump count.

Intuition
---------
The jumps define an unweighted graph on indices, so BFS by layers yields the minimum number of
jumps. Same-value edges form cliques; a clique only needs to be expanded once because the very
first expansion reaches all of its members, and everything beyond that is repeat work.

Geometric view
--------------
Indices on a line with +-1 steps as short hops, and each value as a "teleporter" connecting all
of its indices. BFS expands a frontier one layer at a time; when the frontier first touches a
teleporter, all of its endpoints light up in the next layer and the teleporter switches off.

Steps
-----
1. where[v] = list of indices with value v.
2. BFS from 0 with a seen array and a level counter.
3. For popped i: neighbours = where[arr[i]] plus i-1 and i+1 (in bounds, unseen).
4. After using where[arr[i]], remove the bucket so it is never iterated again.
5. Return the level when n-1 is popped (n == 1 -> 0).

Complexity: O(n) time, O(n) space — each index enqueued once, each bucket consumed once.
Pitfalls: not clearing buckets (O(n^2) on arrays of equal values, TLE); forgetting n == 1;
          marking seen when popping instead of when pushing (duplicates in the queue).
"""
import random
from collections import defaultdict, deque
from typing import List


class Solution:
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        if n == 1:
            return 0
        where = defaultdict(list)
        for i, v in enumerate(arr):
            where[v].append(i)
        seen = [False] * n
        seen[0] = True
        queue = deque([0])
        jumps = 0
        while queue:
            for _ in range(len(queue)):
                i = queue.popleft()
                if i == n - 1:
                    return jumps
                nbrs = where.pop(arr[i], [])         # take the bucket once; never rescan it
                nbrs.extend((i - 1, i + 1))
                for j in nbrs:
                    if 0 <= j < n and not seen[j]:
                        seen[j] = True
                        queue.append(j)
            jumps += 1
        return -1                                     # unreachable: +1 steps always arrive


def brute_force(arr: List[int]) -> int:
    # BFS, but neighbours are found by scanning the whole array for equal values at every pop.
    n = len(arr)
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        if i == n - 1:
            return dist[i]
        nbrs = [j for j in range(n) if arr[j] == arr[i]] + [i - 1, i + 1]   # O(n) scan
        for j in nbrs:
            if 0 <= j < n and dist[j] == -1:
                dist[j] = dist[i] + 1
                queue.append(j)
    return dist[n - 1]


if __name__ == "__main__":
    s = Solution()
    assert s.minJumps([100, -23, -23, 404, 100, 23, 23, 23, 3, 404]) == 3
    assert s.minJumps([7]) == 0
    assert s.minJumps([7, 6, 9, 6, 9, 6, 9, 7]) == 1
    assert s.minJumps([6, 1, 9]) == 2
    assert s.minJumps([11, 22, 7, 7, 7, 7, 7, 7, 7, 22, 13]) == 3
    assert s.minJumps([5] * 1000) == 1                              # the O(n^2) trap

    random.seed(3)
    for _ in range(300):
        a = [random.randint(0, 4) for _ in range(random.randint(1, 15))]
        assert s.minJumps(a) == brute_force(a)
    print("ok")
