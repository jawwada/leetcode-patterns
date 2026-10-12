# K Closest Points to Origin (LeetCode 973)

**Area:** heap · **Difficulty:** Medium · **Key operations:** push (-dist, x, y), evict the root when the heap exceeds k, read the k survivors

## Problem

Given `points` on a plane and an integer `k`, return the `k` points closest to the origin by Euclidean distance. Any order is accepted; the practice script returns the result sorted so it is deterministic.

## Example

```
points = [[3, 3], [5, -1], [-2, 4]], k = 2
squared distances: 18, 26, 20
answer: [[-2, 4], [3, 3]]        (18 and 20 beat 26)
```

Squared distance is enough: `sqrt` is monotonic, so it never changes which point is closer.

## Brute force

Compute every point's squared distance, sort all `n` points by it, take the first `k`.

O(n log n) time, O(n) space. The wasted work: sorting fully orders all `n` points, but we only need to separate the `k` smallest from the rest. The relative order of the `n - k` far points is irrelevant and still paid for.

## From brute force to optimal

A point farther than `k` points already seen can never be in the answer, so it can be rejected the moment it arrives. To make that test cheap we need fast access to the *worst* point currently kept: a max-heap of size `k` keyed on distance, whose root is the farthest kept point. Each new point is pushed; if the heap now holds `k + 1` points, pop the root (the farthest) so that only `k` survive. The heap never exceeds `k + 1` entries, so each push or pop costs O(log k) and the whole pass is O(n log k).

Python's `heapq` is a min-heap, so store `-distance` to make the smallest entry the farthest point. (Quickselect on distance gives O(n) average; the heap is the standard interview answer and streams.)

## Intuition

Hold a "k closest so far" club whose doorman is the farthest member. Every arriving point only has to beat the doorman: it walks in, and if the club is now over capacity, the current farthest member is shown out. Geometrically the kept points fill a disc around the origin whose radius is the root's distance; a new point either lands inside (admitted, and the disc shrinks to the new farthest member) or outside (it is admitted and immediately evicted, the disc unchanged). The radius never grows.

## Walkthrough

Heap drawn as its array, each entry as `(d, (x, y))`; the root is the first entry and the farthest point.

```
point (3, 3)   d=18   push    heap [(18, (3,3))]
point (5, -1)  d=26   push    heap [(26, (5,-1)), (18, (3,3))]            size 2 = k, keep
point (-2, 4)  d=20   push    heap [(26, (5,-1)), (18, (3,3)), (20, (-2,4))]
                      size 3 > k=2: evict root (5, -1) d=26
                              heap [(20, (-2,4)), (18, (3,3))]            radius now 20
end: survivors (-2, 4) and (3, 3), sorted -> [[-2, 4], [3, 3]]
```

```
         radius 26 -> 20
        .  (5,-1) d=26 evicted
      .   (-2,4) d=20 kept     the disc shrinks to the farthest survivor
     .  (3,3) d=18 kept
     O
```

## Steps

1. `kept = []`, a heap of `(-d, x, y)`.
2. For each point: `d = x*x + y*y`, push `(-d, x, y)`.
3. If `len(kept) > k`: `heappop` the root, the farthest kept point.
4. After the loop the heap holds exactly `k` points; return their coordinates (sorted here for determinism).

## Complexity

O(n log k) time: `n` pushes and at most `n` pops on a heap of at most `k + 1` entries. O(k) extra space.

## Pitfalls

- **Forgetting the minus sign.** With `(d, x, y)` the root is the *closest* point, so the eviction throws away the best point every time: `[[1, 3], [-2, 2]], k = 1` keeps `[1, 3]`.
- **Evicting with `>=` instead of `>`.** The heap is trimmed to `k - 1` after every push; `k = 1` returns an empty list.
- **`kept.pop()` instead of `heapq.heappop(kept)`.** `list.pop()` removes the last array slot, which is an arbitrary leaf of the heap (often the point just pushed), not the root.
- **Taking the square root.** Unnecessary, slower, and floating point; squared distances order identically.
- **Manhattan distance.** `abs(x) + abs(y)` is a different metric: `[[3, 0], [2, 2]]` has Euclidean 9 vs 8 but Manhattan 3 vs 4.
