"""
Basic Calculator (LeetCode 224) - Hard
Chapter: stack
Pattern: Sign stack for parentheses

Evaluate a string containing non-negative integers, '+', '-', '(', ')' and spaces,
including unary minus such as "-(2-3)". No eval().
Example: "(1+(4+5+2)-3)+(6+8)" -> 23; " 2-1 + 2 " -> 3; "-(2-3)" -> 1.
"""


# --- brute force ---
def find_closing(expr, open_at):
    """Walk forward from the '(' at open_at, counting depth, to its matching ')'."""
    depth = 0
    j = open_at
    while True:
        if expr[j] == "(":
            depth += 1
        elif expr[j] == ")":
            depth -= 1
        if depth == 0:
            return j
        j += 1


def evaluate(expr):
    """Sum signed terms left to right; a group is a recursive call on the text inside it."""
    total = 0
    sign = 1
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():   # read the whole number
                j += 1
            total += sign * int(expr[i:j])
            i = j
            continue
        if c == "(":
            close_at = find_closing(expr, i)             # look ahead for the matching ')'
            total += sign * evaluate(expr[i + 1:close_at])   # ... then read the inside again
            i = close_at
        elif c == "+":
            sign = 1
        elif c == "-":
            sign = -1
        i += 1
    return total


def brute_force(s):
    """Recursive descent: find each group's closing paren, recurse on the slice. O(n * depth)."""
    return evaluate(s)


# --- optimal ---
def calculate(s):
    """One pass with a stack of context signs; parentheses only flip signs. O(n) time."""
    result = 0
    num = 0
    sign = 1
    signs = [1]                             # sign in effect outside each open parenthesis
    for c in s + "+":                       # the extra "+" flushes the last number
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == "+" or c == "-":
            result += sign * num
            num = 0
            if c == "+":
                sign = signs[-1]            # the enclosing sign is folded into every term
            else:
                sign = -signs[-1]
        elif c == "(":
            signs.append(sign)              # everything inside inherits the sign in front
        elif c == ")":
            signs.pop()
    return result


# --- try the brute force ---
print(brute_force("(1+(4+5+2)-3)+(6+8)"))      # -> 23
print(brute_force(" 2-1 + 2 "))                # -> 3
print(brute_force("-(2-3)"))                   # -> 1
print(brute_force("10 - (2 - (3 - 4)) + 5"))   # -> 12


# --- try the optimal ---
print(calculate("(1+(4+5+2)-3)+(6+8)"))        # -> 23
print(calculate(" 2-1 + 2 "))                  # -> 3
print(calculate("-(2-3)"))                     # -> 1
print(calculate("10 - (2 - (3 - 4)) + 5"))     # -> 12
