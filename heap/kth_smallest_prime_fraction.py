"""
K-th Smallest Prime Fraction (LeetCode 786)  — Hard
Pattern: K-way merge of sorted rows with a heap

Problem
-------
arr is sorted and contains 1 and distinct primes. Consider every fraction arr[i] / arr[j] with
i < j. Return the k-th smallest as [arr[i], arr[j]].
Example: arr=[1,2,3,5], k=3 -> [2,5]  (fractions in order: 1/5, 1/3, 2/5, 1/2, 3/5, 2/3).

Brute force
-----------
Materialise all n(n-1)/2 fractions, sort them, take index k-1: O(n^2 log n) time and O(n^2)
space. The wasted work is sorting fractions that can never be among the first k, and ignoring
the order that is already there: for a fixed numerator arr[i] the fractions arr[i]/arr[j] are
already sorted (decreasing in j), so most of the comparisons the sort performs are redundant.

From brute force to optimal
---------------------------
Step 1 (O(n^2 log n) -> O(k log n)): the fractions form a matrix whose row i (numerator arr[i])
is sorted from right to left; the problem is "k-th smallest in n sorted lists", i.e. a k-way
merge. Seed a min-heap with each row's smallest, arr[i]/arr[n-1]; pop the global minimum k-1
times and after each pop push that row's next fraction arr[i]/arr[j-1]. The heap never holds
more than n entries, so k-1 pops cost O(k log n), and the k-th pop is the answer. Step 2 (when
k is huge, up to n^2): binary search on the VALUE instead. For a guess m, count fractions
< m with a two-pointer sweep in O(n), tracking the largest fraction below m; narrow until
exactly k fractions are below the guess. That is O(n log(precision)), independent of k.

Intuition
---------
Each numerator owns a sorted list of fractions; a heap holding the current head of every list
always exposes the smallest unseen fraction overall. Pop k-1 heads and the heap top is the k-th
smallest: the same mechanism as merging k sorted linked lists.

Geometric view
--------------
Draw an upper-triangular grid: rows are numerators, columns are denominators. Values decrease
along a row to the right and increase down a column, so the smallest entries sit in the last
column. The heap holds one "cursor" per row, all starting at the right edge; each pop slides
one cursor one cell left. The set of visited cells grows as a staircase from the right edge.

Steps
-----
1. heap = [(arr[i] / arr[n-1], i, n-1) for every i < n-1]; heapify.
2. Repeat k-1 times: pop (value, i, j); if j-1 > i push (arr[i] / arr[j-1], i, j-1).
3. The heap top (value, i, j) is the k-th smallest; return [arr[i], arr[j]].

Complexity: O(n + k log n) time, O(n) space — heapify n rows, then k-1 pop/push pairs on a heap
            of at most n entries.
Pitfalls: pushing j+1 instead of j-1 (rows are sorted toward the LEFT); pushing a fraction with
          j == i (not a valid pair); using the heap when k ~ n^2 (binary search is the fix).
"""
import random
from heapq import heapify, heappop, heappush
from typing import List


class Solution:
    def kthSmallestPrimeFraction(self, arr: List[int], k: int) -> List[int]:
        n = len(arr)
        # row i holds arr[i]/arr[j] for j > i; smallest first when j runs n-1 down to i+1
        heap = [(arr[i] / arr[-1], i, n - 1) for i in range(n - 1)]
        heapify(heap)
        for _ in range(k - 1):
            _, i, j = heappop(heap)
            if j - 1 > i:
                heappush(heap, (arr[i] / arr[j - 1], i, j - 1))   # row i's next head
        _, i, j = heap[0]
        return [arr[i], arr[j]]


def brute_force(arr: List[int], k: int) -> List[int]:
    # Materialise every pair, sort all n(n-1)/2 fractions, take the k-th.
    n = len(arr)
    pairs = [(arr[i] / arr[j], arr[i], arr[j]) for i in range(n) for j in range(i + 1, n)]
    pairs.sort()
    return [pairs[k - 1][1], pairs[k - 1][2]]


def primes_upto(limit: int) -> List[int]:
    return [p for p in range(2, limit + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


if __name__ == "__main__":
    s = Solution()
    assert s.kthSmallestPrimeFraction([1, 2, 3, 5], 3) == [2, 5]
    assert s.kthSmallestPrimeFraction([1, 7], 1) == [1, 7]
    assert s.kthSmallestPrimeFraction([1, 2, 3, 5], 6) == [2, 3]   # the largest fraction
    assert s.kthSmallestPrimeFraction([1, 2, 3, 5], 1) == [1, 5]

    random.seed(6)
    pool = primes_upto(200)
    for _ in range(200):
        arr = [1] + sorted(random.sample(pool, random.randint(1, 10)))
        n = len(arr)
        k = random.randint(1, n * (n - 1) // 2)
        assert s.kthSmallestPrimeFraction(arr, k) == brute_force(arr, k)
    print("ok")
