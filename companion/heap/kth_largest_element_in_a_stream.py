"""
Kth Largest Element in a Stream (LeetCode 703) - Easy
Chapter: heap
Pattern: Size-k heap (keep the k best)

Design a class initialised with k and a list of scores that then receives new scores one
at a time via add(val); after every add return the k-th largest element seen so far,
duplicates counted.
Example: k=3, nums=[4,5,8,2]; add(3) -> 4, add(5) -> 5, add(10) -> 5, add(9) -> 8, add(4) -> 8.
"""
import heapq      # heappush / heappop keep the smallest item at index 0


# --- brute force ---
class BruteForce:
    """Keep every number; each add re-sorts the whole list for one rank. O(n log n) per add."""

    def __init__(self, k, nums):
        self.k = k
        self.nums = list(nums)

    def add(self, val):
        self.nums.append(val)
        self.nums.sort(reverse=True)     # re-sort everything although one value changed
        return self.nums[self.k - 1]


# --- optimal ---
class KthLargest:
    """Min-heap holding only the k largest seen; its root is the k-th largest. O(log k) per add."""

    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        for val in nums:
            heapq.heappush(self.heap, val)
            if len(self.heap) > k:
                heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)     # the smallest can never be the k-th largest again
        return self.heap[0]              # root of a size-k min-heap = k-th largest


# --- try the brute force ---
stream = BruteForce(3, [4, 5, 8, 2])
print(stream.add(3))    # -> 4
print(stream.add(5))    # -> 5
print(stream.add(10))   # -> 5
print(stream.add(9))    # -> 8
print(stream.add(4))    # -> 8
stream = BruteForce(1, [7, 7])
print(stream.add(7))    # -> 7
print(stream.add(8))    # -> 8


# --- try the optimal ---
stream = KthLargest(3, [4, 5, 8, 2])
print(stream.add(3))    # -> 4
print(stream.add(5))    # -> 5
print(stream.add(10))   # -> 5
print(stream.add(9))    # -> 8
print(stream.add(4))    # -> 8
stream = KthLargest(1, [7, 7])
print(stream.add(7))    # -> 7
print(stream.add(8))    # -> 8
