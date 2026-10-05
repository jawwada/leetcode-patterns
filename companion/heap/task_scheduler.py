"""
Task Scheduler (LeetCode 621) - Medium
Chapter: heap
Pattern: Max-heap + cooldown queue simulation

Given tasks as uppercase letters and a cooldown n, each unit of time the CPU runs one task
or idles, and two identical tasks must be at least n units apart. Return the minimum total
time to finish all tasks.
Example: tasks=[A,A,A,B,B,B], n=2 -> 8 (A B idle A B idle A B).
"""
import heapq                    # heappush / heappop keep the smallest item at index 0
from collections import deque   # popleft is O(1)


# --- brute force ---
def brute_force(tasks, n):
    """Tick by tick: run the ready task with the most copies left, else idle. O(time * 26)."""
    remaining = {}
    for task in tasks:
        remaining[task] = remaining.get(task, 0) + 1
    last_run = {}
    for task in remaining:
        last_run[task] = -n - 1               # every task starts ready
    time = 0
    while len(remaining) > 0:
        best = None
        for task in remaining:                # rescan every task on every tick
            if last_run[task] + n < time:     # cooled down, so it may run now
                if best is None or remaining[task] > remaining[best]:
                    best = task
        if best is not None:
            remaining[best] -= 1
            last_run[best] = time
            if remaining[best] == 0:
                del remaining[best]
        time += 1                             # best is None means an idle tick
    return time


# --- optimal ---
def least_interval(tasks, n):
    """Max-heap of counts + FIFO cooldown queue; jump the clock over idle gaps. O(T log 26)."""
    counts = {}
    for task in tasks:
        counts[task] = counts.get(task, 0) + 1
    heap = []                                   # negated counts: the root is the most frequent
    for task in counts:
        heapq.heappush(heap, -counts[task])
    cooling = deque()                           # (ready_time, negated count), oldest first
    time = 0
    while len(heap) > 0 or len(cooling) > 0:
        time += 1
        if len(heap) > 0:
            count = -heapq.heappop(heap) - 1    # run one copy of the most frequent ready task
            if count > 0:
                cooling.append((time + n, -count))
        if len(cooling) > 0 and cooling[0][0] == time:
            ready = cooling.popleft()           # its cooldown is over: back into the heap
            heapq.heappush(heap, ready[1])
        if len(heap) == 0 and len(cooling) > 0:
            time = cooling[0][0] - 1            # nothing runnable: jump to the next ready time
    return time


# --- try the brute force ---
print(brute_force(["A", "A", "A", "B", "B", "B"], 2))   # -> 8
print(brute_force(["A", "C", "A", "B", "D", "B"], 1))   # -> 6
print(brute_force(["A", "A", "A", "B", "B", "B"], 3))   # -> 10
print(brute_force(["A", "A", "A", "A"], 5))             # -> 19


# --- try the optimal ---
print(least_interval(["A", "A", "A", "B", "B", "B"], 2))   # -> 8
print(least_interval(["A", "C", "A", "B", "D", "B"], 1))   # -> 6
print(least_interval(["A", "A", "A", "B", "B", "B"], 3))   # -> 10
print(least_interval(["A", "A", "A", "A"], 5))             # -> 19
