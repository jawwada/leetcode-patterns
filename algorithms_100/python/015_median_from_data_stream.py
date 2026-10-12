"""
Find Median from Data Stream - Two Heaps Meet in the Middle

Numbers arrive one at a time; after any arrival, report the median of all the
numbers so far (the mean of the two middle values when the count is even):
add 5, 15, 1, 3 -> medians 5, 10.0, 5, 4.0.
"""
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class MedianFinder:
    """Max-heap of the smaller half, min-heap of the larger half."""

    def __init__(self):
        self.low = []           # max-heap of the smaller half, stored negated
        self.high = []          # min-heap of the larger half

    def add_num(self, num):
        """Pass num through low into high, then rebalance. O(log n)."""
        heapq.heappush(self.low, -num)
        top_low = -heapq.heappop(self.low)    # the largest of low and num
        heapq.heappush(self.high, top_low)
        if len(self.high) > len(self.low):    # low may lead by one, not trail
            top_high = heapq.heappop(self.high)
            heapq.heappush(self.low, -top_high)

    def find_median(self):
        """Read the middle from the two tops. O(1)."""
        if len(self.low) > len(self.high):
            return -self.low[0]               # odd count: low holds the middle
        return (-self.low[0] + self.high[0]) / 2


# --- try it ---
finder = MedianFinder()
finder.add_num(5)
print(finder.find_median())     # -> 5
finder.add_num(15)
print(finder.find_median())     # -> 10.0
finder.add_num(1)
print(finder.find_median())     # -> 5
finder.add_num(3)
print(finder.find_median())     # -> 4.0
