"""
Evaluate Reverse Polish Notation (LeetCode 150) - Medium
Chapter: stack
Pattern: Stack evaluation

Evaluate an arithmetic expression written in postfix (RPN) as a list of tokens: integers and
the operators + - * /. Division truncates toward zero and the expression is always valid.
Example: ["2", "1", "+", "3", "*"] -> (2 + 1) * 3 = 9; ["4", "13", "5", "/", "+"] -> 4 + 13/5 = 6.
"""


# --- helpers ---
def apply_operator(a, b, op):
    """Compute a op b. Division truncates toward zero: int(-7 / 2) is -3, not -4."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return int(a / b)


# --- brute force ---
def brute_force(tokens):
    """Find the first operator, replace it and its two operands by the result, restart. O(n^2)."""
    tokens = list(tokens)                           # copy so the caller's list is untouched
    while len(tokens) > 1:                          # one reduction per full rescan
        for i in range(len(tokens)):
            if tokens[i] in ["+", "-", "*", "/"]:
                a = int(tokens[i - 2])
                b = int(tokens[i - 1])
                value = apply_operator(a, b, tokens[i])
                tokens = tokens[:i - 2] + [str(value)] + tokens[i + 1:]   # splice it back in
                break
    return int(tokens[0])


# --- optimal ---
def eval_rpn(tokens):
    """Push numbers; an operator pops two, computes, pushes the result. O(n) time, O(n) space."""
    stack = []
    for token in tokens:
        if token in ["+", "-", "*", "/"]:
            b = stack.pop()                         # popped first, but it is the RIGHT operand
            a = stack.pop()
            stack.append(apply_operator(a, b, token))
        else:
            stack.append(int(token))
    return stack[0]


# --- try the brute force ---
print(brute_force(["2", "1", "+", "3", "*"]))                                               # -> 9
print(brute_force(["4", "13", "5", "/", "+"]))                                              # -> 6
print(brute_force(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]))   # -> 22
print(brute_force(["-7", "2", "/"]))                                                        # -> -3


# --- try the optimal ---
print(eval_rpn(["2", "1", "+", "3", "*"]))                                               # -> 9
print(eval_rpn(["4", "13", "5", "/", "+"]))                                              # -> 6
print(eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]))   # -> 22
print(eval_rpn(["-7", "2", "/"]))                                                        # -> -3
