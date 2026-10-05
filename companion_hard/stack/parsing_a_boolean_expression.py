"""
Parsing a Boolean Expression (LeetCode 1106) - Hard
Chapter: stack
Pattern: Stack-based expression evaluation

Evaluate a boolean expression built from 't', 'f', !(expr), &(expr,expr,...) and
|(expr,expr,...).
Example: "&(|(f))" -> False; "|(f,f,f,t)" -> True; "!(&(f,t))" -> True.
"""


# --- helpers ---
def apply_op(op, values):
    """Combine operand letters: '!' flips its one letter, '&' fails on any 'f', '|' needs a 't'."""
    if op == "!":
        if values[0] == "f":
            return "t"
        return "f"
    if op == "&":
        if "f" in values:
            return "f"
        return "t"
    if "t" in values:                       # op is "|"
        return "t"
    return "f"


# --- brute force ---
def brute_force(expression):
    """Collapse the innermost group to one letter and rebuild the string; repeat. O(n^2) time."""
    s = expression
    while "(" in s:
        close_at = s.index(")")                 # the first ')' closes an innermost group
        open_at = s.rindex("(", 0, close_at)    # the last '(' before it opens that group
        op = s[open_at - 1]
        inside = s[open_at + 1:close_at]
        letters = inside.split(",")
        value = apply_op(op, letters)
        s = s[:open_at - 1] + value + s[close_at + 1:]   # copies the whole string every round
    return s == "t"


# --- optimal ---
def parse_bool_expr(expression):
    """Push as you read; a ')' pops its group, computes one letter and pushes it. O(n) time."""
    stack = []                              # operators, '(' and letters 't' / 'f'
    for c in expression:
        if c == ",":
            continue                        # commas carry no information
        if c != ")":
            stack.append(c)
            continue
        letters = []
        while stack[-1] != "(":             # collect this group's operand letters
            letters.append(stack.pop())
        stack.pop()                         # the '('
        op = stack.pop()
        stack.append(apply_op(op, letters))     # the group collapses to one letter
    return stack[0] == "t"


# --- try the brute force ---
print(brute_force("&(|(f))"))                      # -> False
print(brute_force("|(f,f,f,t)"))                   # -> True
print(brute_force("!(&(f,t))"))                    # -> True
print(brute_force("&(|(f,t),&(t,!(f)),|(f,f))"))   # -> False


# --- try the optimal ---
print(parse_bool_expr("&(|(f))"))                      # -> False
print(parse_bool_expr("|(f,f,f,t)"))                   # -> True
print(parse_bool_expr("!(&(f,t))"))                    # -> True
print(parse_bool_expr("&(|(f,t),&(t,!(f)),|(f,f))"))   # -> False
