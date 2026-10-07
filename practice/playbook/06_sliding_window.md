## Sliding Window

> A window `[left .. right]` crawls along the array like a caterpillar: the front (`right`) takes one new item every step, the back (`left`) lets go only when the window breaks the rule. Each item enters once and leaves once, so the whole crawl is O(n).

**Reach for it when** the problem says *contiguous* (substring, subarray) and asks for the **longest**, **shortest**, or **number of** windows that satisfy a rule, and you can update the rule's bookkeeping one item at a time.

**In this repo:** `sliding_window/` (13 problems) · bank: `practice/simple/09_longest_substring_without_repeating_characters.py`, `practice/simple/10_minimum_window_substring.py`, `practice/simple/11_sliding_window_maximum.py`, `practice/simple/12_longest_repeating_character_replacement.py`

### The picture

```text
s = a b c a b c b b              rule: no repeated letter inside the window

    [a b c]                      right eats 'a' (index 3) -> 'a' is now twice inside: broken
      [b c a]                    left lets go of the old 'a' -> fixed, record length 3
        [c a b]                  same story for 'b'
             ...
                  [b]            "bb" forces left all the way up
```

Why it is fast: the brute force restarts from every `left` and re-reads the same letters. But two neighbouring windows share everything except one item at each end, so we *update* instead of *recompute*. `left` and `right` only ever move forward, each at most n steps: O(n) total, even though there is a loop inside a loop.

### From idea to code

**The idea in one sentence:** *grow the window by one item; while it breaks the rule, shrink it from the left; now it is the best valid window that ends at `right`, so record it.*

Before typing, answer these seven questions (the same seven work for every technique in this notebook):

| Decision | Sliding-window answer |
|---|---|
| **State**: what must I remember? | `left`, plus a **summary** of the window that updates in O(1) when one item enters or leaves: a count dict, a running sum, the number of zeros, the number of distinct letters |
| **Definition**: what exactly does each variable mean? | write it as a comment: `count[c] = copies of c inside s[left..right]` |
| **Invariant**: what is true at the end of every step? | after the shrink loop, `s[left..right]` obeys the rule |
| **Step**: how does one item change the state? | add `s[right]` to the summary; then `while broken: remove s[left]; left += 1` |
| **Record**: when is the answer updated? | *longest*: after the shrink loop (the window is valid). *shortest*: inside the shrink loop, before you break it |
| **Init**: starting values | `left = 0`, empty summary, `best = 0` (longest) or `math.inf` (shortest) |
| **Return**: what comes back, and for "not found"? | `best`, translating `inf` into `0`, `""` or `-1` as the problem asks |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "take the next item" | `for right, c in enumerate(s):` |
| "put it in the window" | `count[c] += 1` |
| "while the window breaks the rule" | `while count[c] > 1:` (the rule is problem-specific) |
| "let go of the leftmost item" | `count[s[left]] -= 1` then `left += 1` (in that order) |
| "the window's length" | `right - left + 1` |
| "best so far" | `best = max(best, right - left + 1)` |

Two templates cover most problems. The tags in the comments are the decisions above:

```python
def longest_without_repeat(s):
    count = defaultdict(int)                 # STATE: count[c] = copies of c in s[left..right]
    left, best = 0, 0                        # INIT
    for right, c in enumerate(s):            # STEP: the front eats one item
        count[c] += 1
        while count[c] > 1:                  # SHRINK while broken (while, not if)
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)   # RECORD: the window is valid here
    return best


def shortest_with_sum_at_least(nums, target):     # positive numbers only
    total, left, best = 0, 0, math.inf       # STATE + INIT (inf = "not found yet")
    for right, x in enumerate(nums):
        total += x                           # STEP
        while total >= target:               # valid: try to make it shorter
            best = min(best, right - left + 1)   # RECORD before breaking it
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
- Feed it negatives: `shortest_with_sum_at_least([1, -1, 5, 1], 6)` says 4, but `[5, 1]` has length 2. Dropping the `1` lowered the sum, so the loop stopped before it could drop the `-1` that was in the way. This is why negatives need another tool.

### Watch it work

Each line is one step of `right`; the window is drawn under the string at its real position.

```python
def trace_longest(s):
    count, left, best = defaultdict(int), 0, 0
    print(f"{'':10}{s}")
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
        print(f"right={right}:  {window:<{len(s)}}  best={best}{note}")


trace_longest("abcabcbb")
```

**Try it**
- Run `trace_longest("dvdf")` and predict the answer first (3: `"vdf"`). Watch which letters get let go when the second `d` arrives.
- Run `trace_longest("pwwkew")`: at the second `w` the window lets go of `"pw"` in one step. That is the `while` doing its job.
- Add `dict(count)` to the printed line: every letter inside the window has count 1 after the shrink; that is the invariant made visible.

### Where it goes wrong

1. **Recording in the wrong place.** Longest → record *after* the shrink loop. Shortest → record *inside* it. Swap them and you record broken windows.
2. **`if` instead of `while` for shrinking.** One step of `left` may not be enough (`"abcb"`: the new `b` forces `left` past `a` *and* `b`).
3. **Off-by-one length.** The window `[left..right]` has `right - left + 1` items.
4. **Order of "let go".** Update the summary with `s[left]` *before* `left += 1`, or you remove the wrong item.
5. **Distinct counts.** If the rule is "at most k distinct", the number of distinct items is `len(count)`, so delete keys that drop to 0.
6. **The jump variant.** Storing `last[c]` (last index of c) lets `left` jump: `left = max(left, last[c] + 1)`. The `max` matters: on `"abba"`, the second `a` must not drag `left` backwards.
7. **Negative numbers break it.** Shrinking only helps if removing an item can only *fix* the rule. With negatives, removing an item can make the sum *bigger*, so there is no safe moment to shrink: use prefix sums + hashmap (section on prefix sums) or a monotonic deque (Variation below).

### Edge cases to say out loud

Empty input · one item · all items identical · the whole input is valid · no valid window at all · `k = 0` · `k >= n` · negatives (method breaks).

```python
assert longest_without_repeat("") == 0
assert longest_without_repeat("bbbb") == 1
assert longest_without_repeat("abcd") == 4               # whole string valid
assert longest_without_repeat("abba") == 2               # left never moves back
assert shortest_with_sum_at_least([1, 1, 1], 10) == 0    # nothing reaches target
assert shortest_with_sum_at_least([10], 7) == 1
assert shortest_with_sum_at_least([], 1) == 0
print("edge cases pass")
```

**Try it**
- Predict, then add: `assert longest_without_repeat("tmmzuxt") == 5` (the window `"mzuxt"`).
- Change the `"abba"` expectation to 3 to see what a failing check looks like, then put it back.
- What should `shortest_with_sum_at_least([5], 5)` return? Write the assert before running it (the answer is 1: a window can be a single item).

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Longest valid** | record after the shrink loop | 3, 424, 904, 1004 |
| **Shortest valid** | record inside the shrink loop | 76, 209 |
| **Fixed size k** | no shrink loop: once `right >= k`, item `right - k` leaves | 567 |
| **Budget window** | rule is "spent ≤ k" (zeros flipped, letters replaced) | 1004, 424 |
| **Count windows, "exactly K"** | exactly(K) = atMost(K) − atMost(K−1); atMost adds `right - left + 1` per step | 992 |
| **Window max / min** | summary is a monotonic deque of indices, front = answer | 239 |
| **Window median** | two heaps + lazy deletion | 480 |
| **Negatives allowed** | sliding window fails → prefix sums + increasing deque | 862 |
| **Window of size 1..n with a running best** | degenerate window: just keep the minimum so far | 121 |
| **Steps of word length L** | run L independent windows, one per offset | 30 |

**Fixed size**: the window length *is* the rule, so the "shrink" is exactly one item:

```python
def has_permutation(s1, s2):
    k, need, window = len(s1), Counter(s1), Counter()
    for right, c in enumerate(s2):
        window[c] += 1                       # item enters
        if right >= k:                       # item k steps behind leaves
            out = s2[right - k]
            window[out] -= 1
            if window[out] == 0:
                del window[out]              # keep the two Counters comparable
        if window == need:
            return True
    return False


print(has_permutation("ab", "eidbaooo"), has_permutation("ab", "eidboaoo"))   # True False
```

**Try it**
- Delete the two `del window[out]` lines: it still prints `True False`, because since Python 3.10 `Counter` equality ignores zero counts. A plain `dict` would not (`{'a': 1, 'b': 0} != {'a': 1}`), so keep the habit.
- Change `if right >= k:` to `if right > k:`. Both calls now print `False`: the first item `s2[0]` never leaves, so the window is one item too big forever. Print `window` to see the stuck `'e'`.
- Try `has_permutation("abc", "ab")`: the window never reaches size 3, so it is `False` without any special case.

**Counting windows**: "exactly K" is hard to slide directly (shrinking can't tell when to stop), but "at most K" is easy, and every window ending at `right` that starts anywhere in `[left..right]` is valid: that is `right - left + 1` windows.

```python
def at_most_k_distinct(nums, k):
    count, left, windows = defaultdict(int), 0, 0
    for right, x in enumerate(nums):
        count[x] += 1
        while len(count) > k:
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                del count[nums[left]]        # distinct = number of keys
            left += 1
        windows += right - left + 1          # all valid windows ending at right
    return windows


def exactly_k_distinct(nums, k):
    return at_most_k_distinct(nums, k) - at_most_k_distinct(nums, k - 1)


print(exactly_k_distinct([1, 2, 1, 2, 3], 2))   # 7
```

**Try it**
- Print both halves: `at_most_k_distinct([1, 2, 1, 2, 3], 2)` is 12 and `at_most_k_distinct([1, 2, 1, 2, 3], 1)` is 5; 12 − 5 = 7. Write the 5 windows with one distinct value by hand.
- Remove the `del count[...]` line and run again: `IndexError`. Zero-count keys still count as distinct, so the `while` can never be satisfied and `left` runs off the end.
- Change `windows += right - left + 1` to `windows += 1`: the answer becomes 0, because you counted one window per end instead of all of them.
- Try `exactly_k_distinct([1, 2, 1, 3, 4], 3)` and predict before running (3).

**Window maximum**: the summary must answer "max of the window" after removals, which a counter can't do cheaply. Keep a deque of indices whose values *decrease* from front to back: a new item kicks out every smaller item behind it (they are older *and* smaller, so they can never be a maximum again).

```python
def window_max(nums, k):
    dq, out = deque(), []                    # indices; nums[dq] decreasing front -> back
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:      # dominated: older and not bigger
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                   # front fell out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])          # front = max of nums[i-k+1 .. i]
    return out


print(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3, 3, 5, 5, 6, 7]
```

**Try it**
- Change `<=` to `<` in the pop condition and run `window_max([5, 5, 5, 5], 2)`: the answers stay right, but equal values pile up in the deque (print `len(dq)` inside the loop: it reaches 3 instead of 1).
- Delete the two lines that expire the front and run `window_max([5, 1, 1, 1], 2)`: you get `[5, 5, 5]` instead of `[5, 1, 1]`, because the 5 is reported long after it left.
- Why store *indices* rather than values? Try rewriting with values and notice you can no longer tell when the front has left the window.
- With `k = 1` the output is the input itself: run `window_max([4, 2, 7], 1)` to confirm.

**When negatives break the window** (862): work on prefix sums `P`. The subarray `(i, j]` has sum `P[j] - P[i]`. For each end `j`, the useful starts are kept in a deque with increasing `P`: a start whose `P` is not smaller than a later start's is useless (the later one is shorter and at least as good).

```python
def shortest_sum_at_least_k(nums, k):
    prefix = [0] + list(accumulate(nums))
    dq, best = deque(), math.inf             # indices into prefix, prefix values increasing
    for j, p in enumerate(prefix):
        while dq and p - prefix[dq[0]] >= k: # this start is done: j is its best end
            best = min(best, j - dq.popleft())
        while dq and prefix[dq[-1]] >= p:    # a later, lower start is strictly better
            dq.pop()
        dq.append(j)
    return -1 if best == math.inf else best


print(shortest_sum_at_least_k([2, -1, 2], 3), shortest_sum_at_least_k([1, 2], 4))   # 3 -1
```

**Try it**
- Print `prefix` for `[2, -1, 2]`: `[0, 2, 1, 3]`. Every subarray sum is a difference of two of these numbers.
- Delete the second `while` loop and run `shortest_sum_at_least_k([-5, 6], 6)`: it returns -1 instead of 1. The useless start 0 (prefix 0, higher than the later prefix −5) blocks the front of the deque.
- Run `shortest_sum_at_least_k([1, -1, 5, 1], 6)`: 2, the case where the simple template said 4.
- Compare with `shortest_with_sum_at_least` on positive inputs: same lengths, except "not found" is -1 here and 0 there. Read the problem for which one it wants.

### Say it in the interview

> "The brute force tries every start and rescans to the right: O(n²). Neighbouring windows share all but their end items, so I'll keep a window with a count map that I update in O(1) as items enter and leave. `right` adds one item per step; while the window breaks the rule I move `left`. Both pointers only move forward, so it's O(n) time and O(alphabet) space."

Then name the invariant out loud ("after this loop the window has no repeats") and point at the line where you record. Interviewers love hearing *why* the record goes there.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Best Time to Buy and Sell Stock | `sliding_window/best_time_to_buy_and_sell_stock.py` | degenerate window: keep the cheapest price so far; profit = today − cheapest |
| Fruit Into Baskets | `sliding_window/fruit_into_baskets.py` | longest window with ≤ 2 distinct values; distinct = number of dict keys |
| Longest Repeating Character Replacement | `sliding_window/longest_repeating_character_replacement.py` · `practice/simple/12_longest_repeating_character_replacement.py` | valid iff length − max_count ≤ k; a stale max_count is safe because only longer windows can improve the answer |
| Longest Substring Without Repeating Characters | `sliding_window/longest_substring_without_repeating_characters.py` · `practice/simple/09_longest_substring_without_repeating_characters.py` | shrink while the new letter is doubled, or jump `left = max(left, last[c] + 1)` |
| Max Consecutive Ones III | `sliding_window/max_consecutive_ones_iii.py` | budget window: at most k zeros inside |
| Minimum Size Subarray Sum | `sliding_window/minimum_size_subarray_sum.py` | positives only: shrink while sum ≥ target, record inside the shrink loop |
| Minimum Window Substring | `sliding_window/minimum_window_substring.py` · `practice/simple/10_minimum_window_substring.py` | `formed` counts letters with enough copies; shrink while all are satisfied |
| Permutation in String | `sliding_window/permutation_in_string.py` | fixed window of len(s1); compare letter counts |
| Shortest Subarray with Sum at Least K | `sliding_window/shortest_subarray_with_sum_at_least_k.py` | negatives break the window: prefix sums + increasing deque of starts |
| Sliding Window Maximum | `sliding_window/sliding_window_maximum.py` · `practice/simple/11_sliding_window_maximum.py` | deque of indices with decreasing values; pop dominated items, front is the max |
| Sliding Window Median | `sliding_window/sliding_window_median.py` | two heaps (low max-heap, high min-heap) with lazy deletion of leaving items |
| Subarrays with K Different Integers | `sliding_window/subarrays_with_k_different_integers.py` | exactly K = atMost(K) − atMost(K−1); atMost adds `right - left + 1` per step |
| Substring with Concatenation of All Words | `sliding_window/substring_with_concatenation_of_all_words.py` | move in word-sized steps; one window per offset 0..L−1 |

### Self-check

1. Why does "record" sit inside the shrink loop for *shortest* problems but after it for *longest* ones?
<details><summary>Answer</summary>Inside the loop the window is still valid, and each shrink makes it shorter, so every valid length gets recorded before the window breaks. For longest problems the window is only guaranteed valid once the loop has finished, and at that moment it is the longest valid window ending at <code>right</code>.</details>

2. Longest subarray with sum ≤ k, numbers may be negative: does the template work?
<details><summary>Answer</summary>No. Removing a negative number from the left makes the sum larger, so shrinking can make things worse and there is no safe moment to stop. Use prefix sums with a sorted structure or a monotonic deque instead.</details>

3. In Longest Repeating Character Replacement, why is it fine to never decrease `max_count` while shrinking?
<details><summary>Answer</summary>The answer only grows when a window has a larger max_count than ever before. A stale (too large) max_count can only keep the window at a length we already achieved; it never produces a longer, invalid answer.</details>
