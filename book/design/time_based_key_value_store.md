# Time Based Key-Value Store
*LeetCode 981 · Medium · Pattern: Sorted version list + binary search · Reading time ~8 min*

## The problem

Implement TimeMap: set(key, value, timestamp) stores a value for key at that time, and get(key, timestamp) returns the
value whose timestamp is the largest one <= timestamp, or '' if none. All timestamps passed to set are strictly
increasing.

```text
Example: set('foo','bar',1); get('foo',1) -> 'bar'; get('foo',3)
  -> 'bar'; set('foo','bar2',4); get('foo',4) -> 'bar2';
  get('foo',5) -> 'bar2'; get('foo',0) -> ''.
```

## What the problem is really asking

You are building a dictionary that never forgets. Every `set(key, value, timestamp)` does not overwrite the old value; it adds a new *version* of the key, stamped with a time. A `get(key, t)` asks: "what did this key hold at time `t`?" That means the value from the most recent `set` whose timestamp is at or before `t`. If the key had not been written yet at time `t`, the answer is the empty string.

So the answer to each query is one value, but finding it means locating a *boundary* inside a timeline: the last version that is not in the future relative to `t`.

```text
key "foo" as a timeline (time runs right)

  time:   0   1   2   3   4   5   6   7   8   9  10
              |           |                   |
             "a"         "b"                 "c"

  get(foo, 5): stand at 5, look LEFT, first mark you hit
               is at 4 -> "b"
  get(foo, 0): nothing to the left of 0 -> ""
```

One sentence in the statement changes everything: the timestamps passed to `set` are strictly increasing. Keep it in mind; it is the whole problem.

## Do it by hand first

Suppose the history of `foo` is written in a notebook, one line per `set`, in the order the calls came in:

```text
  line   time   value
   1      1      "a"
   2      4      "b"
   3      9      "c"
```

Someone asks "what was `foo` at time 5?" Your finger does not read every line. Because the times only grow down the page, you run your finger down until you hit a time that is *too big* (9 > 5), then step back one line: time 4, value "b". If the very first line is already too big, there is nothing before it, and the answer is empty.

What your hand kept track of was a *sorted column of times*, and the question it answered was "where would 5 slot into this column?" That slot position, minus one, is the answer row. The data structure is exactly that column.

## The first honest attempt

Store, for each key, a list of `(timestamp, value)` pairs. `set` appends a pair. `get` walks the whole list and keeps the best pair whose time is `<= t`.

That is O(1) per `set` and O(n) per `get`, where n is the number of versions of that key. With many versions and many queries it is O(n) per query forever.

Where is the waste? The scan compares `t` against every version, including all those far in the past (which can never beat a later one that is also `<= t`) and all those in the future (which are disqualified anyway):

```text
  get(foo, 5) on 8 versions, linear scan:

  times:  1   4   9   12  15  20  31  40
          ?   ?   ?   ?   ?   ?   ?   ?     8 comparisons
          ok  ok  no  no  no  no  no  no
              ^ the only one that matters
```

Every query re-discovers the same ordering that was already there when the versions were written.

## The turning point

**Claim: each key's list of timestamps is already sorted, for free, so "largest timestamp `<= t`" is one binary search.**

Justification: `set` timestamps strictly increase across all calls. So within one key, each new version is stamped later than every earlier version of that key. Appending to the end therefore keeps the list in ascending order. We never sort, we never insert in the middle, we never need a balanced tree.

On a sorted list, the question "last element `<= t`" is the classic *right bisect*. `bisect_right(times, t)` returns the first index whose time is strictly greater than `t`. Everything to the left of that index is `<= t`, and the element just before it is the largest such one.

```text
  times: [ 1 , 4 , 9 ]
  index:   0   1   2   3

  bisect_right(times, 5) = 2   (9 is the first > 5)
  answer index = 2 - 1 = 1  -> vals[1] = "b"

  bisect_right(times, 4) = 2   (equal goes LEFT of the cut)
  answer index = 1          -> "b"   exact hit included

  bisect_right(times, 0) = 0   -> nothing left of the cut -> ""
```

Two practical choices make this clean. First, keep two *parallel* lists per key, `times[key]` and `vals[key]`, so the bisect runs over plain integers instead of tuples (tuple comparison would fall back to comparing the string values on a tie, which is never what you want). Second, use `bisect_right`, not `bisect_left`: with `bisect_left`, a query at exactly a stored timestamp would land *on* that version and stepping back would skip it.

The structure, then, is a hash map from key to a pair of append-only sorted arrays. The invariant that turns the claim into an algorithm is simply "append keeps it sorted".

## Watch it work

Operations: `set(foo,a,1)`, `set(foo,b,4)`, `set(foo,c,9)`, `get(foo,5)`, `get(foo,0)`, `get(foo,9)`.

Frame 1 — after `set(foo, a, 1)`.

```text
  times["foo"] = [ 1 ]
  vals ["foo"] = [ a ]
```

The key is new, so both lists start with one entry.

Frame 2 — after `set(foo, b, 4)` and `set(foo, c, 9)`.

```text
  times["foo"] = [ 1 , 4 , 9 ]
  vals ["foo"] = [ a , b , c ]
                   0   1   2
```

Each set appended to the end; the times are ascending without any work.

Frame 3 — `get(foo, 5)`.

```text
  times: [ 1 , 4 , 9 ]
                  | cut: bisect_right(5) = 2
                ^ i - 1 = 1
  returns vals[1] = "b"
```

The cut lands before 9, and the version just left of it answers.

Frame 4 — `get(foo, 0)`.

```text
  times: | 1 , 4 , 9 ]
         cut: bisect_right(0) = 0
  nothing to the left -> returns ""
```

The query time is before the first version, so `i == 0` and we return empty.

Frame 5 — `get(foo, 9)`.

```text
  times: [ 1 , 4 , 9 |
                      cut: bisect_right(9) = 3
                ^ i - 1 = 2 -> "c"
```

An exact match goes to the left of the cut, so the version written at time 9 is included.

Across all frames the lists only grew at the right end, and they stayed sorted the whole time. Every query was a cut in a sorted list plus one step left.

## Why it is correct

Invariant: for every key, `times[key]` is strictly increasing and `vals[key][i]` is the value written at `times[key][i]`.

It holds initially (empty lists). A `set` appends a timestamp larger than every timestamp ever passed before, so in particular larger than the last element of this key's list; strict increase is preserved, and the value is appended at the same index, so alignment is preserved.

Given the invariant, `bisect_right(times, t)` returns the unique index `i` such that every element before `i` is `<= t` and every element from `i` on is `> t`. The versions that are legal answers are exactly those at indices `< i`, and since the list is increasing, the largest of them is at `i - 1`. If `i == 0` there are no legal versions and the empty string is correct. A key never set is not in the map and also returns empty.

## Cost

- Time: `set` is O(1) amortised, one append to each of two lists. `get` is O(log n) for the key's n versions, one binary search.
- Space: O(total number of `set` calls); the problem requires keeping every version, so this is the floor.

## Variations you will meet

- **Timestamps not increasing.** If `set` can arrive out of order, appending breaks sortedness. Use `insort` (O(n) insertion) for rare out-of-order writes, or a sorted container / balanced tree for O(log n) inserts. The query side is unchanged.
- **Same timestamp written twice.** If allowed, decide whether the later write overwrites. With parallel lists you check `times[-1] == t` and overwrite in place; the next problem uses exactly this trick.
- **Range queries ("all values between t1 and t2").** Two bisects, `bisect_left(t1)` and `bisect_right(t2)`, give a slice of the version list.
- **Deleting old history (TTL).** If versions older than some horizon can be dropped, a deque per key with pops from the left keeps it sorted and bounded.

## What to carry forward

Versioned data is a sorted timeline per key, and "value as of time t" is a right bisect minus one. The next problem, Snapshot Array, applies the same timeline to every cell of an array, where the "time" is a snapshot counter that we advance ourselves.
