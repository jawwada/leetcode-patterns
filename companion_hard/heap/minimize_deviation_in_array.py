"""
Minimize Deviation in Array (LeetCode 1675) - Hard
Chapter: heap
Pattern: Max-heap of normalised values, repeatedly shrink the maximum

You may apply any number of operations to nums: halve an even element or double an odd element.
The deviation is max(nums) - min(nums). Return the minimum deviation achievable.
Example: [1,2,3,4] -> 1 (double 1, halve 4: [2,2,3,2]). [4,1,5,20,3] -> 3. [2,10,8] -> 3.
"""
import heapq                       # heappush / heappop keep the smallest item at index 0
from itertools import product      # every combination of one choice per list, as tuples


# --- brute force ---
def ladder(x):
    """All values x can become: odd x -> [x, 2x]; even x -> x, x/2, ... down to its odd core."""
    if x % 2 == 1:
        return [x, 2 * x]
    rungs = []
    while x % 2 == 0:
        rungs.append(x)
        x = x // 2
    rungs.append(x)                            # the odd core
    return rungs


def brute_force(nums):
    """Try every choice of one rung per element and score max - min. Exponential time."""
    ladders = []
    for x in nums:
        ladders.append(ladder(x))
    best = None
    for choice in product(*ladders):           # one value picked from each element's ladder
        deviation = max(choice) - min(choice)
        if best is None or deviation < best:
            best = deviation
    return best


# --- optimal ---
def minimum_deviation(nums):
    """Start each element at the top of its ladder; halve the max while even. O(n log M log n)."""
    heap = []                                  # negated values: the root is the current maximum
    low = None                                 # the current minimum, which only ever decreases
    for x in nums:
        if x % 2 == 1:
            x = 2 * x                          # the only sensible start: doubled once
        heapq.heappush(heap, -x)
        if low is None or x < low:
            low = x
    best = None
    while True:
        high = -heapq.heappop(heap)            # the only element worth moving
        if best is None or high - low < best:
            best = high - low
        if high % 2 == 1:
            return best                        # an odd maximum can only grow: nothing else helps
        heapq.heappush(heap, -(high // 2))
        low = min(low, high // 2)


# --- try the brute force ---
print(brute_force([1, 2, 3, 4]))        # -> 1
print(brute_force([4, 1, 5, 20, 3]))    # -> 3
print(brute_force([2, 10, 8]))          # -> 3
print(brute_force([3, 5]))              # -> 1


# --- try the optimal ---
print(minimum_deviation([1, 2, 3, 4]))        # -> 1
print(minimum_deviation([4, 1, 5, 20, 3]))    # -> 3
print(minimum_deviation([2, 10, 8]))          # -> 3
print(minimum_deviation([3, 5]))              # -> 1
