"""
Sliding Window Median (LeetCode 480) - Hard
Chapter: sliding_window
Pattern: Two heaps with lazy deletion

Given an integer array nums and a window size k, return the median of every contiguous
window of size k as it slides from left to right; for even k the median is the mean of the
two middle values.
Example: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3 -> [1.0, -1.0, -1.0, 3.0, 5.0, 6.0].
"""
import heapq                        # heappush / heappop keep the smallest at index 0


# --- brute force ---
def brute_force(nums, k):
    """Sort every window from scratch and read the middle. O(n * k log k) time, O(k) space."""
    result = []
    for start in range(len(nums) - k + 1):
        window = sorted(nums[start:start + k])      # k - 1 of these values were sorted last time
        if k % 2 == 1:
            result.append(float(window[k // 2]))
        else:
            result.append((window[k // 2 - 1] + window[k // 2]) / 2)
    return result


# --- optimal ---
class TwoHeaps:
    """Lower half in a max-heap, upper half in a min-heap; removed values are marked, not popped."""

    def __init__(self):
        self.small = []             # max-heap of the lower half (values stored negated)
        self.large = []             # min-heap of the upper half
        self.delayed = {}           # value -> copies removed from the window but still in a heap
        self.small_n = 0            # live counts, stale values not included
        self.large_n = 0

    def prune(self, heap, sign):
        """Pop stale values while one sits on top (sign undoes the negation in small)."""
        while heap and self.delayed.get(sign * heap[0], 0) > 0:
            self.delayed[sign * heap[0]] -= 1
            heapq.heappop(heap)

    def rebalance(self):
        if self.small_n > self.large_n + 1:         # lower half too big: move its top up
            moved = -heapq.heappop(self.small)
            heapq.heappush(self.large, moved)
            self.small_n -= 1
            self.large_n += 1
            self.prune(self.small, -1)
        elif self.small_n < self.large_n:           # upper half too big: move its top down
            moved = heapq.heappop(self.large)
            heapq.heappush(self.small, -moved)
            self.small_n += 1
            self.large_n -= 1
            self.prune(self.large, 1)

    def add(self, x):
        if len(self.small) == 0 or x <= -self.small[0]:
            heapq.heappush(self.small, -x)
            self.small_n += 1
        else:
            heapq.heappush(self.large, x)
            self.large_n += 1
        self.rebalance()

    def remove(self, x):
        self.delayed[x] = self.delayed.get(x, 0) + 1
        if x <= -self.small[0]:                     # x lives in the lower half
            self.small_n -= 1
            if x == -self.small[0]:
                self.prune(self.small, -1)
        else:
            self.large_n -= 1
            if x == self.large[0]:
                self.prune(self.large, 1)
        self.rebalance()                            # balance by live counts, not heap sizes

    def median(self, k):
        if k % 2 == 1:
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2


def median_sliding_window(nums, k):
    """Two heaps meet at the median; a leaving value is deleted lazily. O(n log k) time."""
    heaps = TwoHeaps()
    for i in range(k):
        heaps.add(nums[i])
    result = [heaps.median(k)]
    for i in range(k, len(nums)):
        heaps.add(nums[i])
        heaps.remove(nums[i - k])                   # the value that just left the window
        result.append(heaps.median(k))
    return result


# --- try the brute force ---
print(brute_force([1, 3, -1, -3, 5, 3, 6, 7], 3))     # -> [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
print(brute_force([1, 2, 3, 4, 2, 3, 1], 3))          # -> [2.0, 3.0, 3.0, 3.0, 2.0]
print(brute_force([1, 4, 2, 3], 4))                   # -> [2.5]
print(brute_force([2, 2, 2, 2], 2))                   # -> [2.0, 2.0, 2.0]


# --- try the optimal ---
print(median_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))    # -> [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
print(median_sliding_window([1, 2, 3, 4, 2, 3, 1], 3))         # -> [2.0, 3.0, 3.0, 3.0, 2.0]
print(median_sliding_window([1, 4, 2, 3], 4))                  # -> [2.5]
print(median_sliding_window([2, 2, 2, 2], 2))                  # -> [2.0, 2.0, 2.0]
