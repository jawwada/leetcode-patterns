# Sort Colors
*LeetCode 75 · Medium · Pattern: Dutch national flag (three-way partition) · Reading time ~7 min*

## What the problem is really asking

The array holds only 0s, 1s and 2s (red, white, blue). Sort it in place, without the library sort, ideally in one pass with O(1) extra space. Nothing is returned.

Sorting three distinct values is really **partitioning**: every 0 must end up in a left band, every 1 in a middle band, every 2 in a right band. The difficulty is doing it in a single pass, because when you read a 2 near the start, you do not yet know where the 2-band begins.

```text
before: [ 2 | 0 | 2 | 1 | 1 | 0 ]
after:  [ 0 | 0 | 1 | 1 | 2 | 2 ]
          \___/   \___/   \___/
           red    white   blue
```

## Do it by hand first

Pretend the cells are coloured cards on a table. A natural way: pick up cards one by one from the left; throw reds onto a pile at the far left, blues onto a pile at the far right, and leave whites where they are. The red pile grows rightward, the blue pile grows leftward, and the whites end up squeezed between.

```text
  red pile -->                  <-- blue pile
  [ 0  0 | 1  1 | ?  ?  ? | 2  2 ]
           ^      ^     ^
          low    mid   high
```

Your hands tracked three boundaries: the end of the red pile, the card you are looking at, and the start of the blue pile. Those are the three pointers.

## The first honest attempt

Counting sort: one pass to count the 0s, 1s and 2s, a second pass to overwrite the array with that many of each. O(n) time, O(1) space. Honestly, this is a fine answer and you should mention it.

Its weakness is the second pass. It rewrites every cell, including the ones that were already right, and it only works because the values are bare integers. If each element were a record with a colour key and a payload, "write three 0s" would lose the payloads.

```text
pass 1 (count):   [2 0 2 1 1 0] -> zeros=2 ones=2 twos=2
pass 2 (rewrite): [0 0 1 1 2 2]   every cell written,
                                   original objects lost
```

The one-pass question is: can each element be moved, by swapping, straight to its band?

## The turning point

**Claim: if you keep four regions (0s, 1s, unknown, 2s), then examining the first unknown cell always lets you shrink the unknown region by one with at most one swap.**

The regions are defined by three indices:

```text
  [ 0 .. 0 | 1 .. 1 | ? .. ? | 2 .. 2 ]
    0        low      mid      high+1    n
  nums[0:low]        all 0
  nums[low:mid]      all 1
  nums[mid:high+1]   unknown
  nums[high+1:n]     all 2
```

Look at `nums[mid]`, the first unknown cell:

- **It is 1.** It already sits right after the 1-band. Advance `mid`; the 1-band grows.
- **It is 0.** Swap it with `nums[low]`, the first cell of the 1-band (or `mid` itself if the 1-band is empty). The 0 lands at the end of the 0-band; the 1 that was at `low` moves to `mid`, the end of the 1-band. Advance both `low` and `mid`.
- **It is 2.** Swap it with `nums[high]`, the last unknown cell. The 2 joins the 2-band; decrement `high`. Do **not** advance `mid`: the value that arrived from `high` was unknown, and nobody has looked at it yet.

That asymmetry is the whole subtlety. After a swap with `low`, you know what came back (a 1, or the same 0). After a swap with `high`, you do not.

The loop runs while the unknown region is non-empty, `mid <= high`. Using `<` would leave the last unknown cell unexamined.

This is a three-pointer version of the reader/writer idea: `mid` reads, `low` writes 0s from the left, `high` writes 2s from the right.

## Watch it work

`nums = [2, 0, 2, 1, 1, 0]`. Start `low = mid = 0`, `high = 5`.

Frame 1. `nums[0] = 2`. Swap with `nums[5]` (a 0). `high = 4`; `mid` stays at 0 because the incoming 0 is unexamined.

```text
  [ 0 | 0 | 2 | 1 | 1 | 2 ]
    L               H   2-band
    M
  low=0 mid=0 high=4
```

Frame 2. `nums[0] = 0`. Swap with `nums[low]`, the same cell. `low = mid = 1`.

```text
  [ 0 | 0 | 2 | 1 | 1 | 2 ]
        L           H
        M
  low=1 mid=1 high=4
```

Frame 3. `nums[1] = 0`. Same again; `low = mid = 2`.

```text
  [ 0 | 0 | 2 | 1 | 1 | 2 ]
            L       H
            M
  low=2 mid=2 high=4
```

Frame 4. `nums[2] = 2`. Swap with `nums[4]` (a 1). `high = 3`; `mid` stays.

```text
  [ 0 | 0 | 1 | 1 | 2 | 2 ]
            L   H
            M
  low=2 mid=2 high=3
```

Frame 5. `nums[2] = 1`: `mid = 3`. Then `nums[3] = 1`: `mid = 4`. Now `mid > high`, the unknown region is empty, and the array is sorted.

```text
  [ 0 | 0 | 1 | 1 | 2 | 2 ]
    \___/   \___/   \___/
     red    white   blue
  low=2 mid=4 high=3   mid > high: stop
```

Every frame satisfied the four-region picture, and the unknown region `[mid, high]` shrank by exactly one cell per step.

## Why it is correct

The invariant is the region description above. It holds at the start (all four regions except "unknown" are empty).

Each case preserves it:

- 1 at `mid`: the 1-band extends by one cell that is a 1.
- 0 at `mid`: after the swap, `nums[low]` is 0, which extends the 0-band. `nums[mid]` now holds what was at `low`: a 1 if the 1-band was non-empty, or the same 0 if `low == mid`. Either way, advancing `mid` keeps `nums[low+1:mid+1]` all 1s.
- 2 at `mid`: after the swap, `nums[high]` is 2, extending the 2-band. `nums[mid]` is unknown and remains inside the unknown region.

Each step shrinks the unknown region by one. When it is empty, the array is 0s, then 1s, then 2s.

## Cost

- Time: O(n). The unknown region starts with n cells and loses one per iteration.
- Space: O(1). Three integers.

Each element is swapped at most twice. Counting sort is also O(n) and O(1) but uses two passes.

## Variations you will meet

- **Partition around a pivot (quicksort's three-way partition)**: replace "is 0 / 1 / 2" with "less than / equal to / greater than pivot". This is exactly how quicksort handles many duplicates without degrading to O(n^2).
- **Sort Colors II / k colours (LintCode 143)**: three-way partition does not extend directly. Either count (O(n + k)) or recursively partition by colour ranges (O(n log k)).
- **Two values only (e.g. evens before odds, LeetCode 905)**: drop the middle band; a reader/writer or a converging pair of pointers suffices.
- **Stable partition required**: swaps break stability. You would need extra space or the reader/writer copy pattern per band.

## What to carry forward

Name every region between your pointers before writing the loop; then each case is "what single swap restores the picture", and the only trap is advancing past a value you have not examined. The next problem goes back to two converging pointers on sorted data and makes explicit why each comparison throws away a whole line of candidate pairs.
