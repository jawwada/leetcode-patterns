"""
Find Median from Data Stream (LeetCode 295)
Support addNum(x) and findMedian() over every number added so far.
  add 5, 15, 1, 3  ->  medians 5.0, 10.0, 5.0, 4.0

Idea: split the numbers into two halves at the median.
      low  = max-heap of the smaller half (stored negated), high = min-heap of the larger half.
      The median sits at the two roots; keep len(low) == len(high) or one more.

Pseudocode:
  addNum(x):
      push x into low
      move low's max into high       # keeps every low <= every high
      if high is bigger: move high's min back to low
  findMedian():
      odd count -> top of low, even -> average of both tops

Time O(log n) per add, O(1) per median. Space O(n).
"""
import heapq


class MedianFinder:
    def __init__(self):
        self.low = []    # max-heap (negated): smaller half
        self.high = []   # min-heap: larger half

    def addNum(self, num):
        heapq.heappush(self.low, -num)                            # into the smaller half
        heapq.heappush(self.high, -heapq.heappop(self.low))       # its max crosses over
        if len(self.high) > len(self.low):                        # rebalance sizes
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self):
        if len(self.low) > len(self.high):                        # odd count
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2                  # even count


if __name__ == "__main__":
    mf = MedianFinder()
    mf.addNum(5)
    print(mf.findMedian())  # 5.0
    mf.addNum(15)
    print(mf.findMedian())  # 10.0
    mf.addNum(1)
    mf.addNum(3)
    print(mf.findMedian())  # 4.0
