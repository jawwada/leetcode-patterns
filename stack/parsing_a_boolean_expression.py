"""
Parsing a Boolean Expression (LeetCode 1106)  — Hard
Pattern: Stack-based expression evaluation

Problem
-------
Evaluate a boolean expression built from 't', 'f', !(expr), &(expr,expr,...), |(expr,expr,...).
Example: "&(|(f))" -> False; "|(f,f,f,t)" -> True; "!(&(f,t))" -> True.

Brute force
-----------
Repeatedly reduce the innermost group: find the first ')', walk back to its '(', the character
before that is the operator, split the inside on ',', evaluate, splice the result letter back
into the string, repeat until no '(' remains. Each round rebuilds the whole string, so for d
nested groups the work is O(n * d) = O(n^2) in the worst case, O(n) space. The wasted work is
re-copying and re-scanning the untouched outer text on every reduction.

From brute force to optimal
---------------------------
The redundancy is re-materialising the whole expression after each inner evaluation.
Observation: the text to the left of an innermost group is never inspected until that group
has collapsed to a single letter, so it can sit untouched on a stack instead of being copied.
Push operators, '(' and 't'/'f' as they arrive; on ')' pop letters down to the matching '(',
pop the operator beneath it, compute one letter, push it back. That letter is exactly the
operand the enclosing group needs. Each character is pushed once and popped once, so the whole
evaluation is a single O(n) pass with O(n) stack space.

Intuition
---------
A ')' is the signal that a complete sub-expression has just ended and everything it needs is at
the top of the stack. Because &, | and ! only care about the SET of operand values (is there
an 'f'? is there a 't'? is the single operand 'f'?), collecting the popped letters into a set
makes each operator a one-liner. Commas carry no information and are skipped.

Geometric view
--------------
The stack mirrors the nesting depth: every '(' opens a new ledge, letters pile on the top ledge,
and ')' sweeps the top ledge into a single letter that drops onto the ledge below. The input is
read strictly left to right; the stack height is the current nesting depth.

Steps
-----
1. For each char c: if c == ',' skip.
2. If c != ')': push c (operators, '(', 't', 'f').
3. On ')': pop into a set until '(' is on top; pop the '('; pop the operator.
4. '!': push 't' if set == {'f'} else 'f'. '&': push 'f' if 'f' in set else 't'.
   '|': push 't' if 't' in set else 'f'.
5. At the end the stack holds one letter; return it == 't'.

Complexity: O(n) time, O(n) space — every character is pushed and popped at most once.
Pitfalls: forgetting to pop the '(' and the operator; evaluating '&' as "all t" on an EMPTY
set (the grammar guarantees >= 1 operand, but the set form is robust anyway); treating a bare
"t"/"f" expression as an error.
"""


class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        stack = []                                   # operators, "(", and letters 't'/'f'
        for c in expression:
            if c == ",":
                continue
            if c != ")":
                stack.append(c)
                continue
            vals = set()
            while stack[-1] != "(":                  # collect this group's operand values
                vals.add(stack.pop())
            stack.pop()                              # the "("
            op = stack.pop()
            if op == "!":
                stack.append("t" if vals == {"f"} else "f")
            elif op == "&":
                stack.append("f" if "f" in vals else "t")
            else:                                    # "|"
                stack.append("t" if "t" in vals else "f")
        return stack[0] == "t"


def brute_force(expression: str) -> bool:
    s = expression
    while "(" in s:
        close = s.index(")")                         # first ")" closes an innermost group
        open_ = s.rindex("(", 0, close)
        op, args = s[open_ - 1], s[open_ + 1:close].split(",")
        if op == "!":
            val = "t" if args == ["f"] else "f"
        elif op == "&":
            val = "f" if "f" in args else "t"
        else:
            val = "t" if "t" in args else "f"
        s = s[:open_ - 1] + val + s[close + 1:]      # rebuild the whole string each round
    return s == "t"


if __name__ == "__main__":
    s = Solution()
    cases = {"&(|(f))": False, "|(f,f,f,t)": True, "!(&(f,t))": True, "t": True, "f": False,
             "&(t,t,!(f))": True, "|(&(t,f,t),!(t))": False, "!(|(f,&(t,t),f))": False,
             "&(|(f,t),&(t,!(f)),|(f,f))": False}
    for expr, want in cases.items():
        assert s.parseBoolExpr(expr) is want, expr
        assert brute_force(expr) is want, expr
    print("ok")
