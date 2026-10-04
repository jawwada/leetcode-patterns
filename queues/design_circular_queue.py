"""
Design Circular Queue (LeetCode 622)  — Medium
Pattern: Ring buffer (circular array with head and count)

Problem
-------
Implement MyCircularQueue(k), a bounded FIFO of capacity k with enQueue(x) -> bool,
deQueue() -> bool, Front() / Rear() -> int (-1 if empty), isEmpty(), isFull().
Example: k = 3; enQueue 1, 2, 3 -> True; enQueue(4) -> False; Rear() -> 3; isFull() -> True;
deQueue() -> True; enQueue(4) -> True; Rear() -> 4.

Brute force
-----------
Keep a Python list: append to enqueue, pop(0) to dequeue, compare len to k for full. Correct,
but pop(0) shifts every remaining element one slot left: O(k) per dequeue. The wasted work is
physically moving k-1 values just to change which one counts as "first".

From brute force to optimal
---------------------------
The only thing a dequeue really changes is where the front is, so move an index instead of the
data. Keep a fixed array of size k, a `head` index and a `count`. The tail slot is derived:
(head + count) % k. Enqueue writes there; dequeue advances head = (head + 1) % k. The modulo
lets both ends wrap from slot k-1 back to slot 0, so freed slots at the start are reused and
nothing ever shifts. Storing count (instead of head and tail) makes empty (count == 0) and full
(count == k) unambiguous.

Intuition
---------
Bend the array into a ring. The queue is an arc of `count` consecutive slots starting at head;
enqueue extends the arc clockwise, dequeue trims it from its start. The arc can cross the seam
between slot k-1 and slot 0 and nobody notices because every index goes through % k.

Geometric view
--------------
A clock face with k positions. The occupied arc runs from head clockwise for count steps.
Both ends only ever move clockwise, chasing each other around the dial; full means the arc
covers the whole dial, empty means it has length zero.

Steps
-----
1. buf = [0] * k; head = 0; count = 0.
2. enQueue(x): if full return False; buf[(head + count) % k] = x; count += 1.
3. deQueue(): if empty return False; head = (head + 1) % k; count -= 1.
4. Front(): -1 if empty else buf[head].  Rear(): -1 if empty else buf[(head + count - 1) % k].
5. isEmpty(): count == 0.  isFull(): count == k.

Complexity: O(1) time per op, O(k) space — only index arithmetic, no shifting.
Pitfalls: head == tail is ambiguous (empty or full?) unless you keep count or waste a slot;
          Rear computed as tail - 1 without % k goes to -1 (Python hides this by indexing
          from the end, other languages crash); forgetting -1 on empty Front/Rear.
"""
import random


class MyCircularQueue:
    def __init__(self, k: int):
        self.buf = [0] * k
        self.head = 0
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.buf[(self.head + self.count) % len(self.buf)] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % len(self.buf)
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.buf[self.head]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self.buf[(self.head + self.count - 1) % len(self.buf)]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == len(self.buf)


class BruteForce:
    """Python list; dequeue is pop(0), which shifts every remaining value, O(k)."""

    def __init__(self, k: int):
        self.k = k
        self.items = []

    def enQueue(self, value: int) -> bool:
        if len(self.items) == self.k:
            return False
        self.items.append(value)
        return True

    def deQueue(self) -> bool:
        if not self.items:
            return False
        self.items.pop(0)
        return True

    def Front(self) -> int:
        return self.items[0] if self.items else -1

    def Rear(self) -> int:
        return self.items[-1] if self.items else -1

    def isEmpty(self) -> bool:
        return not self.items

    def isFull(self) -> bool:
        return len(self.items) == self.k


if __name__ == "__main__":
    q = MyCircularQueue(3)
    assert q.enQueue(1) and q.enQueue(2) and q.enQueue(3)
    assert q.enQueue(4) is False
    assert q.Rear() == 3
    assert q.isFull() is True
    assert q.deQueue() is True
    assert q.enQueue(4) is True          # wraps into slot 0
    assert q.Rear() == 4 and q.Front() == 2

    e = MyCircularQueue(1)               # edge: capacity 1, empty reads
    assert e.Front() == -1 and e.Rear() == -1 and e.deQueue() is False
    assert e.enQueue(5) and e.isFull() and e.Rear() == 5

    random.seed(622)
    ops = ["enQueue", "enQueue", "deQueue", "Front", "Rear", "isEmpty", "isFull"]
    for k in (1, 2, 3, 5, 8):
        fast, slow = MyCircularQueue(k), BruteForce(k)
        for _ in range(500):
            op = random.choice(ops)
            args = (random.randint(0, 99),) if op == "enQueue" else ()
            assert getattr(fast, op)(*args) == getattr(slow, op)(*args)
    print("ok")
