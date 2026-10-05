"""
Expression Add Operators (LeetCode 282) - Hard
Chapter: backtracking
Pattern: Backtracking with running value + last operand

Given a digit string num and an integer target, insert '+', '-' or '*' between some of the
digits (or nothing, to form multi-digit operands) so the expression equals target. Return
all such expressions. Operands may not have leading zeros.
Example: num = "123", target = 6 -> ["1*2*3", "1+2+3"];
num = "105", target = 5 -> ["1*0+5", "10-5"].
"""
from itertools import product   # every combination of one choice per slot


# --- brute force ---
def brute_force(num, target):
    """Pick '', '+', '-' or '*' for every gap, build the string, evaluate it. O(4^n * n)."""
    result = []
    gaps = len(num) - 1
    for separators in product(["", "+", "-", "*"], repeat=gaps):
        expr = num[0]
        for i in range(gaps):
            expr += separators[i] + num[i + 1]
        if has_leading_zero(expr):
            continue
        if eval(expr) == target:                  # Python re-parses the whole string at every leaf
            result.append(expr)
    return result


def has_leading_zero(expr):
    """True when some operand looks like '05': longer than one digit and starting with 0."""
    operand = ""
    for c in expr + "+":                          # the extra '+' flushes the last operand
        if c in "+-*":
            if len(operand) > 1 and operand[0] == "0":
                return True
            operand = ""
        else:
            operand += c
    return False


# --- optimal ---
def expression_add_operators(num, target):
    """DFS over operand ends, carrying (value, last term) so '*' can undo the last term. O(4^n)."""
    result = []
    extend(num, target, 0, "", 0, 0, result)
    return result


def extend(num, target, i, expr, value, last, result):
    if i == len(num):
        if value == target:
            result.append(expr)
        return
    for j in range(i + 1, len(num) + 1):
        piece = num[i:j]
        if len(piece) > 1 and piece[0] == "0":
            break                                 # no leading zeros; longer pieces have one too
        current = int(piece)
        if i == 0:
            extend(num, target, j, piece, current, current, result)   # first operand: no operator
        else:
            extend(num, target, j, expr + "+" + piece, value + current, current, result)
            extend(num, target, j, expr + "-" + piece, value - current, -current, result)
            # '*' binds tighter: take the last term back out, put last * current in instead
            extend(num, target, j, expr + "*" + piece, value - last + last * current,
                   last * current, result)


# --- try the brute force ---
# any order is accepted, so the demos print the expressions sorted
print(sorted(brute_force("123", 6)))    # -> ['1*2*3', '1+2+3']
print(sorted(brute_force("232", 8)))    # -> ['2*3+2', '2+3*2']
print(sorted(brute_force("105", 5)))    # -> ['1*0+5', '10-5']
print(sorted(brute_force("00", 0)))     # -> ['0*0', '0+0', '0-0']


# --- try the optimal ---
# any order is accepted, so the demos print the expressions sorted
print(sorted(expression_add_operators("123", 6)))    # -> ['1*2*3', '1+2+3']
print(sorted(expression_add_operators("232", 8)))    # -> ['2*3+2', '2+3*2']
print(sorted(expression_add_operators("105", 5)))    # -> ['1*0+5', '10-5']
print(sorted(expression_add_operators("00", 0)))     # -> ['0*0', '0+0', '0-0']
