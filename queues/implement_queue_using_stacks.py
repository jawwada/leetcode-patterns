"""
Implement Queue using Stacks (LeetCode 232)  — Easy
Pattern: Two stacks make a queue (lazy transfer)

Problem
-------
Build a FIFO queue (push, pop, peek, empty) using only stack operations: push to top,
pop/peek from top, size, is-empty.
Example: push(1); push(2); peek() -> 1; pop() -> 1; empty() -> False.

Brute force
-----------
Keep everything in one stack `main` with the oldest element on top. To push x, pour all of
main into a helper stack, push x, and pour everything back. O(n) per push, O(1) pop/peek,
O(n) space. The wasted work is moving the same elements back and forth on every push: their
relative order never changes, yet each push touches all of them twice.

From brute force to optimal
---------------------------
Pouring a stack into another reverses it, and reversing twice is a no-op, so the brute force
undoes its own work. Instead keep two stacks with fixed roles: `inbox` takes pushes (newest on
top) and `outbox` serves pops (oldest on top). Only when outbox is empty do we pour inbox into
it once. Invariant: every element in outbox is older than every element in inbox, so the top
of outbox is always the queue's front. Each element is pushed and popped at most twice in its
life, giving amortised O(1) per operation.

Intuition
---------
One reversal turns LIFO into FIFO. Do that reversal once per element, as late as possible, and
never undo it. The outbox is a pre-reversed batch of the oldest elements; new arrivals wait in
the inbox until the batch runs out.

Geometric view
--------------
Two vertical tubes side by side. Elements drop into the left tube; when the right tube is empty
the whole left tube is flipped upside down into it, putting the oldest element on top. Each
element crosses the gap between the tubes exactly once.

Steps
-----
1. inbox = [], outbox = [].
2. push(x): inbox.append(x).
3. peek(): if outbox is empty, move every item from inbox to outbox (pop/append); return outbox[-1].
4. pop(): peek() to ensure outbox is filled, then return outbox.pop().
5. empty(): both stacks are empty.

Complexity: O(1) amortised time per op, O(n) space — each element moves inbox -> outbox once.
Pitfalls: transferring when outbox is NOT empty (breaks order); forgetting to check both stacks
          in empty(); quoting worst-case O(1) (a single pop can be O(n)).
"""
import random


class MyQueue:
    def __init__(self):
        self.inbox = []     # newest on top
        self.outbox = []    # oldest on top

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def pop(self) -> int:
        self.peek()
        return self.outbox.pop()

    def peek(self) -> int:
        if not self.outbox:                 # transfer only when the outbox runs dry
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox


class BruteForce:
    """One stack with the oldest on top; every push pours everything out and back, O(n)."""

    def __init__(self):
        self.main = []

    def push(self, x: int) -> None:
        helper = []
        while self.main:
            helper.append(self.main.pop())
        self.main.append(x)
        while helper:
            self.main.append(helper.pop())

    def pop(self) -> int:
        return self.main.pop()

    def peek(self) -> int:
        return self.main[-1]

    def empty(self) -> bool:
        return not self.main


if __name__ == "__main__":
    q = MyQueue()
    q.push(1)
    q.push(2)
    assert q.peek() == 1
    assert q.pop() == 1
    assert q.empty() is False
    assert q.pop() == 2 and q.empty() is True

    e = MyQueue()                       # edge: interleave pushes with a non-empty outbox
    e.push(1); e.push(2); assert e.pop() == 1
    e.push(3); assert e.pop() == 2 and e.pop() == 3

    random.seed(232)
    for _ in range(50):
        fast, slow = MyQueue(), BruteForce()
        for _ in range(200):
            op = random.choice(["push", "push", "pop", "peek", "empty"])
            if op == "push":
                v = random.randint(-50, 50)
                fast.push(v); slow.push(v)
            elif op == "empty" or slow.empty():
                assert fast.empty() == slow.empty()
            else:
                assert getattr(fast, op)() == getattr(slow, op)()
    print("ok")
