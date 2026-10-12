# LFU Cache
*LeetCode 460 · Hard · Pattern: Frequency buckets of ordered dicts + min-frequency pointer · Reading time ~12 min*

## The problem

Design a fixed-capacity cache with get(key) and put(key, value) in O(1). Each get or put of a key increments its use
count. On overflow evict the key with the smallest use count, breaking ties by evicting the least recently used among
them.

```text
Example: capacity 2; put(1,1), put(2,2), get(1) -> 1, put(3,3)
  evicts 2 (count 1 < count 2), get(2) -> -1, put(4,4) evicts 1
  (1 and 3 both have count 2; 1 is older).
```

## What the problem is really asking

Same contract as LRU Cache: fixed capacity, `get(key)` returns the value or -1, `put(key, value)` inserts or updates, both O(1). What changes is who gets evicted. Every `get` or `put` of a key increments that key's *use count*. When the cache is full and a new key arrives, evict the key with the **smallest use count**; if several keys tie on that count, evict the **least recently used** among them.

So the victim is the minimum of a pair `(count, last_use_time)`. The answer each call returns is still a value, but the hidden object we must maintain is a two-level ranking of all keys, and it must update in O(1) when one key's count goes up by one.

```text
  capacity 2: put(1,1) put(2,2) get(1) put(3,3)

  key   count   last used
   1      2      t3   (put, get)
   2      1      t2   <- smallest count -> evicted by put(3,3)
```

## Do it by hand first

Sort the cards on your desk into piles by how many times each has been used: a "1-use" pile, a "2-use" pile, and so on. Inside each pile, keep the LRU habit from the previous problem: newest on top, oldest at the bottom.

```text
   1 use        2 uses       3 uses
  +-----+      +-----+      +-----+
  |  3  | new  |  1  |      |     |
  +-----+      +-----+      +-----+
  |  ...| old
  +-----+
```

When a card is used, you pull it from its pile and put it on *top* of the next pile to the right. When you must throw one away, you go to the leftmost non-empty pile and take its bottom card.

Your hand tracked three things: which pile each card is in (its count), the order inside each pile (recency), and which pile is leftmost. Hold on to the third one; it is the step people get stuck on.

## The first honest attempt

Store `key -> [value, count, last_tick]` in a dict and keep a global tick counter. `get` and `put` on an existing key update all three fields in O(1). When eviction is needed, scan all keys for the minimum `(count, last_tick)`.

```text
  evict with 6 keys:

  key:    a     b     c     d     e     f
  (c,t): (4,9) (1,3) (2,7) (1,5) (3,8) (2,1)
          ?     ?     ?     ?     ?     ?    6 comparisons
                ^ min (1,3)

  next evict, after ONE key's count changed:
          ?     ?     ?     ?     ?     ?    6 comparisons again
```

Eviction is O(n). The waste is that we recompute the full ranking from scratch, although between two evictions only a handful of keys moved, each by exactly +1.

## The turning point

The eviction scan answers two nested questions:

1. What is the smallest count among live keys?
2. Among keys with that count, which was used least recently?

Kill them separately.

**Question 2 is LRU inside a bucket.** Group keys into buckets by count. Inside each bucket keep keys in recency order with O(1) "remove any key", "append as newest" and "pop oldest". That is exactly an LRU list. In Python, an `OrderedDict` per bucket provides all three: `pop(key)`, `d[key] = value` appends at the end, and `popitem(last=False)` removes from the front. So `bucket[f]` is an `OrderedDict` of the keys whose count is f, oldest first.

**Question 1 is a single integer, `min_freq`, because counts only move by +1.**

**Claim: `min_freq` can change in only two ways, both known at the moment they happen, so it never needs to be searched for.**

Justification:

- *A brand-new key is inserted.* Its count is 1, the smallest possible, so `min_freq = 1`.
- *A key with count f is touched (get or put on an existing key).* It moves from `bucket[f]` to `bucket[f+1]`. If `bucket[f]` is now empty **and** f was the minimum, the new minimum is exactly f+1: the key we just moved is sitting there, and no key can have a count between f and f+1. If `bucket[f]` is still non-empty, or f was not the minimum, `min_freq` is unchanged.
- *Eviction* removes a key from `bucket[min_freq]`, but eviction only happens right before inserting a new key, which resets `min_freq` to 1 anyway.

Nothing else touches counts, so these three cases are complete. The "jump to f+1" step is the one that makes the whole thing O(1): we never need to ask "which is the next non-empty bucket?", because the answer is guaranteed to be the one we just wrote into.

```text
  bucket[1] = {3}   bucket[2] = {1}     min_freq = 1
  get(3):  3 leaves bucket[1] -> empty, and 1 == min_freq
           3 joins bucket[2]
  bucket[2] = {1, 3}                    min_freq = 2
```

So the structure is: `freq_of: key -> count`, `bucket: count -> OrderedDict(key -> value)`, and `min_freq`. Two order of operations rules complete it:

- On a new key with a full cache, **evict first, then insert**. If you insert first, the new key has count 1 and is the newest in `bucket[1]`, but if `bucket[1]` held nothing else it would be the oldest too, and you would evict the key you just added.
- Capacity 0 means `put` does nothing.

## Watch it work

Capacity 2. Operations: `put(1,1)`, `put(2,2)`, `get(1)`, `put(3,3)`, `get(2)`, `get(3)`, `put(4,4)`, `get(1)`, `get(3)`. Each bucket is drawn oldest on the left.

Frame 1 — after `put(1,1)` and `put(2,2)`.

```text
  bucket[1]: [1, 2]           min_freq = 1
  freq_of:   {1:1, 2:1}
```

Both keys are new, count 1; key 1 is older inside the bucket.

Frame 2 — `get(1)` returns 1.

```text
  bucket[1]: [2]              min_freq = 1
  bucket[2]: [1]
  freq_of:   {1:2, 2:1}
```

Key 1 moved up one bucket; bucket 1 is not empty, so `min_freq` stays 1.

Frame 3 — `put(3,3)`: full, so evict the oldest of `bucket[min_freq]`.

```text
  evict: bucket[1].popitem(oldest) -> key 2
  bucket[1]: [3]              min_freq = 1 (reset by insert)
  bucket[2]: [1]
  freq_of:   {1:2, 3:1}
```

Key 2 had the smallest count; eviction happened before key 3 was inserted.

Frame 4 — `get(2)` returns -1; `get(3)` returns 3.

```text
  bucket[1]: (empty -> deleted)
  bucket[2]: [1, 3]           min_freq = 2  (jumped f -> f+1)
  freq_of:   {1:2, 3:2}
```

Key 3 left bucket 1, which emptied while it was the minimum, so the minimum became 2 where key 3 just landed.

Frame 5 — `put(4,4)`: full, evict the oldest of `bucket[2]`.

```text
  evict: bucket[2].popitem(oldest) -> key 1
  bucket[1]: [4]              min_freq = 1
  bucket[2]: [3]
  freq_of:   {3:2, 4:1}
```

Keys 1 and 3 tied at count 2; key 1 had reached bucket 2 earlier, so it was the LRU of that bucket.

Frame 6 — `get(1)` returns -1; `get(3)` returns 3.

```text
  bucket[1]: [4]              min_freq = 1
  bucket[3]: [3]              (bucket[2] emptied, deleted;
  freq_of:   {3:3, 4:1}        2 was not the min, no change)
```

Bucket 2 emptied but `min_freq` was 1, so it stayed 1.

In every frame, each key appeared in exactly one bucket matching its count, each bucket was oldest-first, empty buckets were deleted, and `min_freq` named a non-empty bucket whenever the cache was non-empty.

## Why it is correct

Invariant, true after every operation:

- (a) `freq_of[k] = f` iff k is a key of `bucket[f]`, and the stored value is k's latest value.
- (b) Within `bucket[f]`, keys are ordered by the time they *entered* that bucket, oldest first. Because a key enters `bucket[f]` exactly when it is used for the f-th time and leaves on the next use, entry order equals last-use order among keys with count f.
- (c) No bucket is empty, and if the cache is non-empty, `min_freq` is the smallest f with a bucket.

Touching key k with count f removes it from `bucket[f]` and appends it as newest in `bucket[f+1]`: (a) and (b) hold. If `bucket[f]` emptied, it is deleted. For (c): if f was the minimum and the bucket emptied, every other key has count `>= f+1`, and k has exactly f+1, so f+1 is the minimum. Otherwise the minimum is untouched.

Eviction takes the first key of `bucket[min_freq]`. By (c) that bucket holds exactly the keys of smallest count, and by (b) its first key is the least recently used among them, which is precisely the problem's victim. Inserting a new key puts it in `bucket[1]` as newest and sets `min_freq = 1`, which is correct because 1 is the smallest possible count.

## Cost

- Time: O(1) per `get` and `put`. Every step is a dict lookup, an `OrderedDict` pop or append, or `popitem(last=False)`, all O(1); `min_freq` is updated, never searched.
- Space: O(capacity): each key appears once in `freq_of` and once in one bucket; there are at most capacity non-empty buckets.

For comparison, a heap keyed by `(count, tick)` would also work, at O(log n) per operation with lazy deletion of stale entries. The bucket design is strictly better and not much more code.

## Variations you will meet

- **LRU Cache (previous problem).** The degenerate case where every key is in one bucket; the bucket design collapses to a single ordered list.
- **Hand-built buckets.** Without `OrderedDict`, each bucket is a doubly linked list with sentinels, and the buckets themselves may be kept in a linked list ordered by count. That is exactly the design of the next problem, All O`one.
- **Frequency with decay.** If counts should age (recent use matters more), counts no longer move only by +1, the `min_freq` trick breaks, and a heap or periodic halving of counts is used instead.
- **Top-k most frequent keys online.** The same buckets, read from the highest count downward, answer it without sorting.

## What to carry forward

When a ranking key only changes by +1, group items into buckets by that key, keep any tie-break order inside each bucket, and track the extreme bucket with one integer that moves predictably. The next problem, All O`one, lets counts go *down* as well as up and asks for both the minimum and the maximum, so the buckets themselves must become nodes in a doubly linked list.
