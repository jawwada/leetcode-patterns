"""
Online Majority Element In Subarray (LeetCode 1157)  — Hard
Pattern: Value -> sorted positions + randomized sampling with bisect verification

Problem
-------
Design MajorityChecker(arr) with query(left, right, threshold): return the element that occurs
at least threshold times in arr[left..right], or -1. threshold is always more than half the
length of the range, so at most one answer exists. Many queries follow one construction.
Example: arr=[1,1,2,2,1,1]; query(0,5,4) -> 1; query(0,3,3) -> -1; query(2,3,2) -> 2.

Brute force
-----------
Count the slice with a Counter on every query and check the most common element: O(n) time per
query, O(n) space. The wasted work is counting every value in the range when a majority, if it
exists, occupies more than half the slots; almost any position we look at is already the answer,
and all the other counts are irrelevant.

From brute force to optimal
---------------------------
The redundancy is counting everything to find the one value that dominates. Two observations.
(1) If a value's positions are stored sorted, "how many times does v occur in [l, r]" is two
bisects: O(log n), no scan. So verifying a CANDIDATE is cheap; the only hard part is finding it.
(2) A majority fills more than half the range, so a uniformly random index in [l, r] hits it with
probability > 1/2; after t independent samples the chance of never hitting it is < 2^-t. Sample
about 20 indices, verify each with the bisect count, and return on the first hit; if no sample
verifies, with overwhelming probability there is no majority. The structure is a dict value ->
sorted index list built once in O(n); each query is O(t log n) instead of O(n). (The
deterministic alternative is a segment tree of Boyer-Moore candidates, also verified by bisect.)

Intuition
---------
Guess and check. Guessing by sampling is good precisely because the thing we look for is big:
being a majority is the property that makes it easy to stumble upon. Checking is exact, so the
algorithm never returns a wrong element; the only risk is missing a majority after 20 misses in
a row, probability about one in a million per query.

Geometric view
--------------
Draw the range as a strip of cells, more than half of them painted with the majority colour.
Throwing darts at the strip, each dart lands on that colour with probability > 1/2. For each dart
the sorted position list of its colour is a number line; two binary searches clip it to [l, r]
and the gap between them is the exact count.

Steps
-----
1. Build pos[v] = sorted list of indices holding v (append in index order).
2. query: repeat 20 times: pick a random index in [left, right], read its value v.
3. count = bisect_right(pos[v], right) - bisect_left(pos[v], left).
4. If count >= threshold return v.
5. After all samples miss, return -1.

Complexity: O(n) build; O(t log n) per query with t = 20 samples, O(n) space — sampling is
            O(1), each verification two bisects on a sorted list.
Pitfalls: too few samples (failure probability 2^-t per query); forgetting to verify the sample
          (a random element is not a proof); using random.randrange(left, right) which excludes
          right.
"""
import random
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from typing import List


class MajorityChecker:
    def __init__(self, arr: List[int]):
        self.arr = arr
        self.pos = defaultdict(list)                  # value -> indices in increasing order
        for i, v in enumerate(arr):
            self.pos[v].append(i)
        self.rng = random.Random(0)                   # seeded: reproducible runs

    def query(self, left: int, right: int, threshold: int) -> int:
        for _ in range(20):                           # majority -> each sample misses with p < 1/2
            v = self.arr[self.rng.randint(left, right)]
            idx = self.pos[v]
            count = bisect_right(idx, right) - bisect_left(idx, left)   # exact occurrences in range
            if count >= threshold:
                return v
        return -1                                     # 20 misses: no majority (p_err < 1e-6)


class BruteForce:
    """Count the whole slice on every query."""

    def __init__(self, arr: List[int]):
        self.arr = arr

    def query(self, left: int, right: int, threshold: int) -> int:
        v, c = Counter(self.arr[left:right + 1]).most_common(1)[0]   # O(n) per query
        return v if c >= threshold else -1


if __name__ == "__main__":
    mc = MajorityChecker([1, 1, 2, 2, 1, 1])
    assert mc.query(0, 5, 4) == 1
    assert mc.query(0, 3, 3) == -1
    assert mc.query(2, 3, 2) == 2
    assert MajorityChecker([7]).query(0, 0, 1) == 7                  # single element

    random.seed(11)
    for _ in range(40):
        n = random.randint(1, 30)
        arr = [random.randint(1, 3) for _ in range(n)]
        fast, slow = MajorityChecker(arr), BruteForce(arr)
        for _ in range(30):
            l = random.randrange(n)
            r = random.randint(l, n - 1)
            th = (r - l + 1) // 2 + 1                                  # strictly more than half
            assert fast.query(l, r, th) == slow.query(l, r, th)
    print("ok")
