---
rank: 51
slug: task_scheduler
---

Each task takes one unit of time, and two runs of the same task need at least `n` units between them; the CPU may sit idle. Return the fewest units that run every task. For `["A", "A", "A", "B", "B", "B"]` with `n = 2` the answer is `8`: `A B idle A B idle A B`.

Simulating unit by unit works, but the answer is a formula, because the most frequent task is the bottleneck. Its `max_count` copies need a gap of `n` units after every copy but the last, so they frame a grid: `max_count - 1` full rows of width `n + 1`, each starting with that task, and then a last row. Every other task drops into the gaps column by column, most frequent first, an order that keeps each task's copies at least a full row, `n + 1` units, apart. The tasks tied at `max_count` also need a slot in the last row, so `frame = (max_count - 1) * (n + 1) + tied`. Nothing beats the frame, because the last copies of the tied tasks cannot start before the last row and each needs a unit of its own.

Picture the grid filling up. While gaps remain, the leftover gaps become idles and the answer is the frame. Once the other tasks overflow the gaps, the rows simply widen past `n + 1`; the copies of each task are still a full row apart, so no idle is needed at all and the answer is `len(tasks)`, which no schedule can beat either. Both cases fold into `max(frame, len(tasks))`.

```text
tasks A A A B B B, n = 2      counts A 3, B 3: max_count = 3, tied = 2
            ┌─ n + 1 = 3 ─┐
   row 1    A    B    idle
   row 2    A    B    idle
   row 3    A    B            last row: only the tied tasks
   frame = (3 - 1) * 3 + 2 = 8 ≥ len(tasks) = 6: answer 8

add C C D D                   counts A 3, B 3, C 2, D 2: frame still 8
   row 1    A    B    C    D  rows widen past n + 1
   row 2    A    B    C    D
   row 3    A    B
   frame = 8 < len(tasks) = 10: answer 10, no idles
```

```pseudo
FUNCTION LeastInterval(tasks, n)
    counts ← empty map
    FOR EACH task IN tasks
        counts[task] ← counts.get(task, 0) + 1
    max_count ← 0
    FOR EACH task IN counts
        max_count ← max(max_count, counts[task])
    tied ← 0                               // tasks that also reach max_count
    FOR EACH task IN counts
        IF counts[task] = max_count
            tied ← tied + 1
    frame ← (max_count - 1) * (n + 1) + tied       // full rows, then a last row
    RETURN max(frame, len(tasks))          // overflow: rows widen, no idles
```

Counting takes `O(len(tasks))` time, and the map holds one entry per distinct task, `O(1)` for a fixed alphabet such as the 26 letters of LC 621. Reach for the frame when a problem spaces out repeats with a cooldown and asks only for a length or a yes-or-no answer. When the actual order is needed, simulate instead: a max-heap of remaining counts picks the most frequent ready task each unit, and a queue holds the tasks that are cooling down. Reorganize String (LC 767) is the case `n = 1` with no idle allowed, so an arrangement exists exactly when `frame ≤ len(s)`; LC 358 is the same with cooldown `k - 1`. The classic mistake is forgetting `tied` and adding just `1` for the last row, which answers `7` on the example, while `B` needs a slot in that row too and the answer is `8`.

*Practice:* LC 621 Task Scheduler · LC 767 Reorganize String · LC 358 Rearrange String k Distance Apart
