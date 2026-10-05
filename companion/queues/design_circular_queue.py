"""
Design Circular Queue (LeetCode 622) - Medium
Chapter: queues
Pattern: Ring buffer (circular array with head and count)

Implement MyCircularQueue(k), a bounded first-in-first-out queue of capacity k with
en_queue(x) and de_queue() returning success, front() and rear() returning -1 when empty,
is_empty() and is_full().
Example: k = 3; en_queue 1, 2, 3 -> True; en_queue(4) -> False; rear() -> 3; is_full() -> True;
de_queue() -> True; en_queue(4) -> True; rear() -> 4.
"""


# --- brute force ---
class BruteForce:
    """A Python list; de_queue is pop(0), which shifts every remaining value. de_queue O(k)."""

    def __init__(self, k):
        self.capacity = k
        self.items = []

    def en_queue(self, value):
        if len(self.items) == self.capacity:
            return False
        self.items.append(value)
        return True

    def de_queue(self):
        if len(self.items) == 0:
            return False
        self.items.pop(0)                           # shifts every element one slot left
        return True

    def front(self):
        if len(self.items) == 0:
            return -1
        return self.items[0]

    def rear(self):
        if len(self.items) == 0:
            return -1
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def is_full(self):
        return len(self.items) == self.capacity


# --- optimal ---
class MyCircularQueue:
    """Fixed array plus a head index and a count; both ends wrap with modulo. All O(1)."""

    def __init__(self, k):
        self.buf = [0] * k
        self.head = 0           # slot of the front element
        self.count = 0          # how many slots are in use

    def en_queue(self, value):
        if self.is_full():
            return False
        tail = (self.head + self.count) % len(self.buf)   # wraps from slot k-1 back to slot 0
        self.buf[tail] = value
        self.count += 1
        return True

    def de_queue(self):
        if self.is_empty():
            return False
        self.head = (self.head + 1) % len(self.buf)       # move the index, not the data
        self.count -= 1
        return True

    def front(self):
        if self.is_empty():
            return -1
        return self.buf[self.head]

    def rear(self):
        if self.is_empty():
            return -1
        return self.buf[(self.head + self.count - 1) % len(self.buf)]

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == len(self.buf)


# --- try the brute force ---
q = BruteForce(3)
print(q.en_queue(1))   # -> True
print(q.en_queue(2))   # -> True
print(q.en_queue(3))   # -> True
print(q.en_queue(4))   # -> False (full)
print(q.rear())        # -> 3
print(q.is_full())     # -> True
print(q.de_queue())    # -> True
print(q.en_queue(4))   # -> True (reuses the freed slot)
print(q.rear())        # -> 4
print(q.front())       # -> 2
e = BruteForce(1)
print(e.front())       # -> -1
print(e.de_queue())    # -> False
print(e.en_queue(5))   # -> True
print(e.rear())        # -> 5


# --- try the optimal ---
q = MyCircularQueue(3)
print(q.en_queue(1))   # -> True
print(q.en_queue(2))   # -> True
print(q.en_queue(3))   # -> True
print(q.en_queue(4))   # -> False (full)
print(q.rear())        # -> 3
print(q.is_full())     # -> True
print(q.de_queue())    # -> True
print(q.en_queue(4))   # -> True (reuses the freed slot)
print(q.rear())        # -> 4
print(q.front())       # -> 2
e = MyCircularQueue(1)
print(e.front())       # -> -1
print(e.de_queue())    # -> False
print(e.en_queue(5))   # -> True
print(e.rear())        # -> 5
