"""
Remove K Digits (LeetCode 402) - Basics
Area: monotonic stacks
Key operations: pop while top > digit and k remains, push digit, cut k leftovers from the end, strip leading zeros

Remove k digits from the decimal string num so that the remaining number is as small as possible.
Greedy: a bigger digit standing in front of a smaller one should go first, so the kept digits stay
non-decreasing bottom to top while deletions remain; whatever is left of k is cut from the end.
Example: "1432219", k=3 -> "1219"; "10200", k=1 -> "200"; "10", k=2 -> "0"
"""
import sys
from itertools import combinations

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(num: str, k: int) -> str:
    """Try every choice of n - k positions to keep and take the smallest value. O(C(n, k) * n)."""
    n = len(num)
    best = None
    for keep in combinations(range(n), n - k):
        s = "".join(num[i] for i in keep).lstrip("0") or "0"
        if best is None or int(s) < int(best):
            best = s
    return best


# --- optimal ---
def solve(num: str, k: int) -> str:
    """Non-decreasing stack of digits: pop a bigger top before a smaller digit while k > 0, then trim k from the end. O(n)."""
    stack = []
    for d in num:
        log(f"d={d} k={k} | stack top->bottom {stack[::-1]}")
        while k and stack and stack[-1] > d:
            popped = stack.pop()
            k -= 1
            log(f"    pop {popped} > {d} (k left {k}); stack top->bottom {stack[::-1]}")
        stack.append(d)
        log(f"    push {d}; stack top->bottom {stack[::-1]}")
    stack = stack[:len(stack) - k]
    log(f"cut {k} from the end -> {''.join(stack)!r}")
    return "".join(stack).lstrip("0") or "0"


# --- demo ---
def demo():
    return solve("1432219", 3)


# --- tests ---
def tests():
    assert solve("1432219", 3) == "1219"
    assert solve("10200", 1) == "200"
    assert solve("10", 2) == "0"
    assert solve("9", 1) == "0"
    assert solve("112", 1) == "11"       # equal digits are not popped
    assert solve("12345", 2) == "123"    # increasing: cut from the end
    assert solve("54321", 2) == "321"
    assert solve("10001", 1) == "1"      # leading zeros stripped after the cut
    assert solve("7", 0) == "7"
    import random
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 7)
        num = str(rng.randint(1, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(n - 1))
        k = rng.randint(0, n)
        assert solve(num, k) == brute_force(num, k), (num, k)


# --- bugs ---
BUGS = [
    {
        "replace": "        while k and stack and stack[-1] > d:",
        "with":    "        while k and stack and stack[-1] >= d:",
        "fix": "pop only a STRICTLY bigger top; popping an equal digit wastes a deletion that a later bigger digit needed",
        "why": "'112' with k=1 pops the first 1 for the second 1 and keeps '12' instead of deleting the 2 to get '11'.",
        "decoys": [
            {"line": "        stack.append(d)", "change": "should append int(d)"},
            {"line": "            k -= 1", "change": "should come after the log of the pop, i.e. k is decremented too early"},
            {"line": "    stack = []", "change": "should start as ['0']"},
        ],
    },
    {
        "replace": "    stack = stack[:len(stack) - k]",
        "with":    "    stack = stack[:-k]",
        "fix": "slice with an explicit end: stack[:-0] is stack[:0], the empty list, when no deletions remain",
        "why": "'1432219' uses all three deletions inside the loop, so k is 0 at the end and the whole stack is thrown away: '0' instead of '1219'.",
        "decoys": [
            {"line": "    for d in num:", "change": "should iterate reversed(num)"},
            {"line": "            popped = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "        while k and stack and stack[-1] > d:", "change": "should be < d"},
        ],
    },
    {
        "replace": "    return \"\".join(stack).lstrip(\"0\") or \"0\"",
        "with":    "    return \"\".join(stack).lstrip(\"0\")",
        "fix": "an empty result (every digit removed or only zeros left) must read '0'",
        "why": "'10' with k=2 and '10001' with k=1 end with an empty string after stripping instead of '0' and '1'; the first returns '' instead of '0'.",
        "decoys": [
            {"line": "            k -= 1", "change": "should be k += 1"},
            {"line": "    stack = stack[:len(stack) - k]", "change": "should be stack[k:]"},
            {"line": "        stack.append(d)", "change": "should only push when k is 0"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
