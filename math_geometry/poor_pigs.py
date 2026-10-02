"""
Poor Pigs (LeetCode 458)  — Hard
Pattern: Information counting (states per pig, mixed-radix labelling)

Problem
-------
buckets of liquid, exactly one poisonous. A pig that drinks poison dies after minutesToDie
minutes; you have minutesToTest minutes in total and may feed any pigs any buckets at once, then
wait, then repeat. Return the minimum number of pigs that guarantees finding the poisoned bucket.
Example: buckets=4, minutesToDie=15, minutesToTest=15 -> 2; buckets=1000, 15, 60 -> 5.

Brute force
-----------
Try pigs = 0, 1, 2, ... and for each count how many distinct outcomes the experiment can end in
by enumerating every outcome vector explicitly (for each pig: died in round 1, 2, ..., T, or
survived) with itertools.product, stopping at the first count >= buckets. Enumerating
(T+1)^pigs vectors is exponential time and O(pigs) space per vector. The wasted work is listing
vectors one by one just to count them, when the count is a product we can write down directly.

From brute force to optimal
---------------------------
The redundancy is enumerating outcomes instead of counting them. The observation: with T =
minutesToTest // minutesToDie rounds, each pig ends in exactly one of T+1 states (dies in round
r for r = 1..T, or survives), and a pig's state is independent of the others', so p pigs have
(T+1)^p distinguishable outcomes. Each outcome must point at a distinct bucket, so (T+1)^p >=
buckets is necessary. It is also sufficient: label bucket b by its p-digit base-(T+1) number and
in round r let pig i drink from every bucket whose i-th digit equals r; the round in which pig i
dies (or never) reveals digit i, and all digits together name the bucket. So the answer is the
smallest p with (T+1)^p >= buckets: a loop of O(log buckets) multiplications, no enumeration.

Intuition
---------
A pig is a sensor with T+1 readings, not a yes/no bit. The puzzle looks adversarial but is just
"how many base-(T+1) digits does it take to write the largest bucket index". The scheme that
achieves the bound is to make each pig read one digit of the bucket's label over the rounds.

Geometric view
--------------
Arrange the buckets in a p-dimensional grid with side T+1; pig i is responsible for axis i. In
round r, pig i drinks every bucket on the slice "coordinate i equals r". The round it dies
reports its coordinate; surviving means coordinate 0. The p reports are the coordinates of the
poisoned cell, so the grid must have at least `buckets` cells: (T+1)^p >= buckets.

Steps
-----
1. states = minutesToTest // minutesToDie + 1.
2. pigs = 0; while states ** pigs < buckets: pigs += 1.
3. Return pigs (0 when there is a single bucket).

Complexity: O(log buckets) time, O(1) space — the loop runs once per base-(T+1) digit.
Pitfalls: counting only 2 states per pig (ignores WHICH round it died); using a floating-point
          log with ceil (precision errors at exact powers); forgetting buckets = 1 -> 0 pigs.
"""
from itertools import product


class Solution:
    def poorPigs(self, buckets: int, minutesToDie: int, minutesToTest: int) -> int:
        states = minutesToTest // minutesToDie + 1   # dies in round 1..T, or survives
        pigs = 0
        while states ** pigs < buckets:              # need one distinct outcome per bucket
            pigs += 1
        return pigs


def brute_force(buckets: int, minutesToDie: int, minutesToTest: int) -> int:
    # Enumerate every outcome vector (round of death or survival per pig) and count them.
    rounds = minutesToTest // minutesToDie
    pigs = 0
    while True:
        outcomes = set(product(range(rounds + 1), repeat=pigs))   # (T+1)^pigs vectors
        if len(outcomes) >= buckets:
            return pigs
        pigs += 1


if __name__ == "__main__":
    s = Solution()
    assert s.poorPigs(4, 15, 15) == 2
    assert s.poorPigs(1000, 15, 60) == 5
    assert s.poorPigs(1, 1, 1) == 0                                 # one bucket: nothing to test
    assert s.poorPigs(125, 1, 4) == 3                               # exact power: 5^3 == 125
    assert s.poorPigs(126, 1, 4) == 4

    for buckets in range(1, 300, 7):
        for die in (1, 2, 5):
            for test in (1, 2, 5, 10):
                if test >= die:
                    assert s.poorPigs(buckets, die, test) == brute_force(buckets, die, test)
    print("ok")
