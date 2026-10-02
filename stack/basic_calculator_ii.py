"""
Basic Calculator II (LeetCode 227)  — Medium
Pattern: Stack evaluation

Problem
-------
Evaluate a string expression of non-negative integers, the operators + - * / and spaces,
with normal precedence (* and / before + and -) and integer division truncating toward zero.
Example: "3+2*2" -> 7; " 3/2 " -> 1; " 3+5 / 2 " -> 5.

Brute force
-----------
Tokenise, then make two passes over the token list: first repeatedly find a * or /, collapse
its two neighbours into one number and splice the list; then do the same for + and -.
O(n^2) time (each splice is O(n), up to n/2 splices), O(n) space. The wasted work: every
splice shifts the entire tail of the token list, and the second pass re-reads tokens the
first pass already visited.

From brute force to optimal
---------------------------
The redundancy is the two-pass splice-and-shift. Observation: precedence only ever reaches
back ONE term -- "a * b" must combine b with the term immediately before it, while "+" and
"-" can be deferred entirely by pushing signed terms and summing at the end. So keep a stack
of resolved terms: on + push num, on - push -num, on * or / pop the previous term, combine it
with num, push the result. One pass, every character read once, and the final answer is the
sum of the stack.

Intuition
---------
Treat the expression as a sum of terms, where each term is a product/quotient chain. The
stack holds finished terms; multiplication and division edit the term being built (the top),
addition and subtraction start a new one.

Geometric view
--------------
Reading "3+5/2": push 3; see '+', pending; 5 arrives, see '/', pending; 2 arrives, end of
string -> apply '/' to the top: pop 5, push 5/2 = 2. Stack is [3, 2], sum = 5. Each operator
is applied when the NEXT operator (or the end) arrives, because only then is its right
operand fully read.

Steps
-----
1. stack = [], num = 0, op = '+' (operator preceding the current number).
2. For each char: if digit, num = num*10 + d. If char is an operator or the last char:
   apply `op` to num -- '+': push num; '-': push -num; '*': push pop()*num; '/': push
   int(pop()/num) -- then num = 0, op = char.
3. Return sum(stack).

Complexity: O(n) time, O(n) space — single pass; stack holds at most the number of terms.
Pitfalls: Forgetting to apply the last pending operator at end of string; Python // floors
(use int(a / b) to truncate toward zero: int(-3 / 2) = -1); multi-digit numbers; skipping
spaces but still triggering the "apply" branch on them.
"""


class Solution:
    def calculate(self, s: str) -> int:
        stack = []                                   # resolved terms; answer = their sum
        num, op = 0, "+"                             # op = operator BEFORE the current number
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)
            if ch in "+-*/" or i == len(s) - 1:      # number complete: apply pending op
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    stack.append(int(stack.pop() / num))   # truncate toward zero
                num, op = 0, ch
        return sum(stack)


def brute_force(s: str) -> int:
    tokens, num = [], ""
    for ch in s.replace(" ", "") + "+":
        if ch.isdigit():
            num += ch
        else:
            tokens += [int(num), ch]
            num = ""
    tokens.pop()                                         # drop the trailing '+'
    apply = {"*": lambda a, b: a * b, "/": lambda a, b: int(a / b),
             "+": lambda a, b: a + b, "-": lambda a, b: a - b}
    for level in ("*/", "+-"):                           # two passes: high precedence first
        i = 1
        while i < len(tokens):
            if tokens[i] in level:
                tokens[i - 1:i + 2] = [apply[tokens[i]](tokens[i - 1], tokens[i + 1])]
            else:
                i += 2
    return tokens[0]


if __name__ == "__main__":
    s = Solution()
    cases = ["3+2*2", " 3/2 ", " 3+5 / 2 ", "14-3/2", "0-2*3", "42", "1-1+1", "100*2/3"]
    assert s.calculate("3+2*2") == 7
    assert s.calculate(" 3/2 ") == 1
    assert s.calculate(" 3+5 / 2 ") == 5
    assert s.calculate("14-3/2") == 13
    assert s.calculate("0-2*3") == -6
    assert s.calculate("42") == 42
    for c in cases:
        assert s.calculate(c) == brute_force(c)
    print("ok")
