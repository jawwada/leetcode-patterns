"""
Kth Largest Element in a Stream (LeetCode 703)  — Easy
Pattern: Size-k heap (keep the k best)

Problem
-------
Design a class that is initialised with k and a list of scores, and then receives new scores one
at a time via add(val). After every add, return the k-th largest element seen so far (with
duplicates counted).
Example: k=3, nums=[4,5,8,2]; add(3)->4, add(5)->5, add(10)->5, add(9)->8, add(4)->8.

Brute force
-----------
Keep every number in a list. On each add, append, sort descending and return index k-1.
O(n log n) per add, O(n) space. The wasted work: we re-sort the whole history every time even
though only ONE element changed, and we only ever read a single position of the sorted result.

From brute force to optimal
---------------------------
The redundancy is re-sorting n items to learn one rank. Observation: the answer only depends on
the k largest values seen so far; everything smaller can never become the k-th largest again,
so it can be thrown away the moment it is seen. We need a container that holds exactly k items
and can cheaply (a) tell us its smallest member and (b) evict that smallest member when a bigger
one arrives. A min-heap of size k does both in O(log k): its root IS the k-th largest.

Intuition
---------
Keep only the "top k" club. A newcomer is admitted only by kicking out the weakest member
(the heap root). The weakest surviving member is by definition the k-th largest overall.

Geometric view
--------------
Picture the k kept values as a triangle with the smallest at the apex. A new value falls onto
the heap: if it is smaller than the apex it bounces off; otherwise it joins and the apex is
popped. The apex only ever rises over time.

Steps
-----
1. Heapify the initial nums, then pop until the heap has at most k elements.
2. add(val): push val; if size exceeds k, pop the minimum.
3. Return heap[0], the k-th largest.

Complexity: O(log k) per add, O(k) space — the heap never holds more than k items.
Pitfalls: Forgetting to trim the initial list to k; using a max-heap (you would need to pop
k times to find the answer); handling n < k (heap[0] is still the right answer once k items exist).
"""
import heapq
from typing import List


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:          # keep only the k largest
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:        # evict the weakest member
            heapq.heappop(self.heap)
        return self.heap[0]                # root of a size-k min-heap = k-th largest


class BruteForce:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = list(nums)

    def add(self, val: int) -> int:
        self.nums.append(val)
        self.nums.sort(reverse=True)       # re-sort everything for one rank
        return self.nums[self.k - 1]


if __name__ == "__main__":
    s = KthLargest(3, [4, 5, 8, 2])
    b = BruteForce(3, [4, 5, 8, 2])
    answers = [s.add(v) for v in [3, 5, 10, 9, 4]]
    assert answers == [4, 5, 5, 8, 8]
    assert answers == [b.add(v) for v in [3, 5, 10, 9, 4]]
    # initial list shorter than k
    s2, b2 = KthLargest(2, [3]), BruteForce(2, [3])
    for v in [5, 10, 9, 4]:
        s2.add(v)
        b2.add(v)
    assert s2.add(1) == b2.add(1) == 9
    # duplicates count separately
    s3 = KthLargest(1, [7, 7])
    assert s3.add(7) == 7 and s3.add(8) == 8
    print("ok")
