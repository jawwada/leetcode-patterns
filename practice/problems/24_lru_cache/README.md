# LRU Cache (LeetCode 146)

**Area:** linked list / design · **Difficulty:** Medium-Hard · **Key operations:** dict lookup, unlink a node, push front after sentinel head, evict tail.prev

## Problem

Design a cache with a fixed capacity supporting `get(key)` (the value, or `-1` if absent) and `put(key, value)`, both in O(1) time. When a `put` of a new key would exceed the capacity, evict the least recently used key: the one whose most recent `get` or `put` is the oldest. `OrderedDict` is off limits; build the recency order yourself. In this script `solve(capacity, ops)` runs a list of `("get", k)` / `("put", k, v)` operations and returns the list of `get` results.

## Example

```
capacity 2
put(1,1)  put(2,2)  get(1) -> 1   put(3,3) evicts 2   get(2) -> -1
put(4,4) evicts 1   get(1) -> -1  get(3) -> 3          get(4) -> 4

returned: [1, -1, -1, 3, 4]
```

## Brute force

Keep a plain list of `(key, value)` pairs ordered most recent first. `get` scans the list for the key, pops it and re-inserts it at index 0. `put` scans for the key (to remove the stale pair), inserts the new pair at the front, and drops the last pair if the list is now too long.

O(capacity) per operation, O(capacity) space. Two kinds of waste: the scan walks the whole list to find a key we could jump to directly, and moving one pair to the front shifts every other pair.

## From brute force to optimal

Separate the two costs. Finding the key is a hash lookup away: `dict[key] -> node`. Promoting a node to "most recent" is slow only because an array must shift on removal; a doubly linked list unlinks a node in O(1) given a pointer to it, and the dict hands us exactly that pointer. So the structure is a dict plus nodes chained in recency order between two sentinels `head` and `tail`. The list order *is* the recency information: no timestamps, no counters. Eviction is "unlink `tail.prev` and delete its key from the dict", which is why every node must carry its key.

## Intuition

Think of a conveyor belt. Items enter at the left end (`head`), drift right as other items are used, and fall off the right end (`tail`) when the belt is full. Any `get` or `put` of a key that is already present lifts the item from wherever it is and drops it back on the left. The dict is the index card that says where on the belt each key sits, so you never walk the belt. The two sentinels mean every real node always has a neighbour on both sides, so unlink and push-front need no `None` checks.

## Walkthrough

The chain is drawn most recent first; `(key:value)`.

```
start                    head <-> tail                               keys {}
put(1,1)   new, push     head <-> (1:1) <-> tail                     keys {1}
put(2,2)   new, push     head <-> (2:2) <-> (1:1) <-> tail           keys {1,2}
get(1)     hit: unlink (1:1), push front -> 1
                         head <-> (1:1) <-> (2:2) <-> tail
put(3,3)   new; 3 > 2 so evict tail.prev = (2:2), delete key 2
                         head <-> (3:3) <-> (1:1) <-> tail           keys {1,3}
get(2)     miss -> -1    (chain unchanged)
put(4,4)   new; evict tail.prev = (1:1), delete key 1
                         head <-> (4:4) <-> (3:3) <-> tail           keys {3,4}
get(1)     miss -> -1
get(3)     hit, to front head <-> (3:3) <-> (4:4) <-> tail           -> 3
get(4)     hit, to front head <-> (4:4) <-> (3:3) <-> tail           -> 4

results [1, -1, -1, 3, 4]
```

The two pointer operations, drawn on `unlink(x)` and `push_front(x)`:

```
unlink(x):      p <-> x <-> n        p.next = n, n.prev = p       p <-> n
push_front(x):  head <-> f ...       x.prev = head, x.next = f,
                                     f.prev = x, head.next = x    head <-> x <-> f ...
```

## Steps

1. Sentinels `head <-> tail`; `where = {}` mapping key to node.
2. `unlink(node)`: wire `node.prev` and `node.next` to each other. `push_front(node)`: insert between `head` and `head.next`.
3. `get(k)`: look up the node; if present, unlink it, push it to the front, return its value; else `-1`.
4. `put(k, v)`: if the key exists, update its value and unlink the node. Otherwise create a node, store it in the dict, and if the dict is now larger than the capacity, unlink `tail.prev` and delete its key.
5. Push the (new or updated) node to the front.

## Complexity

O(1) per operation: one dict lookup plus a constant number of pointer rewrites. O(capacity) space for the dict and the nodes.

## Pitfalls

- **Evicting from the wrong end.** `victim = head.next` throws away the most recently used node. In the example `put(3,3)` evicts key 1 and `get(2)` returns 2 instead of `-1`. The least recent node is `tail.prev`.
- **`>=` instead of `>`.** Evicting when the size reaches the capacity makes a capacity-2 cache hold one entry: `put(1)`, `put(2)`, `get(1)` returns `-1`.
- **Updating a value without refreshing recency.** Skipping the unlink (an early `continue` after `where[key].val = val`) leaves the key at its old position. `put(1)`, `put(2)`, `put(1, 10)`, `put(3)` then evicts key 1 instead of key 2.
- **Not storing the key in the node.** Eviction finds the node through `tail.prev` and must delete it from the dict; without `node.key` there is no way to know which entry to remove.
- **Singly linked list.** Unlinking a node needs its predecessor in O(1); only a doubly linked list gives you that.
- **Order of the push-front writes.** Set `node.prev`/`node.next` first, then the old first node's `prev`, then `head.next`. Writing `head.next = node` before `head.next.prev = node` makes the node point to itself.
