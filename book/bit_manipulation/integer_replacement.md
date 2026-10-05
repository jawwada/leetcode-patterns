# Integer Replacement

*LeetCode 397 · Medium · Pattern: Greedy on the low bits · Reading time ~8 min*

## The problem

Given a positive integer n, one step replaces an even n with n / 2 and an odd n with n + 1 or n - 1. Return the
minimum number of steps to reach 1.

```text
Example: 8 -> 3 (8, 4, 2, 1); 7 -> 4 (7, 8, 4, 2, 1).
```

## What the problem is really asking

Start from a positive integer `n` and reach 1 with as few moves as possible. If `n` is even you must halve it. If `n` is odd you choose: add 1 or subtract 1. Return the minimum number of moves.

The answer is a count. The decision points are the odd numbers, where the path forks. A wrong choice is not obviously wrong right away; it shows up several moves later. That is what makes it feel like a search problem.

```text
n = 23

 23 --+1--> 24 -> 12 -> 6 -> 3 --(-1)--> 2 -> 1
 odd        even  even  even odd          even
 6 moves
```

## Do it by hand first

Try `n = 7` both ways on paper.

```text
7 -+1-> 8 -> 4 -> 2 -> 1                4 moves
7 --1-> 6 -> 3 -+1-> 4 -> 2 -> 1        5 moves
7 --1-> 6 -> 3 --1-> 2 -> 1             4 moves
```

Now write the numbers in binary and the pattern jumps out:

```text
 7 = 111   +1 ->  1000   three 1s collapse into one
 7 = 111   -1 ->  110    one 1 removed, two remain
```

Halving just drops the last column. So the real cost is how many 1s you have to get rid of, and how many columns you have to shift away. What your hand kept track of was the **last bits** of the number. They decide whether a +1 will carry through a run of 1s or just turn a lone 1 into a 0.

## The first honest attempt

Recursion that tries both moves at every odd number:

`f(1) = 0`, `f(even) = 1 + f(n/2)`, `f(odd) = 1 + min(f(n+1), f(n-1))`.

It is correct. The cost is that every odd value doubles the work, and the two branches keep landing on the same numbers.

```text
                 f(23)
               /       \
           f(24)        f(22)
             |            |
           f(12)        f(11)
             |         /     \
           f(6)     f(12)    f(10)
             |        |        |
           f(3)     f(6)     f(5)
           /  \       |      /  \
        f(4) f(2)   f(3)  f(6)  f(4)
                     ...   ...
 f(12), f(6), f(3) are each solved again
```

Memoising fixes the repetition. But the branches themselves are the bigger issue: the tree has about `n` leaves in the worst case. With `n` up to `2^31 - 1`, even a memoised search touches many states. What we want is to know, at each odd number, which branch is right without exploring both.

## The turning point

**Claim: at an odd `n > 3`, look at the low two bits. If they are `01`, subtract 1. If they are `11`, add 1. At `n = 3`, subtract.**

Here is why the low two bits are enough. An odd number ends in `01` or `11`.

```text
case ...01                    case ...11
 n   = x x x 0 1              n   = x x 0 1 1 1
 n-1 = x x x 0 0              n+1 = x x 1 0 0 0
   two free halvings next       carry wiped the run of 1s
 n+1 = x x x 1 0              n-1 = x x 0 1 1 0
   leaves a new 1 at col 1      only one 1 removed
```

- **Ending `01`**: subtracting 1 leaves `00` at the bottom, so two halvings follow for free. Adding 1 gives `10`, which halves once into another odd number. You just paid a move and still have a 1 to deal with.
- **Ending `11`**: adding 1 sends a carry left through the whole trailing run of 1s, turning `0111` into `1000`. One move removes several 1s. Subtracting removes only the last 1 and leaves the run, minus one, behind.

The single exception is 3 = `11`. Adding gives 3 → 4 → 2 → 1 (3 moves), but subtracting gives 3 → 2 → 1 (2 moves). The carry pays off only if something remains after it. At 3 the "run" is the whole number, and the extra column the carry creates is wasted.

The test `n & 3` reads the two lowest bits at once: `1` means `01`, `3` means `11`. So the whole algorithm is a loop with no branching search. Even numbers shift right. Odd numbers subtract when `n == 3` or `n & 3 == 1`, and add otherwise. Count the moves until `n` is 1.

## Watch it work

`n = 23 = 10111`.

```text
Frame 1   n = 23 = 1 0 1 1 1   steps = 0
  odd, low bits 11, n != 3  -> add 1
  n = 24 = 1 1 0 0 0
```
The carry ran through three 1s and left a single 1 at column 3.

```text
Frame 2   n = 24 = 1 1 0 0 0   steps = 1
  even -> halve
  n = 12 = 1 1 0 0
```
A shift drops a trailing zero.

```text
Frame 3   n = 12 = 1 1 0 0     steps = 2
  even -> halve
  n = 6 = 1 1 0
```
Another free shift; the carry from Frame 1 created three trailing zeros.

```text
Frame 4   n = 6 = 1 1 0        steps = 3
  even -> halve
  n = 3 = 1 1
```
The number is now `11`, the special case.

```text
Frame 5   n = 3 = 1 1          steps = 4
  n == 3 -> subtract 1
  n = 2 = 1 0
```
Subtracting avoids the wasted extra column that +1 would create.

```text
Frame 6   n = 2 = 1 0          steps = 5
  even -> halve
  n = 1                         steps = 6, stop
```
The answer is 6, matching the full recursion `f(23) = 6`.

Every odd step was immediately followed by at least one halving, so the bit length shrank at least once every two moves. The 1-bits were never increased: +1 at `...11` only collapsed runs, and -1 at `...01` only removed the last 1.

## Why it is correct

Write `f(k)` for the true minimum number of moves from `k`. First, a small lemma: **neighbours differ by at most one**, `|f(k+1) - f(k)| <= 1`. If the smaller of the two is odd, it can step onto the other in one move. If it is even, the odd neighbour can step onto it. Either way one direction is immediate, and the other direction follows by induction on the halves. A quick numerical check confirms it for every `k` below 200,000.

Now take odd `n > 3` ending in `11`, so `n = 4c - 1`.

```text
 +1:  4c - 1 -> 4c -> 2c                 2 moves, then 1 + f(c)
 -1:  4c - 1 -> 4c - 2 -> 2c - 1 (odd)   2 moves, then
      2c - 1 -> 2c   -> c                2 + f(c)
      2c - 1 -> 2c-2 -> c - 1            2 + f(c - 1)
```

The +1 route costs `2 + 1 + f(c)`. The -1 route costs `2 + 2 + min(f(c), f(c-1))`. By the lemma, `f(c) <= f(c-1) + 1`, so `1 + f(c) <= 2 + min(f(c), f(c-1))`. Adding 1 is never worse. The step that needed `2c - 1 > 1` is where `n > 3` came in. At `n = 3`, `2c - 1 = 1` is already the target, so -1 wins outright, 2 moves against 3.

For `n = 4c + 1`, ending in `01`, it is the mirror image. -1 reaches `2c` in two moves, then needs `1 + f(c)`. +1 reaches the odd number `2c + 1`, which then needs `2 + min(f(c), f(c+1))`. The lemma `f(c) <= f(c+1) + 1` makes -1 never worse.

So every greedy move is optimal from its position, and the whole sequence is optimal. The solution file also checks the greedy against full recursion for every `n` below 3000.

## Cost

- Time: O(log n). Every odd move is followed by a halving, so the bit length drops at least once every two moves, giving at most about `2 · 32` iterations.
- Space: O(1).

The memoised recursion is roughly O(log n) states in practice but carries a dictionary and recursion stack. The plain recursion is exponential-shaped.

## Variations you will meet

- **Minimum Operations to Reduce an Integer to 0** (LeetCode 2571: add or subtract powers of two): the same carry logic. A run of 1s costs two operations (add at the bottom, subtract at the top), and a lone 1 costs one. Walk the runs from the low end.
- **Broken Calculator** (LeetCode 991: double or decrement, from X to Y): work backwards from Y, halving when even and adding when odd. Same idea: the low bit decides the move.
- **BFS formulation**: treat numbers as nodes with edges `n/2`, `n±1` and run BFS. It is correct but explores far too much for `n` near `2^31`. It is useful as a brute-force checker.
- **Fixed-width overflow**: in Java/C, `n + 1` at `2^31 - 1` overflows. Use a long, or handle `INT_MAX` specially. Python is unaffected.

## What to carry forward

Odd numbers ending in `11` want +1, because the carry wipes the run of 1s. Those ending in `01` want -1. The number 3 is the lone exception. The low bits of a number are a cheap, local signal for a global decision. The next problem stops treating a number as a value and treats it as a **set**: each word becomes a 26-bit mask of its letters.
