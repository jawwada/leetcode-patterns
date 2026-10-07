## Greedy

> Make the move that looks best right now, never take it back, and carry only a tiny summary of the past: a running sum, the furthest reach, the fuel in the tank. Greedy is fast because it never branches; it is correct only when you can say why the greedy move never closes a door that the best answer needed.

**Reach for it when** one number can summarise everything that matters about the prefix you have seen (best sum ending here, furthest index reachable, fuel so far), the question asks for the minimum number of jumps / taps / patches / removals, sorting by one key (end time, deadline) makes "take the one that finishes first" obviously safe, or a small swap argument shows the locally best move is never worse. Typical words: "minimum number of …", "can you reach …", "maximum … subarray", "as many as possible".

**In this repo:** `greedy/` (14 problems) · greedy on intervals (Non-overlapping Intervals) is in the Intervals section; greedy with a heap (IPO, refuelling stops, Course Schedule III) is in the Heaps section · basics: `practice/simple/basics/graphs/03_union_find.py` (the cycle view of Couples Holding Hands), `practice/simple/basics/monotonic_stacks/05_remove_k_digits.py` (a greedy kept honest by a stack)

### The picture

```text
Kadane: extend, or restart when the past only hurts
nums:      -2    1   -3    4   -1    2    1   -5    4
cur:       -2    1   -2    4    3    5    6    1    5        cur = max(x, cur + x)
                 ^         ^              ^
              restart   restart        best = 6               (both restarts drop a carried -2)

Jump Game II: breadth-first search whose levels are intervals
nums      2  3  1  1  4
index     0  1  2  3  4
level 0  [0]               farthest = 0 + 2 = 2
level 1     [1  2]         farthest = max(1 + 3, 2 + 1) = 4
level 2           [3  4]   holds the last index: 2 jumps
```

**Why it is fast:** the brute force tries every choice: every subarray (O(n²)), every jump path (exponential), every subset of taps (2ⁿ). Greedy notices that one number summarises everything about the past that the future cares about, so each step is a single `max` or a single comparison: O(n), or O(n log n) with a sort in front.

### Can I trust the greedy choice?

With greedy the code is the easy part; *correctness* is the risk. Two plain-language arguments cover almost every interview greedy, plus one habit.

**Exchange argument** ("swap in the greedy choice; nothing gets worse"). Take any best answer. Find the first place where it differs from the greedy. Swap its choice for the greedy one and check that the answer stays valid and is no worse. Repeat, and the best answer turns into the greedy answer without ever getting worse. Example: to keep the most non-overlapping intervals, a best answer's first interval can be swapped for the interval that *ends* first; it ends no later, so it can't clash with anything kept after it.

**Greedy stays ahead** ("after every step, greedy is at least as far along"). Pick a measure of progress and show that after k steps the greedy is never behind any other strategy. Example: Jump Game II. After j jumps the greedy's reach is the furthest that *any* j jumps can get, because it took the best reach from everything reachable in j − 1 jumps. Ahead at every step means first to the end.

**The habit: test it against brute force** (the cross-check from [From Idea to Code](#s01)). Run the greedy against an exhaustive search on a few hundred tiny random inputs. A wrong greedy usually fails within seconds, and the failing input shows you *why*.

### When greedy fails, and what to do

Greedy fails when today's best move blocks a better future. Coin change is the classic: with coins `[1, 3, 4]`, "biggest coin first" pays 6 as 4 + 1 + 1 (three coins) instead of 3 + 3 (two). Don't stare harder at the greedy: *test* it against a brute force on small inputs.

```python
from itertools import combinations_with_replacement


def coins_greedy(coins, amount):
    count = 0
    for c in sorted(coins, reverse=True):    # biggest coin first, as many as fit
        count += amount // c
        amount %= c
    return count if amount == 0 else -1


def coins_brute(coins, amount):              # fewest coins: try 0, 1, 2, ... coins
    for k in range(amount + 1):
        if any(sum(combo) == amount for combo in combinations_with_replacement(coins, k)):
            return k
    return -1


def first_counterexample(fast, slow, coins, amounts):
    for amount in amounts:
        if fast(coins, amount) != slow(coins, amount):
            return amount, fast(coins, amount), slow(coins, amount)
    return None


print(first_counterexample(coins_greedy, coins_brute, [1, 3, 4], range(1, 15)))       # (6, 3, 2)
print(first_counterexample(coins_greedy, coins_brute, [1, 5, 10, 25], range(1, 15)))  # None
```

**Try it**
- Predict, then run, the coins `[1, 7, 10]`: the first counterexample is `(14, 5, 2)`, greedy 10 + 1 + 1 + 1 + 1 against 7 + 7.
- Print `combo` when `coins_brute` succeeds for `[1, 3, 4]` and amount 6: it is `(3, 3)`, found at k = 2.
- Point the same idea at a greedy of your own: for Non-overlapping Intervals, write "try every subset" and compare it with the sort-by-start version. It fails on `[[1, 100], [2, 3], [4, 5]]`.

What to do when the test breaks the greedy:

1. **Try another greedy key.** Many greedies fail with one sort key and work with another: keeping the most intervals fails by start and works by end.
2. **Greedy with regret.** Some need a key *and* a way to undo. Courses fail both shortest-first (`[[3, 3], [1, 4]]`: 1 instead of 2) and deadline-first-if-it-fits (`[[5, 5], [4, 6], [2, 6]]`: 1 instead of 2); deadline order plus a heap that drops the longest course taken works (Course Schedule III, refuelling stops: Heaps section).
3. **Search with pruning.** If choices really interact, explore them: backtracking with good pruning (Backtracking section).
4. **Remember sub-answers.** If the same sub-question keeps coming back ("fewest coins for amount a"), that is dynamic programming, and coin change is its textbook example.

### From idea to code

**The idea in one sentence:** *walk left to right carrying the smallest summary of the past that decides the future; at each item make the locally best update (usually one `max`), and record the answer the moment it is known.*

| Decision | Greedy answer |
|---|---|
| **State / Definition** | one or two numbers that summarise the prefix, defined precisely (the definition is half the proof): `cur` = best sum of a subarray that ENDS at i; `farthest` = furthest index reachable with one more jump |
| **Invariant** | the choices made so far can still be completed into a best answer (the exchange or stays-ahead argument proves it), and the summary is exact for the prefix 0..i |
| **Step** | fold item i in with one local choice, usually a `max`: `cur = max(x, cur + x)`, `farthest = max(farthest, i + nums[i])` |
| **Fix** | when a boundary is reached, start the next stretch: a new jump level (`cur_end = farthest`), a new candidate start, a new part |
| **Record** | right after the step (`best = max(best, cur)`), or at the boundary (count a jump, cut a part) |
| **Init** | the first item (`cur = best = nums[0]`) or a neutral value (`reach = 0`); never `best = 0` if every value can be negative |
| **Return** | `best`, a count, or the failure value: `False` when `i > reach`, −1 when the total gas is below the total cost |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "best sum ending here: extend, or start fresh" | `cur = max(x, cur + x)` |
| "best so far" | `best = max(best, cur)` |
| "the furthest I can get" | `reach = max(reach, i + nums[i])` |
| "I'm standing where I can't be" | `if i > reach: return False` |
| "this jump's range is used up" | `if i == cur_end: jumps += 1; cur_end = farthest` |
| "the tank ran dry: start after here" | `if tank < 0: start, tank = i + 1, 0` |
| "this part must reach every letter's last copy" | `end = max(end, last[c])` |

**Step, then record; reach, then close the level.** Kadane records `cur` only after the step has made it the best sum ending *here*. Jump Game II folds index i's reach into `farthest` before asking whether the level ends at i, because i belongs to the level that is closing.

```python
def max_subarray(nums):
    cur = best = nums[0]                     # STATE + INIT: cur = best sum of a subarray ENDING here
    for x in nums[1:]:
        cur = max(x, cur + x)                # STEP: extend, or restart if the past only hurts
        best = max(best, cur)                # RECORD: cur is final for this index now
    return best                              # RETURN


def min_jumps(nums):
    jumps = cur_end = farthest = 0           # STATE + INIT: cur_end = last index reachable with `jumps` jumps;
                                             #   farthest = furthest index reachable with one more jump
    for i in range(len(nums) - 1):           # stop before the last index: arriving needs no jump
        farthest = max(farthest, i + nums[i])    # STEP: i is in the current level, fold in its reach
        if i == cur_end:                     # FIX: the level is used up; the next one ends at farthest
            jumps += 1                       # RECORD: one more jump
            cur_end = farthest
    return jumps                             # RETURN


print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), max_subarray([-3, -1, -2]))   # 6 -1
print(min_jumps([2, 3, 1, 1, 4]), min_jumps([0]))                                   # 2 0
```

**Try it**
- Start from `cur = best = 0` and loop over all of `nums`: `max_subarray([-3, -1, -2])` returns 0, a sum that no non-empty subarray has.
- Swap the two lines in `max_subarray`'s loop (record, then step): `max_subarray([1, 2])` returns 1. The last step is never recorded.
- In `min_jumps`, move the `if i == cur_end:` block above the `farthest = ...` line: `min_jumps([2, 3, 1, 1, 4])` returns 1. The first level closed before index 0's reach was counted.
- Loop `for i in range(len(nums))` (one step too far) and run `min_jumps([1, 1])`: 2 instead of 1. Standing on the last index triggered a jump to nowhere.

### Watch it work

```python
def trace_kadane(nums):
    cur = best = nums[0]
    print(f"x={nums[0]:>2}  cur={cur:>2}  best={best:>2}  (start)")
    for x in nums[1:]:
        note = "restart: the carried sum was negative" if cur < 0 else "extend"
        cur = max(x, cur + x)
        best = max(best, cur)
        print(f"x={x:>2}  cur={cur:>2}  best={best:>2}  {note}")


trace_kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4])
```

**Try it**
- Run `trace_kadane([5, -9, 6])`: the 5 is carried into −4, then dropped, and `cur` restarts at 6, which is also the best.
- Run `trace_kadane([-3, -1, -2])`: every step restarts, and `best` ends as the single largest number, −1.
- Run `trace_kadane([2, -1, 2])`: the dip is worth crossing; `cur` goes 2, 1, 3.

### Where it goes wrong

1. **Starting `best` (or restarting) at 0.** Kadane on `[-3]` returns 0. Start from `nums[0]` and restart to `x`, not to 0.
2. **Checking reachability after updating it.** In Jump Game, updating `reach` before testing `i > reach` lets you jump *from* an index you never reached: `[0, 1]` becomes `True`.
3. **One loop step too many.** Jump Game II stops at index n − 2; standing on the last index needs no jump (`[1, 1]` gives 2 instead of 1).
4. **Updating `hi` before computing `lo`** in Maximum Product. Compute both from the *old* pair in one tuple assignment; the line-by-line version turns `[-1, -2, -1]` into 4, a product no subarray has (the answer is 2).
5. **Overwriting instead of `max` in Candy's second pass.** The right-to-left pass must keep what the left pass needed: `[1, 2, 3, 1]` gives 6 instead of 7.
6. **Restarting at `i` instead of `i + 1`** in Gas Station: the station where the tank went negative belongs to the doomed stretch. `([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])` returns 2 instead of 3.
7. **Dropping Gas Station's total check.** The scan only finds the last candidate; the total says whether any candidate works: `([2, 3, 4], [3, 4, 3])` returns 2 instead of −1.
8. **Trusting a greedy without a proof or a test.** "Biggest coin first" fails for coins `[1, 3, 4]` and amount 6.

### Edge cases to say out loud

One element · all negative (Kadane) · zeros (Maximum Product restarts there) · `[0]` (already at the end: reachable, 0 jumps) · a 0 you must cross (`[3, 2, 1, 0, 4]` is stuck) · total gas below total cost · equal neighbours (Candy: no rule between them) · ties in the sort order (Set Intersection: by end, then start descending).

```python
assert max_subarray([5]) == 5
assert max_subarray([-3, -1, -2]) == -1                  # all negative: never 0
assert max_subarray([0, -1, 0]) == 0
assert max_subarray([2, -1, 2]) == 3                     # a dip worth crossing
assert min_jumps([0]) == 0                               # already at the end
assert min_jumps([1, 1]) == 1
assert min_jumps([5, 1, 1, 1]) == 1                      # one jump covers everything
assert min_jumps([1, 2, 1, 1, 1]) == 3
print("edge cases pass")
```

**Try it**
- Predict `max_subarray([-1, 5, -1])` (5), then add the assert.
- What should `min_jumps([2, 1])` be? One jump: from index 0 you reach index 1 directly. Add it.
- `min_jumps` assumes the end is reachable: `min_jumps([1, 0, 1])` returns 2. Jump Game's `i > reach` test does not catch it, because the loop never stands on the last index. Check instead whether a closing level reached anything new: `if farthest <= i: return -1` as the first line inside `if i == cur_end:` (`min_taps` below does exactly this). Now `[1, 0, 1]` and `[3, 2, 1, 0, 4]` both return −1.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Extend or restart** | the template; save `start` at each restart to return the subarray; circular: also cut out the most negative run | 53, 918 |
| **Signs flip the order** | carry the largest AND the smallest product ending here | 152 |
| **Reachable frontier** | one number `reach`; stuck when `i > reach` | 55 |
| **Frontier in levels** | the template: count a jump (a tap, a clip) when `i == cur_end` | 45, 1024, 1326 |
| **Running sum with restart** | tank < 0 after i: no start in that stretch works, so restart at i + 1 | 134 |
| **Intervals in disguise** | each letter spans [first, last]; cut where no span crosses | 763 |
| **Two passes** | satisfy the left neighbours, then the right ones; keep the max | 135 |
| **Smallest first** | the smallest card left must start a run; use runs in sorted order | 846 |
| **A range of possible states** | track the lowest and highest possible open-bracket count; `*` widens the range | 678 |
| **Sort by a difference** | sort people by cost to A minus cost to B; the first half go to A | 1029 |
| **Two running minimums** | keep the smallest value, and the smallest value with something smaller before it; a bigger third wins | 334 |
| *Stretch:* **covered prefix** | sums 1..reach are covered; patch reach + 1 to double it | 330 |
| *Stretch:* **work backwards** | undo the last move first: it is the one still fully visible | 936 |
| *Stretch:* **rightmost points** | sort by end; new points go at the right end, where they serve the most later intervals | 757 |
| *Stretch:* **bounds that meet** | the answer is the largest lower bound, and it is always reachable | 517, 1526 |
| *Stretch:* **swap into place** | fix the couches left to right; each swap seats one couple, and a k-cycle needs k − 1 | 765 |

**Extend or restart, follow-ups.** Interviewers often ask for the subarray itself, or for a circular array (Maximum Sum Circular Subarray, 918). For the subarray, remember where the current run started and copy `(start, i)` whenever the best improves. For a circular array, the best run either does not wrap (plain Kadane) or wraps around the end, and a wrapping run is everything except one middle run, so cutting out the *most negative* run gives `total − worst`.

```python
def max_subarray_span(nums):
    cur, start = nums[0], 0                  # STATE: cur = best sum ending at i; start = where that run starts
    best, l, r = nums[0], 0, 0
    for i in range(1, len(nums)):
        if cur < 0:                          # STEP: restart here ...
            cur, start = nums[i], i
        else:                                # ... or extend
            cur += nums[i]
        if cur > best:                       # RECORD: remember where the best run starts and ends
            best, l, r = cur, start, i
    return best, l, r                        # RETURN


def max_circular_subarray(nums):             # 918
    best = cur_hi = cur_lo = worst = nums[0]
    for x in nums[1:]:
        cur_hi = max(x, cur_hi + x)          # STEP: Kadane for the largest run ...
        best = max(best, cur_hi)
        cur_lo = min(x, cur_lo + x)          # ... and for the most negative run
        worst = min(worst, cur_lo)
    return best if best < 0 else max(best, sum(nums) - worst)   # RETURN: all negative, nothing to wrap


print(max_subarray_span([-2, 1, -3, 4, -1, 2, 1, -5, 4]))           # (6, 3, 6)
print(max_circular_subarray([5, -3, 5]), max_circular_subarray([-3, -2, -3]))   # 10 -2
```

**Try it**
- Change `cur > best` to `cur >= best` and run `max_subarray_span([3, -3, 3])`: the sum stays 3, but the span moves from `(0, 0)` to `(0, 2)`. Ties pick a different (also correct) subarray, so ask which one is wanted.
- Drop the `best < 0` guard and run `max_circular_subarray([-3, -2, -3])`: 0, the sum of an empty "everything except the whole array".
- Print `sum(nums) - worst` for `[5, -3, 5]`: 7 − (−3) = 10, the run 5, 5 that wraps around the end.

**Signs flip the order (Maximum Product Subarray).** A negative number turns the largest product into the smallest and the smallest into the largest. So carry both: whichever one the next negative flips into the lead is already in hand. A zero resets both to 0, a fresh start.

```python
def max_product(nums):
    hi = lo = best = nums[0]                 # STATE + INIT: hi / lo = largest / smallest product ENDING here
    for x in nums[1:]:
        hi, lo = max(x, hi * x, lo * x), min(x, hi * x, lo * x)   # STEP: both from the OLD hi and lo
        best = max(best, hi)                 # RECORD
    return best                              # RETURN


print(max_product([2, 3, -2, 4]), max_product([-2, 0, -1]), max_product([-2, 3, -4]))   # 6 0 24
```

**Try it**
- Split the tuple assignment into two lines (`hi = ...`, then `lo = ...`): `max_product([-1, -2, -1])` gives 4, a product no subarray has (the answer is 2). `lo` was computed from the *new* `hi`.
- Print `hi, lo` after each step for `[-2, 3, -4]`: `(3, -6)`, then `(24, -12)`. The −6 waited in `lo` until −4 flipped it into the lead.
- Keep only `hi` (plain Kadane with products, `hi = max(x, hi * x)`): `[-2, 3, -4]` gives 3 instead of 24.

**Reachable frontier (Jump Game).** The indices you can reach always form a prefix `[0, reach]`, so one number is the whole state. Check before you step: an index beyond `reach` can't be stood on, so its jump must not count.

```python
def can_jump(nums):
    reach = 0                                # STATE: furthest index reachable from indices 0..i
    for i, step in enumerate(nums):
        if i > reach:                        # RETURN: I can't even stand here
            return False
        reach = max(reach, i + step)         # STEP: standing on i, fold in its jump
    return True                              # RETURN


print(can_jump([2, 3, 1, 1, 4]), can_jump([3, 2, 1, 0, 4]), can_jump([0]))   # True False True
```

**Try it**
- Move the `reach = ...` line above the `if`: `can_jump([0, 1])` becomes `True`. You jumped from index 1 without ever standing on it.
- Print `i, reach` for `[3, 2, 1, 0, 4]`: reach is 3 at indices 0 to 3, and index 4 is beyond it.

**Running sum with restart (Gas Station).** If you start at s and the tank first goes negative after station i, then *no* start between s and i works either: you reached each of them with a non-negative tank, so starting there with an empty one is no better. Jump the candidate start straight to i + 1. If the total gas covers the total cost, the last candidate is the answer: it sits right after the lowest point of the running balance.

```text
gas - cost   -2  -2  -2   3   3
balance      -2  -4  -6  -3   0      the lowest point is after station 2
start at 3, right after the lowest point: the tank there is balance + 6, never negative
before the end, and total >= 0 keeps it non-negative after wrapping round (tanks 3, 6, 4, 2, 0)
```

```python
def can_complete_circuit(gas, cost):
    total = tank = start = 0                 # STATE: total = balance of the whole loop;
                                             #   tank = balance since the candidate start
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff                        # STEP: station i joins both balances
        tank += diff
        if tank < 0:                         # FIX: dry after i, so no start in start..i works:
            start, tank = i + 1, 0           #   restart at i + 1 with an empty tank
    return start if total >= 0 else -1       # RETURN


print(can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), can_complete_circuit([2, 3, 4], [3, 4, 3]))   # 3 -1
```

**Try it**
- Restart at `i` instead of `i + 1` (`start, tank = i, 0`): the first call returns 2, and starting at station 2 dies at once (3 gas, 5 cost).
- Print `start, tank` at the end of each step of the first call: the start jumps to 1, 2, 3 while the tank keeps dying, then the tank climbs to 3 and 6.
- Return `start` without the total check: the second call returns 2 instead of −1. The scan finds a candidate even when no start works.

**Intervals in disguise (Partition Labels).** Every letter spans from its first to its last copy, and a part must swallow the whole span of every letter it touches. Sweep left to right pushing the part's end out to `last[c]`; when `i` catches up with the end, no letter inside reaches further: cut.

```text
s:    a b a b c b a c a | d e f e g d e | h i j h k l i j
a:    [---------------]
b:      [-------]
c:            [-----]
d:                        [---------]
e:                          [---------]       cut where i == end: after 8, 15, 23 -> [9, 7, 8]
```

```python
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}   # STATE: each letter's span ends at its last copy
    sizes, start, end = [], 0, 0             # STATE: the current part is s[start..end] so far
    for i, c in enumerate(s):
        end = max(end, last[c])              # STEP: the part must reach every letter it has touched
        if i == end:                         # FIX: nothing inside reaches further, close the part
            sizes.append(end - start + 1)    # RECORD
            start = i + 1
    return sizes                             # RETURN


print(partition_labels("ababcbacadefegdehijhklij"))   # [9, 7, 8]
```

**Try it**
- Test `i == end` *before* updating `end`: `partition_labels("abab")` gives `[1, 3]` instead of `[4]`. The first `a` was cut off before its span was known.
- Predict, then run: `partition_labels("abc")` is `[1, 1, 1]` and `partition_labels("abca")` is `[4]`.
- Print `i, end` for `"abab"`: `end` jumps to 2 at the first `a` and to 3 at the first `b`, and the part closes only at index 3.

**Two passes (Candy).** Each child has two rules: more candy than a lower-rated left neighbour, and more than a lower-rated right neighbour. One left-to-right pass satisfies every left rule with the fewest candies; one right-to-left pass does the same for the right rules. A child must satisfy both, so it takes the larger of its two counts.

```text
ratings:      1   2   3   1   0
left pass:    1   2   3   1   1      climb from the left
right pass:   1   1   3   2   1      climb from the right
max of both:  1   2   3   2   1      = 9 candies
```

```python
def candy(ratings):
    n = len(ratings)
    c = [1] * n                              # STATE + INIT: candies; everyone starts with 1
    for i in range(1, n):                    # pass 1, left -> right
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1              # STEP: beat a lower left neighbour
    for i in range(n - 2, -1, -1):           # pass 2, right -> left
        if ratings[i] > ratings[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)   # FIX: beat a lower right neighbour, keep what pass 1 needed
    return sum(c)                            # RETURN


print(candy([1, 0, 2]), candy([1, 2, 2]), candy([1, 2, 3, 1, 0]))   # 5 4 9
```

**Try it**
- Replace `max(c[i], c[i + 1] + 1)` with `c[i + 1] + 1`: `candy([1, 2, 3, 1])` gives 6 instead of 7. The peak lost the 3 it needed for its left side.
- Print `c` after each pass for `[1, 2, 3, 1, 0]` and compare with the picture.
- `candy([2, 2, 2])` is 3: equal neighbours have no rule between them, so everyone gets 1.

**Smallest first (Hand of Straights).** Can the cards be split into runs of `w` consecutive values? Look at the smallest card left: it can't sit in the middle of a run, because that run would need a smaller card. So every copy of it *starts* a run, which forces exactly how many copies of the next `w − 1` values are used. Repeat with the next smallest card.

```python
def is_n_straight_hand(hand, w):             # 846
    count = Counter(hand)                    # STATE: copies of each card still unused
    for x in sorted(count):                  # smallest card first
        need = count[x]                      # every x left must START a run: nothing smaller is left
        if need:
            for y in range(x, x + w):        # the runs need `need` copies of x, x+1, ..., x+w-1
                if count[y] < need:
                    return False             # RETURN: a run can't be completed
                count[y] -= need             # STEP: use them up
    return True                              # RETURN


print(is_n_straight_hand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), is_n_straight_hand([1, 2, 3, 4, 5], 4))   # True False
```

**Try it**
- Iterate `for x in count` (input order) instead of `sorted(count)`: `is_n_straight_hand([2, 1, 3], 3)` gives `False` instead of `True`. The 2 tried to start a run although the 1 was still waiting.
- Print `x, need` inside the `if need:` for the first call: runs start at 1, 2 and 6, once each.

#### Stretch: hard greedies

The six patterns below are Hard problems. Each is one of the ideas above with a twist; learn the core first, then come back.

**Covering with the fewest intervals (Taps).** The taps problem is Jump Game II in disguise: bucket every tap by its left end, `right_end[l]` = the furthest right end of a tap that starts at `l`, then count the "jumps" needed to cover `[0, n]`. A level that reaches nothing new is a dry gap.

```python
def min_taps(n, ranges):
    right_end = [0] * (n + 1)                # STATE: right_end[l] = furthest right end of a tap starting at l
    for i, r in enumerate(ranges):
        left = max(0, i - r)
        right_end[left] = max(right_end[left], i + r)
    taps = cur_end = farthest = 0            # exactly min_jumps, with right_end[i] for i + nums[i]
    for i in range(n):
        farthest = max(farthest, right_end[i])   # STEP
        if i == cur_end:                     # FIX: the watered prefix ends here
            if farthest <= i:                # nothing waters past i: a dry gap
                return -1                    # RETURN
            taps += 1                        # RECORD: open one more tap
            cur_end = farthest
    return taps                              # RETURN


print(min_taps(5, [3, 4, 1, 1, 0, 0]), min_taps(3, [0, 0, 0, 0]), min_taps(7, [1, 2, 1, 0, 2, 1, 0, 1]))   # 1 -1 3
```

**Try it**
- Drop the clamp (`left = i - r`) and rerun the first call: −1 instead of 1. `right_end[-3]` silently wrote into index 3 (negative indexing), so no tap seems to start at 0.
- `min_taps(0, [5])` is 0: a garden that is a single point needs no tap, and the loop never runs.

**Covered prefix (Patching Array).** Keep `reach` with the promise "every value in 1..reach is a subset sum". A number x ≤ reach + 1 extends it to 1..reach + x. A bigger x leaves reach + 1 as a hole no later (bigger) number can fill, so patch reach + 1 itself: it doubles the coverage, the most any single number can add.

```python
def min_patches(nums, n):
    reach, patches, i = 0, 0, 0              # STATE: every value in 1..reach is a subset sum
    while reach < n:
        if i < len(nums) and nums[i] <= reach + 1:   # STEP: glues on, now 1..reach + nums[i]
            reach += nums[i]
            i += 1
        else:                                # FIX: reach + 1 is a hole, patch it (coverage doubles)
            reach += reach + 1
            patches += 1                     # RECORD
    return patches                           # RETURN


print(min_patches([1, 3], 6), min_patches([1, 5, 10], 20), min_patches([1, 2, 2], 5))   # 1 2 0
```

**Try it**
- Change `nums[i] <= reach + 1` to `nums[i] <= reach`: `min_patches([1, 3], 6)` gives 2 instead of 1. The first patch is a 1, although the array already had one.
- Print `reach` after each patch of `min_patches([], 20)`: 1, 3, 7, 15, 31. With no numbers at all, patching 1, 2, 4, 8, 16 doubles the coverage each time: 5 patches.
- Patch a smaller value instead, say always 1 (`reach += 1`): `min_patches([], 20)` needs 20 patches instead of 5.

**Work backwards (Stamping the Sequence).** Forwards you can't know which stamps will be covered later; backwards the *last* stamp is still fully visible. Peel any window that matches the stamp, turning its letters into `?` wildcards (whatever lay underneath was overwritten anyway). Peeling only makes other windows easier to match, which is why "peel anything that matches" is safe. Reverse the peel order to get the stamp order.

```text
target   a b a b c        stamp "abc"
peel 2:  a b ? ? ?        window 2 is exactly "abc"
peel 0:  ? ? ? ? ?        window 0 is "ab?": '?' matches anything
stamp order = the peel order reversed = [0, 2]
```

```python
def moves_to_stamp(stamp, target):
    m, n = len(stamp), len(target)
    t, erased, peeled = list(target), 0, []  # STATE: t = target with peeled cells as '?'
    progress = True
    while erased < n and progress:
        progress = False
        for i in range(n - m + 1):
            window = t[i:i + m]
            fits = all(ch == "?" or ch == sc for ch, sc in zip(window, stamp))
            if fits and window != ["?"] * m:     # matches, and still has a real letter to peel
                for j in range(i, i + m):
                    if t[j] != "?":
                        t[j] = "?"              # STEP: peel it
                        erased += 1
                peeled.append(i)                 # RECORD
                progress = True
    return peeled[::-1] if erased == n else []   # RETURN: the last peel was the first stamp


print(moves_to_stamp("abc", "ababc"), moves_to_stamp("abca", "aabcaca"), moves_to_stamp("ab", "ba"))
# [0, 2] [0, 3, 1] []
```

**Try it**
- Check the second answer forwards by hand: from `???????`, stamp `abca` at 0, 3, 1: `abca???`, `abcabca`, `aabcaca`. That is the target.
- Return `peeled` without reversing it: `[1, 3, 0]`, and applying it forwards gives `abcabca`, not the target. The order matters.
- Why the `window != ["?"] * m` test? Without it, an all-`?` window "matches" on every pass, and on an impossible target such as `moves_to_stamp("ab", "abx")` the loop would never end. Reason it out rather than running it.

**Rightmost points (Set Intersection Size At Least Two).** Process intervals by end. When one still lacks points, add them as far right as possible, at e − 1 and e: every later interval ends at or after e, so right-end points are shared with the most of them. Only the two largest chosen points can matter later. On equal ends, take the *narrower* interval first (start descending), so its points serve the wider one too.

```python
def intersection_size_two(intervals):
    a, b, count = -math.inf, -math.inf, 0    # STATE: the two largest chosen points, a < b
    for s, e in sorted(intervals, key=lambda iv: (iv[1], -iv[0])):   # INIT: by end; equal ends: narrow first
        if s > b:                            # STEP: neither point is inside, add e - 1 and e
            a, b = e - 1, e
            count += 2
        elif s > a:                          # STEP: only b is inside, add e
            a, b = b, e
            count += 1
    return count                             # RETURN


print(intersection_size_two([[1, 3], [3, 7], [8, 9]]), intersection_size_two([[1, 3], [1, 4], [2, 5], [3, 5]]))   # 5 3
```

**Try it**
- Break ties by start *ascending* (`key=lambda iv: (iv[1], iv[0])`) and run `intersection_size_two([[0, 1], [1, 5], [3, 5], [5, 6]])`: 4 instead of 5. The wide `[1, 5]` picks 5, then `[3, 5]` "adds" 5 again, a duplicate.
- Change `s > b` to `s >= b`: the first call gives 6 instead of 5. The intervals are closed, so a point sitting exactly at `s` is inside.

**Bounds that meet (Super Washing Machines, Minimum Increments).** Sometimes the greedy *is* a formula: find the lower bounds every schedule must respect, and the largest one can always be reached. Washing machines: the dresses that must cross a boundary (the prefix balance) cross at most one per move, and an overloaded machine hands out only one dress per move. Increments: every +1 stroke has one left edge, and a step up of d needs d new left edges.

```python
def find_min_moves(machines):
    total, n = sum(machines), len(machines)
    if total % n:
        return -1                            # RETURN: can't split evenly
    target = total // n
    balance = best = 0                       # STATE: balance = dresses that must cross the boundary on the right
    for load in machines:
        excess = load - target               # this machine must hand out `excess`, one per move
        balance += excess                    # STEP
        best = max(best, abs(balance), excess)   # RECORD: the largest lower bound so far
    return best                              # RETURN


def min_number_operations(target):           # strokes start only where the skyline steps up
    return target[0] + sum(max(0, b - a) for a, b in zip(target, target[1:]))


print(find_min_moves([1, 0, 5]), find_min_moves([0, 3, 0]), find_min_moves([0, 2, 0]))   # 3 2 -1
print(min_number_operations([3, 1, 5, 4, 2, 3, 4, 2]))                                   # 9
```

**Try it**
- Drop `excess` from the `max`: `find_min_moves([0, 3, 0])` gives 1 instead of 2. The middle machine has two dresses to give and can only pass one per move.
- Use `abs(excess)` instead: `find_min_moves([3, 0, 3])` gives 2 instead of 1. A machine that is *short* can receive from both sides in the same move.
- List the steps up for `[3, 1, 5, 4, 2, 3, 4, 2]`: 3 at the start, then 4, 1, 1. That is 9 strokes.

**Swap into place (Couples Holding Hands).** Fix the couches from left to right: if seat `i + 1` does not hold the partner of seat `i`, swap the partner in; each swap seats one couple for good. Why minimal? With couples as nodes and couches as edges, the seating splits into cycles; a cycle of k couples needs exactly k − 1 swaps and this fixing never wastes one, so the answer is couples − cycles.

```python
def min_swaps_couples(row):
    row = row[:]                             # don't edit the caller's list
    seat = {p: i for i, p in enumerate(row)} # STATE: where each person sits now
    swaps = 0
    for i in range(0, len(row), 2):          # couch (i, i + 1), left to right
        partner = row[i] ^ 1                 # 0 <-> 1, 2 <-> 3, ...
        if row[i + 1] != partner:
            j = seat[partner]                # STEP: bring the partner next to row[i]
            row[i + 1], row[j] = row[j], row[i + 1]
            seat[row[j]], seat[row[i + 1]] = j, i + 1   # FIX: keep the seat map true
            swaps += 1                       # RECORD
    return swaps                             # RETURN


print(min_swaps_couples([0, 2, 1, 3]), min_swaps_couples([3, 2, 0, 1]), min_swaps_couples([0, 2, 4, 1, 3, 5]))   # 1 0 2
```

**Try it**
- Print `row` after every swap for `[0, 2, 4, 1, 3, 5]`: `[0, 1, 4, 2, 3, 5]`, then `[0, 1, 4, 5, 3, 2]`. Each swap completes one couch for good.
- Delete the line that updates `seat` and run `min_swaps_couples([0, 2, 3, 4, 1, 5])`: 3 instead of 2. A stale seat number sent a swap to the wrong place.
- Check the partner trick: `[x ^ 1 for x in range(6)]` is `[1, 0, 3, 2, 5, 4]`.

### Say it in the interview

> "Brute force tries every choice: O(n²) subarrays, or exponentially many paths and subsets. The greedy move is ___, and it is safe because ___: either an exchange (any best answer can swap its first choice for mine and stay valid and no worse) or stays-ahead (after every step I am at least as far as any other plan). So one pass carrying ___ decides everything: O(n), or O(n log n) with a sort in front."

Fill in the blanks out loud. Jump Game II: "the move is to make the next level end at the farthest index any index in this level can reach; it is safe because after j jumps no plan reaches further; one pass carrying `cur_end` and `farthest`, O(n)." Likely follow-ups and your answers:

- *Return the subarray, not the sum* → save `start` when you restart; copy `(start, i)` whenever `best` improves.
- *The array is circular* (918) → `max(best, total − most negative run)`, unless every number is negative.
- *Jump Game II, but the end may be unreachable* → when a level closes, `if farthest <= i: return -1`.
- *Gas Station: why is `total >= 0` enough?* → the start right after the lowest point of the running balance never runs dry (the picture above).
- *Prove it* → one exchange or stays-ahead sentence.
- *Your greedy breaks on a counterexample* → a regret heap (Heaps section), or search / dynamic programming.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Candy | `greedy/candy.py` | left pass beats the left neighbour, right pass the right one; each child takes the max of both |
| Couples Holding Hands | `greedy/couples_holding_hands.py` | couples are nodes, couches are edges: swaps = couples − cycles; fixing couches left to right achieves it |
| Gas Station | `greedy/gas_station.py` | if the tank dies after i, no start up to i works: restart at i + 1; possible iff total ≥ 0 |
| Jump Game | `greedy/jump_game.py` | reachable indices form a prefix: track reach, fail as soon as i > reach |
| Jump Game II | `greedy/jump_game_ii.py` | BFS whose levels are intervals: jump when i reaches cur_end, then cur_end = farthest |
| Maximum Product Subarray | `greedy/maximum_product_subarray.py` | a negative swaps the max and the min: carry both products ending here |
| Maximum Subarray | `greedy/maximum_subarray.py` | Kadane: cur = max(x, cur + x); a negative running sum is dead weight |
| Minimum Number of Increments on Subarrays to Form a Target Array | `greedy/min_number_operations.py` | every stroke has one left edge: target[0] + the sum of the positive steps up |
| Minimum Number of Taps to Open to Water a Garden | `greedy/minimum_number_of_taps_to_open_to_water_a_garden.py` | bucket taps by left end, then Jump Game II over the right ends; −1 when a level reaches nothing new |
| Partition Labels | `greedy/partition_labels.py` | each letter spans [first, last]; push end to last[c], cut when i == end |
| Patching Array | `greedy/patching_array.py` | sums 1..reach are covered; x ≤ reach + 1 extends it, otherwise patch reach + 1 (doubling) |
| Set Intersection Size At Least Two | `greedy/set_intersection_size_at_least_two.py` | sort by end (ties: start descending); keep the two largest points; add missing ones at e − 1, e |
| Stamping The Sequence | `greedy/stamping_the_sequence.py` | work backwards: peel any window matching the stamp ('?' is a wildcard), then reverse the order |
| Super Washing Machines | `greedy/super_washing_machines.py` | two lower bounds, abs(prefix balance) and a machine's own excess; the larger one is always reachable |

### Self-check

1. In Kadane, why is it safe to throw away a negative running sum?
<details><summary>Answer</summary>Any subarray that ends later and keeps the negative carried part would be strictly larger without it. So the best subarray ending at the next index is either that number alone or an extension of a non-negative carry: dropping a negative prefix never loses the optimum.</details>

2. In Hand of Straights, why must every copy of the smallest card left start a run?
<details><summary>Answer</summary>A run is w consecutive values. If the smallest card left sat in the middle or at the end of a run, that run would need a smaller card, and none is left. So all its copies start runs, and that decides how many copies of the next w − 1 values are used up.</details>

3. Why does Candy's second pass use `max` instead of overwriting?
<details><summary>Answer</summary>The left pass already set the smallest count that satisfies the left neighbour. Overwriting with the right-pass value can lower it and break that rule: in <code>[1, 2, 3, 1]</code> the peak needs 3 because of its left side but only 2 because of its right side.</details>

4. In an interview, how do you check a greedy you are not sure about?
<details><summary>Answer</summary>Attack it with tiny inputs first: ties, zeros, negatives, one huge item, and the input where a "bigger now" choice blocks the future. If it survives, state the exchange or stays-ahead argument in one sentence. When practising, run it against a brute force on a few hundred random small inputs.</details>
