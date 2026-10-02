"""
Largest Component Size by Common Factor (LeetCode 952)  — Hard
Pattern: Union-Find (disjoint set union)

Problem
-------
Given unique positive integers nums, build a graph with an edge between nums[i] and nums[j]
whenever gcd(nums[i], nums[j]) > 1. Return the size of the largest connected component.
Example: [4,6,15,35] -> 4 (4-6, 6-15, 15-35).  [20,50,9,63] -> 2.

Brute force
-----------
Check every pair (i, j): if gcd > 1, union them (or add an edge), then take the largest
component. O(n^2 * log(max)) time, O(n) space. The waste: the pairwise test asks "do these
two share a prime?" n^2 times, re-deriving the same prime factors of each number over and
over; with n = 2*10^4 that is 2*10^8 gcds.

From brute force to optimal
---------------------------
The redundancy is comparing numbers pairwise when the connection is really through a
shared PRIME. Observation: nums[i] and nums[j] are adjacent iff they share a prime factor,
so connectivity is unchanged if we add one hub node per prime and connect each number to
the primes dividing it -- two numbers sharing prime p both touch hub p. Each number has at
most ~6 distinct primes below 10^5 and is factored once by trial division up to sqrt, so
the union-find sees O(n * sqrt(max)) work instead of O(n^2). Finally count how many
original numbers share each root.

Intuition
---------
Primes are the glue. Instead of asking every pair whether they are glued, factor each
number and union it with each of its primes; the hubs transitively connect every number
that shares any prime with any other. The component size is the number of input numbers
(not hubs) under each root, so count roots over nums only.

Geometric view
--------------
Picture a bipartite picture: numbers on the left, primes on the right, a line from each
number to each of its prime factors. Two numbers are in the same component iff you can
walk between them alternating number-prime-number-... Union-find collapses the whole
picture into blobs; the answer is the blob containing the most left-side nodes.

Steps
-----
1. parent = {} (lazily created nodes for numbers and primes).
2. For each x in nums: trial-divide by p = 2, 3, ... while p*p <= remaining; on each prime
   factor union(x, p) and strip it; if the remainder > 1 it is a prime: union(x, remainder).
3. Count find(x) for x in nums; return the largest count.

Complexity: O(n * sqrt(max(nums)) * alpha) time, O(n + P) space — trial division per number dominates; hubs for distinct primes.
Pitfalls: counting prime hub nodes toward component size (count only over nums); treating 1
as having a factor (it has none and is always a singleton); forgetting the leftover factor
after the sqrt loop when the remainder is a large prime.
"""
from collections import Counter
from math import gcd
from typing import List


class Solution:
    def largestComponentSize(self, nums: List[int]) -> int:
        parent = {}

        def find(x: int) -> int:
            parent.setdefault(x, x)
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            parent[find(a)] = find(b)

        for x in nums:
            rem, p = x, 2
            while p * p <= rem:
                if rem % p == 0:
                    union(x, p)  # number <-> prime hub
                    while rem % p == 0:
                        rem //= p
                p += 1
            if rem > 1:
                union(x, rem)  # leftover is a prime factor
        return max(Counter(find(x) for x in nums).values())  # count numbers only, not hubs


def brute_force(nums: List[int]) -> int:
    # Pairwise gcd test, union every pair with gcd > 1, then take the largest component.
    n = len(nums)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            i = parent[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if gcd(nums[i], nums[j]) > 1:
                parent[find(i)] = find(j)
    return max(Counter(find(i) for i in range(n)).values())


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([4, 6, 15, 35], 4),
        ([20, 50, 9, 63], 2),
        ([2, 3, 6, 7, 4, 12, 21, 39], 8),
        ([1], 1),
        ([1, 2, 3, 5, 7, 11, 13], 1),
        ([100000, 99999, 6, 9, 14], 5),
        ([99991, 2], 1),  # 99991 is prime: leftover after the sqrt loop
    )
    for nums, want in cases:
        assert brute_force(nums) == want, (nums, brute_force(nums))
        assert s.largestComponentSize(nums) == want, (nums, s.largestComponentSize(nums))
    print("ok")
