# Task Scheduler (LeetCode 621)

**Area:** heap / greedy · **Difficulty:** Medium-Hard · **Key operations:** pop the most frequent ready task, park it in a cooldown queue with its ready time, re-add when ready, jump the clock over idle gaps

## Problem

Tasks are uppercase letters. Each tick the CPU runs one task or idles. Two copies of the same letter must be at least `n` ticks apart (n other ticks between them). Return the minimum number of ticks needed to run every task.

## Example

```
tasks = [A, A, A, B, B, B], n = 2
tick:   1  2  3     4  5  6     7  8
run:    A  B  idle  A  B  idle  A  B     -> 8
```

Between two A's there are two other ticks (B and idle), as required.

## Brute force

Simulate tick by tick. At each tick scan all 26 letters, find the one with the most copies left whose last run was more than `n` ticks ago, run it (or idle if none is ready).

O(T · 26) for an answer of T ticks, O(26) space. The wasted work: every tick re-scans all counters and re-checks every cooldown, although only one counter changed since the last tick and every expiry time was known the moment the task ran (`last_run + n + 1`). Idle stretches are walked one tick at a time even when nothing can possibly happen.

## From brute force to optimal

Two questions are asked each tick: "which ready task has the largest count?" and "which tasks just became ready?".

The first is a max-heap of remaining counts: pop the top in O(log 26). The greedy choice is right because the most frequent task is the one most likely to force idles later; running it now spreads its copies as far apart as possible.

The second is a FIFO queue. A task run at tick `t` is legal again at `t + n + 1`; tasks leave the heap in time order, so they re-enter in the same order. Store `(ready_time, count, letter)` on a deque and peek at its head once per tick. When the heap is empty but the queue is not, nothing can run until the head's ready time, so jump the clock there instead of idling tick by tick.

## Intuition

Two containers side by side: a triangle (max-heap of remaining counts, biggest on top) and a conveyor belt (the cooldown queue) that carries a task away for `n` ticks and drops it back into the triangle. Each tick: take the top of the triangle, run it, put it on the belt stamped with when it may return. Then check the front of the belt: if its stamp is now, move it back into the triangle. If the triangle is empty, fast-forward the clock to the belt's next drop-off. The answer is the final clock reading.

## Walkthrough

Heap drawn as `(letter, copies left)`, cooling queue as `(letter, copies, 'ready', time)`, oldest first.

```
t=1: run A (2 left)        heap [(B, 3)]          cooling [(A, 2, ready 3)]
t=2: run B (2 left)        heap []                cooling [(A, 2, ready 3), (B, 2, ready 4)]
     nothing runnable: idle t=3, jump the clock to the head's ready time
t=3: (idle) A ready again  heap [(A, 2)]          cooling [(B, 2, ready 4)]
t=4: run A (1 left)        B ready again -> heap [(B, 2)]   cooling [(A, 1, ready 6)]
t=5: run B (1 left)        heap []                cooling [(A, 1, ready 6), (B, 1, ready 7)]
     nothing runnable: idle t=6, jump
t=6: (idle) A ready again  heap [(A, 1)]          cooling [(B, 1, ready 7)]
t=7: run A (0 left)        B ready again -> heap [(B, 1)]   cooling []
t=8: run B (0 left)        heap []                cooling []
return time = 8
```

Timeline:

```
1 2 3 4 5 6 7 8
A B . A B . A B
```

Note the order inside a tick: run first, then let the head of the queue back in. A run at `t` with `ready_time = t + n` therefore comes back during tick `t + n` and runs at the earliest at `t + n + 1`, which is exactly the required gap.

## Steps

1. Count the letters; push `(-count, letter)` for each onto a heap (negated for a max-heap).
2. `time = 0`. While the heap or the cooling queue is non-empty: `time += 1`.
3. If the heap is non-empty: pop the biggest count, run one copy; if copies remain, append `(time + n, count - 1, letter)` to the cooling queue.
4. If the queue head's `ready_time == time`: pop it and push it back into the heap.
5. If the heap is empty but the queue is not: set `time = head.ready_time - 1` so the next tick lands exactly on it.
6. Return `time`.

## Complexity

O(T log 26) = O(T) where T is the answer, with idle gaps skipped in O(1) each; O(26) space for the heap and the queue. (The closed-form `max(len(tasks), (max_count - 1) * (n + 1) + ties)` gives the same number without simulating, but the simulation is the one that generalises to variants.)

## Pitfalls

- **`ready_time = time + n + 1`.** The ready check already happens after the run in the same tick, so `time + n` is the right stamp; one more tick stretches every gap and the example returns 10.
- **`<` instead of `==` on the ready check.** The task is never handed back on its ready tick; the empty heap then jumps the clock to just before that tick, the next tick is the ready time again, and the loop never ends.
- **Jumping to `ready_time` instead of `ready_time - 1`.** The loop's `time += 1` then overshoots the ready time, the `==` check never fires, and the loop spins forever.
- **Forgetting to negate the counts.** With positive counts `heapq` pops the *least* frequent task, and the "copies remain" test on a negative count never holds, so every letter is dropped after one run.
- **Letting tasks back in before running.** Re-adding the head of the queue before the pop would let a task run at `t + n`, one tick too early.
