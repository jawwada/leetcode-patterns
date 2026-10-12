"""
LRU Cache - Hash Map + Doubly Linked List

Design a cache with a fixed capacity: get(key) returns the value or -1, and
put(key, value) inserts or updates; a put that overflows the capacity evicts
the least recently used key.
Capacity 2: put(1, 10), put(2, 20), get(1), put(3, 30), get(2) -> 10, -1.
"""


# --- helpers ---
class Node:
    def __init__(self, key, value):
        self.key = key              # kept so eviction can clean the map
        self.value = value
        self.prev = None
        self.next = None


# --- algorithm ---
class LRUCache:
    """Map key -> node; the list runs from most to least recently used."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}             # key -> node
        self.head = Node(0, 0)      # sentinel: head.next is most recent
        self.tail = Node(0, 0)      # sentinel: tail.prev is least recent
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node):
        """Unlink node: its two neighbors point past it. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def add_front(self, node):
        """Splice node in right after head, the most recent spot. O(1)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Return the value and make the key most recent; -1 if absent. O(1)."""
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self.remove(node)           # a read counts as a use
        self.add_front(node)
        return node.value

    def put(self, key, value):
        """Insert or update the key as most recent; if that overflows the
        capacity, evict the node before tail. O(1)."""
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self.remove(node)       # it moves to the front below
        else:
            node = Node(key, value)
            self.nodes[key] = node
        self.add_front(node)
        if len(self.nodes) > self.capacity:
            lru = self.tail.prev    # least recently used
            self.remove(lru)
            del self.nodes[lru.key]


# --- try it ---
cache = LRUCache(2)
cache.put(1, 10)
cache.put(2, 20)
print(cache.get(1))         # -> 10
cache.put(3, 30)            # evicts key 2
print(cache.get(2))         # -> -1
cache.put(4, 40)            # evicts key 1
print(cache.get(1))         # -> -1
print(cache.get(3))         # -> 30
print(cache.get(4))         # -> 40
