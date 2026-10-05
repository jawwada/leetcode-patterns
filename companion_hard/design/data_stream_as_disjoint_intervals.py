"""
Data Stream as Disjoint Intervals (LeetCode 352) - Hard
Chapter: design
Pattern: Sorted disjoint intervals with bisect

Non-negative integers arrive one at a time. Implement SummaryRanges with addNum(value) and
getIntervals(), which returns the values seen so far as a sorted list of disjoint closed
intervals, with consecutive integers merged.
Example: add 1 -> [[1,1]]; add 3 -> [[1,1],[3,3]]; add 7 -> [[1,1],[3,3],[7,7]];
add 2 -> [[1,3],[7,7]]; add 6 -> [[1,3],[6,7]].
"""
from bisect import bisect_right      # bisect_right(a, x): number of values <= x in sorted a


# --- brute force ---
class BruteForce:
    """Set of seen values; getIntervals re-sorts and re-merges everything. O(n log n) per query."""

    def __init__(self):
        self.seen = set()

    def addNum(self, value):
        self.seen.add(value)

    def getIntervals(self):
        out = []
        for value in sorted(self.seen):       # rebuilt from scratch on every call
            if len(out) > 0 and out[-1][1] == value - 1:
                out[-1][1] = value            # extends the last interval by one
            else:
                out.append([value, value])
        return out


# --- optimal ---
class SummaryRanges:
    """Keep starts and ends sorted; a new value touches at most two neighbours. O(log n) search."""

    def __init__(self):
        self.starts = []                      # sorted interval starts
        self.ends = []                        # the matching inclusive ends

    def addNum(self, value):
        i = bisect_right(self.starts, value)  # interval i - 1 has the largest start <= value
        if i > 0 and self.ends[i - 1] >= value:
            return                            # already inside an interval
        touch_left = i > 0 and self.ends[i - 1] == value - 1
        touch_right = i < len(self.starts) and self.starts[i] == value + 1
        if touch_left and touch_right:        # bridges a gap of exactly one: glue the two
            self.ends[i - 1] = self.ends[i]
            del self.starts[i]
            del self.ends[i]
        elif touch_left:
            self.ends[i - 1] = value
        elif touch_right:
            self.starts[i] = value
        else:
            self.starts.insert(i, value)      # a fresh singleton interval
            self.ends.insert(i, value)

    def getIntervals(self):
        out = []
        for i in range(len(self.starts)):
            out.append([self.starts[i], self.ends[i]])
        return out


# --- try the brute force ---
sr = BruteForce()
sr.addNum(1)
print(sr.getIntervals())     # -> [[1, 1]]
sr.addNum(3)
print(sr.getIntervals())     # -> [[1, 1], [3, 3]]
sr.addNum(7)
print(sr.getIntervals())     # -> [[1, 1], [3, 3], [7, 7]]
sr.addNum(2)
print(sr.getIntervals())     # -> [[1, 3], [7, 7]]
sr.addNum(6)
print(sr.getIntervals())     # -> [[1, 3], [6, 7]]
sr.addNum(2)                 # a duplicate changes nothing
print(sr.getIntervals())     # -> [[1, 3], [6, 7]]
sr.addNum(4)
sr.addNum(5)
print(sr.getIntervals())     # -> [[1, 7]]
print(BruteForce().getIntervals())   # -> []


# --- try the optimal ---
sr = SummaryRanges()
sr.addNum(1)
print(sr.getIntervals())     # -> [[1, 1]]
sr.addNum(3)
print(sr.getIntervals())     # -> [[1, 1], [3, 3]]
sr.addNum(7)
print(sr.getIntervals())     # -> [[1, 1], [3, 3], [7, 7]]
sr.addNum(2)
print(sr.getIntervals())     # -> [[1, 3], [7, 7]]
sr.addNum(6)
print(sr.getIntervals())     # -> [[1, 3], [6, 7]]
sr.addNum(2)                 # a duplicate changes nothing
print(sr.getIntervals())     # -> [[1, 3], [6, 7]]
sr.addNum(4)
sr.addNum(5)
print(sr.getIntervals())     # -> [[1, 7]]
print(SummaryRanges().getIntervals())   # -> []
