"""
24 Game (LeetCode 679)  — Hard
Pattern: Reduce-the-multiset backtracking (combine two values, recurse on the rest)

Problem
-------
Given four cards with values 1..9, decide whether the operators +, -, *, / (real division) and
parentheses can be arranged so that the expression evaluates to 24. Every card is used exactly
once and the operators are binary (no unary minus, no concatenating digits).
Example: [4,1,8,7] -> True because (8 - 4) * (7 - 1) = 24.  [1,2,1,2] -> False.

Brute force
-----------
Enumerate every full expression: 4! orders of the cards, 4^3 operator triples and the 5 ways to
parenthesise four operands; evaluate each one exactly and compare with 24. That is 24 * 64 * 5 =
7680 expressions, O(1) in the problem size but the obvious "try everything" approach is still
instructive. The waste: a+b and b+a, (a*b) and (b*a), and every pair of parenthesisations that
yields the same value for the first sub-expression are all evaluated separately, and the five tree
shapes must be hand-written.

From brute force to optimal
---------------------------
The redundancy is that many (order, shape, operators) triples pass through the same intermediate
state. Observation: any evaluation of a 4-operand expression is a sequence of three steps, each of
which takes two values currently on the table and replaces them with one result. So the state is
just the multiset of values still on the table, and the search is "pick two, combine with one of
six results (a+b, a-b, b-a, a*b, a/b, b/a), recurse on the smaller list". The five tree shapes
fall out automatically (which pair you pick next decides the shape), commutative duplicates are
computed once, and the recursion depth is three. Floats with an epsilon handle 8 / (3 - 8 / 3) =
24, where intermediate values are not integers.

Intuition
---------
Instead of thinking in expression trees, think in table states: four numbers, then three, then
two, then one. Every legal expression is some way of collapsing the table, so exhaustively
collapsing it covers every expression without enumerating parentheses. Early return on the first
success keeps typical runs far below the ~12k leaves.

Geometric view
--------------
A tree of depth 3. The root holds 4 values and has C(4,2)*6 = 36 children (each a 3-value table);
each of those has C(3,2)*6 = 18 children (2-value tables), each of those 6 leaves (1 value). Check
each leaf against 24 with a tolerance; the whole tree has at most 36*18*6 = 3888 leaves.

Steps
-----
1. Convert the cards to floats; solve(nums).
2. If one number remains, return |nums[0] - 24| < 1e-6.
3. For every unordered pair (i < j): build rest = the other numbers.
4. For each of a+b, a-b, b-a, a*b, a/b (if b != 0), b/a (if a != 0): recurse on rest + [value].
5. Return True on the first success, False after all pairs are exhausted.

Complexity: O(1) time (bounded by 3888 leaves for four cards; O(n!^2 * 6^n) style growth in
general), O(n) space for the recursion stack.
Pitfalls: comparing floats with == instead of a tolerance; dividing by a value that is 0 (or
~0); forgetting b-a and b/a while only iterating i < j (subtraction and division are not
commutative).
"""
import random
from fractions import Fraction
from itertools import permutations, product
from typing import List


class Solution:
    def judgePoint24(self, cards: List[int]) -> bool:
        EPS = 1e-6

        def solve(nums: List[float]) -> bool:
            if len(nums) == 1:
                return abs(nums[0] - 24) < EPS
            n = len(nums)
            for i in range(n):
                for j in range(i + 1, n):
                    a, b = nums[i], nums[j]
                    rest = [nums[k] for k in range(n) if k != i and k != j]
                    results = [a + b, a - b, b - a, a * b]      # six ways to merge the pair
                    if abs(b) > EPS:
                        results.append(a / b)
                    if abs(a) > EPS:
                        results.append(b / a)
                    for v in results:
                        if solve(rest + [v]):                   # table shrinks by one value
                            return True
            return False

        return solve([float(x) for x in cards])


def brute_force(cards: List[int]) -> bool:
    # Every order x every operator triple x every one of the 5 parenthesisations, exact arithmetic.
    def ap(x, y, op):
        if op == "+":
            return x + y
        if op == "-":
            return x - y
        return x * y if op == "*" else x / y          # Fraction raises on division by zero

    shapes = (lambda a, b, c, d, p, q, r: ap(ap(ap(a, b, p), c, q), d, r),   # ((a b) c) d
              lambda a, b, c, d, p, q, r: ap(ap(a, ap(b, c, q), p), d, r),   # (a (b c)) d
              lambda a, b, c, d, p, q, r: ap(ap(a, b, p), ap(c, d, r), q),   # (a b) (c d)
              lambda a, b, c, d, p, q, r: ap(a, ap(ap(b, c, q), d, r), p),   # a ((b c) d)
              lambda a, b, c, d, p, q, r: ap(a, ap(b, ap(c, d, r), q), p))   # a (b (c d))
    for order in permutations(Fraction(x) for x in cards):
        for ops in product("+-*/", repeat=3):
            for shape in shapes:
                try:
                    if shape(*order, *ops) == 24:
                        return True
                except ZeroDivisionError:
                    pass
    return False


if __name__ == "__main__":
    s = Solution()
    cases = (([4, 1, 8, 7], True), ([1, 2, 1, 2], False), ([3, 3, 8, 8], True),   # 8/(3-8/3)
             ([1, 1, 1, 1], False), ([6, 6, 6, 6], True), ([1, 5, 5, 5], True))    # 5*(5-1/5)
    for cards, want in cases:
        assert s.judgePoint24(cards) == want, cards
        assert brute_force(cards) == want, cards
    rng = random.Random(7)
    for _ in range(12):                                      # random cross-check, both agree
        cards = [rng.randint(1, 9) for _ in range(4)]
        assert s.judgePoint24(cards) == brute_force(cards), cards
    print("ok")
