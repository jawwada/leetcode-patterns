# Snapshot Array
*LeetCode 1146 · Medium · Pattern: Sorted version list + binary search · Reading time ~8 min*

## What the problem is really asking

You hold an array of `length` zeros. You can `set(index, val)` like any array. At any moment you can call `snap()`, which freezes the current contents and hands you a ticket number: 0 for the first snapshot, 1 for the second, and so on. Later, `get(index, snap_id)` asks what that cell held at the moment ticket `snap_id` was issued.

The answer to each query is a single integer. What makes it hard is the scale: the array can be large (tens of thousands of cells) and there can be tens of thousands of snaps, so anything that touches the whole array per snap is too slow and too big.

```text
  SnapshotArray(3), then: set(0,5), snap()->0, set(0,6)

                  cell0  cell1  cell2
  snapshot 0:       5      0      0
  current:          6      0      0     (not frozen yet)

  get(0, 0) -> 5    (the frozen value, not the current 6)
```

## Do it by hand first

Imagine the array as a row of boxes, and every time you change a box you write the change on a sticky note attached to that box: "during snapshot period k, I became v". The period number is simply "how many snaps have happened so far".

```text
  period:     0              1
  ops:    set(0,5) snap  set(0,6) set(0,7) set(2,1) snap

  notes on box 0:  [ (0,5) , (1,7) ]   (6 was overwritten by 7
                                        inside the same period)
  notes on box 1:  [ (0,0) ]           (never touched)
  notes on box 2:  [ (0,0) , (1,1) ]
```

To answer "box 0 at snapshot 0", you read box 0's notes and take the last one whose period is `<= 0`: value 5. Your hand kept track of *per-cell change logs keyed by period*. Unchanged cells cost nothing extra.

## The first honest attempt

Keep the current array, and on every `snap()` copy the entire array into a list of frozen copies. `get` just indexes `copies[snap_id][index]`.

Gets and sets are O(1), but snap is O(length), and memory is O(snaps x length). With 50,000 cells and 50,000 snaps that is 2.5 billion integers.

The waste is copying cells that did not change:

```text
  copy 0:  [ 5 0 0 0 0 0 0 0 0 0 ]
  copy 1:  [ 7 0 1 0 0 0 0 0 0 0 ]
  copy 2:  [ 7 0 1 0 0 0 0 0 0 0 ]   <- nothing changed,
  copy 3:  [ 7 0 1 0 0 0 0 0 0 3 ]      full copy anyway
             ^   ^ ^ ^ ^ ^ ^ ^ ^
             most columns are the same number repeated
```

Read any column top to bottom and it is long runs of the same value. We are storing every run element instead of just the moments the run changes.

## The turning point

**Claim: store changes, not copies. Each cell keeps a list of `(snap_id, value)` pairs, one per snapshot period in which it was written, and that list is sorted by construction.**

Why sorted: writes during period k are tagged k, and the current period number only ever increases (each `snap()` bumps it by one). So appending a new pair always appends a larger snap id. This is the same "append keeps it sorted" gift the previous problem got from increasing timestamps, except that here we manufacture the clock ourselves.

Why it answers queries: the value of a cell at snapshot k is the value of its last write during a period `<= k`. That is "the last pair with `snap_id <= k`", which is a right bisect, exactly like "largest timestamp `<= t`".

Two details turn this into a tight design.

1. **Overwrite within a period.** If a cell is set several times before the next `snap()`, only the last value can ever be observed. So if the last pair's period equals the current period, replace it instead of appending. That bounds each list's length by the number of periods in which the cell actually changed.
2. **Seed with `(0, 0)`.** Every cell starts as zero. Seeding each list with `(0, 0)` means every bisect finds at least one pair, so there is no "nothing to the left" case. A `set` during period 0 simply overwrites the seed.

The search key needs care because the list holds tuples. We want every pair with first component `<= k` to fall left of the cut, whatever its value. Bisecting on `(k, +inf)` does that: `(k, v) < (k, +inf)` for any value v.

`snap()` itself becomes trivial: increment the period counter and return the old value. O(1), no copying at all.

## Watch it work

Operations on `SnapshotArray(3)`: `set(0,5)`, `snap()`, `set(0,6)`, `set(0,7)`, `set(2,1)`, `snap()`, then a few gets.

Frame 1 — initial state.

```text
  snap_id (current period) = 0
  hist[0] = [ (0,0) ]
  hist[1] = [ (0,0) ]
  hist[2] = [ (0,0) ]
```

Every cell is seeded with "period 0, value 0".

Frame 2 — `set(0,5)` then `snap()` returns 0.

```text
  hist[0] = [ (0,5) ]      seed overwritten (same period 0)
  hist[1] = [ (0,0) ]
  hist[2] = [ (0,0) ]
  snap_id = 1              snap() returned 0
```

The write landed in period 0, so it replaced the seed; the snap only moved the counter.

Frame 3 — `set(0,6)`, `set(0,7)`, `set(2,1)`.

```text
  hist[0] = [ (0,5) , (1,6) ]   after set(0,6): appended
  hist[0] = [ (0,5) , (1,7) ]   after set(0,7): overwrote
  hist[2] = [ (0,0) , (1,1) ]   appended
  hist[1] = [ (0,0) ]           untouched
```

The 6 never survives to a snapshot, so it is overwritten in place rather than stored.

Frame 4 — `snap()` returns 1; the state is now frozen as follows.

```text
  snap_id = 2
            period: 0      1
  hist[0] = [ (0,5) , (1,7) ]
  hist[1] = [ (0,0) ]
  hist[2] = [ (0,0) , (1,1) ]
```

Again the snap copied nothing; it only advanced the counter.

Frame 5 — gets.

```text
  get(0,0): bisect hist[0] for (0,+inf) -> cut 1 -> (0,5) -> 5
  get(0,1): bisect hist[0] for (1,+inf) -> cut 2 -> (1,7) -> 7
  get(1,1): bisect hist[1] for (1,+inf) -> cut 1 -> (0,0) -> 0
  get(2,0): bisect hist[2] for (0,+inf) -> cut 1 -> (0,0) -> 0
```

Each get is a right bisect and a step back, and the seed guarantees the step back exists.

Throughout, every per-cell list stayed sorted by period, had at most one pair per period, and never contained a pair for a period in which the cell was untouched.

## Why it is correct

Invariant: for every cell, `hist[i]` is sorted by strictly increasing period; its last pair for period p holds the last value written to cell i during period p; and the first pair has period 0 (the seed or a period-0 write that replaced it).

`set` either overwrites the last pair (if it has the current period) or appends a pair with the current period, which is larger than every period already present. Both preserve the invariant. `snap` changes no list.

For `get(i, k)`: the true value at snapshot k is the last value written to cell i in any period `<= k`, or 0 if none. Periods `<= k` are exactly the pairs left of the cut at `(k, +inf)`; the rightmost of them is the latest period `<= k`, and by the invariant it holds that period's last write. If no write happened in periods `<= k`, the rightmost such pair is the seed, value 0. Either way we return the right number.

## Cost

- Time: `set` O(1), `snap` O(1), `get` O(log m) where m is the number of periods in which that cell changed.
- Space: O(length + number of sets), one seed per cell plus at most one pair per set.

The brute force was O(length) per snap and O(snaps x length) space; the change log cuts both to what was actually written.

## Variations you will meet

- **Lazy seeding.** For a huge array with few writes, use a dict of lists and treat a missing cell as `[(0,0)]`. Space drops to O(number of sets).
- **Persistent segment tree.** If queries ask for a range sum "as of snapshot k", per-cell logs are not enough; a persistent segment tree shares unchanged subtrees across versions, O(log n) new nodes per write.
- **Time Based Key-Value Store (previous problem).** Same per-key timeline; there the clock comes from the caller and there is no "same period" overwrite.
- **Rollback / undo to snapshot k.** Truncate every list past period k. Doing that lazily (store a "current base" and ignore newer pairs) avoids touching every cell.

## What to carry forward

Snapshots of mostly-unchanged data are cheap if you log changes per cell and let a monotone counter keep each log sorted; reading the past is a right bisect. The next problem, Design Bitset, keeps the idea of not touching every cell, but replaces "remember every version" with a single lazy flag that reinterprets the whole array at once.
