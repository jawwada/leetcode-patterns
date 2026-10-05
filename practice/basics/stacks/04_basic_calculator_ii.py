"""
Basic Calculator II (LeetCode 227) - Basics
Area: stacks
Key operations: build the number digit by digit, apply the pending operator, push a signed term, multiply or divide the top

Evaluate an expression of non-negative integers, the operators + - * / and spaces; integer division
truncates toward zero. Keep a stack of terms: '+' and '-' push the number with its sign, '*' and '/'
combine it with the top right away, and the answer is the sum of the stack.
Example: "3+2*2" -> 7, " 3/2 " -> 1, "14-3/2" -> 13
"""
import re
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(s: str) -> int:
    """Tokenize, then repeatedly collapse the leftmost '*' or '/', then the '+' and '-' left to right. O(n^2) from the list deletions."""
    toks = [int(t) if t.isdigit() else t for t in re.findall(r"\d+|[+\-*/]", s)]
    for group in ("*/", "+-"):
        i = 1
        while i < len(toks):
            if toks[i] in group:
                a, op, b = toks[i - 1], toks[i], toks[i + 1]
                if op == "+":
                    v = a + b
                elif op == "-":
                    v = a - b
                elif op == "*":
                    v = a * b
                else:
                    v = int(a / b)
                toks[i - 1:i + 2] = [v]
            else:
                i += 2
    return toks[0]


# --- optimal ---
def solve(s: str) -> int:
    """Stack of signed terms; when an operator (or the end) arrives, apply the PREVIOUS operator to the number just read. O(n)."""
    stack = []
    num, op = 0, "+"
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in "+-*/" or i == len(s) - 1:
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))
            log(f"ch={ch!r}: apply pending '{op}' to {num}; stack top->bottom {stack[::-1]}")
            num, op = 0, ch
    return sum(stack)


# --- demo ---
def demo():
    return solve("14-3/2")


# --- tests ---
def tests():
    assert solve("3+2*2") == 7
    assert solve(" 3/2 ") == 1
    assert solve(" 3+5 / 2 ") == 5
    assert solve("14-3/2") == 13
    assert solve("42") == 42
    assert solve("0") == 0
    assert solve("1-7/2") == -2          # truncate toward zero, not floor
    assert solve("2*3+4*5-6/4") == 25
    assert solve("100 - 100 * 2 / 3") == 34
    import random
    rng = random.Random(0)
    for _ in range(200):
        parts = [str(rng.randint(1, 20))]
        for _ in range(rng.randint(0, 5)):
            parts.append(rng.choice(["+", "-", "*", "/"]))
            parts.append(str(rng.randint(1, 20)))
        s = rng.choice(["", " "]).join(parts) + rng.choice(["", " "])
        assert solve(s) == brute_force(s), s


# --- bugs ---
BUGS = [
    {
        "replace": "        if ch in \"+-*/\" or i == len(s) - 1:",
        "with":    "        elif ch in \"+-*/\" or i == len(s) - 1:",
        "fix": "use a second 'if', not 'elif': the last character is usually a digit and must trigger the final apply",
        "why": "With 'elif' the last digit of '3+2*2' is read but never applied, so the result is 3 + 2 = 5 instead of 7.",
        "decoys": [
            {"line": "            num = num * 10 + int(ch)", "change": "should be num = int(ch)"},
            {"line": "    return sum(stack)", "change": "should return stack[-1]"},
            {"line": "                stack.append(-num)", "change": "should append num and subtract later"},
        ],
    },
    {
        "replace": "                stack.append(int(stack.pop() / num))",
        "with":    "                stack.append(stack.pop() // num)",
        "fix": "truncate toward zero with int(a / b); '//' floors, which differs for a negative top",
        "why": "In '1-7/2' the top is -7 and -7 // 2 = -4, giving -3 instead of 1 - 3 = -2.",
        "decoys": [
            {"line": "                stack.append(stack.pop() * num)", "change": "should push num and multiply at the end"},
            {"line": "    num, op = 0, \"+\"", "change": "op should start as ''"},
            {"line": "        if ch.isdigit():", "change": "should be 'elif'"},
        ],
    },
    {
        "replace": "            num, op = 0, ch",
        "with":    "            op = ch",
        "fix": "reset num to 0 after applying it, or the next number's digits are appended to the old one",
        "why": "'3+2*2' keeps num = 3 after the push, reads 32 at the '*', and the sum is far too large.",
        "decoys": [
            {"line": "                stack.append(num)", "change": "should append -num"},
            {"line": "    stack = []", "change": "should start as [0]"},
            {"line": "    for i, ch in enumerate(s):", "change": "should iterate over s.split()"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
