"""
Online Majority Element In Subarray (LeetCode 1157) - Hard
Chapter: design
Pattern: Value -> sorted positions + randomized sampling with bisect verification

Design MajorityChecker(arr) with query(left, right, threshold), which returns the element occurring
at least threshold times in arr[left..right], or -1. threshold is always more than half the range
length, so at most one answer exists. Many queries follow a single construction.
Example: arr=[1,1,2,2,1,1]; query(0,5,4) -> 1, query(0,3,3) -> -1, query(2,3,2) -> 2.
"""
import random
from bisect import bisect_left, bisect_right   # index of the first value >= x / > x in sorted a


# --- brute force ---
class BruteForce:
    """Count every value of the slice on every query. O(n) per query."""

    def __init__(self, arr):
        self.arr = arr

    def query(self, left, right, threshold):
        counts = {}
        for i in range(left, right + 1):      # the whole slice, every time
            counts[self.arr[i]] = counts.get(self.arr[i], 0) + 1
        for value in counts:
            if counts[value] >= threshold:
                return value
        return -1


# --- optimal ---
class MajorityChecker:
    """Guess by random sampling, check with two bisects on the value's positions. O(20 log n)."""

    def __init__(self, arr):
        self.arr = arr
        self.positions = {}                   # value -> its indices in increasing order
        for i in range(len(arr)):
            if arr[i] not in self.positions:
                self.positions[arr[i]] = []
            self.positions[arr[i]].append(i)
        self.rng = random.Random(0)           # seeded so every run behaves the same

    def count_in_range(self, value, left, right):
        idx = self.positions[value]
        return bisect_right(idx, right) - bisect_left(idx, left)   # exact occurrences in [l, r]

    def query(self, left, right, threshold):
        for _ in range(20):                   # a majority is missed by one sample with p < 1/2
            value = self.arr[self.rng.randint(left, right)]
            if self.count_in_range(value, left, right) >= threshold:
                return value
        return -1                             # 20 misses in a row: no majority (p < 1e-6)


# --- try the brute force ---
mc = BruteForce([1, 1, 2, 2, 1, 1])
print(mc.query(0, 5, 4))     # -> 1
print(mc.query(0, 3, 3))     # -> -1
print(mc.query(2, 3, 2))     # -> 2
print(BruteForce([7]).query(0, 0, 1))   # -> 7


# --- try the optimal ---
mc = MajorityChecker([1, 1, 2, 2, 1, 1])
print(mc.query(0, 5, 4))     # -> 1
print(mc.query(0, 3, 3))     # -> -1
print(mc.query(2, 3, 2))     # -> 2
print(MajorityChecker([7]).query(0, 0, 1))   # -> 7
