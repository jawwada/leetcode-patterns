---
rank: 149
slug: job_scheduler
---

Design a scheduler that runs jobs at given times. `schedule(name, run_at, interval)` registers a job that first runs at `run_at` and then every `interval` time units, or only once when `interval` is 0; `cancel(name)` drops a job; and `run_due(now)` runs every job that is due by `now`, in time order with ties going to the entry inserted first, and returns the runs as `[time, name]` pairs. The caller passes the time, the way an event loop passes its clock. With `ping` every 5 units from time 5, `save` once at 10 and `mail` once at 12, `run_due(10)` returns `[[5, 'ping'], [10, 'save'], [10, 'ping']]`.

The brute force scans every job on every tick to find the due ones, `O(n)` per check even when nothing is due. A scheduler only ever asks which run comes first, and a min-heap keyed by run time keeps that answer at its top, at `O(log n)` per push and pop. So keep one heap entry per pending run, `(run_at, seq, name)`, and let `run_due` pop while the top is due. The `seq` comes from a counter stamped on every push: it breaks ties between equal times in insertion order, and since no two entries share it, the heap never compares names. A recurring job goes back in at `run_at + interval` right after it runs; if that time is still at or before `now`, the same loop pops it again, so a scheduler that fell behind catches up on every missed run, in order.

Cancelling cannot reach into the middle of a heap cheaply, so it does not try. Each name maps to the `seq` of its one live entry; `cancel` deletes that mapping in `O(1)`, and the orphaned entry stays in the heap until it surfaces at the top, where `run_due` sees that it is not the live entry and discards it. Comparing the `seq`, not just the name, matters once a cancelled name is scheduled again: the old entry and the new one carry the same name, and only the number tells them apart. Rescheduling a live name works the same way.

```text
entries are (run_at, seq, name), listed earliest first; ✗ = stale
schedule(ping, 5, 5)    heap (5,1,ping)
schedule(save, 10, 0)   heap (5,1,ping) (10,2,save)
schedule(mail, 12, 0)   heap (5,1,ping) (10,2,save) (12,3,mail)
run_due(10)             pop (5,1,ping): run, push (10,4,ping)
                        pop (10,2,save): run, a one-off: done
                        pop (10,4,ping): run, push (15,5,ping)
                        top (12,3,mail) is after 10: stop
                        returns [[5, 'ping'], [10, 'save'], [10, 'ping']]
cancel(mail)            heap (12,3,mail)✗ (15,5,ping)
run_due(12)             pop (12,3,mail): stale, skip; returns []
run_due(26)             pops 15, 20, 25 and pushes 20, 25, 30: catch-up
                        heap (30,8,ping)
cancel(ping)            heap (30,8,ping)✗
schedule(ping, 35, 0)   heap (30,8,ping)✗ (35,9,ping)
run_due(40)             pop (30,8,ping): live seq is 9, so stale, skip
                        pop (35,9,ping): run; returns [[35, 'ping']]
```

```pseudo
CLASS JobScheduler
    FUNCTION Init()
        self.heap ← empty min-heap      // (run_at, seq, name), earliest on top
        self.interval ← empty map       // name → repeat interval, 0 for one-off
        self.live ← empty map           // name → seq of its one live entry
        self.seq ← 0                    // insertion counter: breaks ties

    FUNCTION Push(name, run_at)
        self.seq ← self.seq + 1
        self.live[name] ← self.seq
        self.heap.push((run_at, self.seq, name))

    FUNCTION Schedule(name, run_at, interval)
        self.interval[name] ← interval
        self.Push(name, run_at)         // an older entry for name goes stale

    FUNCTION Cancel(name)
        IF name NOT IN self.live
            RETURN false
        self.live.remove(name)
        self.interval.remove(name)
        RETURN true

    FUNCTION RunDue(now)
        ran ← empty list
        WHILE len(self.heap) > 0 AND self.heap.top()[0] ≤ now
            (run_at, seq, name) ← self.heap.pop()
            IF name NOT IN self.live OR self.live[name] ≠ seq
                CONTINUE                // cancelled or replaced: stale
            ran.append([run_at, name])
            interval ← self.interval[name]
            IF interval > 0
                self.Push(name, run_at + interval)  // if still due: catch up
            ELSE
                self.live.remove(name)  // a one-off job is done
                self.interval.remove(name)
        RETURN ran
```

Scheduling costs `O(log n)` for `n` heap entries, each run costs one pop and at most one push, and a cancel is `O(1)`; a stale entry is popped once, so lazy deletion adds at most one pop per cancel or reschedule. Dead entries do occupy the heap until they surface, so a scheduler whose timers are mostly cancelled, as timeouts usually are, rebuilds the heap from its live entries once the dead ones outnumber them; the expiring cache of #94 and the price tracker of #140 lean on the same lazy deletion. For millions of timers, kernels and network libraries use a timing wheel: a circular array of buckets, one per tick, where a timer due `d` ticks ahead goes into the bucket `d` slots past the current one, so adding and cancelling cost `O(1)` and each tick empties one bucket, with coarser wheels stacked above for long delays. Replaying missed runs is a policy; a job that should not replay them re-arms at the first `run_at + k × interval` after `now`. The signals are "run at time t", "every k seconds", timeouts, delayed retries, and simulations that serve tasks or meetings in time order, such as Single-Threaded CPU and Meeting Rooms III, which builds on the end-time heap of #27. The classic mistake is checking only the name for staleness: above, the dead entry `(30,8,ping)` would pass that test and run `ping` five units early, and the real run at 35 would then be thrown away.

*Practice:* LC 1834 Single-Threaded CPU · LC 621 Task Scheduler · LC 2402 Meeting Rooms III
