"""
Moving Average from Data Stream (LeetCode 346) - Easy
Chapter: design
Pattern: Sliding window queue with running sum

Implement MovingAverage(size) with next(val) -> the average of the last size values seen so far,
or of all values while fewer than size have arrived.
Example: size 3; next(1) -> 1.0; next(10) -> 5.5; next(3) -> 4.667; next(5) -> 6.0.
"""
from collections import deque   # popleft is O(1)


# --- brute force ---
class BruteForce:
    """Keep the whole stream; re-sum the last size values on every call. O(size) per next."""

    def __init__(self, size):
        self.size = size
        self.seen = []

    def next(self, val):
        self.seen.append(val)
        start = max(0, len(self.seen) - self.size)
        tail = self.seen[start:]          # the last size values (fewer while the stream is short)
        total = 0
        for x in tail:
            total += x                    # re-summed from scratch every time
        return total / len(tail)


# --- optimal ---
class MovingAverage:
    """A deque holds only the window; a running total avoids re-summing. O(1) per next."""

    def __init__(self, size):
        self.size = size
        self.window = deque()
        self.total = 0

    def next(self, val):
        self.window.append(val)
        self.total += val
        if len(self.window) > self.size:
            oldest = self.window.popleft()    # the value that just slid out of the window
            self.total -= oldest
        return self.total / len(self.window)


# --- try the brute force ---
m = BruteForce(3)
print(m.next(1))                 # -> 1.0
print(m.next(10))                # -> 5.5
print(round(m.next(3), 3))       # -> 4.667
print(m.next(5))                 # -> 6.0


# --- try the optimal ---
m = MovingAverage(3)
print(m.next(1))                 # -> 1.0
print(m.next(10))                # -> 5.5
print(round(m.next(3), 3))       # -> 4.667
print(m.next(5))                 # -> 6.0
