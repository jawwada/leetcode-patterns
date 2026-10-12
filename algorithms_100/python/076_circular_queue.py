"""
Circular Queue - Ring Buffer with Head and Count

Design a FIFO queue of fixed capacity on one array whose end wraps around to
its start: enqueue and dequeue return True or False, front and rear return -1
when empty. Capacity 3: enqueue 1, 2, 3, then enqueue 4 -> False (full).
"""


# --- algorithm ---
class CircularQueue:
    def __init__(self, capacity):
        self.items = [0] * capacity
        self.capacity = capacity
        self.head = 0                   # index of the front value
        self.count = 0                  # how many values are stored

    def enqueue(self, value):
        """Write at tail = (head + count) mod capacity. O(1)."""
        if self.is_full():
            return False
        tail = (self.head + self.count) % self.capacity    # wraps to 0
        self.items[tail] = value
        self.count += 1
        return True

    def dequeue(self):
        """Drop the front value by moving head one step, wrapping. O(1)."""
        if self.is_empty():
            return False
        self.head = (self.head + 1) % self.capacity    # old value stays
        self.count -= 1
        return True

    def front(self):
        """The oldest value, or -1 if empty. O(1)."""
        if self.is_empty():
            return -1
        return self.items[self.head]

    def rear(self):
        """The newest value, at (head + count - 1) mod capacity. O(1)."""
        if self.is_empty():
            return -1
        return self.items[(self.head + self.count - 1) % self.capacity]

    def is_empty(self):
        """No values stored. O(1)."""
        return self.count == 0

    def is_full(self):
        """Every slot holds a value. O(1)."""
        return self.count == self.capacity


# --- try it ---
queue = CircularQueue(3)
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(queue.enqueue(4), queue.rear())               # -> False 3
print(queue.dequeue(), queue.enqueue(4))            # -> True True
print(queue.front(), queue.rear(), queue.items)     # -> 2 4 [4, 2, 3]
print(queue.is_full(), queue.head, queue.count)     # -> True 1 3
