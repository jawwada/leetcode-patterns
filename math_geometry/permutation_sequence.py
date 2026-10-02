"""
Permutation Sequence (LeetCode 60)  — Hard
Pattern: Factorial number system (direct ranking into blocks)

Problem
-------
The permutations of "1".."n" listed in lexicographic order are numbered 1..n!. Return the k-th
one as a string (1 <= n <= 9).
Example: n=3, k=3 -> "213"  (order: 123, 132, 213, 231, 312, 321); n=4, k=9 -> "2314".

Brute force
-----------
Generate the permutations in lexicographic order (itertools.permutations, or next-permutation
k-1 times) and stop at the k-th: O(k * n) time, up to O(n! * n), O(n) space. The wasted work is
building every permutation before the k-th one in full, although whole blocks of them share a
prefix we could skip in one step.

From brute force to optimal
---------------------------
The redundancy is walking through permutations one at a time. The observation: in lexicographic
order, all permutations starting with the smallest unused digit come first, then those starting
with the second smallest, and so on; each such block has exactly (n-1)! members. So with a
0-indexed rank r = k-1, the first digit is the unused digit at index r // (n-1)!, and the
remaining problem is the same question on n-1 digits with rank r % (n-1)!. Repeating this is
writing r in the factorial number system: digits d_i with weights i!, each digit selecting one
element from the shrinking list of unused digits. That is n steps of a division and a list pop:
O(n^2) with a list, which for n <= 9 is instant, versus O(n! * n) for the walk.

Intuition
---------
Lexicographic order is a tree: the first digit splits the n! leaves into n equal blocks of
(n-1)!, the second digit splits each block into n-1 blocks of (n-2)!, and so on. Finding the
k-th leaf is a descent in this tree, choosing the child by integer division at every level,
exactly like reading off digits of a number in a mixed-radix system.

Geometric view
--------------
A ruler of length n! with big ticks every (n-1)! (first digit), smaller ticks every (n-2)!
within each big interval (second digit), and so on. The position k-1 on the ruler is read off
tick by tick; the i-th reading says which of the remaining digits to take next, and taking it
removes it from the pool.

Steps
-----
1. digits = ['1', ..., 'n']; fact[i] = i!; r = k - 1.
2. For i = n-1 down to 0: idx, r = divmod(r, fact[i]); append digits.pop(idx).
3. Join the appended digits.

Complexity: O(n^2) time, O(n) space — n iterations each popping from a list of length <= n.
Pitfalls: forgetting k is 1-indexed (use k-1); indexing the ORIGINAL digit list instead of the
          shrinking pool; off-by-one in which factorial to divide by at each step.
"""
import random
from itertools import permutations


class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        digits = [str(d) for d in range(1, n + 1)]      # unused digits, ascending
        fact = [1] * n
        for i in range(1, n):
            fact[i] = fact[i - 1] * i
        r = k - 1                                       # 0-indexed rank
        out = []
        for i in range(n - 1, -1, -1):                  # i = positions left after this one
            idx, r = divmod(r, fact[i])                 # each leading digit owns a block of i!
            out.append(digits.pop(idx))
        return "".join(out)


def brute_force(n: int, k: int) -> str:
    # Walk all permutations in lexicographic order and stop at the k-th: O(n! * n).
    for i, perm in enumerate(permutations(range(1, n + 1)), 1):
        if i == k:
            return "".join(map(str, perm))
    return ""


if __name__ == "__main__":
    s = Solution()
    assert s.getPermutation(3, 3) == "213"
    assert s.getPermutation(4, 9) == "2314"
    assert s.getPermutation(3, 1) == "123"
    assert s.getPermutation(1, 1) == "1"                            # smallest input
    assert s.getPermutation(9, 362880) == "987654321"               # last permutation

    for n in range(1, 6):
        fact = 1
        for i in range(2, n + 1):
            fact *= i
        for k in range(1, fact + 1):
            assert s.getPermutation(n, k) == brute_force(n, k)
    random.seed(10)
    for _ in range(20):
        k = random.randint(1, 5040)
        assert s.getPermutation(7, k) == brute_force(7, k)
    print("ok")
