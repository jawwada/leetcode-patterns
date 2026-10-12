"""
Evaluate Reverse Polish Notation (LeetCode 150) - Medium
Area: stack
Key operations: push number, pop two operands (right one first), apply operator, push result

Evaluate an arithmetic expression written in postfix notation as a list of tokens: integers and
the operators + - * /. Division truncates toward zero. The expression is always valid.
Example: ["2", "1", "+", "3", "*"] -> (2 + 1) * 3 = 9
"""
from typing import List


# --- brute force ---
def brute_force(tokens: List[str]) -> int:
    """Find the first operator, apply it to the two numbers just before it, splice the result back
    in as one token and rescan from the start. O(n^2): every pass re-reads the unchanged front."""
    toks = list(tokens)
    while len(toks) > 1:
        for i, tok in enumerate(toks):
            if tok in {"+", "-", "*", "/"}:
                a, b = int(toks[i - 2]), int(toks[i - 1])
                val = a + b if tok == "+" else a - b if tok == "-" else a * b if tok == "*" else int(a / b)
                toks[i - 2:i + 1] = [str(val)]
                break
    return int(toks[0])


# --- optimal ---
def solve(tokens: List[str]) -> int:
    """Stack of numbers not yet consumed. A number is pushed; an operator pops its two operands
    (the right operand was pushed last, so it comes off first), computes, and pushes the result.
    One pass: O(n) time, O(n) space."""
    stack = []
    for tok in tokens:
        if tok in {"+", "-", "*", "/"}:
            b, a = stack.pop(), stack.pop()
            if tok == "+":
                val = a + b
            elif tok == "-":
                val = a - b
            elif tok == "*":
                val = a * b
            else:
                # int(a / b) truncates toward zero; a // b would floor -7 / 2 to -4 instead of -3
                val = int(a / b)
            stack.append(val)
        else:
            stack.append(int(tok))
    return stack[-1]


# --- demo ---
def demo():
    return solve(["2", "1", "+", "3", "*"])


# --- bugs ---
BUGS = [
    {
        "replace": "            b, a = stack.pop(), stack.pop()",
        "with":    "            a, b = stack.pop(), stack.pop()",
        "fix": "the first pop is the right operand b, the second pop is the left operand a",
        "why": "Postfix pushes the left operand first, so it is deeper in the stack; swapping makes \"6 3 -\" compute 3 - 6 = -3 instead of 3.",
        "decoys": [
            {"line": "                val = a - b", "change": "should be b - a"},
            {"line": "            stack.append(val)", "change": "should push a and b back before val"},
            {"line": "    return stack[-1]", "change": "should return stack[0]"},
        ],
    },
    {
        "replace": "                val = int(a / b)",
        "with":    "                val = a // b",
        "fix": "use int(a / b): the problem truncates toward zero, // floors toward -infinity",
        "why": "For a negative quotient floor and truncation differ: -7 // 2 is -4 but the expected answer for \"-7 2 /\" is -3.",
        "decoys": [
            {"line": "            b, a = stack.pop(), stack.pop()", "change": "should pop a first, then b"},
            {"line": "            stack.append(int(tok))", "change": "should push tok without int()"},
            {"line": "                val = a * b", "change": "should be int(a * b)"},
        ],
    },
    {
        "replace": "        if tok in {\"+\", \"-\", \"*\", \"/\"}:",
        "with":    "        if not tok.isdigit():",
        "fix": "test membership in the operator set; a negative number like \"-7\" is not a digit string",
        "why": "\"-7\".isdigit() is False, so a negative number is treated as an operator and pops from an empty stack on [\"-7\", \"2\", \"/\"].",
        "decoys": [
            {"line": "    stack = []", "change": "should start as [0]"},
            {"line": "                val = a + b", "change": "should be int(a + b)"},
            {"line": "            stack.append(val)", "change": "should be stack.insert(0, val)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
