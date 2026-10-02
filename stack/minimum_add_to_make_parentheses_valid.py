"""
Minimum Add to Make Parentheses Valid (LeetCode 921)  — Medium
Pattern: Balance counter (stack collapsed to a count)

Problem
-------
s contains only '(' and ')'. In one move you may insert a single parenthesis anywhere.
Return the minimum number of insertions that make s a valid (balanced) string.
Example: s = "())" -> 1; s = "(((" -> 3; s = "()))((" -> 4.

Brute force
-----------
Repeatedly delete every adjacent "()" pair until none is left; what remains has the shape
")))...(((" and every leftover character needs one partner, so the answer is its length.
O(n^2) time (up to n/2 rounds of O(n) string rebuilding), O(n) space. The waste: every
round re-scans and copies the whole string to remove pairs that a single left-to-right
pass could have matched immediately.

From brute force to optimal
---------------------------
The deletions are just stack matching: a ')' cancels the most recent unmatched '('. A stack
of '(' characters would do it in one pass, but all entries are identical, so the stack
collapses to its height: open = number of unmatched '(' so far. On ')' with open > 0 we
match it; with open == 0 that ')' can never be matched by anything to its right, so it
costs one insertion right away. At the end each of the open '(' needs one ')'. Answer =
unmatched ')' + leftover open. One pass, two integers.

Intuition
---------
Read left to right keeping a balance. The balance must never go below zero; every time it
would, a '(' has to be inserted before that ')' (count it and stay at zero). Whatever
balance is left at the end is the number of ')' to append.

Geometric view
--------------
Draw the balance as a mountain path: '(' steps up, ')' steps down. Valid strings stay at
or above sea level and end at sea level. Each dip below sea level is clipped (one insert
each), and the final altitude is how far we must descend at the end.

Steps
-----
1. open = 0, adds = 0.
2. For c in s: if c == '(': open += 1; elif open > 0: open -= 1; else: adds += 1.
3. Return adds + open.

Complexity: O(n) time, O(1) space — single pass, the stack is reduced to a counter.
Pitfalls: Returning |#'(' - #')'| (fails on ")(" which needs 2); letting the balance go
negative and "repaying" it with a later '(' (a later '(' cannot fix an earlier ')').
"""


class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        open_ = 0          # unmatched '(' so far (height of the would-be stack)
        adds = 0           # ')' that had nothing to match: each needs an inserted '('
        for c in s:
            if c == "(":
                open_ += 1
            elif open_ > 0:
                open_ -= 1
            else:
                adds += 1
        return adds + open_   # leftover '(' each need a closing ')'


def brute_force(s: str) -> int:
    while "()" in s:
        s = s.replace("()", "")   # one O(n) rebuild per round of cancellations
    return len(s)


if __name__ == "__main__":
    sol = Solution()
    cases = [("())", 1), ("(((", 3), ("()))((", 4), ("", 0), (")(", 2), ("(()())", 0)]
    for s, want in cases:
        assert sol.minAddToMakeValid(s) == want, s
        assert brute_force(s) == want, s
    print("ok")
