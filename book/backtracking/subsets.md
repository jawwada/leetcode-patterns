# Subsets

*LeetCode 78 · Medium · Pattern: Backtracking include/exclude decision tree · Reading time ~7 min*

## The problem

Given an array of distinct integers, return all possible subsets (the power set) in any order, with no duplicate
subsets.

```text
Example: [1,2,3] -> [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]].
```

## What the problem is really asking

You get a list of distinct integers. Return every possible selection of them: the empty selection, every single element, every pair, and so on up to the whole list. Order inside a subset does not matter, and no subset may appear twice.

The answer is a list of lists, and its size is fixed by arithmetic: each of the n elements is either in or out, so there are exactly 2^n subsets. For n = 3 that is 8.

```text
 nums = [1, 2, 3]

 size 0:  []
 size 1:  [1]   [2]   [3]
 size 2:  [1,2] [1,3] [2,3]
 size 3:  [1,2,3]
                        total 1 + 3 + 3 + 1 = 8 = 2^3
```

What makes it "hard" is not finding the answers, since every combination is valid. It is producing each one exactly once, with no duplicates like `[2,1]` next to `[1,2]`, and doing it with a method that will survive when later problems add rules. This problem is where the chapter's template is born.

## Do it by hand first

Ask yourself to write all subsets of `{1, 2, 3}` on paper without missing any. Most people settle into a rhythm like this:

```text
 start with nothing:            []
 add 1:                         [1]
   add 2 after it:              [1,2]
     add 3 after that:          [1,2,3]
   back to [1], add 3 instead:  [1,3]
 back to nothing, add 2:        [2]
   add 3 after it:              [2,3]
 back to nothing, add 3:        [3]
```

Look at what your hand did. It never wrote `[2,1]`, because after writing 2 you only ever added numbers to the right of 2. And it kept a "current list" that grew by one and then shrank by one: `[1] -> [1,2] -> [1,2,3] -> [1,2] -> [1] -> [1,3]`. Your hand was tracking two things:

1. the current partial subset (a stack: push on the right, pop from the right), and
2. the position from which you are allowed to pick next.

That pair, `(path, start)`, is the entire state of the algorithm.

## The first honest attempt

A strong candidate's first answer is usually the bitmask trick: subsets of n items correspond one-to-one with n-bit numbers. Loop `mask` from 0 to 2^n - 1; for each mask, collect `nums[i]` whenever bit i is set.

```text
 mask  bits(3 2 1)  subset
  0     0 0 0       []
  1     0 0 1       [1]
  2     0 1 0       [2]
  3     0 1 1       [1,2]
  4     1 0 0       [3]
  5     1 0 1       [1,3]
  6     1 1 0       [2,3]
  7     1 1 1       [1,2,3]
```

It is correct and costs O(n · 2^n). The output itself has that size, so you cannot beat it asymptotically. Why not stop here?

Because of where the work goes. Every mask is decoded from scratch. Masks 3 and 7 both start by testing bits 0 and 1 and building `[1,2]`; mask 7 rebuilds that prefix instead of extending the one mask 3 already built.

```text
 mask 3:  test b0 -> 1, test b1 -> 2, test b2 -> no   [1,2]
 mask 7:  test b0 -> 1, test b1 -> 2, test b2 -> 3    [1,2,3]
          \________ same prefix rebuilt ________/
```

More importantly, the bitmask gives you no place to stand when a rule arrives. If a later problem says "only subsets with sum 7", the mask approach must still build all 2^n subsets and filter at the end. There is no moment where it can say "this prefix already sums to 9, stop".

## The turning point

**Claim: the subsets are the nodes of a tree in which each node extends its parent by one element taken from the right of the parent's last element; walking that tree depth first with one shared list visits every subset exactly once.**

Justify each half.

*Every subset appears.* Take any subset, write its elements in index order, for example `[1,3]`. Start at the root `[]`, take the edge for 1, then the edge for 3. Both edges are legal because 3 is to the right of 1. So every subset is the end of a unique root-to-node path.

*No subset appears twice.* A node's path is a sequence of increasing indices. Two different paths give two different increasing sequences, and an increasing sequence is determined by its set of indices. So distinct nodes are distinct subsets.

```text
 pick-from-index tree for [1,2,3]; every node is a subset
                    []
           /         |        \
         [1]        [2]       [3]
        /   \        |
    [1,2]  [1,3]   [2,3]
      |
  [1,2,3]
```

Now turn the tree into an algorithm. You do not build it. You walk it with a function `dfs(start)` and one list `path`:

- On entering a node, record a copy of `path`. Every node is an answer.
- For each `i` from `start` to `n-1`: append `nums[i]` (choose), call `dfs(i+1)` (explore), pop (un-choose).

The `i + 1` is what encodes "to the right of the last element". The append/pop pair is what makes `path` equal "the edges from root to here" at every moment. Recording `path[:]` instead of `path` freezes a snapshot; the live list keeps changing.

This is the include/exclude decision tree from the background with the "skip" chains folded. In the binary tree, "skip 1, skip 2, take 3" is three levels; here it is one edge `[] -> [3]`. Same 8 answers, 8 nodes instead of 15, and every node is useful.

The prize is the template. Combination Sum adds a single `if` before the append to cut a subtree; Subsets II adds a single `if` to skip duplicate siblings. The skeleton never changes.

## Watch it work

Example `nums = [1, 2, 3]`. Legend: `*` on the current path, `<-` current node, `?` not visited yet, plain means finished. No branch is pruned in this problem: every node is a valid subset, so no `x` appears.

**Frame 1.** Enter the root and record it.

```text
                 *[] <-
          /        |        \
         ?         ?         ?
 path=[]  start=0  stack depth 1
 result=[[]]
```

The root is the empty subset; the loop is about to try i = 0.

**Frame 2.** Choose 1, descend, record; then choose 2, descend, record; then choose 3, descend, record.

```text
                 *[]
          /        |        \
       *[1]        ?         ?
       /   \
   *[1,2]    ?
      |
  *[1,2,3] <-
 path=[1,2,3]  start=3  stack depth 4
 result=[[],[1],[1,2],[1,2,3]]
```

Three appends, three recorded copies. At start=3 the loop is empty, so this call returns.

**Frame 3.** Pop 3, return to `[1,2]` (its loop is done), pop 2, return to `[1]`, whose loop now tries i = 2.

```text
                 *[]
          /        |        \
       *[1]        ?         ?
       /   \
    [1,2]  *[1,3] <-
      |
  [1,2,3]
 path=[1,3]  start=3  stack depth 3
 result=[[],[1],[1,2],[1,2,3],[1,3]]
```

The pencil line `[1,2,...]` was erased segment by segment before `[1,3]` was drawn.

**Frame 4.** Back at the root: pop 1, choose 2, record `[2]`, choose 3, record `[2,3]`.

```text
                 *[]
          /        |        \
       [1]       *[2]        ?
       /   \       |
    [1,2] [1,3] *[2,3] <-
      |
  [1,2,3]
 path=[2,3]  start=3  stack depth 3
 result=[...,[1,3],[2],[2,3]]
```

Nothing to the right of 3, so `[2,3]` returns at once.

**Frame 5.** Unwind to the root, choose 3, record `[3]`; its loop (start=3) is empty; return; the root's loop ends.

```text
                  []
          /        |        \
       [1]        [2]      [3]
       /   \       |
    [1,2] [1,3]  [2,3]
      |
  [1,2,3]
 path=[]  stack empty
 result=[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
```

Eight nodes, eight answers, in exactly the order the solution returns them.

Across every frame, `path` equalled the starred nodes' last label sequence, the stack depth was `len(path) + 1`, and every index on the path was strictly increasing. When a call returned, `path` was one element shorter than during it, never longer.

## Why it is correct

Two properties, both maintained by the choose/explore/un-choose pattern.

*Path invariant.* When `dfs(start)` begins, `path` lists the elements chosen on the way down, their indices are increasing, and every index is below `start`. The call appends `nums[i]` with `i >= start` (still increasing), recurses with `i + 1` (so the child's `start` exceeds every index on its path), and pops before the next `i` (restoring the precondition for the next sibling). By induction it holds at every call and is restored at every return.

*Bijection.* Each call records its `path` once. By the path invariant, recorded lists correspond to increasing index sequences, which correspond one-to-one with subsets of indices. The loop at each node tries every legal next index, so every increasing sequence is reached. So each of the 2^n subsets is recorded exactly once.

Copying matters for correctness, not just style: `result.append(path)` would store 8 references to the same list, which is empty when the walk ends.

## Cost

- **Time: O(n · 2^n).** The tree has 2^n nodes, each does O(1) append/pop plus an O(n) copy when it records itself.
- **Space: O(n) beyond the output.** The path and the call stack are at most n + 1 deep; the output itself is O(n · 2^n).

## Variations you will meet

- **Subsets II (duplicates in the input).** `[1,2,2]` would produce `[2]` twice. Sort and skip a sibling equal to its left neighbour. That is the very next problem.
- **Combinations (LeetCode 77): all subsets of size k.** Record only when `len(path) == k` and return there. Prune when there are too few elements left to reach k: loop `i` only up to `n - (k - len(path))`.
- **Include/exclude form.** Write `dfs(i)` that either takes `nums[i]` or skips it and records only at `i == n`. Same answers, a binary tree with 2^n leaves; it is the natural form when each item has exactly two fates (Partition to K Equal Sum Subsets, Target Sum).

## What to carry forward

A subset is a root-to-node path of increasing indices; walk the tree with one list you push before recursing and pop after, and record a copy at every node. The next problem keeps this exact tree but feeds it repeated values, and adds one line to cut the branches that would repeat a subset.
