"""
Expression Add Operators (LeetCode 282)  — Hard
Pattern: Backtracking with running value + last operand (incremental evaluation)

Problem
-------
Given a digit string num and an integer target, insert the binary operators '+', '-' or '*'
between some of the digits (or none, to form multi-digit numbers) so that the expression equals
target. Return all such expressions in any order. Operands may not have leading zeros.
Example: num = "123", target = 6 -> ["1*2*3", "1+2+3"].  num = "105", target = 5 -> ["1*0+5", "10-5"].

Brute force
-----------
Between each pair of adjacent digits choose one of four separators: nothing, '+', '-', '*'. Build
all 4^(n-1) strings, reject those with a leading-zero operand, and evaluate each one from scratch
with a precedence-aware evaluator (or eval). O(4^n * n) time, O(n) space. Exponential by nature,
but the specific waste is the evaluation: two strings that share the prefix "1+2*3" re-parse and
re-evaluate that prefix independently, and every leaf pays a full O(n) parse.

From brute force to optimal
---------------------------
The redundancy is re-evaluating shared prefixes at every leaf. Observation: the value of a
prefix can be carried down the recursion, except that '*' binds tighter than the '+'/'-' already
applied, so appending "*x" must undo the last additive term and re-add it multiplied. Carry two
numbers: value (the prefix evaluated so far) and last (the most recent multiplicative term, with
its sign). Then '+x' gives (value + x, x), '-x' gives (value - x, -x) and '*x' gives
(value - last + last * x, last * x). Each extension is O(1), so the search costs O(4^n) total with
no per-leaf parse, and the leading-zero rule prunes whole subtrees as soon as an operand starts
with '0' and is longer than one digit.

Intuition
---------
Treat the expression as a sum of terms, where a term is a product of operands. '+' and '-' start a
new term; '*' extends the current term. If you know the total so far and the current term, you
can absorb a new operand in O(1) for any operator. The DFS walks digit positions, chooses where
each operand ends, and branches three ways on the operator - except for the very first operand,
which takes no operator.

Geometric view
--------------
A tree over positions 0..n. From position i a branch picks an end j (operand num[i:j]) and an
operator; depth equals the number of operands. Each node stores (expr, value, last); the '*' branch
"reaches back" one term: it replaces the last leaf of the running sum with last * x. Leaves at
position n are compared with target; the leading-zero rule chops every subtree where an operand
"0d..." would start.

Steps
-----
1. dfs(i, expr, value, last): if i == n, record expr when value == target.
2. For j in i+1..n: operand s = num[i:j]; stop extending if s has a leading zero.
3. If i == 0: dfs(j, s, cur, cur) with no operator.
4. Else branch: '+' -> (value + cur, cur); '-' -> (value - cur, -cur);
   '*' -> (value - last + last * cur, last * cur).
5. Start dfs(0, "", 0, 0) and return the collected expressions.

Complexity: O(4^n) time, O(n) space — each of the n-1 gaps picks one of 4 options; each node
does O(1) arithmetic (string building adds O(n) per leaf, only for the output).
Pitfalls: handling '*' by multiplying value directly (wrong precedence); not keeping the sign in
last after '-' (2-3*4 must become 2-12); allowing "05" as an operand but forgetting that "0"
alone is legal; forgetting the first operand has no operator in front.
"""
from itertools import product
from typing import List


class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        n, out = len(num), []

        def dfs(i: int, expr: str, value: int, last: int) -> None:
            if i == n:
                if value == target:
                    out.append(expr)
                return
            for j in range(i + 1, n + 1):
                s = num[i:j]
                if len(s) > 1 and s[0] == "0":
                    break                                       # no leading zeros: prune
                cur = int(s)
                if i == 0:
                    dfs(j, s, cur, cur)                         # first operand, no operator
                else:
                    dfs(j, expr + "+" + s, value + cur, cur)
                    dfs(j, expr + "-" + s, value - cur, -cur)
                    dfs(j, expr + "*" + s, value - last + last * cur, last * cur)

        dfs(0, "", 0, 0)
        return out


def brute_force(num: str, target: int) -> List[str]:
    # Every choice of separator in the n-1 gaps, then evaluate each string from scratch.
    out = []
    for seps in product(("", "+", "-", "*"), repeat=len(num) - 1):
        expr = num[0] + "".join(sep + d for sep, d in zip(seps, num[1:]))
        operands = expr.replace("+", " ").replace("-", " ").replace("*", " ").split()
        if any(len(x) > 1 and x[0] == "0" for x in operands):
            continue
        if eval(expr) == target:                                 # full re-parse at every leaf
            out.append(expr)
    return out


if __name__ == "__main__":
    s = Solution()
    cases = (("123", 6, ["1*2*3", "1+2+3"]), ("232", 8, ["2*3+2", "2+3*2"]),
             ("105", 5, ["1*0+5", "10-5"]), ("00", 0, ["0*0", "0+0", "0-0"]),
             ("3456237490", 9191, []), ("1", 1, ["1"]), ("1", 2, []), ("2147483647", 2147483647, ["2147483647"]))
    for num, target, want in cases:
        assert sorted(s.addOperators(num, target)) == sorted(want), (num, target)
        if len(num) <= 7:
            assert sorted(brute_force(num, target)) == sorted(want), (num, target)
    assert sorted(s.addOperators("123456", 100)) == sorted(brute_force("123456", 100))
    assert sorted(s.addOperators("10203", 15)) == sorted(brute_force("10203", 15))
    print("ok")
