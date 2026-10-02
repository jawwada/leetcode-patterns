"""
Generate Parentheses (LeetCode 22)  — Medium
Pattern: Backtracking with validity-preserving constraints (open/close counts)

Problem
-------
Given n pairs of parentheses, return all strings of n "(" and n ")" that are well-formed.
Example: n=3 -> ["((()))","(()())","(())()","()(())","()()()"].  n=1 -> ["()"].

Brute force
-----------
Generate every string of length 2n over {"(", ")"} (2^(2n) of them) and keep those that pass a
balance check (running count never negative, ends at zero).
O(2n * 4^n) time, O(n) space beyond the output. The waste: strings starting with ")" or that
have more ")" than "(" at any prefix are still generated to full length and then rejected; the
valid strings are a vanishing fraction (the Catalan number C_n versus 4^n).

From brute force to optimal
---------------------------
The redundancy is extending prefixes that can no longer become valid. Observation: a prefix can
be completed to a well-formed string iff open <= n and close <= open, where open/close are the
counts placed so far. So at each step allow "(" only if open < n and ")" only if close < open.
Every branch the DFS takes is then a prefix of some valid answer, so the tree has exactly C_n
leaves and zero dead ends. The shared path list with append/pop keeps the per-node cost O(1).

Intuition
---------
You may open a bracket while you still have unopened ones, and you may close a bracket only if
one is currently open. Two counters make the whole validity check local.

Geometric view
--------------
A binary tree where the left branch adds "(" and the right adds ")". Draw the balance (open -
close) as height above a floor: branches that would dip below the floor (close > open) or exceed
the ceiling (open > n) are cut, so every drawn path is a mountain range that starts and ends at
the floor without going underground. Those are exactly the Dyck paths.

Steps
-----
1. result = [], path = []. dfs(open, close).
2. If len(path) == 2n record "".join(path) and return.
3. If open < n: append "(", dfs(open + 1, close), pop.
4. If close < open: append ")", dfs(open, close + 1), pop.
5. Call dfs(0, 0), return result.

Complexity: O(4^n / sqrt(n)) time (number of outputs times O(n) to join), O(n) recursion space
beyond the output.
Pitfalls: Allowing ")" when close < n instead of close < open (produces invalid strings);
forgetting the open < n cap (infinite recursion); checking validity only at the leaf.
"""
from itertools import product
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result: List[str] = []
        path: List[str] = []

        def dfs(opened: int, closed: int) -> None:
            if len(path) == 2 * n:
                result.append("".join(path))
                return
            if opened < n:                      # still have "(" left to place
                path.append("(")
                dfs(opened + 1, closed)
                path.pop()
            if closed < opened:                 # may only close something that is open
                path.append(")")
                dfs(opened, closed + 1)
                path.pop()

        dfs(0, 0)
        return result


def brute_force(n: int) -> List[str]:
    out = []
    for bits in product("()", repeat=2 * n):          # all 4^n strings, checked when complete
        balance = 0
        for ch in bits:
            balance += 1 if ch == "(" else -1
            if balance < 0:
                break
        if balance == 0:
            out.append("".join(bits))
    return out


if __name__ == "__main__":
    s = Solution()
    assert sorted(s.generateParenthesis(3)) == sorted(["((()))", "(()())", "(())()", "()(())", "()()()"])
    assert s.generateParenthesis(1) == ["()"]
    assert s.generateParenthesis(0) == [""]                     # zero pairs: the empty string
    assert len(s.generateParenthesis(5)) == 42                  # Catalan(5)
    for n in range(0, 6):
        assert sorted(s.generateParenthesis(n)) == sorted(brute_force(n)), n
    print("ok")
