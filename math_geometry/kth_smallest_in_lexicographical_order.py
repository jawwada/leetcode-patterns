"""
K-th Smallest in Lexicographical Order (LeetCode 440)  — Hard
Pattern: Denary (10-ary) trie traversal with subtree-size skipping

Problem
-------
Return the k-th smallest integer in [1, n] when the integers are ordered lexicographically as
strings (n, k <= 10^9).
Example: n = 13, k = 2 -> 10  (order: 1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9).
Example: n = 1, k = 1 -> 1.

Brute force
-----------
Create the strings "1".."n", sort them, return the k-th. O(n log n) time, O(n) space — n = 10^9
strings is impossible. The waste: sorting enumerates every number although the lexicographic
order is a pre-order walk of a fixed tree, so the position of any node can be computed from the
tree's shape without listing its contents.

From brute force to optimal
---------------------------
The redundancy is visiting numbers one at a time. Lexicographic order is a PRE-ORDER traversal
of the denary trie: node v has children 10v..10v+9 and the roots are 1..9. In pre-order, after
visiting v you visit all descendants of v before v+1, so the k-th element can be reached by
jumping: standing at cur with k steps still to take, compute steps = size of cur's subtree
within [1, n]. If steps <= k, the answer is not under cur: skip the whole subtree (k -= steps,
cur += 1). Otherwise it is: descend (k -= 1, cur *= 10). The subtree size is the count of
numbers in [cur, cur+1), [10cur, 10cur+10), [100cur, ...) clipped to n+1, which takes
O(log n) per level, so the whole walk is O(log^2 n).

Intuition
---------
Treat the numbers as a trie of digit strings; pre-order = lexicographic. Each level you ask
"is the target inside this subtree?" by comparing k with the subtree size — the same trick as
finding the k-th element of a sorted list via block sizes — and either skip the block or dive
into it.

Geometric view
--------------
Draw the roots 1..9 across the top; under each hang its ten children 10..19, 20..29, ..., then
grandchildren, with the tree ragged at the right where values exceed n. The answer is the k-th
node met walking the tree depth-first, left to right. The algorithm hops sibling to sibling when
the subtree is small enough to skip, and steps down one level when the target is inside.

Steps
-----
1. cur = 1; k -= 1 (cur itself is the first element).
2. While k > 0: count numbers in cur's subtree: a, b = cur, cur + 1; steps = 0;
   while a <= n: steps += min(n + 1, b) - a; a *= 10; b *= 10.
3. If steps <= k: k -= steps; cur += 1 (skip sibling subtree).
4. Else: k -= 1; cur *= 10 (go to the first child).
5. Return cur.

Complexity: O(log^2 n) time, O(1) space — each of <= 10 levels does an O(log n) subtree count.
Pitfalls: clipping with min(n, b) instead of min(n + 1, b) (drops the number n itself);
decrementing k before the loop and then again when descending is correct but easy to double
count; stepping cur += 1 when cur ends in 9 moves to the next sibling of the PARENT only if the
subtree count was taken over the full range — the loop handles it because 19 + 1 = 20.
"""


class Solution:
    def findKthNumber(self, n: int, k: int) -> int:
        def subtree(a: int) -> int:                  # how many numbers in [1, n] start with a
            b, total = a + 1, 0
            while a <= n:                            # one level of the trie at a time
                total += min(n + 1, b) - a           # numbers in [a, b) that are <= n
                a, b = a * 10, b * 10
            return total

        cur, k = 1, k - 1                            # cur is the 1st element
        while k:
            steps = subtree(cur)
            if steps <= k:                           # target is past this whole subtree
                k -= steps
                cur += 1                             # jump to the next sibling
            else:                                    # target is inside: visit the first child
                k -= 1
                cur *= 10
        return cur


def brute_force(n: int, k: int) -> int:
    return int(sorted(str(i) for i in range(1, n + 1))[k - 1])   # lists every number


if __name__ == "__main__":
    s = Solution()
    assert s.findKthNumber(13, 2) == 10
    assert s.findKthNumber(1, 1) == 1
    assert s.findKthNumber(13, 13) == 9                    # last element
    assert s.findKthNumber(100, 3) == 100                  # deep node clipped at n
    assert s.findKthNumber(10**9, 10**9) == 999999999
    for n in (9, 10, 13, 27, 100, 101, 999, 1000, 1234):
        for k in range(1, n + 1):
            assert s.findKthNumber(n, k) == brute_force(n, k), (n, k)
    print("ok")
