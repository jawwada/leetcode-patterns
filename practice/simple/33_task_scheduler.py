"""
Task Scheduler (LeetCode 621)
Each tick runs one task or idles; equal tasks need n ticks between them. Return the minimum ticks.
  tasks = ["A", "A", "A", "B", "B", "B"], n = 2  ->  8   (A B idle A B idle A B)

Idea: always run the ready task with the most copies left (max-heap of counts).
      A task just run waits in a FIFO cooldown queue until time + n, then goes back to the heap.
      If nothing is ready, jump the clock straight to the next ready time.

Pseudocode:
  heap = max-heap of counts; cooling = queue of (ready_time, count)
  while heap or cooling:
      time += 1
      if heap: pop biggest count, run it; if copies remain: cooling.append((time + n, count - 1))
      if cooling front is ready at time: move it back to heap
      if heap empty: time = cooling front ready_time - 1   # skip the idle ticks

Time O(T) for T ticks (heap holds at most 26 letters), space O(1).
"""
import heapq
from collections import Counter, deque


def least_interval(tasks, n):
    heap = [-c for c in Counter(tasks).values()]  # max-heap of counts (negated)
    heapq.heapify(heap)
    cooling = deque()                             # (ready_time, -count_left)
    time = 0
    while heap or cooling:
        time += 1
        if heap:
            cnt = heapq.heappop(heap) + 1         # run one copy of the most frequent task
            if cnt < 0:                           # copies left: cool down
                cooling.append((time + n, cnt))
        if cooling and cooling[0][0] == time:     # cooldown over: ready again
            heapq.heappush(heap, cooling.popleft()[1])
        if not heap and cooling:                  # nothing ready: skip idle ticks
            time = cooling[0][0] - 1
    return time


if __name__ == "__main__":
    print(least_interval(["A", "A", "A", "B", "B", "B"], 2))  # 8
    print(least_interval(["A", "A", "A", "B", "B", "B"], 0))  # 6
    print(least_interval(["A", "A", "A", "A", "B", "C"], 2))  # 10
