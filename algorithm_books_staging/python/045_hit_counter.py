"""
Design Hit Counter - Circular Buckets over the Last 300 Seconds

Count recent hits: hit(t) records a hit at second t, and get_hits(t) returns
the hits at times s with t - 300 < s <= t (calls arrive in time order):
hits at 1, 2, 2, 3, 300; get_hits(300), get_hits(301) -> 5, 4.
"""


# --- algorithm ---
class HitCounter:
    """300 buckets, one per second of the window, reused round the clock."""

    def __init__(self):
        self.window = 300                   # seconds that get_hits looks back
        self.times = [0] * self.window      # bucket i: the second it counts
        self.counts = [0] * self.window     # bucket i: hits in that second

    def hit(self, timestamp):
        """Add the hit to bucket timestamp mod 300, reset if stale. O(1)."""
        slot = timestamp % self.window
        if self.times[slot] != timestamp:   # empty, or 300+ seconds old
            self.times[slot] = timestamp
            self.counts[slot] = 0
        self.counts[slot] += 1

    def get_hits(self, timestamp):
        """Add up the buckets whose second is under 300 seconds old. O(300)."""
        total = 0
        for slot in range(self.window):
            if timestamp - self.times[slot] < self.window:  # inside the window
                total += self.counts[slot]
        return total


# --- try it ---
counter = HitCounter()
counter.hit(1)
counter.hit(2)
counter.hit(2)
counter.hit(3)
print(counter.get_hits(4))                              # -> 4
counter.hit(300)
print(counter.get_hits(300), counter.get_hits(301))     # -> 5 4
counter.hit(301)                    # bucket 1 still holds second 1: reset
print(counter.get_hits(301))                            # -> 5
print(counter.get_hits(600), counter.get_hits(601))     # -> 1 0
