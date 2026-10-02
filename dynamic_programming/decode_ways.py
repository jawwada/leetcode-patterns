"""
Decode Ways (LeetCode 91)  — Medium
Pattern: 1-D DP over prefixes (Fibonacci-style)

Problem
-------
Letters map to numbers 'A' -> "1" ... 'Z' -> "26". Given a digit string s, return how
many ways it can be decoded back into letters. "06" is not a valid code (no leading 0).
Example: "226" -> 3 ("2 2 6" = BBF, "22 6" = VF, "2 26" = BZ).  "06" -> 0.

Brute force
-----------
Recursion on the start index: ways(i) = [s[i] != '0'] * ways(i+1)
+ [10 <= int(s[i:i+2]) <= 26] * ways(i+2), with ways(n) = 1. Each call can branch twice,
so the call tree has up to Fibonacci(n) ~ 1.6^n leaves: exponential time, O(n) stack.
The waste: ways(i+2) is computed once directly and again inside ways(i+1).

From brute force to optimal
---------------------------
Overlapping subproblems: ways(i) depends only on the suffix s[i:], and there are just
n + 1 suffixes, yet the recursion tree evaluates each one Fibonacci-many times.
State: dp[i] = number of decodings of the prefix s[:i] (dp[0] = 1, the empty prefix).
Recurrence: dp[i] = dp[i-1] if s[i-1] != '0'  +  dp[i-2] if "10" <= s[i-2:i] <= "26".
Evaluation order: i = 1..n left to right, so both dependencies are ready (this is the
user's original table). Space reduction: dp[i] reads only the two previous cells, so
keep two rolling variables: O(n) time, O(1) space.

Intuition
---------
The last letter of any decoding uses either the last one digit or the last two digits.
So the count for a prefix is (count for the prefix one shorter, if the last digit is
1..9) plus (count for the prefix two shorter, if the last two digits form 10..26).

Geometric view
--------------
Picture the string as a row of stepping stones. You hop one stone (single digit) or two
stones (two-digit code), and some hops are forbidden by zeros or values > 26. The answer
is the number of hop paths from the left bank to the right bank, accumulated stone by
stone like climbing stairs.

Steps
-----
1. prev2, prev1 = 1, 1 if s[0] != '0' else 0   (dp[0], dp[1]).
2. For i in 2..n: cur = prev1 if s[i-1] != '0' else 0; add prev2 if 10 <= s[i-2:i] <= 26.
3. Shift: prev2, prev1 = prev1, cur.
4. Return prev1.

Complexity: O(n) time, O(1) space — one pass, two rolling counters.
Pitfalls: a '0' can only be the second digit of "10" or "20"; "06" is invalid as a
two-digit code; leading '0' makes the answer 0.
"""


class Solution:
    def numDecodings(self, s: str) -> int:
        prev2, prev1 = 1, 1 if s[0] != "0" else 0  # dp[i-2], dp[i-1]
        for i in range(2, len(s) + 1):
            cur = prev1 if s[i - 1] != "0" else 0
            if 10 <= int(s[i - 2:i]) <= 26:
                cur += prev2
            prev2, prev1 = prev1, cur
        return prev1


def brute_force(s: str) -> int:
    # ways(i) = decodings of s[i:]; tries a 1-digit and a 2-digit code: exponential.
    def ways(i: int) -> int:
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        total = ways(i + 1)
        if i + 1 < len(s) and int(s[i:i + 2]) <= 26:
            total += ways(i + 2)
        return total

    return ways(0)


if __name__ == "__main__":
    s = Solution()
    cases = [("12", 2), ("226", 3), ("06", 0), ("10", 1), ("2101", 1),
             ("11106", 2), ("1111111111", 89), ("100", 0)]
    for text, want in cases:
        assert s.numDecodings(text) == want, text
        assert brute_force(text) == want, text
    print("ok")
