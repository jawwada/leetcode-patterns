"""
Decode String (LeetCode 394) - Basics
Area: stacks
Key operations: accumulate the count digit by digit, push (prefix, count) on '[', pop and repeat on ']'

Decode k[encoded] meaning the encoded string repeated k times; brackets nest and counts may have
several digits. Letters outside brackets are copied as they are.
Example: "3[a2[c]]" -> "accaccacc"
"""
import re
import sys

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(s: str) -> str:
    """Expand one innermost k[letters] group per round until no bracket is left. Rescans the whole string every round, O(rounds * length)."""
    innermost = re.compile(r"(\d+)\[([a-z]*)\]")
    while "[" in s:
        s = innermost.sub(lambda m: m.group(2) * int(m.group(1)), s, count=1)
    return s


# --- optimal ---
def solve(s: str) -> str:
    """One stack of (string built before the bracket, repeat count); ']' pops it and glues prefix + cur * count. O(output length)."""
    stack = []
    cur, k = "", 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, k))
            log(f"'[': push ({cur!r}, {k}); stack top->bottom {stack[::-1]}")
            cur, k = "", 0
        elif ch == "]":
            prev, cnt = stack.pop()
            cur = prev + cur * cnt
            log(f"']': pop ({prev!r}, {cnt}) -> cur = {cur!r}; stack top->bottom {stack[::-1]}")
        else:
            cur += ch
    return cur


# --- demo ---
def demo():
    return solve("3[a2[c]]")


# --- tests ---
def tests():
    assert solve("3[a2[c]]") == "accaccacc"
    assert solve("3[a]2[bc]") == "aaabcbc"
    assert solve("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert solve("abc") == "abc"
    assert solve("") == ""
    assert solve("10[a]") == "a" * 10          # multi-digit count
    assert solve("x2[y3[z]]w") == "xyzzzyzzzw"  # prefix before the bracket is kept in order
    import random
    rng = random.Random(0)

    def gen(depth):
        out = ""
        for _ in range(rng.randint(0, 3)):
            if depth < 3 and rng.random() < 0.4:
                out += f"{rng.randint(1, 12)}[{gen(depth + 1)}]"
            else:
                out += rng.choice("abc")
        return out

    for _ in range(200):
        s = gen(0)
        assert solve(s) == brute_force(s), s


# --- bugs ---
BUGS = [
    {
        "replace": "            k = k * 10 + int(ch)",
        "with":    "            k = int(ch)",
        "fix": "a count can have several digits: shift the old digits left with k * 10 before adding the new one",
        "why": "'10[a]' reads the count as 0 and returns '' instead of ten a's.",
        "decoys": [
            {"line": "            cur += ch", "change": "should be cur = ch"},
            {"line": "            prev, cnt = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "    return cur", "change": "should return ''.join(stack)"},
        ],
    },
    {
        "replace": "            cur = prev + cur * cnt",
        "with":    "            cur = cur * cnt + prev",
        "fix": "the text built BEFORE the bracket comes first: prefix + repeated bracket body",
        "why": "'3[a2[c]]' closes the inner bracket with prev 'a', cur 'c': the result must be 'acc', not 'cca'.",
        "decoys": [
            {"line": "            stack.append((cur, k))", "change": "should push (k, cur)"},
            {"line": "        if ch.isdigit():", "change": "should be ch.isalnum()"},
            {"line": "    cur, k = \"\", 0", "change": "k should start at 1"},
        ],
    },
    {
        "replace": "            cur, k = \"\", 0",
        "with":    "            cur = \"\"",
        "fix": "reset the count as well as the string after pushing; otherwise the next count builds on top of the old one",
        "why": "In '3[a2[c]]' the inner count becomes 3 * 10 + 2 = 32 because the 3 was never cleared.",
        "decoys": [
            {"line": "    stack = []", "change": "should start with ('', 1) on it"},
            {"line": "        elif ch == \"]\":", "change": "should also handle ')'"},
            {"line": "        elif ch == \"[\":", "change": "should be 'if', not 'elif'"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
