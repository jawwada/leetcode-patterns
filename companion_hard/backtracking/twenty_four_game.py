"""
24 Game (LeetCode 679) - Hard
Chapter: backtracking
Pattern: Reduce-the-multiset backtracking (combine two values, recurse on the rest)

Given four cards with values 1..9, decide whether +, -, *, / (real division) and parentheses
can be arranged so the expression equals 24. Every card is used exactly once and the
operators are binary.
Example: [4,1,8,7] -> True because (8 - 4) * (7 - 1) = 24; [1,2,1,2] -> False.
"""
from fractions import Fraction               # exact arithmetic, so 8 / (3 - 8 / 3) is exactly 24
from itertools import permutations, product  # every card order, every operator triple


# --- brute force ---
def brute_force(cards):
    """Every card order x operator triple x bracketing (5 shapes), exact arithmetic. 7680 tries."""
    for order in permutations(cards):
        for ops in product("+-*/", repeat=3):
            for shape in range(5):
                try:
                    if evaluate(shape, order, ops) == 24:
                        return True
                except ZeroDivisionError:         # divided by zero: not a legal expression
                    pass
    return False


def apply_op(x, y, op):
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    if op == "*":
        return x * y
    return x / y


def evaluate(shape, order, ops):
    """The 5 ways to bracket four operands a b c d with operators p q r."""
    a, b, c, d = Fraction(order[0]), Fraction(order[1]), Fraction(order[2]), Fraction(order[3])
    p, q, r = ops
    if shape == 0:
        return apply_op(apply_op(apply_op(a, b, p), c, q), d, r)      # ((a b) c) d
    if shape == 1:
        return apply_op(apply_op(a, apply_op(b, c, q), p), d, r)      # (a (b c)) d
    if shape == 2:
        return apply_op(apply_op(a, b, p), apply_op(c, d, r), q)      # (a b) (c d)
    if shape == 3:
        return apply_op(a, apply_op(apply_op(b, c, q), d, r), p)      # a ((b c) d)
    return apply_op(a, apply_op(b, apply_op(c, d, r), q), p)          # a (b (c d))


# --- optimal ---
def twenty_four_game(cards):
    """Pick two numbers, replace them by one of six results, recurse on the rest. 3888 leaves."""
    numbers = []
    for card in cards:
        numbers.append(float(card))
    return solve(numbers)


def solve(numbers):
    if len(numbers) == 1:
        return abs(numbers[0] - 24) < 1e-6          # floats: compare with a tolerance, never ==
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            a = numbers[i]
            b = numbers[j]
            rest = []
            for k in range(len(numbers)):
                if k != i and k != j:
                    rest.append(numbers[k])
            results = [a + b, a - b, b - a, a * b]   # six ways to merge the pair
            if abs(b) > 1e-6:
                results.append(a / b)
            if abs(a) > 1e-6:
                results.append(b / a)
            for value in results:
                if solve(rest + [value]):             # the table shrinks by one number
                    return True
    return False


# --- try the brute force ---
print(brute_force([4, 1, 8, 7]))   # -> True
print(brute_force([1, 2, 1, 2]))   # -> False
print(brute_force([3, 3, 8, 8]))   # -> True
print(brute_force([1, 5, 5, 5]))   # -> True


# --- try the optimal ---
print(twenty_four_game([4, 1, 8, 7]))   # -> True
print(twenty_four_game([1, 2, 1, 2]))   # -> False
print(twenty_four_game([3, 3, 8, 8]))   # -> True
print(twenty_four_game([1, 5, 5, 5]))   # -> True
