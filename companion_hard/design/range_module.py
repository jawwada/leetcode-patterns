"""
Range Module (LeetCode 715) - Hard
Chapter: design
Pattern: Sorted disjoint intervals with bisect

Track half-open ranges [left, right) of numbers. addRange(l, r) marks the range tracked,
removeRange(l, r) untracks it, and queryRange(l, r) returns True iff every point of [l, r) is
currently tracked; the three operations interleave arbitrarily.
Example: addRange(10,20); removeRange(14,16); queryRange(10,14) -> True;
queryRange(13,15) -> False; queryRange(16,17) -> True.
"""
from bisect import bisect_left, bisect_right   # index of the first value >= x / > x in sorted a


# --- brute force ---
class BruteForce:
    """Set of every tracked integer point. O(right - left) per operation."""

    def __init__(self):
        self.points = set()

    def addRange(self, left, right):
        for x in range(left, right):          # touches every point of the block, not its two ends
            self.points.add(x)

    def queryRange(self, left, right):
        for x in range(left, right):
            if x not in self.points:
                return False
        return True

    def removeRange(self, left, right):
        for x in range(left, right):
            self.points.discard(x)


# --- optimal ---
class RangeModule:
    """Flat sorted list of boundaries [l0, r0, l1, r1, ...]; parity says in or out. O(log n)."""

    def __init__(self):
        self.ends = []                        # even index opens a tracked block, odd closes it

    def addRange(self, left, right):
        i = bisect_left(self.ends, left)      # left == an existing end -> i is odd: blocks merge
        j = bisect_right(self.ends, right)    # right == an existing start -> j odd: blocks merge
        new = []
        if i % 2 == 0:
            new.append(left)                  # left falls in a gap: it opens the merged block
        if j % 2 == 0:
            new.append(right)                 # right falls in a gap: it closes the merged block
        self.ends[i:j] = new                  # every boundary strictly inside is swallowed

    def queryRange(self, left, right):
        i = bisect_right(self.ends, left)
        j = bisect_left(self.ends, right)
        return i == j and i % 2 == 1          # both ends inside the same tracked block

    def removeRange(self, left, right):
        i = bisect_left(self.ends, left)
        j = bisect_right(self.ends, right)
        new = []
        if i % 2 == 1:
            new.append(left)                  # left was inside a block: that block now ends here
        if j % 2 == 1:
            new.append(right)                 # right was inside a block: a block restarts here
        self.ends[i:j] = new


# --- try the brute force ---
rm = BruteForce()
rm.addRange(10, 20)
rm.removeRange(14, 16)
print(rm.queryRange(10, 14))     # -> True
print(rm.queryRange(13, 15))     # -> False
print(rm.queryRange(16, 17))     # -> True
rm.addRange(14, 16)              # fills the hole: one block [10, 20) again
print(rm.queryRange(10, 20))     # -> True
rm.addRange(20, 25)              # a touching block merges
print(rm.queryRange(10, 25))     # -> True
rm.removeRange(10, 25)
print(rm.queryRange(10, 11))     # -> False


# --- try the optimal ---
rm = RangeModule()
rm.addRange(10, 20)
rm.removeRange(14, 16)
print(rm.queryRange(10, 14))     # -> True
print(rm.queryRange(13, 15))     # -> False
print(rm.queryRange(16, 17))     # -> True
rm.addRange(14, 16)              # fills the hole: one block [10, 20) again
print(rm.queryRange(10, 20))     # -> True
rm.addRange(20, 25)              # a touching block merges
print(rm.queryRange(10, 25))     # -> True
rm.removeRange(10, 25)
print(rm.queryRange(10, 11))     # -> False
