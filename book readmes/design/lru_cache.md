# LRU Cache
*LeetCode 146 · Medium · Pattern: Hash map + doubly linked list · Reading time ~10 min*

## The problem

Design a fixed-capacity cache with get(key) -> value (or -1) and put(key, value), both in O(1) average time. When a
put exceeds capacity, evict the least recently used key, i.e. the one whose last get or put is oldest.

```text
Example: capacity 2; put(1,1), put(2,2), get(1) -> 1, put(3,3)
  evicts key 2, get(2) -> -1, get(3) -> 3.
```

## What the problem is really asking

Build a key-value store with a fixed capacity. `get(key)` returns the value or -1. `put(key, value)` inserts or updates. When an insert would exceed the capacity, throw out the *least recently used* key: the one whose last `get` or `put` happened longest ago. Both operations must be O(1).

So the cache is really two things at once: a dictionary (find a key fast) and a *queue ordered by recency* (find the oldest fast, and move any key to the "newest" end fast). The difficulty is that a `get` on a key in the middle of the queue must yank it to the front, in constant time.

```text
  capacity 2

  put(1,1)  put(2,2)  get(1)  put(3,3)
  recency, newest on the left:
  [1]       [2 1]     [1 2]   [3 1]   <- 2 was oldest, evicted
```

## Do it by hand first

Picture a pile of index cards on a desk, newest on top. Every time a card is used, you pull it out of the pile and put it on top. When the desk is full and a new card arrives, the bottom card goes in the bin.

```text
  top (most recent)
    +-------+
    | key 1 |   <- just used, pulled out and put on top
    +-------+
    | key 2 |
    +-------+
  bottom (least recent: evict this one)
```

Two physical motions happened: *finding* the card in the pile, and *pulling it out without disturbing the others*. Your hand kept track of an ordered pile, plus your memory of where each card sits. Those two pieces are the two halves of the data structure.

## The first honest attempt

Keep a Python list of `(key, value)` pairs, most recent first. `get` scans for the key, pops it, and inserts it at index 0. `put` scans for an existing key to remove, inserts at the front, and pops the last item if over capacity.

Every operation is O(n): one scan to find, one shift to move.

```text
  list:  [ (5,.) (8,.) (2,.) (7,.) (1,.) (4,.) ]
  get(1):
    scan   ->  ->  ->  ->  found at index 4     (4 compares)
    pop(4), then insert(0):
           [ (1,.) (5,.) (8,.) (2,.) (7,.) (4,.) ]
               ^     >>    >>    >>    >>       every element
                                                 shifts right
```

There are two distinct wastes: scanning to *find* a key whose location we could have remembered, and shifting every neighbour just to *move* one element.

## The turning point

**Claim: the two costs are separable; a hash map kills the search and a doubly linked list kills the shift, and the map can hand the list exactly the pointer it needs.**

Locating: a dict from key to "where this key lives" gives O(1) lookup. If the thing it stores is a pointer to a list node, we jump straight to it.

Moving: an array shifts on removal because positions are implicit. In a linked list positions are explicit pointers, and removing a node only rewrites its neighbours' pointers. But with a *singly* linked list you need the predecessor to unlink, and finding it is a scan. With a *doubly* linked list, each node knows `prev` and `next`, so unlinking is two pointer writes:

```text
  before:   A <-> X <-> B
  unlink X: A.next = B ; B.prev = A
  after:    A <-> B          (X is free, O(1))
```

Pushing to the front is four pointer writes. Evicting the oldest is "unlink `tail.prev`". Two *sentinel* nodes, `head` and `tail`, that are never removed mean every real node always has both neighbours, so there are no special cases for an empty list or for the first/last node.

One more detail matters: each node stores its own **key**, not just the value. When we evict `tail.prev`, we must also delete its dict entry, and the node is the only place we can learn which key that is.

The final shape is a dict `key -> node` laid over a doubly linked list whose *order* is the recency. We never store timestamps; position is the timestamp.

```text
  map:  {1: *, 2: *}
             |    \
             v     v
  head <-> [1:1] <-> [2:2] <-> tail
          newest            oldest
```

## Watch it work

Capacity 2. Operations: `put(1,1)`, `put(2,2)`, `get(1)`, `put(3,3)`, `get(2)`, `put(4,4)`, `get(3)`.

Frame 1 — after `put(1,1)` and `put(2,2)`.

```text
  map: {1, 2}
  head <-> [2:2] <-> [1:1] <-> tail
           newest    oldest
```

Each new node was pushed right after `head`, so 2 is newer than 1.

Frame 2 — `get(1)` returns 1.

```text
  map: {1, 2}
  head <-> [1:1] <-> [2:2] <-> tail
            ^ unlinked, pushed to front
```

The map gave us node 1 directly; two writes unlinked it and four put it at the front.

Frame 3 — `put(3,3)`: new key, map size becomes 3 > 2.

```text
  victim = tail.prev = [2:2]  -> unlink, del map[2]
  map: {1, 3}
  head <-> [3:3] <-> [1:1] <-> tail
```

The node itself told us its key, so the map entry could be deleted.

Frame 4 — `get(2)` returns -1; nothing changes.

```text
  map: {1, 3}
  head <-> [3:3] <-> [1:1] <-> tail
```

A miss does not touch the recency order.

Frame 5 — `put(4,4)`: evicts `tail.prev`, which is key 1.

```text
  map: {3, 4}
  head <-> [4:4] <-> [3:3] <-> tail
```

Key 1 was used at Frame 2, earlier than key 3's insertion, so it was the oldest.

Frame 6 — `get(3)` returns 3.

```text
  map: {3, 4}
  head <-> [3:3] <-> [4:4] <-> tail
```

Key 3 moves to the front; key 4 is now the next eviction candidate.

Across all frames the map and the list held exactly the same key set, and the list read newest to oldest from `head` to `tail`.

## Why it is correct

Invariant: (a) the keys in the map are exactly the keys in the list, at most `capacity` of them, and `map[k]` points to k's node holding k's latest value; (b) walking from `head` to `tail`, nodes appear in decreasing order of last use.

- `get` hit: the key becomes the most recently used. Moving its node to the front makes it first and leaves the relative order of all others unchanged, so (b) holds. A miss changes nothing.
- `put` existing key: update the value and move to front, same reasoning. No eviction, because the key count did not change.
- `put` new key: insert into the map; if the count exceeds capacity, the least recently used key is, by (b), the node just before `tail`. Removing it from both list and map restores (a). Then push the new node to the front, which is correct because it is now the most recent.

Since (b) holds after every step, `tail.prev` is always the right victim.

## Cost

- Time: O(1) per `get` and `put`: one dict lookup plus a constant number of pointer rewrites.
- Space: O(capacity): one node and one dict entry per live key, plus two sentinels.

Python note: `collections.OrderedDict` is itself a hash map over a doubly linked list; `move_to_end(key)` and `popitem(last=False)` give the same design in a few lines. Interviewers usually want to see the hand-built version once.

## Variations you will meet

- **LFU Cache (next problem).** Evict by lowest use count, ties broken by recency: the LRU list survives, but one per frequency.
- **TTL / expiring entries.** Add an expiry time to each node; on `get`, treat an expired node as a miss and remove it. If expiries are uniform, the LRU order is also expiry order.
- **Design Browser History.** A doubly linked list (or array with a cursor) where moving back and forth is pointer walking, without the map.
- **Thread-safe LRU.** One lock around both structures; the two must change atomically, since the invariant ties them together.

## What to carry forward

"O(1) find plus O(1) reorder" means a hash map whose values are pointers into a doubly linked list, and the list order *is* the state you would otherwise timestamp. The next problem, LFU Cache, keeps this exact machine but asks it to rank by how often, not just how recently, which forces one list per frequency and a pointer to the smallest.
