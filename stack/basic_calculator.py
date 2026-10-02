"""
Basic Calculator (LeetCode 224)  — Hard
Pattern: Sign stack for parentheses

Problem
-------
Evaluate a string containing non-negative integers, '+', '-', '(', ')' and spaces. Unary minus
may appear ("-(2-3)"). No eval().
Example: "(1+(4+5+2)-3)+(6+8)" -> 23; " 2-1 + 2 " -> 3; "-(2-3)" -> 1.

Brute force
-----------
Recursive descent on substrings: scan left to right summing signed numbers; on '(' walk forward
counting depth to find the matching ')', recurse on the slice between them, and add the result
with the current sign. Finding the match re-scans the whole inner text, and the recursive call
scans it again, so deeply nested input costs O(n * depth) = O(n^2) time and O(n) space for
slices plus recursion. The wasted work is the look-ahead scan: the matching ')' is located by
reading characters that will all be read again.

From brute force to optimal
---------------------------
The redundancy is looking ahead for the matching parenthesis. Observation: with only + and -,
parentheses change nothing except the SIGN that applies to the terms inside: "a - (b - c)" is
"a - b + c". So each term's effective sign is (sign of its own operator) x (effective sign of
the enclosing context). Keep a stack of context signs: on '(' push the sign that precedes it
(that is the context for everything inside), on ')' pop. Every number is then added directly to
one running total as soon as it is complete; no recursion, no slicing, no look-ahead. One
left-to-right pass, O(n) time, O(depth) stack.

Intuition
---------
Distribute the minus. Instead of computing a parenthesised value and then negating it, negate
each term inside as you meet it. The stack top always answers "am I inside an odd number of
negated groups?" and a fresh operator inside a group just multiplies with that.

Geometric view
--------------
   1 - ( 2 + 3 )            signs stack:  [+1]   then at "(" push -1 -> [+1, -1]
       ^ context = -1       term 2: sign = -1 * (+) = -1 ; term 3: sign = -1 * (+) = -1
Picture each parenthesis pair as a lens: a '-' lens flips the sign of every term seen through
it, two nested '-' lenses cancel. The stack is the pile of lenses the cursor is currently
looking through.

Steps
-----
1. res = 0, num = 0, sign = 1, signs = [1]. Iterate over s + "+" (sentinel flushes the last
   number).
2. Digit: num = num*10 + digit.
3. '+' / '-': res += sign * num; num = 0; sign = signs[-1] * (+1 or -1).
4. '(': signs.append(sign)  (the sign in front of the group becomes the inner context).
5. ')': signs.pop().
6. Return res.

Complexity: O(n) time, O(d) space — one pass; the stack holds one sign per open parenthesis.
Pitfalls: forgetting to flush the final number (use a sentinel operator or add after the loop);
on '(' push the CURRENT sign, not +1; resetting sign to +1 after ')' (it must come from the
next operator x signs[-1]); multi-digit numbers.
"""


class Solution:
    def calculate(self, s: str) -> int:
        res, num, sign = 0, 0, 1
        signs = [1]                                  # effective sign of the enclosing context
        for c in s + "+":                            # sentinel operator flushes the last number
            if c.isdigit():
                num = num * 10 + int(c)
            elif c in "+-":
                res += sign * num
                num = 0
                sign = signs[-1] * (1 if c == "+" else -1)
            elif c == "(":
                signs.append(sign)                   # everything inside inherits this sign
            elif c == ")":
                signs.pop()
        return res


def brute_force(s: str) -> int:
    def evaluate(expr: str) -> int:
        total, sign, i = 0, 1, 0
        while i < len(expr):
            c = expr[i]
            if c.isdigit():
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                total, i = total + sign * int(expr[i:j]), j
                continue
            if c == "(":                             # look ahead for the matching ")"
                depth, j = 0, i
                while True:
                    depth += (expr[j] == "(") - (expr[j] == ")")
                    if depth == 0:
                        break
                    j += 1
                total, i = total + sign * evaluate(expr[i + 1:j]), j   # re-reads the inside
            elif c in "+-":
                sign = 1 if c == "+" else -1
            i += 1
        return total
    return evaluate(s)


if __name__ == "__main__":
    s = Solution()
    cases = {"1 + 1": 2, " 2-1 + 2 ": 3, "(1+(4+5+2)-3)+(6+8)": 23, "-(2-3)": 1,
             "2147483647": 2147483647, "- (3 + (4 + 5))": -12, "1-(5)": -4,
             "-(-(-(7)))": -7, "(7)-(0)+(4)": 11, "10 - (2 - (3 - 4)) + 5": 12}
    for expr, want in cases.items():
        assert s.calculate(expr) == want, expr
        assert brute_force(expr) == want, expr
    print("ok")
