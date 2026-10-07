## Sliding Window

> A window `[left .. right]` crawls along the array like a caterpillar: the front (`right`) takes one new item every step, and the back (`left`) moves only to repair the window (longest problems) or to tighten it (shortest problems). Each item enters once and leaves once, so the whole crawl is O(n).

**Reach for it when** the problem says *contiguous* (substring, subarray) and asks for the **longest**, **shortest**, or **number of** windows that satisfy a rule, and the rule is **monotone**: adding an item can never repair a broken window. Quick test: "can adding one more item make a bad window good again?" If yes (for example a sum with negative numbers), this tool does not apply; use prefix sums instead.

**In this repo:** `sliding_window/` (13 problems) · bank: `practice/simple/09_longest_substring_without_repeating_characters.py`, `practice/simple/10_minimum_window_substring.py`, `practice/simple/11_sliding_window_maximum.py`, `practice/simple/12_longest_repeating_character_replacement.py`

### The picture

```text
index  0 1 2 3 4 5 6 7
s      a b c a b c b b         rule: no letter twice inside s[L..R]

       L   R                   "abc" valid -> record 3
       L     R                 R eats s[3]='a': "abca" has two a's -> broken
         L   R                 L lets go of the old 'a': "bca" valid -> record 3
           L   R               same story for 'b': "cab"
                ...
                 L   R         R eats s[7]='b': "cbb" -> broken
                     L=R       L lets go of 'c' AND 'b' (while, not if): "b"
```

**Why it is fast:** the brute force restarts from every `left` and re-reads the same letters. Two neighbouring windows share everything except one item at each end, so we *update* instead of *recompute*. `left` and `right` only move forward, each at most n steps: O(n) in total, even though there is a loop inside a loop.

**Why it is correct:** if `[left..right]` is broken, every window that starts at or before `left` and ends at or after `right` contains it, so it is broken too (that is what "monotone" buys). The start `left` is finished for good, which is why `left` never has to move back, and why every window `[i..right]` with `left ≤ i ≤ right` is valid once the window is repaired: that is `right - left + 1` valid windows ending at `right`. Negative numbers break exactly this argument.

### From idea to code

**The idea in one sentence:** *the front eats one item; then the back moves until the window is the best it can be for this front (repaired for longest, as tight as possible for shortest), and the answer is recorded at the moment the window is known to be valid.*

The seven decisions, for the two templates side by side:

| Decision | Longest valid (3, 424, 904, 1004) | Shortest valid (209, 76) |
|---|---|---|
| **State / Definition** | `left`; `count[c]` = copies of c in `s[left..right]` | `left`; `total` = sum of `nums[left..right]` |
| **Invariant** (after the `while`) | the window is valid | the window is *not* valid; every earlier start already had its shortest window recorded |
| **Step** | add the new item to the summary | add the new item to the summary |
| **Fix** | `while broken:` drop `s[left]`, `left += 1` | `while valid:` record, drop `nums[left]`, `left += 1` |
| **Record** | after the `while` | inside the `while`, before dropping |
| **Init** | `left = 0`, empty summary, `best = 0` | `left = 0`, `total = 0`, `best = math.inf` |
| **Return** | `best` | translate `inf` into `0`, `""` or `-1` |

**From the rule to the code.** The step that freezes people is turning the problem's rule into a *summary* you can update in O(1) and a `while` condition. These cover almost every problem:

| Rule | Summary | `while` condition | Record |
|---|---|---|---|
| no repeated letter (3) | `count` dict | broken: `count[c] > 1` (only the new `c` can be doubled) | after |
| at most k distinct (904, 340) | `count`, delete zeros | broken: `len(count) > k` | after |
| at most k zeros (1004) | `zeros` | broken: `zeros > k` | after |
| at most k replacements (424) | `count`, `max_count` | broken: `(right - left + 1) - max_count > k` | after |
| sum ≥ target, no negatives (209) | `total` | valid: `total >= target` | inside |
| covers every letter of t (76) | `window`, `formed` | valid: `formed == len(need)` | inside |
| product < k, count them (713) | `prod` | broken: `prod >= k` | `count += right - left + 1` |

And the words of the idea, line by line:

| In words | In code |
|---|---|
| "the front eats the next item" | `for right, c in enumerate(s):` then `count[c] += 1` |
| "while the window is broken" | `while count[c] > 1:` |
| "the back lets go" | `count[s[left]] -= 1` then `left += 1` (in that order) |
| "the window's length" | `right - left + 1` |
| "best so far" | `best = max(best, right - left + 1)` |

```python
def longest_without_repeat(s):
    count = defaultdict(int)                 # STATE: count[c] = copies of c in s[left..right]
    left, best = 0, 0                        # INIT
    for right, c in enumerate(s):
        count[c] += 1                        # STEP: the front eats s[right]
        while count[c] > 1:                  # FIX while broken (while, not if)
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)   # RECORD: the window is valid here
    return best                              # RETURN


def shortest_with_sum_at_least(nums, target):     # non-negative numbers only
    total, left, best = 0, 0, math.inf       # STATE + INIT (inf = "not found yet")
    for right, x in enumerate(nums):
        total += x                           # STEP
        while left <= right and total >= target:  # FIX: valid, so tighten it
            best = min(best, right - left + 1)    # RECORD before breaking it
            total -= nums[left]
            left += 1
    return 0 if best == math.inf else best   # RETURN: translate "not found"


print(longest_without_repeat("abcabcbb"), longest_without_repeat("pwwkew"))   # 3 3
print(shortest_with_sum_at_least([2, 3, 1, 2, 4, 3], 7))                       # 2  ([4, 3])
```

**Try it**
- Change `while count[c] > 1:` to `if count[c] > 1:` and run `longest_without_repeat("abcbd")`. It answers 4 instead of 3: one step of `left` was not enough, so the broken window `"bcbd"` got recorded.
- Move the `best = max(...)` line *above* the `while` loop and rerun `"abcabcbb"`: you get 4, because you recorded `"abca"` before fixing it.
- In `shortest_with_sum_at_least`, move the `best = min(...)` line *below* `left += 1`: `[2, 3, 1, 2, 4, 3], 7` now answers 1 (it measured windows that were already broken).
- Feed it negatives: `shortest_with_sum_at_least([1, -1, 5, 1], 6)` says 4, but `[5, 1]` has length 2. Dropping the `1` lowered the sum, so the loop stopped before it could drop the `-1` that was in the way. The rule is not monotone any more.

### Watch it work

Each line is one step of `right`; the window is drawn under the string at its real position.

```python
def trace_longest(s):
    count, left, best = defaultdict(int), 0, 0
    print(f"{'':11}{s}")
    for right, c in enumerate(s):
        count[c] += 1
        dropped = ""
        while count[c] > 1:
            dropped += s[left]
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
        window = " " * left + s[left:right + 1]
        note = f"  (let go of {dropped!r})" if dropped else ""
        print(f"right={right:<2}:  {window:<{len(s)}}  best={best}{note}")


trace_longest("abcabcbb")
```

**Try it**
- Run `trace_longest("dvdf")` and predict the answer first (3: `"vdf"`). Watch which letters get let go when the second `d` arrives.
- Run `trace_longest("pwwkew")`: at the second `w` the window lets go of `"pw"` in one step. That is the `while` doing its job.
- Add `dict(count)` to the printed line: every letter inside the window has count 1 after the fix, which is the invariant made visible. Letters that already left still show 0; they are harmless here, but they would break a rule that counts distinct keys.

### Where it goes wrong

1. **Recording in the wrong place.** Longest → record *after* the fix. Shortest → record *inside* it. Recording above the `while` on `"abcabcbb"` gives 4.
2. **`if` instead of `while` for the fix.** One step of `left` may not be enough: `"abba"` gives 3 instead of 2, `"abcbd"` gives 4 instead of 3.
3. **Off-by-one length.** The window `[left..right]` has `right - left + 1` items; `right - left` on `"abc"` gives 2.
4. **Order of "let go".** Update the summary with `s[left]` *before* `left += 1`; doing `left += 1` first removes the wrong letter (`"abac"` gives 2 instead of 3).
5. **Distinct counts.** If the rule is "at most k distinct", the number of distinct items is `len(count)`, so delete keys that drop to 0. Without the delete, `exactly_k_distinct([1, 2, 1, 2, 3], 2)` below crashes with `IndexError`.
6. **The jump variant.** Storing `last[c]` (last index of c) lets `left` jump: `left = max(left, last[c] + 1)`. The `max` matters: on `"abba"` the second `a` must not drag `left` backwards (see the cell in Variations).
7. **Negative numbers break it.** Removing an item can make a sum *bigger*, so there is no safe moment to shrink: use prefix sums + hashmap (Prefix Sums section) or the deque follow-up at the end of this section.
8. **Degenerate parameters.** `target = 0` makes every window valid, so the shortest loop would shrink past `right` and index outside the array; `k = 0` in "exactly k" calls atMost(−1). Guard them: `while left <= right and ...`, and `if k < 0: return 0`.

### Edge cases to say out loud

Empty input · one item · all items identical · the whole input is valid · no valid window at all · `k = 0` or `target = 0` · `k >= n` · negatives (method breaks).

```python
assert longest_without_repeat("") == 0
assert longest_without_repeat("bbbb") == 1
assert longest_without_repeat("abcd") == 4               # whole string valid
assert longest_without_repeat("abba") == 2               # left never moves back
assert shortest_with_sum_at_least([1, 1, 1], 10) == 0    # nothing reaches target
assert shortest_with_sum_at_least([10], 7) == 1
assert shortest_with_sum_at_least([], 1) == 0
assert shortest_with_sum_at_least([1], 0) == 1           # target 0: any single item works
print("edge cases pass")
```

**Try it**
- Predict, then add: `assert longest_without_repeat("tmmzuxt") == 5` (the window `"mzuxt"`).
- Return `best` without translating `inf` (`return best`): which assert fails first? (`[1, 1, 1], 10` now returns `inf`.)
- Remove `left <= right and` from the shortest template and rerun: the `target = 0` assert crashes with `IndexError`, because every window is valid, even the empty one.

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Longest valid** | record after the fix | 3, 424, 904, 1004 |
| **Shortest valid** | record inside the fix | 76, 209 |
| **Fixed size k** | no `while`: once `right >= k`, item `right - k` leaves | 567, 438 (collect every start) |
| **Budget window** | rule is "spent ≤ k" (zeros flipped, letters replaced) | 1004, 424 |
| **Count windows, "exactly K"** | exactly(K) = atMost(K) − atMost(K−1); atMost adds `right - left + 1` per step | 992, 713 |
| **At most k distinct** | `len(count) > k` with zero-count keys deleted | 904 (k = 2), 340 |
| **Window max / min** | the summary is a monotonic deque of indices | 239; two deques for "max − min ≤ limit" (1438) |
| **Window median** | two heaps + lazy deletion | 480 |
| **Take from both ends** | complement: keep a middle window with sum = total − x | 1423, 1658 |
| **Sort first** | sort, then a budget window over the sorted values | 1838 |
| **Negatives allowed** | the window fails → prefix sums + increasing deque | 862 |
| **Cheapest day so far** | degenerate window: `left` jumps to today when today is cheaper | 121 |
| **Steps of word length L** | run L independent windows, one per offset | 30 |

**Fixed size**: the window length *is* the rule, so the "fix" is exactly one item leaving:

```python
def has_permutation(s1, s2):
    k, need, window = len(s1), Counter(s1), Counter()
    for right, c in enumerate(s2):
        window[c] += 1                       # STEP: item enters
        if right >= k:                       # FIX: the item k steps behind leaves
            out = s2[right - k]
            window[out] -= 1
            if window[out] == 0:
                del window[out]              # keep the two Counters comparable
        if window == need:                   # RECORD
            return True
    return False


print(has_permutation("ab", "eidbaooo"), has_permutation("ab", "eidboaoo"))   # True False
```

**Try it**
- Delete the `if window[out] == 0:` line and the `del` under it: it still prints `True False`, because since Python 3.10 `Counter` equality ignores zero counts. A plain `dict` would not (`{'a': 1, 'b': 0} != {'a': 1}`), so keep the habit.
- Change `if right >= k:` to `if right > k:`. Both calls now print `False`: the first item `s2[0]` never leaves, so the window is one item too big forever. Print `window` to see the stuck `'e'`.
- Try `has_permutation("abc", "ab")`: the window never reaches size 3, so it is `False` without any special case.
- `window == need` costs O(26) per step. The O(1) follow-up keeps a `matches` counter of letters whose counts agree; try writing it.

**Budget window with a stale maximum** (424): a window can become one repeated letter if `length − (count of its most common letter) ≤ k`. Keeping `max_count` exact while shrinking is expensive, and it turns out you never need to:

```python
def character_replacement(s, k):
    count = defaultdict(int)                 # STATE: letter counts in s[left..right]
    left = max_count = best = 0              # max_count: the highest count ever seen
    for right, c in enumerate(s):
        count[c] += 1                        # STEP
        max_count = max(max_count, count[c])
        while (right - left + 1) - max_count > k:    # FIX: too many letters to replace
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)   # RECORD
    return best


print(character_replacement("AABABBA", 1), character_replacement("ABAB", 2))   # 4 4
```

**Try it**
- Replace `max_count` in the `while` with an exact `max(count.values())`: same answers, just slower. The stale value never lets a *longer* invalid window through, because the answer only grows when some letter reaches a new highest count.
- Change `while` to `if`: still correct here (unlike Longest Substring), because the window grows by at most one per step, so it never needs to shrink by more than one.
- Trace `"AABABBA", 1` by hand: which window is the first of length 4, and which letter is replaced?

**Shortest window that covers t** (76): `formed` counts the letters of `t` that have *enough* copies; the window is valid when all of them do.

```python
def min_window(s, t):
    need, window = Counter(t), Counter()     # STATE: what t needs, what the window has
    formed, left = 0, 0                      # formed = letters of t with enough copies
    best_len, best_left = math.inf, 0
    for right, c in enumerate(s):
        window[c] += 1                       # STEP
        if c in need and window[c] == need[c]:
            formed += 1                      # this letter just became satisfied
        while formed == len(need):           # FIX: valid, so tighten it
            if right - left + 1 < best_len:  # RECORD before breaking it
                best_len, best_left = right - left + 1, left
            out = s[left]
            window[out] -= 1
            if out in need and window[out] < need[out]:
                formed -= 1                  # this letter is no longer satisfied
            left += 1
    return "" if best_len == math.inf else s[best_left:best_left + best_len]   # RETURN


print(min_window("ADOBECODEBANC", "ABC"), repr(min_window("a", "aa")))   # BANC ''
```

**Try it**
- Change `window[c] == need[c]` to `>=` and run `min_window("aab", "ab")`: it returns `'a'` instead of `'ab'`, because the second `a` counted as satisfying a letter again.
- Notice the window is stored as `(best_left, best_len)`, not as a slice, so recording stays O(1). The same trick answers the follow-up "return the substring, not its length" in every template.
- Run `min_window("ab", "b")`: the window opens at index 1. Predict the value of `formed` after each step.

**Counting windows**: "exactly K" is hard to slide directly (shrinking can't tell when to stop), but "at most K" is easy, and every window ending at `right` that starts anywhere in `[left..right]` is valid: `right - left + 1` windows.

```python
def at_most_k_distinct(nums, k):
    if k < 0:
        return 0                             # guard: no window has fewer than 0 distinct values
    count, left, windows = defaultdict(int), 0, 0
    for right, x in enumerate(nums):
        count[x] += 1                        # STEP
        while len(count) > k:                # FIX
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                del count[nums[left]]        # distinct = number of keys
            left += 1
        windows += right - left + 1          # RECORD: all valid windows ending at right
    return windows


def exactly_k_distinct(nums, k):
    return at_most_k_distinct(nums, k) - at_most_k_distinct(nums, k - 1)


print(exactly_k_distinct([1, 2, 1, 2, 3], 2), exactly_k_distinct([1, 2], 0))   # 7 0
```

**Try it**
- Print both halves: `at_most_k_distinct([1, 2, 1, 2, 3], 2)` is 12 and `at_most_k_distinct([1, 2, 1, 2, 3], 1)` is 5; 12 − 5 = 7. Write the 5 windows with one distinct value by hand.
- Remove the `if count[...] == 0:` line and the `del` under it, then run again: `IndexError`. Zero-count keys still count as distinct, so the `while` can never be satisfied and `left` runs off the end.
- Change `windows += right - left + 1` to `windows += 1`: the answer becomes 0, because you counted one window per end instead of all of them.
- Try `exactly_k_distinct([1, 2, 1, 3, 4], 3)` and predict before running (3).

**The jump variant**: remember the last index of each letter and let `left` jump straight past the old copy.

```python
def longest_without_repeat_jump(s):
    last, left, best = {}, 0, 0              # STATE: last[c] = most recent index of c
    for right, c in enumerate(s):
        if c in last:
            left = max(left, last[c] + 1)    # FIX: jump past the old copy, never backwards
        last[c] = right                      # STEP
        best = max(best, right - left + 1)   # RECORD
    return best


print(longest_without_repeat_jump("abba"), longest_without_repeat_jump("tmmzuxt"))   # 2 5
```

**Try it**
- Drop the `max(left, ...)` and write `left = last[c] + 1`: `"abba"` gives 3 and `"tmmzuxt"` gives 6. The old copy was already outside the window, so jumping to it moved `left` backwards.
- Compare with `longest_without_repeat` on `"pwwkew"`: same answer, but here each step is O(1) without an inner loop.
- What does `last` look like at the end of `"abba"`? (`{'a': 3, 'b': 2}`.)

**Window maximum**: the summary must answer "max of the window" after removals, which a counter can't do cheaply. Keep a deque of indices whose values *never increase* from front to back: a new item kicks out every item behind it that is not bigger (older *and* not bigger, so it can never be a maximum again).

```python
def window_max(nums, k):
    dq, out = deque(), []                    # STATE: indices; nums[dq] never increasing front -> back
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:      # FIX: dominated, older and not bigger
            dq.pop()
        dq.append(i)                         # STEP
        if dq[0] <= i - k:                   # the front fell out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])          # RECORD: front = max of nums[i-k+1 .. i]
    return out


print(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3, 3, 5, 5, 6, 7]
```

**Try it**
- Change `<=` to `<` in the pop condition and run `window_max([5, 5, 5, 5], 4)` with `print(len(dq))` right after `dq.append(i)`: the answers stay right, but equal values pile up (the length reaches 4 instead of staying 1).
- Delete the two lines that expire the front and run `window_max([5, 1, 1, 1], 2)`: you get `[5, 5, 5]` instead of `[5, 1, 1]`, because the 5 is reported long after it left.
- Why indices rather than values? A values-only deque can work, but it needs two extra rules (keep duplicates, and pop the front when the leaving value equals it). With indices, expiry is one comparison.
- With `k = 1` the output is the input itself: run `window_max([4, 2, 7], 1)` to confirm.

**Follow-up: what if negatives are allowed?** (862) Work on prefix sums `P`: the subarray `(i, j]` has sum `P[j] - P[i]`. For each end `j`, the useful starts are kept in a deque with increasing `P`: a start whose `P` is not smaller than a later start's is useless (the later one is shorter and at least as good).

```python
def shortest_sum_at_least_k(nums, k):
    prefix = [0] + list(accumulate(nums))
    dq, best = deque(), math.inf             # STATE: indices into prefix, prefix values increasing
    for j, p in enumerate(prefix):
        while dq and p - prefix[dq[0]] >= k: # RECORD: this start is done, j is its best end
            best = min(best, j - dq.popleft())
        while dq and prefix[dq[-1]] >= p:    # FIX: a later, lower start is strictly better
            dq.pop()
        dq.append(j)                         # STEP
    return -1 if best == math.inf else best  # RETURN


print(shortest_sum_at_least_k([2, -1, 2], 3), shortest_sum_at_least_k([1, 2], 4))   # 3 -1
```

**Try it**
- Print `prefix` for `[2, -1, 2]`: `[0, 2, 1, 3]`. Every subarray sum is a difference of two of these numbers.
- Delete the second `while` loop and run `shortest_sum_at_least_k([-5, 6], 6)`: it returns -1 instead of 1. The useless start 0 (prefix 0, higher than the later prefix −5) blocks the front of the deque.
- Run `shortest_sum_at_least_k([1, -1, 5, 1], 6)`: 2, the case where the simple template said 4.

### Say it in the interview

> "The brute force tries every start and rescans to the right: O(n²). Neighbouring windows share all but their end items, so I'll keep a window with a count map that I update in O(1) as items enter and leave. `right` adds one item per step; while the window breaks the rule I move `left`. `left` never has to come back: once a window is broken, every longer window containing it is broken too. Both pointers only move forward, so it's O(n) time and O(alphabet) space."

Then name the invariant out loud ("after this loop the window has no repeats") and point at the line where you record. Likely follow-ups and your answers:

- *Return the substring, not the length* → store `best_left` when you record.
- *Numbers can be negative* → the rule is not monotone; prefix sums with a hashmap, or the deque follow-up.
- *The input is a stream* → the window works online: it only ever needs the current window's summary.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Best Time to Buy and Sell Stock | `sliding_window/best_time_to_buy_and_sell_stock.py` | degenerate window: keep the cheapest price so far; profit = today − cheapest |
| Fruit Into Baskets | `sliding_window/fruit_into_baskets.py` | longest window with ≤ 2 distinct values; distinct = number of dict keys |
| Longest Repeating Character Replacement | `sliding_window/longest_repeating_character_replacement.py` · `practice/simple/12_longest_repeating_character_replacement.py` | valid iff length − max_count ≤ k; a stale max_count is safe because only longer windows can improve the answer |
| Longest Substring Without Repeating Characters | `sliding_window/longest_substring_without_repeating_characters.py` · `practice/simple/09_longest_substring_without_repeating_characters.py` | shrink while the new letter is doubled, or jump `left = max(left, last[c] + 1)` |
| Max Consecutive Ones III | `sliding_window/max_consecutive_ones_iii.py` | budget window: at most k zeros inside |
| Minimum Size Subarray Sum | `sliding_window/minimum_size_subarray_sum.py` | non-negative numbers: tighten while sum ≥ target, record inside the loop |
| Minimum Window Substring | `sliding_window/minimum_window_substring.py` · `practice/simple/10_minimum_window_substring.py` | `formed` counts letters with enough copies; tighten while all are satisfied |
| Permutation in String | `sliding_window/permutation_in_string.py` | fixed window of len(s1); compare letter counts |
| Shortest Subarray with Sum at Least K | `sliding_window/shortest_subarray_with_sum_at_least_k.py` | negatives break the window: prefix sums + increasing deque of starts |
| Sliding Window Maximum | `sliding_window/sliding_window_maximum.py` · `practice/simple/11_sliding_window_maximum.py` | deque of indices with never-increasing values; pop dominated items, front is the max |
| Sliding Window Median | `sliding_window/sliding_window_median.py` | two heaps (low max-heap, high min-heap) with lazy deletion of leaving items |
| Subarrays with K Different Integers | `sliding_window/subarrays_with_k_different_integers.py` | exactly K = atMost(K) − atMost(K−1); atMost adds `right - left + 1` per step |
| Substring with Concatenation of All Words | `sliding_window/substring_with_concatenation_of_all_words.py` | move in word-sized steps; one window per offset 0..L−1 |

### Self-check

1. Why does "record" sit inside the fix loop for *shortest* problems but after it for *longest* ones?
<details><summary>Answer</summary>For shortest problems, each <code>left</code> is recorded with the first <code>right</code> that makes it valid, which is its shortest window; longer windows with the same start are useless, so <code>left</code> moves on. For longest problems the window is only guaranteed valid once the loop has finished, and at that moment it is the longest valid window ending at <code>right</code>.</details>

2. Longest subarray with sum ≤ k, numbers may be negative: does the template work, and what would you do?
<details><summary>Answer</summary>No: removing a negative number from the left makes the sum larger, so the rule is not monotone. For each end j you need the earliest i with P[i] ≥ P[j] − k. Only positions where the prefix sum reaches a new maximum can be that earliest i, so keep them (their P values increase) and binary-search with bisect: O(n log n).</details>

3. In Longest Repeating Character Replacement, why is it fine to never decrease `max_count` while shrinking?
<details><summary>Answer</summary>The answer only grows when a window has a larger max_count than ever before. A stale (too large) max_count can only keep the window at a length we already achieved; it never produces a longer, invalid answer.</details>
