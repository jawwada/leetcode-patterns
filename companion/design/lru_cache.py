"""
LRU Cache (LeetCode 146) - Medium
Chapter: design
Pattern: Hash map + doubly linked list

Design a fixed-capacity cache with get(key) -> value (or -1) and put(key, value), both in O(1)
average time. When a put exceeds capacity, evict the least recently used key, i.e. the one whose
last get or put is oldest.
Example: capacity 2; put(1,1), put(2,2), get(1) -> 1, put(3,3) evicts key 2, get(2) -> -1,
get(3) -> 3.
"""


# --- helpers ---
class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


# --- brute force ---
class BruteForce:
    """List of [key, value], most recently used first; every op scans and shifts. O(n) per op."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def get(self, key):
        for i in range(len(self.items)):
            if self.items[i][0] == key:
                item = self.items.pop(i)
                self.items.insert(0, item)    # move to the front: it is now the most recent
                return item[1]
        return -1

    def put(self, key, value):
        for i in range(len(self.items)):
            if self.items[i][0] == key:
                self.items.pop(i)         # drop the old entry; it is re-added at the front
                break
        self.items.insert(0, [key, value])
        if len(self.items) > self.capacity:
            self.items.pop()              # the last item is the least recently used


# --- optimal ---
class LRUCache:
    """Dict key -> node plus a doubly linked list ordered by recency. O(1) per get and put."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}                   # key -> Node
        self.head = Node(0, 0)            # sentinel: head.next is the most recently used
        self.tail = Node(0, 0)            # sentinel: tail.prev is the least recently used
        self.head.next = self.tail
        self.tail.prev = self.head

    def unlink(self, node):
        node.prev.next = node.next        # the two neighbours skip over node
        node.next.prev = node.prev

    def push_front(self, node):
        node.prev = self.head             # squeeze node in between head and head.next
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self.unlink(node)                 # touching a key makes it the most recent
        self.push_front(node)
        return node.val

    def put(self, key, value):
        if key in self.nodes:
            node = self.nodes[key]
            node.val = value
            self.unlink(node)
        else:
            node = Node(key, value)
            self.nodes[key] = node
            if len(self.nodes) > self.capacity:
                victim = self.tail.prev   # least recently used
                self.unlink(victim)
                del self.nodes[victim.key]
        self.push_front(node)


# --- try the brute force ---
c = BruteForce(2)
c.put(1, 1)
c.put(2, 2)
print(c.get(1))      # -> 1
c.put(3, 3)          # evicts key 2
print(c.get(2))      # -> -1
c.put(4, 4)          # evicts key 1
print(c.get(1))      # -> -1
print(c.get(3))      # -> 3
print(c.get(4))      # -> 4


# --- try the optimal ---
c = LRUCache(2)
c.put(1, 1)
c.put(2, 2)
print(c.get(1))      # -> 1
c.put(3, 3)          # evicts key 2
print(c.get(2))      # -> -1
c.put(4, 4)          # evicts key 1
print(c.get(1))      # -> -1
print(c.get(3))      # -> 3
print(c.get(4))      # -> 4
