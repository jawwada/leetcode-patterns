"""
Basic Calculator II (LeetCode 227) - Medium
Chapter: stack
Pattern: Stack evaluation

Evaluate a string expression of non-negative integers, the operators + - * / and spaces,
with normal precedence; integer division truncates toward zero.
Example: "3+2*2" -> 7; " 3/2 " -> 1; " 3+5 / 2 " -> 5.
"""


# --- helpers ---
def apply_operator(a, b, op):
    """Compute a op b. Division truncates toward zero."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return int(a / b)


def tokenize(s):
    """'3+5 / 2' -> [3, '+', 5, '/', 2]: numbers and operators alternate, spaces are dropped."""
    tokens = []
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-*/":
            tokens.append(num)
            tokens.append(ch)
            num = 0
    tokens.append(num)                              # the last number has no operator after it
    return tokens


# --- brute force ---
def brute_force(s):
    """Tokenize, collapse every * and / first, then every + and -. O(n^2) time, O(n) space."""
    tokens = tokenize(s)
    for level in ["*/", "+-"]:                      # two passes: high precedence first
        i = 1                                       # operators sit at the odd positions
        while i < len(tokens):
            if tokens[i] in level:
                value = apply_operator(tokens[i - 1], tokens[i + 1], tokens[i])
                tokens = tokens[:i - 1] + [value] + tokens[i + 2:]   # splice shifts the tail
            else:
                i += 2
    return tokens[0]


# --- optimal ---
def calculate(s):
    """Push +num or -num; on * or / combine with the previous term. O(n) time, O(n) space."""
    stack = []                  # resolved terms; the answer is their sum
    num = 0
    op = "+"                    # the operator that came BEFORE the number being read
    for i in range(len(s)):
        ch = s[i]
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in "+-*/" or i == len(s) - 1:         # number finished: apply the pending op
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)     # precedence reaches back one term only
            else:
                stack.append(int(stack.pop() / num))   # truncate toward zero
            num = 0
            op = ch
    return sum(stack)


# --- try the brute force ---
print(brute_force("3+2*2"))       # -> 7
print(brute_force(" 3/2 "))       # -> 1
print(brute_force(" 3+5 / 2 "))   # -> 5
print(brute_force("14-3/2"))      # -> 13


# --- try the optimal ---
print(calculate("3+2*2"))       # -> 7
print(calculate(" 3/2 "))       # -> 1
print(calculate(" 3+5 / 2 "))   # -> 5
print(calculate("14-3/2"))      # -> 13
