# K-th Smallest in Lexicographical Order

*LeetCode 440 · Hard · Pattern: Denary trie traversal with subtree skipping · Reading time ~9 min*

## What the problem is really asking

Write the integers `1..n` as strings and sort them like words in a dictionary. Return the `k`-th one. Both `n` and `k` go up to `10^9`.

The answer is one integer. Dictionary order is strange for numbers: `10` comes before `2`, and `100` comes before `11`. What makes the problem hard is the size: a billion strings cannot be listed, let alone sorted, so the answer has to be *located*, not found by scanning.

```text
 n = 13, dictionary order
 pos: 1  2  3  4  5  6 7 8 9 10 11 12 13
 val: 1 10 11 12 13  2 3 4 5  6  7  8  9
         ^ k = 2 -> 10
```

## Do it by hand first

Take `n = 25`, `k = 15`. Write the dictionary order and look at its shape.

```text
 1 10 11 12 13 14 15 16 17 18 19   <- "1" and everything
                                      starting with "1": 11
 2 20 21 22 23 24 25               <- "2..." : 7 numbers
 3                                 <- "3" alone (30 > 25)
 4 5 6 7 8 9
 count: 11 + 7 + 1 + 6 = 25
```

The numbers starting with `1` form one contiguous run; so do those starting with `2`. This is the same block structure as Permutation Sequence: dictionary order compares first characters first, so everything with prefix `1` comes before everything with prefix `2`.

So for `k = 15`: the `1...` block has 11 numbers. `15 > 11`, so skip it entirely; 4 more to go. The `2...` block has 7 numbers; the target is inside. Step into it: its first element is `2` itself (that uses 1 of the 4, leaving 3). Next come `20`, `21`, `22`: count off 3 more. Answer: `22`.

What did your hand keep track of? A current prefix, the number of positions still to move, and — the crucial new piece — *how many numbers start with this prefix*. In Permutation Sequence that was `(m-1)!`. Here it depends on `n` and must be counted.

## The first honest attempt

Build the strings `"1".."n"`, sort them, index `k - 1`. Or, smarter, generate dictionary order directly with a DFS (`1, 10, 100, ...`) and stop at the `k`-th visit, which is the approach of LeetCode 386 (Lexicographical Numbers).

The sort costs `O(n log n)` time and `O(n)` memory; the DFS costs `O(k)` time. With `k` up to `10^9`, both are hopeless within a second.

Where is the repeated work? The DFS walks into every subtree it passes, one node at a time, even when the target is nowhere inside it.

```text
 DFS walk for n = 25, k = 15
   1 -> 10 -> 11 -> ... -> 19      (11 visits)
   2 -> 20 -> 21 -> 22  stop
 the first 11 visits only established "not under 1";
 one number, "subtree(1) = 11", says the same thing
```

## The turning point

**Claim: dictionary order on `1..n` is the pre-order traversal of the 10-ary tree in which node `v` has children `10v, ..., 10v+9` (only those `<= n`); so you can find the `k`-th node by comparing `k` with subtree sizes, skipping whole subtrees or stepping into them.**

Why pre-order? Pre-order visits a node, then all its descendants, then the next sibling. The descendants of `v` are exactly the numbers whose decimal string starts with `str(v)`. Dictionary order lists `v`, then everything with prefix `v` (which is longer, hence later), before moving to prefix `v+1`. Same thing.

```text
 the denary tree for n = 25 (numbers > 25 pruned)
                     (root)
      /       /       |    \   ...   \
     1        2       3     4  ...    9
   / ... \  / ... \
  10 ... 19 20 ... 25
 pre-order: 1 10..19 2 20..25 3 4 5 6 7 8 9
```

So the walk becomes: stand at `cur` with `k` = number of moves still to make in pre-order (start at `cur = 1`, `k = k - 1`, since `1` is the first element). Count `steps = size of cur's subtree`.

- If `steps <= k`, the target is past this subtree. Skip it in one move: `k -= steps`, `cur += 1` (next sibling).
- Otherwise the target is inside. Moving to the first child is one pre-order step: `k -= 1`, `cur *= 10`.

Stop when `k == 0`; `cur` is the answer.

Now the new piece: how big is the subtree of `cur`, clipped to `n`? Level by level. At depth 0 it holds `[cur, cur+1)`. At depth 1, `[10cur, 10cur+10)`. At depth 2, `[100cur, 100cur+100)`. Each level is a contiguous range of integers, so its count within `1..n` is `min(n + 1, b) - a` for the half-open range `[a, b)`, as long as `a <= n`.

```text
 subtree(1) for n = 130
 level  [a, b)        clip at n+1 = 131    count
   0    [1, 2)        [1, 2)                  1
   1    [10, 20)      [10, 20)               10
   2    [100, 200)    [100, 131)             31
   3    [1000, 2000)  a > n: stop
                                    total =  42
```

At most ten levels, each `O(1)`, so `O(log n)` per subtree count. And how many skip-or-step decisions are made? Each decision either moves to a sibling (at most 10 per level) or goes one level deeper (at most `log10 n` times). So `O(log n)` decisions, `O(log^2 n)` total.

One thing that looks like a bug and is not: when `cur` ends in `9` and you skip, `cur += 1` produces e.g. `19 + 1 = 20`, which is not a sibling of `19` but a node at the same depth in the parent's next sibling's subtree. Pre-order would next visit `2` there, not `20`. Why is this fine? Because we only stepped into `1`'s subtree if the target was inside it; and subtree sizes inside it sum to all of it, so `k` runs out before we would have to leave it. The jump `19 -> 20` happens only in the clipped tail where it is never needed.

## Watch it work

Example: `n = 25`, `k = 15`. Expected answer: `22` (position 15 in the hand-written order).

Frame 1 — `cur = 1`, `k = 14` (we stand on the first element). `subtree(1) = 1 + 10 = 11`. `11 <= 14`: skip.

```text
 levels of 1: [1,2)->1   [10,20)->10       steps = 11
   (1) 10 11 ... 19 | 2 20..25 | 3 ...
   \___ skip 11 __/  ^ cur
 k = 14 - 11 = 3,  cur = 2
```

Frame 2 — `cur = 2`, `k = 3`. `subtree(2) = 1 + 6 = 7` (`[20, 26)` clipped). `7 > 3`: step into the first child.

```text
 levels of 2: [2,3)->1   [20,26)->6        steps = 7
   2 (20) 21 22 23 24 25
   ^ visited, move down
 k = 3 - 1 = 2,  cur = 20
```

Frame 3 — `cur = 20`, `k = 2`. `subtree(20) = 1` (`[200, 210)` is past `n`). `1 <= 2`: skip.

```text
 levels of 20: [20,21)->1  [200,..) > 25   steps = 1
   20 | (21) 22 ...
 k = 2 - 1 = 1,  cur = 21
```

Frame 4 — `cur = 21`, `k = 1`. `subtree(21) = 1`. `1 <= 1`: skip.

```text
 levels of 21: [21,22)->1                  steps = 1
   21 | (22) 23 ...
 k = 1 - 1 = 0,  cur = 22
```

Frame 5 — `k == 0`: stop. Answer `22`, matching the hand count.

```text
 order: 1 10 11 12 13 14 15 16 17 18 19 2 20 21 22
 pos:   1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
                                                 ^ 22
```

What stayed invariant: `cur` is always the node at pre-order position `k_original - k`, and `k` is how many further pre-order steps reach the target. A skip advanced past an entire subtree, a descent advanced exactly one node, and both reduced `k` by exactly the number of positions passed.

## Why it is correct

Invariant: *the target is the node reached by making `k` more pre-order moves from `cur`, and the target lies in the subtree of `cur` or in the subtrees of `cur`'s later siblings (within the current parent).*

Initially `cur = 1`, the first pre-order node, and `k = k - 1` moves remain.

If `steps(cur) <= k`: the `steps` nodes of `cur`'s subtree occupy the next `steps` pre-order positions starting at `cur`, so the target is not among them; the node right after them in pre-order is `cur`'s next sibling. Moving there consumes `steps` positions. If `steps(cur) > k`: the target is strictly inside `cur`'s subtree (and not `cur` itself, since `k > 0`); the next pre-order node is `cur`'s first child `10 * cur`, one position later. Since `steps > k >= 1` implies a child exists, `10 * cur <= n`.

Each move preserves the invariant, `k` strictly decreases, and when `k = 0` the target is `cur`. The subtree count is correct because the descendants of `cur` at depth `d` are exactly the integers in `[cur * 10^d, (cur + 1) * 10^d)`, and clipping to `[1, n]` gives `min(n + 1, b) - a` when `a <= n`.

## Cost

- **Time:** `O(log^2 n)` — at most `log10 n` descents plus at most 9 sibling skips per level, so `O(log n)` decisions, each paying an `O(log n)` subtree count.
- **Space:** `O(1)` — a handful of integers.

Compare: `O(n log n)` for sorting, `O(k)` for the DFS. At `n = k = 10^9`, the skip walk does a few hundred arithmetic operations.

## Variations you will meet

- **Lexicographical Numbers (LeetCode 386).** Output *all* of `1..n` in dictionary order in `O(n)` time and `O(1)` extra space. That is the pre-order walk itself, done iteratively: try `cur * 10`; else `cur + 1` while backing off trailing nines and values past `n`. Here you must visit every node, so no skipping.
- **Count numbers `<= n` with a given prefix.** That is exactly `subtree(prefix)`; it shows up inside autocomplete-style questions.
- **K-th string in lexicographic order over a trie of words.** Store subtree counts in each trie node, then the same skip-or-enter walk finds the `k`-th word in `O(depth * alphabet)`.
- **Permutation Sequence, revisited.** There every block had size `(m-1)!` and one division sufficed. Here blocks differ (`subtree(1) = 11` vs `subtree(3) = 1` for `n = 25`), so we subtract block sizes one sibling at a time. Unequal blocks force subtraction; equal blocks allow division.

## What to carry forward

Dictionary order on numbers is pre-order on the 10-ary tree; find the `k`-th by comparing `k` with subtree sizes, each counted level by level as clipped ranges.

The next problem, Number of Digit One, keeps the habit of counting whole ranges at once, but instead of counting numbers under a prefix it counts how often one digit position shows a `1` across all of `0..n`.
