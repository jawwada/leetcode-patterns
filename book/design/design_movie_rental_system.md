# Design Movie Rental System

*LeetCode 1912 · Hard · Pattern: Heaps with lazy deletion by version stamp · Reading time ~13 min*

## What the problem is really asking

A chain has n shops. Each entry `[shop, movie, price]` says that shop owns one copy of that movie, at that price. A copy
is in one of two states: on the shelf (available) or out (rented). Four operations:

- `search(movie)`: up to 5 shops with an available copy of this movie, cheapest first, ties by smaller shop id.
- `rent(shop, movie)`: that copy moves from shelf to out.
- `drop(shop, movie)`: that copy moves back from out to shelf.
- `report()`: up to 5 rented copies as `[shop, movie]`, cheapest first, ties by shop, then by movie.

So the answer objects are short sorted lists, "top 5 by (price, shop)" over two families of sets: one available-set per
movie, and one global rented-set. What makes it hard is that copies keep moving between the sets while the top-5 queries
keep coming.

```text
entries: shop movie price
          0    1     5
          0    2     6
          0    3     7
          1    1     4
          1    2     7
          2    1     5

shelf, movie 1:  (4,s1) (5,s0) (5,s2)   search(1) -> [1,0,2]
shelf, movie 2:  (6,s0) (7,s1)
shelf, movie 3:  (7,s0)
out:             empty                  report()  -> []
```

## Do it by hand first

Imagine index cards. For each movie, a pile of cards for its available copies, kept sorted by price then shop. One more
pile for rented copies, sorted by price, shop, movie. To `rent(0,1)`, you pull shop 0's card out of the movie-1 pile
and slide it into the rented pile at the right spot. `search` reads the first five cards of a pile.

```text
rent(0,1):
  movie-1 pile  (4,s1) (5,s0) (5,s2)
                        |
                        v move card
  rented pile   (5,s0,m1)
  movie-1 pile  (4,s1) (5,s2)
```

What the hand maintained is a sorted collection per state, with three operations: insert a card, remove a specific
card, read the first five. Any language with a sorted set (Java's TreeSet, C++'s set) does exactly this in O(log n).
Python's standard library has no sorted set, and that is where the design gets interesting.

## The first honest attempt

Keep a dict `(shop, movie) -> [price, rented]`. Rent and drop flip the flag, O(1). Search filters all entries for that
movie that are not rented and sorts them; report filters all rented entries and sorts them. That is O(E log E) per
query in the worst case, with E up to 10^5 entries and 10^5 calls.

The waste: between two consecutive queries, one copy moved. The query sorts everything again.

```text
report():  sort all rented -> (5,s0,m1) (7,s1,m2)
rent(2,1)
report():  sort all rented -> (5,s0,m1) (5,s2,m1) (7,s1,m2)
                              ~~~~~~~~~           ~~~~~~~~~
                              already in order last time
```

A heap fixes "read the smallest" and "insert" in O(log n). What a heap cannot do is remove an arbitrary element: when a
copy is rented, its entry is buried somewhere in the middle of the shelf heap, and finding it is O(n).

## The turning point

**Claim: you never need to remove an entry from a heap at the moment it becomes invalid; it is enough to recognise it
as invalid when it reaches the top, provided every entry carries a stamp that says which version of its copy it
describes.**

This is lazy deletion. Leave dead entries in the heap. Whenever a query pops from the top, check whether the popped
entry is still true; if not, throw it away for good and pop again. Every dead entry is popped at most once, so the
cleanup is paid for by the push that created it.

The subtle part is the "is it still true" check. The obvious test is "is this copy currently rented?" Look at what
happens with rent followed by drop:

```text
avail[1] heap, test = "copy not rented"
start:      (5,s0)
rent(0,1):  (5,s0)            entry left behind
drop(0,1):  (5,s0) (5,s0)     drop pushes a fresh entry
search(1):  both pass "not rented" -> shop 0 listed twice
```

The old entry looks valid again because the copy happens to be back on the shelf. It is a ghost of a previous stay.
The fix is to make every stay distinguishable:

- `ver[(shop, movie)]` starts at 0 and is incremented on every rent and every drop.
- Every heap entry stores the version that was current when it was pushed.
- An entry is alive iff its stored version equals the current `ver`.
- Each state change pushes exactly one new entry, with the new version, into the heap the copy now belongs to.

Since only the latest push carries the current version, at any moment each copy has exactly one live entry, and it is
in the right heap. Everything else is stale and will be discarded when it surfaces.

```text
copy (0,1): ver timeline
  ver 0: on shelf   entry (5,s0,v0) in avail[1]
  rent  -> ver 1:   entry (5,s0,m1,v1) in out
  drop  -> ver 2:   entry (5,s0,v2) in avail[1]
  alive now: only the v2 entry; v0 and v1 are stale
```

The query routine is shared. Pop until you have 5 live entries or the heap is empty, discarding stale ones permanently.
Then push the live ones back, because the query must not change the state.

```text
_top5(heap):
  kept = []
  while heap and len(kept) < 5:
      e = pop(heap)
      if alive(e): kept.append(e)      # stale: dropped
  for e in kept: push(heap, e)         # restore
  return kept
```

The tuple layout gives the tie rules for free: `(price, shop, ver)` per movie for search, and
`(price, shop, movie, ver)` for report, both compared lexicographically by the heap.

## Watch it work

The example from the statement, extended with `drop(0,1)`, `report()`, `search(1)` to show the ghost being caught.
`ver` values not shown are 0.

Frame 1: construction, then `search(1)`.

```text
avail[1]: (4,s1,0) (5,s0,0) (5,s2,0)
avail[2]: (6,s0,0) (7,s1,0)
avail[3]: (7,s0,0)
out:      empty
search(1): pops 3 live entries, pushes them back
-> [1, 0, 2]
```

Every entry starts at version 0, which matches `ver`, so all are alive.

Frame 2: `rent(0,1)`, `rent(1,2)`.

```text
ver: (0,1)=1  (1,2)=1
avail[1]: (4,s1,0) (5,s0,0)* (5,s2,0)
avail[2]: (6,s0,0) (7,s1,0)*
out:      (5,s0,m1,1) (7,s1,m2,1)
                    * = stale (stamp 0 != ver 1)
```

Nothing is removed from the shelves; two entries silently became stale, and `out` gained two live entries.

Frame 3: `report()`.

```text
pop (5,s0,m1,1): ver(0,1)=1 live
pop (7,s1,m2,1): ver(1,2)=1 live
heap empty, push both back
-> [[0,1], [1,2]]
```

Both rented entries are current.

Frame 4: `drop(1,2)`.

```text
ver: (1,2)=2
avail[2]: (6,s0,0) (7,s1,0)* (7,s1,2)
out:      (5,s0,m1,1) (7,s1,m2,1)*
```

A fresh entry with stamp 2 goes onto the shelf; the `out` entry with stamp 1 is now stale.

Frame 5: `search(2)`.

```text
pop (6,s0,0): ver(0,2)=0 live    keep
pop (7,s1,0): ver(1,2)=2 stale   discard
pop (7,s1,2): ver(1,2)=2 live    keep
push back kept
avail[2]: (6,s0,0) (7,s1,2)
-> [0, 1]
```

The stale entry is gone for good; the heap is cleaner after the query than before it.

Frame 6: `drop(0,1)`, then `report()`.

```text
drop: ver(0,1)=2, push (5,s0,2) to avail[1]
report:
  pop (5,s0,m1,1): ver(0,1)=2 stale  discard
  pop (7,s1,m2,1): ver(1,2)=2 stale  discard
out: empty  -> []
```

Both rented entries surface as stale and are discarded, so `report()` correctly shows nothing rented.

Frame 7: `search(1)`, the ghost test.

```text
avail[1]: (4,s1,0) (5,s0,0) (5,s0,2) (5,s2,0)
pop (4,s1,0): live          keep
pop (5,s0,0): ver(0,1)=2    stale, discard
pop (5,s0,2): live          keep
pop (5,s2,0): live          keep
-> [1, 0, 2]   (a rented-flag test would give [1,0,0,2])
```

Shop 0 appears once: the version stamp told the old stay apart from the current one.

Across all frames, every copy had exactly one entry whose stamp matched `ver`, and that entry sat in the heap matching
the copy's state. Queries only ever removed stale entries and returned live ones in heap order.

## Why it is correct

Invariant: for each copy, exactly one entry in all the heaps has stamp equal to `ver[copy]`, and it is in `avail[movie]`
if the copy is on the shelf, in `out` if rented. All other entries for the copy have smaller stamps.

Initially every copy has one entry with stamp 0 in its shelf heap and `ver` = 0. A rent or drop increments `ver`, which
makes the previous live entry stale, and pushes one entry with the new stamp into the heap for the new state. The
invariant holds again. A query pops and discards only stale entries, and pushes back exactly the live entries it
popped, so it does not change the set of live entries.

A query pops in heap order, so the live entries it collects are the smallest live entries by the tuple order, which is
the required sort. Stale entries are skipped, so they cannot appear in an answer, and since each copy has at most one
live entry no copy is listed twice.

## Cost

- `rent`, `drop`: one push, O(log H) where H is the heap size.
- `search`, `report`: up to 5 live pops and 5 pushes, plus some stale pops. Each stale entry was created by one rent or
  drop and is popped at most once, so the stale pops are amortised against those operations: O(log H) amortised per
  operation.
- Space: O(E + number of rent/drop calls), since stale entries can linger until they surface.

With a real sorted set (TreeSet, `sortedcontainers.SortedList`), every operation is O(log E) worst case and no stamps
are needed.

## Variations you will meet

- **Design Twitter, Top K Frequent Words.** Top-k by a key over a changing collection: a heap plus lazy invalidation, or
  a merge of per-user sorted streams.
- **Sliding Window Median, The Skyline Problem.** Lazy deletion again: elements leaving the window, or buildings that
  ended, stay in the heap until they reach the top. There, a "has this ended?" test is enough, because an element never
  comes back. The version stamp is what you add when it can come back.
- **Using a sorted container.** In an interview with `sortedcontainers` allowed, keep `SortedList` per movie and one for
  rented, and `rent` becomes `remove` plus `add`. Say so, and explain that the heap version is the stdlib-only plan.
- **Price changes.** If a copy's price can change, a stamp still works: bump `ver` and push a new entry with the new price.

## What to carry forward

When a heap cannot delete, delete lazily, and when an item can leave and come back, stamp each stay with a version so
ghosts of earlier stays never pass the liveness test. The next problem, Design In-Memory File System, leaves ordering
behind and asks you to store a hierarchy, where every operation becomes a walk down a tree of dictionaries.
