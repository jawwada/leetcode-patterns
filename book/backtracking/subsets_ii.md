# Subsets II

*LeetCode 90 · Medium · Pattern: Backtracking with sort + skip-duplicates-at-same-depth · Reading time ~7 min*

## What the problem is really asking

Same as Subsets, with one change: the input may contain repeated values, and the output must not contain the same subset twice. "Same" means same multiset of values. With `[1,2,2]`, picking the first 2 or the second 2 gives the same subset `[2]`, and it must appear only once.

```text
 nums = [1, 2, 2]     index:  0  1  2
                       value:  1  2  2

 distinct subsets (6, not 2^3 = 8):
   []   [1]   [2]   [1,2]   [2,2]   [1,2,2]

 [2] can be made from index 1 OR index 2
 [1,2] can be made from {0,1} OR {0,2}
```

The answer is still a list of lists, but its size is no longer 2^n. If a value appears d times, a subset can contain 0, 1, ..., d copies of it, so the count is the product of (d + 1) over the distinct values. Here that is (1+1)·(2+1) = 6. The difficulty is generating exactly those 6, not 8 and then cleaning up.

## Do it by hand first

On paper, a person would not think of "the first 2" and "the second 2". They would think in terms of how many 2s to take.

```text
 how many 1s?   how many 2s?   subset
     0              0          []
     0              1          [2]
     0              2          [2,2]
     1              0          [1]
     1              1          [1,2]
     1              2          [1,2,2]
```

The hand treated equal values as interchangeable and decided a count per distinct value. Keep that in mind: it means that among "next element to add", two copies of the same value are one option, not two. The thing your hand tracked was the current subset plus "which distinct value am I deciding about now", and it naturally kept equal values together.

## The first honest attempt

Run the Subsets algorithm unchanged, convert each subset to a sorted tuple, throw them into a set.

```text
 Subsets on [1,2,2] (indices) -> values
   {}      -> []
   {0}     -> [1]
   {0,1}   -> [1,2]
   {0,1,2} -> [1,2,2]
   {0,2}   -> [1,2]     duplicate of {0,1}
   {1}     -> [2]
   {1,2}   -> [2,2]
   {2}     -> [2]       duplicate of {1}
```

Cost O(n · 2^n) time and O(n · 2^n) space for the set. It is correct, but look at where the work goes. In the tree, whole subtrees are generated twice:

```text
                  []
         /         |         \
       [1]        [2]a       [2]b      <- same value
      /   \         |
  [1,2]a [1,2]b   [2,2]
     |      ^
 [1,2,2]    same value as left sibling
```

`[2]b`'s subtree (just `[2]b` itself here) is a copy of the leftmost part of `[2]a`'s subtree. With d copies of a value, a subset with j of them is built C(d, j) times. For `[2,2,2,2]` the subset `[2,2]` is built six times. All of that is generated, sorted, hashed, and discarded.

## The turning point

**Claim: if the input is sorted, then among the children of a single node, a child whose value equals its left sibling's value roots a subtree that only repeats subsets already produced under that left sibling; skipping it loses nothing.**

Why? Siblings are the candidates for "the next element" from the same node, at indices `start, start+1, ...`. Suppose `nums[i] == nums[i-1]` and both are children of the node. The left sibling at `i-1` may continue with any index from `i` onward, including `i` itself. The right sibling at `i` may continue with any index from `i+1` onward. Map each subset under the right sibling (`nums[i]` plus some indices after `i`) to the same set with `i` replaced by `i-1`: it is a subset under the left sibling with the same values. So the right sibling's subtree is a strict subset, by value, of the left sibling's.

```text
 children of [] after sorting [1,2,2]:

                 []
        /         |         \
      [1]        [2]        [2]
                  |          x  equal to left sibling:
                [2,2]           everything it could build
                                ([2] and nothing else) is
                                already under [2]
```

Why does sorting matter? The skip is a single comparison with the immediate left neighbour. That only catches all equal siblings if equal values are adjacent. Sorting lines them up.

Why `i > start` and not `i > 0`? Because the rule is about **siblings**. When `i == start`, the element at `i` is the first child of this node; its "left neighbour" `i-1` is the element the parent just chose, which sits on the path, not beside it. Taking a second 2 right after the first 2 (`[2] -> [2,2]`) is how you decide "take two copies". Forbid that and `[2,2]` disappears.

```text
 i > start compares SIBLINGS     i > 0 compares across LEVELS
         [2]                          [2]
          |   i = start = 2            |   i = 2, nums[1] == 2
        [2,2]  allowed               [2,2]  x  wrongly pruned
```

So the change to the Subsets code is one sort and one guard at the top of the loop: `if i > start and nums[i] == nums[i-1]: continue`. In the language of the hand method: at any node, equal values are one option, and "how many copies" is decided by going deeper, never by trying equal siblings.

## Watch it work

Example `nums = [1, 2, 2]` (already sorted). Legend: `*` current path, `<-` current node, `?` not visited, `x` pruned (never entered). Index labels on edges: `2a` is index 1, `2b` is index 2.

**Frame 1.** Record `[]`, choose 1, record `[1]`, choose 2a, record `[1,2]`, choose 2b, record `[1,2,2]`.

```text
                 *[]
        /          |          \
     *[1]          ?           ?
     /   \
 *[1,2]a   ?
    |
 *[1,2,2] <-
 path=[1,2,2]  start=3  depth 4
 result=[[],[1],[1,2],[1,2,2]]
```

At node `[1,2]a` the child 2b had `i == start`, so it was not a sibling duplicate. It is the second copy, taken deeper.

**Frame 2.** Pop back to `[1]`. Its loop moves to i = 2 (value 2b). `i > start` (2 > 1) and `nums[2] == nums[1]`: prune.

```text
                 *[]
        /          |          \
     *[1] <-       ?           ?
     /   \
  [1,2]   x 2b   same value as sibling 2a
    |
 [1,2,2]
 path=[1]  start=1  depth 2
 result unchanged
```

Without this cut, `[1,2]` would be emitted a second time.

**Frame 3.** Pop to the root. Its loop tries i = 1 (2a): i > start, but nums[1] = 2 differs from nums[0] = 1, so no skip. Choose 2, record `[2]`, choose 2b at i == start = 2, record `[2,2]`.

```text
                 *[]
        /          |          \
     [1]         *[2]a         ?
     /   \         |
  [1,2]   x     *[2,2] <-
    |
 [1,2,2]
 path=[2,2]  start=3  depth 3
 result=[...,[1,2,2],[2],[2,2]]
```

**Frame 4.** Pop to the root. Its loop tries i = 2 (2b): `i > start` (2 > 0) and `nums[2] == nums[1]`: prune. Loop ends; the walk is over.

```text
                  []
        /          |          \
     [1]          [2]          x 2b
     /   \         |
  [1,2]   x      [2,2]
    |
 [1,2,2]
 path=[]  stack empty
 result=[[],[1],[1,2],[1,2,2],[2],[2,2]]
```

Six answers, matching the solution's output, with no set used.

In every frame, among the children of any node, values were strictly increasing left to right after the cuts, while along any path values could repeat. That is the whole rule: no repeats across siblings, repeats allowed down a path.

## Why it is correct

*No duplicates.* Suppose two different emitted nodes hold the same multiset. Each path has increasing indices, so its values are in sorted order, and the two value sequences are identical. Follow both paths from the root; they agree for a while and then, at some node N, pick different indices i < j that carry the same value. Both are children of N, so `start <= i < j`. The array is sorted, so every index from i to j holds that value; in particular `nums[j] == nums[j-1]` and `j > start`. The guard skips j. Contradiction: the second path was never walked.

*Nothing missing.* Take any target multiset, say with values in sorted order `v1 <= v2 <= ...`. Build it greedily: at each node choose the smallest unused index holding the next needed value. That index is always the first in its run among the node's candidates, or it equals `start` (when the previous pick was the same value at the previous index). Either way the guard lets it through. So every distinct multiset is reached.

Together: every distinct subset is emitted exactly once.

## Cost

- **Time: O(n · 2^n) worst case**, when all values are distinct (then it is exactly Subsets). With repeats, it is O(n · number of distinct subsets) plus O(n log n) for the sort; the pruned siblings cost O(1) each.
- **Space: O(n)** for the path and recursion beyond the output; no set of seen tuples.

## Variations you will meet

- **Combination Sum II.** Same duplicate rule, plus a sum budget. Three problems from now.
- **Permutations II (LeetCode 47).** Duplicates in a pick-from-set tree. The sibling rule becomes: skip `nums[i]` if it equals `nums[i-1]` and `nums[i-1]` is not currently used. The "not used" plays the role of `i > start`: it says the equal neighbour is a sibling option, not something already on the path.
- **Count-based recursion.** Compress the input into `(value, count)` pairs and at level k loop "take 0..count copies of value k". It makes the hand method literal and avoids the guard entirely.
- **Brute force with a set.** Acceptable for n <= 10 in a pinch; say out loud that it generates C(d, j) duplicates and that pruning removes them at the source.

## What to carry forward

Sort so equal values touch, then let equal values be one choice among siblings and a "how many" choice down the path: `i > start and nums[i] == nums[i-1]` means skip. The next problem changes the tree's shape: instead of picking from an index onward, every slot may pick any value not yet used, and that needs a `used` array instead of `start`.
