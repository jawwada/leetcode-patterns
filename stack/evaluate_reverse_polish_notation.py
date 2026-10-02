"""
Evaluate Reverse Polish Notation (LeetCode 150)  — Medium
Pattern: Stack evaluation

Problem
-------
Evaluate an arithmetic expression given in postfix (RPN) as a list of tokens: integers and
the operators + - * /. Division truncates toward zero; the expression is always valid.
Example: ["2","1","+","3","*"] -> (2+1)*3 = 9; ["4","13","5","/","+"] -> 4 + 13/5 = 6.

Brute force
-----------
Repeatedly scan the token list for the first operator, apply it to the two numbers right
before it, splice the result back in as a single token, and restart. O(n^2) time (n/2
reductions, each an O(n) scan plus list rebuild), O(n) space. The wasted work: every pass
re-reads the numbers at the front of the list that have not changed.

From brute force to optimal
---------------------------
The redundancy is re-reading the pending operands. Observation: in postfix the operands of an
operator are always the two most recently seen unconsumed values -- LIFO order. So keep the
unconsumed values on a stack: a number is pushed, an operator pops two, computes, and pushes
the result. Every token is processed exactly once in a single left-to-right pass, and the
"splice back in" step becomes a push.

Intuition
---------
Postfix is designed for a stack: by the time you read an operator its operands are the last
two things you saw. Push numbers, and let operators consume the top two.

Geometric view
--------------
Tokens flow in from the left; the stack is a column of pending numbers. A number lands on
the column, an operator plucks the top two, fuses them, and drops the result back. At the
end exactly one number remains.

Steps
-----
1. stack = [].
2. For each token: if it is an operator, pop b then a, push a op b; else push int(token).
3. Return the single remaining stack element.

Complexity: O(n) time, O(n) space — one push/pop per token.
Pitfalls: Operand order (a = second pop, b = first pop; "6 3 -" is 6-3); Python's // floors
toward -inf, so use int(a / b) to truncate toward zero; treating "-3" as an operator.
"""
from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: int(a / b),          # truncate toward zero, not floor
        }
        stack = []
        for tok in tokens:
            if tok in ops:
                b, a = stack.pop(), stack.pop()    # second-popped is the left operand
                stack.append(ops[tok](a, b))
            else:
                stack.append(int(tok))
        return stack[0]


def brute_force(tokens: List[str]) -> int:
    toks = list(tokens)
    while len(toks) > 1:                                   # one reduction per full rescan
        for i, tok in enumerate(toks):
            if tok in {"+", "-", "*", "/"}:
                a, b = int(toks[i - 2]), int(toks[i - 1])
                val = a + b if tok == "+" else a - b if tok == "-" else a * b if tok == "*" else int(a / b)
                toks[i - 2:i + 1] = [str(val)]
                break
    return int(toks[0])


if __name__ == "__main__":
    s = Solution()
    cases = [
        ["2", "1", "+", "3", "*"],
        ["4", "13", "5", "/", "+"],
        ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],
        ["-7", "2", "/"],
        ["42"],
    ]
    assert s.evalRPN(["2", "1", "+", "3", "*"]) == 9
    assert s.evalRPN(["4", "13", "5", "/", "+"]) == 6
    assert s.evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    assert s.evalRPN(["-7", "2", "/"]) == -3
    for c in cases:
        assert s.evalRPN(c) == brute_force(c)
    print("ok")
