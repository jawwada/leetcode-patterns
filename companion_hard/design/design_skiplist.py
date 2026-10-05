"""
Design Skiplist (LeetCode 1206) - Hard
Chapter: design
Pattern: Multi-level sorted linked list with randomised express lanes

Implement a Skiplist with search(target) -> bool, add(num) and erase(num) -> bool, which returns
False if num is absent. Duplicates are allowed and erase removes one copy. All three should run in
O(log n) expected time without any built-in ordered structure.
Example: after add 1, 2, 3, search(0) is False; after add 4, erase(1) is True and then search(1)
is False.
"""
import random


# --- brute force ---
class BruteForce:
    """Sorted Python list; every operation walks and shifts elements. O(n) per operation."""

    def __init__(self):
        self.items = []

    def search(self, target):
        for value in self.items:              # linear scan
            if value == target:
                return True
        return False

    def add(self, num):
        i = 0
        while i < len(self.items) and self.items[i] < num:
            i += 1                            # walk to the insertion point
        self.items.insert(i, num)             # shifts everything after it

    def erase(self, num):
        for i in range(len(self.items)):
            if self.items[i] == num:
                self.items.pop(i)
                return True
        return False


# --- optimal ---
class Node:
    def __init__(self, val, height):
        self.val = val
        self.forward = [None] * height        # forward[i] = the next node on row i


class Skiplist:
    """Rows of sorted lists, each about half as dense as the one below. O(log n) expected."""

    MAX_LEVEL = 16                            # enough rows for about 65k elements

    def __init__(self):
        self.head = Node(None, self.MAX_LEVEL)   # sentinel in front of every row
        self.level = 1                        # rows currently in use
        self.rng = random.Random(1206)        # seeded so every run builds the same structure

    def random_level(self):
        height = 1
        while height < self.MAX_LEVEL and self.rng.random() < 0.5:
            height += 1                       # each extra row is a coin flip: half as many nodes
        return height

    def path(self, target):
        """update[i] = the last node on row i with a value < target (where we step down)."""
        update = [self.head] * self.MAX_LEVEL
        node = self.head
        for i in range(self.level - 1, -1, -1):
            while node.forward[i] is not None and node.forward[i].val < target:
                node = node.forward[i]        # ride the express lane as far as it goes
            update[i] = node
        return update

    def search(self, target):
        node = self.path(target)[0].forward[0]   # the first node with a value >= target
        return node is not None and node.val == target

    def add(self, num):
        update = self.path(num)
        height = self.random_level()
        self.level = max(self.level, height)  # new rows start at head, which update already holds
        node = Node(num, height)
        for i in range(height):               # splice in after the turning point on each row
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def erase(self, num):
        update = self.path(num)
        node = update[0].forward[0]
        if node is None or node.val != num:
            return False
        for i in range(len(node.forward)):    # node follows update[i] on every row it occupies
            update[i].forward[i] = node.forward[i]
        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1                   # drop rows that became empty
        return True


# --- try the brute force ---
sl = BruteForce()
sl.add(1)
sl.add(2)
sl.add(3)
print(sl.search(0))      # -> False
sl.add(4)
print(sl.search(1))      # -> True
print(sl.erase(0))       # -> False
print(sl.erase(1))       # -> True
print(sl.search(1))      # -> False
sl.add(5)                # duplicates: erase removes one copy at a time
sl.add(5)
print(sl.erase(5))       # -> True
print(sl.search(5))      # -> True
print(sl.erase(5))       # -> True
print(sl.search(5))      # -> False
print(sl.erase(5))       # -> False
print(BruteForce().search(7))   # -> False


# --- try the optimal ---
sl = Skiplist()
sl.add(1)
sl.add(2)
sl.add(3)
print(sl.search(0))      # -> False
sl.add(4)
print(sl.search(1))      # -> True
print(sl.erase(0))       # -> False
print(sl.erase(1))       # -> True
print(sl.search(1))      # -> False
sl.add(5)                # duplicates: erase removes one copy at a time
sl.add(5)
print(sl.erase(5))       # -> True
print(sl.search(5))      # -> True
print(sl.erase(5))       # -> True
print(sl.search(5))      # -> False
print(sl.erase(5))       # -> False
print(Skiplist().search(7))   # -> False
