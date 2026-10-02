# Maximum Running Time of N Computers

*LeetCode 2141 · Hard · Pattern: Binary search on the answer · Reading time ~10 min*

## What the problem is really asking

There are `n` computers and a pile of batteries, where `batteries[i]` is how many minutes of charge battery `i` holds. A computer runs on one battery at a time. At any whole minute we may pull batteries out and swap them between computers as often as we like, but a battery can power only one computer at any given moment, and charge never moves from one battery to another. We want the longest time for which **all `n` computers run simultaneously**.

The answer is a number of minutes. The hard part is the swapping. It sounds like it makes the problem a scheduling puzzle with an enormous search space, but it actually makes the problem simpler, once you see what swapping does and does not allow.

```text
n = 3, batteries = [10, 10, 3, 5]      answer: 8

total charge = 28 minutes
3 computers  -> at most 28 / 3 = 9 minutes if nothing is wasted

but at t = 9 each 10-battery can give only 9 minutes:
  a battery is in ONE computer at a time, so over
  9 minutes it can supply at most 9 minutes of charge
```

So the answer is not simply `sum // n`. Big batteries carry charge that cannot all be spent in time.

## Do it by hand first

Take `n = 2`, `batteries = [3, 3, 3]`. There are 9 minutes of charge and 2 computers, so at best we get 4 minutes (8 battery-minutes, with one left over). Can we actually reach 4? Write a 2-row timeline, one row per computer and one column per minute, and fill it in.

```text
minute:      1  2  3  4
computer 1:  A  A  A  B
computer 2:  B  B  C  C
                         A used 3, B used 3, C used 2
```

Battery B appears in both rows, but never in the same column, so it never powers two computers at once. That schedule works, and the answer is 4.

What did your hand track? **How many cells of the n-by-t grid still need filling, and whether any single battery was being asked to fill two cells in the same column.** A battery can be in a column at most once, so it can fill at most `t` cells. That cap is the seed of the whole solution.

## The first honest attempt

Simulate the run minute by minute. Each minute, put the `n` batteries with the most charge left into the computers, run one minute, and subtract 1 from each. Stop when fewer than `n` batteries have charge. Picking the fullest batteries is the right greedy, since it saves the small ones for later, when the big ones have come down to their size.

```text
n=3, batteries [10,10,3,5]: remaining charge after each minute
  t=1  [9, 9, 3, 4]
  t=2  [8, 8, 3, 3]
  t=3  [7, 7, 2, 3]
  t=4  [6, 6, 2, 2]
  t=5  [5, 5, 1, 2]
  t=6  [4, 4, 1, 1]
  t=7  [3, 3, 0, 1]
  t=8  [2, 2, 0, 0]  <- only two batteries left: stop at 8
```

That costs O(T · m log m), where T is the answer, and T can be around 10^14 / n. The repeated work is that every minute re-sorts and re-decides, although the outcome is settled by a single fact we could compute up front: how much usable charge exists for a given duration.

## The turning point

**Claim: all `n` computers can run for `t` minutes if and only if `sum(min(b, t) for b in batteries) >= n · t`.**

*Necessary.* Running `n` computers for `t` minutes uses `n · t` battery-minutes. A battery sits in at most one computer per minute, so over `t` minutes it supplies at most `min(b, t)`. If the clamped total falls short, no schedule exists.

*Sufficient.* Draw the `n · t` battery-minutes as a strip of `n` rows and `t` columns. Lay the clamped batteries end to end along the rows, reading left to right and wrapping to the next row whenever a row fills. Stop once all `n · t` cells are full.

```text
n=2, t=4, clamped [3, 3, 3]
row 1 (computer 1):  A A A B
row 2 (computer 2):  B B C C      (C's 3rd minute unused)
                     ^ ^     ^
       B wraps: it ends row 1 at column 4 and
       starts row 2 at column 1 -- different columns
```

A battery of length `L <= t` that wraps covers the right end of one row and the left start of the next, and those two parts cannot overlap in any column, because together they span `L <= t` columns. So no battery is ever in two computers in the same minute, and the strip is a valid schedule. The clamp `min(b, t)` is exactly what guarantees `L <= t`.

**The predicate is `can(t)`: the clamped total is at least `n · t`. It is monotone.** If `can(t)` holds, a valid `t`-minute schedule exists, and stopping it one minute early gives a valid `(t-1)`-minute schedule, so `can(t-1)` holds. Over `t` the picture is `T ... T F ... F`, and we want the **last T**.

```text
t       :  1  2  3  4  5  6  7  8  9
clamped :  4  8 12 15 18 20 22 24 26
need n*t:  3  6  9 12 15 18 21 24 27
can(t)  :  T  T  T  T  T  T  T  T  F
                                ^
                       last T = answer 8
```

*The range.* `lo = 0`, which always holds trivially. `hi = sum(batteries) // n` is the no-waste ceiling, since even clamping nothing you cannot spread more than `sum` minutes over `n` computers.

*The template for "last T".* Use `while lo < hi` with `mid = (lo + hi + 1) // 2`. On T set `lo = mid`, on F set `hi = mid - 1`. Rounding `mid` up matters: with `lo = 5, hi = 6`, a rounded-down `mid` would be 5, a T would set `lo = 5` again, and the loop would never end.

```text
mid = (lo + hi + 1) // 2
if can(mid): lo = mid        # mid works; maybe more
else:        hi = mid - 1    # mid fails; so does all above
```

## Watch it work

`n = 3`, `batteries = [10, 10, 3, 5]`. The range is `[0, 28 // 3] = [0, 9]`.

```text
Frame 1   lo=0  hi=9  mid=5
  clamp to 5: [5, 5, 3, 5]  sum=18   need 3*5=15
  18 >= 15  -> T
```
Five minutes is achievable, and the answer may be larger: `lo = 5`.

```text
Frame 2   lo=5  hi=9  mid=(5+9+1)//2=7
  clamp to 7: [7, 7, 3, 5]  sum=22   need 21
  22 >= 21  -> T
```
Seven works: `lo = 7`.

```text
Frame 3   lo=7  hi=9  mid=8
  clamp to 8: [8, 8, 3, 5]  sum=24   need 24
  24 >= 24  -> T  (exactly: zero slack)
```
Eight works with no charge to spare in the clamped total: `lo = 8`.

```text
Frame 4   lo=8  hi=9  mid=9
  clamp to 9: [9, 9, 3, 5]  sum=26   need 27
  26 <  27  -> F
            ^ each 10 loses 1 minute to the clamp
```
Nine fails because each big battery can contribute only 9: `hi = 8`. Now `lo == hi == 8`, so the answer is 8.

```text
Frame 5   the t=8 schedule as a strip (3 rows x 8)
  computer 1:  A A A A A A A A
  computer 2:  B B B B B B B B
  computer 3:  C C C D D D D D
```
The strip for the final answer fills every cell exactly, which matches the zero slack in frame 3.

In every frame, `can(lo)` was known true and everything above `hi` known false. Each probe was a single pass with no schedule built. The schedule exists because of the strip argument, but the algorithm never needs to construct it.

## Why it is correct

**Invariant: `can(lo)` is true and `can(hi + 1)` is false (or `hi` is the ceiling `sum // n`, above which `n · t > sum >= clamped total`).** Initially `can(0)` is trivially true. On T, `lo = mid` keeps `can(lo)` true. On F, monotonicity makes every `t >= mid` false, so `hi = mid - 1` keeps the upper half false. Since `mid > lo` when rounded up, `lo` strictly increases on T, and `hi` strictly decreases on F, so the loop terminates. When `lo == hi`, that value is true and the one above is false: it is the largest feasible `t`. The iff-claim above ensures "feasible" in the predicate means a real schedule exists, so this is the maximum running time.

## Cost

- **Simulation: O(T · m log m)** time with T up to about 10^14, which is hopeless.
- **Binary search: O(m log(S / n))** time, where S = `sum(batteries)`. There are about 47 probes at worst, each one pass over `m` batteries. **O(1)** space.
- An alternative O(m log m) solution sorts the batteries and repeatedly discards the largest one while it exceeds `sum / n` (that battery gets a dedicated computer). It is the same clamp insight applied directly.

## Variations you will meet

- **Sorted greedy instead of search.** Sort descending. While the largest battery exceeds `remaining_sum / remaining_n`, give it its own computer and drop both. The answer is then `remaining_sum // remaining_n`. Same proof, different engine.
- **Minimum Time to Complete Trips (LeetCode 2187).** First-T search on time, where the check is `sum(t // time[i]) >= totalTrips`. Same shape with an easier check.
- **Batteries with a swap cost.** Swapping is no longer free, the strip argument fails, and the problem becomes real scheduling.
- **Different computers need different power.** The rows now have different lengths, and the clamp turns into a flow problem.

## What to carry forward

A single resource that can be in only one place at a time contributes at most `t` to a length-`t` schedule. Clamp each resource to `t`, compare the total to the demand, and binary search the last `t` that passes, rounding `mid` up.

The next problem leaves feasibility behind for counting: to find the k-th smallest value of a huge implicit table, binary search on the value and count how many entries fall at or below it.
