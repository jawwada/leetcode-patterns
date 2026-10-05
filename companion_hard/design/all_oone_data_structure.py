"""
All O`one Data Structure (LeetCode 432) - Hard
Chapter: design
Pattern: Hash map + doubly linked list of count buckets

Design AllOne with inc(key), dec(key) (the key exists; a count of 1 removes it), getMaxKey() and
getMinKey() (any key with the max/min count, or "" when empty), all in O(1).
Example: inc("hello") twice, inc("leet") -> getMaxKey() = "hello", getMinKey() = "leet".
"""


# --- helpers ---
class Bucket:
    def __init__(self, count):
        self.count = count
        self.keys = set()                     # every key that currently has this count
        self.prev = None
        self.next = None


def any_key(keys):
    """Any one element of a set ("" when it is empty)."""
    for key in keys:
        return key
    return ""


# --- brute force ---
class BruteForce:
    """Dict key -> count; every max/min query scans all keys. O(n) per query."""

    def __init__(self):
        self.counts = {}

    def inc(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1

    def dec(self, key):
        self.counts[key] -= 1
        if self.counts[key] == 0:
            del self.counts[key]

    def getMaxKey(self):
        best = ""
        for key in self.counts:               # scan every key
            if best == "" or self.counts[key] > self.counts[best]:
                best = key
        return best

    def getMinKey(self):
        best = ""
        for key in self.counts:
            if best == "" or self.counts[key] < self.counts[best]:
                best = key
        return best


# --- optimal ---
class AllOne:
    """Sorted doubly linked list of count buckets; a key hops to a neighbour. O(1) per op."""

    def __init__(self):
        self.head = Bucket(0)                 # sentinel: also acts as the count-0 bucket
        self.tail = Bucket(0)                 # sentinel: tail.prev is the max bucket
        self.head.next = self.tail
        self.tail.prev = self.head
        self.where = {}                       # key -> the bucket holding it

    def insert_after(self, node, count):
        new = Bucket(count)                   # squeeze a new bucket in between node and node.next
        new.prev = node
        new.next = node.next
        node.next.prev = new
        node.next = new
        return new

    def remove_key(self, node, key):
        node.keys.discard(key)
        if len(node.keys) == 0 and node is not self.head:
            node.prev.next = node.next        # drop an empty bucket right away
            node.next.prev = node.prev

    def inc(self, key):
        cur = self.where.get(key, self.head)  # a new key starts from the count-0 sentinel
        nxt = cur.next
        if nxt is self.tail or nxt.count != cur.count + 1:
            nxt = self.insert_after(cur, cur.count + 1)   # the next count does not exist yet
        nxt.keys.add(key)
        self.where[key] = nxt
        self.remove_key(cur, key)

    def dec(self, key):
        cur = self.where[key]
        if cur.count == 1:
            del self.where[key]               # count 0: the key disappears
        else:
            prv = cur.prev
            if prv is self.head or prv.count != cur.count - 1:
                prv = self.insert_after(cur.prev, cur.count - 1)
            prv.keys.add(key)
            self.where[key] = prv
        self.remove_key(cur, key)

    def getMaxKey(self):
        return any_key(self.tail.prev.keys)   # the head sentinel has no keys, so "" when empty

    def getMinKey(self):
        return any_key(self.head.next.keys)


# --- try the brute force ---
a = BruteForce()
a.inc("hello")
a.inc("hello")
print(a.getMaxKey())     # -> hello
print(a.getMinKey())     # -> hello
a.inc("leet")
print(a.getMaxKey())     # -> hello
print(a.getMinKey())     # -> leet
a.dec("hello")
a.dec("hello")           # hello is gone
print(a.getMaxKey())     # -> leet
print(a.getMinKey())     # -> leet
a.dec("leet")
print(repr(a.getMaxKey()))   # -> ''
print(repr(a.getMinKey()))   # -> ''


# --- try the optimal ---
a = AllOne()
a.inc("hello")
a.inc("hello")
print(a.getMaxKey())     # -> hello
print(a.getMinKey())     # -> hello
a.inc("leet")
print(a.getMaxKey())     # -> hello
print(a.getMinKey())     # -> leet
a.dec("hello")
a.dec("hello")           # hello is gone
print(a.getMaxKey())     # -> leet
print(a.getMinKey())     # -> leet
a.dec("leet")
print(repr(a.getMaxKey()))   # -> ''
print(repr(a.getMinKey()))   # -> ''
