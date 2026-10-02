# Daily Temperatures

*LeetCode 739 · Medium · Pattern: Monotonic stack · Reading time ~8 min*

## What the problem is really asking

You get a list of daily temperatures. For each day, report how many days you must wait until a strictly warmer day. If no warmer day ever comes, report 0.

The answer is an array of distances, one per day. Each entry is "distance to the next greater element on the right". That phrase, next greater element, is the single most common question a monotonic stack answers, and this problem is its cleanest form.

```text
temps (bar height = temp - 68):

                            #
              #             #
           #  #             #
        #  #  #             #  #
        #  #  #        #    #  #
        #  #  #  #     #    #  #
        #  #  #  #     #    #  #
        #  #  #  #  #  #    #  #
day:    0  1  2  3  4  5    6  7
temp:  73 74 75 71 69 72   76 73
ans:    1  1  4  2  1  1    0  0
```

Day 2 (75) has to wait until day 6 (76): four days. Day 6 is the hottest of all, so it waits forever: 0. What makes the problem interesting is that the obvious method looks at the same days over and over.

## Do it by hand first

Read the days left to right as if they were arriving one per morning. Keep a list on a sticky note of the days that are still waiting for a warmer day.

```text
morning 0 (73): note = [73]
morning 1 (74): 74 beats 73 -> day 0 answered (1)
                note = [74]
morning 2 (75): 75 beats 74 -> day 1 answered (1)
                note = [75]
morning 3 (71): beats nobody. note = [75, 71]
morning 4 (69): beats nobody. note = [75, 71, 69]
morning 5 (72): beats 69 and 71 -> answered
                stops at 75.   note = [75, 72]
```

Look at the sticky note. It is always sorted, warmest at the start, coolest at the end. That is not a coincidence: if a cooler day were followed on the note by a warmer one, the warmer one would have answered the cooler one the moment it arrived, and the cooler one would be gone. And when a new morning arrives, you only ever cross off from the end of the note, the coolest end, and you stop as soon as you hit someone warmer than today. Your hand was keeping a list of unresolved days, ordered, and touching only one end of it. That is a stack.

## The first honest attempt

For every day `i`, scan forward `j = i+1, i+2, ...` until `temps[j] > temps[i]`. Record `j - i`, or 0 if the scan runs off the end.

It is O(n^2) in the worst case, O(1) extra space. The worst case is a long cooling streak followed by one hot day: every day in the streak scans across all the later days of the streak before reaching the hot one.

```text
temps:  75 71 69 72 76
scan from 75:  71 69 72 76     (4 steps)
scan from 71:     69 72        (2 steps)
scan from 69:        72        (1 step)
                ~~ ~~
71 and 69 are walked over by the scan from 75
even though both are themselves still waiting
```

The waste is precise. The scan from 75 walks over 71 and 69, days that are themselves still waiting for something warmer. A day that is still waiting is cooler than everything after it up to its own answer, so it can never be the answer for a day that is warmer than it. The scan is inspecting candidates that have already been ruled out.

## The turning point

**Claim: flip the question. Instead of each day searching forward for its answer, let each new day announce itself as the answer for every earlier day that is still waiting and cooler than it.**

The days still waiting form a stack whose temperatures strictly decrease from bottom to top (for equal temperatures, non-increasing; equal is not warmer, so neither answers the other). When day `i` arrives:

1. While the top of the stack is cooler than `temps[i]`, pop it. Day `i` is its first warmer day, so its answer is `i - j`.
2. Stop at the first day that is at least as warm. Everything below it is warmer still, so nobody below can be answered by day `i` either.
3. Push `i`. It is now the coolest unresolved day, which keeps the stack sorted.

We store indices, not temperatures, because the answer is a distance. The temperature is a lookup away.

Picture the stack as a staircase going down from left to right. A new bar arrives at the right edge. Every step lower than it is flooded and removed, and each flooded step writes down its distance to the new bar. The new bar becomes the last step. That staircase is the picture to carry through the rest of this chapter.

## Watch it work

Same input. Each frame shows the array with the current day `i`, and beside it the stack drawn as a staircase: one row per stacked day, bottom of the stack first, bar length `temp - 68`.

Frame 1 — days 0 and 1.

```text
day:   0  1  2  3  4  5  6  7
temp: 73 74 75 71 69 72 76 73
          ^ i=1
pop d0 (73 < 74): ans[0] = 1-0 = 1
staircase:
  d1 74 |######        <- top
ans: [1, 0, 0, 0, 0, 0, 0, 0]
```

Day 1 is warmer than day 0, so day 0 leaves the stack with its answer fixed.

Frame 2 — day 2 arrives.

```text
day:   0  1  2  3  4  5  6  7
temp: 73 74 75 71 69 72 76 73
             ^ i=2
pop d1 (74 < 75): ans[1] = 1
staircase:
  d2 75 |#######       <- top
ans: [1, 1, 0, 0, 0, 0, 0, 0]
```

Frame 3 — days 3 and 4 are cooler; nothing pops.

```text
day:   0  1  2  3  4  5  6  7
temp: 73 74 75 71 69 72 76 73
                   ^ i=4
staircase:
  d2 75 |#######
  d3 71 |###
  d4 69 |#             <- top
```

A strictly descending staircase: three days all waiting.

Frame 4 — day 5 (72) floods the two lowest steps.

```text
day:   0  1  2  3  4  5  6  7
temp: 73 74 75 71 69 72 76 73
                      ^ i=5
pop d4 (69 < 72): ans[4] = 1
pop d3 (71 < 72): ans[3] = 2
stop at d2 (75 >= 72), push d5
staircase:
  d2 75 |#######
  d5 72 |####          <- top
ans: [1, 1, 0, 2, 1, 0, 0, 0]
```

Frame 5 — day 6 (76) floods everything.

```text
day:   0  1  2  3  4  5  6  7
temp: 73 74 75 71 69 72 76 73
                         ^ i=6
pop d5 (72 < 76): ans[5] = 1
pop d2 (75 < 76): ans[2] = 4
staircase:
  d6 76 |########      <- top
ans: [1, 1, 4, 2, 1, 1, 0, 0]
```

Frame 6 — day 7 (73) is cooler; the loop ends.

```text
staircase:
  d6 76 |########
  d7 73 |#####         <- top
ans: [1, 1, 4, 2, 1, 1, 0, 0]
```

Days 6 and 7 are never popped, so they keep their default 0.

Across all frames the staircase only went down from bottom to top, and a day's answer was written exactly once, at the moment it was popped. Every pop came from the top, and every day entered the stack exactly once.

## Why it is correct

Two facts carry the proof.

**The stack never gets warmer from bottom to top.** We only push `i` after popping everything cooler than `temps[i]`, so the day left beneath the new top is at least as warm as it. Equal temperatures do not pop each other, so ties can sit side by side; the order (non-increasing) never breaks.

**A popped element's answer is fixed at pop time, and it is right.** Suppose day `j` is popped by day `i`. We need `i` to be the first warmer day after `j`. Take any day `k` strictly between `j` and `i`. Day `k` was pushed after `j`, so when it arrived it sat above `j`. If `temps[k]` were greater than `temps[j]`, day `k` would have popped `j` when it arrived. It did not, since `j` was still there for `i` to pop. So every day between them is no warmer than `j`, and `i` is the first warmer day. The answer `i - j` is final; no later day can be an earlier warmer day.

**A day never popped has no warmer day.** If `j` is still on the stack at the end, every later day failed to pop it. A later day `k` might not have reached `j` because something above `j` blocked the loop — but anything above `j` is no warmer than `j`, so if `temps[k] > temps[j]` it would also have beaten every blocker and reached `j`. So no later day is warmer, and the default 0 is right.

## Cost

Time O(n): each index is pushed exactly once and popped at most once, so the inner `while` runs at most `n` times across the whole loop, not per day.

Space O(n): a strictly cooling input (90, 80, 70, ...) leaves every index on the stack.

The brute force is O(n^2) time, O(1) space.

## Variations you will meet

- **Next greater element in a circular array** (LeetCode 503, next in this chapter). The right neighbour of the last element is the first. Run the same loop twice over the array.
- **Previous greater / next smaller.** Scan right to left for "previous", flip the comparison for "smaller". The stack's direction flips too: for "next smaller" it is increasing.
- **Stock span** (LeetCode 901). For each price, how many consecutive days back were priced at most today? That is distance to the previous greater element; keep a decreasing stack and read the answer off the new top after popping.
- **Constant extra space** by jumping: walk right to left and, for day `i`, hop `j = i+1`, then `j += ans[j]` until warmer. Same O(n) amortised, no stack, but harder to explain.

## What to carry forward

The waiting days form a descending staircase; a newcomer floods every lower step and each flooded step learns its answer at that instant. That "answer fixed at pop time" argument is the proof you will reuse for every remaining problem in this chapter.

The next problem keeps the same staircase but bends the array into a circle, so some days only find their answer on a second lap.
