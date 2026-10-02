"""
Sliding Window Median (LeetCode 480)  — Hard
Pattern: Two heaps with lazy deletion

Problem
-------
Given an integer array nums and a window size k, return the median of every contiguous
window of size k as it slides from left to right (for even k, the mean of the two middle
values).
Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 -> [1, -1, -1, 3, 5, 6].

Brute force
-----------
For each of the n - k + 1 windows, copy the k elements, sort them and read the middle.
O(n k log k) time, O(k) space. The wasted work is re-sorting: consecutive windows differ by
one element leaving and one arriving, yet each is sorted from scratch.

From brute force to optimal
---------------------------
Step 1: keep the window in sorted order and update it incrementally — bisect to insert the
new element and to remove the old one. The median is then an index lookup, but a Python
list insert/delete is O(k), so this is O(n k): better constants, same shape. Step 2: the
median only needs the boundary between the lower half and the upper half, which is what a
max-heap `small` (lower half) plus a min-heap `large` (upper half) expose in O(1). Inserts
are O(log k). The obstacle is deletion: heaps cannot remove an arbitrary element. Lazy
deletion fixes that — record the outgoing value in a `delayed` counter, keep explicit
counts of the *valid* elements in each half for balancing, and only physically pop a stale
value when it surfaces at a heap top. Each element is pushed once and popped once, so the
total is O(n log k) and the medians are always read from valid tops.

Intuition
---------
The two-heap median trick works for a stream because elements only arrive. A sliding window
also makes elements leave, and a buried element in a heap is unreachable. The insight is
that a buried element is also irrelevant: it does not affect the top, so it does not affect
the median. Mark it dead, adjust the logical size of its half, and evict it only if it ever
rises to the top. Balancing uses the logical sizes, so the median stays correct even while
corpses sit inside the heaps.

Geometric view
--------------
Picture two piles leaning against each other at the median: the lower pile points up with
its largest value on top, the upper pile points down with its smallest on top. A new value
lands on whichever pile it belongs to; a departing value is crossed out where it lies. If
one pile's live count grows two taller than the other, its top value is moved across. Dead
values are swept off only when they reach a pile's top.

Steps
-----
1. small = max-heap (negated values) for the lower half, large = min-heap for the upper half,
   delayed = Counter of values waiting to be removed, small_n / large_n = live counts.
2. add(x): push onto small if x <= top(small) else onto large; rebalance.
3. remove(x): delayed[x] += 1; decrement the live count of the half x belongs to (compare to
   top(small)); if x is that half's top, prune it; rebalance.
4. rebalance: if small_n > large_n + 1 move top(small) to large; if small_n < large_n move
   top(large) to small; prune the heap just popped from.
5. prune(heap): while its top is in delayed, pop it and decrement delayed.
6. Add the first k values, emit the median; then for each new index add nums[i], remove
   nums[i-k], emit the median.

Complexity: O(n log k) time, O(n) space — every element is pushed and popped at most once; stale values may linger until popped.
Pitfalls: balancing on physical heap lengths instead of live counts; deciding which half an
outgoing value belongs to by its own value rather than by comparison to small's top (they are
the same test, but it must use the *current* top); forgetting to prune after moving an element
across; using integer division for the even-k median.
"""
import heapq
from collections import defaultdict
from typing import List


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        small, large = [], []            # max-heap (negated) lower half, min-heap upper half
        delayed = defaultdict(int)       # value -> pending removals not yet popped
        small_n = large_n = 0            # live (non-deleted) counts per half

        def prune(heap, sign):           # pop stale values sitting on top
            while heap and delayed[sign * heap[0]]:
                delayed[sign * heap[0]] -= 1
                heapq.heappop(heap)

        def rebalance():
            nonlocal small_n, large_n
            if small_n > large_n + 1:
                heapq.heappush(large, -heapq.heappop(small))
                small_n, large_n = small_n - 1, large_n + 1
                prune(small, -1)
            elif small_n < large_n:
                heapq.heappush(small, -heapq.heappop(large))
                small_n, large_n = small_n + 1, large_n - 1
                prune(large, 1)

        def add(x):
            nonlocal small_n, large_n
            if not small or x <= -small[0]:
                heapq.heappush(small, -x)
                small_n += 1
            else:
                heapq.heappush(large, x)
                large_n += 1
            rebalance()

        def remove(x):
            nonlocal small_n, large_n
            delayed[x] += 1
            if x <= -small[0]:
                small_n -= 1
                if x == -small[0]:
                    prune(small, -1)
            else:
                large_n -= 1
                if x == large[0]:
                    prune(large, 1)
            rebalance()

        def median():
            return float(-small[0]) if k % 2 else (-small[0] + large[0]) / 2

        for x in nums[:k]:
            add(x)
        result = [median()]
        for i in range(k, len(nums)):
            add(nums[i])
            remove(nums[i - k])
            result.append(median())
        return result


def brute_force(nums: List[int], k: int) -> List[float]:
    result = []
    for i in range(len(nums) - k + 1):
        window = sorted(nums[i:i + k])
        if k % 2:
            result.append(float(window[k // 2]))
        else:
            result.append((window[k // 2 - 1] + window[k // 2]) / 2)
    return result


if __name__ == "__main__":
    s = Solution()
    assert s.medianSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [1, -1, -1, 3, 5, 6]
    assert s.medianSlidingWindow([1, 2, 3, 4, 2, 3, 1, 4, 2], 3) == [2, 3, 3, 3, 2, 3, 2]
    assert s.medianSlidingWindow([1, 4, 2, 3], 4) == [2.5]
    assert s.medianSlidingWindow([5], 1) == [5]
    assert s.medianSlidingWindow([2, 2, 2, 2], 2) == [2, 2, 2]
    import random
    random.seed(480)
    for _ in range(200):
        n = random.randint(1, 14)
        nums = [random.randint(-5, 5) for _ in range(n)]
        k = random.randint(1, n)
        assert s.medianSlidingWindow(nums, k) == brute_force(nums, k)
    print("ok")
