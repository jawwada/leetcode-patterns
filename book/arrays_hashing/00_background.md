# Arrays and Hashing

*17 problems · Reading time ~30 min*

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
- **Use numbers as positions.** Frequencies are small integers, so they can be array indices (top k frequent
  elements); values themselves can be cut into buckets on the number line (maximum gap, contains duplicate III).
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

## Advanced patterns

The basic material above has one shape: walk the array once, ask a notebook about the past, write the current
element in. That shape carries you through the Easy and Medium problems. The Hard problems at the end of the chapter
break it in one of two ways. Either the budget forbids the notebook (O(1) extra space, or no sorting allowed), or the
question mixes **two orders at once**: index order ("earlier", "to the right", "within k positions") and value order
("smaller", "within t", "the gap between neighbours"). A hash table is excellent at exact value lookups and useless at
value order, because hashing scatters nearby numbers to unrelated buckets. Each pattern below is a way of handling one
order with structure while the other order is handled by the scan.

### Prefix sums with a hash map of earlier prefixes

**When it shows up**: a question about contiguous subarrays whose sum (or count, or balance) hits an exact target,
especially when values can be negative, which breaks the sliding window.

**The intuition**: a subarray `a[i..j-1]` has sum `P[j] - P[i]`. So "a subarray ending here sums to k" is the same
sentence as "some earlier prefix equals `P[j] - k`". That is two sum again, but run over the prefix array instead of the
input: the complement is `P[j] - k`, and the notebook holds prefixes seen so far. What you store decides what you can
answer. Store a **count** per prefix value and you count subarrays. Store the **first index** where each prefix value
appeared (and never overwrite it) and you get the longest such subarray, because the earliest matching start makes the
widest window. The empty prefix `P[0] = 0` must be in the notebook before the loop, or subarrays starting at index 0 are
invisible.

```text
nums = [1, 2, 3, -2, 2]   k = 3
j:      0   1   2   3   4   5
P:      0   1   3   6   4   6

mid-run at j = 4, P = 4, want earlier P = 4 - 3 = 1
notebook (count):  {0:1, 1:1, 3:1, 6:1}
                         ^ one hit -> subarray a[1..3] = 2+3-2
running count: 3     (final count after j = 5: 4)

first-seen map: {0:0, 1:1, 3:2, 6:3, 4:4}
longest with sum 3: j=4 minus first[1]=1 -> length 3
```

**Where you'll use it**: Subarray Sum Equals K, directly; Product of Array Except Self uses the same prefix idea with
multiplication and no map. Beyond the chapter: Contiguous Array (525) turns 0 into -1 and looks for a repeated balance
with first-seen indices; Subarray Sums Divisible by K (974) stores `P mod k`.

### Difference arrays: prefix sums run backwards

**When it shows up**: many updates of the form "add v to every element in `[l, r]`", followed by reading the final
array (or one query at the end). Doing each update element by element is O(n) per update.

**The intuition**: prefix sums turn "sum of a range" into two point reads. The inverse trick turns "add to a range" into
two point writes. Keep an array `D` of changes: an update adds `v` at `D[l]` (the effect switches on) and subtracts `v`
at `D[r + 1]` (it switches off). Take the prefix sum of `D` once at the end, and each position has accumulated exactly
the updates that cover it, because it has passed every "on" to its left and every "off" to its left. It is the same
picture as people boarding and leaving a bus: you record only the stops where the count changes, and the running total
tells you the load between stops. `q` updates and one rebuild cost O(n + q) instead of O(n * q).

```text
n = 5, updates: add 2 on [1..3], add 3 on [2..4]
index:     0   1   2   3   4   5
D:       [ 0, +2, +3,  0, -2, -3 ]
              on  on      off off
prefix:  [ 0,  2,  5,  5,  3,  0 ]   <- final values
                   ^ covered by both updates
```

**Where you'll use it**: no problem in this chapter needs it, but it is the mirror image of the prefix sums used in
Product of Array Except Self and Subarray Sum Equals K, and it is the same "+1 at a start, -1 after an end" sweep the
intervals chapter uses. Beyond the chapter: Corporate Flight Bookings (1109), Car Pooling (1094).

### The array as its own hash table

**When it shows up**: O(1) extra space is demanded, and the values that matter fit in the index range, typically
`1..n` for an array of length `n`. Words like "missing", "duplicate", "disappeared" with values bounded by `n`.

**The intuition**: a hash table needs a function from value to slot. When values live in `1..n`, `v -> v - 1` is a
perfect hash with no collisions, and the input array already has those `n` slots. The only problem is that the slots are
occupied by data you still need. Two ways around it. **Cyclic placement** swaps each value into its home slot, evicting
the occupant, which then goes to its own home; each swap homes one value for good, so the nested loop is O(n) in total.
**Sign marking** keeps the data in place and uses a spare bit to record "seen": to tick value `v`, make `a[v - 1]`
negative, and always read values through `abs()` so the tick never destroys the number stored there. Either way, the
second pass asks every slot "do you hold your tick?", and the first slot that does not names the answer. The key
observation that makes this legal: with `n` slots, the answer to "smallest missing" lies in `1..n+1`, so values outside
`1..n` are noise that can be overwritten.

```text
sign marking, nums = [3, 4, -1, 1], n = 4
noise -> n+1:   [ 3,  4,  5,  1 ]
tick |3|:       [ 3,  4, -5,  1 ]    slot 2 negative
tick |4|:       [ 3,  4, -5, -1 ]    slot 3 negative
skip |5|        (out of 1..4)
tick |1|:       [-3,  4, -5, -1 ]    slot 0 negative
index:            0   1   2   3
                      ^ first positive slot -> answer 2
```

**Where you'll use it**: First Missing Positive (cyclic placement in the problem file; sign marking as its variation).
Beyond the chapter: Find All Numbers Disappeared in an Array (448), Find the Duplicate Number (287), where the values
become pointers and the problem becomes cycle detection.

### Pigeonhole buckets on the number line

**When it shows up**: a question about **closeness in value** (the widest gap between sorted neighbours, "any two values
within t") with a linear-time budget, so sorting is not allowed.

**The intuition**: cut the number line into equal buckets and compute a value's bucket with arithmetic, `x // width`,
which costs O(1) and involves no comparisons. Buckets give you **approximate order for free**: everything in bucket 3 is
below everything in bucket 4, though the order inside a bucket is unknown. The art is choosing the width so that the
unknown inside order never matters. In Maximum Gap, pigeonhole says the widest gap is at least the average gap
`(hi - lo) / (n - 1)`; make buckets narrower than that and the widest gap cannot hide inside a bucket, so each bucket
only needs its min and max. In Contains Duplicate III, width `t + 1` makes "same bucket" imply "within t", and
"within t" imply "same or adjacent bucket", so three lookups decide every question. Note the two uses run in opposite
directions: one wants the answer to **cross** bucket borders, the other wants it **inside** a bucket or next door.

```text
maximum gap, nums = [3, 6, 9, 1]: lo=1 hi=9 n=4
width = 8 // 3 = 2, bucket = (x - 1) // 2
bucket:   b0     b1     b2     b3     b4
covers:  1..2   3..4   5..6   7..8   9..10
min/max:  1/1    3/3    6/6    -/-    9/9
gaps:        3-1=2  6-3=3  skip   9-6=3
                                  ^ answer 3 crosses empty b3
```

**Where you'll use it**: Maximum Gap and Contains Duplicate III. Top K Frequent Elements is the gentle version (buckets
indexed by count, width 1). Beyond the chapter: bucket ideas reappear in sliding-window problems that need "is anything
close to x in the window".

### Counting cross pairs during merge sort

**When it shows up**: "for each element, how many later (or earlier) elements satisfy a value condition", or the total
number of such pairs: inversions, smaller-after-self, `nums[i] > 2 * nums[j]`. The brute force is O(n^2) over all pairs.

**The intuition**: merge sort splits the array into a left half and a right half, and **every left element was earlier
in the original array than every right element**. So at the moment of a merge, the index condition is true for every
cross pair, and only the value condition is left to check. Better still, both halves are sorted by then, so the value
condition becomes monotone: for a sorted left element `x`, the right elements that pair with it form a prefix, and that
prefix only grows as `x` grows. One pointer that only moves forward counts all cross pairs in linear time. Every pair
`p < q` is split apart at exactly one level of the recursion, so summing over levels counts each pair exactly once, and
the total is O(n log n). When the pair condition is the merge comparison itself (`r < x`), you can count while merging;
when it differs (`2r < x`), you count in a separate staircase pass, then merge.

```text
one merge level, condition x > 2r
left  (earlier, sorted):  2   4   7
right (later,   sorted):  1   3   5
x=2: 2r<2 for none          j=0 -> +0
x=4: 2*1<4                  j=1 -> +1
x=7: 2*1<7, 2*3<7, 2*5<7?no j=2 -> +2
cross pairs at this level = 3; j never moved back
```

**Where you'll use it**: Count of Smaller Numbers After Self (count during the merge, sorting indices so counts land on
the right element) and Reverse Pairs (separate counting pass). Beyond the chapter: Count of Range Sum (327) runs the
same staircase over prefix sums, with two pointers for the two bounds.

### Fenwick tree over values, with coordinate compression

**When it shows up**: rank questions asked **online**, one insertion at a time: "how many values inserted so far are
less than x, how many are greater". Also as a drop-in replacement for merge-sort counting when a left-to-right or
right-to-left scan is more natural.

**The intuition**: turn the question around. Keep `cnt[v]`, the number of times value `v` has been inserted; then "how
many inserted values are below x" is the prefix sum `cnt[1] + ... + cnt[x - 1]`. A plain array makes that query O(V).
A Fenwick tree stores block sums, where cell `i` covers the `lowbit(i)` values ending at `i`, so a prefix query strips
low bits (at most log V cells) and an insertion adds low bits (at most log V cells). If values are huge or negative,
**coordinate compression** first: sort the distinct values and replace each by its rank `1..m`. Only order matters for
"less than", and ranks preserve order, so the tree needs only `m <= n` cells. The scan direction encodes the index
condition: scanning right to left, the tree holds exactly the elements to the right.

```text
count smaller after self, nums = [5, 2, 6, 1]
compress: sorted distinct 1 2 5 6 -> ranks 1 2 3 4
scan right to left, answer = prefix(rank - 1), then add:
  1 (r1): prefix(0) = 0      cnt by rank: [1 . . .]
  6 (r4): prefix(3) = 1      cnt by rank: [1 . . 1]
  2 (r2): prefix(1) = 1      cnt by rank: [1 1 . 1]
  5 (r3): prefix(2) = 2      cnt by rank: [1 1 1 1]
answers (left to right): [2, 1, 1, 0]
```

**Where you'll use it**: Create Sorted Array through Instructions builds the tree from scratch; Count of Smaller Numbers
After Self and Reverse Pairs both have Fenwick versions (Reverse Pairs compresses `nums` and `2 * nums` into one rank
table). Beyond the chapter: Range Sum Query - Mutable (307), Count of Range Sum (327).

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

The order follows one thread: what you choose to remember about the past, and how much structure that memory needs.
It starts with a dict of raw values and ends with a tree of counts indexed by value. Each problem changes one thing
about the previous one.

### Warm-up: a notebook of the past

**Two Sum.** The puzzle is that the obvious answer checks every pair, and the question a curious person asks is: when I
stand on 7 and need 3, why am I searching for 3 instead of just asking whether I have met it? A dict from value to index
answers that in O(1). This is the chapter's template: query with the complement, then insert, never the other way round.

**Contains Duplicate II.** Same one-pass dict, but now "seen before" is not enough; it must have been seen within the
last k positions. The new idea is that what you store matters: keep the *last* index of each value and overwrite it on
every sighting, because the nearest earlier copy is the only one that can be close enough.

**Majority Element.** A dict of counts works, and that is the trap: it is O(n) memory for a question that needs one
answer. Boyer-Moore voting shows that a candidate and a counter suffice, because every non-majority vote can be
cancelled against a majority vote and the majority still has votes left. Memory can shrink to a summary when the
question only asks for a summary.

**Max Consecutive Ones.** The smallest notebook possible: one running count, reset to zero by every wall. It looks too
easy to teach anything, but it is the seed of every running accumulator later in the chapter, from prefix sums to the
staircase pointer in Reverse Pairs.

### Designing what to store

**Valid Sudoku.** Back to sets, now 27 of them at once: nine rows, nine columns, nine boxes. The interesting part is the
routing arithmetic, `(r // 3) * 3 + c // 3`, which sends each cell to its box without any lookup table. It teaches that
the key of a table can be computed from position as easily as from value.

**Group Anagrams.** The key stops being the item itself. "eat" and "tea" must land in the same bucket, so you design a
canonical form (sorted letters, or a 26-count tuple) that is equal exactly when the items belong together. Everything
in this problem is the choice of key; once it is right, the grouping is one `defaultdict(list)`.

**Top K Frequent Elements.** Counting is easy; the tension is in ranking the counts without an O(n log n) sort. The new
idea is that counts are small integers between 1 and n, so they can be array indices: put each value on the shelf for
its count and read shelves from the top. This is the chapter's first bucket sort, and the gentle version of the buckets
in Maximum Gap.

### Running totals and amortised loops

**Product of Array Except Self.** Division is forbidden, which kills the obvious "total divided by me". The new idea is
prefix and suffix accumulation: the product of everything except `a[i]` is the product of the left part times the
product of the right part, and both can be accumulated in one pass each. It is the first time the chapter stores
running totals instead of raw items.

**Longest Consecutive Sequence.** A set makes "is x + 1 present" O(1), but walking up from every element repeats work
quadratically on a long run. The fix is a start-of-run test: only begin walking from x when x - 1 is absent. The inner
while loop then looks nested but touches each element once overall, the chapter's first real amortised argument.

**Subarray Sum Equals K.** Negative numbers break the sliding window, and the brute force checks all O(n^2) subarrays.
The new idea joins two earlier ones: prefix sums turn a subarray into a difference `P[j] - P[i]`, and Two Sum's dict
finds earlier prefixes equal to `P[j] - k`. Seeding the dict with `{0: 1}` is the detail everyone forgets once.

**Encode and Decode Strings.** A change of pace: no array question, but a question about representation. Any delimiter
can appear inside the strings, so a naive join is ambiguous. Length-prefixing (`4#abcd`) makes the format unambiguous,
because the reader always knows how many characters to take before looking for the next header. It is canonical keys
from Group Anagrams, seen from the other side: designing a representation that cannot be confused.

### The Hard end, part one: beating the budget

**First Missing Positive.** O(n) time rules out sorting and O(1) space rules out a set, so both standard tools are
gone. The new idea is that the answer lies in `1..n+1`, which makes the array itself a collision-free hash table:
park value v at index v - 1, then read off the first slot that does not hold its own value. The swap loop is the
Longest Consecutive amortised argument again: every swap homes one value for good.

**Maximum Gap.** It sounds like it needs a sort, and comparison sorting is O(n log n). The new idea is pigeonhole: the
widest gap is at least the average gap, so buckets narrower than that cannot contain it, and each bucket only needs its
min and max. It builds on First Missing Positive's "values bounded, so something is forced" and on Top K's buckets,
now laid over value ranges instead of single values.

**Contains Duplicate III.** Contains Duplicate II plus a twist: values need only be within t, not equal, and a hash
set cannot find "nearby" values. Buckets of width t + 1 make "same bucket" mean "close enough", so each step checks
only three buckets, and the buckets slide with the window of the last k indices. It combines the index window from
earlier in the chapter with the value buckets from Maximum Gap.

### The Hard end, part two: counting across two orders

**Count of Smaller Numbers After Self.** Each answer mixes index order (to the right) with value order (smaller), and
neither a dict nor buckets can count by rank. The new idea is merge sort as a counting machine: at every merge the
right half is entirely later than the left half, so "later and smaller" becomes "already emitted from the right".
Sorting indices instead of values keeps each count attached to its owner.

**Reverse Pairs.** The same merge skeleton, but the pair test `x > 2r` differs from the merge's own comparison, so
counting while merging gives wrong answers. The new idea is to separate the two jobs: a staircase pass that counts with
a pointer that only moves forward, then the ordinary merge. Any monotone pair condition fits this shape.

**Create Sorted Array through Instructions.** Now the questions arrive online, one insertion at a time, so there is no
"whole array" to merge-sort. The new idea is a Fenwick tree indexed by value: "how many inserted values are below x"
becomes a prefix sum over counts, answered and updated in O(log V). It is the general tool behind the previous two
problems, and it closes the arc that started with Two Sum's dict: from remembering which values you have seen to
remembering, in order, how many.
