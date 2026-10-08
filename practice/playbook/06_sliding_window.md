## Sliding Window

> A window `[left .. right]` crawls along the array like a caterpillar. Its front, `right`, takes one new item every step; its back, `left`, moves only to repair the window in longest problems or to tighten it in shortest ones. Each item enters once and leaves once, so the whole crawl is O(n).

[Two Pointers](#s05) moved two fingers toward each other, and every move was a proof that killed a row of pairs. A window is two fingers that both move right, and its proof is that a broken window stays broken: no longer window that contains it can be valid, so the back finger never has to move back.

**Reach for it when** the problem says *contiguous*, a substring or a subarray, and asks for the **longest**, **shortest**, or **number of** windows that satisfy a rule, and the rule is **monotone**: adding an item can never repair a broken window. Quick test: "can adding one more item make a bad window good again?" If yes, as for a sum with negative numbers, this tool does not apply; use [Prefix Sums](#s04) instead.

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

**Why it is correct:** if `[left..right]` is broken, every window that starts at or before `left` and ends at or after `right` contains it, so it is broken too; that is what "monotone" buys. The start `left` is finished for good, which is why `left` never moves back. And once the window is repaired, every window `[i..right]` with `left ≤ i ≤ right` sits inside it and is valid too: `right - left + 1` valid windows end at `right`. Negative numbers break exactly this argument.

### From idea to code

**The idea in one sentence:** *the front eats one item; then the back moves until the window is the best it can be for this front, repaired for longest and as tight as possible for shortest, and the answer is recorded at the moment the window is known to be valid.*

Longest Substring Without Repeating Characters (3) asks for the longest stretch with no letter twice, and it is the template for every *longest* window. Its **State** is the back finger `left` plus a summary of the window, and the summary's **Definition** is `count[c]`, the copies of `c` in `s[left..right]`. The **Invariant** holds after the repair loop: the window is valid. A **Step** adds `s[right]` to the summary, and the **Fix** drops `s[left]` and moves `left` while the window is broken.

The **Record** comes after the fix, because only then is the window valid, and at that moment it is the longest valid window ending at `right`. **Init** is `left = 0`, an empty summary and `best = 0`, and the **Return** is `best`.

Minimum Size Subarray Sum (209) asks for the shortest subarray whose sum reaches a target, and it turns the loop inside out for every *shortest* window. Its summary is `total`, the sum of `nums[left..right]`, and its fix runs *while the window is valid*: record, then drop `nums[left]`, because a longer window with the same start is useless. After that loop the window is *not* valid, and every earlier start has had its shortest window recorded. Init is `best = math.inf`, and the return translates `inf` into 0, `""` or −1.

The step that freezes people is turning the rule into a summary that updates in O(1) and a `while` condition. "No repeated letter" keeps a `count` dict and is broken when `count[c] > 1`: only the new letter `c` can be the doubled one. "At most k distinct" keeps the same dict, deletes keys that fall to zero, and is broken when `len(count) > k`. That is Fruit Into Baskets (904), the longest stretch of trees holding at most two kinds of fruit, and Longest Substring with At Most K Distinct Characters (340).

Budget rules count what the window spends. Max Consecutive Ones III (1004), the longest run of 1s once at most k zeros are flipped, keeps `zeros` and is broken when `zeros > k`. Longest Repeating Character Replacement (424), the longest stretch that becomes one repeated letter after at most k replacements, keeps `count` and `max_count` and is broken when `(right - left + 1) - max_count > k`. Every rule so far records after the fix.

Shortest rules are *valid* conditions, and they record inside the fix. Minimum Size Subarray Sum, with no negative numbers, stays valid while `total >= target`. Minimum Window Substring (76), the shortest stretch of `s` that holds every letter of `t` with its count, keeps `window` and `formed` and stays valid while `formed == len(need)`. Counting rules record on every step: Subarray Product Less Than K (713), how many subarrays have a product below k, is broken when `prod >= k` and records `count += right - left + 1`.

The first function solves Longest Substring Without Repeating Characters: `"abcabcbb" → 3`, for `"abc"`. Its words become lines one by one: the front eats the next letter, `count[c] += 1`; while the window is broken, `while count[c] > 1:`, the back lets go, `count[s[left]] -= 1` and then `left += 1`, in that order; the length is `right - left + 1`. The second function solves Minimum Size Subarray Sum: `[2, 3, 1, 2, 4, 3]` with target 7 gives 2, for `[4, 3]`, recorded inside the loop while the window is still valid.

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
- In `shortest_with_sum_at_least`, move the `best = min(...)` line *below* `left += 1`: `[2, 3, 1, 2, 4, 3], 7` now answers 1, because it measured windows that were already broken.
- Feed it negatives: `shortest_with_sum_at_least([1, -1, 5, 1], 6)` says 4, but `[5, 1]` has length 2. Dropping the `1` lowered the sum, so the loop stopped before it could drop the `-1` that was in the way. The rule is not monotone any more.

### Watch it work

The trace runs the first template on `"abcabcbb"` and prints one line per step of `right`, with the window drawn under the string at its real position. Watch `left`: it only ever moves forward, sometimes by two letters at once, and `best` never shrinks.

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
6. **The jump variant.** Storing `last[c]`, the last index of c, lets `left` jump: `left = max(left, last[c] + 1)`. The `max` matters: without it, `"abba"` gives 3 instead of 2, because the second `a` drags `left` backwards (the cell in Variations shows it).
7. **Negative numbers break it.** Removing an item can make a sum *bigger*, so there is no safe moment to shrink: use prefix sums with a hash map ([Prefix Sums](#s04)) or the deque follow-up at the end of this section. The map answers an exact sum, the deque a sum of at least k. `shortest_with_sum_at_least([1, -1, 5, 1], 6)` says 4, but `[5, 1]` has length 2.
8. **Degenerate parameters.** `target = 0` makes every window valid, even the empty one, so the shortest loop shrinks past `right` and reads outside the array: `[1]` with target 0 raises `IndexError` without the guard. `k = 0` in "exactly k" calls atMost(−1), and `exactly_k_distinct([1, 2], 0)` raises `IndexError` too. Guard them: `while left <= right and ...`, and `if k < 0: return 0`.

### Edge cases to say out loud

Empty input · one item · all items identical · the whole input is valid · no valid window at all · `k = 0` or `target = 0` · `k >= n` · negatives (method breaks). The asserts below check the cases that apply to the two templates.

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

Each variation keeps the crawl and changes one thing: the rule, the summary, or what is recorded. The table is the overview, and the cells after it follow its order.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Longest valid** | record after the fix | Longest Substring Without Repeating Characters (3), Longest Repeating Character Replacement (424), Fruit Into Baskets (904), Max Consecutive Ones III (1004) |
| **Shortest valid** | record inside the fix | Minimum Size Subarray Sum (209), Minimum Window Substring (76) |
| **Fixed size k** | no `while`: once `right >= k`, item `right - k` leaves | Permutation in String (567): does `s2` contain an anagram of `s1`; Find All Anagrams in a String (438): every start of one |
| **Budget window** | the rule is "spent ≤ k": zeros flipped, letters replaced | Longest Repeating Character Replacement (424), Max Consecutive Ones III (1004) |
| **Shortest cover** | `formed` counts the letters of `t` that have enough copies | Minimum Window Substring (76) |
| **Count windows, "exactly K"** | exactly(K) = atMost(K) − atMost(K−1); atMost adds `right - left + 1` per step | Subarrays with K Different Integers (992): subarrays with exactly K distinct values; Subarray Product Less Than K (713) |
| **At most k distinct** | `len(count) > k`, with zero-count keys deleted | Fruit Into Baskets (904), where k = 2; Longest Substring with At Most K Distinct Characters (340) |
| **Jump instead of shrink** | `last[c]` lets `left` jump: `left = max(left, last[c] + 1)` | Longest Substring Without Repeating Characters (3) |
| **Window max / min** | the summary is a monotonic deque of indices | Sliding Window Maximum (239): the max of every window of size k; Longest Continuous Subarray With Absolute Diff ≤ Limit (1438): two deques |
| **Take from both ends** | complement: keep a middle window with sum = total − x | Maximum Points You Can Obtain from Cards (1423): k cards from the two ends; Minimum Operations to Reduce X to Zero (1658): remove from the ends until x is used up |
| **Sort first** | sort, then a budget window over the sorted values | Frequency of the Most Frequent Element (1838): the highest count of one value after at most k increments |
| **Cheapest day so far** | degenerate window: `left` jumps to today when today is cheaper | Best Time to Buy and Sell Stock (121): the best profit from one buy and a later sell |
| *Second pass:* **negatives allowed** | the window fails: prefix sums and an increasing deque of starts | Shortest Subarray with Sum at Least K (862): the shortest subarray reaching k, negatives allowed |
| *Second pass:* **window median** | two heaps with lazy deletion | Sliding Window Median (480): the median of every window of size k |
| *Second pass:* **steps of word length L** | L independent windows over word-sized chunks, one per offset | Substring with Concatenation of All Words (30): every start of all the words glued in any order |

**Fixed size.** The simplest change comes first: the window length *is* the rule, so the fix is exactly one item leaving. Permutation in String asks whether `s2` contains a block that is an anagram of `s1`: `"ab"` in `"eidbaooo"` is True, thanks to `"ba"`. Slide a window of `len(s1)` letters over `s2`, keep its letter counts, and compare them with the counts of `s1` after every step.

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
- `window == need` costs O(26) per step. Write the O(1) follow-up, a `matches` counter of the letters whose counts agree, and check that it prints `True False` too.

**Budget window with a stale maximum.** A budget is the next step up: the window may hold some bad items, as long as it can pay for them. Longest Repeating Character Replacement asks for the longest stretch that can become one repeated letter after at most k replacements: `"AABABBA"` with k = 1 gives 4. A window qualifies when its length minus the count of its most common letter is at most k. Keeping `max_count` exact while shrinking is expensive, and it never needs to be.

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
- Change `while` to `if`: still correct here, unlike Longest Substring, because the window grows by at most one per step, so it never needs to shrink by more than one.
- Trace `"AABABBA", 1` by hand, then print `left, right` at each record to check: which window is the first of length 4, and which letter is replaced?

**Shortest window that covers t.** Back to the shortest template, now with a richer summary. Minimum Window Substring asks for the shortest stretch of `s` that contains every letter of `t`, copies included: `"ADOBECODEBANC"` with `t = "ABC"` gives `"BANC"`. Comparing whole counters on every step would cost O(alphabet), so `formed` counts the letters of `t` that already have *enough* copies, and the window is valid when all of them do.

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
- Record the slice instead, `best = s[left:right + 1]` whenever it is shorter: the answers stay the same, but every record now copies the window. Storing `(best_left, best_len)` keeps the record O(1), and it answers "return the substring, not its length" in every template.
- Run `min_window("ab", "b")`: the window opens at index 1. Predict the value of `formed` after each step, then print it.

**Counting windows.** Counting is the third thing a window can record. Subarrays with K Different Integers asks how many subarrays hold exactly K distinct values: `[1, 2, 1, 2, 3]` with K = 2 has 7. "Exactly K" is hard to slide directly, because shrinking cannot tell when to stop, but "at most K" is easy: every window ending at `right` that starts anywhere in `[left..right]` is valid, which is `right - left + 1` windows. So exactly(K) = atMost(K) − atMost(K − 1).

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

**The jump variant.** Longest Substring Without Repeating Characters has a faster fix than letting go one letter at a time. Remember the last index of each letter, and when a letter repeats, let `left` jump straight past its old copy. The `max` keeps `left` from moving backwards when that old copy already lies outside the window: `"abba"` gives 2 and `"tmmzuxt"` gives 5.

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
- Print `last` at the end of `"abba"` and predict it first (`{'a': 3, 'b': 2}`).

**Window maximum.** The last summary answers a question no counter can: the maximum of the window after items have left it. Sliding Window Maximum asks for the maximum of every window of size k: `[1, 3, -1, -3, 5, 3, 6, 7]` with k = 3 gives `[3, 3, 5, 5, 6, 7]`. The summary is a deque of indices whose values never increase from front to back, a *monotonic* deque.

A new item kicks out every item behind it that is not bigger: older and not bigger, such an item can never be a maximum again. The front is then the maximum of the window, and it leaves the moment it falls out of the window. Each index is pushed once and popped at most once, so the whole pass is O(n).

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
- Change `<=` to `<` in the pop condition and run `window_max([5, 5, 5, 5], 4)` with `print(len(dq))` right after `dq.append(i)`: the answers stay right, but equal values pile up, and the length reaches 4 instead of staying 1.
- Delete the two lines that expire the front and run `window_max([5, 1, 1, 1], 2)`: you get `[5, 5, 5]` instead of `[5, 1, 1]`, because the 5 is reported long after it left.
- Store values instead of indices: append `x`, pop while `dq[-1] <= x`, and expire with `if i >= k and dq[0] == nums[i - k]: dq.popleft()`. `window_max([3, 3, 1], 2)` gives `[3, 1]` instead of `[3, 3]`, because the expiry removed the newer 3. A values deque needs `<` in the pop to keep duplicates; with indices, expiry is one comparison.
- With `k = 1` the output is the input itself: run `window_max([4, 2, 7], 1)` to confirm.

Three mediums reuse these windows with one twist each. Maximum Points You Can Obtain from Cards takes k cards from the two ends, and Minimum Operations to Reduce X to Zero removes items from the two ends until they sum to x. Both flip into a middle window, the items left behind: the n − k cards with the smallest sum, or the longest stretch whose sum is total − x.

Frequency of the Most Frequent Element sorts first, because after sorting the cheapest values to raise to `nums[right]` are its nearest left neighbours. A window can be raised to its last value for `nums[right] * length - window_sum` increments, so it is broken when that cost passes k, and the longest unbroken window is the answer.

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

**Negatives allowed.** Shortest Subarray with Sum at Least K is Minimum Size Subarray Sum with negative numbers allowed: `[2, -1, 2]` with k = 3 gives 3, the whole array. The window fails, so work on prefix sums `P`, where the subarray `(i, j]` has sum `P[j] - P[i]`. For each end `j`, keep the useful starts in a deque with increasing `P`. A start whose `P` is not smaller than a later start's is useless, because the later one is shorter and at least as good.

```python
def shortest_sum_at_least_k(nums, k):
    prefix = [0] + list(accumulate(nums))
    dq, best = deque(), math.inf             # STATE: indices into prefix, prefix values increasing
    for j, p in enumerate(prefix):
        while dq and p - prefix[dq[0]] >= k: # this start is done: j is its best end
            best = min(best, j - dq.popleft())   # RECORD
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

Sliding Window Median asks for the median of every window of size k: `[1, 3, -1, -3, 5, 3, 6, 7]` with k = 3 gives `[1, -1, -1, 3, 5, 6]`. Keep the window in the two heaps of the median finder from [Heaps](#s13), a max-heap for the lower half and a min-heap for the upper half. A heap cannot delete from its middle, so a leaving item is only noted in a dict of pending deletions and popped once it reaches a top: lazy deletion. Balance the halves by their live counts, never by their lengths.

Substring with Concatenation of All Words asks for every start of a block made of all the given words, each used once, in any order; the words share one length L. `"barfoothefoobarman"` with `["foo", "bar"]` gives `[0, 9]`. Cut `s` into chunks of length L, once for each offset 0..L−1, and slide a counting window over the chunks, as in Permutation in String. A chunk that is not a word empties the window, and a word seen too often shrinks it from the left: O(n · L) in total.

### Say it in the interview

> "The brute force tries every start and rescans to the right: O(n²). Neighbouring windows share all but their end items, so I'll keep a window with a count map that I update in O(1) as items enter and leave. `right` adds one item per step; while the window breaks the rule I move `left`. `left` never has to come back: once a window is broken, every longer window containing it is broken too. Both pointers only move forward, so it's O(n) time and O(alphabet) space."

Then name the invariant out loud ("after this loop the window has no repeats") and point at the line where you record. Likely follow-ups and your answers:

- *Return the substring, not the length* → store `best_left` when you record.
- *Numbers can be negative* → the rule is not monotone; prefix sums with a hash map, or the deque follow-up.
- *The input is a stream* → the window works online: it only ever needs the current window's summary.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Best Time to Buy and Sell Stock | `sliding_window/best_time_to_buy_and_sell_stock.py` | degenerate window: keep the cheapest price so far; profit = today − cheapest (coded in [From Idea to Code](#s01)) |
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
<details><summary>Answer</summary>No: removing a negative number from the left makes the sum larger, so the rule is not monotone. For each end j you need the earliest i with P[i] ≥ P[j] − k. Only positions where the prefix sum reaches a new maximum can be that earliest i, so keep them, in increasing order of P, and binary-search them with bisect: O(n log n).</details>

3. In Longest Repeating Character Replacement, why is it fine to never decrease `max_count` while shrinking?
<details><summary>Answer</summary>The answer only grows when a window has a larger max_count than ever before. A stale, too-large max_count can only keep the window at a length already achieved; it never produces a longer, invalid answer.</details>
