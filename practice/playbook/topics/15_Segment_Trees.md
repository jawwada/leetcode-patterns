## Segment Trees

> A segment tree is a binary tree laid over an array. Each node owns a range of indices and stores one summary of that range, such as its sum, minimum or maximum. A range query glues together O(log n) nodes that exactly cover the range, and a point update repairs one root-to-leaf path. Both cost O(log n), so the array can keep changing between questions.

[Trees](13_Trees.ipynb#topic-trees) wrote recursive functions that ask two children for a fact and combine it. A segment tree does the same thing, but it **stores** each node's answer instead of recomputing it, so a question about a range is answered from a few stored pieces.

**Reach for it when** a problem asks many **range questions** (sum, min, max, gcd, count) **and** the array **changes** between them; when the brute force rescans a range per query, or rebuilds prefix sums after every update; when a count over **values** must grow as items arrive ("how many smaller numbers so far"); or when whole **ranges are updated** at once (add 1 to every time in [start, end)) and only the peak is wanted.

### The picture

```text
nums  =  [1, 3, 5, 7, 9, 11]        indices 0..5          each node: sum of its range

                         [0..5] 36                         node 1  (the root)
                  /                    \
           [0..2] 9                  [3..5] 27             nodes 2, 3
           /      \                  /       \
      [0..1] 4   [2] 5          [3..4] 16   [5] 11         nodes 4, 5, 6, 7
      /    \                    /    \
   [0] 1  [1] 3              [3] 7  [4] 9                  nodes 8, 9, 12, 13

query(1, 4) = 3 + 5 + 16 = 24       pieces [1], [2], [3..4]: they cover 1..4 exactly, no overlap
update(1, 2)                        repair the path [1] -> [0..1] -> [0..2] -> [0..5]: 4 nodes
```

A node `k` keeps its children at `2k` and `2k + 1`, the same index arithmetic as a heap, so the tree lives in a plain list with no node objects. Node `k` covering `[lo..hi]` splits at `mid = (lo + hi) // 2`: the left child covers `[lo..mid]`, the right child `[mid+1..hi]`, and every leaf covers one index.

The brute force has two bad choices. Summing `nums[l:r+1]` on every query costs O(n) per query. A prefix-sum array answers in O(1), but one update shifts every later prefix and costs O(n). With q queries and updates mixed, both are O(n·q). The segment tree pays O(log n) for each: a query uses at most two pieces per level, and an update changes one node per level.

A Fenwick tree (binary indexed tree, built in [Hash Maps and Sets](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets)) also gives O(log n) update and prefix sum, with less code. It needs an operation that can be undone, because a range is `prefix(r) − prefix(l − 1)`. Minimum and maximum cannot be undone that way, and ranges that are updated as a whole need lazy marks. Both are where the segment tree earns its extra lines.

### From idea to code

**The idea in one sentence:** *store the summary of every range in a halving tree, answer a range by gluing the stored nodes that fit inside it, and after changing a leaf, recompute only its ancestors.*

The **State** is a list `tree` of size `4n` and, for each call, a node index with the range `[lo..hi]` it covers. The **Definition** is the whole contract: `tree[node]` equals the sum of `nums[lo..hi]`. The **Invariant** keeps it true after every operation: each inner node equals the merge of its two children, `tree[node] = tree[2·node] + tree[2·node + 1]`.

A query **Step** looks at one node and its range against the query `[l..r]` and has three cases: no overlap, so return the identity 0; the node's range sits fully inside, so return `tree[node]` without going deeper; a partial overlap, so ask both children. An update **Step** walks down to the leaf for index `i`, the only way the range can contain `i`. The **Record** is the line that restores the invariant: after the recursion returns, the node recomputes itself from its children. It must come *after* the recursive call, because a parent can only be repaired once its child is right. **Init** builds bottom-up the same way: leaves copy `nums`, and each parent merges its children after they are built. The **Return** of a query is the merge of the pieces it found.

Range Sum Query - Mutable (307) asks for exactly this: `update(i, val)` sets `nums[i] = val`, and `sum_range(l, r)` returns the sum of `nums[l..r]`, with both calls interleaved. For `[1, 3, 5, 7, 9, 11]`, `sum_range(1, 3)` is 15; after `update(1, 2)` it is 14. The class below hides the node and range arguments behind defaults so the caller writes `st.query(1, 3)`.

<!-- cell -->

```python
class SegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)        # STATE: tree[node] = sum of nums[lo..hi] for node's range
        if self.n:
            self._build(nums, 1, 0, self.n - 1)   # INIT: node 1 covers the whole array

    def _build(self, nums, node, lo, hi):
        if lo == hi:
            self.tree[node] = nums[lo]        # a leaf holds one value
            return
        mid = (lo + hi) // 2
        self._build(nums, 2 * node, lo, mid)
        self._build(nums, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, i, val, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        if lo == hi:
            self.tree[node] = val             # STEP: the leaf for index i
            return
        mid = (lo + hi) // 2
        if i <= mid:
            self.update(i, val, 2 * node, lo, mid)        # i lives in exactly one half
        else:
            self.update(i, val, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]   # RECORD: repair on the way back up

    def query(self, l, r, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        if r < lo or hi < l:
            return 0                          # no overlap: the identity of +
        if l <= lo and hi <= r:
            return self.tree[node]            # STEP: the whole node fits, stop here
        mid = (lo + hi) // 2
        return (self.query(l, r, 2 * node, lo, mid)          # RETURN: glue the two halves
                + self.query(l, r, 2 * node + 1, mid + 1, hi))


st = SegmentTree([1, 3, 5, 7, 9, 11])
print(st.query(1, 3), st.query(0, 5))   # 15 36
st.update(1, 2)
print(st.query(1, 3), st.query(0, 5))   # 14 35
```

<!-- cell -->

**Try it**
- Print `st.tree[:16]` after the update: `[0, 35, 8, 27, 3, 5, 16, 11, 1, 2, 0, 0, 7, 9, 0, 0]`. Index 0 is never used, node 1 is the total, and the zeros at 10, 11, 14, 15 are children of leaves that never exist.
- Delete the last line of `update` (the repair) and rerun: the second line still prints `14`, but then `36`. `query(1, 3)` happens to read the leaf directly, while `query(0, 5)` stops at the stale root, so two queries now disagree about the same array.
- Change `self.tree = [0] * (4 * self.n)` to `2 * self.n`: `SegmentTree([1] * 6)` raises `IndexError`, because with this split the leaf for index 5 is node 13. The recursive tree is not perfectly packed; `4n` is always enough.
- Change `return 0` to `return 1` in `query`: after the update, `st.query(1, 3)` becomes 17 instead of 14. Each of the three nodes outside the range leaks a 1 into the answer, so the identity must be the value that changes nothing.

<!-- cell -->

### Watch it work

The cell below records the pieces a query glues together and counts the nodes it visits. On `[1..8]`, the range `1..6` is covered by four pieces: one leaf, two pairs, one leaf. On an array of 1 000 ones, the query `1..998` visits only 37 nodes, about 4 per level of a tree 10 levels deep.

<!-- cell -->

```python
def pieces(st, l, r, node=1, lo=0, hi=None, found=None):
    hi = st.n - 1 if hi is None else hi
    found = [] if found is None else found
    if r < lo or hi < l:
        return found
    if l <= lo and hi <= r:
        found.append((f"node {node}", f"[{lo}..{hi}]", st.tree[node]))
        return found
    mid = (lo + hi) // 2
    pieces(st, l, r, 2 * node, lo, mid, found)
    pieces(st, l, r, 2 * node + 1, mid + 1, hi, found)
    return found


def visits(st, l, r, node=1, lo=0, hi=None):
    hi = st.n - 1 if hi is None else hi
    if r < lo or hi < l or (l <= lo and hi <= r):
        return 1
    mid = (lo + hi) // 2
    return 1 + visits(st, l, r, 2 * node, lo, mid) + visits(st, l, r, 2 * node + 1, mid + 1, hi)


eight = SegmentTree([1, 2, 3, 4, 5, 6, 7, 8])
for piece in pieces(eight, 1, 6):
    print(piece)                                   # [1..1] 2, [2..3] 7, [4..5] 11, [6..6] 7
print(eight.query(1, 6), visits(SegmentTree([1] * 1000), 1, 998))   # 27 37
```

<!-- cell -->

**Try it**
- Run `pieces(eight, 0, 7)`: one piece, the root. A query that covers the whole array stops at the first node.
- Run `pieces(eight, 3, 4)`: two leaves, `[3..3]` and `[4..4]`, from opposite halves. The middle of the array is the worst place for a short range, because it splits at the root.
- Run `visits(SegmentTree([1] * 1000), 0, 999)` and `visits(SegmentTree([1] * 1000), 1, 998)`: 1 and 37. Predict `visits` for 100 000 ones and `1..99998` before running: 65. A hundred times more data costs fewer than twice the visits.

<!-- cell -->

### Where it goes wrong

1. **Array too small.** The recursive split is not a perfect tree: for n = 6 the last leaf is node 13, so a list of `2n` raises `IndexError`. Use `4n`, or the iterative tree below, which really fits in `2n`.
2. **Wrong identity.** The no-overlap case must return the value that leaves the merge unchanged: 0 for sum, `math.inf` for min, `-math.inf` for max, 0 for gcd. A range minimum that returns 0 for an empty side answers 0 for `query(1, 2)` on `[5, 2, 8]`.
3. **Repair before the recursion.** `tree[node] = tree[2·node] + tree[2·node + 1]` placed before the recursive call recomputes the parent from the old child, and the update is lost above the leaf.
4. **Two different splits.** `build`, `update` and `query` must all split at the same `mid` into `[lo..mid]` and `[mid+1..hi]`. If one of them uses `[lo..mid−1]`, a node points at a range it does not hold.
5. **Inclusive or exclusive right end.** This template takes `query(l, r)` with `r` included. A booking `[start, end)` is the inclusive range `start..end − 1`; passing `end` counts one extra slot, so two bookings that only touch at a point overlap.
6. **Set versus add.** Range Sum Query - Mutable *sets* `nums[i] = val`. If the update adds `val` instead, `update(1, 2)` on `[1, 3, 5]` makes index 1 hold 5, not 2. When the problem says "add", keep the old value or add a delta at the leaf.
7. **Lazy mark forgotten on the way down.** With range updates, a node that holds a pending add for its whole range must apply it to every answer read from below it. A query that skips it reports the old maximum (the Try it under Falling Squares shows the failure).
8. **An empty array.** `SegmentTree([])` has no root range; the guard in `__init__` skips the build, and no query or update may be called.

### Edge cases to say out loud

One element · a query of one index · a query of the whole array · updating the same index twice · negative values · `l == r` at the very ends (0 and n − 1) · an empty array. The asserts below check each case and then compare the tree against plain `sum` on 300 random arrays with random updates.

<!-- cell -->

```python
one = SegmentTree([7])
assert one.query(0, 0) == 7
one.update(0, -2)
assert one.query(0, 0) == -2                                 # a single leaf is also the root

st = SegmentTree([4, -1, 6])
assert st.query(0, 0) == 4 and st.query(2, 2) == 6 and st.query(0, 2) == 9
st.update(1, 5)
st.update(1, 0)                                              # the second set wins
assert st.query(0, 2) == 10 and st.query(1, 1) == 0
assert SegmentTree([]).n == 0                                # built without a crash

rng = random.Random(0)
for _ in range(300):
    nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 20))]
    st = SegmentTree(nums)
    for _ in range(20):
        i = rng.randrange(len(nums))
        nums[i] = rng.randint(-9, 9)
        st.update(i, nums[i])
        l = rng.randrange(len(nums))
        r = rng.randrange(l, len(nums))
        assert st.query(l, r) == sum(nums[l:r + 1])
print("edge cases pass")
```

<!-- cell -->

**Try it**
- Change `if i <= mid:` in `update` to `if i < mid:` and rerun: the random check fails. On `[1, 3, 5, 7]`, `update(1, 10)` now walks into the right half and overwrites index 2, so `query(0, 3)` is 21. One mismatched split is enough.
- Add `print(len(SegmentTree([1] * 6).tree))` and predict: 24. Node 13 is the largest index used, so most of the list stays 0.
- Call `SegmentTree([]).query(0, 0)`: it returns 0, because the root range `[0..−1]` overlaps nothing. `SegmentTree([]).update(0, 1)` never reaches a leaf and raises `RecursionError`. Guard empty input before building.

<!-- cell -->

### Variations

Every variation keeps the halving tree and changes one thing: the merge, the layout, what the indices mean, or how a whole range is updated. The table is the lookup; the paragraphs below take them in order.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Any merge** | `+` becomes `min`, `max` or `gcd`; the identity changes with it | range minimum / maximum queries with updates |
| **Iterative tree in 2n** | leaves at `n..2n−1`, parents built from `n − 1` down to 1; the query climbs both ends | Range Sum Query - Mutable (307: point set, range sum) |
| **Tree over values** | the index is a value's rank, the stored number a count; insert = add 1, "how many smaller" = a prefix query | Count of Smaller Numbers After Self (315: for each item, how many later items are smaller) |
| **Range max over values for a DP** | `best[v]` = the best answer ending at value v; read a window of values, write one value | Longest Increasing Subsequence II (2407: a longest increasing subsequence whose neighbours differ by at most k) |
| **Lazy range update** | a node keeps a pending add for its whole range and does not touch its children | My Calendar III (732: after each booking, the most bookings that overlap at one instant) |
| *Second pass:* **Range raise, compressed coordinates** | compress the x's; a node keeps the height it was raised to; a query takes the max with every mark on its path | Falling Squares (699: the tallest stack after each square lands) |

The first change is the merge itself. The tree only needs the merge to be associative, `(a·b)·c = a·(b·c)`, so that the order in which pieces are glued does not matter, and it needs an identity for the empty side. Passing both in makes one class answer sums, minimums, maximums and gcds. For `[5, 2, 8, 6, 3, 7]` the minimum of indices 2..5 is 3, and after setting index 4 to 9 it is 6.

<!-- cell -->

```python
class MergeTree:
    def __init__(self, nums, merge, identity):
        self.n, self.merge, self.identity = len(nums), merge, identity
        self.tree = [identity] * (4 * self.n)
        if self.n:
            self._build(nums, 1, 0, self.n - 1)

    def _build(self, nums, node, lo, hi):
        if lo == hi:
            self.tree[node] = nums[lo]
            return
        mid = (lo + hi) // 2
        self._build(nums, 2 * node, lo, mid)
        self._build(nums, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.merge(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, i, val):
        def go(node, lo, hi):
            if lo == hi:
                self.tree[node] = val
                return
            mid = (lo + hi) // 2
            if i <= mid:
                go(2 * node, lo, mid)
            else:
                go(2 * node + 1, mid + 1, hi)
            self.tree[node] = self.merge(self.tree[2 * node], self.tree[2 * node + 1])
        go(1, 0, self.n - 1)

    def query(self, l, r):
        def go(node, lo, hi):
            if r < lo or hi < l:
                return self.identity          # the empty side changes nothing
            if l <= lo and hi <= r:
                return self.tree[node]
            mid = (lo + hi) // 2
            return self.merge(go(2 * node, lo, mid), go(2 * node + 1, mid + 1, hi))
        return go(1, 0, self.n - 1)


nums = [5, 2, 8, 6, 3, 7]
lowest = MergeTree(nums, min, math.inf)
highest = MergeTree(nums, max, -math.inf)
gcds = MergeTree([12, 18, 24, 9], math.gcd, 0)
print(lowest.query(2, 5), highest.query(0, 1), gcds.query(0, 2), gcds.query(0, 3))   # 3 5 6 3
lowest.update(4, 9)
print(lowest.query(2, 5))                                                              # 6
```

<!-- cell -->

**Try it**
- Build `MergeTree(nums, min, 0)` and query `2..5`: 0, a value that is not in the array. The wrong identity wins every comparison.
- Use `MergeTree(nums, lambda a, b: a + b, 0)` and check `query(0, 5)` is 31, the template's sum again.
- Try a merge that is not associative, `lambda a, b: a - b`, on `[1, 2, 3, 4]`: `query(0, 3)` gives `(1 − 2) − (3 − 4) = 0`, while subtracting left to right gives −8. The tree regroups the pieces, so the merge must not care about grouping.

<!-- cell -->

The same tree can be written without recursion, and that version really fits in `2n`. Put the leaves at `tree[n..2n−1]` and build every parent `i` from `n − 1` down to 1 as `tree[2i] + tree[2i + 1]`. An update sets a leaf and climbs with `i //= 2`, repairing each parent.

A query keeps two fingers, `left` and `right`, on the leaf level and climbs. If `left` is a right child (odd), its parent also covers an index outside the range, so take `tree[left]` alone and step right; if `right` is a left child (even), take it and step left. Then both climb. For `[1, 3, 5, 7, 9]`, `query(1, 3)` is 15, and 20 after setting index 2 to 10.

<!-- cell -->

```python
class SegTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (2 * self.n)            # leaves at n..2n-1, parents at 1..n-1
        for i, v in enumerate(nums):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):        # children before parents
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, idx, val):
        i = idx + self.n
        self.tree[i] = val
        i //= 2
        while i:                                  # repair every ancestor
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            i //= 2

    def query(self, left, right):                 # inclusive
        left += self.n
        right += self.n
        res = 0
        while left <= right:
            if left % 2 == 1:                     # a right child: its parent sticks out on the left
                res += self.tree[left]
                left += 1
            if right % 2 == 0:                    # a left child: its parent sticks out on the right
                res += self.tree[right]
                right -= 1
            left //= 2
            right //= 2
        return res


st = SegTree([1, 3, 5, 7, 9])
print(st.query(1, 3))   # 15
st.update(2, 10)
print(st.query(1, 3), st.query(0, 4), st.tree)   # 20 30 [0, 30, 17, 13, 16, 1, 3, 10, 7, 9]
```

<!-- cell -->

**Try it**
- Compare the sum before and after a point update: `s = SegTree([2, 4, 6, 8])`, then `s.query(0, 3)` is 20, and after `s.update(1, 10)` it is 26.
- Read the printed list: the leaves `1, 3, 10, 7, 9` sit at 5..9. Node 2 is `16 + 1 = 17`: node 4 holds array indices 3 and 4, and node 5 holds index 0. With n not a power of two, some nodes mix the end of the array with its start, and the query never takes one of them whole.
- Change `left % 2 == 1` to `left % 2 == 0`: `st.query(1, 3)` gives 10 instead of 20. The parity test is what keeps a parent's extra index out.
- Swap the two `if` blocks: the answers do not change. Each block only consumes its own end, so their order does not matter.

<!-- cell -->

The index does not have to be a position. Count of Smaller Numbers After Self (315) asks, for every item, how many items to its right are smaller: `[5, 2, 6, 1]` gives `[2, 1, 1, 0]`. Walk from the right and keep a count for every value seen so far; the answer for `x` is the number of seen values below `x`, a prefix query.

Values can be huge or negative, so first compress them to ranks 0..m−1. Then the tree holds `seen[rank]`, adding a value is a point update, and "how many smaller" is `query(0, rank − 1)`. The Fenwick tree in [Hash Maps and Sets](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets) solves it the same way; here the same `MergeTree` does it.

<!-- cell -->

```python
def count_smaller(nums):
    ranks = {v: r for r, v in enumerate(sorted(set(nums)))}    # value -> 0..m-1
    seen = [0] * len(ranks)
    tree = MergeTree(seen, lambda a, b: a + b, 0)               # STATE: tree over ranks, counts of seen values
    out = []
    for x in reversed(nums):                                    # only items to the right are seen
        r = ranks[x]
        out.append(tree.query(0, r - 1) if r else 0)            # RECORD: seen values strictly smaller
        seen[r] += 1
        tree.update(r, seen[r])                                 # STEP: x is now seen
    return out[::-1]


print(count_smaller([5, 2, 6, 1]), count_smaller([-1, -1]), count_smaller([2, 0, 1]))   # [2, 1, 1, 0] [0, 0] [2, 0, 0]
```

<!-- cell -->

**Try it**
- Change `tree.query(0, r - 1)` to `tree.query(0, r)`: `[-1, -1]` gives `[1, 0]`. An equal value to the right is now counted as smaller, the off-by-one to watch.
- Walk left to right instead (`for x in nums`) and drop the final `[::-1]`: `[5, 2, 6, 1]` gives `[0, 0, 2, 0]`, the count of smaller items to the *left*.
- Skip the compression and index by the value itself, with a tree of size `max(nums) + 1`: `[5, 2, 6, 1]` still works, but `[-1, 10**9]` needs a negative index and a billion leaves. Compression makes the tree's size depend on n, not on the values.

<!-- cell -->

A maximum over values turns some DP problems from O(n²) into O(n log V). Longest Increasing Subsequence II (2407) asks for the longest strictly increasing subsequence whose neighbours differ by at most k: for `[4, 2, 1, 4, 3, 4, 5, 8, 15]` and k = 3 it is 5, from `1, 3, 4, 5, 8`. A subsequence ending at x continues one ending at a value in `x − k .. x − 1`, so `best[x] = 1 + max(best[x − k .. x − 1])`.

The quadratic version scans every earlier item; the tree keeps `best` indexed by value and answers the window maximum in O(log V). A Fenwick tree cannot do this, because a maximum of a window cannot be found by subtracting two prefixes.

<!-- cell -->

```python
def length_of_lis(nums, k):
    best = MergeTree([0] * (max(nums) + 1), max, 0)    # STATE: best[v] = longest valid run ending at value v
    answer = 0
    for x in nums:
        run = 1 + (best.query(max(0, x - k), x - 1) if x > 0 else 0)   # STEP: extend the best run in the window
        best.update(x, run)                            # RECORD: the best run ending at value x
        answer = max(answer, run)
    return answer                                       # RETURN


print(length_of_lis([4, 2, 1, 4, 3, 4, 5, 8, 15], 3), length_of_lis([7, 4, 5, 1, 8, 12, 4, 7], 5), length_of_lis([1, 5], 1))   # 5 4 1
```

<!-- cell -->

**Try it**
- Overwriting `best[x]` looks risky: what if a later x has a shorter run? It cannot. Every `best` value only grows, so the window a later x reads is at least as good as before. Check it: `length_of_lis([1, 2, 3, 1, 2, 3, 4], 1)` is 4, and the second 3 writes the same 3.
- Query `x − k .. x` instead of `x − k .. x − 1`: equal neighbours are allowed and `[4, 4, 4]` with k = 1 gives 3, but the subsequence must be strictly increasing, so the answer is 1.
- Set k very large (`10**9`) on `[4, 2, 1, 4, 3, 4, 5, 8, 15]`: 5 becomes 6, the plain longest increasing subsequence `2, 3, 4, 5, 8, 15`.

<!-- cell -->

The last main variation updates a whole range at once. My Calendar III (732) books intervals `[start, end)` and after each one reports the most bookings overlapping at a single instant: after `(10, 20)`, `(50, 60)`, `(10, 40)` and `(5, 15)` the answers are 1, 1, 2, 3. One booking adds 1 to every time in `start..end − 1`, a range of up to 10⁹ points.

Adding to each leaf would be O(range). Instead, when a node's range fits inside the booking, add 1 to that node's **lazy mark** and stop: the mark means "everything below me is 1 higher", and the children are never touched. A node's maximum is then its own mark plus the larger maximum of its children. Only the root is ever read, so the marks never need to be pushed down. Nodes live in dicts and are created only when touched, so the tree over `0..10⁹` stays small.

<!-- cell -->

```python
class MyCalendarThree:
    def __init__(self):
        self.peak = defaultdict(int)   # STATE: node -> max overlap inside its range, its own mark included
        self.mark = defaultdict(int)   # STATE: node -> bookings that cover its whole range (lazy)

    def _add(self, l, r, node, lo, hi):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self.peak[node] += 1                  # STEP: the whole range rises by 1 ...
            self.mark[node] += 1                  # ... noted here, children untouched
            return
        mid = (lo + hi) // 2
        self._add(l, r, 2 * node, lo, mid)
        self._add(l, r, 2 * node + 1, mid + 1, hi)
        self.peak[node] = self.mark[node] + max(self.peak[2 * node], self.peak[2 * node + 1])   # RECORD

    def book(self, start, end):
        self._add(start, end - 1, 1, 0, 10**9)    # [start, end) is start..end-1 inclusive
        return self.peak[1]                       # RETURN: the root's peak is the global peak


calendar = MyCalendarThree()
print([calendar.book(s, e) for s, e in [(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)]])   # [1, 1, 2, 3, 3, 3]
print(len(calendar.peak))   # 97 nodes for a range of a billion points
```

<!-- cell -->

**Try it**
- Drop `self.mark[node]` from the RECORD line: the answers become `[1, 1, 2, 3, 2, 2]`, and the peak goes *down* after a booking. A parent recomputed after a partial booking forgets the bookings that covered it whole.
- Pass `end` instead of `end - 1`: `(10, 20)` then `(20, 30)` gives `[1, 2]`, although one booking ends exactly when the other starts.
- Compare with the sweep in [Intervals and Sweep Line](17_Intervals_and_Sweep_Line.ipynb#topic-intervals-and-sweep-line): it re-scans every boundary on each booking, O(n) per call, while `_add` visits O(log C) nodes: about a hundred calls for a booking that spans most of `0..10⁹`.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Falling Squares (699) drops squares `[left, side]` one by one onto a line: each lands on the tallest square under `[left, left + side)` and its top becomes `that height + side`. After each drop it reports the tallest stack: `[[1, 2], [2, 3], [6, 1]]` gives `[2, 5, 5]`. Two touching squares do not stack, so the cells are the integers `left .. left + side − 1`.

The updates are range "raise to h", and the new top is always at least as high as everything it covers, so a mark can be the maximum ever applied to a node's whole range. Coordinates are compressed to the ranks of the cell ends, so the tree has at most 2n leaves. A query takes the max of the marks on its path with the nodes it reaches, because a mark on an ancestor raises every cell below it.

<!-- cell -->

```python
def falling_squares(positions):
    xs = sorted({x for left, side in positions for x in (left, left + side - 1)})
    rank = {x: i for i, x in enumerate(xs)}                # compressed cell coordinates
    n = len(xs)
    high = [0] * (4 * n)                                   # tallest point anywhere in the node's range
    mark = [0] * (4 * n)                                   # height the WHOLE range was raised to (lazy)

    def raise_to(l, r, h, node, lo, hi):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            high[node] = max(high[node], h)
            mark[node] = max(mark[node], h)
            return
        mid = (lo + hi) // 2
        raise_to(l, r, h, 2 * node, lo, mid)
        raise_to(l, r, h, 2 * node + 1, mid + 1, hi)
        high[node] = max(mark[node], high[2 * node], high[2 * node + 1])

    def tallest(l, r, node, lo, hi):
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return high[node]
        mid = (lo + hi) // 2
        return max(mark[node], tallest(l, r, 2 * node, lo, mid), tallest(l, r, 2 * node + 1, mid + 1, hi))

    out = []
    for left, side in positions:
        l, r = rank[left], rank[left + side - 1]
        top = tallest(l, r, 1, 0, n - 1) + side            # land on the tallest thing below
        raise_to(l, r, top, 1, 0, n - 1)
        out.append(high[1])
    return out


print(falling_squares([[1, 2], [2, 3], [6, 1]]), falling_squares([[100, 100], [200, 100]]))   # [2, 5, 5] [100, 100]
```

<!-- cell -->

**Try it**
- Delete `mark[node]` from the `max` in `tallest`: `[[1, 4], [2, 1]]` gives `[4, 4]` instead of `[4, 5]`. The first square marked a big node, the second square's query went below it without seeing the mark, and it landed on the floor.
- Use `left + side` instead of `left + side - 1` for both ends: `[[100, 100], [200, 100]]` gives `[100, 200]`, because touching squares now share a cell.
- Print `n` for `[[1, 2], [2, 3], [6, 1]]`: 4, the distinct cell ends 1, 2, 4, 6. The tree's size depends on the number of squares, not on how far apart they are.

<!-- cell -->

<details><summary>Rectangle Area II (850): a segment tree of cover counts</summary>

Rectangle Area II asks for the total area covered by possibly overlapping rectangles. Sweep x from left to right; between two consecutive x's, the covered height is the length of the union of the active y-intervals, and the strip adds `width × covered`. A segment tree over the compressed y's keeps, per node, `count` (rectangles covering the node's whole range) and `covered` (the covered length inside it): if `count > 0` the whole range is covered, else it is the sum of the children. A rectangle's left edge adds 1 on its y-range, its right edge subtracts 1, and the root's `covered` is the height for the next strip, O(n log n) in total. The marks never need to be pushed down because every −1 matches an earlier +1 on exactly the same nodes. The sweep without a tree is in `intervals/rectangle_area_ii.py`.

</details>

### Say it in the interview

> "Recomputing each range is O(n) per query, and prefix sums break on every update. A segment tree stores the sum of every halving range: a query glues at most two nodes per level, and an update repairs one root-to-leaf path, so both are O(log n) with O(n) space. If only prefix sums with point updates are needed, a Fenwick tree is shorter; I'd use the segment tree for min or max, or for range updates with lazy marks."

While coding, point at the three cases of `query` ("no overlap returns the identity, full overlap stops here, partial asks both halves") and at the repair line after the recursion ("this keeps every parent equal to its children"). Be ready for the follow-ups:

- *Why `4n`?* The recursive split is not perfectly packed; the last leaf for n = 6 is node 13. The iterative tree fits in `2n`.
- *Values instead of positions?* Compress them to ranks and count in the tree (315).
- *Range updates?* Lazy marks: a node that fits the range takes the change and stops; the marks are applied on the way down or added in on the way up.
- *Huge coordinate range online?* Create nodes in a dict only when touched (732), O(log C) nodes per update.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Count of Smaller Numbers After Self | `arrays_hashing/count_of_smaller_numbers_after_self.py` | walk from the right; a tree of counts over value ranks; answer = prefix count below the rank |
| Falling Squares | not in repo (LeetCode 699) | compress cell ends; land at 1 + range max; raise the range with a lazy max mark |
| Longest Increasing Subsequence II | not in repo (LeetCode 2407) | `best[x] = 1 + max(best[x − k .. x − 1])`: a range-max tree indexed by value |
| My Calendar III | `intervals/my_calendar_iii.py` | dynamic lazy tree over 0..10⁹: +1 on `start..end − 1`, the root's peak is the answer |
| Range Sum Query - Mutable | not in repo (LeetCode 307) | point set, range sum; repair the ancestors after the leaf |
| Rectangle Area II | `intervals/rectangle_area_ii.py` | sweep x; a cover-count tree over compressed y gives the covered height per strip |

### Self-check

1. Why does a range query touch only O(log n) nodes?
<details><summary>Answer</summary>At each level, at most two nodes partially overlap the range: the ones holding its two ends. Every node strictly between them fits inside, so the query stops there instead of going deeper. Two partial nodes per level, each asking at most two children, keeps the work at about 4 per level.</details>

2. What must the no-overlap case return, and why?
<details><summary>Answer</summary>The identity of the merge: 0 for sum, <code>math.inf</code> for min, <code>-math.inf</code> for max, 0 for gcd. The empty side is merged into the answer, so it must change nothing.</details>

3. When is a Fenwick tree not enough?
<details><summary>Answer</summary>A Fenwick tree answers prefixes, and gets a range as <code>prefix(r) − prefix(l − 1)</code>. Min and max cannot be subtracted, so a range minimum or a window maximum (2407) needs a segment tree, as do range updates that read a maximum, such as My Calendar III.</details>

4. In My Calendar III, what does a lazy mark mean, and why is it added back in the repair line?
<details><summary>Answer</summary>It means "every time in my range has this many more bookings". The children never saw those bookings, so a node's peak is its mark plus the larger peak of its children. Without the mark, a later partial booking that repairs the node would forget every booking that had covered it whole.</details>
