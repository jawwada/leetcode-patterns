"""
LFU Cache - Frequency Buckets That Keep LRU Order

Design a cache of fixed capacity whose get(key) and put(key, value) run in O(1);
when full, it evicts the least frequently used key, the least recent on a tie.
Capacity 2: put(1, 10), get(1), put(2, 20), put(3, 30), get(2) -> -1.
"""


# --- helpers ---
class Node:
    def __init__(self, key, value):
        self.key = key              # kept so eviction can clean the map
        self.value = value
        self.freq = 1               # how many times the key was used
        self.prev = None
        self.next = None


# --- algorithm ---
class Bucket:
    """The keys used freq times, newest after head, oldest before tail."""

    def __init__(self):
        self.head = Node(0, 0)      # sentinel: head.next is the newest
        self.tail = Node(0, 0)      # sentinel: tail.prev is the oldest
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_front(self, node):
        """Splice node in right after head, the newest spot. O(1)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node):
        """Unlink node: its two neighbors point past it. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def is_empty(self):
        """True when only the two sentinels are left. O(1)."""
        return self.head.next is self.tail


class LFUCache:
    """Map key -> node, map freq -> bucket, and the smallest freq in use.
    get and put O(1)."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}             # key -> node
        self.buckets = {}           # freq -> bucket of the keys used freq times
        self.min_freq = 0           # the smallest freq that has a key

    def add(self, node):
        """Put node at the front of the bucket for its freq. O(1)."""
        if node.freq not in self.buckets:
            self.buckets[node.freq] = Bucket()
        self.buckets[node.freq].add_front(node)

    def touch(self, node):
        """One more use: move node from bucket f to bucket f + 1. O(1)."""
        bucket = self.buckets[node.freq]
        bucket.remove(node)
        if bucket.is_empty():
            del self.buckets[node.freq]
            if self.min_freq == node.freq:
                self.min_freq += 1      # node moves up to it
        node.freq += 1
        self.add(node)

    def get(self, key):
        """Return the value and count the use; -1 if absent. O(1)."""
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self.touch(node)
        return node.value

    def put(self, key, value):
        """Update and count a use, or evict when full, add at freq 1. O(1)."""
        if self.capacity == 0:
            return
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self.touch(node)
            return
        if len(self.nodes) == self.capacity:
            self.evict()                # before the new key is added
        node = Node(key, value)
        self.nodes[key] = node
        self.add(node)
        self.min_freq = 1               # a new key is the least used

    def evict(self):
        """Drop the oldest node of the least used bucket. O(1)."""
        bucket = self.buckets[self.min_freq]
        victim = bucket.tail.prev       # least used, then least recent
        bucket.remove(victim)
        if bucket.is_empty():
            del self.buckets[self.min_freq]
        del self.nodes[victim.key]


# --- try it ---
cache = LFUCache(2)
cache.put(1, 10)
print(cache.get(1))                 # -> 10
cache.put(2, 20)
cache.put(3, 30)                    # evicts 2: used once, key 1 twice
print(cache.get(2), cache.get(3))   # -> -1 30
cache.put(4, 40)                    # 1 and 3 tie at 2 uses: evicts 1, older
print(cache.get(1), cache.get(3), cache.get(4))     # -> -1 30 40
empty = LFUCache(0)
empty.put(1, 10)
print(empty.get(1))                 # -> -1
