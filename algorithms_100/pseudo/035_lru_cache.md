---
rank: 35
slug: lru_cache
---

Design a cache with a fixed capacity. `get(key)` returns the value or -1, `put(key, value)` inserts or updates, and when the cache grows past its capacity it evicts the least recently used key, the one whose last `get` or `put` is oldest. Both operations must run in `O(1)`. With capacity 2, after `put(1, 10)` and `put(2, 20)`, `get(1)` returns 10 and makes key 1 the most recent, so `put(3, 30)` evicts key 2 and `get(2)` returns -1.

The brute force keeps the keys in a list ordered by recency, and every operation scans the list to find a key and shift it to the front, `O(n)` each time. The cache needs two abilities at once. Finding a key in `O(1)` is a hash map's job. Keeping the keys in order of recency, moving any one of them to the front and dropping the oldest, each in `O(1)`, is a doubly linked list's job, because a node that knows both of its neighbors can unlink itself without a search. So use both. The list orders the nodes from the most recent, next to `head`, to the least recent, next to `tail`, and the map sends each key straight to its node: its values are arrows into the chain.

Every use of a key is the same two moves: unlink its node and splice it back in right after `head`. Eviction unlinks the node just before `tail` and deletes its key from the map, which is why a node stores its key as well as its value. The two sentinels sit at the ends forever, so the list is never empty, every real node has two neighbors, and the unlink and splice code needs no special cases.

```text
       nodes[3]      nodes[1]          the map holds an arrow to each node
          │             │
          ▼             ▼
head ─── 3:30 ──────── 1:10 ─── tail   after put(3, 30), key 2 is gone
         most recent   least recent

operation        list from head to tail             note
put(1, 10)       head ─ 1:10 ─ tail
put(2, 20)       head ─ 2:20 ─ 1:10 ─ tail
get(1) → 10      head ─ 1:10 ─ 2:20 ─ tail          1 moves to the front
put(3, 30)       head ─ 3:30 ─ 1:10 ─ tail          over capacity: evict 2
get(2) → -1      head ─ 3:30 ─ 1:10 ─ tail          a miss moves nothing
put(4, 40)       head ─ 4:40 ─ 3:30 ─ tail          over capacity: evict 1
get(1) → -1      head ─ 4:40 ─ 3:30 ─ tail
get(3) → 30      head ─ 3:30 ─ 4:40 ─ tail
get(4) → 40      head ─ 4:40 ─ 3:30 ─ tail
```

```pseudo
CLASS Node
    FUNCTION Init(key, value)
        self.key ← key                  // kept so eviction can clean the map
        self.value ← value
        self.prev ← null
        self.next ← null

CLASS LRUCache
    FUNCTION Init(capacity)
        self.capacity ← capacity
        self.nodes ← empty map          // key → node
        self.head ← Node(0, 0)          // sentinel: head.next is most recent
        self.tail ← Node(0, 0)          // sentinel: tail.prev is least recent
        self.head.next ← self.tail
        self.tail.prev ← self.head

    FUNCTION Remove(node)
        node.prev.next ← node.next
        node.next.prev ← node.prev

    FUNCTION AddFront(node)
        node.prev ← self.head
        node.next ← self.head.next
        self.head.next.prev ← node
        self.head.next ← node

    FUNCTION Get(key)
        IF key NOT IN self.nodes
            RETURN -1
        node ← self.nodes[key]
        self.Remove(node)               // a read counts as a use
        self.AddFront(node)
        RETURN node.value

    FUNCTION Put(key, value)
        IF key IN self.nodes
            node ← self.nodes[key]
            node.value ← value
            self.Remove(node)           // it moves to the front below
        ELSE
            node ← Node(key, value)
            self.nodes[key] ← node
        self.AddFront(node)
        IF len(self.nodes) > self.capacity
            lru ← self.tail.prev        // least recently used
            self.Remove(lru)
            self.nodes.remove(lru.key)
```

Each operation is one map lookup plus a fixed number of pointer changes, so `get` and `put` run in `O(1)`, and the cache holds at most `capacity` nodes. Reach for this pairing whenever a problem needs fast lookup plus an order that changes on every access: caches, recently used lists, an eviction policy inside a larger design. Python's `OrderedDict` is this very structure, a hash map threaded with a doubly linked list, and `move_to_end` with `popitem(last=False)` gives a dozen-line solution, but interviewers usually want the list built by hand. LFU Cache extends the idea to one list per use count plus the smallest count in play. The classic mistake is creating a second node when `put` updates an existing key: the map points at the new node, the old one stays in the list, and when that ghost reaches the tail its eviction deletes the live key. Forgetting that `get` also moves its key to the front is the other one.

*Practice:* LC 146 LRU Cache · LC 460 LFU Cache · LC 707 Design Linked List
