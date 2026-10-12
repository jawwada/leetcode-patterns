"""
Kth Largest Element in a Stream (basics: heaps)
Design KthLargest(k, nums) whose add(val) returns the k-th largest value so far (LeetCode 703).
  k = 3, nums = [4, 5, 8, 2]; add 3, 5, 10, 9, 4  ->  4, 5, 5, 8, 8

Idea: keep only the k largest values, in a min-heap. Its root is the smallest of them, which is
      exactly the k-th largest overall; a value that drops out can never be the answer again.

Pseudocode:
  add(val):
      push val
      if len(heap) > k: pop the root               # back to exactly k
      return heap[0]
  __init__: add every value of nums

Time O(log k) per add (O(n log k) to start), space O(k).
"""
import heapq


class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []                   # min-heap of the k largest so far
        for x in nums:
            self.add(x)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:      # one too many: drop the smallest
            heapq.heappop(self.heap)
        return self.heap[0]              # smallest of the k largest = k-th largest


if __name__ == "__main__":
    kth = KthLargest(3, [4, 5, 8, 2])
    print(kth.add(3), kth.add(5), kth.add(10))  # 4 5 5
    print(kth.add(9), kth.add(4))               # 8 8
