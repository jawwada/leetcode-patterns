"""
Create Sorted Array through Instructions (LeetCode 1649)  — Hard
Pattern: Fenwick tree over values (order-statistics counting)

Problem
-------
Insert the numbers of instructions one by one into a sorted container. Inserting x costs
min(number of elements already present that are < x, number that are > x). Return the total
cost modulo 1e9+7.
Example: [1,5,6,2] -> 0 + 0 + 0 + min(1, 2) = 1  (inserting 2: one smaller {1}, two larger {5,6}).

Brute force
-----------
Keep a Python list sorted. For each x, bisect_left gives the count of smaller values and
len - bisect_right the count of larger ones, then insort(x). The bisects are O(log n) but the
list insert shifts everything after the slot: O(n) per step, O(n^2) time overall, O(n) space.
The wasted work is physically moving elements just to keep the ORDER, when all we ever ask is
"how many inserted values are below / above x" - counts, not positions.

From brute force to optimal
---------------------------
The redundancy is maintaining a sorted sequence when only counts by value are needed. Values
are bounded (1..1e5), so index a structure by VALUE rather than by position: cnt[v] = how many
times v has been inserted. "Smaller than x" is the prefix sum cnt[1..x-1] and "larger than x" is
inserted_so_far - cnt[1..x]. A Fenwick tree gives point increment and prefix sum in O(log V)
each, so every instruction costs two prefix queries and one update. The invariant: tree[i]
stores the count of inserted values in the block (i - lowbit(i), i], so any prefix is the sum
of O(log V) blocks. Total O(n log V) instead of O(n^2).

Intuition
---------
Sorting is overkill when the alphabet of values is small and fixed: a histogram over values,
read as a prefix sum, answers rank questions directly. The Fenwick tree is a histogram whose
prefix sums stay cheap under increments.

Geometric view
--------------
A number line 1..V with a counter at each tick. Inserting x raises the counter at x; the cost is
the smaller of the total mass left of x and the total mass right of x. The Fenwick tree layers
blocks over the line (sizes 1, 2, 4, ... by lowest set bit) so that the mass left of any point
is a sum of O(log V) blocks.

Steps
-----
1. size = max(instructions); tree = [0] * (size + 1).
2. For the k-th instruction x (k values already inserted):
   less = prefix(x - 1); greater = k - prefix(x); cost += min(less, greater).
3. add(x): walk i = x, x + lowbit(x), ... incrementing tree[i].
4. Return cost % (1e9 + 7).

Complexity: O(n log V) time, O(V) space — each instruction does two prefix walks and one update
            over O(log V) nodes; the tree spans the value range.
Pitfalls: counting values equal to x as smaller or larger (use prefix(x-1) and k - prefix(x));
          forgetting the modulo; a 0-indexed Fenwick walk (lowbit(0) = 0 loops forever).
"""
import random
from bisect import bisect_left, bisect_right, insort
from typing import List


class Solution:
    def createSortedArray(self, instructions: List[int]) -> int:
        MOD = 10 ** 9 + 7
        size = max(instructions)
        tree = [0] * (size + 1)                 # 1-indexed Fenwick tree over values

        def add(i: int) -> None:
            while i <= size:
                tree[i] += 1
                i += i & -i

        def prefix(i: int) -> int:              # how many inserted values are <= i
            total = 0
            while i > 0:
                total += tree[i]
                i -= i & -i
            return total

        cost = 0
        for inserted, x in enumerate(instructions):
            less = prefix(x - 1)
            greater = inserted - prefix(x)      # all inserted so far minus those <= x
            cost += min(less, greater)
            add(x)
        return cost % MOD


def brute_force(instructions: List[int]) -> int:
    # Sorted list with insort: bisects are O(log n) but each insert shifts O(n) elements.
    arr, cost = [], 0
    for x in instructions:
        less = bisect_left(arr, x)
        greater = len(arr) - bisect_right(arr, x)
        cost += min(less, greater)
        insort(arr, x)                          # O(n) shift
    return cost % (10 ** 9 + 7)


if __name__ == "__main__":
    s = Solution()
    assert s.createSortedArray([1, 5, 6, 2]) == 1
    assert s.createSortedArray([1, 2, 3, 6, 5, 4]) == 3
    assert s.createSortedArray([1, 3, 3, 3, 2, 4, 2, 1, 2]) == 4
    assert s.createSortedArray([7]) == 0                          # single element
    assert s.createSortedArray([4, 4, 4, 4]) == 0                 # equal values cost nothing

    random.seed(9)
    for _ in range(300):
        a = [random.randint(1, 12) for _ in range(random.randint(1, 25))]
        assert s.createSortedArray(a) == brute_force(a)
    print("ok")
