# Backtracking

Backtracking is depth-first search over a tree of partial answers. One list, `path`, is the current partial answer. At every node you loop over the candidates that are still allowed, and for each one you do three things: **choose** it (append), **explore** (recurse), **unchoose** it (pop) so the list is exactly as it was for the next candidate. The answers are the nodes (subsets) or the leaves (combinations, permutations, bracket strings) of that tree. Every family of problems is the same template with a different rule for "which candidates are allowed here".

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| choose: `path.append(x)` | O(1) | plus marking (`used[i] = True`) when order matters |
| explore: recursive call | one node of the tree | depth is at most n |
| unchoose: `path.pop()` | O(1) | restores the exact state; forgetting it corrupts every sibling |
| record: `res.append(path[:])` | O(k) | copy, never the list itself |
| whole search | O(size of the tree * cost per node) | 2^n subsets, C(n, k) combinations, n! permutations |
| prune | saves a whole subtree | skip duplicates, stop when not enough elements remain, stop when the sum overshoots |

## Which rule for the candidates?

| Family | Allowed candidates at this node | Where answers live |
|---|---|---|
| subsets | `i` from `start` to the end (start-index template) | every node |
| combinations | same, plus prune when fewer numbers remain than slots | leaves with `len(path) == k` |
| combination sum (reuse) | recurse with `i`, not `i + 1`; break when `cands[i] > remaining` | leaves with `remaining == 0` |
| permutations | every `i` with `used[i]` False | leaves with `len(path) == n` |
| with duplicates | sort, then skip `a[i] == a[i-1]` when it is not the first of its run on this level (`i > start`) or its twin is unused (`not used[i-1]`) | as above |
| parentheses | open while `opened < n`, close while `closed < opened` | leaves of length 2n |

## Drawn example: subsets of [1, 2, 3]

Each node is a `path`; children are made by choosing an element after the last chosen index.

```
                        []
            ┌───────────┼────────────┐
         choose 1    choose 2     choose 3
            │           │            │
           [1]         [2]          [3]
        ┌───┴───┐       │
    choose 2 choose 3 choose 3
        │       │       │
      [1,2]   [1,3]   [2,3]
        │
    choose 3
        │
     [1,2,3]
```

The trace of the program is the depth-first walk of this tree, indented by depth:

```
record []
  choose 1 -> path [1]
  record [1]
    choose 2 -> path [1, 2]
    record [1, 2]
      choose 3 -> path [1, 2, 3]
      record [1, 2, 3]
      unchoose 3 -> path [1, 2]
    unchoose 2 -> path [1]
    choose 3 -> path [1, 3]
    record [1, 3]
    unchoose 3 -> path [1]
  unchoose 1 -> path []
  choose 2 -> path [2]
  ...
```

Eight records, one per node: that is the power set.

## The invariant to say out loud

"Choose, explore, unchoose: when a call returns, `path` (and `used`) look exactly as they did before the call."

And for the start index: "everything I may still choose comes after the last thing I chose, so each subset is built in exactly one order and never twice."

## Exercises

| File | Drills |
|---|---|
| `01_subsets.py` | the start-index template; record at every node; copy the path |
| `02_subsets_with_duplicates.py` | sort, then skip `a[i] == a[i-1]` when `i > start` |
| `03_combinations_n_choose_k.py` | leaves of size k; prune when `n - i + 1 < k - len(path)` |
| `04_combination_sum.py` | reuse by recursing with `i`; break when `cands[i] > remaining` |
| `05_permutations.py` | `used[]` flags instead of a start index |
| `06_permutations_with_duplicates.py` | sort, then skip `a[i] == a[i-1]` while `used[i-1]` is False |
| `07_generate_parentheses.py` | two counters as the guard: `opened < n`, `closed < opened` |
