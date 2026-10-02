"""
Median of Two Sorted Arrays (LeetCode 4)  — Hard
Pattern: Binary search on a partition

Problem
-------
Given two sorted arrays nums1 (size m) and nums2 (size n), return the median of the merged array
in O(log(m+n)).
Example: nums1 = [1,3], nums2 = [2] -> 2.0; nums1 = [1,2], nums2 = [3,4] -> 2.5.

Brute force
-----------
Merge the two arrays with two pointers (or just sort nums1 + nums2) and read the middle
element(s). O(m+n) time, O(m+n) space. The wasted work: we materialise the whole merged order
when all we need is to know WHICH elements form the lower half — the order inside each half is
irrelevant.

From brute force to optimal
---------------------------
The redundancy is building the full merge. Observation: the median splits the combined data into
a left half of exactly (m+n+1)//2 elements and a right half, and the left half consists of a
prefix of nums1 (i elements) plus a prefix of nums2 (j = half - i elements). The split is valid
iff every left element <= every right element, which only needs the four boundary values:
A[i-1] <= B[j] and B[j-1] <= A[i]. If A[i-1] > B[j], i is too big; if B[j-1] > A[i], i is too
small. That is monotone in i, so binary search i over the SHORTER array in O(log min(m,n)) and
read the median off the boundary values.

Intuition
---------
Choose how many items of the shorter array go to the left half; that forces how many of the
longer array go left. A cut is correct when the largest of the left side is <= the smallest of
the right side across both arrays. Binary search the cut position; the median is max(lefts) or
the average of max(lefts) and min(rights).

Geometric view
--------------
Two sorted rows with a vertical cut through each:

    A:  a0 a1 | a2 a3
    B:  b0 b1 b2 | b3 b4

Everything left of the cuts is the lower half. Sliding A's cut right forces B's cut left so the
left count stays fixed. The cuts are right when the two left-edge values are both <= the two
right-edge values.

Steps
-----
1. Ensure A is the shorter array; m = len(A), n = len(B), half = (m+n+1)//2.
2. Binary search i in [0, m]: j = half - i.
3. Aleft = A[i-1] or -inf, Aright = A[i] or +inf; same for B with j.
4. If Aleft > Bright: hi = i - 1 (too many from A). Elif Bleft > Aright: lo = i + 1.
5. Else the cut is correct: if (m+n) odd return max(Aleft, Bleft);
   else return (max(Aleft, Bleft) + min(Aright, Bright)) / 2.

Complexity: O(log min(m, n)) time, O(1) space — binary search over cut positions of the shorter array.
Pitfalls: not swapping so that the shorter array is searched (j can go negative); forgetting
+-inf sentinels at the edges; off-by-one in half for odd totals; returning int instead of float.
"""
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)
        m, n = len(A), len(B)
        half = (m + n + 1) // 2               # size of the left half
        lo, hi = 0, m                         # i = how many of A go left
        INF = float("inf")
        while lo <= hi:
            i = (lo + hi) // 2
            j = half - i
            a_left = A[i - 1] if i > 0 else -INF
            a_right = A[i] if i < m else INF
            b_left = B[j - 1] if j > 0 else -INF
            b_right = B[j] if j < n else INF
            if a_left > b_right:
                hi = i - 1                    # took too many from A
            elif b_left > a_right:
                lo = i + 1                    # took too few from A
            else:                             # valid cut
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
        raise ValueError("inputs must be sorted")


def brute_force(nums1: List[int], nums2: List[int]) -> float:
    merged = sorted(nums1 + nums2)
    k = len(merged)
    if k % 2:
        return float(merged[k // 2])
    return (merged[k // 2 - 1] + merged[k // 2]) / 2


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 3], [2], 2.0),
        ([1, 2], [3, 4], 2.5),
        ([], [1], 1.0),
        ([2], [], 2.0),
        ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], 6.0),
        ([100], [1, 2, 3], 2.5),
    ]
    for a, b, want in cases:
        assert s.findMedianSortedArrays(a, b) == want
        assert brute_force(a, b) == want
    print("ok")
