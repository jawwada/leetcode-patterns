# Permutations

*LeetCode 46 · Medium · Pattern: Backtracking with a used-set · Reading time ~7 min*

## The problem

Given an array of distinct integers, return all possible orderings (permutations) of its elements, in any order.

```text
Example: [1,2,3] ->
  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]. Example:
  [1] -> [[1]].
```

## What the problem is really asking

Given n distinct integers, list every way to arrange all of them in a row. Unlike subsets, every answer uses every element, and order now matters: `[1,2,3]` and `[2,1,3]` are different answers.

The answer is a list of n! sequences, each of length n.

```text
 nums = [1, 2, 3]

 slot:      0   1   2
           [1,  2,  3]     [2,  1,  3]     [3,  1,  2]
           [1,  3,  2]     [2,  3,  1]     [3,  2,  1]

 3 choices for slot 0, then 2, then 1: 3 x 2 x 1 = 6
```

The difficulty is the opposite of Subsets. There, you prevented reorderings by only picking to the right. Here reorderings are the point, so "pick from an index onward" is wrong: after placing 3 first you still need to place 1 and 2, which sit to its left. You need a different way to remember what is still available.

## Do it by hand first

Fill the slots left to right. At each slot, write any number you have not written yet. When a row is full, back up to the last slot where you had an untried option.

```text
 slot0  slot1  slot2     what I still hold
   1                     {2,3}
   1      2              {3}
   1      2      3       {}        -> write down 123
   1      3              {2}       (back up, try 3 in slot1)
   1      3      2       {}        -> write down 132
   2                     {1,3}     (back up to slot0)
   ...
```

The thing your hand tracked was the column on the right: **which numbers are still in my hand**. Each time you wrote one down it left your hand; each time you erased one it came back. That "in hand / on the paper" bit per number is the seed of the `used` array.

## The first honest attempt

The plainest idea: generate every length-n sequence over the n values (`itertools.product(nums, repeat=n)`), keep those with no repeated value.

```text
 product([1,2,3], repeat=3): 27 sequences
   111 x  112 x  113 x  121 x  122 x  123 ok  131 x ...
   ...  only 6 of the 27 survive the filter

 n = 8:  8^8 = 16,777,216 sequences for 40,320 answers
```

Cost O(n · n^n) time. The waste is visible in the sequence `1 1 ...`: the repeat is obvious at slot 1, yet the method fills slot 2 (and, for bigger n, every slot after) before checking. Every sequence that begins `1 1` is a whole dead subtree of size n^(n-2) that is fully generated and then thrown away.

```text
                  root
        /          |          \
       1           2           3
     / | \       / | \       / | \
    1  2  3     1  2  3     1  2  3
   /|\ ...     ...         ...
   ^ dead the moment it is drawn, yet expanded to the leaves
```

## The turning point

**Claim: if you refuse to place a value that is already on the path at the moment you choose it, every branch you enter is a prefix of a valid permutation, and the tree shrinks from n^n leaves to exactly n! leaves with no dead ends.**

Justification: a prefix with no repeated value can always be completed (put the remaining values in any order), so no such branch is dead. A prefix with a repeat can never be completed. So "no repeat so far" is exactly the right test, and it is checkable in O(1) per choice if you keep a boolean `used[i]` per index.

That gives the third template from the background, **pick-from-set**. At every node the children are all indices whose `used` flag is false. The level-k node has n - k children: n at the root, then n - 1, down to 1.

```text
 pick-from-set on [1,2,3]
                      []
          /           |           \
        [1]          [2]          [3]
       /   \        /   \        /   \
   [1,2] [1,3]  [2,1] [2,3]  [3,1] [3,2]
     |     |      |     |      |     |
  [123] [132]  [213] [231]  [312] [321]
```

The choose/explore/un-choose triple now has two pieces of shared state to keep in sync:

```text
   choose      used[i] = True ; path.append(nums[i])
   explore     dfs()
   un-choose   path.pop()     ; used[i] = False
```

Compare with Subsets. There, the `start` index was the memory of "what may come next", and it was passed as an argument, so it reset itself on return. Here the memory is a mutable array, so un-choose must reset it by hand. Forget `used[i] = False` and, after the first leaf, value i is never offered again anywhere.

Where is the answer? Only at leaves, when `len(path) == n`. Internal nodes are partial arrangements, not answers. That differs from Subsets, where every node was an answer.

Why not test `nums[i] in path`? It works and is O(n) per test instead of O(1). For n <= 8 nobody will notice, but the `used` array is also the habit that carries over: in N-Queens it becomes "column used", in Word Search "cell visited".

## Watch it work

Example `nums = [1, 2, 3]`. Legend: `*` current path, `<-` current node, `?` not visited, `xV` the child for value V is pruned because V is used.

**Frame 1.** Choose 1, then 2 (1 is pruned at depth 1), then 3 (1 and 2 pruned at depth 2). Leaf: record `[1,2,3]`.

```text
                  *[]
        /          |          \
     *[1]          ?           ?
    /  |   \
  x1 *[1,2]  ?
     / |  \
   x1  x2 *[1,2,3] <-
 path=[1,2,3]  used=[T,T,T]  depth 4
 result=[[1,2,3]]
```

**Frame 2.** Pop 3 (used[2] = F), and node `[1,2]` has no options left; pop 2 (used[1] = F). At `[1]`, try 3, then 2 (1 and 3 pruned). Record `[1,3,2]`.

```text
                  *[]
        /          |          \
     *[1]          ?           ?
    /  |   \
  x1 [1,2] *[1,3]
       |    / |  \
   [1,2,3] x1 *[1,3,2] x3
                  <-
 path=[1,3,2]  used=[T,T,T]  depth 4
 result=[[1,2,3],[1,3,2]]
```

Between frames the `used` array went T,T,T -> T,F,F -> T,F,T -> T,T,T: every flag came back before a sibling was tried.

**Frame 3.** Unwind to the root, unmark 1. Choose 2. At `[2]`: 1 is free, 2 is pruned, 3 is free. Take 1, then 3. Record `[2,1,3]`.

```text
                  *[]
        /          |          \
      [1]        *[2]          ?
    (done)      /  |   \
           *[2,1]  x2   ?
            / | \
          x1 x2 *[2,1,3] <-
 path=[2,1,3]  used=[T,T,T]  depth 4
 result=[[1,2,3],[1,3,2],[2,1,3]]
```

**Frame 4.** Back at `[2]`, try 3, then 1. Record `[2,3,1]`.

```text
                  *[]
        /          |          \
      [1]        *[2]          ?
    (done)      /  |   \
           [2,1]   x2  *[2,3]
             |         / | \
         [2,1,3] *[2,3,1] x2 x3
                     <-
 path=[2,3,1]  used=[T,T,T]  depth 4
```

**Frame 5.** The `[3]` subtree runs the same way, recording `[3,1,2]` and `[3,2,1]`. The root's loop ends.

```text
                   []
        /          |          \
      [1]         [2]         [3]
    (done)      (done)       /  |  \
                         [3,1] [3,2] x3
                           |     |
                       [3,1,2] [3,2,1]
 path=[]  used=[F,F,F]  stack empty
 result: 6 permutations, in lexicographic order
```

At every moment `used[i]` was true exactly for the indices on the starred path, and `len(path)` equalled depth minus one. Each pruned `x` sat directly under a node whose path already contained that value.

## Why it is correct

*Invariant.* At entry to `dfs()`, `used[i]` is true iff `nums[i]` is on `path`, and `path` has no repeats. Choose sets one flag and appends the same element, preserving it; un-choose reverses both in the opposite order, restoring the entry state. By induction it holds at every call and every return.

*Completeness.* Any permutation `p0 p1 ... p(n-1)` is reachable: at depth k, `pk` is not on the path (the path is `p0..p(k-1)`, all distinct from `pk`), so its flag is false and the loop tries it.

*No duplicates.* Two different leaves differ in some first slot, where they took different indices with different values (inputs are distinct), so they record different sequences.

*Only valid sequences.* Leaves have length n with no repeats, hence use every value exactly once.

## Cost

- **Time: O(n · n!).** There are n! leaves, each copied in O(n). Internal nodes number about (e - 1) · n!, and each scans n flags, which is also O(n · n!).
- **Space: O(n)** beyond the output: the path, the used array, and n + 1 stack frames.

## Variations you will meet

- **Permutations II (LeetCode 47): duplicates in the input.** Sort, then skip `nums[i]` when `nums[i] == nums[i-1]` and `not used[i-1]`. The `not used[i-1]` says "the equal twin is a sibling option, not already placed", the same idea as `i > start` in Subsets II.
- **Swap-based permutation.** Instead of a used array, swap `nums[k]` with each `nums[i]` for `i >= k`, recurse on k + 1, swap back. The prefix `nums[0..k-1]` is the path, the suffix is the hand. No extra memory, but output order is not lexicographic.
- **Next Permutation / k-th permutation.** When only one permutation is wanted, do not walk the tree: compute the next one in O(n) or index into the factorial number system.
- **N-Queens.** A permutation of columns, one per row, with extra diagonal constraints pruning more children. The used array is exactly "column taken".

## What to carry forward

Pick-from-set: any unused element may fill the next slot, a `used` flag per element remembers the hand, and both the path and the flag are undone on the way back. The next problem returns to pick-from-index but adds a budget: a running sum that cuts a whole subtree the moment it overflows.
