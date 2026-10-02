"""
Task Scheduler (LeetCode 621)  — Medium
Pattern: Max-heap + cooldown queue simulation

Problem
-------
Given tasks as uppercase letters and a cooldown n, each unit of time the CPU runs one task or
idles. Two identical tasks must be at least n units apart. Return the minimum total time.
Example: tasks=["A","A","A","B","B","B"], n=2 -> 8  (A B idle A B idle A B).

Brute force
-----------
Simulate tick by tick. At each tick scan all 26 letters, find the one with the most remaining
copies whose last-run time is more than n ticks ago, and run it (or idle if none is ready).
O(T * 26) time where T is the final answer, O(26) space. The waste: every tick re-scans all 26
counters and re-checks their cooldown, even though only one counter changed since the last tick
and the cooldown expiries are completely predictable (last_run + n + 1).

From brute force to optimal
---------------------------
The redundancy is two separate linear scans per tick: "which ready task has the highest count"
and "which tasks are ready". Observation 1: the greedy choice is always the ready task with the
largest remaining count (it is the one most likely to force idles later), so a max-heap of
counts answers the first question in O(log 26). Observation 2: a task that just ran becomes
ready again at exactly time t + n + 1, and tasks re-enter in the order they left, so a FIFO
queue of (ready_time, count) answers the second question by peeking at its head. Heap + queue
replaces 26-wide scans with O(log 26) work per tick.

Intuition
---------
Always run the most frequent available task; park it in a cooldown queue stamped with when it
may return. When nothing is available, jump time straight to the head of the queue instead of
idling tick by tick.

Geometric view
--------------
Two containers side by side: a triangle (max-heap of remaining counts, biggest on top) and a
conveyor belt (queue) that carries a task away for n+1 ticks before dropping it back into the
triangle. The clock advances one tick per pop; when the triangle is empty the clock skips ahead
to the belt's first drop-off time.

Steps
-----
1. Count tasks; push -count for each letter onto a max-heap.
2. time = 0. While heap or queue is non-empty: time += 1.
3. If heap non-empty: pop the biggest count, decrement, and if copies remain enqueue
   (time + n, count).
4. If the queue head's ready time == time, move it back to the heap.
5. If the heap is empty but the queue is not, jump time to the queue head's ready time.
6. Return time.

Complexity: O(T log 26) = O(T) time where T is the answer, O(26) space — heap and queue hold at
most 26 entries.
Pitfalls: Off-by-one on the ready time (a task run at t may run again at t + n + 1); forgetting
to jump the clock when idle (TLE on huge n); not re-adding tasks before choosing the next one.
"""
import heapq
from collections import Counter, deque
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        heap = [-c for c in Counter(tasks).values()]     # max-heap of remaining counts
        heapq.heapify(heap)
        cooling: deque = deque()                          # (ready_time, -count), FIFO by time
        time = 0
        while heap or cooling:
            time += 1
            if heap:
                cnt = heapq.heappop(heap) + 1            # run one copy (counts are negative)
                if cnt:
                    cooling.append((time + n, cnt))
            if cooling and cooling[0][0] == time:        # cooldown over, back into the heap
                heapq.heappush(heap, cooling.popleft()[1])
            if not heap and cooling:                      # nothing runnable: skip the idle gap
                time = cooling[0][0] - 1
        return time


def brute_force(tasks: List[str], n: int) -> int:
    remaining = Counter(tasks)
    last_run = {t: -n - 1 for t in remaining}
    time = 0
    while remaining:
        ready = [t for t in remaining if last_run[t] + n < time]   # rescan all tasks each tick
        if ready:
            t = max(ready, key=lambda x: remaining[x])
            remaining[t] -= 1
            last_run[t] = time
            if remaining[t] == 0:
                del remaining[t]
        time += 1
    return time


if __name__ == "__main__":
    s = Solution()
    cases = [
        (["A", "A", "A", "B", "B", "B"], 2, 8),
        (["A", "C", "A", "B", "D", "B"], 1, 6),
        (["A", "A", "A", "B", "B", "B"], 3, 10),
        (["A"], 0, 1),                                   # single task, no cooldown
        (["A", "A", "A", "A"], 5, 19),                   # long idles
    ]
    for tasks, n, want in cases:
        assert s.leastInterval(tasks, n) == want, (tasks, n)
        assert brute_force(tasks, n) == want, (tasks, n)
    print("ok")
