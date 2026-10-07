## LRU Cache

Track recency with a doubly linked list and locate nodes with a dictionary. Both structures must contain the same keys after each operation.

<!-- cell -->

### The LRU cache

A cache is the classic design question, and LRU is the method's showcase: two structures, one invariant, three helpers. LRU Cache asks for `get(key)`, the value or −1, and `put(key, value)`, both in O(1); when a `put` of a new key would exceed the capacity, the key whose last `get` or `put` is the oldest is evicted. With capacity 2, `put(1, 1)`, `put(2, 2)`, `get(1)`, `put(3, 3)` evicts key 2, because key 1 was used more recently.

The design, sentence by sentence, is the code. Finding the key's node is `node = self.map.get(key)`. Taking it out of the line is two pointer writes, `node.prev.next, node.next.prev = node.next, node.prev`, which join its neighbours to each other. Putting it at the front, where the newest sits, sets the node's own two pointers first, `node.prev, node.next = self.head, self.head.next`, then `self.head.next.prev = node`, and only then `self.head.next = node`.

The oldest item is `self.tail.prev`. Forgetting it completely means unlinking it and `del self.map[victim.key]`, which is why every node stores its key. "Too full" is `len(self.map) > self.cap`.

`head` and `tail` are **sentinels**, the dummy nodes of [Linked Lists](12_Linked_Lists.ipynb#topic-linked-lists): they never hold data, so every real node has a neighbour on both sides and no method ever checks for `None`. The empty list is `self.head.next, self.tail.prev = self.tail, self.head`. Each helper below restores the invariant its contract names, and `get` and `put` are a few helper calls each. The prints replay the example, then one more `put` that evicts key 1.

<!-- cell -->

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key, self.val = key, val            # the key lets eviction delete the map entry
        self.prev = self.next = None


class LRUCache:
    """get(key), put(key, value): both O(1). When full, evict the least recently used key."""

    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                            # STATE + INIT (truth): key -> Node
        self.head, self.tail = Node(), Node()    # STATE + INIT (index): sentinels; head.next newest, tail.prev oldest
        self.head.next, self.tail.prev = self.tail, self.head
        # INVARIANT: the keys in map are exactly the nodes between head and tail, and len(map) <= cap

    def _unlink(self, node):                     # contract: node leaves the list, its neighbours are joined
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):                 # contract: node becomes the newest
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _evict(self):                            # contract: the oldest key is forgotten everywhere
        victim = self.tail.prev
        self._unlink(victim)
        del self.map[victim.key]

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1                            # RETURN: missing key
        self._unlink(node)                       # STEP: a read is a use, so move it to the front
        self._push_front(node)
        return node.val                          # RETURN

    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.val = value                     # STEP: update AND refresh
            self._unlink(node)
        else:
            node = self.map[key] = Node(key, value)   # STEP: a new key
        self._push_front(node)
        if len(self.map) > self.cap:             # FIX: restore len(map) <= cap (insert first: capacity 0 also works)
            self._evict()


cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))                              # 1
cache.put(3, 3)                                  # evicts 2: key 1 was used more recently
print(cache.get(2))                              # -1
cache.put(4, 4)                                  # evicts 1
print(cache.get(1), cache.get(3), cache.get(4))  # -1 3 4
```

<!-- cell -->

**Try it**
- Delete the line `del self.map[victim.key]` and rerun: the second print shows `2` instead of `-1`. The dict still points at a node that left the list; the invariant broke, and the answer is wrong without any error.
- Swap the last two lines of `_push_front` and rerun: the cell prints `1`, then `2` instead of `-1`, then crashes with `KeyError: 1`. After `self.head.next = node`, the line `self.head.next.prev = node` points the node at itself. Swap them back before the trace below: on the broken list its walk never ends.
- Move the two eviction lines above `self._push_front(node)` (evict first, as `practice/simple/24_lru_cache.py` does) and run `LRUCache(0).put(1, 1)`: `AttributeError`. In an empty list `tail.prev` is the head sentinel, whose `prev` is `None`. With capacity ≥ 1 both orders work.
- Predict, then check: `c = LRUCache(2)`, `put(1, 1)`, `put(2, 2)`, `put(1, 10)`, `put(3, 3)`. Key 2 is evicted, because updating key 1 also refreshed it: `c.get(2)` is -1 and `c.get(1)` is 10.

<!-- cell -->

### Watch it work

The invariant is easiest to believe when you can see it. The helper below walks the list from `head` to `tail` and prints the keys from newest to oldest after each call, next to what the call returned. The calls are the example's four, then `get(2)`, an update of key 1 and `get(3)`.

<!-- cell -->

```python
def recency(c):                                  # keys from newest to oldest
    keys, node = [], c.head.next
    while node is not c.tail:
        keys.append(node.key)
        node = node.next
    return keys


c = LRUCache(2)
for op, *args in [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3),
                  ("get", 2), ("put", 1, 10), ("get", 3)]:
    result = getattr(c, op)(*args)
    call = f"{op}({', '.join(map(str, args))})"
    print(f"{call:10} -> {str(result):4}  newest..oldest {recency(c)}")
```

<!-- cell -->

**Try it**
- Add `("put", 4, 4)` at the end of the list and predict which key leaves before running: 1, because `get(3)` made 3 the newest.
- Print `sorted(c.map)` next to `recency(c)`: always the same keys. That is the invariant, made visible.
- Run it with `LRUCache(1)`: the list never holds more than one key, and every `get` returns -1, because each one asks for a key that the previous `put` pushed out.

<!-- cell -->

### Where it goes wrong

1. **The node does not store its key.** Eviction finds the oldest node as `tail.prev` and must then delete its dict entry, which needs the key. An eviction that skips `del map[key]` leaves a ghost: in `LRUCache(1)`, `put(1, 1)`, `put(2, 2)`, `get(1)` returns 1 instead of −1.
2. **Updating the truth and forgetting an index**, or the other way round. Every helper must leave the invariant true: unlink *and* `del map[key]`, pop the deque *and* subtract from the total. A HitCounter whose `_expire` pops without subtracting answers `getHits(301)` with 2 instead of 1 after hits at 1 and 301.
3. **Pointer order in `_push_front`.** Set the node's own two pointers first, then `head.next.prev = node`, then `head.next = node`; swapping the last two points the node at itself. The LRU example then answers `get(2)` with 2 instead of −1 and crashes on the next `put`.
4. **`put` of an existing key that only updates the value.** A write is a use, so it must refresh the key as well. With capacity 2, `put(1, 1)`, `put(2, 2)`, `put(1, 10)`, `put(3, 3)` must evict key 2; a value-only update evicts key 1, and `get(1)` returns −1 instead of 10.
5. **A running value left stale by a write.** Every write must update `latest` or `total` in the same method, or a read answers from the past. In StockPrice, `latest = t` in place of `max(latest, t)` lets a correction move "now" backwards: after `update(1, 10)`, `update(2, 5)`, `update(1, 3)`, `current()` returns 3 instead of 5.
6. **Trusting a lazily deleted heap top**, or cleaning it with `if` instead of `while`. After the updates (1, 10), (2, 9), (1, 1), (2, 2), a trusted top says the maximum is 10 and a single `if` says 9; the `while` loop gives 2.
7. **Window boundaries.** "The last 300 seconds" is `(t - 300, t]`, so pop while `timestamp <= now - 300`: with `<`, a hit at 1 still counts in `getHits(301)`. A logger's "10 seconds" allows the same message again at exactly `t + 10`, so a message printed at 1 prints again at 11.
8. **`bisect_left` for "as of time t".** Use `bisect_right`, or probe with `(t, inf)`, or an exact match is skipped: with writes at 1 and 4, `bisect_left` makes `get("foo", 1)` return `""` instead of `"bar"`.
9. **Reads that write.** `self.times[key]` on a `defaultdict` inside a query creates an entry for every key ever asked about: after `tm.get("nope", 5)`, `"nope" in tm.times` is True. Read with `.get(key, [])`.
10. **Class-level state and name clashes** ([Python Toolkit](03_Python_Toolkit.ipynb#topic-python-toolkit)). `next_ok = {}` in the class body is shared by every Logger, so a fresh logger refuses `"foo"` at time 2 because another one printed it at 1. An attribute named like a method hides the method: `self.next = 0` in `MovingAverage.__init__` makes `avg.next(1)` raise `TypeError`.
11. **Insert-then-evict in LFU Cache**, the variation below that evicts the key with the fewest uses. There the newcomer has the smallest count and can evict itself, so LFU must evict first, while LRU may do either. In `LFUCache(1)`, `put(1, 1)`, `get(1)`, `put(2, 2)` must evict key 1; insert-first evicts the newcomer, and `get(2)` returns −1.
12. **Swap-with-last deletion in the wrong order**, in Insert Delete GetRandom O(1), the set below with O(1) insert, remove and random pick. Write `pos[last] = i` before `del pos[val]`, or removing the last element leaves a ghost: `insert(1)`, `remove(1)`, `insert(1)` returns False.

### Edge cases to say out loud

Capacity 0 and 1 · `get` of a missing key · `put` of an existing key (refresh, no eviction) · an empty structure · a burst of events at one timestamp · a query before the first timestamp · a correction of the latest timestamp · removing the only element, which is also the last one.

The cell asserts each of them on the classes above, and every line is one sentence you would say while coding. The two caches of Variations check their own.

<!-- cell -->

```python
c = LRUCache(1)
c.put(5, 5)
c.put(5, 6)                                      # update an existing key: no eviction
assert c.get(5) == 6 and c.get(7) == -1          # a missing key reads -1
c.put(7, 7)                                      # capacity 1: the only stored key is evicted
assert c.get(5) == -1 and recency(c) == [7]
z = LRUCache(0)                                  # capacity 0: insert, then evict at once
z.put(1, 1)
assert z.get(1) == -1 and z.map == {}
```
