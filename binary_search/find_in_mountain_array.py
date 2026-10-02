"""
Find in Mountain Array (LeetCode 1095)  — Hard
Pattern: Binary search on a hidden array (peak, then two sorted halves)

Problem
-------
A mountain array strictly increases to a single peak and then strictly decreases. You may only
access it through `MountainArray.get(i)` and `MountainArray.length()`, and at most 100 `get`
calls are allowed. Return the MINIMUM index whose value equals `target`, or -1.
Example: arr = [1,2,3,4,5,3,1], target = 3 -> 2 (3 also sits at index 5, but 2 is smaller).

Brute force
-----------
Scan i = 0..n-1 with get(i) and return the first index holding target. O(n) calls — but n can be
10^4 and only 100 calls are allowed, so this is rejected by the call budget, not just by taste.
The waste: every `get` tells us where we are on the mountain (rising or falling side, above or
below target) and a linear scan throws that information away.

From brute force to optimal
---------------------------
The redundancy is probing indices whose answer is already implied by the mountain shape. A
mountain is two sorted arrays glued at the peak, so once the peak is known each side admits
an ordinary binary search. The peak itself is a binary-search target too: the predicate
"get(i) < get(i+1)" is TTT...TFFF...F (true on the ascent, false from the peak on), so the
first F is the peak in log n probes. Then search the ascending half [0, peak] for target; it
holds the smaller index, so if found we stop. Otherwise search the descending half
[peak+1, n-1] with the comparison direction flipped. Three binary searches = ~3 log n <= 45
probes for n = 10^4; a memo dict on top guarantees no index is fetched twice.

Intuition
---------
Reduce an unfamiliar shape to familiar sorted pieces. "Where does the array stop climbing?" is a
monotone yes/no question, so it is answerable by binary search; after that the problem is two
textbook searches. Searching the left half first is what gives the minimum index for free.

Geometric view
--------------
Draw the values as a hill. The predicate arr[i] < arr[i+1] is a row of T's up the left slope and
F's from the summit down the right slope; lo/hi squeeze onto the T|F boundary, the summit. Then
the left slope is a sorted array read left-to-right and the right slope is a sorted array read
right-to-left; binary search each with the matching orientation.

Steps
-----
1. Wrap `get` in a cache so no index costs two calls.
2. Peak: lo = 0, hi = n-1; while lo < hi: mid; if get(mid) < get(mid+1): lo = mid+1 else hi = mid.
3. Binary search [0, peak] ascending for target; if found return it (smallest index).
4. Binary search [peak+1, n-1] descending for target (move left when get(mid) < target).
5. Return the found index or -1.

Complexity: O(log n) time and `get` calls, O(log n) space for the cache — three binary searches.
Pitfalls: searching the descending side first (returns a larger index); comparing with mid-1 in
the peak search (mid+1 is safe because hi = n-1 keeps mid <= n-2); off-by-one making the right
search start at the peak again (it was already covered).
"""
from typing import List


class MountainArray:
    """Mock of LeetCode's interface; counts calls so the 100-call budget can be asserted."""

    def __init__(self, arr: List[int]):
        self._arr = arr
        self.calls = 0

    def get(self, index: int) -> int:
        self.calls += 1
        return self._arr[index]

    def length(self) -> int:
        return len(self._arr)


class Solution:
    def findInMountainArray(self, target: int, mountainArr: "MountainArray") -> int:
        n = mountainArr.length()
        cache = {}

        def get(i: int) -> int:                        # memoised: an index is fetched once
            if i not in cache:
                cache[i] = mountainArr.get(i)
            return cache[i]

        lo, hi = 0, n - 1                              # 1) peak = first i with get(i) > get(i+1)
        while lo < hi:
            mid = (lo + hi) // 2
            if get(mid) < get(mid + 1):
                lo = mid + 1                           # still climbing
            else:
                hi = mid                               # at or past the summit
        peak = lo

        def search(lo: int, hi: int, ascending: bool) -> int:
            while lo <= hi:
                mid = (lo + hi) // 2
                v = get(mid)
                if v == target:
                    return mid
                if (v < target) == ascending:          # target lies to the right of mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            return -1

        idx = search(0, peak, True)                    # 2) left slope first: smaller index
        if idx != -1:
            return idx
        return search(peak + 1, n - 1, False)          # 3) right slope, descending order


def brute_force(target: int, mountainArr: "MountainArray") -> int:
    for i in range(mountainArr.length()):             # one get per index: O(n) calls
        if mountainArr.get(i) == target:
            return i
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 2, 3, 4, 5, 3, 1], 3, 2),
        ([0, 1, 2, 4, 2, 1], 3, -1),
        ([1, 5, 2], 2, 2),
        ([0, 5, 3, 1], 5, 1),                 # target is the peak
        ([1, 2, 3, 4, 3], 1, 0),              # target at the far left
        ([3, 5, 3, 2, 0], 0, 4),              # target at the far right
    ]
    for arr, target, want in cases:
        m = MountainArray(arr)
        assert s.findInMountainArray(target, m) == want, (arr, target)
        assert m.calls <= 100
        assert brute_force(target, MountainArray(arr)) == want
    big = list(range(5000)) + list(range(5000, -1, -1))      # 10001 elements
    m = MountainArray(big)
    assert s.findInMountainArray(4321, m) == 4321 and m.calls <= 100
    print("ok")
