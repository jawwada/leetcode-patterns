"""
Basic Calculator - Evaluate + - * / and Parentheses with a Stack

Evaluate a valid expression of non-negative integers, + - * /, parentheses
and spaces, with the usual precedence; / truncates toward zero and a minus
may open the expression or a group: "2*(3+4)-10/3" -> 11.
"""


# --- algorithm ---
def calculate(s):
    """Evaluate the whole string. O(n) time, O(n) space."""
    value, end = evaluate(s, 0)
    return value


def evaluate(s, i):
    """Evaluate from index i up to the matching ')' or the end of s.
    Returns (value, next index to read). Linear in what it reads."""
    stack = []                  # signed terms of this level; value = their sum
    num = 0
    op = "+"                    # the operator in front of num
    while i < len(s):
        ch = s[i]
        i += 1
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "(":
            num, i = evaluate(s, i)     # a whole group acts as one number
        elif ch in "+-*/)":
            apply_op(stack, op, num)
            if ch == ")":
                return sum(stack), i
            op = ch
            num = 0
    apply_op(stack, op, num)
    return sum(stack), i


def apply_op(stack, op, num):
    """Fold num into the terms using the operator in front of it. O(1)."""
    if op == "+":
        stack.append(num)
    elif op == "-":
        stack.append(-num)
    elif op == "*":
        stack.append(stack.pop() * num)     # * reaches back one term only
    else:
        stack.append(int(stack.pop() / num))    # int() truncates toward 0


# --- try it ---
print(calculate("2*(3+4)-10/3"))           # -> 11
print(calculate(" 3+5 / 2 "))              # -> 5
print(calculate("(1+(4+5+2)-3)+(6+8)"))    # -> 23
print(calculate("-(2 + 3)"))               # -> -5
