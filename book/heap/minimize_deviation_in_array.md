# Minimize Deviation in Array

*LeetCode 1675 · Hard · Pattern: Max-heap of normalised values, repeatedly shrink the maximum · Reading time ~12 min*

## The problem

You may apply any number of operations to nums: halve an even element or double an odd element. The deviation is
max(nums) - min(nums). Return the minimum deviation achievable.

```text
Example: [1,2,3,4] -> 1 (double 1, halve 4: [2,2,3,2]).
  [4,1,5,20,3] -> 3. [2,10,8] -> 3.
```

## What the problem is really asking

You have an array of positive integers and two moves you may repeat as often as you like: halve an **even** number, or double an **odd** number. The deviation of the array is `max - min`. Make the deviation as small as possible and return it.

The answer is a single number, but behind it is a choice of one value per element. What makes it hard is that the moves go in two directions (up for odd, down for even) and they interact: doubling a small odd number might lift the minimum, while halving a big even number might pull the maximum down, or might overshoot and become the new minimum.

Our example: `[4, 1, 5, 20, 3]`. The answer is 3, for instance by reaching `[4, 2, 5, 5, 3]`: max 5, min 2.

```text
  4 | ####
  1 | #                     <- min 1
  5 | #####
 20 | ####################  <- max 20
  3 | ###
      start: deviation 20 - 1 = 19
```

## Do it by hand first

Look at what each number can actually become.

- An odd number `x` can double to `2x`. Now it is even, so the only move is to halve back to `x`. So an odd `x` has exactly two values: `{x, 2x}`.
- An even number can only halve, and it can keep halving until it hits an odd number (its "odd core"). That core could double again, but that only climbs back up the same ladder.

So every element lives on a short **ladder** of rungs, each rung half the one above.

```text
 element:   4      1      5      20     3
           ---    ---    ---    ---    ---
 rungs:     4      2     10     20      6     <- top rung
            2      1      5     10      3
            1                    5            <- bottom (odd)
```

Now, by hand: start everyone at the top of their ladder: `[4, 2, 10, 20, 6]`, deviation `20 - 2 = 18`. The biggest number, 20, is clearly the problem. Pull it down a rung: 10. Now the max is 10 (twice). Pull one 10 down to 5, then the other 10 down to 5. Max is 6; pull it to 3. Now the max is 5, which is odd, the bottom of its ladder. You cannot lower it, and nothing else you do can reduce the maximum.

What did your hand keep looking at? Always *the current biggest number*, and you kept stepping it down. A collection where you repeatedly take the largest, change it, and put it back is a max-heap. You also kept an eye on the smallest number, but it only ever moved down, so one variable suffices.

## The first honest attempt

Every element independently picks a rung of its ladder. Try every combination (the Cartesian product of all ladders), compute `max - min`, and keep the smallest. With `n` elements and ladders of length up to `log M + 1` (where `M` is the largest value), that is `O((log M)^n)` combinations, exponential in `n`.

The waste: almost every combination is dominated. Take any combination and lower an element that is *not* the maximum. The maximum stays put, the minimum can only stay or fall. The deviation cannot improve.

```text
 combination      max  min  dev
 [4,2,10,20,6]    20    2   18
 [2,2,10,20,6]    20    2   18   lowered a non-max: no gain
 [1,2,10,20,6]    20    1   19   lowered a non-max: worse
 [4,1,10,20,6]    20    1   19   lowered a non-max: worse
 ... all of these are enumerated and thrown away
```

The brute force spends nearly all its time on moves that cannot help.

## The turning point

There are two observations, and the second only works because of the first.

**Observation 1 (normalise): start every element on the top rung of its ladder.** Double every odd number once; leave even numbers alone. From that starting point, every possible configuration is reachable using only one kind of move: halve an even number. The two-directional problem becomes one-directional.

**Observation 2 (the claim): from the top-rung start, the only move worth making is to halve the current maximum, and once the maximum is odd, you can stop.**

Justify it. With only halvings available:

- Halving an element that is *not* the maximum leaves the maximum where it is and can only lower the minimum. The deviation cannot shrink.
- Halving the maximum is the only way to lower the maximum. It might lower the deviation. It might also overshoot: if the halved value drops below the current minimum, the minimum falls and the deviation could get worse. So the deviation is not monotone along the way, and we must remember the **best deviation seen**, not the last one.
- When the maximum is odd it sits at the bottom of its ladder. No move can lower it, so the maximum is stuck forever, and all further moves can only lower the minimum. Nothing after this point can beat what we already saw. Stop.

So the process is forced. There is no search: at each step exactly one move is worth considering. The data structure follows directly:

- a **max-heap** of current values (in Python, negated values in `heapq`) to find the maximum and replace it with its half;
- a single variable **`lo`**, the running minimum. Values only ever decrease, so the minimum only ever decreases, and `lo = min(lo, hi // 2)` after each halving keeps it exact.

At each step, read `hi` from the heap's root, record `hi - lo`, stop if `hi` is odd, otherwise replace the root by `hi // 2`. `heapreplace` does the pop and push as one sift.

## Watch it work

Normalised start: `4 -> 4`, `1 -> 2`, `5 -> 10`, `20 -> 20`, `3 -> 6`. The heap is shown largest first; `lo` is the running minimum.

Frame 1: Read the max, record, halve.

```text
        20            values {20, 10, 6, 4, 2}
       /  \           hi 20   lo 2   dev 18   best 18
      6    10         20 is even -> replace with 10
     / \
    2   4
 stored: [-20, -6, -10, -2, -4]
```

The worst offender, 20, steps down one rung.

Frame 2: Two 10s; the root is one of them.

```text
 values {10, 10, 6, 4, 2}
 hi 10   lo 2   dev 8    best 8
 10 even -> replace with 5;  lo stays 2
```

The deviation fell from 18 to 8 in one move.

Frame 3: The other 10 is now the max.

```text
 values {10, 6, 5, 4, 2}
 hi 10   lo 2   dev 8    best 8
 10 even -> replace with 5
```

Same deviation as before, because a tied maximum must be lowered twice before the max actually moves.

Frame 4: The max is 6.

```text
 values {6, 5, 5, 4, 2}
 hi 6    lo 2   dev 4    best 4
 6 even -> replace with 3;  lo stays 2
```

Frame 5: The max is 5, which is odd. Stop.

```text
        5             values {5, 5, 4, 3, 2}
       / \            hi 5    lo 2   dev 3    best 3
      5   3           5 is odd: bottom of its ladder
     / \              -> return 3
    2   4
 stored: [-5, -5, -3, -2, -4]
```

The answer is 3.

Throughout, every element was at the top rung of its ladder or had been halved only while it was the maximum, `lo` was the true minimum of the heap, and `best` was the smallest deviation of any configuration we passed through.

## Why it is correct

**Everything we record is real.** Each recorded `hi - lo` is the deviation of an actual configuration reachable with legal moves. So `best` is never smaller than the true optimum.

**We record something at least as good as the optimum: a dominance (exchange) argument.** Take any optimal configuration `C`, with maximum `Mc` and minimum `mc`. Compare it, rung by rung, with the algorithm's state at the first moment the heap's maximum is `<= Mc`.

First, that moment exists. The algorithm only stops when the maximum is odd, at the bottom of its ladder. If that happened while the maximum was still `> Mc`, then that element cannot go below `Mc` at all, so `C` (whose max is `Mc`) could not exist.

Now, at that moment, look at each element. Either it was never halved, so it sits at its top rung, which is at least as high as its rung in `C`. Or it was halved, and the last time, it was the maximum of a state whose maximum was still `> Mc`; so its previous rung was `> Mc`, and its current rung is the highest rung `<= Mc`. Its rung in `C` is also `<= Mc`, hence no higher. Either way, **every element is at least as high as in `C`**, so the algorithm's minimum `lo >= mc`, while its maximum is `<= Mc`. The recorded deviation is at most `Mc - mc`, the optimum.

That is the exchange in plain words: any optimal configuration can be "raised" element by element to the algorithm's state at the right moment, without raising the maximum above `Mc` and without lowering the minimum. So the greedy walk passes through a configuration at least as good as any optimum, and `best` catches it.

## Cost

- **Time `O(n log M log n)`.** Each element can be halved at most `log M` times (where `M` is the largest normalised value), and each halving is one heap operation on `n` items. Building the heap is `O(n)`.
- **Space `O(n)`.** The heap holds one value per element.

Brute force is `O((log M)^n · n)` time.

## Variations you will meet

- **Only one direction from the start.** If the problem only allowed halving evens (no doubling), you would skip normalisation and run the same loop from the original values.
- **Smallest Range Covering Elements from K Lists (earlier in this chapter).** Read the ladders as `n` sorted lists, one per element; you must pick one value from each list and minimise `max - min`. That is exactly this problem's structure. There you advanced the *minimum* with a min-heap and tracked the max; here you lower the *maximum* with a max-heap and track the min. The same "move the extreme, track the other end" idea.
- **Remove Stones to Minimize the Total (LeetCode 1962).** A fixed budget of `k` "halve the biggest pile" moves. No minimum to track and no early stop, but the same max-heap loop: replace the root with its reduced value `k` times.

## What to carry forward

Normalise so every move goes one way, then the only useful move is on the heap's root: shrink the max, track the min in a variable, and remember the best deviation seen along the way. The next problem, Meeting Rooms III, keeps a heap's root as "the only item that matters right now", but uses two heaps of rooms that pass items back and forth as time advances.
