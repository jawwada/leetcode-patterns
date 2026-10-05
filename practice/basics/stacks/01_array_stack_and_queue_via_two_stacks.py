"""
Array Stack and Queue via Two Stacks - Basics
Area: stacks
Key operations: push, pop, peek, drain inbox into outbox only when outbox is empty

A Stack on a Python list (the end is the top) and a Queue made of two stacks: enqueue pushes on
'inbox'; dequeue and peek take from 'outbox', refilling it by draining inbox only when it is empty.
Every element crosses once, so n operations cost O(n) in total (amortized O(1) each).
solve(ops) runs ops like "enq 3", "deq", "peek", "empty" and returns the outputs of the last three.
Example: ["enq 1", "enq 2", "peek", "deq", "enq 3", "deq", "deq", "empty"] -> [1, 1, 2, 3, True]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(ops: List[str]) -> list:
    """Queue as a plain list: pop(0) shifts every remaining element, O(n) per dequeue."""
    q, out = [], []
    for op in ops:
        if op.startswith("enq"):
            q.append(int(op.split()[1]))
        elif op == "deq":
            out.append(q.pop(0))
        elif op == "peek":
            out.append(q[0])
        else:
            out.append(not q)
    return out


# --- optimal ---
class Stack:
    def __init__(self):
        self.items = []  # the end of the list is the top

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def empty(self):
        return not self.items


class Queue:
    def __init__(self):
        self.inbox, self.outbox = Stack(), Stack()  # enqueue into inbox, dequeue from outbox

    def enqueue(self, x):
        self.inbox.push(x)
        log(f"    enq {x}: inbox top->bottom {self.inbox.items[::-1]} | outbox top->bottom {self.outbox.items[::-1]}")

    def _refill(self):
        if self.outbox.empty():
            while not self.inbox.empty():
                self.outbox.push(self.inbox.pop())
            log(f"    outbox empty -> drain inbox: outbox top->bottom {self.outbox.items[::-1]}")

    def dequeue(self):
        self._refill()
        x = self.outbox.pop()
        log(f"    deq -> {x}: inbox top->bottom {self.inbox.items[::-1]} | outbox top->bottom {self.outbox.items[::-1]}")
        return x

    def peek(self):
        self._refill()
        return self.outbox.peek()

    def empty(self):
        return self.inbox.empty() and self.outbox.empty()


def solve(ops: List[str]) -> list:
    """Drive a two-stack Queue with "enq x" / "deq" / "peek" / "empty"; amortized O(1) per op."""
    q, out = Queue(), []
    for op in ops:
        log(f"op {op}")
        if op.startswith("enq"):
            q.enqueue(int(op.split()[1]))
        else:
            out.append({"deq": q.dequeue, "peek": q.peek, "empty": q.empty}[op]())
            log(f"    output {out[-1]}")
    return out


# --- demo ---
def demo():
    return solve(["enq 1", "enq 2", "peek", "deq", "enq 3", "deq", "deq", "empty"])


# --- tests ---
def tests():
    assert solve(["enq 1", "enq 2", "peek", "deq", "enq 3", "deq", "deq", "empty"]) == [1, 1, 2, 3, True]
    assert solve([]) == []
    assert solve(["empty"]) == [True]
    assert solve(["enq 5", "empty", "peek", "deq", "empty"]) == [False, 5, 5, True]
    assert solve(["enq 1", "enq 2", "deq", "enq 3", "deq", "deq"]) == [1, 2, 3]  # refill only when outbox is empty
    st = Stack()
    assert st.empty()
    st.push(1)
    st.push(2)
    assert st.peek() == 2 and not st.empty()
    assert st.pop() == 2 and st.pop() == 1 and st.empty()
    import random
    rng = random.Random(0)
    for _ in range(200):
        ops, size = [], 0
        for _ in range(rng.randint(0, 12)):
            r = rng.random()
            if size == 0 or r < 0.5:
                ops.append(f"enq {rng.randint(0, 9)}")
                size += 1
            elif r < 0.75:
                ops.append("deq")
                size -= 1
            elif r < 0.9:
                ops.append("peek")
            else:
                ops.append("empty")
        assert solve(ops) == brute_force(ops), ops


# --- bugs ---
BUGS = [
    {
        "replace": "        if self.outbox.empty():",
        "with":    "        if not self.inbox.empty():",
        "fix": "drain inbox only when outbox is EMPTY; moving elements onto a non-empty outbox puts newer ones in front of older ones",
        "why": "After enq 1, enq 2, deq, enq 3 the outbox still holds 2; draining 3 on top of it makes the next deq return 3 instead of 2.",
        "decoys": [
            {"line": "        return self.inbox.empty() and self.outbox.empty()", "change": "should be 'or'"},
            {"line": "                self.outbox.push(self.inbox.pop())", "change": "should push self.inbox.peek()"},
            {"line": "        x = self.outbox.pop()", "change": "should pop from inbox"},
        ],
    },
    {
        "replace": "        return self.inbox.empty() and self.outbox.empty()",
        "with":    "        return self.outbox.empty()",
        "fix": "the queue is empty only when BOTH stacks are empty; fresh elements sit in inbox until the first refill",
        "why": "After 'enq 5' nothing has been moved yet, so outbox is empty and the queue wrongly reports empty.",
        "decoys": [
            {"line": "        self.inbox.push(x)", "change": "should push on outbox"},
            {"line": "        return self.items[-1]", "change": "should be self.items[0]"},
            {"line": "            q.enqueue(int(op.split()[1]))", "change": "should enqueue op.split()[1] without int()"},
        ],
    },
    {
        "replace": "        return self.items[-1]",
        "with":    "        return self.items[0]",
        "fix": "the top of an array stack is the END of the list, items[-1]",
        "why": "items[0] is the bottom: after enq 1, enq 2 the outbox list is [2, 1] and peek must return 1, not 2.",
        "decoys": [
            {"line": "        return self.items.pop()", "change": "should be pop(0)"},
            {"line": "        return not self.items", "change": "should be len(self.items) == 0 or"},
            {"line": "        return self.outbox.peek()", "change": "should peek inbox when outbox is empty"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
