"""
Integer Replacement (LeetCode 397)  — Medium
Pattern: Greedy on the low bits

Problem
-------
Given a positive integer n, in one step you may: if n is even, replace it with n / 2;
if n is odd, replace it with n + 1 or n - 1. Return the minimum steps to reach 1.
Example: 8 -> 3 (8,4,2,1).  7 -> 4 (7,8,4,2,1 or 7,6,3,2,1).

Brute force
-----------
Plain recursion that tries both options at every odd number (the user's original
solution): f(1) = 0, f(even) = 1 + f(n/2), f(odd) = 1 + min(f(n+1), f(n-1)). Every
odd value branches in two, giving up to ~2^(log2 n) = O(n) calls, and the two branches
keep re-solving the same values (f(n+1) and f(n-1) both halve into neighbouring numbers
that overlap one level down). O(n) time worst case, O(log n) stack.

From brute force to optimal
---------------------------
The redundancy is exploring BOTH branches at every odd n. Observation on the binary form:
halving just drops the last bit, so the cost is driven by how many 1-bits we must clear.
For odd n, look at the low two bits. If they are 01, n-1 makes them 00 (two free halvings
follow) while n+1 makes 10. If they are 11, n+1 carries through the run of 1s and turns
it into a single 1 further left, clearing several 1-bits at once, while n-1 clears only
one. So the choice is forced: n & 3 == 1 -> subtract, n & 3 == 3 -> add. The single
exception is n == 3, where 3 -> 2 -> 1 (two steps) beats 3 -> 4 -> 2 -> 1. Each step
either halves n or is immediately followed by a halving: O(log n) time, O(1) space.

Intuition
---------
You want n to become a power of two as fast as possible. Trailing runs of 1s are the
expensive part; adding 1 to ...0111 collapses the run to ...1000, removing many 1s for
the price of one step. A lone trailing 1 (...01) is cheaper to just subtract.

Geometric view
--------------
Read n as a bit string and walk it right to left. A 0 at the end is one shift. A 1 at
the end is either chipped off (01) or turned into a carry that ripples left through a
block of 1s (11), wiping the block out in one move.

Steps
-----
1. While n > 1:
2.   If n is even: n >>= 1.
3.   Elif n == 3 or n & 3 == 1: n -= 1.
4.   Else: n += 1.
5.   steps += 1.

Complexity: O(log n) time, O(1) space — bit length shrinks by one at least every two steps.
Pitfalls: the n == 3 special case; true division n / 2 producing floats in Python;
n + 1 overflow in fixed-width languages when n == 2^31 - 1 (not an issue in Python).
"""


class Solution:
    def integerReplacement(self, n: int) -> int:
        steps = 0
        while n > 1:
            if n & 1 == 0:
                n >>= 1
            elif n == 3 or n & 3 == 1:  # ...01: subtract; 3 is the lone exception
                n -= 1
            else:                       # ...11: add, carry clears the run of 1s
                n += 1
            steps += 1
        return steps


def brute_force(n: int) -> int:
    # Try both moves at every odd number (exponential-shaped recursion tree).
    if n <= 1:
        return 0
    if n % 2 == 0:
        return 1 + brute_force(n // 2)
    return 1 + min(brute_force(n + 1), brute_force(n - 1))


if __name__ == "__main__":
    s = Solution()
    for n, want in ((8, 3), (7, 4), (4, 2), (1, 0), (3, 2), (2147483647, 32)):
        assert s.integerReplacement(n) == want, n
    for n in range(1, 3000):
        assert s.integerReplacement(n) == brute_force(n), n
    print("ok")
