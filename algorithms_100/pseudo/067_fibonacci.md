---
rank: 67
slug: fibonacci
---

The Fibonacci numbers start with `F(0) = 0` and `F(1) = 1`, and every later term is the sum of the two before it: `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55`. Given `n`, compute `F(n)`; for example `F(5) = 5` and `F(10) = 55`.

The definition is already an algorithm, and a famously slow one. Each call makes two more calls, so the calls form a binary tree with `2F(n + 1) - 1` nodes, a count that grows like `1.618^n`, and the same subproblems sit in it over and over: computing `F(5)` solves `F(3)` twice and `F(2)` three times. Memoization stores each answer the first time it is computed, and every later request becomes a lookup. The tree collapses to its left edge, with each `F(k)` computed once, at the cost of an `O(n)` map and a call stack `n` frames deep.

The loop keeps only what the recurrence still needs. Every new term reads just the two before it, so a window of two numbers slides along the sequence: `(prev, curr) = (F(i), F(i + 1))` becomes `(F(i + 1), F(i + 2))` in each step, and after `n` steps `prev` is `F(n)`. Fast doubling stops walking and starts jumping. From the pair `(F(k), F(k + 1))` the identities `F(2k) = F(k)(2F(k + 1) - F(k))` and `F(2k + 1) = F(k)² + F(k + 1)²` land directly on position `2k` or `2k + 1`, so the recursion halves `n` on the way down and rebuilds one bit of `n` per level on the way back up. Both identities fall out of squaring a power of the matrix `[[1, 1], [1, 0]]`, whose powers hold consecutive Fibonacci numbers, which makes this the same halving trick as fast exponentiation (#93).

```text
plain recursion for F(5): 15 calls, F(3) twice, F(2) three times
                         F(5)
               ┌──────────┴───────────┐
              F(4)                   F(3)
        ┌──────┴──────┐           ┌───┴────┐
       F(3)          F(2)        F(2)     F(1)
    ┌───┴────┐     ┌──┴──┐     ┌──┴──┐
   F(2)     F(1)  F(1)  F(0)  F(1)  F(0)
 ┌──┴──┐
F(1)  F(0)

memo      9 calls: 5 4 3 2 1 0 1 2 3 (the second 2 and 3 are lookups)
loop      (prev, curr) = (0,1) (1,1) (1,2) (2,3) (3,5) (5,8) → F(5) = 5
doubling  n = 10 → 5 → 2 → 1 → 0, then (F(k), F(k + 1)) climbs back:
          (0,1) → (1,1) → (1,2) → (5,8) → (55,89) → F(10) = 55
```

```pseudo
FUNCTION FibNaive(n)
    IF n < 2
        RETURN n
    RETURN FibNaive(n - 1) + FibNaive(n - 2)  // two calls per call

FUNCTION FibMemo(n, memo)
    IF n < 2
        RETURN n
    IF n IN memo
        RETURN memo[n]                  // solved before: skip the whole subtree
    memo[n] ← FibMemo(n - 1, memo) + FibMemo(n - 2, memo)
    RETURN memo[n]

FUNCTION FibIter(n)
    prev ← 0
    curr ← 1
    FOR i FROM 0 TO n - 1               // prev = F(i), curr = F(i + 1)
        nxt ← prev + curr
        prev ← curr
        curr ← nxt
    RETURN prev

FUNCTION FibPair(n)                     // returns (F(n), F(n + 1))
    IF n = 0
        RETURN (0, 1)
    (a, b) ← FibPair(floor(n / 2))      // a = F(k), b = F(k + 1)
    even ← a * (2 * b - a)              // F(2k)
    odd ← a * a + b * b                 // F(2k + 1)
    IF n mod 2 = 0
        RETURN (even, odd)
    RETURN (odd, even + odd)            // n = 2k + 1: one step further

FUNCTION FibFast(n)
    pair ← FibPair(n)
    RETURN pair[0]
```

The plain recursion costs exponential time, memoization `O(n)` time and space, the loop `O(n)` time and `O(1)` space, and fast doubling `O(log n)` arithmetic steps, one per bit of `n`; `F(n)` has about `0.69n` bits, so for huge `n` the big-integer multiplications set the real cost. Reach for the two-variable loop whenever each state depends only on the previous two: Climbing Stairs counts the ways to reach step `n` as the ways to reach `n - 1` plus the ways to reach `n - 2`, which is `F(n + 1)`, and Tribonacci slides a window of three. The classic mistake is presenting the plain recursion as the answer in an interview, where `F(50)` already takes about 40 billion calls; the second is memoizing in Python and hitting the default recursion limit near `n = 1000`, which the loop never touches.

*Practice:* LC 509 Fibonacci Number · LC 70 Climbing Stairs · LC 1137 N-th Tribonacci Number
