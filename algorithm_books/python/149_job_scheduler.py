"""
Job Scheduler - A Min-Heap of Next Run Times

Run jobs at given times: schedule(name, run_at, interval) runs a job at
run_at and then every interval (0 = once), cancel(name) drops it, and
run_due(now) returns every run due by now, earliest first: ping every 5 from
5, save once at 10 -> run_due(10) = [[5, 'ping'], [10, 'save'], [10, 'ping']].
"""
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class JobScheduler:
    """A min-heap of (run_at, seq, name); a map marks each name's live
    entry. O(log n) per push or pop, O(1) to cancel."""

    def __init__(self):
        self.heap = []          # (run_at, seq, name), earliest on top
        self.interval = {}      # name -> repeat interval, 0 for one-off
        self.live = {}          # name -> seq of its one live heap entry
        self.seq = 0            # insertion counter: breaks ties in time

    def push(self, name, run_at):
        """Add a fresh heap entry for name and make it the live one.
        O(log n)."""
        self.seq += 1
        self.live[name] = self.seq
        heapq.heappush(self.heap, (run_at, self.seq, name))

    def schedule(self, name, run_at, interval):
        """Run name at run_at, then every interval (0 = once). O(log n)."""
        self.interval[name] = interval
        self.push(name, run_at)         # an older entry for name goes stale

    def cancel(self, name):
        """Forget name; its heap entry is skipped when it surfaces. O(1)."""
        if name not in self.live:
            return False
        del self.live[name]
        del self.interval[name]
        return True

    def run_due(self, now):
        """Pop every live entry with run_at <= now in time order; a recurring
        job goes back in at run_at + interval. O(log n) per pop."""
        ran = []
        while len(self.heap) > 0 and self.heap[0][0] <= now:
            run_at, seq, name = heapq.heappop(self.heap)
            if name not in self.live or self.live[name] != seq:
                continue                # cancelled or replaced: stale
            ran.append([run_at, name])
            interval = self.interval[name]
            if interval > 0:
                self.push(name, run_at + interval)  # if still due: catch up
            else:
                del self.live[name]     # a one-off job is done
                del self.interval[name]
        return ran


# --- try it ---
scheduler = JobScheduler()
scheduler.schedule("ping", 5, 5)        # every 5 time units from 5
scheduler.schedule("save", 10, 0)       # once, at 10
scheduler.schedule("mail", 12, 0)
print(scheduler.run_due(10))    # -> [[5, 'ping'], [10, 'save'], [10, 'ping']]
print(scheduler.cancel("mail"), scheduler.run_due(12))      # -> True []
print(scheduler.run_due(26))    # -> [[15, 'ping'], [20, 'ping'], [25, 'ping']]
scheduler.cancel("ping")                # its entry for 30 stays, now stale
scheduler.schedule("ping", 35, 0)       # same name, new seq
print(scheduler.run_due(40), len(scheduler.heap))   # -> [[35, 'ping']] 0
