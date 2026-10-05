"""
Min Stack (LeetCode 155) - Medium
Area: stack
Key operations: push (value, running min), pop the pair, top reads the value, getMin reads the stored min

Design a stack with push, pop, top and getMin, each in O(1). Operations are given as a list such as
("push", -2), ("pop",), ("top",), ("getMin",); return the outputs of top and getMin in order.
Example: push(-2), push(0), push(-3), getMin, pop, top, getMin -> [-3, 0, -2]
"""
import sys
from typing import List, Tuple

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
def run(stack, ops: List[Tuple]) -> List[int]:
    """Apply the operations in order and collect what top and getMin return."""
    out = []
    for op in ops:
        result = getattr(stack, op[0])(*op[1:])
        if op[0] in ("top", "getMin"):
            out.append(result)
    return out


# --- brute force ---
class BruteStack:
    """Plain list; getMin scans everything. O(n) per getMin, and the scan is wasted work:
    the minimum of the entries below the top never changes while they sit there."""
    def __init__(self):
        self.items = []

    def push(self, val: int) -> None:
        self.items.append(val)

    def pop(self) -> None:
        self.items.pop()

    def top(self) -> int:
        return self.items[-1]

    def getMin(self) -> int:
        return min(self.items)


def brute_force(ops: List[Tuple]) -> List[int]:
    return run(BruteStack(), ops)


# --- optimal ---
class MinStack:
    """Each entry stores (value, min of everything at or below it). The stack only changes at the
    top, so the stored mins below never go stale and pop restores the old min for free. All O(1)."""
    def __init__(self):
        self.items = []  # (value, current_min) pairs; the top is items[-1]

    def push(self, val: int) -> None:
        current_min = min(val, self.items[-1][1]) if self.items else val
        self.items.append((val, current_min))
        log(f"push {val:3d}   top->bottom  {' | '.join(f'{v} (min {m})' for v, m in reversed(self.items))}")

    def pop(self) -> None:
        val, _ = self.items.pop()
        log(f"pop  {val:3d}   top->bottom  {' | '.join(f'{v} (min {m})' for v, m in reversed(self.items)) or 'empty'}")

    def top(self) -> int:
        log(f"top       -> {self.items[-1][0]}   (value of the top pair)")
        return self.items[-1][0]

    def getMin(self) -> int:
        log(f"getMin    -> {self.items[-1][1]}   (stored min of the top pair)")
        return self.items[-1][1]


def solve(ops: List[Tuple]) -> List[int]:
    return run(MinStack(), ops)


# --- demo ---
def demo():
    return solve([("push", -2), ("push", 0), ("push", -3), ("getMin",), ("pop",), ("top",), ("getMin",)])


# --- tests ---
def tests():
    assert solve([("push", -2), ("push", 0), ("push", -3), ("getMin",), ("pop",), ("top",), ("getMin",)]) == [-3, 0, -2]
    assert solve([("push", 5), ("top",), ("getMin",)]) == [5, 5]
    assert solve([("push", 1), ("push", 1), ("push", 2), ("pop",), ("pop",), ("getMin",)]) == [1]  # duplicate min survives a pop
    assert solve([("push", 3), ("push", 1), ("push", 2), ("getMin",), ("pop",), ("pop",), ("getMin",)]) == [1, 3]
    assert solve([("push", 2), ("push", 1), ("pop",), ("push", 5), ("getMin",), ("top",)]) == [2, 5]
    assert solve([]) == []
    import random
    random.seed(1)
    for _ in range(200):
        ops, size = [], 0
        for _ in range(random.randint(1, 12)):
            choice = random.choice(["push", "push", "pop", "top", "getMin"]) if size else "push"
            if choice == "push":
                ops.append(("push", random.randint(-5, 5)))
                size += 1
            elif choice == "pop":
                ops.append(("pop",))
                size -= 1
            else:
                ops.append((choice,))
        assert solve(ops) == brute_force(ops), ops


# --- bugs ---
BUGS = [
    {
        "replace": "        current_min = min(val, self.items[-1][1]) if self.items else val",
        "with":    "        current_min = min(val, self.items[-1][0]) if self.items else val",
        "fix": "compare with the stored min of the top pair, items[-1][1], not with its value",
        "why": "Comparing with the top's value forgets smaller entries deeper down: push 1, push 5, push 3 stores min 3 on top, so getMin returns 3 instead of 1.",
        "decoys": [
            {"line": "        self.items.append((val, current_min))", "change": "should append (current_min, val)"},
            {"line": "        return self.items[-1][0]", "change": "should return self.items[0][0]"},
            {"line": "        val, _ = self.items.pop()", "change": "should only pop when val == current min"},
        ],
    },
    {
        "replace": "        return self.items[-1][1]",
        "with":    "        return self.items[-1][0]",
        "fix": "getMin reads the stored min, the second field: self.items[-1][1]",
        "why": "Reading the first field returns the top value instead of the minimum: push 2, push 5, getMin gives 5 instead of 2.",
        "decoys": [
            {"line": "        current_min = min(val, self.items[-1][1]) if self.items else val", "change": "should be min(val, self.items[0][1])"},
            {"line": "        self.items.append((val, current_min))", "change": "should append only when val <= current_min"},
            {"line": "        self.items = []  # (value, current_min) pairs; the top is items[-1]", "change": "should hold two separate lists"},
        ],
    },
    {
        "replace": "        val, _ = self.items.pop()",
        "with":    "        val, _ = self.items.pop(0)",
        "fix": "pop the top: self.items.pop()",
        "why": "pop(0) removes the bottom entry, so after push 1, push 2, pop the top is still 2 instead of 1 and the stored mins above it are now wrong.",
        "decoys": [
            {"line": "        return self.items[-1][0]", "change": "should return self.items[-1][1]"},
            {"line": "        self.items.append((val, current_min))", "change": "should be insert(0, ...)"},
            {"line": "    return run(MinStack(), ops)", "change": "should return run(MinStack(), ops)[::-1]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
