"""
Find Median from Data Stream (LeetCode 295) - Hard
Chapter: heap
Pattern: Two heaps (balanced max-heap / min-heap)

Design a class with add_num(num) and find_median(). find_median returns the median of all
numbers added so far: the middle value for an odd count, the mean of the two middle values
for an even count.
Example: add 1, add 2 -> find_median() = 1.5; add 3 -> find_median() = 2.0.
"""
import heapq                       # heappush / heappop keep the smallest item at index 0


# --- brute force ---
class BruteForce:
    """Keep every number; sort the whole list on each query. add O(1), find_median O(n log n)."""

    def __init__(self):
        self.nums = []

    def add_num(self, num):
        self.nums.append(num)

    def find_median(self):
        ordered = sorted(self.nums)            # re-sorts everything on every query
        n = len(ordered)
        if n % 2 == 1:
            return float(ordered[n // 2])
        return (ordered[n // 2 - 1] + ordered[n // 2]) / 2


# --- optimal ---
class MedianFinder:
    """Lower half in a max-heap, upper half in a min-heap; the roots are the middle. O(log n)."""

    def __init__(self):
        self.small = []                        # lower half, negated so the root is its maximum
        self.large = []                        # upper half, the root is its minimum

    def add_num(self, num):
        heapq.heappush(self.small, -num)
        biggest_small = -heapq.heappop(self.small)
        heapq.heappush(self.large, biggest_small)   # keeps every small <= every large
        if len(self.large) > len(self.small):       # small may hold one extra, never large
            smallest_large = heapq.heappop(self.large)
            heapq.heappush(self.small, -smallest_large)

    def find_median(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2


# --- try the brute force ---
finder = BruteForce()
finder.add_num(1)
finder.add_num(2)
print(finder.find_median())    # -> 1.5
finder.add_num(3)
print(finder.find_median())    # -> 2.0
finder.add_num(10)
finder.add_num(-4)
print(finder.find_median())    # -> 2.0
single = BruteForce()
single.add_num(-5)
print(single.find_median())    # -> -5.0


# --- try the optimal ---
finder = MedianFinder()
finder.add_num(1)
finder.add_num(2)
print(finder.find_median())    # -> 1.5
finder.add_num(3)
print(finder.find_median())    # -> 2.0
finder.add_num(10)
finder.add_num(-4)
print(finder.find_median())    # -> 2.0
single = MedianFinder()
single.add_num(-5)
print(single.find_median())    # -> -5.0
