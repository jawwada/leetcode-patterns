"""
Minimum Interval to Include Each Query (LeetCode 1851)  — Hard
Pattern: Offline queries sorted + sweep by start + min-heap by size with lazy removal

Problem
-------
Given intervals [left, right] and queries q, answer each query with the size
(right - left + 1) of the smallest interval containing q, or -1 if none does. Answers must be
returned in the original query order.
Example: intervals=[[1,4],[2,4],[3,6],[4,4]], queries=[2,3,4,5] -> [3,3,1,4].

Brute force
-----------
For each query scan every interval, keep the smallest size among those with left <= q <= right.
O(n * m) time for n intervals and m queries, O(1) extra space. The waste: consecutive queries
(in sorted order) share almost all of their containing intervals, yet every query rediscovers
the whole set from scratch.

From brute force to optimal
---------------------------
The redundancy is recomputing "which intervals contain q" independently per query. Answer the
queries OFFLINE in increasing order (remembering their original positions). Then an interval
becomes a candidate once its left <= q -- and stays one for all later queries until q passes
its right. So two monotone pointers: sort intervals by left and push every interval whose left
<= q into a candidate set as q grows. Within the candidates we want the smallest size among
those with right >= q. Keep them in a min-heap keyed by (size, right); before answering, pop
the top while its right < q (expired, lazily removed -- an expired interval below the top does
no harm because we only read the top). Each interval is pushed once and popped at most once:
O((n + m) log n) plus the two sorts.

Intuition
---------
Sort both sides so the sweep moves one way only. Walking the queries from left to right, the
pool of intervals that have "started" grows and never shrinks; some of those have "ended" and
are useless, but we only need to discard them when they would otherwise be reported as the
answer. The heap's top is always the smallest live candidate, so each query is answered in
amortised O(log n).

Geometric view
--------------
Intervals as horizontal bars above a number line, sorted by left edge. A vertical sweep line
jumps from query to query, left to right. Every bar whose left edge the line has passed is
dropped into a min-heap triangle with the shortest bar at the apex. Bars whose right edge is
behind the line are dead: they stay in the triangle until they reach the apex and are then
discarded. The apex length is the answer for the query at the line.

Steps
-----
1. Sort intervals by left; sort query indices by query value; i = 0; heap = [].
2. For each query q (ascending): while i < n and intervals[i].left <= q: push (size, right), i += 1.
3. While heap and heap[0].right < q: pop (expired).
4. ans[original index] = heap[0].size if heap else -1.
5. Return ans.

Complexity: O(n log n + m log m) time, O(n + m) space — sorting, then each interval is pushed and
popped at most once across all queries.
Pitfalls: Returning answers in sorted-query order instead of the original order; popping with
<= instead of < (a query equal to the right endpoint IS contained); using an inclusive size
of right - left instead of right - left + 1.
"""
import heapq
from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort()                                        # by left edge
        order = sorted(range(len(queries)), key=queries.__getitem__)
        live = []                                               # min-heap of (size, right)
        ans = [-1] * len(queries)
        i = 0
        for qi in order:
            q = queries[qi]
            while i < len(intervals) and intervals[i][0] <= q:  # intervals that have started
                left, right = intervals[i]
                heapq.heappush(live, (right - left + 1, right))
                i += 1
            while live and live[0][1] < q:                      # lazy removal of ended ones
                heapq.heappop(live)
            if live:
                ans[qi] = live[0][0]
        return ans


def brute_force(intervals: List[List[int]], queries: List[int]) -> List[int]:
    # For each query, scan every interval and keep the smallest size that contains it.
    ans = []
    for q in queries:
        best = -1
        for left, right in intervals:
            if left <= q <= right and (best < 0 or right - left + 1 < best):
                best = right - left + 1
        ans.append(best)
    return ans


if __name__ == "__main__":
    s = Solution()
    cases = (
        (([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]), [3, 3, 1, 4]),
        (([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]), [2, -1, 4, 6]),
        (([[1, 1]], [1, 2]), [1, -1]),                       # size-1 interval; query past the end
        (([[5, 9]], [4]), [-1]),                             # query before every interval
        (([[1, 10], [3, 4], [3, 4]], [4, 4, 1]), [2, 2, 10]),  # repeated queries, duplicate intervals
    )
    for (iv, qs), want in cases:
        assert s.minInterval([x[:] for x in iv], qs[:]) == want, (iv, qs, want)
        assert brute_force(iv, qs) == want, (iv, qs, want)
    import random
    random.seed(1851)
    for _ in range(200):
        iv = []
        for _ in range(random.randint(1, 8)):
            l = random.randint(0, 20)
            iv.append([l, l + random.randint(0, 8)])
        qs = [random.randint(0, 30) for _ in range(random.randint(1, 8))]
        assert s.minInterval([x[:] for x in iv], qs[:]) == brute_force(iv, qs), (iv, qs)
    print("ok")
