"""
Task Scheduler (LeetCode 621) - Medium-Hard
Area: heap / greedy
Key operations: pop the most frequent ready task, park it in a cooldown queue with its ready time, re-add when ready, jump the clock over idle gaps

Tasks are uppercase letters; each tick the CPU runs one task or idles. Two copies of the same
letter must be at least n ticks apart. Return the minimum number of ticks to run every task.
Example: tasks = ["A", "A", "A", "B", "B", "B"], n = 2 -> 8  (A B idle A B idle A B)
"""
import heapq
from collections import Counter, deque
from typing import List


# --- brute force ---
def brute_force(tasks: List[str], n: int) -> int:
    """Tick by tick: rescan every letter, pick the one with the most copies left whose last run is
    more than n ticks ago, or idle. O(T * 26) for T ticks: every tick re-checks all 26 cooldowns
    although only one counter changed and every expiry time was known in advance."""
    remaining = Counter(tasks)
    last_run = {ch: -n - 1 for ch in remaining}
    time = 0
    while remaining:
        ready = [ch for ch in remaining if last_run[ch] + n < time]
        if ready:
            ch = max(ready, key=lambda c: remaining[c])
            remaining[ch] -= 1
            last_run[ch] = time
            if remaining[ch] == 0:
                del remaining[ch]
        time += 1
    return time


# --- optimal ---
def solve(tasks: List[str], n: int) -> int:
    """Max-heap of remaining counts picks the most frequent ready task in O(log 26); a FIFO cooldown
    queue of (ready_time, count, letter) hands tasks back the tick they become legal again. When
    nothing is ready the clock jumps straight to the next ready time. O(T log 26) = O(T)."""
    heap = [(-c, ch) for ch, c in sorted(Counter(tasks).items())]
    heapq.heapify(heap)
    cooling = deque()  # (ready_time, -count, letter), oldest first
    time = 0
    while heap or cooling:
        time += 1
        if heap:
            cnt, ch = heapq.heappop(heap)
            if cnt + 1 < 0:
                cooling.append((time + n, cnt + 1, ch))
        if cooling and cooling[0][0] == time:
            _, cnt, ch = cooling.popleft()
            heapq.heappush(heap, (cnt, ch))
        if not heap and cooling:
            time = cooling[0][0] - 1
    return time


# --- demo ---
def demo():
    return solve(["A", "A", "A", "B", "B", "B"], 2)


# --- bugs ---
BUGS = [
    {
        "replace": "                cooling.append((time + n, cnt + 1, ch))",
        "with":    "                cooling.append((time + n + 1, cnt + 1, ch))",
        "fix": "ready_time is time + n; the check after the run adds the tick",
        "why": "The ready check happens after the run in the same tick, so ready_time t + n already means the next run is at t + n + 1; adding one more tick stretches every gap and the example returns 10 instead of 8.",
        "decoys": [
            {"line": "            if cnt + 1 < 0:", "change": "should be cnt + 1 <= 0"},
            {"line": "        time += 1", "change": "should run after the cooldown check"},
            {"line": "    heap = [(-c, ch) for ch, c in sorted(Counter(tasks).items())]", "change": "should store (c, ch) without the minus"},
        ],
    },
    {
        "replace": "        if cooling and cooling[0][0] == time:",
        "with":    "        if cooling and cooling[0][0] < time:",
        "fix": "a task whose ready_time equals the tick comes back now: use ==",
        "why": "With < the task is never handed back on its ready tick; the empty heap makes the clock jump to just before that tick, the next tick is the ready time again, and the loop repeats forever.",
        "decoys": [
            {"line": "            heapq.heappush(heap, (cnt, ch))", "change": "should push (-cnt, ch)"},
            {"line": "            _, cnt, ch = cooling.popleft()", "change": "should be cooling.pop()"},
            {"line": "    while heap or cooling:", "change": "should be while heap"},
        ],
    },
    {
        "replace": "            time = cooling[0][0] - 1",
        "with":    "            time = cooling[0][0]",
        "fix": "jump to ready_time - 1 so the loop's time += 1 lands on it",
        "why": "Jumping onto the ready time itself makes the next tick overshoot it, the == check never fires, the task never returns and the loop keeps jumping forever.",
        "decoys": [
            {"line": "        if not heap and cooling:", "change": "should be if not heap"},
            {"line": "            cnt, ch = heapq.heappop(heap)", "change": "should be heap.pop()"},
            {"line": "    return time", "change": "should return time - 1"},
        ],
    },
    {
        "replace": "    heap = [(-c, ch) for ch, c in sorted(Counter(tasks).items())]",
        "with":    "    heap = [(c, ch) for ch, c in sorted(Counter(tasks).items())]",
        "fix": "negate the counts: heapq is a min-heap, most frequent pops first",
        "why": "Without the minus the counts are positive, so cnt + 1 < 0 never holds and every letter is dropped after a single run: the example returns 2 instead of 8.",
        "decoys": [
            {"line": "    heapq.heapify(heap)", "change": "should be heap.sort(reverse=True)"},
            {"line": "    cooling = deque()  # (ready_time, -count, letter), oldest first", "change": "should be a list sorted by count"},
            {"line": "                cooling.append((time + n, cnt + 1, ch))", "change": "should append (time + n, cnt, ch)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
