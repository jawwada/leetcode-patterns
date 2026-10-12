---
rank: 107
slug: segment_tree
---

Keep an array of numbers under two operations that arrive in any mix: `update(index, value)` sets one element, and `query(left, right)` returns the sum of `nums[left..right]`, both ends included. On `[5, 8, 6, 3, 2, 7, 2, 6]`, `query(2, 6)` is `6 + 3 + 2 + 7 + 2 = 20`; after `update(4, 9)` the same query returns `27`.

The plain array updates in `O(1)` but sums a range in `O(n)`. Prefix sums flip the trade: a range sum is the difference of two prefixes, `O(1)`, but changing one element shifts every prefix after it, `O(n)`. A segment tree stores the sums of ranges at every scale, chosen so that both operations touch only `O(log n)` of them. The root owns the whole array, each node hands the halves of its segment to its two children, and each leaf owns a single element; every node stores the sum of its segment. Numbered like a heap, node `i` has the children `2i` and `2i + 1`, and an array of `4n` slots always holds them.

A query walks down from the root, and each node it meets is one of three cases. A segment entirely outside `left..right` contributes `0`. A segment entirely inside contributes its stored sum, and nothing below it is visited. A segment that overlaps partly asks both children and adds their answers. Only a segment that contains an end of the range can overlap partly, so each level holds at most two such nodes and the query visits at most four nodes per level. An update walks the one path from the root to its leaf and redoes each sum on the way back up, since those are the only segments containing the index.

```text
                                 [0..7] 39 ○
                  ┌───────────────────┴───────────────────┐
             [0..3] 22 ○                             [4..7] 17 ○
        ┌─────────┴─────────┐                   ┌─────────┴─────────┐
   [0..1] 13 ✗         [2..3] 9 ●          [4..5] 9 ●          [6..7] 8 ○
   ┌────┴────┐         ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
   5         8         6         3         2         7         2 ●       6 ✗
● full overlap: use the stored sum  ○ partial: ask both halves  ✗ no overlap: 0
query(2, 6) = [2..3] 9 + [4..5] 9 + [6..6] 2 = 20, visiting 9 of the 15 nodes
update(4, 9): [4..4] 2 → 9, then its path up: [4..5] 9 → 16, [4..7] 17 → 24,
              [0..7] 39 → 46; query(2, 6) now returns 9 + 16 + 2 = 27
```

```pseudo
CLASS SegmentTree
    FUNCTION Init(nums)
        self.n ← len(nums)
        self.tree ← array of 4 * self.n zeros  // 4n slots always suffice
        IF self.n > 0
            self.Build(nums, 1, 0, self.n - 1)

    FUNCTION Build(nums, node, lo, hi)
        IF lo = hi
            self.tree[node] ← nums[lo]         // a leaf owns one element
            RETURN
        mid ← floor((lo + hi) / 2)
        self.Build(nums, 2 * node, lo, mid)
        self.Build(nums, 2 * node + 1, mid + 1, hi)
        self.tree[node] ← self.tree[2 * node] + self.tree[2 * node + 1]

    FUNCTION Update(index, value)
        self.UpdateAt(1, 0, self.n - 1, index, value)

    FUNCTION UpdateAt(node, lo, hi, index, value)
        IF lo = hi
            self.tree[node] ← value
            RETURN
        mid ← floor((lo + hi) / 2)
        IF index ≤ mid                         // index lies in the left half
            self.UpdateAt(2 * node, lo, mid, index, value)
        ELSE
            self.UpdateAt(2 * node + 1, mid + 1, hi, index, value)
        self.tree[node] ← self.tree[2 * node] + self.tree[2 * node + 1]

    FUNCTION Query(left, right)
        RETURN self.QueryAt(1, 0, self.n - 1, left, right)

    FUNCTION QueryAt(node, lo, hi, left, right)
        IF right < lo OR hi < left
            RETURN 0                           // no overlap
        IF left ≤ lo AND hi ≤ right
            RETURN self.tree[node]             // full overlap: the stored sum
        mid ← floor((lo + hi) / 2)             // partial overlap: both halves
        left_sum ← self.QueryAt(2 * node, lo, mid, left, right)
        right_sum ← self.QueryAt(2 * node + 1, mid + 1, hi, left, right)
        RETURN left_sum + right_sum
```

The build fills each of the `2n - 1` nodes once, `O(n)`; `update` and `query` each cost `O(log n)`, and the tree takes `O(n)` space. Reach for a segment tree when range questions interleave with changes: sums, minimums or maximums of a changing array, or counts over ranges of values, as in Count of Smaller Numbers After Self, where the tree, indexed by value rank, counts the numbers already passed on a walk from the right. Swapping `+` for `min` or `max`, and the no-overlap `0` for `∞` or `-∞`, gives the minimum and maximum trees. A Fenwick tree, or binary indexed tree, answers prefix sums with point updates in about ten lines at the same `O(log n)`, but it turns prefixes into ranges by subtraction, so it does not carry over directly to minimum and maximum. Adding to a whole range at once needs lazy propagation, which parks pending updates on nodes. The classic mistake is sizing the array `2n` because the tree has `2n - 1` nodes: the heap numbering leaves gaps, and with six elements the deepest leaf is node 13, past the end of a 12-slot array.

*Practice:* LC 307 Range Sum Query - Mutable · LC 315 Count of Smaller Numbers After Self · LC 308 Range Sum Query 2D - Mutable · LC 303 Range Sum Query - Immutable
