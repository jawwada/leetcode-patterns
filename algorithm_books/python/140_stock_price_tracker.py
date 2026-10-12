"""
Stock Price Tracker - Hash Map + Heaps with Lazy Deletion

Prices arrive as (timestamp, price) records, and a later record may correct
an earlier timestamp; report the latest price and the maximum and minimum of
the current prices. update(1, 10), update(2, 5), update(1, 3) -> current 5,
maximum 5, minimum 3.
"""
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class StockPrice:
    """Map timestamp -> price, plus a max-heap and a min-heap of records
    whose stale tops are discarded lazily. Amortized O(log n) per call."""

    def __init__(self):
        self.prices = {}            # timestamp -> its current price
        self.latest = 0             # the largest timestamp seen so far
        self.max_heap = []          # (-price, timestamp): highest on top
        self.min_heap = []          # (price, timestamp): lowest on top

    def update(self, timestamp, price):
        """Record or correct one price; older records go stale. O(log n)."""
        self.prices[timestamp] = price
        if timestamp > self.latest:
            self.latest = timestamp
        heapq.heappush(self.max_heap, (-price, timestamp))
        heapq.heappush(self.min_heap, (price, timestamp))

    def current(self):
        """The price at the latest timestamp. O(1)."""
        return self.prices[self.latest]

    def maximum(self):
        """Pop stale tops until the top agrees with the map. Amortized
        O(log n)."""
        while True:
            price = -self.max_heap[0][0]
            timestamp = self.max_heap[0][1]
            if self.prices[timestamp] == price:
                return price                # the record is still true
            heapq.heappop(self.max_heap)    # stale: corrected since

    def minimum(self):
        """The mirror image of maximum on the min-heap. Amortized O(log n)."""
        while True:
            price = self.min_heap[0][0]
            timestamp = self.min_heap[0][1]
            if self.prices[timestamp] == price:
                return price
            heapq.heappop(self.min_heap)


# --- try it ---
tracker = StockPrice()
tracker.update(1, 10)
tracker.update(2, 5)
print(tracker.current(), tracker.maximum())     # -> 5 10
tracker.update(1, 3)                            # time 1 was wrong: now 3
print(tracker.maximum(), tracker.minimum())     # -> 5 3
tracker.update(4, 2)
print(tracker.current(), tracker.minimum())     # -> 2 2
print(len(tracker.max_heap), len(tracker.min_heap))     # -> 3 4
