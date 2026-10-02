"""
Moving Average from Data Stream (LeetCode 346)  — Easy
Pattern: Sliding window queue with running sum

Problem
-------
Implement MovingAverage(size) with next(val) -> the average of the last `size` values seen so
far (or of all values if fewer than size have arrived).
Example: size 3; next(1)->1.0; next(10)->5.5; next(3)->4.667; next(5)->6.0 (= (10+3+5)/3).

Brute force
-----------
Append every value to a list and, on each call, sum the last `size` entries and divide.
O(size) per call and O(n) space for the whole stream. The wasted work is re-adding size - 1
numbers that were already summed last time, and keeping values that have left the window and
can never influence an answer again.

From brute force to optimal
---------------------------
Consecutive windows overlap in all but two elements: the newest enters and the oldest leaves.
So maintain the window's sum incrementally: total += new; if the window exceeds size,
total -= the element that falls out. A deque gives O(1) append at the back and pop at the
front, and the division uses the current window length (which is < size only during warm-up).
The tracker remembers at most `size` values plus one running total; everything that has
slid out of the window is forgotten immediately.

Intuition
---------
A moving average is a sum that slides. Sliding means one value in, one value out, so update the
sum by exactly those two numbers instead of recomputing it. The queue exists only so we know
which value is the oldest.

Geometric view
--------------
stream: 1 10 3 5 8        size = 3
         [1 10 3]          total 14 -> 14/3
           [10 3 5]        1 leaves, 5 enters: total 14 - 1 + 5 = 18 -> 6.0
              [3 5 8]      10 leaves, 8 enters: total 18 - 10 + 8 = 16 -> 5.33
The bracket slides right one slot per call; both edges move together.

Steps
-----
1. window = deque(); total = 0.
2. next(val): append val; total += val.
3. If len(window) > size: total -= window.popleft().
4. Return total / len(window).

Complexity: O(1) time per call, O(size) space — one append, at most one pop, one division.
Pitfalls: dividing by size during warm-up (must divide by the current length); popping before
          appending with size 1; integer division.
"""
import random
from collections import deque


class MovingAverage:
    def __init__(self, size: int):
        self.size = size
        self.window = deque()
        self.total = 0

    def next(self, val: int) -> float:
        self.window.append(val)
        self.total += val
        if len(self.window) > self.size:
            self.total -= self.window.popleft()    # drop the value that slid out
        return self.total / len(self.window)


class BruteForce:
    """Keep the whole stream; re-sum the last `size` values on each call, O(size)."""

    def __init__(self, size: int):
        self.size = size
        self.seen = []

    def next(self, val: int) -> float:
        self.seen.append(val)
        tail = self.seen[-self.size:]
        return sum(tail) / len(tail)


if __name__ == "__main__":
    m = MovingAverage(3)
    assert m.next(1) == 1.0
    assert m.next(10) == 5.5
    assert abs(m.next(3) - 14 / 3) < 1e-9
    assert m.next(5) == 6.0

    e = MovingAverage(1)                       # edge: window of one is always the latest value
    assert e.next(4) == 4.0 and e.next(-2) == -2.0

    random.seed(11)
    for size in (1, 2, 5):
        fast, slow = MovingAverage(size), BruteForce(size)
        for _ in range(500):
            v = random.randint(-100, 100)
            assert abs(fast.next(v) - slow.next(v)) < 1e-9
        assert len(fast.window) <= size
    print("ok")
