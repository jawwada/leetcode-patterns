# All O`one Data Structure
*LeetCode 432 · Hard · Pattern: Hash map + doubly linked list of count buckets · Reading time ~12 min*

## What the problem is really asking

Keep a multiset of string keys with counts. `inc(key)` adds one to a key's count (creating it at 1 if new). `dec(key)` subtracts one (the key is guaranteed to exist; at count 0 it disappears). `getMaxKey()` returns any key with the largest count and `getMinKey()` any key with the smallest, or `""` if there are no keys. **All four in O(1).**

The answers are single keys, but to produce them instantly we must always know the extremes of a set of counts that changes one step at a time, in both directions.

```text
  inc(hello) inc(hello) inc(leet)

  counts:  hello -> 2,  leet -> 1
  getMaxKey() = "hello"   getMinKey() = "leet"
```

What makes it hard: a min-heap answers min, a max-heap answers max, neither answers both, and neither does it in O(1) with arbitrary decrements. A sorted container would be O(log n). We need something that exploits the fact that counts change by exactly one.

## Do it by hand first

Lay out shelves on a wall, one shelf per count that currently exists, lowest count on the left. Put each key's name tag on its shelf.

```text
   count 1      count 2      count 3
  +--------+   +--------+
  |  b     |   |  a     |      (no shelf: nobody has 3)
  +--------+   +--------+
   ^ min                ^ max
```

When `a` is incremented, you move its tag one shelf to the right. If there is no shelf for count 3 yet, you nail one up *immediately to the right* of shelf 2. If a shelf becomes empty, you take it down. The leftmost shelf is always the min, the rightmost always the max.

Your hand tracked: for each key, which shelf it is on; and for the shelves, their left-to-right order. A key never jumps more than one shelf, so you only ever look at the shelf *next to* the current one.

## The first honest attempt

A dict `key -> count`. `inc` and `dec` are O(1). `getMaxKey` is `max(counts, key=counts.get)` and `getMinKey` is the same with `min`: each O(n).

```text
  counts: {a:3, b:1, c:2, d:3, e:1}

  getMaxKey: look at a, b, c, d, e   -> a    (5 reads)
  inc(c)   : c becomes 3             (one key moved one step)
  getMaxKey: look at a, b, c, d, e   -> a    (5 reads again)
```

The waste is re-deriving the entire order of counts after each tiny change. One `inc` can only move one key to the adjacent count, yet the query pays for every key.

## The turning point

**Claim: because counts change by exactly ±1, a key only ever moves between *adjacent* count buckets, so the distinct counts can be kept as a sorted doubly linked list that is maintained with O(1) local edits.**

Build it in three pieces.

*Buckets.* A node holds one count and the set of keys with that count. Nodes are linked in increasing count order between two sentinels, `head` and `tail`. There is at most one node per distinct count, and no empty nodes.

*Index.* A dict `where: key -> node` gives the bucket for any key in O(1).

*Local moves.* On `inc(key)` from node `cur` with count c:

- Look at `cur.next`. If it exists and its count is c+1, the key moves there.
- Otherwise there is a gap (the next count is larger, or we are at the end), so a new node with count c+1 is spliced in right after `cur`. This keeps the list sorted, because c < c+1 < anything after `cur`.
- Remove the key from `cur.keys`; if `cur` is now empty, unlink it.

`dec` is the mirror image using `cur.prev` and count c-1, except that at c = 1 the key is simply deleted from `where` and from `cur`.

```text
  inc(a) when a is in [2] and next is [5]:

  before:  head <-> [1:{b}] <-> [2:{a}] <-> [5:{x}] <-> tail
  splice:  ... [2:{a}] <-> [3:{}] <-> [5:{x}] ...
  move a,  [2] empties and is unlinked:
  after:   head <-> [1:{b}] <-> [3:{a}] <-> [5:{x}] <-> tail
```

A neat trick for new keys: treat `head` itself as the bucket for count 0. A new key "lives" at `head`, so `inc` follows the same code path: look at `head.next`, use it if its count is 1, otherwise splice a count-1 node after `head`. We never unlink `head`, even though its key set is empty.

*Queries.* The min bucket is `head.next` and the max bucket is `tail.prev`. Return any key from its set, or `""` if the list is empty. O(1).

Why a doubly linked list and not an array of buckets indexed by count? Counts can be huge and sparse (one key at count 1, another at a million); an array would need to be scanned across the empty slots in between. The linked list stores only counts that exist, and adjacency in the list is what "next count" means.

## Watch it work

Operations: `inc(a)`, `inc(b)`, `inc(a)`, `inc(a)`, `dec(a)`, `dec(b)`, `inc(c)`. Buckets drawn as `[count:{keys}]`.

Frame 1 — `inc(a)`, `inc(b)`.

```text
  head <-> [1:{a,b}] <-> tail
  where: {a:[1], b:[1]}          min = a or b, max = a or b
```

Both came from `head` (count 0); the first created bucket 1, the second reused it.

Frame 2 — `inc(a)`.

```text
  head <-> [1:{b}] <-> [2:{a}] <-> tail
  where: {a:[2], b:[1]}          min = b, max = a
```

`[1].next` was `tail`, so a count-2 bucket was spliced in after `[1]`.

Frame 3 — `inc(a)`.

```text
  head <-> [1:{b}] <-> [3:{a}] <-> tail
           [2] emptied -> unlinked
  where: {a:[3], b:[1]}          min = b, max = a
```

A count-3 bucket was spliced after `[2]`, then `[2]` lost its only key and was removed.

Frame 4 — `dec(a)`.

```text
  head <-> [1:{b}] <-> [2:{a}] <-> tail
  where: {a:[2], b:[1]}          min = b, max = a
```

`[3].prev` had count 1, not 2, so a count-2 bucket was spliced between them; `[3]` emptied and was removed.

Frame 5 — `dec(b)`.

```text
  head <-> [2:{a}] <-> tail
  where: {a:[2]}                 min = a, max = a
```

b had count 1, so it left `where` entirely; `[1]` emptied and was unlinked.

Frame 6 — `inc(c)`.

```text
  head <-> [1:{c}] <-> [2:{a}] <-> tail
  where: {a:[2], c:[1]}          min = c, max = a
```

`head.next` had count 2, not 1, so a count-1 bucket was spliced right after `head`.

In every frame the bucket counts were strictly increasing from `head` to `tail`, no bucket was empty, and `where` pointed each key at the bucket holding it; so `head.next` and `tail.prev` were always the min and max.

## Why it is correct

Invariant:

- (a) Between the sentinels, node counts are strictly increasing.
- (b) Every node between the sentinels has a non-empty key set.
- (c) Each live key k is in exactly one node's set, that node's count equals k's count, and `where[k]` is that node.

From (a)–(c): the node after `head` has the smallest count of any live key, and the node before `tail` has the largest; any key in those sets is a valid answer.

`inc(k)` with k at node `cur` (count c, or `head` with c = 0). The target count is c+1. If `cur.next` has count c+1, we use it. Otherwise, by (a), `cur.next` has count > c+1 or is `tail`, so splicing a node with count c+1 between them keeps (a). The key is added to the target, `where` updated, and removed from `cur`; if `cur` (not `head`) empties it is unlinked, restoring (b). Unlinking a node from a strictly increasing list keeps it strictly increasing. (c) holds by construction. `dec` is symmetric, using `cur.prev` and count c-1; at c = 1 the key leaves the structure entirely, which is what count 0 means.

Each operation touches only `cur` and one neighbour, so all of this is constant work.

## Cost

- Time: O(1) for all four operations: one dict access, at most one node splice and one unlink, and set add/discard.
- Space: O(n) for n live keys: one dict entry per key, one set slot per key, at most one node per distinct count (so at most n nodes).

## Variations you will meet

- **LFU Cache (previous problem).** Counts only go up, and only the minimum is needed; an integer `min_freq` plus a dict of buckets suffices. All O`one needs both ends and decrements, which is what forces the buckets into a linked list.
- **Return the key that reached the max first.** Replace each bucket's `set` with an ordered structure (an `OrderedDict`) so ties have an order, exactly as LFU does.
- **Arbitrary increments (`inc(key, d)`).** Adjacency breaks: a key can jump past many buckets. Fall back to a sorted container keyed by count, O(log n).
- **Maximum Frequency Stack (next problem).** Also tracks the maximum frequency under ±1 changes, but answers "which element" with a stack per frequency instead of a set.

## What to carry forward

When values change by exactly ±1 and you need the extremes, keep the distinct values as a sorted linked list of buckets and move each item to an adjacent bucket, creating or removing buckets locally. The next problem, Maximum Frequency Stack, tracks the maximum frequency the same way but must also remember *push order* within a frequency, and discovers that a stack per frequency does it for free.
