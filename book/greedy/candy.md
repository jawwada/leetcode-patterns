# Candy

*LeetCode 135 · Hard · Pattern: Two-pass greedy (left-to-right, right-to-left) · Reading time ~9 min*

## What the problem is really asking

Children stand in a line, each with a rating. You hand out candies under two rules. Everyone gets at least one. If a child is rated strictly higher than an immediate neighbour, that child must get strictly more candy than that neighbour. Minimise the total.

The answer is one number, but behind it sits an assignment: a candy count per child. The rules are purely local, each one compares two adjacent children, yet the counts are not local at all. A child at the top of a long downhill slope needs many candies because every child below them on the slope needs one more than the next. A single comparison can force a number that depends on something five seats away.

Two details matter. "Strictly higher" means equal neighbours impose nothing on each other: two children rated 2 and 2 may get 1 and 7 candies. And the constraint is one-directional per pair: the higher-rated one must have more, the lower one has no obligation.

```text
ratings:  1   2   4   3   2   1
          .   .   #   .   .   .        # = peak
              /\
candies:  1   2   4   3   2   1      total 13
          left climb   right descent
          1->2->?      ?<-3<-2<-1
```

The peak at rating 4 sits between a climb of length 3 on the left and a descent of length 4 on the right. It needs more than the child on its left (who has 2) and more than the child on its right (who has 3). The descent wins: 4 candies.

## Do it by hand first

With pen and paper you would probably start everyone at 1 and then go looking for broken rules.

```text
ratings:  1   2   4   3   2   1
start:    1   1   1   1   1   1
fix i=1 (2>1):            1 2 1 1 1 1
fix i=2 (4>2):            1 2 3 1 1 1
fix i=4 (2>1):            1 2 3 1 2 1
fix i=3 (3>2):            1 2 3 3 2 1
fix i=2 (4>3, 3 !> 3):    1 2 4 3 2 1
```

Notice what your hand did. It walked up the left slope pushing counts forward, then it had to walk down the right slope from the far end, because the child rated 3 cannot know their count until the child rated 2 knows theirs, who waits on the child rated 1. Then it came back to the peak and raised it a second time.

What your hand kept track of was, for each child, two lengths: how long a strictly rising run ends at them coming from the left, and how long a strictly rising run ends at them coming from the right. That pair of numbers is the seed of the algorithm.

## The first honest attempt

The brute force is exactly the hand procedure, automated. Give everyone 1. Sweep the line; whenever a child is rated higher than a neighbour but does not have more candy, set them to neighbour + 1. Repeat sweeps until one full sweep changes nothing.

It is correct, because it only raises a child when a rule forces it, so it never overshoots the minimum. But it is slow. A descending line `5 4 3 2 1` swept left to right fixes only one child per sweep, because each fix depends on the child to its right, which has not been fixed yet:

```text
ratings:  5 4 3 2 1
sweep 1:  1 1 1 2 1    only i=3 sees a settled neighbour
sweep 2:  1 1 3 2 1
sweep 3:  1 4 3 2 1
sweep 4:  5 4 3 2 1
sweep 5:  no change -> stop
          each sweep re-reads all n children to move
          one value one seat
```

That is O(n^2) time. The repeated work is the information travelling one seat per sweep against the direction of the scan.

There is also a tempting greedy that is wrong. "Go left to right; if you are higher than your left neighbour take their count + 1, otherwise take 1. Then go right to left and, if you are higher than your right neighbour, set yourself to their count + 1." It sounds symmetrical and fair. Try `ratings = [1, 2, 3, 1]`:

```text
ratings:      1  2  3  1
left pass:    1  2  3  1
right pass, overwrite:
  i=2: 3>1 -> c[2] = c[3]+1 = 2
result:       1  2  2  1      BROKEN: rating 3 next to
                              rating 2, both have 2
```

The second pass threw away what the first pass had learned. That is the whole bug, and the fix is one word: `max`.

## The turning point

**Claim: the rules split into two independent families, and each family alone is solved exactly by one directional pass; a child's answer is the larger of the two passes.**

Look at the rules again. Each rule is "if `r[i] > r[i-1]` then `c[i] > c[i-1]`" (a left rule) or "if `r[i] > r[i+1]` then `c[i] > c[i+1]`" (a right rule). Left rules only ever point from a child to the child on their left. If you scan left to right, then by the time you reach child `i` the left neighbour's count is already final for the left family, so you can give `i` exactly what is needed: `L[i] = L[i-1] + 1` if `r[i] > r[i-1]`, else 1. Nothing smaller works, because `L[i]` is the length of the strictly rising run ending at `i`, and every child on that run needs at least one more than the one before.

The right family is the mirror image, solved by scanning right to left: `R[i] = R[i+1] + 1` if `r[i] > r[i+1]`, else 1.

Now each child must satisfy both families at once, and the smallest number that is at least `L[i]` and at least `R[i]` is `max(L[i], R[i])`. The question is whether taking the max at one child can break a rule at a neighbour. It cannot. Suppose `r[i] > r[i-1]`. Then `c[i] >= L[i] = L[i-1] + 1`. And `c[i-1]`? If `c[i-1] = L[i-1]` we are fine. If instead `c[i-1] = R[i-1]`, note that `R[i-1]` is 1 because `r[i-1] < r[i]`, so the descent going right from `i-1` has length 1. Either way `c[i-1] <= L[i-1]` or `c[i-1] = 1`, and `c[i]` beats both. The symmetric argument handles right rules.

In code, the solution stores `L` directly in the `candies` array and folds the right pass in with a `max`, so there is no separate `R` array:

```text
pass 2 step:  if r[i] > r[i+1]:
                 c[i] = max(c[i], c[i+1] + 1)
                 ^ keep left knowledge  ^ add right knowledge
```

Geometrically: plot the ratings as terrain. The left pass paints a staircase up every ascent, dropping back to 1 at each non-rise. The right pass paints the mirror staircase up every descent read backwards. The answer is the upper envelope of the two staircases.

## Watch it work

Example: `ratings = [1, 2, 4, 3, 2, 1]`. The solution returns 13.

Frame 1. Initialise everyone to 1.

```text
i:        0  1  2  3  4  5
ratings:  1  2  4  3  2  1
candies:  1  1  1  1  1  1
```

Every child has the floor value; no rule has been looked at yet.

Frame 2. Left pass, i = 1..2: each is a rise, so each takes left + 1.

```text
i:        0  1  2  3  4  5
ratings:  1  2  4  3  2  1
candies:  1  2  3  1  1  1
                 ^ i=2: 4>2 -> 2+1
```

The climb 1, 2, 4 becomes the staircase 1, 2, 3.

Frame 3. Left pass, i = 3..5: no rises (3<4, 2<3, 1<2), so they stay 1.

```text
candies after left pass:
          1  2  3  1  1  1
          L staircase:  _/^\___   (only rises counted)
```

Every left rule now holds; right rules at i = 2, 3, 4 are still broken.

Frame 4. Right pass starts at i = 4: 2 > 1, so max(1, 1+1) = 2.

```text
i:        0  1  2  3  4  5
candies:  1  2  3  1  2  1
                       ^ i=4: right neighbour 1 -> 2
```

The descent is now being measured from its low end.

Frame 5. i = 3: 3 > 2, so max(1, 2+1) = 3.

```text
i:        0  1  2  3  4  5
candies:  1  2  3  3  2  1
                    ^ i=3 -> 3
```

Child 3 now ties the peak, which is a broken rule at the peak, but the peak is next.

Frame 6. i = 2: 4 > 3, so max(3, 3+1) = 4. The right side wins at the peak.

```text
i:        0  1  2  3  4  5
candies:  1  2  4  3  2  1
                 ^ max(L=3, R=4) = 4
```

Frame 7. i = 1 and i = 0: 2 < 4 and 1 < 2, no right rule applies. Sum = 13.

```text
final:    1  2  4  3  2  1    sum = 13
```

Across the frames, after the left pass every left rule held and no later step lowered any value, so the left rules kept holding. During the right pass, every position to the right of the scan pointer satisfied all right rules. When the pointer reached 0, both families held everywhere.

## Why it is correct

There are two halves: the result is valid, and it is minimal.

Validity is the invariant above. After pass 1, `c[i] = L[i]` and every left rule holds. Pass 2 only raises values (the `max`), and raising a child cannot break a left rule where that child is the higher one; could it break a left rule where the raised child is the lower one, `r[i-1] < r[i]`? Pass 2 raises `c[i-1]` only if `r[i-1] > r[i]`, which contradicts `r[i-1] < r[i]`. So left rules survive. And when pass 2 processes `i`, it makes `c[i] > c[i+1]` whenever the right rule demands it, while `c[i+1]` is never touched again. So right rules hold too.

Minimality is a chain argument rather than an exchange. Take any valid assignment `d`. If `L[i] = k`, there is a strictly rising run of length `k` ending at `i`, so `d` must increase by at least 1 at each step along it, giving `d[i] >= k`. The same holds for `R[i]`. So `d[i] >= max(L[i], R[i]) = c[i]` for every child, and the total of `d` is at least the total of `c`. Every candy we hand out is forced by some chain; nothing is given away.

## Cost

Time O(n): two linear passes plus a sum.

Space O(n) for the candies array. There is an O(1)-space one-pass version that counts the current up-run and down-run lengths and adds triangular numbers, correcting the peak when the down-run outgrows the up-run; it is the same staircase idea with more bookkeeping and is easy to get wrong under pressure.

## Variations you will meet

- **Circular line.** The first and last children become neighbours. A rising run can now wrap, so rotate the array to start at a global minimum (a child with nothing forced below it) and run the linear algorithm.
- **Equal ratings must get equal candy.** Now equality is a constraint, so collapse runs of equal ratings into one node, solve the staircase on the compressed line, and multiply back by run length.
- **Only the left rule.** One pass suffices; this is the length of the strictly rising run ending at each index, a pattern that also underlies "longest increasing contiguous subarray".
- **Trapping Rain Water.** Same two-pass shape: a left-to-right prefix quantity, a right-to-left suffix quantity, combined per position (there with `min`, here with `max`).

## What to carry forward

When local rules point in two directions, satisfy each direction with its own sweep and merge with `max`; every value is then forced by a chain, so it is minimal. The next problem also reads only adjacent pairs, but asks how many contiguous +1 strokes build a target, and the answer comes from counting rises alone.
