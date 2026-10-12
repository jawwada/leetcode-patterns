# Moving Average from Data Stream

*LeetCode 346 · Easy · Pattern: Sliding window queue with running sum · Reading time ~5 min*

## The problem

Implement MovingAverage(size) with next(val) -> the average of the last size values seen so far, or of all values
while fewer than size have arrived.

```text
Example: size 3; next(1) -> 1.0; next(10) -> 5.5; next(3) ->
  4.667; next(5) -> 6.0 (= (10 + 3 + 5) / 3).
```

## What the problem is really asking

You build an object that is told a window size once, then receives numbers one at a time through `next(val)`. After each number it must report the average of the most recent `size` numbers — or of all numbers so far, if fewer than `size` have arrived. The answer to each call is a single float, but the object answering it lives across many calls, so the real deliverable is the *state* it keeps.

What makes it hard: the stream is unbounded, so you cannot touch `size` numbers per call or keep everything.

```text
 size = 3
 stream:  1   10   3   5   8
 next(5): window is the last 3 seen -> [10, 3, 5]
          average = 18 / 3 = 6.0
```

## Do it by hand first

Take size 3 and the stream 1, 10, 3, 5. On paper you would write the numbers in a row and put a bracket over the last three. When 5 arrives you do not re-add 10 + 3; you remember that the previous bracket summed to 14, cross out the 1 that fell out, and add the 5.

```text
 [1 10 3]          sum 14
    [10 3 5]       14 - 1 + 5 = 18
     ^ out  ^ in
```

Your hand kept track of two things: the running sum of what is under the bracket, and which number is the oldest under the bracket (so you know what to subtract next). That is the whole data structure: a sum, and a queue that knows its oldest element.

## The first honest attempt

Append every value to a list. On each call, slice the last `size` values, sum them, and divide by the slice length. It costs O(size) per call, and O(n) memory for a stream of n values.

The waste is visible if you line up two consecutive calls:

```text
 call 4 sums:  10 + 3 + 5        (3 additions)
 call 5 sums:       3 + 5 + 8    (3 additions)
                    ^^^^^ added again
 window of 1000 -> 999 numbers re-added every call
```

Consecutive windows share all but two elements, and the brute force re-adds every shared one. It also keeps every value forever, though a value that has slid out of the window can never affect another answer.

## The turning point

**Claim: the next window's sum is the previous sum plus the new value minus the value that just left.**

Justification: the window after the call contains exactly the elements of the window before, minus the oldest one (if the window was full), plus the new one. Sums are additive, so the sum changes by exactly those two numbers.

That claim needs two pieces of state. A running `total` holds the sum. And we need the identity of the oldest value at the moment it leaves — that is exactly what a queue gives: push at the back when a value arrives, pop from the front when the window overflows. A `deque` does both in O(1).

This is the chapter's core habit: store only what a future answer can depend on. Here that is the values still in the window, so the deque holds at most `size` of them.

One detail: during warm-up, when fewer than `size` values have arrived, the divisor is the current queue length, not `size`.

## Watch it work

Size 3, stream 1, 10, 3, 5, 8. The deque is drawn front (oldest) on the left.

```text
Frame 1  next(1)
 window: [1]             total = 1    len 1
 return 1/1 = 1.0
```
First value: append, add, no overflow, divide by 1.

```text
Frame 2  next(10)
 window: [1, 10]         total = 11   len 2
 return 11/2 = 5.5
```
Still warming up, so the divisor is 2, not 3.

```text
Frame 3  next(3)
 window: [1, 10, 3]      total = 14   len 3
 return 14/3 = 4.667
```
The window is now exactly full.

```text
Frame 4  next(5)
 append:   [1, 10, 3, 5] total = 19   len 4 > 3
 popleft:  1 leaves
 window:   [10, 3, 5]    total = 18
 return 18/3 = 6.0
```
First overflow: the oldest value is popped and subtracted.

```text
Frame 5  next(8)
 append:   [10, 3, 5, 8] total = 26
 popleft:  10 leaves
 window:   [3, 5, 8]     total = 16
 return 16/3 = 5.333
```
Same move again: one in, one out, two arithmetic operations.

Across every frame, `total` equals the sum of the deque and the deque holds the last `min(size, calls)` values in arrival order. The work per frame never depended on `size`.

## Why it is correct

The invariant, true after every call: the deque contains the last `min(size, k)` values in order, where k is the number of calls so far, and `total` equals their sum. Initially both are empty and zero. A call appends the new value and adds it to `total`, so the invariant holds for k + 1 values with no cap. If that makes the deque longer than `size`, the front is the oldest value, which is precisely the one that no longer belongs; popping it and subtracting it restores the cap. Then `total / len(window)` is by definition the average of the right values.

## Cost

- **Time:** O(1) per call — one append, at most one pop, one addition, one subtraction, one division.
- **Space:** O(size) — the deque never holds more than `size` values plus one transiently.

## Variations you will meet

- **Exponential moving average.** No window at all: `avg = alpha * val + (1 - alpha) * avg`. The state shrinks to one float, because the definition already compresses the past.
- **Moving median or max of the window.** A running sum cannot be "un-maxed". Max needs a monotonic deque; median needs two heaps with lazy deletion. Same window, different aggregate, much harder state.
- **Fixed array ring buffer.** Replace the deque with an array of `size` slots and a write index `i % size`; the value being overwritten is the one leaving. Same cost, no allocation.

## What to carry forward

A sliding aggregate is updated by what enters and what leaves, never recomputed; the queue exists only to tell you what leaves. The next problem keeps the stream but keys it by message, so the state becomes one hash map value per key instead of one queue.
