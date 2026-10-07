## Monotonic Stack

> Keep a stack of the items that are still **waiting** for their answer. Each new item looks at the top: if it beats that item, the waiting item has just found its answer (pop it and record), and the newcomer looks at the next one down. Then the newcomer waits too. Beaten items leave, so the waiting values are always in sorted order: that is the "monotonic".

**Reach for it when** the problem asks, for every element, about the **nearest** element to its left or right that is **bigger or smaller** (the next warmer day, the next greater element, the previous smaller one, how far a bar can stretch, a stock's span), about the minimum or maximum of **every subarray**, or about deleting digits or letters to get the **smallest or largest sequence** while keeping the order.

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

The waiting days always form a staircase that never steps up. A newcomer knocks down every step shorter than itself (each knocked-down step has found its warmer day) and becomes the new last step.

**Why it is fast:** the brute force scans forward from every day: O(n²). On a falling stretch like 75 71 69, the scan from 75 walks over 71 and 69, which are *themselves still waiting* for a warmer day, so neither can be 75's answer. The stack flips the question: instead of each day searching forward for its answer, each new day announces itself as the answer to every waiting day it beats. Every index is pushed once and popped at most once, so the whole pass is O(n), even with a `while` inside the `for`.

**Why it is correct:** when day `i` pops day `j`, `j` was still waiting, so no day between them was warmer than `j` (it would have popped `j` first). So `i` is the *first* warmer day after `j`, which is exactly the answer. A day that is never popped never met a warmer day.

### From idea to code

**The idea in one sentence:** *for each new item: while it beats the item on top of the stack, that item is resolved (pop it, record its answer); then push the new item, which now waits for its own answer.*

| Decision | Monotonic-stack answer |
|---|---|
| **State / Definition** | a stack of **indices** of the items still waiting for their answer: `stack` = days whose warmer day hasn't come yet, temperatures never rising from bottom to top. Indices, not values: you need the position to write `ans[j]` and the distance `i - j` |
| **Invariant** | every index left of `i` that is *not* on the stack already has its answer; the values on the stack are sorted; and every day between a waiting day `j` and today was no warmer than `j`, or it would have popped `j` |
| **Step** | `stack.append(i)`: the newcomer waits for its own answer |
| **Fix** | before the step, `while stack and temps[stack[-1]] < t:` pop. The newcomer resolves (for *previous* questions: discards) every waiting item it beats |
| **Record** | *next* questions: at the pop (the popped index is answered by `i`). *Previous* questions: after the fix, before the step (the survivor on top answers `i`) |
| **Init** | `ans = [0] * n` or `[-1] * n` (the answer for "never"), `stack = []`; sometimes a sentinel item at the end to flush the stack |
| **Return** | `ans` (indices never popped keep the default), or the best value recorded at the pops |

**Which comparison?** Derive it from the question instead of memorising it. *Next* questions: pop while the newcomer *is* the top's answer, using the problem's own comparison ("strictly greater" → pop while `top < x`; "greater or equal" → pop while `top <= x`). *Previous* questions: pop while the top *can't be* the newcomer's answer (the negation: "strictly smaller" → pop while `top >= x`), then read the top. Each pop gives two facts at once: the popped item's next answer is the newcomer, and after the loop the top is the newcomer's previous answer, with the opposite strictness. Largest Rectangle uses both. The four common cases, as a check:

| For every item, find the nearest ... | Pop while the top is ... `x` | Values on the stack, bottom → top |
|---|---|---|
| greater to the **right** (next greater) | `< x` | never rising |
| smaller to the **right** (next smaller) | `> x` | never falling |
| greater to the **left** (previous greater) | `<= x`, then read the top | strictly falling |
| smaller to the **left** (previous smaller) | `>= x`, then read the top | strictly rising |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "the items still waiting for an answer" | `stack = []` (indices) |
| "the newcomer beats the most recent waiting item" | `while stack and temps[stack[-1]] < t:` |
| "that item is resolved, and I am its answer" | `j = stack.pop()`, then `ans[j] = i - j` (or `ans[j] = t` for the value) |
| "now I wait too" | `stack.append(i)` |
| "my nearest smaller item on the left" | after popping everything `>= x`: `nums[stack[-1]] if stack else -1` |
| "nobody ever beat it" | the default left in `ans` |
| "resolve whatever still waits at the end" | a sentinel item: `heights + [0]` |

Two templates: *next* answers are written at the pop, *previous* answers after the loop. FIX runs before STEP: the newcomer must resolve or discard the waiting items before it waits itself. Pushed first, it would sit on top and block every comparison (`[73, 74]` → `[0, 0]`).

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

**Try it**
- Use the rule to turn `previous_smaller` into *previous greater* (pop while `nums[stack[-1]] <= x`) and predict `[3, 1, 4, 1, 5]` before running: `[-1, 3, -1, 4, -1]`.
- Push the temperature instead of the index (`stack.append(t)`) and run the first example: `IndexError`, because the stack's entries are used as positions.
- Print `stack` right before the `return` for the first example: `[6, 7]`, the two days that never got a warmer day.
- In `previous_smaller`, change `>=` to `>` and run `previous_smaller([2, 2])`: `[-1, 2]` instead of `[-1, -1]`. An equal value is not smaller.

### Watch it work

The richest use of the loop is Largest Rectangle in Histogram (84), where one pop answers *both* questions. Bars pop when a bar that is not taller arrives (`>=`), so the newcomer is the popped bar's right wall, and the bar under it on the stack is its left wall (its previous smaller bar, or -1, an imaginary wall before the array, if there is none). The rectangle with the popped bar's height spans the bars strictly between the walls. A final bar of height 0 pops whatever still waits.

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

**Try it**
- Find the line that gives 10: bar 4 pops bar 2 (height 5), walls 1 and 4, width 2.
- Run `trace_rectangle([3, 3, 3])`: equal bars pop each other with widths 1 and 2 (under-measured), and only the last one gets width 3 (area 9). Harmless, which is why `>` and `>=` give the same answer.
- Run `trace_rectangle([1, 2, 3])`: nothing pops until the height-0 bar arrives, then all three pop at `i = 3`, and the best is 4.

### Where it goes wrong

1. **Storing values instead of indices.** You lose the position, so there is no way to write `ans[j]` or compute `i - j`. Push `i`; read the value as `nums[stack[-1]]`.
2. **`<` vs `<=` when popping.** "Strictly warmer" pops on `<`. Popping on `<=` lets an equal temperature answer: `[70, 70, 71]` would give `[1, 1, 0]` instead of `[2, 1, 0]`.
3. **Recording in the wrong place.** *Next* answers are written for the **popped** index, at the pop. *Previous* answers are written for the **current** index, after the loop. Mixing them up gives answers to the wrong items.
4. **Forgetting the leftovers.** Items still on the stack at the end were never resolved. They need the default (`-1`, `0`), or, in the histogram, a final bar of height 0 so they get measured: `[1, 2, 3]` must give 4, but without the flush nothing is ever popped and you get 0.
5. **Width off by one.** When bar `j` pops at `i` and `left` is the index under it, the bars strictly between the walls number `i - left - 1`, not `i - left`.
6. **Counting ties twice.** In Sum of Subarray Minimums, `[2, 2]` has two equal minimums, and the subarray `[2, 2]` must be credited to exactly one of them: one wall strict, the other not. A single stack pass does this by itself; computing the left and right walls in two separate passes with the same comparison gives 8 or 4 instead of 6.
7. **Remove K Digits leftovers.** If the digits never fall (`"12345"`, k = 2), the loop pops nothing, so cut the last k digits at the end. Then strip leading zeros, and return `"0"` if nothing is left (`"10"`, k = 2).

### Edge cases to say out loud

Empty input · one item · all equal (nothing is strictly greater) · strictly rising (everything resolves at once) · strictly falling (nothing resolves; everything is left at the end) · ties. And one habit worth more than any list: check the fast version against a brute force on many small random inputs.

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

**Try it**
- Predict `previous_smaller([5, 4, 3])` and `previous_smaller([1, 3, 2])` before running: `[-1, -1, -1]` and `[-1, 1, 1]`.
- Break `daily_temperatures` on purpose (pop on `<=`) and rerun this cell: the `[70, 70, 70]` assert fails first. Delete that assert and rerun: the random check fails too, and its message shows the input it failed on.
- Add `assert daily_temperatures([50] * 100_000) == [0] * 100_000`: it runs instantly. Every index is pushed once and never popped.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Next greater value** | record `ans[j] = x` instead of the distance | 496 |
| **Next greater in a linked list** | copy the values into a list, then run the template | 1019 |
| **Circular array** | walk `2n` steps with `i % n`; push only during the first lap | 503 |
| **Previous smaller / greater** | pop the useless items, then read the top for the current item | 84, 901 |
| **Span, online** | store `(price, span)`; a popped day's span is absorbed into today's | 901 |
| **Both walls at once** | rising stack: when `j` pops at `i`, `i` is its right wall and the new top its left wall | 84, 85; Trapping Rain Water (42) has a stack version too, but is taught in [Two Pointers](#s05) |
| **Both walls + prefix sums** | each minimum's walls bound the widest subarray it rules; its sum comes from prefix sums | 1856 |
| **Contribution counting** | `nums[j]` is the minimum of `(j - left) * (i - j)` subarrays | 907; 2104 is 907 twice (maxima minus minima) |
| **Greedy smallest / largest sequence** | pop while the top is worse than `x` *and* you can still afford to drop it | 402, 1081, 321 |
| **Scan from the right** | 132 Pattern: walk right to left; the last value popped is the best "2" | 456 |
| **Candidates, then a second scan** | keep a falling stack of left candidates, then match them from the right | 962 |
| **Monotonic deque** | this stack plus expiry from the front: the window maximum | 239, in [Sliding Window](#s06) |
| **Sort first, then stack** | sort by position; a car whose solo arrival time is later than the fleet ahead's starts a new fleet | 853 |

**Circular array** (503): after the last element comes the first. Walk the array twice: the second lap lets the elements at the start answer the items still waiting at the end. Only the first lap pushes, so each index waits once.

```python
def next_greater_circular(nums):
    n = len(nums)
    ans, stack = [-1] * n, []                # STATE + INIT: indices still waiting; -1 = "never"
    for i in range(2 * n):                   # two laps around the circle
        x = nums[i % n]
        while stack and nums[stack[-1]] < x: # FIX + RECORD: x answers every smaller waiting item
            ans[stack.pop()] = x
        if i < n:
            stack.append(i)                  # STEP: only the first lap creates waiting items
    return ans                               # RETURN


print(next_greater_circular([1, 2, 1]), next_greater_circular([1, 2, 3, 4, 3]))   # [2, -1, 2] [2, 3, 4, -1, 4]
```

**Try it**
- Delete `if i < n:` so the second lap pushes too: `IndexError`, since `i` (not `i % n`) is then used as a position past the end of `nums`.
- Walk one lap only (`range(n)`) and run `[1, 2, 1]`: `[2, -1, -1]`. The last 1 never sees the 2 at the front.
- Predict `[5, 4, 3, 2, 1]` and `[3, 3, 3]` before running: `[-1, 5, 5, 5, 5]` and `[-1, -1, -1]`.

**Largest rectangle** (84, 85): the loop traced in Watch it work. Bar `j`'s best rectangle has its height and stretches until the first shorter bar on each side; the pop delivers both walls. Maximal Rectangle turns each row of the matrix into a histogram of the 1s standing on that row, then reuses the same function.

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


def maximal_rectangle(matrix):
    best, heights = 0, [0] * (len(matrix[0]) if matrix else 0)
    for row in matrix:
        for c, cell in enumerate(row):       # the 1s standing on this row, per column
            heights[c] = heights[c] + 1 if cell == "1" else 0
        best = max(best, largest_rectangle(heights))
    return best


grid = [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]
print(largest_rectangle([2, 1, 5, 6, 2, 3]), largest_rectangle([2, 4]), maximal_rectangle(grid))   # 10 4 6
```

**Try it**
- Drop the sentinel (`bars = heights`) and run `largest_rectangle([1, 2, 3])`: 0 instead of 4. The heights only rose, so no bar was ever popped and measured.
- Change the width to `i - left` and run `[2, 1, 5, 6, 2, 3]` again: 15 instead of 10. Every rectangle now counts one bar too many (height 5 gets width 3).
- Print `heights` after each row in `maximal_rectangle(grid)`: `[1, 0, 1, 0, 0]`, `[2, 0, 2, 1, 1]`, `[3, 1, 3, 2, 2]`, `[4, 0, 0, 3, 0]`. A `"0"` resets its column to the ground.

**Sum of subarray minimums** (907): turn the sum around. Instead of finding the minimum of every subarray, ask for every element *how many subarrays it is the minimum of*. With its walls at `left` and `i` (the nearest smaller items), a subarray has `nums[j]` as its minimum when it starts in `left+1 .. j` and ends in `j .. i-1`: that is `(j - left) * (i - j)` subarrays. The histogram's pop hands you both walls.

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

**Try it**
- Check it against the brute force: with `nums = [3, 1, 2, 4]`, `sum(min(nums[i:j]) for i in range(4) for j in range(i + 1, 5))` is also 17.
- Print `(vals[j], j - left, i - j)` at each pop for `[3, 1, 2, 4]`: the 1 is the minimum of 2 × 3 = 6 subarrays.
- Change `>=` to `>`: still 17, and still 6 for `[2, 2]`. One pass always makes one wall strict and the other not, so a tie is counted once either way.

**Smallest sequence by deleting** (402, 1081, 321): to make the smallest number, the leftmost digits matter most. A digit sitting right before a smaller one should go, because deleting it slides the smaller digit into a more important place. So the digits you keep should never fall: pop while deletions are left. Smallest Subsequence of Distinct Characters (1081, same as 316) swaps the budget for a different test: drop a letter only if it appears again later. Create Maximum Number (321) uses the mirror image to keep the *largest* t digits.

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


def max_subsequence(nums, t):                # 321's building block: the largest t digits, in order
    drop, stack = len(nums) - t, []
    for x in nums:
        while drop and stack and stack[-1] < x:   # FIX: the mirror image, drop smaller digits
            stack.pop()
            drop -= 1
        stack.append(x)                      # STEP
    return stack[:t]


print(remove_k_digits("1432219", 3), remove_k_digits("10200", 1), remove_k_digits("10", 2))   # 1219 200 0
print(smallest_subsequence("bcabc"), smallest_subsequence("cbacdcbc"))                      # abc acdb
print(max_subsequence([9, 1, 2, 5, 8, 3], 3), max_subsequence([3, 4, 6, 5], 2))             # [9, 8, 3] [6, 5]
```

**Try it**
- Delete the line that trims leftover deletions and run `remove_k_digits("12345", 2)`: `12345` instead of `123`.
- Drop `or "0"` and run `remove_k_digits("10", 2)`: an empty string instead of `0`.
- In `smallest_subsequence`, delete `and last[stack[-1]] > i` and run `"cbacdcbc"`: `abc`. The `d` was dropped although it never comes back.
- Predict `max_subsequence([6, 0, 4], 2)` before running: `[6, 4]`.

**Span and fleets** (901, 853): a stock's span asks for the *previous greater* price, online: how many days in a row, ending today, had a price ≤ today's? A day that today beats lies inside today's span, and so does every day it had already absorbed, so store `(price, span)` pairs and add the spans you pop. Car Fleet sorts by position and walks from the car closest to the target, comparing *solo arrival times*, not speeds. A car whose time is later than the fleet ahead's can never catch it and leads a new fleet; one that would arrive at the same time or sooner catches up and merges. The times on that stack only rise, so it never pops: it is really just a running maximum.

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
    times = []                               # STATE + INIT: arrival times of the fleets, front fleet first
    for pos, spd in sorted(zip(position, speed), reverse=True):   # closest to the target first
        t = (target - pos) / spd             # this car's solo arrival time
        if not times or t > times[-1]:       # arrives later than the fleet ahead: a new fleet
            times.append(t)                  # STEP (otherwise it catches up and merges)
    return len(times)                        # RETURN


spanner = StockSpanner()
print([spanner.next(p) for p in [100, 80, 60, 70, 60, 75, 85]])   # [1, 1, 1, 2, 1, 4, 6]
print(car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))           # 3
```

**Try it**
- Change `<=` to `<` in `next` and replay `[60, 60, 60]` on a fresh spanner: `[1, 1, 1]` instead of `[1, 2, 3]`.
- Count each popped day as 1 (`span += 1`) instead of adding its span, and replay the main prices: `[1, 1, 1, 2, 1, 3, 3]`. The 75 loses the day that the 70 had absorbed, and the 85 gets 3 instead of 6.
- In `car_fleet`, drop `reverse=True` and rerun: 1 instead of 3. Each car now compares itself with a car *behind* it.
- Run `car_fleet(10, [0, 5], [2, 1])`: 1, because both cars reach the target at t = 5 and arrive together. With `t >= times[-1]` it would say 2.

### Say it in the interview

> "The brute force scans right from every item for the first bigger one: O(n²). Those scans keep walking over items that are themselves still waiting. So I'll flip it: a stack holds the indices still waiting, whose values never rise; each new item pops and answers every smaller item on top, then waits itself. When `i` pops `j`, `j` was still waiting, so nothing between them beat it: `i` is `j`'s first warmer day. Every index is pushed once and popped once, so it's O(n) time and O(n) space."

Then point at the pop line and say *who* is resolved there ("this index just met its next warmer day"), and say what is left on the stack at the end and which answer those items get. Likely follow-ups and your answers:

- *Values instead of distances* (496) → record `ans[j] = t`.
- *A circular array* (503) → walk two laps with `i % n`; push only during the first.
- *The previous item instead of the next* → record after the loop, before pushing.
- *A stream of prices* (901) → the same stack, kept between calls; each call is amortized O(1).
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
