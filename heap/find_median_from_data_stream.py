"""
Find Median from Data Stream (LeetCode 295)  — Hard
Pattern: Two heaps (balanced max-heap / min-heap)

Problem
-------
Design a class with addNum(num) and findMedian(). findMedian returns the median of all numbers
added so far: the middle value for an odd count, the mean of the two middle values for an even
count.
Example: add(1), add(2) -> findMedian()=1.5; add(3) -> findMedian()=2.0.

Brute force
-----------
Append each number to a list; on findMedian, sort the list and read the middle element(s).
O(1) add, O(n log n) findMedian, O(n) space. (Inserting in sorted order with bisect gives
O(n) add, O(1) median, still linear.) The waste: the full sorted order is rebuilt or maintained
even though only the boundary between the lower half and the upper half ever matters.

From brute force to optimal
---------------------------
The redundancy is maintaining order inside each half. Observation: the median is determined by
the MAX of the lower half and the MIN of the upper half; the internal order of each half is
irrelevant. So keep the lower half in a max-heap and the upper half in a min-heap, each exposing
exactly the element we need at its root. Insertion pushes into one heap and, if the sizes drift
apart by more than one, moves a root across. Both operations are O(log n), and findMedian reads
the roots in O(1).

Intuition
---------
Split the numbers into "small half" and "large half" so that every small <= every large and the
halves differ in size by at most one. The median lives at the seam: the biggest small and the
smallest large. Heaps are the cheapest structure that always exposes a max or a min.

Geometric view
--------------
Two triangles joined apex to apex along a horizontal seam. The left triangle (max-heap) points
right, its apex is the largest small number; the right triangle (min-heap) points left, its apex
is the smallest large number. A new number drops into the lower triangle, and if it is too big
for that side the apex is flicked across the seam. The seam IS the median.

Steps
-----
1. Keep small (max-heap via negation) and large (min-heap). Invariant: len(small) is len(large)
   or len(large) + 1, and max(small) <= min(large).
2. addNum: push onto small, then move small's max to large (this guarantees the ordering).
3. If large is now bigger than small, move large's min back to small (restores the size rule).
4. findMedian: if sizes differ return -small[0]; else return (-small[0] + large[0]) / 2.

Complexity: O(log n) addNum, O(1) findMedian, O(n) space — two heaps hold all n numbers.
Pitfalls: Forgetting to negate when moving between heaps; letting the size invariant drift so the
median reads the wrong root; integer division when the count is even.
"""
import heapq


class MedianFinder:
    def __init__(self):
        self.small = []          # max-heap (negated) of the lower half
        self.large = []          # min-heap of the upper half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        # move the lower half's max across; guarantees max(small) <= min(large)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):           # keep small the (possibly) bigger side
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2


class BruteForce:
    def __init__(self):
        self.nums = []

    def addNum(self, num: int) -> None:
        self.nums.append(num)

    def findMedian(self) -> float:
        a = sorted(self.nums)                           # re-sorts everything each query
        n = len(a)
        if n % 2:
            return float(a[n // 2])
        return (a[n // 2 - 1] + a[n // 2]) / 2


if __name__ == "__main__":
    m, b = MedianFinder(), BruteForce()
    m.addNum(1); b.addNum(1)
    m.addNum(2); b.addNum(2)
    assert m.findMedian() == 1.5 == b.findMedian()
    m.addNum(3); b.addNum(3)
    assert m.findMedian() == 2.0 == b.findMedian()
    m2 = MedianFinder()
    m2.addNum(-5)
    assert m2.findMedian() == -5.0                      # single element, negative
    import random
    m3, b3 = MedianFinder(), BruteForce()
    for _ in range(300):                                # random cross-check vs brute force
        v = random.randint(-100, 100)
        m3.addNum(v); b3.addNum(v)
        assert m3.findMedian() == b3.findMedian()
    print("ok")
