"""
Implement Stack using Queues (LeetCode 225)  — Easy
Pattern: Rotate a queue to make a stack

Problem
-------
Build a LIFO stack (push, pop, top, empty) using only queue operations: push to back,
pop/peek from front, size, is-empty.
Example: push(1); push(2); top() -> 2; pop() -> 2; empty() -> False.

Brute force
-----------
Keep two queues. push appends to q1. pop/top move the first n-1 items of q1 into q2, read the
last one (pop removes it, top puts it back too), then swap q1 and q2. O(1) push, O(n) pop and
O(n) top, O(n) space. The wasted work is re-shuffling the whole queue on every read: top()
called twice in a row moves n-1 items twice to find the same element.

From brute force to optimal
---------------------------
Reads happen at the front of a queue, so the cheapest design keeps the newest element at the
front at all times. Then pop and top are O(1) and all the cost is paid once, at push time.
Observation: appending x and then rotating the queue n-1 times (popleft + append) brings x to
the front while keeping the older elements in newest-to-oldest order behind it. One queue is
enough; the second queue of the brute force was only a parking lot for the rotation.

Intuition
---------
A queue is a ring you can turn. After each push, turn the ring until the new element sits at
the exit. The queue then always reads newest -> oldest from front to back, which is exactly a
stack read from top to bottom.

Geometric view
--------------
Picture the queue as a conveyor belt. A new item lands at the back; then every older item
rides off the front and re-joins at the back, one after another, until the new item is at the
front. The belt has rotated by n-1 positions; the relative order of the old items is unchanged.

Steps
-----
1. q = deque().
2. push(x): q.append(x); repeat len(q)-1 times: q.append(q.popleft()).
3. pop(): q.popleft().
4. top(): q[0].
5. empty(): not q.

Complexity: O(n) push, O(1) pop/top/empty, O(n) space — each push rotates past n-1 items.
Pitfalls: rotating n times instead of n-1 (puts x back at the end); using deque.pop() or
          index -1, which are not queue operations.
"""
import random
from collections import deque


class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q) - 1):    # rotate older items behind x
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q


class BruteForce:
    """Two queues; every pop/top moves n-1 items across to reach the newest, O(n)."""

    def __init__(self):
        self.q1, self.q2 = deque(), deque()

    def push(self, x: int) -> None:
        self.q1.append(x)

    def _drain(self) -> int:
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        last = self.q1.popleft()
        self.q1, self.q2 = self.q2, self.q1
        return last

    def pop(self) -> int:
        return self._drain()

    def top(self) -> int:
        last = self._drain()
        self.q1.append(last)
        return last

    def empty(self) -> bool:
        return not self.q1


if __name__ == "__main__":
    s = MyStack()
    s.push(1)
    s.push(2)
    assert s.top() == 2
    assert s.pop() == 2
    assert s.empty() is False
    assert s.pop() == 1 and s.empty() is True

    e = MyStack()                       # edge: single element round trip
    e.push(7); assert e.top() == 7 and e.pop() == 7 and e.empty()

    random.seed(225)
    for _ in range(50):
        fast, slow = MyStack(), BruteForce()
        for _ in range(200):
            op = random.choice(["push", "push", "pop", "top", "empty"])
            if op == "push":
                v = random.randint(-50, 50)
                fast.push(v); slow.push(v)
            elif op == "empty" or slow.empty():
                assert fast.empty() == slow.empty()
            else:
                assert getattr(fast, op)() == getattr(slow, op)()
    print("ok")
