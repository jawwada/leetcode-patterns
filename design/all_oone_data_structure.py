"""
All O`one Data Structure (LeetCode 432)  — Hard
Pattern: Hash map + doubly linked list of count buckets

Problem
-------
Design AllOne with inc(key), dec(key) (key exists; count 1 -> removed), getMaxKey() and
getMinKey() (any key with the max/min count, "" if empty), each in O(1).
Example: inc("hello") x2, inc("leet") -> getMaxKey() = "hello", getMinKey() = "leet".

Brute force
-----------
A dict key -> count. inc/dec are O(1), but getMaxKey/getMinKey scan all keys with max()/min()
over the dict values: O(n) per query, O(n) space. The wasted work: a query re-examines every
key even though a single inc/dec moves ONE key by ONE step, so the ordering of counts barely
changed since the last query.

From brute force to optimal
---------------------------
The redundancy is re-deriving the ordering of counts from scratch. Observation: counts change by
exactly +-1, so a key only ever moves to the ADJACENT count. If we keep the distinct counts in a
sorted doubly linked list of buckets (each bucket = one count + the set of keys having it), an
inc moves a key from its bucket to the next bucket (creating it if the next bucket's count is not
count+1), and a dec moves it to the previous bucket. The dict key -> bucket hands us the node in
O(1), and insert/unlink of a neighbouring node is O(1) pointer work. Min and max are then just
head.next and tail.prev. Empty buckets are unlinked immediately so the extremes are always real.

Intuition
---------
Sort by count, but exploit that nothing ever jumps: a +-1 step can only land in the neighbouring
bucket, so the sorted order is maintained with local pointer surgery, never a sort or a scan.
Buckets hold sets so that many keys with the same count share one node, and removing a key from
a set is O(1). The sentinel head doubles as a virtual count-0 bucket, which makes inc of a brand
new key the same code path as inc of an existing one.

Geometric view
--------------
   head <-> [1: {leet}] <-> [2: {hello}] <-> tail
   inc("leet"): next bucket has count 2 == 1+1 -> move leet right, bucket 1 empties, unlink it
   head <-> [2: {leet, hello}] <-> tail
   dec("hello"): prev bucket is head (count 0) -> create [1] left of 2, move hello there
   head <-> [1: {hello}] <-> [2: {leet}] <-> tail
Keys hop one bucket left or right along a number line of counts; empty buckets vanish, so the
two ends of the line are always the current min and max.

Steps
-----
1. Node(count, keys=set(), prev, next); sentinels head (count 0) <-> tail; where = {key: node}.
2. inc(key): cur = where.get(key, head); nxt = cur.next; if nxt is tail or nxt.count !=
   cur.count+1 insert a new node with count cur.count+1 after cur. Add key to nxt, update
   where, remove key from cur (unlink cur if it became empty and is not head).
3. dec(key): cur = where[key]; if cur.count == 1 delete where[key]; else find/create the
   bucket with cur.count-1 just before cur and move key there. Remove key from cur; unlink
   cur if empty.
4. getMaxKey: any key in tail.prev (or ""); getMinKey: any key in head.next (or "").

Complexity: O(1) time per operation, O(n) space — dict lookup plus constant pointer rewrites;
one node per distinct count, one dict entry per key.
Pitfalls: not unlinking empty buckets (getMax/getMin then return stale nodes); creating a new
bucket when the neighbour already has the right count (breaks the "distinct counts" invariant);
forgetting to delete the key from the dict when its count hits 0.
"""
import random


class Node:
    __slots__ = ("count", "keys", "prev", "next")

    def __init__(self, count: int = 0):
        self.count = count
        self.keys = set()
        self.prev = self.next = None


class AllOne:
    def __init__(self):
        self.head, self.tail = Node(), Node()          # sentinels; counts ascend in between
        self.head.next, self.tail.prev = self.tail, self.head
        self.where = {}                                # key -> bucket node holding it

    def _insert_after(self, node: Node, count: int) -> Node:
        new = Node(count)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        return new

    def _remove_key(self, node: Node, key: str) -> None:
        node.keys.discard(key)
        if not node.keys and node is not self.head:    # drop empty buckets immediately
            node.prev.next, node.next.prev = node.next, node.prev

    def inc(self, key: str) -> None:
        cur = self.where.get(key, self.head)           # head acts as the count-0 bucket
        nxt = cur.next
        if nxt is self.tail or nxt.count != cur.count + 1:
            nxt = self._insert_after(cur, cur.count + 1)
        nxt.keys.add(key)
        self.where[key] = nxt
        self._remove_key(cur, key)

    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.count == 1:
            del self.where[key]
        else:
            prv = cur.prev
            if prv is self.head or prv.count != cur.count - 1:
                prv = self._insert_after(cur.prev, cur.count - 1)
            prv.keys.add(key)
            self.where[key] = prv
        self._remove_key(cur, key)

    def getMaxKey(self) -> str:
        node = self.tail.prev
        return next(iter(node.keys)) if node is not self.head else ""

    def getMinKey(self) -> str:
        node = self.head.next
        return next(iter(node.keys)) if node is not self.tail else ""


class BruteForce:
    """Dict key -> count; every max/min query scans all keys, O(n)."""

    def __init__(self):
        self.counts = {}

    def inc(self, key: str) -> None:
        self.counts[key] = self.counts.get(key, 0) + 1

    def dec(self, key: str) -> None:
        self.counts[key] -= 1
        if self.counts[key] == 0:
            del self.counts[key]

    def getMaxKey(self) -> str:
        return max(self.counts, key=self.counts.get) if self.counts else ""

    def getMinKey(self) -> str:
        return min(self.counts, key=self.counts.get) if self.counts else ""


if __name__ == "__main__":
    a = AllOne()
    a.inc("hello")
    a.inc("hello")
    assert a.getMaxKey() == "hello" and a.getMinKey() == "hello"
    a.inc("leet")
    assert a.getMaxKey() == "hello" and a.getMinKey() == "leet"
    a.dec("hello")
    a.dec("hello")                                     # hello removed entirely
    assert a.getMaxKey() == "leet" and a.getMinKey() == "leet"
    a.dec("leet")
    assert a.getMaxKey() == "" and a.getMinKey() == ""   # edge: empty structure

    random.seed(0)
    for _ in range(20):
        fast, slow = AllOne(), BruteForce()
        for _ in range(400):
            k = random.choice("abcde")
            r = random.random()
            if r < 0.45:
                fast.inc(k)
                slow.inc(k)
            elif r < 0.75 and k in slow.counts:
                fast.dec(k)
                slow.dec(k)
            else:                                      # any key with the extreme count is valid
                mx, mn = fast.getMaxKey(), fast.getMinKey()
                assert slow.counts.get(mx, 0) == slow.counts.get(slow.getMaxKey(), 0)
                assert slow.counts.get(mn, 0) == slow.counts.get(slow.getMinKey(), 0)
                assert (mx == "") == (not slow.counts) and (mn == "") == (not slow.counts)
    print("ok")
