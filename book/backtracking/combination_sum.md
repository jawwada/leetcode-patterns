# Combination Sum

*LeetCode 39 · Medium · Pattern: Backtracking with start index and sum pruning · Reading time ~7 min*

## The problem

Given distinct positive candidates and a target, return all unique combinations (each candidate may be reused any
number of times) that sum to target; order inside a combination does not matter.

```text
Example: candidates=[2,3,6,7], target=7 -> [[2,2,3],[7]].
```

## What the problem is really asking

You have a set of distinct positive numbers, the candidates, and a target. Find every multiset of candidates that adds up to the target. You may use a candidate as many times as you like. Order does not matter: `[2,2,3]` and `[3,2,2]` are the same answer and must appear once.

The answer is a list of lists. Unlike Subsets, most combinations are not answers; only those with the exact sum are. And unlike Subsets, a combination has no length limit set by n: with candidate 2 and target 40, the answer `[2]*20` is twenty long.

```text
 candidates = [2, 3, 6, 7]   target = 7

   2 + 2 + 3 = 7   ->  [2,2,3]
   7         = 7   ->  [7]

   2 + 2 + 2 = 6   (1 short; adding 2 more overshoots)
   3 + 3     = 6   (1 short; no candidate equals 1)
```

What makes it hard: the search space is unbounded without the target (you could add 2 forever), duplicates by reordering lurk everywhere, and most partial sums go nowhere.

## Do it by hand first

People do this by working down from the target, writing what is left after each pick, and keeping the picks in non-decreasing order so they never write `[3,2,2]` after `[2,2,3]`.

```text
 left 7: try 2 -> left 5
   left 5: try 2 -> left 3
     left 3: try 2 -> left 1
       left 1: smallest candidate is 2 > 1. Dead.
     left 3: try 3 -> left 0. Found [2,2,3].
     left 3: try 6? 6 > 3. Stop, so will 7.
   left 5: try 3 -> left 2
     left 2: 3 > 2. Dead.
   left 5: try 6? too big. Stop.
 left 7: try 3 -> ...
```

Your hand kept two numbers per line: **what is left** and **the smallest candidate I am still allowed to use**. It also did something sharp without thinking: once 6 was too big, it did not bother with 7. Those three habits (remaining budget, non-decreasing picks, stop at the first overflow) are the algorithm.

## The first honest attempt

A candidate might say: the answer has at most `target // min(candidates)` elements, so for each length r up to that, generate every multiset of size r (`combinations_with_replacement`) and keep those whose sum hits the target.

```text
 target 7, min 2 -> r up to 3, candidates 4 values
 r=1:  4 multisets    r=2: 10    r=3: 20    -> 34 built
 answers: 2

 r=3 multisets that start with 6 or 7:
   (6,6,6) (6,6,7) (6,7,7) (7,7,7)  all built, all > 7
```

The cost is the sum over r of C(n + r - 1, r) times r to sum each one, which explodes with the target. The waste: a multiset is fully built before its sum is looked at. `(6,6,x)` already overshoots after two picks, and every extension of it is hopeless, yet each one is generated and summed. Nothing learned about one failing prefix is used to skip its extensions.

## The turning point

**Claim: because candidates are positive, the remaining budget only shrinks as you go deeper; the moment a pick would make it negative, that child and its entire subtree contain no answer and can be cut.**

That is the first true **prune** of the chapter: a test before descending that removes a whole subtree. Two more decisions finish the design.

*Non-decreasing picks kill reorderings.* Use the pick-from-index template: a node remembers `start`, the smallest index it may pick. A child chosen at index i passes `start = i` down, so later picks are at index i or higher. Every multiset then has exactly one path, its sorted order.

*Passing `i`, not `i + 1`, allows reuse.* In Subsets, the child got `i + 1` because each element was used once. Here the same candidate may be picked again, so the child may still pick index i.

```text
 recursion arguments, the only difference that matters
   Subsets         dfs(i + 1)              each once
   Combination Sum dfs(i, remaining - c)   reuse allowed
```

*Sorting turns `continue` into `break`.* If the candidates are sorted ascending and `candidates[i] > remaining`, every candidate after i is larger still. So one failed comparison cuts the current child and every sibling to its right.

```text
 node "left 5", sorted children from start=0:
     2      3      6      7
     ok     ok     x      (never looked at)
                   ^ 6 > 5: break the loop
```

Answers are nodes where the budget hits exactly 0. Record a copy of the path there and return; there is nothing to gain by going deeper, since every candidate is positive.

So the algorithm is: sort; `dfs(start, remaining)`; if remaining is 0 record; else for i from start, break if `candidates[i] > remaining`, otherwise append, `dfs(i, remaining - candidates[i])`, pop.

## Watch it work

Example `candidates = [2,3,6,7]`, `target = 7`. The tree is drawn sideways: each node shows the remaining budget, each edge the candidate taken. Legend: `*` on the current path, `<-` current node, `x` pruned (break), `?` not visited.

**Frame 1.** Take 2, 2, 2. At "left 1" (start 0) the first candidate 2 > 1: break.

```text
 *7
 +-2-> *5
 |     +-2-> *3
 |     |     +-2-> *1 <-
 |     |     |     +-2 x  (2 > 1, break)
 |     |     +-?
 |     +-?
 +-?
 path=[2,2,2]  remaining=1  depth 4
```

**Frame 2.** Pop to "left 3", take 3 (start 1): remaining 0, record `[2,2,3]`. Back at "left 3", 6 > 3: break.

```text
 *7
 +-2-> *5
 |     +-2-> *3
 |     |     +-2-> 1
 |     |     |     +-2 x
 |     |     +-3-> *0 <-  record [2,2,3]
 |     |     +-6 x  (6 > 3, break; 7 never seen)
 |     +-?
 +-?
 path=[2,2,3]  result=[[2,2,3]]
```

**Frame 3.** Pop to "left 5", take 3 (start 1) -> "left 2": 3 > 2, break. Back at "left 5": 6 > 5, break.

```text
 *7
 +-2-> *5
 |     +-2-> 3   (done)
 |     +-3-> *2 <-
 |     |     +-3 x  (3 > 2)
 |     +-6 x  (6 > 5)
 +-?
 path=[2,3]  remaining=2
```

**Frame 4.** Pop to the root, take 3 (start 1) -> "left 4". Take 3 -> "left 1": 3 > 1, break. At "left 4": 6 > 4, break.

```text
 *7
 +-2-> 5   (done)
 +-3-> *4
 |     +-3-> *1 <-
 |     |     +-3 x  (3 > 1)
 |     +-6 x  (6 > 4)
 +-?
 path=[3,3]  remaining=1
```

Note that 2 is never offered under the 3-branch: start is 1, so `[3,2,...]` cannot be formed, and `[2,3,...]` was already explored.

**Frame 5.** Root takes 6 -> "left 1": 6 > 1, break. Root takes 7 -> "left 0": record `[7]`. Loop ends.

```text
 7
 +-2-> 5   (done)
 +-3-> 4   (done)
 +-6-> 1
 |     +-6 x  (6 > 1)
 +-7-> 0      record [7]
 result=[[2,2,3],[7]]   path=[]  stack empty
```

Across frames, `remaining = target - sum(path)` held at every node, and every edge label along a path was non-decreasing. Each `x` was the first candidate in sorted order that exceeded the node's budget, and nothing to its right was examined.

## Why it is correct

*Each recorded path is an answer.* Records happen only when remaining is 0, and remaining equals target minus the path's sum (choose subtracts, un-choose is automatic because remaining is passed by value).

*Every answer is recorded.* Take any answer and sort it: `c1 <= c2 <= ... <= ck`. At the root, start is 0, so c1's index is tried; c1 <= target since all candidates are positive, so no break happens before it. At each later step the start is c(j-1)'s index, which is <= cj's index, and cj <= remaining (the rest of the answer is still to come and is positive). So every edge of the sorted path is taken.

*Each answer appears once.* Paths are non-decreasing in index and candidates are distinct, so one multiset has one non-decreasing order, hence one path.

*Pruning is safe.* A break at `candidates[i] > remaining` skips only children whose first pick overshoots; positivity means no extension can come back down.

## Cost

- **Time: O(n^(T/m))** in the worst case, where T is the target and m the smallest candidate: branching at most n, depth at most T/m. Recording adds O(T/m) per answer. In practice the break makes the explored tree far smaller.
- **Space: O(T/m)** for the path and recursion depth, beyond the output.

## Variations you will meet

- **Combination Sum II (each candidate once, input may repeat).** Recurse with `i + 1` and add the duplicate-sibling skip from Subsets II. That is the next problem.
- **Combination Sum III (LeetCode 216): k numbers from 1..9, each once, summing to n.** Same tree with `i + 1`, a fixed length k, and a cut when the path is already k long.
- **Combination Sum IV (LeetCode 377): count ordered sequences.** The question is "how many", and order matters; the states `remaining` repeat across paths, so this is DP over remaining, not backtracking.
- **Coin Change (LeetCode 322/518).** Same candidate/target shape, but asks for a minimum or a count, again DP. If the interviewer asks for "all ways", you are back here.

## What to carry forward

Carry the remaining budget down the tree, sort so the first overflow lets you `break`, and pass `i` to allow reuse while forbidding reorderings. The next problem forbids reuse and allows repeated values in the input, so it needs this budget cut and Subsets II's duplicate-sibling skip at the same time.
