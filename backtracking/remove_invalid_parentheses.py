"""
Remove Invalid Parentheses (LeetCode 301)  — Hard
Pattern: Backtracking with counted removals and balance pruning

Problem
-------
Remove the MINIMUM number of parentheses so the string becomes valid; return every distinct
result. Letters are kept as-is.
Example: "()())()" -> ["(())()", "()()()"]; "(a)())()" -> ["(a())()", "(a)()()"]; ")(" -> [""].

Brute force
-----------
Try every subset of characters to delete (2^n masks), keep the subsets that leave a valid
string, and return the valid strings of maximum length (deduplicated). O(2^n * n) time,
exponential, O(2^n) space for the result pool. The wasted work: most masks are doomed early
(they keep a ')' with nothing open, or they delete far more than necessary) yet the whole
string is still assembled and validated for each of them.

From brute force to optimal
---------------------------
Two independent pieces of wasted work. First, how MANY '(' and ')' to delete is known before any
search: one left-to-right pass counting unmatched ')' (right) and leftover '(' (left) gives the
exact minimum removals, so the search only needs to decide WHICH ones. Second, a partial string
whose running balance goes negative, or that has already deleted more than `left`/`right`
allows, can never be completed, so prune it immediately. The DFS therefore carries
(index, open balance, left budget, right budget, path) and branches at most two ways per bracket
(delete it if the budget allows, or keep it if balance stays >= 0). Duplicates arising from
deleting different copies of the same character are collapsed by a set. The search space is
bounded by C(n, left) * C(n, right) states instead of 2^n, and every leaf it reaches is an
answer.

Intuition
---------
Count first, then search. The counting pass is the same balance check you would use to validate
a string; its two leftover counters are exactly the deletions you are forced to make. With the
budgets known, DFS is a walk along the string where each bracket is a fork: spend budget on it
or keep it. Keeping a ')' is only allowed when something is open, which kills the vast majority
of hopeless branches at the first wrong step.

Geometric view
--------------
   s = ( ) ( ) ) ( )       pass 1: right = 1 unmatched ')', left = 0
   DFS tree: at each ')' with right > 0 branch into [delete] and [keep if open > 0]
       keep ( -> keep ) -> keep ( -> keep ) -> ')' open=0 -> must delete -> ( ) => "()()()"
                         -> delete ) -> keep ) -> ( ) => "(())()"
The recursion tree is a binary tree of width bounded by the removal budgets; the balance
counter is a fence that stops any branch from dipping below zero.

Steps
-----
1. Scan s: '(' -> left += 1; ')' -> if left: left -= 1 else right += 1.
2. dfs(i, open, left, right, path): if i == n and open == 0 and left == right == 0: add path.
3. If s[i] == '(' and left > 0: dfs skipping it with left-1. If s[i] == ')' and right > 0:
   dfs skipping it with right-1.
4. Keep s[i]: '(' -> open+1; ')' only if open > 0 -> open-1; letter -> unchanged.
5. Return the result set as a list.

Complexity: O(2^n) worst-case time (exponential, but bounded by C(n, left) * C(n, right) leaves
with pruning), O(n) recursion depth plus the output.
Pitfalls: not requiring open == 0 at the end (a leftover '(' slips through when left was
mis-counted); producing duplicates when identical adjacent brackets are deleted in different
orders (use a set or skip repeated characters); forgetting that letters must be kept.
"""
from typing import List


class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        left = right = 0                                   # minimum "(" and ")" removals
        for c in s:
            if c == "(":
                left += 1
            elif c == ")":
                if left:
                    left -= 1
                else:
                    right += 1

        res = set()

        def dfs(i: int, open_: int, left: int, right: int, path: str) -> None:
            if i == len(s):
                if open_ == 0 and left == 0 and right == 0:
                    res.add(path)
                return
            c = s[i]
            if c == "(" and left:                          # option: delete this "("
                dfs(i + 1, open_, left - 1, right, path)
            if c == ")" and right:                         # option: delete this ")"
                dfs(i + 1, open_, left, right - 1, path)
            if c == "(":
                dfs(i + 1, open_ + 1, left, right, path + c)
            elif c == ")":
                if open_:                                  # prune: balance never goes negative
                    dfs(i + 1, open_ - 1, left, right, path + c)
            else:
                dfs(i + 1, open_, left, right, path + c)

        dfs(0, 0, left, right, "")
        return list(res)


def brute_force(s: str) -> List[str]:
    def valid(t: str) -> bool:
        bal = 0
        for c in t:
            bal += (c == "(") - (c == ")")
            if bal < 0:
                return False
        return bal == 0

    n = len(s)
    kept = set()
    for mask in range(1 << n):                             # exponential: every delete-subset
        t = "".join(s[i] for i in range(n) if mask >> i & 1)
        if valid(t):
            kept.add(t)
    longest = max(map(len, kept))
    return [t for t in kept if len(t) == longest]


if __name__ == "__main__":
    s = Solution()
    assert sorted(s.removeInvalidParentheses("()())()")) == ["(())()", "()()()"]
    assert sorted(s.removeInvalidParentheses("(a)())()")) == ["(a())()", "(a)()()"]
    assert s.removeInvalidParentheses(")(") == [""]
    assert s.removeInvalidParentheses("n") == ["n"]
    assert sorted(s.removeInvalidParentheses("(((")) == [""]
    import random
    random.seed(6)
    for _ in range(150):
        w = "".join(random.choice("(()))a") for _ in range(random.randint(1, 11)))
        assert sorted(s.removeInvalidParentheses(w)) == sorted(brute_force(w)), w
    print("ok")
