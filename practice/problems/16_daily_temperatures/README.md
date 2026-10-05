# Daily Temperatures (LeetCode 739)

**Area:** monotonic stack · **Difficulty:** Medium · **Key operations:** push index, pop while top is colder, answer = i - popped index

## Problem

Given a list of daily temperatures, return a list `answer` where `answer[i]` is the number of days you have to wait after day `i` for a warmer temperature. If no warmer day comes, `answer[i] = 0`.

## Example

```
temps  = [73, 74, 75, 71, 69, 72, 76, 73]
answer = [ 1,  1,  4,  2,  1,  1,  0,  0]
```

Day 2 (75) waits 4 days for day 6 (76). Days 6 and 7 never see anything warmer.

## Brute force

For every day `i`, scan forward until you meet a temperature greater than `temps[i]`. Record the distance, or 0 if the scan runs off the end.

O(n²) time, O(1) extra space. The wasted work: the cold stretch 71, 69 is rescanned by day 2, then again by day 3, and the long plateau before a hot day is walked once per earlier day.

## From brute force to optimal

Flip the question. Instead of each day looking forward for its answer, let each new day look back and *resolve* the days that were waiting for it. Which earlier days does day `i` resolve? Exactly the waiting days colder than `temps[i]`. And once a day is resolved it never matters again, so it can be thrown away.

Keep the waiting days on a stack. A new day pops every waiting day colder than itself (those are resolved now), then joins the stack as a waiting day. Because a day only stays on the stack if it is at least as warm as everything pushed after it, the stack is always decreasing from bottom to top. Each index is pushed once and popped at most once, so the whole pass is O(n).

## Intuition

Picture the waiting days as a line of people holding up their temperature. When a new day arrives, it walks up to the end of the line and sends home everyone colder than itself, telling each how many days they waited. The people still in line are all at least as warm as the newcomer, so the line reads hottest at the front, coolest at the back. The newcomer joins the back. Nobody is ever looked at twice after being sent home, which is where the speed comes from.

## Walkthrough

Stack shown top first (the top is the right end of the Python list). `a` is the answer array.

```
day 0, 73   stack []            -> push 0        stack [0]            a [0,0,0,0,0,0,0,0]
day 1, 74   top 73 < 74 pop 0   a[0] = 1-0 = 1   stack []
            push 1                               stack [1]            a [1,0,0,0,0,0,0,0]
day 2, 75   top 74 < 75 pop 1   a[1] = 2-1 = 1   stack []
            push 2                               stack [2]            a [1,1,0,0,0,0,0,0]
day 3, 71   top 75 not < 71     push 3           stack [2,3]          a [1,1,0,0,0,0,0,0]
day 4, 69   top 71 not < 69     push 4           stack [2,3,4]        a [1,1,0,0,0,0,0,0]
day 5, 72   top 69 < 72 pop 4   a[4] = 5-4 = 1   stack [2,3]
            top 71 < 72 pop 3   a[3] = 5-3 = 2   stack [2]
            top 75 not < 72     push 5           stack [2,5]          a [1,1,0,2,1,0,0,0]
day 6, 76   top 72 < 76 pop 5   a[5] = 6-5 = 1   stack [2]
            top 75 < 76 pop 2   a[2] = 6-2 = 4   stack []
            push 6                               stack [6]            a [1,1,4,2,1,1,0,0]
day 7, 73   top 76 not < 73     push 7           stack [6,7]          a [1,1,4,2,1,1,0,0]
end: days 6 and 7 still waiting -> stay 0
```

The stack read bottom to top is always decreasing: `[2,3,4]` is 75, 71, 69.

## Steps

1. `answer = [0] * n`, `waiting = []` (indices).
2. For each day `i` with temperature `t`:
3. While the stack is non-empty and the top's temperature is **strictly less** than `t`: pop `j`, set `answer[j] = i - j`.
4. Push `i`.
5. Return `answer`. Whatever is left on the stack keeps 0.

## Complexity

O(n) time: every index is pushed once and popped at most once. O(n) space for the stack in the worst case (a decreasing sequence).

## Pitfalls

- **`<=` instead of `<`.** Equal is not warmer. With `<=`, `[5, 5, 5]` returns `[1, 1, 0]` instead of `[0, 0, 0]`.
- **Off by one in the wait.** The wait is exactly `i - j`. Writing `i - j - 1` makes two consecutive warmer days report 0.
- **Pushing to the wrong end.** `insert(0, i)` puts the newest day at the bottom, so the next comparison looks at the oldest waiting day and waits are attributed to the wrong days. The top is `waiting[-1]`.
- **Storing temperatures instead of indices.** You need the index to compute the distance; the temperature is a lookup away.
- **Forgetting the leftovers.** Days still on the stack at the end have no warmer day. The initial zeros handle this, so do not "fix" them.
