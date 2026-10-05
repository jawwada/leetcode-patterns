# Permutation Sequence

*LeetCode 60 · Hard · Pattern: Factorial number system (direct ranking into blocks) · Reading time ~8 min*

## The problem

The permutations of the digits 1..n, listed in lexicographic order, are numbered 1..n!. Return the k-th one as a
string (1 <= n <= 9).

```text
Example: n=3, k=3 -> "213" (order: 123, 132, 213, 231, 312,
  321); n=4, k=9 -> "2314".
```

## What the problem is really asking

Take the digits `1..n` and list all `n!` of their orderings in dictionary order. Number them `1, 2, ..., n!`. Given `n` (at most 9) and `k`, return the `k`-th ordering as a string.

The answer is a single permutation. What makes it hard is not the size of the answer, which has `n` characters, but the size of the list it lives in: `9! = 362880`. Listing is affordable for `n = 9`, which is why this problem is often "solved" by brute force. But the real question is whether you can *jump* to position `k` without walking there, and that skill is what the next problems in this chapter demand at scales where walking is impossible.

```text
 n = 3, all 3! = 6 permutations in order
   k:  1     2     3     4     5     6
      123   132   213   231   312   321
                   ^
              k = 3 -> "213"
```

## Do it by hand first

Take `n = 4`, `k = 9`. Write the list, but notice its shape as you write.

```text
 rank  perm   rank  perm   rank  perm   rank  perm
 (k-1)        (k-1)        (k-1)        (k-1)
  0    1234    6    2134   12    3124   18    4123
  1    1243    7    2143   13    3142   19    4132
  2    1324    8    2314   14    3214   20    4213
  3    1342    9    2341   15    3241   21    4231
  4    1423   10    2413   16    3412   22    4312
  5    1432   11    2431   17    3421   23    4321
 \__ block "1" __/ \__ block "2" __/ ...  each 3! = 6
```

The list falls into four columns, one per first digit, each of exactly `3! = 6` rows. That is no accident: once the first digit is fixed, the rest is "all permutations of the three remaining digits", and there are `3!` of those.

So to find `k = 9`, which is 0-indexed rank `8`: rank `8` is in the second block (ranks 6..11), so the first digit is `2`. Inside that block, it is at offset `8 - 6 = 2`. Now the block itself splits by second digit, from the remaining `{1, 3, 4}`, into sub-blocks of `2! = 2`: `21..` (offsets 0,1), `23..` (2,3), `24..` (4,5). Offset 2 is in `23..`. Inside, offset 0, remaining `{1, 4}`, sub-blocks of `1! = 1`: `231.` then `234.`. Offset 0 picks `1`. The last digit is forced: `4`. Answer `2314`.

What did your hand keep track of? Two things: a shrinking pool of unused digits, and a shrinking offset that says where you are inside the current block. That pair is the whole algorithm.

## The first honest attempt

Generate permutations in lexicographic order and stop at the `k`-th. Either iterate `itertools.permutations(range(1, n+1))`, which yields them in lexicographic order for sorted input, or call a next-permutation routine `k - 1` times.

Cost: up to `n!` permutations, each costing `O(n)` to produce or compare, so `O(n! * n)` time in the worst case, `O(n)` space. For `n = 9` that is about 3 million character operations, which passes. For `n = 20` it would be `2.4 * 10^18 * 20`, which does not.

Where is the repeated work? Every permutation before the answer is built in full, character by character, even though whole blocks of them share a prefix we already know is wrong.

```text
 walking to k = 9 (rank 8) for n = 4
   1234 1243 1324 1342 1423 1432   <- all six start with 1;
   2134 2143                        we built 6 strings to
   2314  <- stop                    learn "not this block"
 the walk spends 3! steps to skip a block it could skip
 with one division
```

## The turning point

**Claim: in lexicographic order, the permutations starting with the `j`-th smallest unused digit form one contiguous block of exactly `(m-1)!` permutations, where `m` is the number of unused digits; so the block containing rank `r` is `r // (m-1)!`, and the rank inside it is `r % (m-1)!`.**

Justify it. Lexicographic order compares first characters first. So every permutation beginning with the smallest digit precedes every permutation beginning with the second smallest, and so on: the blocks are contiguous and ordered by the leading digit. Within a block, the leading digit is identical, so the order is decided by the remaining `m - 1` digits, which run through all their `(m-1)!` permutations in lexicographic order. All blocks therefore have the same size, `(m-1)!`. Equal-sized consecutive blocks are exactly the situation in which integer division tells you which block a position is in, and the remainder tells you where inside it.

The sub-problem inside a block is the same problem with one fewer digit. So you repeat: `m` goes from `n` down to `1`, the divisor goes `(n-1)!, (n-2)!, ..., 0!`, and each quotient is an index into the current pool of unused digits.

This repeated division has a name. It writes `r` in the **factorial number system**:

```text
 r = d(n-1)*(n-1)! + ... + d2*2! + d1*1! + d0*0!
     with 0 <= d_i <= i

 r = 8, n = 4:
   8 = 1*3! + 1*2! + 0*1! + 0*0!
   digits (d3 d2 d1 d0) = (1 1 0 0)
   pool  1 2 3 4 -> idx 1 -> 2   pool 1 3 4
   pool  1 3 4   -> idx 1 -> 3   pool 1 4
   pool  1 4     -> idx 0 -> 1   pool 4
   pool  4       -> idx 0 -> 4
```

Each factorial digit `d_i` ranges over `0..i`, which is exactly the number of choices left when `i + 1` digits remain. It is the same mixed-radix idea as decimal, just with a different weight per position. The digits are *indices into a shrinking list*, not digit values. That distinction is the most common bug: if you index the original list `1..n` instead of the pool, you can pick the same digit twice.

```text
 one level of the descent as a picture
   pool = [a, b, c, d], block size w = 3! = 6
   |---- a ----|---- b ----|---- c ----|---- d ----|
   0           6           12          18          24
                    ^ r=8
   idx = 8 // 6 = 1 -> take b;  r = 8 % 6 = 2
```

Two small details matter. First, `k` is 1-indexed; set `r = k - 1` before dividing, or the block boundaries are off by one (rank 6 is the first permutation of block 1, but `k = 6` is the last of block 0). Second, precompute factorials `0!..(n-1)!` once.

## Watch it work

Example: `n = 4`, `k = 9`. State: `r` (rank left), the divisor `i!`, the pool, and the output.

Frame 1 — setup. `r = k - 1 = 8`. Factorials `[1, 1, 2, 6]` for `0!..3!`.

```text
 r = 8          pool: [1, 2, 3, 4]       out: ""
 i = 3, i! = 6  blocks:  1:[0,6) 2:[6,12) 3:[12,18) 4:[18,24)
                                    ^ r = 8
```

Frame 2 — `divmod(8, 6) = (1, 2)`. Take `pool[1] = 2`; rank inside block is `2`.

```text
 idx = 1 -> take "2"
 r = 2          pool: [1, 3, 4]          out: "2"
 i = 2, i! = 2  blocks: 21:[0,2) 23:[2,4) 24:[4,6)
                                   ^ r = 2
```

Frame 3 — `divmod(2, 2) = (1, 0)`. Take `pool[1] = 3`.

```text
 idx = 1 -> take "3"
 r = 0          pool: [1, 4]             out: "23"
 i = 1, i! = 1  blocks: 231:[0,1) 234:[1,2)
                           ^ r = 0
```

Frame 4 — `divmod(0, 1) = (0, 0)`. Take `pool[0] = 1`.

```text
 idx = 0 -> take "1"
 r = 0          pool: [4]                out: "231"
 i = 0, i! = 1  blocks: 2314:[0,1)
```

Frame 5 — `divmod(0, 1) = (0, 0)`. Take `pool[0] = 4`. Pool empty; answer `"2314"`.

```text
 idx = 0 -> take "4"
 r = 0          pool: []                 out: "2314"
 check: rank 8 in the hand-written table is 2314
```

What stayed invariant: at every frame, the answer is the `r`-th (0-indexed) lexicographic permutation of the current pool, prefixed by `out`. Each division chose the block holding that permutation and reduced `r` to its position inside the block. The pool always stayed sorted, because popping from a sorted list keeps it sorted, which is what makes "index `idx` in the pool" equal "the `idx`-th smallest unused digit".

## Why it is correct

The invariant: *before each step, the target permutation equals `out` followed by the `r`-th permutation (0-indexed, lexicographic) of the sorted `pool`, and `0 <= r < len(pool)!`.*

It holds at the start: `out` is empty, the pool is `1..n`, and `r = k - 1` lies in `[0, n!)`.

Step: let `m = len(pool)`, `w = (m-1)!`. By the block claim, the `r`-th permutation of the pool starts with `pool[r // w]`, and its remainder is the `(r % w)`-th permutation of the pool with that digit removed. Since `r < m!` we have `r // w < m`, so the index is valid. Appending the digit to `out`, removing it from the pool and replacing `r` by `r % w < (m-1)!` restores the invariant with `m` one smaller.

When the pool is empty, the only permutation of an empty pool is the empty one, so the target is exactly `out`.

## Cost

- **Time:** `O(n^2)` — `n` divisions, each followed by a `list.pop(idx)` that shifts up to `n` elements. For `n <= 9` this is a few dozen operations.
- **Space:** `O(n)` — the pool, the factorial table and the output.

With a Fenwick tree or order-statistic tree over the pool, "find and delete the `idx`-th unused element" becomes `O(log n)`, giving `O(n log n)`. That matters for the inverse and general-`n` variants below, not here.

## Variations you will meet

- **The inverse: rank of a given permutation.** Given `"2314"`, return `9`. Walk left to right: for each character, count the unused digits smaller than it (that is the factorial digit `d_i`), add `d_i * i!`, mark it used. Finish with `+1`. The same blocks, read the other way.
- **Next Permutation (LeetCode 31).** Moves one step along the same order without ranks: find the rightmost ascent, swap with the next larger digit to its right, reverse the suffix. Use it when you need neighbours, not a jump.
- **Permutations with repeated elements.** Blocks are no longer equal: the block for leading digit `x` has `(m-1)! / prod(count!)` members after removing one `x`. You still skip blocks by subtraction, but now you compare `r` against each block size in turn instead of one division. This "unequal blocks" version is exactly the shape of the next problem.
- **k-th combination / k-th subset in lexicographic order.** Replace `(m-1)!` with binomial coefficients `C(remaining, needed)`; the skip-or-enter decision is identical.

## What to carry forward

When objects are listed in an order that groups them into blocks of known size, find the `k`-th by dividing (or subtracting) block sizes level by level, never by walking.

The next problem, K-th Smallest in Lexicographical Order, keeps "skip a whole block or step into it", but the blocks are subtrees of a ragged 10-ary tree, so their sizes must be computed rather than read off a factorial.
