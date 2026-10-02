"""
Number of Digit One (LeetCode 233)  — Hard
Pattern: Digit counting by position (high / current / low split)

Problem
-------
Count the total number of digit 1 appearing in all non-negative integers <= n (n <= 2*10^9).
Example: n = 13 -> 6  (1, 10, 11, 12, 13 contain 1+1+2+1+1 = 6 ones).  n = 0 -> 0.

Brute force
-----------
For every i in 0..n convert to a string and count its '1' characters. O(n log n) time, O(1)
space — 2*10^9 numbers is far too slow. The waste: the ones digit cycles 0..9 every 10 numbers,
the tens digit every 100, and so on; the brute force rediscovers these perfectly periodic
patterns one number at a time.

From brute force to optimal
---------------------------
The redundancy is counting across numbers when the structure is across digit POSITIONS. Fix a
position with weight p (1, 10, 100, ...). Split n = high * 10p + cur * p + low, where cur is
the digit of n at that position. Each full cycle of the higher digits (0..high-1) makes the
position spend exactly p consecutive numbers showing a 1 — contributing high * p. The partial
cycle at high itself depends on cur: if cur > 1 the position has already shown 1 for a full
block of p numbers; if cur == 1 it has shown 1 for low + 1 numbers (from ...1000 up to n); if
cur == 0 none. Summing over the ~10 positions answers in O(log n) instead of O(n).

Intuition
---------
Count ones column by column, not number by number. In any column the digit 1 appears in a
regular rhythm (p numbers on, 9p off) and n just truncates the rhythm; the truncation is fully
described by the digit above the cut (cur) and the remainder below it (low).

Geometric view
--------------
Write 0..n as rows of digits and look at one column. Reading downwards the column is
0...0 1...1 2...2 ... 9...9 repeated, each run p rows long. high complete repetitions give
high * p ones; then the last partial repetition is cut at row n — before the 1-run (cur = 0),
inside it (cur = 1, low + 1 rows), or after it (cur > 1, all p rows).

Steps
-----
1. total = 0; p = 1.
2. While p <= n: high = n // (10 p); cur = (n // p) % 10; low = n % p.
3. total += high * p.
4. If cur > 1: total += p; elif cur == 1: total += low + 1.
5. p *= 10. Return total.

Complexity: O(log10 n) time, O(1) space — one constant-time step per decimal position.
Pitfalls: forgetting the +1 in low + 1 (the number n itself counts when cur == 1); using
n // p % 10 before casting in languages with overflow; stopping the loop at p < n instead of
p <= n (misses the leading digit when n is a power of ten).
"""


class Solution:
    def countDigitOne(self, n: int) -> int:
        total, p = 0, 1                              # p = weight of the current position
        while p <= n:
            high, cur, low = n // (p * 10), (n // p) % 10, n % p
            total += high * p                        # full cycles above this position
            if cur > 1:
                total += p                           # partial cycle already passed its 1-run
            elif cur == 1:
                total += low + 1                     # inside the 1-run: 0..low below it
            p *= 10
        return total


def brute_force(n: int) -> int:
    return sum(str(i).count("1") for i in range(n + 1))   # visits every number


if __name__ == "__main__":
    s = Solution()
    assert s.countDigitOne(13) == 6
    assert s.countDigitOne(0) == 0
    assert s.countDigitOne(1) == 1
    assert s.countDigitOne(100) == 21
    assert s.countDigitOne(1000) == 301                    # power of ten (leading digit)
    assert s.countDigitOne(2 * 10**9) == 2800000000        # upper limit, cur = 2 at the top
    for n in list(range(0, 300)) + [999, 1111, 1234, 5555, 9999, 10000, 12345]:
        assert s.countDigitOne(n) == brute_force(n), n
    print("ok")
