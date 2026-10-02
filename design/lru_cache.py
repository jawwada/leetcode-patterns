"""
LRU Cache (LeetCode 146)  — Medium
Pattern: Hash map + doubly linked list

Problem
-------
Design a fixed-capacity cache with get(key) -> value (or -1) and put(key, value), both in O(1).
When a put would exceed capacity, evict the least recently used key, i.e. the one whose last
get/put is oldest.
Example: capacity 2; put(1,1) put(2,2) get(1)->1 put(3,3) evicts 2; get(2)->-1 get(3)->3.

Brute force
-----------
Keep a plain list of (key, value) ordered most-recent first. get scans the list to find the key
(O(n)), then pops it and re-inserts it at index 0 (another O(n) shift). put does the same scan
and, on overflow, pops the last element. O(n) per operation, O(capacity) space. The wasted work
is twofold: we re-walk the whole list to find a key we could jump to directly, and moving ONE
element to the front shifts every other element.

From brute force to optimal
---------------------------
Two separate costs: locating the key, and promoting it to "most recent". A hash map kills the
first: key -> node in O(1). The second is O(n) only because an array must shift on removal; a
doubly linked list unlinks a node in O(1) given a pointer to it, and the hash map hands us
exactly that pointer. So the tracker is dict[key] -> Node plus nodes chained in recency order
between two sentinels. It needs no timestamps or counters: the list ORDER is the recency
information, and the per-entry memory is just (key, val, prev, next).

Intuition
---------
Head side = "just used", tail side = "about to be evicted". Every access unlinks the node from
wherever it is and re-links it right after head. Eviction is "unlink tail.prev and drop its key
from the map", which is why the node must store its key. Everything is a constant number of
pointer rewrites because each node already knows both neighbours.

Geometric view
--------------
A conveyor belt: items enter at the left (head), drift right as other items are used, and fall
off the right end (tail) when the belt is full. A get lifts an item from the middle of the belt
and drops it back on the left. The hash map is the index card telling you where on the belt
each key currently sits, so you never walk the belt.

Steps
-----
1. Node(key, val, prev, next); sentinels head <-> tail so no None checks anywhere.
2. get: if key not in map return -1; unlink node, push it to front, return node.val.
3. put: if key in map update val and unlink; else create node, map it, and if the map is now
   over capacity unlink tail.prev and delete its key from the map.
4. Push the (new or updated) node to the front.

Complexity: O(1) time per operation, O(capacity) space — one hash lookup plus constant pointer rewrites.
Pitfalls: not storing key in the node (eviction can't delete from the map); singly linked list
          (no O(1) unlink); updating the value on put without also refreshing recency.
"""
import random


class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}                                 # key -> Node
        self.head, self.tail = Node(), Node()         # sentinels: head <-> ... <-> tail
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._unlink(node)
        else:
            node = Node(key, value)
            self.map[key] = node
            if len(self.map) > self.cap:
                victim = self.tail.prev           # least recently used
                self._unlink(victim)
                del self.map[victim.key]
        self._push_front(node)


class BruteForce:
    """List of (key, value) ordered most-recent first; every op scans and shifts, O(n)."""

    def __init__(self, capacity: int):
        self.cap = capacity
        self.items = []

    def get(self, key: int) -> int:
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.insert(0, self.items.pop(i))   # O(n) scan + O(n) shift
                return v
        return -1

    def put(self, key: int, value: int) -> None:
        for i, (k, _) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                break
        self.items.insert(0, (key, value))
        if len(self.items) > self.cap:
            self.items.pop()


if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                      # evicts 2
    assert c.get(2) == -1
    c.put(4, 4)                      # evicts 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

    c = LRUCache(1)                  # edge: capacity 1, update existing key
    c.put(5, 5)
    c.put(5, 6)
    assert c.get(5) == 6
    c.put(7, 7)
    assert c.get(5) == -1 and c.get(7) == 7

    random.seed(0)
    for cap in (1, 2, 3, 5):
        fast, slow = LRUCache(cap), BruteForce(cap)
        for _ in range(500):
            k = random.randint(0, 7)
            if random.random() < 0.5:
                v = random.randint(0, 99)
                fast.put(k, v)
                slow.put(k, v)
            else:
                assert fast.get(k) == slow.get(k)
    print("ok")
