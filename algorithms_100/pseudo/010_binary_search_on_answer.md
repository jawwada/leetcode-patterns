---
rank: 10
slug: binary_search_on_answer
---

Koko has piles of bananas and `h` hours. She picks one eating speed `k`; each hour she eats `k` bananas from a single pile, and when fewer than `k` are left in that pile she still spends the whole hour on it. Return the smallest `k` that finishes every pile within `h` hours; `h` is at least the number of piles, so some speed always works. For piles `[3, 6, 7, 11]` and `h = 8` the answer is `4`: at speed 4 the piles take `1 + 2 + 2 + 3 = 8` hours, while at speed 3 they take `1 + 2 + 3 + 4 = 10`.

Nothing here is sorted, yet binary search applies, because the search runs over the answer instead of over the array. Trying every speed from 1 upward costs `O(n · m)` for the largest pile `m`. The insight is that feasibility is monotone: if Koko finishes at speed `k`, she finishes at every faster speed, so the question "can she finish at speed `k`?" reads ✗ ✗ ✗ then ✓ ✓ ✓ along the number line of speeds. The answer is the first ✓, exactly the boundary that the lower-bound template of #9 finds. Only the probe changes: instead of comparing `nums[mid]` with a target, it simulates a whole meal at speed `mid` in one pass, summing `ceil(pile / mid)` hours.

Every problem of this kind has the same three parts. The range `[lo, hi]` holds every candidate answer, with `lo` the smallest conceivable value and `hi` a value that surely works; here they are `1` and `max(piles)`, since at that speed every pile takes one hour. The check `feasible(x)` is a simple simulation, usually `O(n)`, whose answer flips once from no to yes. The loop keeps a ✓ at `mid` with `hi ← mid`, drops a ✗ with `lo ← mid + 1`, and stops when `lo = hi`. "Largest value that still works" is the mirror image: search for the first value that fails and step back one.

```text
speed          1   2   3   4   5   6   7   8   9  10  11
hours         27  15  10   8   8   6   5   5   5   5   4
hours ≤ 8?     ✗   ✗   ✗   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓
                           ▲ the answer: the first ✓

   lo   hi   mid   hours at mid   ≤ 8?   move
    1   11     6         6         yes   hi ← 6
    1    6     3        10         no    lo ← 4
    4    6     5         8         yes   hi ← 5
    4    5     4         8         yes   hi ← 4
    4    4   lo = hi: the smallest speed is 4
```

```pseudo
FUNCTION CanFinish(piles, h, speed)      // the yes/no check
    hours ← 0
    FOR EACH pile IN piles
        hours ← hours + ceil(pile / speed)   // a partial hour costs a full one
    RETURN hours ≤ h

FUNCTION MinEatingSpeed(piles, h)
    lo ← 1                               // the slowest possible speed
    hi ← max(piles)                      // one pile per hour: always enough
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF CanFinish(piles, h, mid)
            hi ← mid                     // mid works; a slower speed might too
        ELSE
            lo ← mid + 1                 // mid fails, so does every slower one
    RETURN lo
```

The check runs once per halving of the speed range, so the cost is `O(n log m)` time and `O(1)` space. The signals are phrases such as "minimum capacity", "smallest speed", "minimize the largest" or "maximize the minimum", together with a check that is easy for any fixed answer and flips only once as the answer grows. The classic mistakes sit in the check and in the range: `pile // mid` rounds down and forgets the partial last hour, which makes slow speeds look feasible, and starting `lo` at `0` can divide by zero.

*Practice:* LC 875 Koko Eating Bananas · LC 1011 Capacity To Ship Packages Within D Days · LC 410 Split Array Largest Sum · LC 1482 Minimum Number of Days to Make m Bouquets
