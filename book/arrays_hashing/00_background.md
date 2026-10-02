# Arrays and Hashing

*17 problems · Reading time ~16 min*

## Why this chapter exists

Almost every array problem, stripped down, is a question about what you have already seen. "Is there an earlier number
that completes this sum?" "Was this value here a few steps ago?" "Have I met a word with these same letters before?" The
slow answer re-reads the array to find out. The fast answer remembers, in a structure that can be asked "have I seen X?"
in constant time. This chapter is about building that memory and choosing what to remember.

The seventeen problems fall into a few families:

- **Remember what you have seen.** A dict or set fed one element at a time answers lookups about the past (two sum,
  contains duplicate II, valid sudoku, longest consecutive sequence).
- **Remember a summary, not the items.** Sometimes one or two numbers carry everything that matters (majority element,
  max consecutive ones).
- **Group by a canonical key.** Map every item to a fingerprint that is equal exactly when the items are "the same" (group
  anagrams, encode and decode strings).
- **Count, then use counts as positions.** Frequencies are small integers, so they can be array indices (top k frequent
  elements, maximum gap, contains duplicate III).
- **Prefix accumulation.** Store running totals so any range is a difference or a product of two of them (product of
  array except self, subarray sum equals k).
- **The array is its own hash table.** When values fit in the index range, park value `v` at index `v - 1` (first missing
  positive).
- **Count across the order of the array.** "How many earlier/later elements are smaller?" needs merge sort or a Fenwick
  tree over values (count of smaller numbers after self, reverse pairs, create sorted array through instructions).

## What it is

### The array

An array is one contiguous block of memory, cut into equal-sized slots. If the block starts at address `base` and each slot
is `w` bytes, slot `i` lives at `base + i * w`. That is one multiplication and one addition, whatever `i` is. This is why
reading `a[i]` costs O(1): the machine does not walk to slot `i`, it computes where slot `i` is.

```text
address:  1000  1008  1016  1024  1032     (w = 8 bytes)
        +-----+-----+-----+-----+-----+
  a     |  3  |  8  |  5  |  2  |  9  |
        +-----+-----+-----+-----+-----+
index:     0     1     2     3     4

a[3] -> base + 3*8 = 1000 + 24 = 1024 -> 2
```

(A Python list stores pointers to objects in those slots rather than the numbers themselves, but the arithmetic is the
same, and indexing is still O(1).)

The catch is the other direction. Indexing goes from position to value for free. Going from value to position, "where is
the 5?", has no formula. You must look at slots one by one: O(n). And "have I seen X?" is exactly a value-to-position
question. That asymmetry is the whole reason this chapter exists.

### Making value-to-position cheap: hashing

The trick is to invent a formula from value to position. A **hash function** turns any key into an integer; we then reduce
that integer to a slot number with `hash(key) % m`, where `m` is the number of slots (called **buckets**). To store a key,
compute its bucket and put it there. To look it up, compute the same bucket and look only there.

```text
m = 8 buckets, hash(int) = the int itself (true in Python)

insert 3   -> 3  % 8 = 3
insert 8   -> 8  % 8 = 0
insert 5   -> 5  % 8 = 5
insert 11  -> 11 % 8 = 3   collision with 3!

bucket: 0     1    2    3          4    5    6    7
      +----+----+----+----------+----+----+----+----+
      | 8  |    |    | 3 -> 11  |    | 5  |    |    |
      +----+----+----+----------+----+----+----+----+
```

Two different keys landing in the same bucket is a **collision**, and it is unavoidable: there are more possible keys
than buckets. The simplest fix, **chaining**, lets each bucket hold a short list. A lookup computes the bucket, then walks
that list comparing keys with `==`. CPython's dict and set actually use **open addressing** (on a collision, probe
another slot by a fixed rule), but the cost story is identical, so picture chains.

### Why lookups are O(1) on average

The cost of a lookup is the length of the chain you walk. Define the **load factor** as `n / m`, keys per bucket. If
the hash spreads keys evenly, the average chain has length `n / m`. Keep that ratio below a constant and the average
chain is short no matter how big `n` gets.

The table keeps it below a constant by **resizing**: when `n / m` crosses a threshold (CPython uses about 2/3), it
allocates a table roughly twice as large and re-inserts every key, since `% m` has changed.

```text
before (m = 4, n = 3, load 0.75 -> too full)
  0:[8]  1:[]  2:[]  3:[3, 11]

after resize (m = 8): every key re-hashed
  0:[8]  1:[]  2:[]  3:[3, 11]  4:[]  5:[]  6:[]  7:[]
                     (3 and 11 still collide mod 8)
```

Two honest caveats. "Average" assumes keys spread out; a nasty input can push many keys into one bucket and a lookup
degrades to O(n). For interview inputs this does not happen, and we write O(1). Second, a key must be **hashable**: its
hash must never change while it sits in the table, otherwise it would be looked for in the wrong bucket. That is why
Python refuses lists as keys and accepts tuples.

### What "amortised" means

A resize costs O(n), which looks like it ruins O(1) inserts. It does not, because resizes are rare. Doubling from 1 to 2
to 4 ... to `n` copies `1 + 2 + 4 + ... + n < 2n` keys in total across all resizes. Spread those `2n` copies over `n`
inserts and each insert pays about 2 extra copies. "Amortised O(1)" means exactly this: any single operation may be
expensive, but a sequence of `n` operations costs O(n) in total.

```text
insert #:   1  2  3  4  5  6  7  8  9 ...
copy cost:  0  1  2  0  4  0  0  0  8 ...
            ^  ^  ^     ^           ^ resizes (double)
running total of copies always < 2 * inserts
```

The same word appears in this chapter for algorithms, not just tables. In longest consecutive sequence an inner `while`
loop looks quadratic, yet across the whole run it touches each element once. Charging work to the element that causes it,
not to the loop iteration, is amortised thinking.

## Operations and what they cost

| Operation | Cost | Why |
|---|---|---|
| `a[i]` read or write | O(1) | address = base + i * w |
| `x in list` | O(n) | no formula from value to slot; scan |
| `list.append(x)` | O(1) amortised | occasional doubling, paid off over many appends |
| `list.insert(0, x)` | O(n) | every element shifts right by one |
| `d[key]`, `key in d`, `s.add(x)` | O(1) average | hash to one bucket, compare a few keys |
| `del d[key]` | O(1) average | same bucket lookup |
| Iterate a dict or set | O(n) | visit every stored key |
| Build `Counter(a)` or `set(a)` | O(n) | n inserts |
| `sorted(a)` | O(n log n) | comparison sort |
| Prefix sums of length n | O(n) build, O(1) query | each total extends the previous one |

Lookup in a hash table, drawn:

```text
"is 11 in the table?"
  hash(11) % 8 = 3
  bucket 3: [3 -> 11]
             ^    ^
           3==11? no   11==11? yes -> found
  buckets 0,1,2,4..7 never looked at
```

A prefix sum, drawn. `P[i]` is the sum of the first `i` elements, so `P` has one extra slot at the front:

```text
index:      0   1   2   3   4
a:        [ 3,  8,  5,  2 ]
P:        [ 0,  3, 11, 16, 18 ]
                 ^           ^
sum of a[1..3] = 8+5+2 = P[4] - P[1] = 18 - 3 = 15
```

Any range sum becomes one subtraction. The same idea with multiplication gives prefix products (product of array except
self), and the same idea combined with a hash map of earlier `P` values counts subarrays with a given sum.

A canonical key, drawn. Anagrams differ in order, so remove order:

```text
"eat" --sort--> "aet"     "eat" --count--> (1,0,0,0,1,..,1,..)
"tea" --sort--> "aet"     "tea" --count--> (1,0,0,0,1,..,1,..)
"tan" --sort--> "ant"                       a       e     t
equal key  <=>  same group
```

The index-as-hash trick, drawn. If the values you care about are `1..n` and the array has `n` slots, slot `v - 1` is a
perfect, collision-free bucket for `v`:

```text
values:   [ 3, 4, -1, 1 ]    n = 4, care about 1..4
park v at index v-1:
index:      0   1   2   3
          [ 1, -1,  3,  4 ]
                ^ slot 1 does not hold 2 -> 2 is missing
```

Bucket sort, drawn. When sort keys are small integers in `0..K`, make `K + 1` shelves and drop each item on its shelf;
reading shelves left to right is sorted order, with no comparisons:

```text
item:count   a:3  b:1  c:3  d:2
shelf:   0    1    2    3
       [   ][ b ][ d ][ a c ]   read right to left: a c d b
```

## The invariant

Nearly every one-pass solution here protects one sentence:

> When you stand at index `i`, the structure summarises exactly `a[0..i-1]`: everything to the left, nothing to the right,
> and not the current element.

Check-then-insert is how you keep it. You query the structure about `a[i]` first (it knows only the past), then fold `a[i]`
in so the next step sees it.

```text
LEGAL at i = 2  (two sum, target 10)
  a:     3   8  [5]  2
  seen: {3:0, 8:1}          left part only; 5 not yet inserted
  ask "is 10-5 = 5 in seen?" -> no (correct: only one 5)

ILLEGAL at i = 2  (inserted before checking)
  a:     3   8  [5]  2
  seen: {3:0, 8:1, 5:2}     current element leaked in
  ask "is 5 in seen?" -> yes -> pairs index 2 with itself
```

The hash table itself has an internal invariant you rely on without seeing: every key sits in (or on the probe path
from) the bucket its hash names. Mutate a key after inserting it and that invariant breaks silently; that is the
hashability rule from above.

## How to picture it

Picture the array as a conveyor belt moving left to right past you, and the hash table as a notebook on your desk. You
see one item at a time. You may glance in the notebook (O(1)), and you may write in it (O(1)), but you may not turn
around and look at the belt behind you. Every question about the past must be answerable from the notebook. Designing a
solution is deciding what to write: the items themselves (a set), where you last saw them (value to index), how many
times (value to count), or one running number (a sum, a product, a vote tally).

```text
            past (only in notebook)      future
belt:   ... [ 3 ] [ 8 ] [ 5 ]  >[ 2 ]<  [ 9 ] [ 1 ] ...
                                  ^ you
notebook: {3, 8, 5}   or  {3:0, 8:1, 5:2}   or  sum = 16
```

For the harder problems, picture a second image: values laid on a number line, cut into equal buckets. Maximum gap and
contains duplicate III both reason about which bucket a value falls into, so that only neighbouring buckets need
checking.

## Signals in a problem statement

- "Return indices of two numbers that ..." with an unsorted array: complement lookup in a dict.
- "Duplicate", "appears twice", "seen before", "distinct": a set.
- "Within distance k", "at most k apart": store the last index per value, or a window set.
- "Group", "anagram", "same pattern", "equivalent": a canonical key in a dict of lists.
- "Most frequent", "top k", "appears more than n/2": counting; maybe bucket sort over frequencies.
- "Subarray sum equals", "contiguous with total": prefix sums plus a dict of earlier prefixes.
- "Without division", "except self": prefix and suffix accumulation.
- "O(n) time, O(1) extra space" with values in `1..n`: the array is its own hash table.
- "O(n)" where sorting would be natural: buckets or a set replaces the sort.
- "Count elements after/before that are smaller": merge sort counting or a Fenwick tree.

Counter-signals:

- The array is sorted: two pointers or binary search usually beat a hash map and use O(1) space.
- "Longest/shortest contiguous window with a property" and all values positive: sliding window.
- You need order (smallest, next larger, k-th): a heap, a sorted structure, or a balanced tree, not a dict.

## Python toolbox

```python
from collections import Counter, defaultdict
seen = {}                         # value -> index
if target - v in seen: ...        # O(1) average membership
groups = defaultdict(list)        # missing key -> new []
groups[tuple(sorted(w))].append(w)  # tuple: hashable key
freq = Counter(nums)              # value -> count
freq.most_common(k)               # k largest counts, O(n log k)
last = d.get(v, -1)               # default without KeyError
from itertools import accumulate
P = [0, *accumulate(nums)]        # prefix sums, P[0] = 0
```

Quirks worth knowing. `hash(-1) == hash(-2)` in CPython; harmless, it is only a collision. Dicts remember insertion order
(Python 3.7+), but sets do not promise any order, so never depend on set iteration order. `Counter` returns 0 for a
missing key without inserting it; `defaultdict` inserts the default on every read of a missing key, so `if d[k]:` on a
defaultdict quietly grows it. Lists, sets and dicts are unhashable; `tuple` and `frozenset` are hashable.

## Mistakes people make

1. Inserting the current element before checking it, so it pairs with itself. Fix: check, then insert.
2. Using a list as a dict key. Fix: `tuple(lst)` or a joined string.
3. `x in some_list` inside a loop, silently O(n) each time. Fix: build `set(some_list)` once.
4. Storing the first index of a value when the nearest one matters. Fix: overwrite on every sighting.
5. Iterating the original list (with duplicates) instead of the set, repeating work. Fix: loop over the set.
6. Forgetting the empty prefix `P[0] = 0` (or `{0: 1}` in a count map), missing subarrays that start at index 0. Fix:
   seed it before the loop.
7. Bucket array of size `n` when a count can equal `n`. Fix: size `n + 1`.
8. Assuming a dict is O(1) worst case and arguing complexity from it on adversarial input. Fix: say "average".
9. Reading a defaultdict to test membership, which inserts. Fix: use `k in d`.
10. Sorting to "simplify" when the problem demands O(n). Fix: buckets or a set.

## The journey ahead

1. **Two sum.** The template: a dict of the past, queried with a complement, check before insert.
2. **Contains duplicate II.** The dict stores where a value was last seen, and overwriting keeps it nearest.
3. **Majority element.** You do not always need a table: one candidate and one counter can carry the answer.
4. **Max consecutive ones.** The smallest possible memory: one running count that a wall resets.
5. **Valid sudoku.** Many sets at once, and computing which set a cell belongs to.
6. **Group anagrams.** The key is no longer the item: design a canonical key so equal keys mean same group.
7. **Top k frequent elements.** Count with a dict, then use counts as array indices: bucket sort.
8. **Product of array except self.** Prefix and suffix accumulation; "all but one" becomes "left times right".
9. **Longest consecutive sequence.** A set plus a start-of-run test; the first real amortised argument.
10. **Subarray sum equals k.** Prefix sums meet the two sum dict: count earlier prefixes equal to `P - k`.
11. **Encode and decode strings.** A key that cannot be confused: length-prefixed serialisation.
12. **First missing positive.** The array becomes its own hash table via index `v - 1`.
13. **Maximum gap.** Pigeonhole buckets on the number line find the answer without sorting.
14. **Contains duplicate III.** Value buckets of width `t + 1` inside a sliding window of indices.
15. **Count of smaller numbers after self.** Counting pairs across positions with merge sort.
16. **Reverse pairs.** The same merge-sort count, with a condition that differs from the merge order.
17. **Create sorted array through instructions.** Counting by value with a Fenwick tree, the general tool behind 15 and 16.
