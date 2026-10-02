"""
Smallest Range Covering Elements from K Lists (LeetCode 632)  — Hard
Pattern: K-way merge with a min-heap of list pointers (track the running max)

Problem
-------
Given k sorted integer lists, find the smallest range [a, b] that contains at least one number
from every list. Range [a, b] is smaller than [c, d] if b - a < d - c, or if equal and a < c.
Example: [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]] -> [20,24] (20 from list 2, 24 from list 1,
22 from list 3).

Brute force
-----------
Every candidate range can be assumed to start and end at values that occur in the lists.
For every pair of values (lo, hi) with lo <= hi, check whether each list has an element in
[lo, hi]; keep the smallest valid range. With N total elements that is O(N^2) pairs times
O(N) checking, so O(N^3) time, O(N) space. The waste: for a fixed lo, the best hi is the
largest of "the first element >= lo in each list", so scanning every hi is pointless -- and
even the per-lo recomputation repeats work, since moving lo to the next value only changes the
first element >= lo in ONE list.

From brute force to optimal
---------------------------
Redundancy one: for a fixed lower bound, the only hi worth checking is forced. That gives an
O(N * k) sweep over lo (step every list pointer to the first element >= lo), already a big
win. Redundancy two: as lo advances to the next value in merged order, only one list's
pointer moves. So treat it as a k-way merge: keep one pointer per list and a min-heap of
(value, list, index) over the current pointers. The heap root is the smallest "current"
element -- the range's low end -- and the largest current element (tracked as a running max)
is the forced high end. Record [root, max], then advance the list that owns the root; the
range it belonged to can never shrink by keeping that element because every later range
has a lower bound that is at least as large. Stop when any list is exhausted. O(N log k).

Intuition
---------
Hold one finger on each list, all starting at index 0. Those k fingered values define a
window [min, max] that covers every list. The only way to shrink the window is to raise its
minimum, and the only finger that can raise the minimum is the one sitting ON the minimum.
Advance that finger, update max, re-read min. When that finger runs off its list, no later
window can cover that list, so we are done.

Geometric view
--------------
k horizontal rows of dots (sorted values) above a shared number line. One marker per row.
The window is the span from the leftmost marker to the rightmost marker. Each step picks the
leftmost marker (heap root) and slides it right one dot; the right edge only ever moves
right, the left edge jumps to the new leftmost marker. The narrowest span seen is the answer.

Steps
-----
1. Push (nums[i][0], i, 0) for every list into a min-heap; cur_max = max of those firsts.
2. best = [-inf, inf] (as a huge dummy range).
3. Loop: pop (val, i, j). If cur_max - val < best width, best = [val, cur_max].
4. If j + 1 == len(nums[i]) stop (list i exhausted); else push (nums[i][j+1], i, j+1) and
   cur_max = max(cur_max, nums[i][j+1]).
5. Return best.

Complexity: O(N log k) time, O(k) space — each of N elements enters the heap once; heap holds k.
Pitfalls: Forgetting to update the running max when pushing; stopping before recording the
range that includes the last pushed element (record BEFORE checking exhaustion); using <=
instead of < so a later equal-width range with a larger start replaces the correct one.
"""
import heapq
from typing import List


class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        heap = [(row[0], i, 0) for i, row in enumerate(nums)]   # (value, list id, index)
        heapq.heapify(heap)
        cur_max = max(row[0] for row in nums)
        best = [heap[0][0], cur_max]
        while True:
            val, i, j = heapq.heappop(heap)            # smallest current element = low end
            if cur_max - val < best[1] - best[0]:
                best = [val, cur_max]
            if j + 1 == len(nums[i]):                  # list i exhausted: no later range covers it
                return best
            nxt = nums[i][j + 1]
            heapq.heappush(heap, (nxt, i, j + 1))
            cur_max = max(cur_max, nxt)                # high end only moves right


def brute_force(nums: List[List[int]]) -> List[int]:
    # Try every (lo, hi) pair of values; check all k lists have an element inside.
    values = sorted(set(v for row in nums for v in row))
    best = None
    for a in range(len(values)):
        for b in range(a, len(values)):
            lo, hi = values[a], values[b]
            if best is not None and hi - lo >= best[1] - best[0]:
                break                                   # wider than best already; larger b only worse
            if all(any(lo <= v <= hi for v in row) for row in nums):
                best = [lo, hi]
                break                                   # smallest hi for this lo found
    return best


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]], [20, 24]),
        ([[1, 2, 3], [1, 2, 3], [1, 2, 3]], [1, 1]),
        ([[10]], [10, 10]),                                  # single list, single element
        ([[1, 5], [4, 8]], [4, 5]),
        ([[-5, 0, 7], [2, 3], [-1, 9]], [-1, 2]),
    )
    for lists, want in cases:
        assert s.smallestRange(lists) == want, (lists, want)
        assert brute_force(lists) == want, (lists, want)
    import random
    random.seed(632)
    for _ in range(200):
        k = random.randint(1, 4)
        lists = [sorted(random.randint(-20, 20) for _ in range(random.randint(1, 5))) for _ in range(k)]
        assert s.smallestRange(lists) == brute_force(lists), lists
    print("ok")
