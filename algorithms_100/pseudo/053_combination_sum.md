---
rank: 53
slug: combination_sum
---

Given an array of distinct positive integers `candidates` and a `target`, return every combination of candidates that sums to the target. A candidate may be used any number of times, and order does not matter, so `[2, 2, 3]` and `[3, 2, 2]` are the same combination. For `[2, 3, 6, 7]` and target `7` the answer is `[[2, 2, 3], [7]]`.

This is the subsets tree of #22 with two changes. First, a chosen candidate may be chosen again, so the recursion passes `start = i` instead of `i + 1`: the next pick may repeat the current candidate or move right, but it never moves left. Every path is therefore non-decreasing, one canonical order per combination, so each combination is built exactly once. Second, each call also carries what is still missing, `remaining`, and a node records its path only when `remaining` hits 0 exactly.

Sorting first turns overshooting into a wall. Scanning left to right, the first candidate larger than `remaining` proves that every later one is larger too, so the loop breaks instead of continuing, and a whole fan of hopeless branches is never entered. In the tree below each node shows its path and what is still missing; the whole search takes ten calls.

```text
[]  7 left                    candidates sorted: [2, 3, 6, 7]
├── [2]  5 left
│   ├── [2,2]  3 left
│   │   ├── [2,2,2]  1 left   then 2 > 1: break
│   │   ├── [2,2,3]  0 left   ✓ record
│   │   └── 6 > 3: break
│   ├── [2,3]  2 left         loop starts at 3 (start = 1); 3 > 2: break
│   └── 6 > 5: break
├── [3]  4 left
│   ├── [3,3]  1 left         then 3 > 1: break
│   └── 6 > 4: break
├── [6]  1 left               then 6 > 1: break
└── [7]  0 left               ✓ record
```

```pseudo
FUNCTION Backtrack(candidates, start, remaining, path, result)
    IF remaining = 0
        result.append(path.copy())          // exact hit: one combination
        RETURN
    FOR i FROM start TO len(candidates) - 1
        IF candidates[i] > remaining
            BREAK                           // sorted: the rest are bigger
        path.append(candidates[i])          // choose
        // pass i, not i + 1: the same candidate may be chosen again
        Backtrack(candidates, i, remaining - candidates[i], path, result)
        path.pop()                          // un-choose

FUNCTION CombinationSum(candidates, target)
    candidates ← sorted(candidates)         // makes the BREAK valid
    result ← empty list
    Backtrack(candidates, 0, target, empty list, result)
    RETURN result
```

The tree is at most `t / m` levels deep, for target t and smallest candidate m, and branches at most n ways, so it has `O(n^(t/m + 1))` nodes: exponential, which the small constraints keep in check; the extra space is the `O(t / m)` depth. Signals: all combinations that reach a sum, an unlimited supply of each item, and a request to list them rather than count them. Two neighbors change a line or two. LC 40 uses each candidate at most once and may contain duplicates, so it recurses with `i + 1` and skips `candidates[i]` when `i > start` and `candidates[i] = candidates[i - 1]`, the rule from Subsets II; LC 216 picks exactly k distinct digits from 1 to 9. LC 377 only looks similar: it counts ordered sequences, which is a counting DP rather than a listing. Recursing with `i + 1` here loses `[2, 2, 3]`. The classic mistake goes the other way, recursing with `start = 0`: the path may then move left, and `[2, 2, 3]`, `[2, 3, 2]` and `[3, 2, 2]` come back as three different answers.

*Practice:* LC 39 Combination Sum · LC 40 Combination Sum II · LC 216 Combination Sum III · LC 377 Combination Sum IV
