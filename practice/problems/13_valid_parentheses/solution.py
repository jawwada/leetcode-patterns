"""
Valid Parentheses (LeetCode 20) - Medium
Area: stack
Key operations: push an opener, on a closer check the top and pop, empty stack at the end

Given a string of the brackets ()[]{}, decide whether it is valid: every opener is closed by the
same kind of bracket, in nested order, and nothing is left open.
Example: "([]{})" -> True; "([)]" -> False; "((" -> False
"""
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(s: str) -> bool:
    """Repeatedly delete an adjacent pair "()", "[]" or "{}" until none is left; valid iff the string
    is empty. O(n^2): n/2 deletions, each rescanning and copying the whole string."""
    changed = True
    while changed:
        changed = False
        for pair in ("()", "[]", "{}"):
            if pair in s:
                s = s.replace(pair, "", 1)
                changed = True
    return s == ""


# --- optimal ---
def solve(s: str) -> bool:
    """Stack of open brackets. A closer must match the most recent opener (the top), which is then
    popped; at the end nothing may remain open. One push or pop per character: O(n)."""
    pairs = {")": "(", "]": "[", "}": "{"}  # closer -> matching opener
    stack = []
    log(f"{s}")
    for i, ch in enumerate(s):
        if ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                log(f"{' ' * i}^ '{ch}' closer, top {stack[-1] if stack else 'empty'} does not match '{pairs[ch]}' -> False")
                return False
            stack.pop()
            log(f"{' ' * i}^ '{ch}' closer matches top '{pairs[ch]}' -> pop   stack top->bottom {stack[::-1]}")
        else:
            stack.append(ch)
            log(f"{' ' * i}^ '{ch}' opener -> push   stack top->bottom {stack[::-1]}")
    log(f"end: stack {stack[::-1]} -> {not stack}")
    return not stack


# --- demo ---
def demo():
    return solve("([]{})")


# --- tests ---
def tests():
    assert solve("([]{})") is True
    assert solve("()") is True
    assert solve("()[]{}") is True
    assert solve("{[]}") is True
    assert solve("") is True
    assert solve("(]") is False
    assert solve("([)]") is False  # right counts, wrong order
    assert solve("((") is False  # left open
    assert solve("]") is False  # closer with nothing open
    assert solve("())") is False
    import random
    random.seed(1)
    for _ in range(200):
        t = "".join(random.choice("()[]{}") for _ in range(random.randint(0, 10)))
        assert solve(t) == brute_force(t), t


# --- bugs ---
BUGS = [
    {
        "replace": "    return not stack",
        "with":    "    return True",
        "fix": "return not stack: openers still on the stack were never closed",
        "why": "Reaching the end without a mismatch is not enough; \"((\" and \"(\" would be accepted even though nothing closes them.",
        "decoys": [
            {"line": "            stack.pop()", "change": "should run before the top is compared"},
            {"line": "        if ch in pairs:", "change": "should be ch in pairs.values()"},
            {"line": "            stack.append(ch)", "change": "should push pairs[ch]"},
        ],
    },
    {
        "replace": "            if not stack or stack[-1] != pairs[ch]:",
        "with":    "            if stack and stack[-1] != pairs[ch]:",
        "fix": "a closer with an empty stack is invalid: if not stack or stack[-1] != pairs[ch]",
        "why": "With the empty check dropped, \"]\" and \")(\" fall through to stack.pop() on an empty list and raise IndexError instead of returning False.",
        "decoys": [
            {"line": "    return not stack", "change": "should be return len(stack) == 1"},
            {"line": "    pairs = {\")\": \"(\", \"]\": \"[\", \"}\": \"{\"}  # closer -> matching opener", "change": "should map openers to closers"},
            {"line": "            stack.append(ch)", "change": "should be stack.insert(0, ch)"},
        ],
    },
    {
        "replace": "            stack.pop()",
        "with":    "            stack.pop(0)",
        "fix": "pop the top, stack.pop(): the match was checked against stack[-1]",
        "why": "pop(0) removes the oldest opener instead of the one just matched, so \"([])\" leaves '[' on top and rejects the final ')'.",
        "decoys": [
            {"line": "            if not stack or stack[-1] != pairs[ch]:", "change": "should compare stack[0]"},
            {"line": "    stack = []", "change": "should start with a sentinel \"#\""},
            {"line": "    return not stack", "change": "should return stack == [\"\"]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
