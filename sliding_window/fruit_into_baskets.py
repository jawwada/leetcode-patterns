"""
Fruit Into Baskets (LeetCode 904)  — Medium
Pattern: Variable-size sliding window

Problem
-------
fruits[i] is the type of the tree at position i. You have two baskets, each holding one type
only (unlimited quantity). Starting anywhere, pick one fruit per tree moving right; stop when
a tree's type fits neither basket. Return the maximum fruits picked. Equivalently: the longest
subarray with at most 2 distinct values.
Example: fruits = [1,2,3,2,2] -> 4 ([2,3,2,2]).

Brute force
-----------
For every start i, walk right while the set of types stays <= 2, record the length.
O(n^2) time, O(1) space. The wasted work: start i+1 re-walks the stretch that start i
already proved has <= 2 types.

From brute force to optimal
---------------------------
The redundancy is re-validating a stretch already known to be valid. Observation: validity
("at most 2 distinct") is monotone -- shrinking a valid window keeps it valid, growing an
invalid one keeps it invalid -- so when the window becomes invalid we can advance left
instead of restarting. To know when a type leaves the window we need its count, hence a
small hash map type -> count. The window grows by one on the right and shrinks on the left
only until the third type disappears; each index enters and leaves once.

Intuition
---------
Keep the longest window ending at the current tree that uses at most two types. A third type
arriving forces the left edge forward until one of the old types is exhausted. Track counts
so you know exactly when that happens.

Geometric view
--------------
A window [L, R] slides over the row of trees. Above it a tiny histogram of at most two bars
(the baskets). When R hits a third type a third bar appears; L moves right, shrinking bars,
until one bar hits zero and vanishes, leaving two again.

Steps
-----
1. count = {} (type -> occurrences in window), left = 0, best = 0.
2. For each right, type f: count[f] += 1.
3. While len(count) > 2: decrement count[fruits[left]], delete it at zero, left += 1.
4. best = max(best, right - left + 1). Return best.

Complexity: O(n) time, O(1) space — the map holds at most 3 keys; each index is touched twice.
Pitfalls: Forgetting to delete a key when its count hits zero (len(count) would stay 3);
treating it as "two specific types chosen up front" instead of "any two".
"""
from collections import defaultdict
from typing import List


class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        count = defaultdict(int)             # type -> occurrences inside the window
        left = best = 0
        for right, f in enumerate(fruits):
            count[f] += 1
            while len(count) > 2:            # third type: shrink until one type is gone
                count[fruits[left]] -= 1
                if count[fruits[left]] == 0:
                    del count[fruits[left]]
                left += 1
            best = max(best, right - left + 1)
        return best


def brute_force(fruits: List[int]) -> int:
    best = 0
    for i in range(len(fruits)):
        types = set()                        # re-walks the stretch for every start
        for j in range(i, len(fruits)):
            types.add(fruits[j])
            if len(types) > 2:
                break
            best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = [[1, 2, 1], [0, 1, 2, 2], [1, 2, 3, 2, 2], [3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4], [7]]
    assert s.totalFruit([1, 2, 1]) == 3
    assert s.totalFruit([0, 1, 2, 2]) == 3
    assert s.totalFruit([1, 2, 3, 2, 2]) == 4
    assert s.totalFruit([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]) == 5
    assert s.totalFruit([7]) == 1
    for c in cases:
        assert s.totalFruit(c) == brute_force(c)
    print("ok")
