# Combination Sum II

*LeetCode 40 · Medium · Pattern: Backtracking with sort + skip-duplicates-at-same-depth · Reading time ~7 min*

## The problem

Given candidates (which may repeat) and a target, return all unique combinations summing to target where each
candidate index is used at most once.

```text
Example: candidates=[10,1,2,7,6,1,5], target=8 ->
  [[1,1,6],[1,2,5],[1,7],[2,6]].
```

## What the problem is really asking

You get a list of positive numbers that may contain repeats, and a target. Find every distinct multiset of them that sums to the target, where each **position** in the list can be used at most once. If the list has three 2s, an answer may contain up to three 2s, never four. And `[1,2,2]` built from different 2s still counts as one answer.

```text
 candidates = [2, 5, 2, 1, 2]    target = 5

 sorted:      [1, 2, 2, 2, 5]
 index:        0  1  2  3  4

 answers:  1 + 2 + 2 = 5   ->  [1,2,2]
           5         = 5   ->  [5]

 [1,2,2] can be built from indices {0,1,2}, {0,1,3}
 or {0,2,3}: three index sets, one answer
```

The answer is a list of lists. This problem is the meeting point of two earlier ones: from Combination Sum it inherits the target and the "too big, stop" cut; from Subsets II it inherits duplicate values that must not produce duplicate answers. The only new rule is "each index once", which is a one-character change.

## Do it by hand first

By hand, you would first group the numbers: one 1, three 2s, one 5. Then ask "how many of each" while tracking what is left of the target.

```text
 left 5.  how many 1s? (have 1)
   take one 1 -> left 4.  how many 2s? (have 3)
     take two -> left 0.  [1,2,2]  done
     take one -> left 2.  5s? too big. dead
     take three -> 6 > 4. impossible
   take zero 1s -> left 5.  how many 2s?
     two -> left 1. 5 too big. dead
     ...
     zero 2s -> one 5 -> left 0.  [5]  done
```

Two things were tracked: **the remaining budget** and **which distinct value I am deciding on next**. The hand never chose "the first 2" or "the third 2"; equal values were one decision with a count. That is the sort + skip rule in human form.

## The first honest attempt

Enumerate every subset of indices with a bitmask, keep those whose sum is the target, put the sorted tuple in a set to remove duplicates.

```text
 2^5 = 32 index sets for [1,2,2,2,5]
   {0,1,2} -> (1,2,2)  sum 5  keep
   {0,1,3} -> (1,2,2)  sum 5  keep  (already in set)
   {0,2,3} -> (1,2,2)  sum 5  keep  (already in set)
   {1,2,3,4} -> sum 11      decoded, summed, rejected
   ...
```

O(n · 2^n) time, plus a set of tuples. Two kinds of waste, both drawn above. First, a set like `{1,2,3,4}` overshoots as soon as its third 2 is added (2+2+2 = 6), yet it is decoded and summed in full. Second, the same answer is built once per choice of which copies, here three times, then deduplicated after the fact.

## The turning point

**Claim: after sorting, two independent cuts remove both kinds of waste: break when the next candidate exceeds the remaining budget, and skip a candidate equal to its left sibling at the same node.**

Each cut was justified in its own chapter; here is why they compose cleanly.

*Cut 1, budget break (from Combination Sum).* All values are positive, so remaining only decreases. Sorted ascending, the first child that overshoots means every child to its right overshoots too: `break`.

*Cut 2, sibling skip (from Subsets II).* At a node with children at indices `start, start+1, ...`, if `i > start` and `candidates[i] == candidates[i-1]`, the subtree under i is a by-value copy of part of the subtree under i - 1. Skip it with `continue`. Going deeper and taking the next equal value (i == start) is still allowed; that is how `[1,2,2]` gets its second 2.

*Each index once.* Recurse with `i + 1`, not `i`. That is the only line that differs from Combination Sum.

```text
 three problems, three loop bodies
                  dedupe sibling?   overflow cut?  recurse
 Subsets II        yes               no            i + 1
 Combination Sum   no                break         i
 Comb. Sum II      yes               break         i + 1
```

*Order of the two tests.* Check the break first. If `candidates[i] > remaining`, nothing to the right matters, duplicate or not. If the value fits, then check for a duplicate sibling. Swapping them is still correct but can loop over a run of too-large duplicates before stopping.

```text
 node "left 4", start=1, sorted candidates from index 1:
     2a     2b     2c     5
     take   x dup  x dup  x break (5 > 4)
```

Why does the combination not interfere? The budget cut removes children by value; the duplicate cut removes children by being equal to a left neighbour. A child removed by either has no answers that are not already produced elsewhere (none at all for the budget cut; copies for the duplicate cut). Removing a union of such children is still safe.

## Watch it work

Example: `candidates = [2,5,2,1,2]`, `target = 5`, sorted to `[1,2,2,2,5]`. The three 2s are labelled `2a 2b 2c` (indices 1, 2, 3). Sideways tree: nodes show remaining budget. Legend: `*` current path, `<-` current node, `x dup` sibling skip, `x brk` budget break, `?` not visited.

**Frame 1.** Take 1 (left 4, start 1), take 2a (left 2, start 2), take 2b (left 0): record `[1,2,2]`.

```text
 *5
 +-1-> *4
 |     +-2a-> *2
 |     |      +-2b-> *0 <-  record [1,2,2]
 |     |      +-?
 |     +-?
 +-?
 path=[1,2,2]  result=[[1,2,2]]
```

2b here is at `i == start`, so it is the "second copy, deeper" case and is allowed.

**Frame 2.** Back at "left 2" (start 2): 2c is a duplicate sibling of 2b, skip; 5 > 2, break. Back at "left 4": 2b and 2c are duplicate siblings of 2a, skip; 5 > 4, break.

```text
 *5
 +-1-> *4 <-
 |     +-2a-> 2
 |     |      +-2b-> 0   [1,2,2]
 |     |      +-2c x dup
 |     |      +-5  x brk
 |     +-2b x dup
 |     +-2c x dup
 |     +-5  x brk
 +-?
 path=[1]  remaining=4
```

Without the skips, `[1,2,2]` would be found twice more, via (2a,2c) and (2b,2c).

**Frame 3.** Root takes 2a (left 3, start 2). Take 2b (left 1, start 3): 2c > 1, break. Back at "left 3": 2c dup, 5 brk.

```text
 *5
 +-1-> 4   (done)
 +-2a-> *3 <-
 |      +-2b-> 1
 |      |      +-2c x brk (2 > 1)
 |      +-2c x dup
 |      +-5  x brk
 +-?
 path=[2]  remaining=3
```

**Frame 4.** Root: 2b and 2c are duplicate siblings of 2a, skip. Take 5 (left 0): record `[5]`. Loop ends.

```text
 5
 +-1-> 4   (done)
 +-2a-> 3  (done)
 +-2b x dup
 +-2c x dup
 +-5-> 0   record [5]
 result=[[1,2,2],[5]]   stack empty
```

The two answers match the solution's output. Across frames, the children of any node that were actually entered had strictly increasing values, remaining always equalled 5 minus the path sum, and indices along any path strictly increased.

## Why it is correct

*Soundness.* A path is recorded only at remaining 0, so its sum is the target. Indices strictly increase along a path (recursion with `i + 1`), so each position is used at most once.

*Completeness.* Take any valid multiset and write it in sorted order. Build it by always choosing, among positions holding the next needed value, the leftmost one not before `start`. That position is either `start` itself (when the previous pick was the same value at the previous position) or the first of its run among this node's children; either way the duplicate guard lets it through. Its value is at most remaining (the rest of the answer is positive), so the break does not stop before it.

*Uniqueness.* If two recorded paths had the same multiset, at their first difference they would be sibling children with equal values at different indices; sortedness makes the later one adjacent to an equal left neighbour inside the same node's range, and the guard would have skipped it.

## Cost

- **Time: O(2^n)** in the worst case (each index in or out) plus O(n) per recorded answer, plus O(n log n) for the sort. Both cuts usually shrink the tree drastically.
- **Space: O(n)** for the path and recursion, beyond the output.

## Variations you will meet

- **Subsets II with a target.** That is this problem; recognising it as "Subsets II + budget" is the whole interview.
- **Combination Sum III (LeetCode 216).** Values 1..9, each once, exactly k numbers. No duplicates in the input, so no skip; add a length cut (`len(path) == k`).
- **Partition to K Equal Sum Subsets (LeetCode 698).** Several buckets each with a target. Sort descending so the budget cut fires early, and skip trying equal values in the same bucket, the same sibling-dedupe idea applied to buckets.
- **Counting instead of listing.** "How many distinct multisets" with large n is a bounded-knapsack DP over (value, count), not a tree walk.

## What to carry forward

Sort once, then two lines guard the loop: break on the first overflow, skip an equal sibling; recurse with `i + 1` because each index is used once. The next problem drops sums and duplicates entirely: each level has its own alphabet, and the tree has a fixed depth.
