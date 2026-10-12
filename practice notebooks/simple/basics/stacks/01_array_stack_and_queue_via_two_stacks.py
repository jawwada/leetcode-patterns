"""
Array Stack and Queue via Two Stacks (basics: stacks)
Build a stack on a Python list, then a first-in first-out queue out of two such stacks.
  enqueue 1, enqueue 2, peek, dequeue, enqueue 3, dequeue, dequeue, empty  ->  1, 1, 2, 3, True

Idea: a list is a stack whose top is its end. Pouring one stack into another reverses it,
      so the oldest item lands on top. Refill the outbox only when it is empty: every item
      is moved once, so each queue operation is amortized O(1).

Pseudocode:
  Stack:      push = append, pop = pop from the end, peek = items[-1], empty = no items
  enqueue(x): inbox.push(x)
  _refill():  if outbox is empty: pop every inbox item and push it onto outbox
  dequeue():  _refill(); return outbox.pop()
  peek():     _refill(); return outbox.peek()
  empty():    inbox is empty and outbox is empty

Time O(1) per stack operation, amortized O(1) per queue operation; space O(n).
"""


class Stack:
    def __init__(self):
        self.items = []                  # the end of the list is the top

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
        self.inbox = Stack()             # enqueue pushes here
        self.outbox = Stack()            # dequeue pops here, oldest on top

    def enqueue(self, x):
        self.inbox.push(x)

    def _refill(self):
        if self.outbox.empty():          # only when outbox is empty
            while not self.inbox.empty():
                self.outbox.push(self.inbox.pop())  # pouring reverses the order

    def dequeue(self):
        self._refill()
        return self.outbox.pop()

    def peek(self):
        self._refill()
        return self.outbox.peek()

    def empty(self):
        return self.inbox.empty() and self.outbox.empty()  # both stacks


if __name__ == "__main__":
    s = Stack()
    s.push(1); s.push(2)
    print(s.pop(), s.peek())             # 2 1
    q = Queue()
    q.enqueue(1); q.enqueue(2)
    print(q.peek(), q.dequeue())         # 1 1
    q.enqueue(3)
    print(q.dequeue(), q.dequeue())      # 2 3
    print(q.empty())                     # True
