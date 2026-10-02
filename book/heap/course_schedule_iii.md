# Course Schedule III

*LeetCode 630 · Hard · Pattern: Sort by deadline + max-heap of taken durations (swap out the longest) · Reading time ~12 min*

## What the problem is really asking

Each course is a pair `(duration, lastDay)`: it takes `duration` days of your full attention and must be *finished* on or before `lastDay`. You take courses one at a time, back to back, starting from day 0 (finishing a course of length 5 started at day 0 means finishing on day 5). Return the largest number of courses you can complete.

The answer is a count, but behind it is a choice of a *subset* and an *order*. Both are free, and that is what makes it hard: a long course might block three short ones, an early deadline might force an awkward order, and it is not obvious which courses to sacrifice.

Our running example has four courses:

```text
 course   duration   lastDay
   A          5          5
   B          4          6
   C          2          6
   D          6          9

 timeline (days)  0    2    4    6    8    10   12
                  |----|----|----|----|----|----|
 deadlines                  A=5^ B,C=6^     D=9^
```

The answer is 2. For instance B then C finish on days 4 and 6. You cannot fit three: any three of these need at least 4 + 2 + 5 = 11 days, but the latest deadline is day 9.

## Do it by hand first

The first thing a person does is put the courses in deadline order. It feels right: do the urgent thing first. Then walk through and keep a running clock.

- A (5 days, due 5): clock 0 -> 5. Fine.
- B (4 days, due 6): clock 5 -> 9. Too late. Something has to go. You have A and B on your plate, both counting as one course each. Throw out A: it is longer. Now the plate is just B, clock 4.
- C (2 days, due 6): clock 4 -> 6. Fine. Plate: B, C.
- D (6 days, due 9): clock 6 -> 12. Too late. Plate is B, C, D. Throw out the longest, which is D itself. Clock back to 6.

```text
 plate after each course (bars laid end to end)
 after A : [AAAAA]               clock 5   ok (<= 5)
 after B : [AAAAA][BBBB]         clock 9   > 6  -> drop A
           [BBBB]                clock 4
 after C : [BBBB][CC]            clock 6   ok (<= 6)
 after D : [BBBB][CC][DDDDDD]    clock 12  > 9  -> drop D
           [BBBB][CC]            clock 6   answer 2
```

What did your hand track? The set of courses on the plate and its total length, and when the clock broke a deadline you asked one question: "which course on the plate is longest?" A collection you push into and repeatedly ask for its largest item is a max-heap.

## The first honest attempt

Try every subset. For each, check whether it can be scheduled; keep the biggest that can. Checking needs an order, and here is the first useful fact: **if a set of courses can be scheduled at all, it can be scheduled in deadline order.** (If two adjacent courses are out of deadline order, swapping them does not hurt: the later-due one now finishes at the time the earlier-due one used to finish, which was within the earlier deadline, so it is within its own later deadline too; the other course finishes earlier than before.)

So brute force sorts by deadline and tries all `2^n` subsets, walking each in order: `O(2^n · n)`.

The waste is enormous and easy to see. Most subsets differ from a good one by "this long course instead of that short one":

```text
 sorted:  A(5,5)  B(4,6)  C(2,6)  D(6,9)
 subset {A,C}   : 5, 7  -> fails at C
 subset {A,C,D} : 5, 7  -> fails at C   (same failure again)
 subset {A,B,C} : 5, 9  -> fails at B
 subset {A,B,D} : 5, 9  -> fails at B   (same failure again)
 every subset containing A plus anything due by 6 is
 re-walked only to fail at the same point
```

The sorted walk already *tells* you which course is the culprit every time it fails: the long one sitting on the plate. A single pass with the right repair rule should be enough.

## The turning point

**Claim: walk the courses in deadline order, provisionally take each one, and whenever the clock passes the current deadline, drop the longest course on the plate. The plate then always holds as many courses as possible, using as little total time as possible.**

Two separate ideas are welded together here.

*Why deadline order makes each check local.* Once courses are processed by deadline, the only question at course `i` is "does the total time already committed, plus this course, fit before `lastDay[i]`?" The current course goes last in the schedule, and every course already on the plate has an earlier or equal deadline that it already met. So the state you need is just one number, the total committed time.

*Why "drop the longest" is the right repair.* When the clock overflows, you have `k + 1` courses on the plate and the count cannot be `k + 1`. So you must drop one, and the count stays `k`. All `k + 1` candidates for dropping leave the same count, so the only thing that differs between them is the total time left on the plate. And total time is the only thing the future cares about: every later check is "total + next duration <= next deadline". Less total time is never worse. So drop the course that removes the most time: the longest one.

There is a neat side effect. If the current course is itself the longest on the plate, it gets dropped right back. "Push then pop the max" handles both the "swap a long old course for this short new one" case and the "this course does not fit, skip it" case with the same two lines.

Does dropping keep the plate feasible? Removing a course from a deadline-ordered schedule only pulls every later course earlier, so old deadlines stay met. And the current course, now finishing at `total + d - longest`, finishes no later than `total` (because `longest >= d`), which was within an earlier deadline, so within its own.

The structure: a max-heap of durations on the plate, plus one integer `time`. Push the duration, add it to `time`, and if `time > lastDay`, pop the max and subtract it. The answer is the heap's size.

## Watch it work

Sorted by deadline: A(5,5), B(4,6), C(2,6), D(6,9). The heap is listed largest first.

Frame 1: Take A.

```text
 push 5          time 0 -> 5     deadline 5   ok
 heap [5]        count 1
```

A fits exactly on its deadline.

Frame 2: Take B; the clock overflows; drop the longest.

```text
 push 4          time 5 -> 9     deadline 6   9 > 6
 heap [5, 4]  -> pop 5           time 9 -> 4
 heap [4]        count 1
```

Same count as before, but the plate now uses 4 days instead of 5.

Frame 3: Take C.

```text
 push 2          time 4 -> 6     deadline 6   ok
 heap [4, 2]     count 2
```

The 1 day saved in Frame 2 is exactly what lets C fit; with A kept, C would finish on day 7.

Frame 4: Take D; overflow; the longest is D itself.

```text
 push 6          time 6 -> 12    deadline 9   12 > 9
        6        stored negated: [-6, -2, -4]
       / \       (6 sifted up past 4 to the root)
      2   4
 heap [6, 4, 2] -> pop 6         time 12 -> 6
 heap [4, 2]     count 2
```

The new course was the worst choice, so it bounces straight back out.

Frame 5: Done.

```text
 final plate  [BBBB][CC]   time 6
 answer = len(heap) = 2
```

Across all frames, `time` equalled the sum of the heap, the plate was always schedulable in deadline order, and its size never decreased.

## Why it is correct

Two facts.

**Fact 1: the plate is always feasible.** Shown above: pushing a course that fits keeps it feasible, and after an overflow, popping the longest leaves a feasible plate. A useful consequence: *any subset of the plate is feasible too*, because removing courses from a deadline-ordered schedule only pulls the remaining ones earlier.

**Fact 2: the exchange argument.** Let `O` be any optimal set of courses, and suppose greedy and `O` disagree. Look at the first moment greedy evicts a course `L` that `O` contains. Say this happens while processing course `i`, with `k + 1` courses on the plate `P`.

- Every course greedy evicted *before* this moment is not in `O` (this is the first disagreement of this kind), so the courses of `O` among the first `i` all lie on `P`.
- `P` itself is infeasible, so `O` cannot contain all of `P`. Hence there is a course `s` on `P` that `O` skips, and `s` is no longer than `L`, because `L` is the longest on `P`.

Swap: `O' = O - L + s`. Its part among the first `i` courses is a subset of `P - L`, which is the plate greedy keeps, so it is feasible by Fact 1. Its total time among the first `i` is smaller or equal, because `len(s) <= len(L)`. The courses of `O` after `i` come later in deadline order, so they now start no later than before and still meet their deadlines. `O'` has the same size as `O`, so it is also optimal, and it agrees with greedy on one more eviction.

Repeat until greedy never evicts a course of the optimal set. Then every course of that optimal set survives on the final plate, so the plate is at least as large as the optimum. Since the plate is feasible, it is exactly optimal.

The plain-words version: when something must go, every candidate costs the same one unit of count, so evict the one that frees the most time. An optimal schedule that kept the longest course could always trade it for a shorter one it skipped and lose nothing.

## Cost

- **Time `O(n log n)`.** The sort is `O(n log n)`; each course does one push and at most one pop on a heap of size at most `n`.
- **Space `O(n)`.** The heap of taken durations.

The intermediate version, which finds the longest taken course by scanning a list, is `O(n^2)` time and `O(n)` space. Brute force is `O(2^n · n)`.

## Variations you will meet

- **Weighted courses (job scheduling with profits).** If each course has a value and you maximise total value instead of count, "drop the longest" stops being safe, because a long course might be worth a lot. That becomes a DP over sorted deadlines.
- **Unit-length jobs with deadlines and profits.** When every duration is 1, swap the rule: keep a *min*-heap of profits and, on overflow, drop the least profitable. Same skeleton, different "worst item".
- **Non-overlapping Intervals / Meeting Rooms II.** Courses there have fixed start times, so there is no freedom to slide them. Sorting by end time and a greedy count (or a heap of end times) replaces the "total time" state.
- **Minimise lateness instead of dropping.** If every course must be taken and you minimise the maximum lateness, plain deadline order (Earliest Deadline First) is optimal, by the same adjacent-swap argument used above.

## What to carry forward

Sort by the constraint, take greedily, and when the constraint breaks, evict the heap's worst item so the count is kept and the slack is maximised. The next problem, Maximum Performance of a Team, also sorts by the constraint first (efficiency), then uses a size-capped heap to evict the weakest teammate.
