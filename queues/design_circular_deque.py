"""
Design Circular Deque (LeetCode 641)  — Medium
Pattern: Ring buffer (circular array with head and count)

Problem
-------
Implement MyCircularDeque(k), a bounded double-ended queue of capacity k with insertFront,
insertLast, deleteFront, deleteLast (each -> bool), getFront / getRear (-1 if empty), isEmpty,
isFull. Example: k = 3; insertLast(1), insertLast(2) -> True; insertFront(3) -> True;
insertFront(4) -> False; getRear() -> 2; isFull() -> True; deleteLast() -> True;
insertFront(4) -> True; getFront() -> 4.

Brute force
-----------
A Python list: insert(0, x) / pop(0) for the front, append / pop() for the back. Correct, but
every front operation shifts all k values one slot: O(k) per front insert/delete. The wasted
work is moving the data when only the label "this slot is the front" needs to change.

From brute force to optimal
---------------------------
Same fix as the circular queue (622), now applied at both ends. Keep a fixed array, a `head`
index and a `count`; the rear slot is (head + count - 1) % k. insertLast writes at
(head + count) % k; deleteLast just decrements count. insertFront moves head one step
counter-clockwise, head = (head - 1) % k, and writes there; deleteFront moves head clockwise.
Nothing shifts, every operation is two or three integer updates, and count keeps empty vs full
unambiguous.

Intuition
---------
The deque is an arc on a ring. The front end can grow or shrink counter-clockwise / clockwise
by moving head; the back end grows or shrinks by changing count. Modulo arithmetic makes
"one slot before index 0" equal to index k-1, so the arc wraps freely in either direction.

Geometric view
--------------
A clock face with k positions and an arc of length count starting at head. insertFront pulls
the arc's start one tick backwards; insertLast pushes its end one tick forwards. Both ends can
cross the 0 / k-1 seam. Full: the arc closes into a circle.

Steps
-----
1. buf = [0] * k; head = 0; count = 0.
2. insertFront(x): if full False; head = (head - 1) % k; buf[head] = x; count += 1.
3. insertLast(x): if full False; buf[(head + count) % k] = x; count += 1.
4. deleteFront(): if empty False; head = (head + 1) % k; count -= 1.
5. deleteLast(): if empty False; count -= 1.
6. getFront: buf[head]; getRear: buf[(head + count - 1) % k]; both -1 when empty.

Complexity: O(1) time per op, O(k) space — each op is constant index arithmetic.
Pitfalls: (head - 1) % k is fine in Python but negative in C++/Java (add k first);
          writing before moving head on insertFront; head == tail ambiguity without count.
"""
import random


class MyCircularDeque:
    def __init__(self, k: int):
        self.buf = [0] * k
        self.head = 0
        self.count = 0

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False
        self.head = (self.head - 1) % len(self.buf)     # step back, then write
        self.buf[self.head] = value
        self.count += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False
        self.buf[(self.head + self.count) % len(self.buf)] = value
        self.count += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % len(self.buf)
        self.count -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False
        self.count -= 1
        return True

    def getFront(self) -> int:
        return -1 if self.isEmpty() else self.buf[self.head]

    def getRear(self) -> int:
        if self.isEmpty():
            return -1
        return self.buf[(self.head + self.count - 1) % len(self.buf)]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == len(self.buf)


class BruteForce:
    """Python list; front ops are insert(0)/pop(0), which shift every value, O(k)."""

    def __init__(self, k: int):
        self.k = k
        self.items = []

    def insertFront(self, value: int) -> bool:
        if len(self.items) == self.k:
            return False
        self.items.insert(0, value)
        return True

    def insertLast(self, value: int) -> bool:
        if len(self.items) == self.k:
            return False
        self.items.append(value)
        return True

    def deleteFront(self) -> bool:
        if not self.items:
            return False
        self.items.pop(0)
        return True

    def deleteLast(self) -> bool:
        if not self.items:
            return False
        self.items.pop()
        return True

    def getFront(self) -> int:
        return self.items[0] if self.items else -1

    def getRear(self) -> int:
        return self.items[-1] if self.items else -1

    def isEmpty(self) -> bool:
        return not self.items

    def isFull(self) -> bool:
        return len(self.items) == self.k


if __name__ == "__main__":
    d = MyCircularDeque(3)
    assert d.insertLast(1) and d.insertLast(2)
    assert d.insertFront(3) is True      # head wraps to slot 2
    assert d.insertFront(4) is False
    assert d.getRear() == 2
    assert d.isFull() is True
    assert d.deleteLast() is True
    assert d.insertFront(4) is True
    assert d.getFront() == 4

    e = MyCircularDeque(1)               # edge: capacity 1, empty reads and deletes
    assert e.getFront() == -1 and e.getRear() == -1
    assert e.deleteFront() is False and e.deleteLast() is False
    assert e.insertFront(9) and e.getRear() == 9 and e.deleteLast() and e.isEmpty()

    random.seed(641)
    ops = ["insertFront", "insertLast", "deleteFront", "deleteLast",
           "getFront", "getRear", "isEmpty", "isFull"]
    for k in (1, 2, 3, 5, 8):
        fast, slow = MyCircularDeque(k), BruteForce(k)
        for _ in range(500):
            op = random.choice(ops)
            args = (random.randint(0, 99),) if op.startswith("insert") else ()
            assert getattr(fast, op)(*args) == getattr(slow, op)(*args)
    print("ok")
