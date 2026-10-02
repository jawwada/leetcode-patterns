"""
Design HashMap (LeetCode 706)  — Easy
Pattern: Separate chaining with load-factor resizing

Problem
-------
Implement MyHashMap without built-in hash tables: put(key, value), get(key) -> value or -1,
remove(key). Keys and values are non-negative ints up to 10^6.
Example: put(1,1) put(2,2) get(1)->1 get(3)->-1 put(2,1) get(2)->1 remove(2) get(2)->-1.

Brute force
-----------
Keep one list of [key, value] pairs. put scans for the key (update or append), get scans,
remove scans and pops. O(n) per operation, O(n) space. The wasted work is comparing the target
against EVERY stored key, even though a key's own digits could tell us where to look.

From brute force to optimal
---------------------------
The scan is slow because all keys share one list. Partition them: compute an address from the
key (hash(key) % buckets) so each lookup only scans the few keys that share that address. With
B buckets and n keys the expected chain length is n/B; keep that constant by doubling B when
n > 2B and rehashing every pair (amortised O(1), since each doubling costs O(n) but happens
only after n inserts). The tracker remembers only the pairs themselves plus the bucket count;
it does not need ordering or a global index.

Intuition
---------
A hash function turns "search" into "go directly to shelf k, then look at the handful of items
there". Collisions are unavoidable, so each shelf is a short list. Resizing keeps the shelves
short as the map grows, which is what makes the average O(1) honest.

Geometric view
--------------
B shelves in a row; each key is thrown onto shelf hash(key) % B and lands at the end of that
shelf's chain. After 1, 2, 9, 17 with B = 8:
  shelf 1: [1,_] -> [9,_] -> [17,_]      shelf 2: [2,_]      others empty
A get walks only one shelf. Doubling B spreads every chain across twice as many shelves.

Steps
-----
1. buckets = [[] for _ in range(8)], size = 0.
2. put: find pair in bucket -> update; else append and size += 1; if size > 2 * B, resize.
3. get: scan the one bucket, return value or -1.
4. remove: scan the one bucket, pop the pair, size -= 1.
5. resize: allocate 2B empty buckets and re-append every pair by its new address.

Complexity: O(1) average time per operation (O(n) worst case on a resize or bad collisions),
            O(n + B) space — short chains kept short by the load factor.
Pitfalls: forgetting to rehash on resize (addresses change with B); storing tuples (immutable,
          so update needs a replace); treating value 0 as "missing".
"""


class MyHashMap:
    def __init__(self):
        self.size = 0
        self.buckets = [[] for _ in range(8)]

    def _bucket(self, key: int) -> list:
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key: int, value: int) -> None:
        b = self._bucket(key)
        for pair in b:
            if pair[0] == key:
                pair[1] = value
                return
        b.append([key, value])
        self.size += 1
        if self.size > 2 * len(self.buckets):       # load factor > 2: double and rehash
            self._resize()

    def get(self, key: int) -> int:
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                self.size -= 1
                return

    def _resize(self) -> None:
        old = self.buckets
        self.buckets = [[] for _ in range(2 * len(old))]
        for b in old:
            for k, v in b:
                self.buckets[hash(k) % len(self.buckets)].append([k, v])


class BruteForce:
    """One flat list of [key, value]; every operation scans all pairs, O(n)."""

    def __init__(self):
        self.pairs = []

    def put(self, key: int, value: int) -> None:
        for pair in self.pairs:
            if pair[0] == key:
                pair[1] = value
                return
        self.pairs.append([key, value])

    def get(self, key: int) -> int:
        for k, v in self.pairs:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        self.pairs = [p for p in self.pairs if p[0] != key]


if __name__ == "__main__":
    import random

    m = MyHashMap()
    m.put(1, 1)
    m.put(2, 2)
    assert m.get(1) == 1
    assert m.get(3) == -1
    m.put(2, 1)
    assert m.get(2) == 1
    m.remove(2)
    assert m.get(2) == -1

    e = MyHashMap()                      # edge: value 0 is a real value, remove of absent key is a no-op
    e.put(0, 0)
    assert e.get(0) == 0
    e.remove(99)
    assert e.get(0) == 0

    random.seed(3)
    fast, slow = MyHashMap(), BruteForce()
    for _ in range(3000):                # forces several resizes
        k, op = random.randint(0, 500), random.random()
        if op < 0.5:
            v = random.randint(0, 10**6)
            fast.put(k, v)
            slow.put(k, v)
        elif op < 0.8:
            assert fast.get(k) == slow.get(k)
        else:
            fast.remove(k)
            slow.remove(k)
    assert fast.size == len(slow.pairs)
    print("ok")
