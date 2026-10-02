"""
Minimize Deviation in Array (LeetCode 1675)  — Hard
Pattern: Max-heap of normalised values, repeatedly shrink the maximum

Problem
-------
You may apply any number of operations to nums: halve an even element, or double an odd
element. The deviation is max(nums) - min(nums). Return the minimum deviation achievable.
Example: [1,2,3,4] -> 1 (double 1 -> 2, halve 4 -> 2: [2,2,3,2]). [4,1,5,20,3] -> 3
([4,2,5,5,3] after doubling 1 and halving 20 twice). [2,10,8] -> 3.

Brute force
-----------
Each element can only ever reach a short chain of values: an odd x reaches {x, 2x}; an even x
reaches {x, x/2, x/4, ..., its odd core} -- doubling an even number is never useful because
halving undoes it and both ends of the chain are already present. Enumerate every combination
of one value per element (a Cartesian product), compute max - min, keep the best. Exponential:
O(prod of chain lengths) ~ O((log M)^n), O(n) space. The waste: almost all combinations are
dominated -- lowering any element that is not the current maximum cannot reduce the deviation
and may raise it.

From brute force to optimal
---------------------------
The redundancy is varying elements independently when only the maximum matters. Observation 1:
every element's reachable chain is a geometric ladder, and the only sensible starting state is
the TOP of each ladder (double every odd; evens stay). From there every move is a halving, and
all moves are reversible, so there is no "wrong order" -- only the choice of which element to
halve. Observation 2: halving a non-maximum element cannot shrink max - min (max stays, min may
drop), so the only useful move is to halve the current maximum, and it is useful only if that
maximum is even. So: push all top-of-ladder values into a max-heap, track the min, record the
deviation, pop the max; if it is odd, no further move can help, stop; otherwise halve it, push
it back, update the min. Each element is halved at most log M times -> O(n log M log n).

Intuition
---------
Normalise so that the only operation left is "halve". Then the deviation is a quantity that
only a halving of the maximum can improve, and a halving of the maximum can also hurt (if it
drops below the current min) -- so we take the best deviation seen along the way rather than
the final one. The process is forced: the maximum is the only element whose move can shrink
the gap, and once the maximum is odd it is frozen, and so is every deviation after it.

Geometric view
--------------
Each element is a vertical ladder of rungs at x, x/2, x/4, ... down to its odd core; we start
every element on its top rung. A max-heap triangle holds the current rung of each element with
the highest at the apex. Each step the apex element steps down one rung; the band between the
highest and lowest rung is the deviation, and we remember its narrowest width. The process
stops when the apex sits on an odd rung (bottom of its ladder).

Steps
-----
1. For each x: v = 2x if x is odd else x. Push -v onto a max-heap; lo = min(lo, v).
2. best = infinity.
3. Loop: hi = -heap[0]; best = min(best, hi - lo).
4. If hi is odd, break (cannot halve the maximum any more).
5. Pop hi, push hi // 2, lo = min(lo, hi // 2).
6. Return best.

Complexity: O(n log M log n) time, O(n) space — each element is halved at most log M times, each
heap op is log n.
Pitfalls: Returning the final deviation instead of the minimum seen; forgetting to update the
running minimum after a halving; treating "double an even" as a useful move.
"""
import heapq
from typing import List


class Solution:
    def minimumDeviation(self, nums: List[int]) -> int:
        heap = [-(x * 2 if x % 2 else x) for x in nums]   # every element at the top of its ladder
        heapq.heapify(heap)
        lo = -max(heap)                                    # running minimum (max of negatives)
        best = float("inf")
        while True:
            hi = -heap[0]                                  # the only element worth moving
            best = min(best, hi - lo)
            if hi % 2:                                     # odd maximum: frozen, nothing else helps
                return best
            heapq.heapreplace(heap, -(hi // 2))
            lo = min(lo, hi // 2)


def brute_force(nums: List[int]) -> int:
    # Exponential: every element independently picks one rung of its ladder
    # (odd x -> {x, 2x}; even x -> {x, x/2, ..., odd core}); score max - min.
    from itertools import product
    ladders = []
    for x in nums:
        if x % 2:
            rungs = [x, 2 * x]
        else:
            rungs = []
            while x % 2 == 0:
                rungs.append(x)
                x //= 2
            rungs.append(x)                                 # the odd core
        ladders.append(rungs)
    return min(max(choice) - min(choice) for choice in product(*ladders))


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([1, 2, 3, 4], 1),
        ([4, 1, 5, 20, 3], 3),
        ([2, 10, 8], 3),
        ([7], 0),                                           # single element
        ([3, 5], 1),                                        # all odd: double one, keep the other
        ([1, 1024], 0),
    )
    for nums, want in cases:
        assert s.minimumDeviation(nums[:]) == want, (nums, want)
        assert brute_force(nums) == want, (nums, want)
    import random
    random.seed(1675)
    for _ in range(150):
        nums = [random.randint(1, 40) for _ in range(random.randint(1, 6))]
        assert s.minimumDeviation(nums[:]) == brute_force(nums), nums
    print("ok")
