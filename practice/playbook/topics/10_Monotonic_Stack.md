## Monotonic Stack

> Keep a stack of the items that are still **waiting** for their answer. Each new item looks at the top: if it beats that item, the waiting item has just found its answer (pop it and record), and the newcomer looks at the next one down. Then the newcomer waits too. Beaten items leave, so the waiting values are always in sorted order: that is the "monotonic".

This section continues [Stacks & Queues](00_Topic_Index.ipynb#s07) with one change. There, a closer or an operator popped the one entry it finished. Here a newcomer may finish several waiting items in a row, and the comparison that pops them keeps the waiting items sorted.

**Reach for it when** the problem asks, for every element, about the **nearest** element to its left or right that is **bigger or smaller**: the next warmer day, the next greater element, the previous smaller one, how far a bar can stretch, a stock's span. The same stack answers questions about the minimum or maximum of **every subarray**, and it builds the **smallest or largest sequence** when digits or letters may be deleted but their order must be kept.

**In this repo:** `stack/` (6 of its 16 problems: daily temperatures, next greater II, the two rectangle problems, car fleet, create maximum number) · bank: `practice/simple/16_daily_temperatures.py`, `practice/simple/17_largest_rectangle_in_histogram.py` · basics in `practice/simple/basics/monotonic_stacks/`: `01_next_greater_element.py`, `02_previous_smaller_element.py`, `03_online_stock_span.py`, `04_sum_of_subarray_minimums.py`, `05_remove_k_digits.py`

### The picture

```text
temps   73  74  75  71  69  72  76  73       question: how many days until a warmer day?
day      0   1   2   3   4   5   6   7

the days still waiting, just before day 5:   day 5 (72) arrives and looks at the top:

    #                                          69 < 72: pop day 4, it waited 5 - 4 = 1 day
    #   #                                      71 < 72: pop day 3, it waited 5 - 3 = 2 days
    #   #   #                                  75 > 72: stop, day 2 keeps waiting
   75  71  69                                  push day 5: the waiting temps are now 75 72
   d2  d3  d4
```

The waiting days always form a staircase that never steps up. A newcomer knocks down every step shorter than itself, and each knocked-down step has found its warmer day; then the newcomer becomes the new last step.

**Why it is fast:** the brute force scans forward from every day: O(n²). On a falling stretch like 75 71 69, the scan from 75 walks over 71 and 69, which are *themselves still waiting* for a warmer day, so neither can be 75's answer. The stack flips the question: instead of each day searching forward for its answer, each new day announces itself as the answer to every waiting day it beats. Every index is pushed once and popped at most once, so the whole pass is O(n), even with a `while` inside the `for`.

**Why it is correct:** when day `i` pops day `j`, `j` was still waiting, so no day between them was warmer than `j` (it would have popped `j` first). So `i` is the *first* warmer day after `j`, which is exactly the answer. A day that is never popped never met a warmer day.

### From idea to code

**The idea in one sentence:** *for each new item: while it beats the item on top of the stack, that item is resolved (pop it, record its answer); then push the new item, which now waits for its own answer.*

The **State** is a stack of **indices** of the items still waiting for their answer, and its **Definition** goes in a comment: `stack` holds the days whose warmer day has not come yet, temperatures never rising from bottom to top. It holds indices, not values, because the answer is written into `ans[j]` and is often a distance, `i - j`.

The **Invariant** has three parts. Every index left of `i` that is *not* on the stack already has its answer; the values on the stack are sorted; and every day between a waiting day `j` and today was no warmer than `j`, or it would have popped `j`. A **Step** pushes the newcomer, `stack.append(i)`, so that it waits for its own answer.

Before the step comes the **Fix**, `while stack and temps[stack[-1]] < t:`, which pops every waiting item the newcomer beats: a *next* question resolves them, a *previous* question discards them. **Record** at the pop for a *next* question, `ans[j] = i - j`, or `ans[j] = t` when the value is wanted, because the popped index has just met its answer. For a *previous* question, record after the fix and before the step, because the survivor on top is the answer for `i`.

**Init** is `ans = [0] * n` or `[-1] * n`, whichever means "never", and `stack = []`; sometimes a sentinel item at the end, such as `heights + [0]`, flushes whatever still waits. **Return** `ans`, where the indices never popped keep the default, or the best value recorded at the pops.

Which comparison pops is derived from the question instead of memorised. A *next* question pops while the newcomer *is* the top's answer, with the problem's own comparison: "strictly greater" pops while `top < x`, "greater or equal" while `top <= x`. A *previous* question pops while the top *cannot be* the newcomer's answer, which is the negation: for "strictly smaller", pop while `top >= x`, then read the top.

So next greater pops while the top is `< x`, and the waiting values never rise from bottom to top; next smaller pops while `> x`, and they never fall. Previous greater pops while `<= x` and then reads the top, on a stack that strictly falls; previous smaller pops while `>= x`, on a stack that strictly rises.

Each pop gives two facts at once: the popped item's next answer is the newcomer, and after the loop the top is the newcomer's previous answer, with the opposite strictness. Largest Rectangle, in Watch it work, uses both.

Two templates follow, one per kind of question. Daily Temperatures (739) asks, for each day, how many days until a warmer one, 0 if none ever comes: `[73, 74, 75, 71, 69, 72, 76, 73] → [1, 1, 4, 2, 1, 1, 0, 0]`. It is a *next* question, so the answer is written at the pop. FIX runs before STEP: pushed first, the newcomer would sit on top and block every comparison ([From Idea to Code](02_Idea_to_Code.ipynb#topic-idea-to-code) runs this swap).

Previous Smaller Element asks, for each item, for the nearest smaller value on its left, -1 if there is none: `[3, 1, 4, 1, 5] → [-1, -1, 1, -1, 1]`. It is a *previous* question, so the pops only discard: an item at least as big as `x` can never answer anyone again, because `x` is nearer and no bigger. After the loop the answer is `nums[stack[-1]] if stack else -1`, and then `x` waits.

<!-- cell -->

```python
def daily_temperatures(temps):
    ans = [0] * len(temps)                   # INIT: 0 = "no warmer day ever comes"
    stack = []                               # STATE: days still waiting; temps never rise bottom -> top
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:    # FIX: today beats the latest waiting day
            j = stack.pop()
            ans[j] = i - j                   # RECORD: j is resolved; i is its FIRST warmer day
        stack.append(i)                      # STEP: today waits for its own warmer day
    return ans                               # RETURN: never resolved -> stays 0


def previous_smaller(nums):
    ans, stack = [], []                      # STATE + INIT: indices; values strictly rise bottom -> top
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] >= x:    # FIX: not smaller than x, and x is nearer: useless now
            stack.pop()
        ans.append(nums[stack[-1]] if stack else -1)   # RECORD: the survivor on top is the answer
        stack.append(i)                      # STEP: x may answer later items
    return ans                               # RETURN


print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))   # [1, 1, 4, 2, 1, 1, 0, 0]
print(previous_smaller([3, 1, 4, 1, 5]))                      # [-1, -1, 1, -1, 1]
```

<!-- cell -->

**Try it**
- Use the rule to turn `previous_smaller` into *previous greater* (pop while `nums[stack[-1]] <= x`) and predict `[3, 1, 4, 1, 5]` before running: `[-1, 3, -1, 4, -1]`.
- Push the temperature instead of the index (`stack.append(t)`) and run the first example: `IndexError`, because the stack's entries are used as positions.
- Print `stack` right before the `return` for the first example: `[6, 7]`, the two days that never got a warmer day.
- In `previous_smaller`, change `>=` to `>` and run `previous_smaller([2, 2])`: `[-1, 2]` instead of `[-1, -1]`. An equal value is not smaller.

<!-- cell -->

### Watch it work

The richest use of the loop is Largest Rectangle in Histogram (84). It asks for the largest rectangle inside a bar chart of width-1 bars: `[2, 1, 5, 6, 2, 3]` gives 10, height 5 across the bars of heights 5 and 6. The best rectangle of one bar has that bar's height and stretches until the first shorter bar on each side, so each bar needs its *previous smaller* and its *next smaller* bar, and one pop delivers both.

Bars pop when a bar that is not taller arrives, `>=`, so the newcomer is the popped bar's right wall. The bar under it on the stack is its left wall: its previous smaller bar, or -1, an imaginary wall before the array. The rectangle spans the bars strictly between the walls, and a final bar of height 0 pops whatever still waits. The trace prints every pop, then the heights still waiting after each step.

<!-- cell -->

```python
def trace_rectangle(heights):
    bars, stack, best = heights + [0], [], 0
    for i, h in enumerate(bars):
        while stack and bars[stack[-1]] >= h:
            j = stack.pop()
            left = stack[-1] if stack else -1
            area = bars[j] * (i - left - 1)
            best = max(best, area)
            print(f"  bar {i} (h={h}) pops bar {j} (h={bars[j]}): walls {left} and {i}, width {i - left - 1}, area {area}")
        stack.append(i)
        print(f"i={i} h={h}  stack heights: {[bars[k] for k in stack]}")
    return best


print(trace_rectangle([2, 1, 5, 6, 2, 3]))   # 10
```

<!-- cell -->

**Try it**
- Find the line that gives 10: bar 4 pops bar 2 (height 5), walls 1 and 4, width 2.
- Run `trace_rectangle([3, 3, 3])`: equal bars pop each other with widths 1 and 2 (under-measured), and only the last one gets width 3 (area 9). Harmless, which is why `>` and `>=` give the same answer.
- Run `trace_rectangle([1, 2, 3])`: nothing pops until the height-0 bar arrives, then all three pop at `i = 3`, and the best is 4.

<!-- cell -->

### Where it goes wrong

1. **Storing values instead of indices.** You lose the position, so there is no way to write `ans[j]` or compute `i - j`: pushing temperatures makes `daily_temperatures([73, 74])` read `temps[73]`, an `IndexError`. Push `i`; read the value as `nums[stack[-1]]`.
2. **`<` vs `<=` when popping.** "Strictly warmer" pops on `<`. Popping on `<=` lets an equal temperature answer: `[70, 70, 71]` would give `[1, 1, 0]` instead of `[2, 1, 0]`.
3. **Recording in the wrong place.** *Next* answers are written for the **popped** index, at the pop. *Previous* answers are written for the **current** index, after the loop. Mixing them up gives answers to the wrong items: writing `ans[i] = i - j` at the pop turns `[73, 74]` into `[0, 1]` instead of `[1, 0]`.
4. **Forgetting the leftovers.** Items still on the stack at the end were never resolved. They need the default (`-1`, `0`), or, in the histogram, a final bar of height 0 so they get measured: `[1, 2, 3]` must give 4, but without the flush nothing is ever popped and you get 0.
5. **Width off by one.** When bar `j` pops at `i` and `left` is the index under it, the bars strictly between the walls number `i - left - 1`, not `i - left`. With `i - left`, `[2, 1, 5, 6, 2, 3]` gives 15 instead of 10.
6. **Counting ties twice.** In Sum of Subarray Minimums, which adds up the minimum of every subarray, `[2, 2]` has two equal minimums, and the subarray `[2, 2]` must be credited to exactly one of them: one wall strict, the other not. A single stack pass does this by itself; computing the left and right walls in two separate passes with the same comparison gives 8 or 4 instead of 6.
7. **Leftover deletions.** When you delete k digits to make the smallest number, digits that never fall (`"12345"`, k = 2) pop nothing, so cut the last k digits at the end. Then strip leading zeros, and return `"0"` if nothing is left (`"10"`, k = 2).

### Edge cases to say out loud

Empty input · one item · all equal (nothing is strictly greater) · strictly rising (everything resolves at once) · strictly falling (nothing resolves; everything is left at the end) · ties. And one habit worth more than any list: check the fast version against a brute force on many small random inputs.

<!-- cell -->

```python
assert daily_temperatures([]) == []
assert daily_temperatures([50]) == [0]
assert daily_temperatures([70, 70, 70]) == [0, 0, 0]        # equal is not warmer
assert daily_temperatures([30, 40, 50]) == [1, 1, 0]        # each one resolved at once
assert daily_temperatures([50, 40, 30]) == [0, 0, 0]        # nobody is ever resolved
assert previous_smaller([]) == []
assert previous_smaller([2, 2]) == [-1, -1]                 # equal is not smaller
assert previous_smaller([1, 2, 3]) == [-1, 1, 2]


def brute_daily(temps):                      # O(n²) reference: scan forward from every day
    return [next((j - i for j in range(i + 1, len(temps)) if temps[j] > temps[i]), 0)
            for i in range(len(temps))]


random.seed(0)
for _ in range(300):                         # small random inputs, full of ties
    T = [random.randint(30, 35) for _ in range(random.randint(0, 9))]
    assert daily_temperatures(T) == brute_daily(T), T
print("edge cases pass")
```

<!-- cell -->

**Try it**
- Predict `previous_smaller([5, 4, 3])` and `previous_smaller([1, 3, 2])` before running: `[-1, -1, -1]` and `[-1, 1, 1]`.
- Break `daily_temperatures` on purpose (pop on `<=`) and rerun this cell: the `[70, 70, 70]` assert fails first. Delete that assert and rerun: the random check fails too, and its message shows the input it failed on.
- Add `assert daily_temperatures([50] * 100_000) == [0] * 100_000`: it runs instantly. Every index is pushed once and never popped.

<!-- cell -->

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Next greater value** | record `ans[j] = x` instead of the distance | Next Greater Element I (496): the next greater value of each item of a subset, looked up in the full array |
| **Next greater in a linked list** | copy the values into a list, then run the template | Next Greater Node In Linked List (1019) |
| **Circular array** | walk `2n` steps with `i % n`; push only during the first lap | Next Greater Element II (503): the array wraps around |
| **Previous smaller / greater** | pop the useless items, then read the top for the current item | Largest Rectangle in Histogram (84); Online Stock Span (901): how many days in a row up to today had a price at most today's |
| **Span, online** | store `(price, span)`; a popped day's span is absorbed into today's | Online Stock Span (901) |
| **Sort first, then stack** | sort by position; a car whose solo arrival time is later than the fleet ahead's starts a new fleet | Car Fleet (853): how many groups of cars reach the target |
| **Greedy smallest / largest sequence** | pop while the top is worse than `x` *and* you can still afford to drop it | Remove K Digits (402): the smallest number after k deletions; Smallest Subsequence of Distinct Characters (1081): each letter once, smallest order |
| **Both walls at once** | rising stack: when `j` pops at `i`, `i` is its right wall and the new top its left wall | Largest Rectangle in Histogram (84); Trapping Rain Water (42), the water held between bars, has a stack version too, but is taught in [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers) |
| **Contribution counting** | `nums[j]` is the minimum of `(j - left) * (i - j)` subarrays | Sum of Subarray Minimums (907); Sum of Subarray Ranges (2104), the total of max − min over all subarrays, is 907 twice |
| **Both walls + prefix sums** | each minimum's walls bound the widest subarray it rules; its sum comes from prefix sums | Maximum Subarray Min-Product (1856): the best minimum × sum over all subarrays |
| **Scan from the right** | walk right to left; the last value popped is the best "2" | 132 Pattern (456): is there `i < j < k` with `nums[i] < nums[k] < nums[j]`? |
| **Candidates, then a second scan** | keep a falling stack of left candidates, then match them from the right | Maximum Width Ramp (962): the widest `i < j` with `nums[i] <= nums[j]` |
| **Monotonic deque** | this stack plus expiry from the front: the window maximum | Sliding Window Maximum (239), in [Sliding Window](07_Sliding_Window.ipynb#topic-sliding-window) |
| *Second pass:* **Rows into histograms** | each row of a binary matrix becomes a histogram of the 1s standing on it; run Largest Rectangle per row | Maximal Rectangle (85): the largest rectangle of 1s in a binary matrix |
| *Second pass:* **Largest sequence from two arrays** | keep the largest t digits of each array with the mirror-image stack; try every split of k; merge by comparing remaining tails | Create Maximum Number (321): the largest k-digit number from two digit arrays, each keeping its order |

The first variation changes only the input. Next Greater Element II (503) asks for the next greater value of every item in a circular array, where the first item follows the last, -1 if there is none: `[1, 2, 1] → [2, -1, 2]`. Walk the array twice: the second lap lets the items at the start answer the items still waiting at the end. Only the first lap pushes, so each index waits once.

<!-- cell -->

```python
def next_greater_circular(nums):
    n = len(nums)
    ans, stack = [-1] * n, []                # STATE + INIT: indices still waiting; -1 = "never"
    for i in range(2 * n):                   # two laps around the circle
        x = nums[i % n]
        while stack and nums[stack[-1]] < x: # FIX: x answers every smaller waiting item
            ans[stack.pop()] = x             # RECORD
        if i < n:
            stack.append(i)                  # STEP: only the first lap creates waiting items
    return ans                               # RETURN


print(next_greater_circular([1, 2, 1]), next_greater_circular([1, 2, 3, 4, 3]))   # [2, -1, 2] [2, 3, 4, -1, 4]
```

<!-- cell -->

**Try it**
- Delete `if i < n:` so the second lap pushes too: `IndexError`, since `i` (not `i % n`) is then used as a position past the end of `nums`.
- Walk one lap only (`range(n)`) and run `[1, 2, 1]`: `[2, -1, -1]`. The last 1 never sees the 2 at the front.
- Predict `[5, 4, 3, 2, 1]` and `[3, 3, 3]` before running: `[-1, 5, 5, 5, 5]` and `[-1, -1, -1]`.

<!-- cell -->

The *previous* question comes next, asked online, so the stack lives between calls. Online Stock Span (901) gets one price per call and returns how many consecutive days, ending today, had a price at most today's: prices 100, 80, 60, 70, 60, 75, 85 give 1, 1, 1, 2, 1, 4, 6. A day that today beats lies inside today's span, and so does every day it had already absorbed, so the stack stores `(price, span)` pairs and today adds up the spans it pops.

Car Fleet (853) sits at the other extreme: a monotonic stack that never pops. Cars drive toward a target, a car that catches a slower one slows down and joins its fleet, and the question is how many fleets arrive: target 12, positions `[10, 8, 0, 5, 3]`, speeds `[2, 4, 1, 1, 3]` → 3. Sort by position and walk from the car closest to the target, comparing *solo arrival times*, not speeds.

A car whose time is later than the fleet ahead's can never catch it and leads a new fleet; one that would arrive at the same time or sooner catches up and merges. The times on the stack only rise, which is why nothing pops: the stack is really a running maximum.

<!-- cell -->

```python
class StockSpanner:                          # 901
    def __init__(self):
        self.stack = []                      # STATE + INIT: (price, span); prices strictly fall bottom -> top

    def next(self, price):
        span = 1                             # today itself
        while self.stack and self.stack[-1][0] <= price:   # FIX: absorb every day today beats
            span += self.stack.pop()[1]      # ... and every day that day had covered
        self.stack.append((price, span))     # STEP
        return span                          # RECORD + RETURN


def car_fleet(target, position, speed):      # 853
    cars = sorted(zip(position, speed), reverse=True)   # INIT: closest to the target first
    times = []                               # STATE: arrival times of the fleets, front fleet first
    for pos, spd in cars:
        t = (target - pos) / spd             # this car's solo arrival time
        if not times or t > times[-1]:       # arrives later than the fleet ahead: a new fleet
            times.append(t)                  # STEP (otherwise it catches up and merges)
    return len(times)                        # RETURN


spanner = StockSpanner()
print([spanner.next(p) for p in [100, 80, 60, 70, 60, 75, 85]])   # [1, 1, 1, 2, 1, 4, 6]
print(car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))           # 3
```

<!-- cell -->

**Try it**
- Change `<=` to `<` in `next` and replay `[60, 60, 60]` on a fresh spanner: `[1, 1, 1]` instead of `[1, 2, 3]`.
- Count each popped day as 1 (`span += 1`) instead of adding its span, and replay the main prices: `[1, 1, 1, 2, 1, 3, 3]`. The 75 loses the day that the 70 had absorbed, and the 85 gets 3 instead of 6.
- In `car_fleet`, drop `reverse=True` and rerun: 1 instead of 3. Each car now compares itself with a car *behind* it.
- Run `car_fleet(10, [0, 5], [2, 1])`: 1, because both cars reach the target at t = 5 and arrive together. With `t >= times[-1]` it would say 2.

<!-- cell -->

The stack can also *build* an answer instead of answering questions. Remove K Digits (402) asks for the smallest number left after deleting k digits from a number string: `"1432219"`, k = 3 → `"1219"`. The leftmost digits matter most, so a digit sitting right before a smaller one should go, because deleting it slides the smaller digit into a more important place. The kept digits should therefore never fall: pop while the top is bigger than the newcomer and deletions are left.

Smallest Subsequence of Distinct Characters (1081), the same problem as Remove Duplicate Letters (316), keeps every distinct letter exactly once and wants the smallest such string: `"cbacdcbc"` → `"acdb"`. It swaps the budget for a different test: a bigger letter on top is dropped only if it appears again later.

<!-- cell -->

```python
def remove_k_digits(num, k):
    stack = []                               # STATE + INIT: kept digits, never falling
    for d in num:
        while k and stack and stack[-1] > d: # FIX: a bigger digit before a smaller one: drop it
            stack.pop()
            k -= 1
        stack.append(d)                      # STEP
    stack = stack[:len(stack) - k]           # deletions left over come off the tail
    return "".join(stack).lstrip("0") or "0" # RETURN


def smallest_subsequence(s):                 # every distinct letter exactly once
    last = {c: i for i, c in enumerate(s)}   # the last position of each letter
    stack, used = [], set()
    for i, c in enumerate(s):
        if c in used:
            continue
        while stack and stack[-1] > c and last[stack[-1]] > i:   # FIX: it comes back later: drop it
            used.remove(stack.pop())
        stack.append(c)                      # STEP
        used.add(c)
    return "".join(stack)


print(remove_k_digits("1432219", 3), remove_k_digits("10200", 1), remove_k_digits("10", 2))   # 1219 200 0
print(smallest_subsequence("bcabc"), smallest_subsequence("cbacdcbc"))                      # abc acdb
```

<!-- cell -->

**Try it**
- Delete the line that trims leftover deletions and run `remove_k_digits("12345", 2)`: `12345` instead of `123`.
- Drop `or "0"` and run `remove_k_digits("10", 2)`: an empty string instead of `0`.
- In `smallest_subsequence`, delete `and last[stack[-1]] > i` and run `"cbacdcbc"`: `abc`. The `d` was dropped although it never comes back.
- Print `stack` after every digit of `"1432219"` with k = 3: the 4, the 3 and one 2 are popped, each by the smaller digit right after it, and `['1', '2', '1', '9']` is left.

<!-- cell -->

Both walls at once come next, in the loop traced in Watch it work, without the prints. Bar `j`'s best rectangle has its own height and stretches until the first shorter bar on each side, and the pop delivers both walls: `i` on the right, the new top on the left. `[2, 1, 5, 6, 2, 3]` gives 10, and `[2, 4]` gives 4, from the bar of height 4 alone or from both bars at height 2.

<!-- cell -->

```python
def largest_rectangle(heights):
    bars = heights + [0]                     # a height-0 bar resolves everything at the end
    stack, best = [], 0                      # STATE + INIT: indices; heights rise bottom -> top
    for i, h in enumerate(bars):
        while stack and bars[stack[-1]] >= h:    # FIX: the top can't stretch past i
            height = bars[stack.pop()]
            left = stack[-1] if stack else -1    # its left wall: the nearest shorter bar
            best = max(best, height * (i - left - 1))   # RECORD: bars strictly between the walls
        stack.append(i)                      # STEP
    return best                              # RETURN


print(largest_rectangle([2, 1, 5, 6, 2, 3]), largest_rectangle([2, 4]))   # 10 4
```

<!-- cell -->

**Try it**
- Drop the sentinel (`bars = heights`) and run `largest_rectangle([1, 2, 3])`: 0 instead of 4. The heights only rose, so no bar was ever popped and measured.
- Change the width to `i - left` and run `[2, 1, 5, 6, 2, 3]` again: 15 instead of 10. Every rectangle now counts one bar too many (height 5 gets width 3).
- Predict `largest_rectangle([6, 2, 5, 4, 5, 1, 6])` before running: 12, height 4 across the three bars 5, 4 and 5. Print `(height, i - left - 1)` at each pop to see which pop finds it.

<!-- cell -->

Counting with both walls closes the main path. Sum of Subarray Minimums (907) asks for the sum of `min(sub)` over every contiguous subarray, modulo 10⁹ + 7: `[3, 1, 2, 4]` → 17. Turn the sum around: instead of finding the minimum of every subarray, ask for every element *how many subarrays it is the minimum of*.

With its walls at `left` and `i`, the nearest smaller items on each side, `nums[j]` is the minimum of every subarray that starts in `left+1 .. j` and ends in `j .. i-1`: that is `(j - left) * (i - j)` subarrays. The histogram's pop hands you both walls, and making one wall strict and the other not counts a tie exactly once.

<!-- cell -->

```python
def sum_subarray_mins(nums):
    vals = nums + [-math.inf]                # sentinel: smaller than everything, pops all
    stack, total = [], 0                     # STATE + INIT: indices; values rise bottom -> top
    for i, x in enumerate(vals):
        while stack and vals[stack[-1]] >= x:    # FIX
            j = stack.pop()                  # i = right wall: the first value <= vals[j]
            left = stack[-1] if stack else -1    # left wall: the last value < vals[j]
            total += vals[j] * (j - left) * (i - j)   # RECORD: vals[j] is the min of that many subarrays
        stack.append(i)                      # STEP
    return total % (10**9 + 7)               # RETURN


print(sum_subarray_mins([3, 1, 2, 4]), sum_subarray_mins([11, 81, 94, 43, 3]), sum_subarray_mins([2, 2]))   # 17 444 6
```

<!-- cell -->

**Try it**
- Check it against the brute force: with `nums = [3, 1, 2, 4]`, `sum(min(nums[i:j]) for i in range(4) for j in range(i + 1, 5))` is also 17.
- Print `(vals[j], j - left, i - j)` at each pop for `[3, 1, 2, 4]`: the 1 is the minimum of 2 × 3 = 6 subarrays.
- Change `>=` to `>`: still 17, and still 6 for `[2, 2]`. One pass always makes one wall strict and the other not, so a tie is counted once either way.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Maximal Rectangle (85) asks for the largest rectangle made only of 1s in a binary matrix; in the 4 × 5 grid of the cell, the answer is 6, two rows of three 1s. Turn each row into a histogram: `heights[c]` counts the 1s standing on this row in column c, and a `"0"` resets its column to the ground. The largest rectangle that sits on this row is then `largest_rectangle(heights)`, and the answer is the best over all rows.

<!-- cell -->

```python
def maximal_rectangle(matrix):
    best, heights = 0, [0] * (len(matrix[0]) if matrix else 0)
    for row in matrix:
        for c, cell in enumerate(row):       # the 1s standing on this row, per column
            heights[c] = heights[c] + 1 if cell == "1" else 0
        best = max(best, largest_rectangle(heights))
    return best


grid = [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]
print(maximal_rectangle(grid), maximal_rectangle([["0"]]), maximal_rectangle([]))   # 6 0 0
```

<!-- cell -->

**Try it**
- Print `heights` after each row in `maximal_rectangle(grid)`: `[1, 0, 1, 0, 0]`, `[2, 0, 2, 1, 1]`, `[3, 1, 3, 2, 2]`, `[4, 0, 0, 3, 0]`. A `"0"` resets its column to the ground.
- Print `largest_rectangle(heights)` after each row as well: 1, 3, 6 and 4. The best rectangle sits on the third row.
- Compare with the number instead of the character (`cell == 1`) and rerun: 0. The matrix holds the characters `"0"` and `"1"`, and no character equals the number 1.

<!-- cell -->

Create Maximum Number (321) asks for the largest number of k digits taken from two digit arrays, each keeping its own order: `[3, 4, 6, 5]` and `[9, 1, 2, 5, 8, 3]` with k = 5 give `[9, 8, 6, 5, 3]`. The full solution tries every split of k between the two arrays, takes the best subsequence of each, and merges the two by comparing the remaining tails, not just the heads.

Its building block is Remove K Digits mirrored. To keep the *largest* t digits of one array in order, pop while the top is *smaller* than the newcomer and drops are left; drops that are left over come off the tail, which `stack[:t]` does.

<!-- cell -->

```python
def max_subsequence(nums, t):                # 321's building block: the largest t digits, in order
    drop, stack = len(nums) - t, []
    for x in nums:
        while drop and stack and stack[-1] < x:   # FIX: the mirror image, drop smaller digits
            stack.pop()
            drop -= 1
        stack.append(x)                      # STEP
    return stack[:t]


print(max_subsequence([9, 1, 2, 5, 8, 3], 3), max_subsequence([3, 4, 6, 5], 2))   # [9, 8, 3] [6, 5]
```

<!-- cell -->

**Try it**
- Predict `max_subsequence([6, 0, 4], 2)` before running: `[6, 4]`.
- Delete the `[:t]` and run `max_subsequence([5, 4, 3], 1)`: `[5, 4, 3]` instead of `[5]`. Falling digits never pop, so the unused drops must come off the tail, as in Remove K Digits.
- Change `<` to `<=` and run `max_subsequence([6, 6, 5], 2)`: `[6, 5]` instead of `[6, 6]`. Popping an equal digit spends a drop for nothing.
- Finish 321: for every split `i + (k - i) = k` that both arrays can supply, merge `a = max_subsequence(nums1, i)` and `b = max_subsequence(nums2, k - i)` with `[max(a, b).pop(0) for _ in a + b]`, which compares the remaining tails, and keep the largest result. The example gives `[9, 8, 6, 5, 3]`.

<!-- cell -->

### Say it in the interview

> "The brute force scans right from every item for the first bigger one: O(n²). Those scans keep walking over items that are themselves still waiting. So I'll flip it: a stack holds the indices still waiting, whose values never rise; each new item pops and answers every smaller item on top, then waits itself. When `i` pops `j`, `j` was still waiting, so nothing between them beat it: `i` is `j`'s first warmer day. Every index is pushed once and popped once, so it's O(n) time and O(n) space."

Then point at the pop line and say *who* is resolved there ("this index just met its next warmer day"), and say what is left on the stack at the end and which answer those items get. Likely follow-ups and your answers:

- *Values instead of distances* (496) → record `ans[j] = t`.
- *A circular array* (503) → walk two laps with `i % n`; push only during the first.
- *The previous item instead of the next* → record after the loop, before pushing.
- *A stream of prices* (901) → the same stack, kept between calls; each call is amortised O(1), which means O(1) on average over all calls, because each price is pushed once and popped at most once.
- *O(1) extra space for 739* → scan right to left; to find day `i`'s answer, start at `j = i + 1` and jump `j += ans[j]` over days that are not warmer.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Car Fleet | `stack/car_fleet.py` | sort by position, closest first; compare solo arrival times: later than the fleet ahead → new fleet, same or sooner → merges |
| Create Maximum Number | `stack/create_maximum_number.py` | try every split; best subsequence per array by monotonic stack; merge by comparing remaining tails, not heads |
| Daily Temperatures | `stack/daily_temperatures.py` · `practice/simple/16_daily_temperatures.py` | stack of days still waiting (temperatures never rising); a warmer day pops them and records i − j |
| Largest Rectangle in Histogram | `stack/largest_rectangle_in_histogram.py` · `practice/simple/17_largest_rectangle_in_histogram.py` | rising stack; a popped bar's walls are the current index and the new top; flush with a 0 bar |
| Maximal Rectangle | `stack/maximal_rectangle.py` | each row is a histogram of the 1s standing on it; run Largest Rectangle once per row |
| Next Greater Element | `practice/simple/basics/monotonic_stacks/01_next_greater_element.py` | waiting indices; a bigger value pops and answers them; leftovers keep −1 |
| Next Greater Element II | `stack/next_greater_element_ii.py` | circular: walk 2n steps with i % n and push only during the first lap |
| Online Stock Span | `practice/simple/basics/monotonic_stacks/03_online_stock_span.py` | (price, span) pairs; a price ≤ today's is absorbed with every day it covered |
| Previous Smaller Element | `practice/simple/basics/monotonic_stacks/02_previous_smaller_element.py` | pop everything ≥ x (x is nearer and no bigger), then the top is the answer |
| Remove K Digits | `practice/simple/basics/monotonic_stacks/05_remove_k_digits.py` | drop a digit bigger than the next while k lasts; trim the tail; strip zeros; "0" if empty |
| Sum of Subarray Minimums | `practice/simple/basics/monotonic_stacks/04_sum_of_subarray_minimums.py` | nums[j] is the min of (j − left)(i − j) subarrays; one wall strict, the other not |

### Self-check

1. Why does the stack hold indices rather than values?
<details><summary>Answer</summary>The answer is written for a specific position (<code>ans[j]</code>) and often needs a distance or a width (<code>i - j</code>, <code>i - left - 1</code>). A value loses its position, while an index can always give the value back as <code>nums[j]</code>.</details>

2. In Daily Temperatures, when exactly is a day resolved, and what happens to the days still on the stack at the end?
<details><summary>Answer</summary>A day is resolved at the moment it is popped: the current day is the first one warmer than it, so its answer is <code>i - j</code>. Days still waiting at the end never met a warmer day, so they keep the default 0.</details>

3. The loop has a `while` inside a `for`. Why is it O(n) and not O(n²)?
<details><summary>Answer</summary>Count pops instead of loops. Each index is pushed exactly once, so it can be popped at most once, and all the <code>while</code> loops together pop at most n times. The total work is O(n).</details>

4. In Largest Rectangle, why is the left wall of a popped bar simply the new top of the stack?
<details><summary>Answer</summary>It is <code>previous_smaller</code> in disguise. When bar j arrived, it popped every bar at least as tall, so the bar left under it is its previous shorter bar, and nothing under an entry changes while that entry waits.</details>
