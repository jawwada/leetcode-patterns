## Two Pointers

> Two fingers on the array. Each step looks at the items under the fingers and moves one finger, and every move is a small *proof*: it throws away a whole family of candidates that cannot win. About n moves replace the n² pairs of the brute force.

**Reach for it when** the input is sorted (or you may sort it) and the question is about pairs or triplets ("sum to target", "how many pairs", "all unique triplets"); you compare mirror positions (palindromes, reversing); you must rewrite an array **in place** with O(1) extra space ("remove", "move the zeros", "dedupe", "partition into groups"); two sorted inputs must be merged or compared; or the answer is the area between two walls (container, trapped water).

**In this repo:** `two_pointers/` (10 problems) · bank: `practice/simple/06_three_sum.py`, `practice/simple/07_container_with_most_water.py`, `practice/simple/08_trapping_rain_water.py` · basics: `practice/simple/basics/strings/02_two_pointer_palindromes_and_reverse_words.py`, `practice/simple/basics/sorting/03_quick_sort.py` (partition is a read / write pass), `practice/simple/basics/sorting/02_merge_sort.py` (merge is one finger per sorted list) · the same idea elsewhere: `linked_list/remove_nth_from_end.py` (two pointers with a fixed gap, [Linked Lists](#s10))

### The picture

Write down every pair as a table: one row per left item, one column per right item. The two fingers walk this table from its top-right corner.

```text
nums = [1, 2, 4, 6, 8, 9], target = 12       (row = left item, column = right item)

        2    4    6    8    9
  1     .    .    .    .   10 <     1 + 9 too small, and 9 was the biggest partner left: row 1 is dead
  2          .    .    .   11 <     the same for 2
  4               .   12 = 13 >     4 + 9 too big, and 4 was the smallest partner left: column 9 is dead;
  6                    .    .       then 4 + 8 = 12: found
  8                         .
```

Why it is fast: each comparison kills a whole row or a whole column of the table, so the walk is a staircase from the top-right corner: at most n − 1 steps instead of n² pairs. The answer is never killed, because only rows and columns proven hopeless are.

Four shapes cover almost every problem:

```text
opposite ends     L ->               <- R     pairs in sorted data, palindromes, containers, rain water
same direction    W ->  R ->                  read / write: keep some items, in place (W never passes R)
two inputs        i -> in a,  j -> in b       merge, subsequence, intersections, compare
three regions     low, mid, high              Dutch flag: [ 0s | 1s | unknown | 2s ]
```

### From idea to code

**The idea in one sentence:** *opposite ends: the comparison of the two ends tells you which one can never be part of a better answer, so move that finger inward until they meet. Same direction: read every item once, and copy each keeper to slot `write`.*

| Decision | Opposite ends (pair in sorted data) | Same direction (read / write) |
|---|---|---|
| **State**: what must I remember? | `lo`, `hi` | `write`, the next free slot (`read` scans) |
| **Definition**: what exactly does each variable mean? | the candidates still alive are `nums[lo..hi]` | `nums[:write]` is the finished output |
| **Invariant**: what is true at the end of every step? | if an answer exists, both of its indices are in `[lo, hi]` | `nums[:write]` = the keepers of `nums[:read]`, in order (so `write <= read`, and nothing unread is overwritten) |
| **Step**: how does one item change the state? | too small → `lo += 1`; too big → `hi -= 1` | if `nums[read]` is a keeper: `nums[write] = nums[read]`, `write += 1` |
| **Record**: when is the answer updated? | when the sum hits (or update a best on *every* step) | at the copy |
| **Init**: starting values | `lo, hi = 0, len(nums) - 1` (sort first if allowed) | `write = 0` |
| **Return**: what comes back, and for "not found"? | the hit, or "not found" once `lo >= hi` | `write`, the new length |

```text
read / write:   [ kept  kept  kept | junk  junk | unread  unread ]
                                     ^            ^
                                   write        read
```

**From the comparison to the move.** Every opposite-ends problem is one comparison and a move that the comparison justifies:

| Problem | Compare | Move, and what it proves | Record |
|---|---|---|---|
| pair = target (167) | `a[lo] + a[hi]` vs target | small → `lo += 1` (row dead); big → `hi -= 1` (column dead) | at the hit |
| count pairs below target (2824, 259) | the same | fits → `count += hi - lo`, then `lo += 1` (the whole row fits); else `hi -= 1` | in the move |
| triangles (611) | `a[lo] + a[hi]` vs the longest side `a[k]` | bigger → `count += hi - lo`, then `hi -= 1`; else `lo += 1` | in the move |
| closest sum (16) | the same as 167 | the same as 167 | the best distance, every step |
| container (11) | `h[lo]` vs `h[hi]` | move the shorter wall: it has met its best partner | the area, every step |
| rain water (42) | `h[lo]` vs `h[hi]` | the lower side's water level is known: settle it, move on | at the settle |
| boats (881) | lightest + heaviest vs the limit | the heaviest always leaves; the lightest joins it if they fit | one boat per step |
| palindrome (125) | `s[lo]` vs `s[hi]` | junk: move that finger alone; a match: move both | `False` at a mismatch |
| squares (977) | `abs(a[lo])` vs `abs(a[hi])` | the bigger end's square goes to the back of the output | at the write |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "one finger at each end" | `lo, hi = 0, len(nums) - 1` |
| "until the fingers meet" | `while lo < hi:` (`<=` only when the middle item needs its own visit) |
| "too small: the left item is hopeless" | `lo += 1` |
| "too big: the right item is hopeless" | `hi -= 1` |
| "keep this item" | `nums[write] = nums[read]` then `write += 1` |
| "skip copies of the value I just used" | `while lo < hi and nums[lo] == nums[lo - 1]: lo += 1` |

One template per main shape. In the pair template RECORD comes before the STEPs: a hit must be reported before a finger moves past it. In the read / write template, copying a keeper *is* the record.

```python
def pair_with_sum_sorted(nums, target):      # nums sorted ascending
    lo, hi = 0, len(nums) - 1                # STATE + INIT: the candidates still alive are nums[lo..hi]
    while lo < hi:                           # a pair needs two different items
        total = nums[lo] + nums[hi]
        if total == target:
            return [lo, hi]                  # RECORD
        if total < target:
            lo += 1                          # STEP: nums[lo] is too small even with the biggest partner left
        else:
            hi -= 1                          # STEP: nums[hi] is too big even with the smallest partner left
    return []                                # RETURN: no pair


def remove_value(nums, val):                 # keep every item except val, in place
    write = 0                                # STATE + INIT: nums[:write] = the keepers of nums[:read], in order
    for read in range(len(nums)):
        if nums[read] != val:                # a keeper
            nums[write] = nums[read]         # STEP + RECORD: copy it into the next free slot
            write += 1
    return write                             # RETURN: the new length


print(pair_with_sum_sorted([1, 2, 4, 6, 8, 9], 12))   # [2, 4]
arr = [3, 2, 2, 3, 4]
n_kept = remove_value(arr, 3)
print(n_kept, arr[:n_kept])                            # 3 [2, 2, 4]
```

**Try it**
- Change `while lo < hi` to `while lo <= hi` and run `pair_with_sum_sorted([2, 5, 9], 10)`: `[1, 1]`. The 5 was used twice.
- Run `pair_with_sum_sorted([4, 1, 3], 4)` on unsorted input: `[]`, although 1 + 3 = 4. The moves are only proofs when the data is sorted.
- Replace the body of `remove_value` with `nums = [x for x in nums if x != val]` and `return len(nums)`, then run it on `arr = [3, 2, 2, 3]`: it returns 2, but `arr` is untouched and `arr[:2]` is `[3, 2]`. The assignment only rebinds the local name.

### Watch it work

Each line is one comparison; `L` and `R` are drawn under the items they point at.

```python
def trace_pair(nums, target):
    lo, hi = 0, len(nums) - 1
    print("nums " + "".join(f"{x:>4}" for x in nums))
    while lo < hi:
        total = nums[lo] + nums[hi]
        marks = "".join(f"{'L' if i == lo else 'R' if i == hi else '':>4}" for i in range(len(nums)))
        if total == target:
            print(f"     {marks}   {nums[lo]} + {nums[hi]} = {total}: found [{lo}, {hi}]")
            return
        if total < target:
            print(f"     {marks}   {nums[lo]} + {nums[hi]} = {total} < {target}: drop {nums[lo]} (lo += 1)")
            lo += 1
        else:
            print(f"     {marks}   {nums[lo]} + {nums[hi]} = {total} > {target}: drop {nums[hi]} (hi -= 1)")
            hi -= 1
    print("     no pair")


trace_pair([1, 2, 4, 6, 8, 9], 12)
```

**Try it**
- Run `trace_pair([1, 2, 4, 6, 8, 9], 7)`: this time R does the walking (9 and 8 are dropped), then 1 + 6 hits.
- Run `trace_pair([1, 2, 4, 6, 8, 9], 30)`: every sum is too small, so L walks all the way to R and the trace ends with "no pair".
- Match each line to a row or a column of the pair table in the picture: every "drop" kills one of them.

### Where it goes wrong

1. **`<=` for pairs.** With `while lo <= hi` the fingers can meet on one item: `pair_with_sum_sorted([2, 5, 9], 10)` returns `[1, 1]`. Pairs need `lo < hi`; `<=` is right only when the middle item needs its own visit (the Dutch flag; Squares of a Sorted Array's `for write` loop runs n times, which is the same thing).
2. **Unsorted input.** Opposite ends works only because the order proves which side is hopeless: `[4, 1, 3]` with target 4 finds nothing. Sort first (carrying the original indices if they are the answer), or use a hash map.
3. **Moving the taller wall.** In Container With Most Water the *shorter* wall is the one that can never do better; moving the taller one gives 3 instead of 6 on `[1, 3, 2, 3]`.
4. **3Sum bookkeeping.** Skip an anchor equal to the *previous* one (`nums[i] == nums[i - 1]`); comparing with the *next* one throws away `[-1, -1, 2]`. After recording a triplet, move both fingers, or the loop records it forever.
5. **Dutch flag: advancing `mid` after a swap with `high`.** The value that came from the right has not been looked at yet: `[1, 2, 2, 0]` ends as `[1, 0, 2, 2]`.
6. **Looking back into the input instead of the output.** In Remove Duplicates II compare with `nums[write - 2]`, not `nums[read - 2]`: that slot may already be overwritten, so `[1, 1, 1, 2, 2]` keeps 3 items instead of 4.
7. **Unguarded skip loops.** `while not s[lo].isalnum(): lo += 1` runs off the end of `".,"` (`IndexError`). Guard every inner loop with `lo < hi`, or move one finger per iteration with `if / elif`.
8. **Rebinding instead of writing in place.** `nums = [x for x in nums if x != val]` builds a new list and points the local name at it; the caller's list does not change. Write through `nums[write]`, or use `nums[:] = ...` if extra space is allowed.

### Edge cases to say out loud

Empty input · one item · two items · all items equal (dedupe!) · no answer · negatives · the fingers meeting on one item · already sorted, or sorted backwards.

```python
assert pair_with_sum_sorted([], 5) == []
assert pair_with_sum_sorted([5], 10) == []                  # one item can't pair with itself
assert pair_with_sum_sorted([2, 5, 9], 10) == []            # 5 + 5 would reuse an item
assert pair_with_sum_sorted([3, 3], 6) == [0, 1]            # equal values, two items
assert pair_with_sum_sorted([-3, -1, 2, 7], 1) == [1, 2]    # negatives
all_sevens = [7, 7, 7]
assert remove_value(all_sevens, 7) == 0                     # everything removed
keep_all = [1, 2]
assert remove_value(keep_all, 9) == 2 and keep_all == [1, 2]   # nothing removed
assert remove_value([], 1) == 0
print("edge cases pass")
```

**Try it**
- LeetCode 167 wants 1-based indices: return `[lo + 1, hi + 1]` and check that `[2, 7, 11, 15]` with target 9 gives `[1, 2]`.
- Predict, then add: `assert pair_with_sum_sorted([1, 1, 1, 1], 2) == [0, 3]` (the outermost pair is found first).
- Add `assert pair_with_sum_sorted([1, 5, 10], 11) == [0, 2]`: an answer that uses both ends is found on the very first comparison.

### Variations

The opposite-ends problems are in the table "From the comparison to the move"; these change the shape itself.

| Variation | What changes from the template | Problems |
|---|---|---|
| **k-sum** | sort; fix one item (or k − 2 items); two-pointer the rest; skip equal neighbours | 15, 18 |
| **Count pairs** | when a pair fits, every partner between the fingers fits too: `count += hi - lo` | 2824, 259, 611 |
| **Two inputs, one finger each** | merge from the back (88); advance the pattern finger only on a match (392); advance the list whose interval ends first (986); walk from the end, skipping deleted chars (844) | 88, 392, 986, 844 |
| **Read / write compaction** | `write` trails `read`; copy (or swap) the keepers | 27, 283 |
| **Look-back dedupe** | keep `nums[read]` unless it equals `nums[write - k]` | 26, 80 |
| **Three pointers, four regions** | Dutch flag: `low`, `mid`, `high`; after a swap with `high`, `mid` stays | 75 |
| **Fixed gap** | the front finger starts k ahead and both move together ([Linked Lists](#s10)) | 19 |
| **Two strings with a bookmark** (Hard) | one finger per string; on a mismatch, jump back to the last `*` | 44 |

**k-sum.** 3Sum is Two Sum II run once per anchor: sort, fix `nums[i]`, and two-pointer the rest for `-nums[i]`. Sorting also puts equal values side by side, so duplicates are skipped by comparing with a neighbour instead of collecting a set. 4Sum wraps one more loop around it.

```python
def three_sum(nums):
    nums = sorted(nums)
    n, out = len(nums), []
    for i in range(n - 2):
        if nums[i] > 0:
            break                            # the smallest of the three is positive: no zero sum is left
        if i > 0 and nums[i] == nums[i - 1]:
            continue                         # same anchor as last time: same triplets
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1                      # STEP
            elif total > 0:
                hi -= 1                      # STEP
            else:
                out.append([nums[i], nums[lo], nums[hi]])   # RECORD
                lo, hi = lo + 1, hi - 1      # STEP: a new triplet needs BOTH values to change
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                  # skip copies of the value just used
    return out


print(three_sum([-1, 0, 1, 2, -1, -4]))   # [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0, 0]))            # [[0, 0, 0]]
```

**Try it**
- Replace the anchor check with `if nums[i] == nums[i + 1]: continue` and run `three_sum([-1, -1, 2])`: `[]`. The first −1 was skipped while it was still needed.
- Delete the inner `while ... nums[lo] == nums[lo - 1]` loop and run `three_sum([-2, 0, 0, 2, 2])`: `[[-2, 0, 2], [-2, 0, 2]]`, a duplicate.
- There is no skip loop for `hi`. Print `i, lo, hi, total` inside the `while` for `[-2, 0, 1, 1, 2, 2]`: after the first hit, `hi` sits on a copy of 2, the total is 1, and `total > 0` moves it on by itself.

**Count pairs.** "How many pairs sum below the target?" When `nums[lo] + nums[hi]` fits, `nums[lo]` fits with *every* partner between the fingers too (they are all smaller than `nums[hi]`), so a single comparison counts a whole row of the pair table.

```python
def count_pairs_below(nums, target):         # pairs i < j with nums[i] + nums[j] < target (2824, 259)
    nums = sorted(nums)
    lo, hi, count = 0, len(nums) - 1, 0
    while lo < hi:
        if nums[lo] + nums[hi] < target:
            count += hi - lo                 # RECORD: nums[lo] fits with EVERY partner in lo+1..hi
            lo += 1                          # STEP: that whole row is counted
        else:
            hi -= 1                          # STEP: nums[hi] is too big even with the smallest partner
    return count


print(count_pairs_below([-1, 1, 2, 3, 1], 2))   # 3
```

**Try it**
- Replace `count += hi - lo` with `count += 1`: `count_pairs_below([-1, 1, 2, 3, 1], 2)` gives 1 instead of 3. One comparison proved a whole row, so it must count a whole row.
- Print `lo, hi` whenever the pair fits: for that input the only hit is `lo = 0, hi = 3` on the sorted list `[-1, 1, 1, 2, 3]`, and it adds 3 pairs at once (−1 with 1, 1 and 2).
- Valid Triangle Number (611) is the same move from the other side. Sort, fix the longest side `sides[k]` from the right, and run the fingers on `sides[:k]`: when `sides[lo] + sides[hi] > sides[k]`, do `count += hi - lo` and `hi -= 1`, else `lo += 1`. `[2, 2, 3, 4]` gives 3.

**Reasoning about the smaller side (container).** The area is `min(left, right) × width`. The shorter wall caps the height, and any narrower container that keeps it is no better, so the shorter wall has already met its best partner: drop it and move that finger inward.

**Reasoning about the smaller side (rain water).** The water above a bar is `min(tallest on its left, tallest on its right) − bar`. A finger only ever leaves the *lower* of the two current bars, so the taller current bar is at least as tall as every bar passed so far. So when `height[lo] < height[hi]`, `left_max <= height[hi] <=` the tallest bar right of `lo`, and the level at `lo` is exactly `left_max`, whatever the unseen bars between the fingers are.

```text
height = [3, 0, 2, 0, 4]

            #          water above each bar = min(max on its left, max on its right) - bar
#  ~  ~  ~  #
#  ~  #  ~  #          = 3 + 1 + 3 = 7
#  ~  #  ~  #
3  0  2  0  4
```

```python
def max_area(height):
    lo, hi, best = 0, len(height) - 1, 0
    while lo < hi:
        best = max(best, min(height[lo], height[hi]) * (hi - lo))   # RECORD every pair we look at
        if height[lo] < height[hi]:
            lo += 1                          # STEP: the shorter wall can't do better with a closer partner
        else:
            hi -= 1
    return best


def trap(height):
    lo, hi = 0, len(height) - 1
    left_max = right_max = water = 0         # STATE: the tallest bar passed so far from each side
    while lo < hi:
        if height[lo] < height[hi]:
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]   # RECORD: left_max <= height[hi], so left_max sets the level at lo
            lo += 1                          # STEP
        else:
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]  # RECORD: right_max <= height[lo], so right_max sets the level at hi
            hi -= 1                          # STEP
    return water


print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))         # 49
print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))    # 6
```

**Try it**
- In `max_area`, flip `<` to `>` so the taller wall moves, and run `max_area([1, 3, 2, 3])`: 3 instead of 6.
- In the left branch of `trap`, swap the two lines (add water before updating `left_max`) and run `trap([2, 0, 3])`: 0 instead of 2. The first bar added 0 − 2 = −2 units of "water".
- Print `lo, hi, left_max, right_max, water` at the top of the `trap` loop for `[4, 2, 0, 3, 2, 5]`: `hi` never moves (5 is the tallest bar, so the left side is always the lower one), and the water grows 0, 0, 2, 6, 7 before the last step brings it to 9.

**Opposite ends without a target.** Squaring a sorted array folds it: the biggest squares sit at the two *ends* and the smallest somewhere in the middle. So compare the ends and fill the output from the back. A palindrome check is the same walk on mirror positions, where skipping punctuation means moving one finger without comparing (`practice/simple/basics/strings/02_two_pointer_palindromes_and_reverse_words.py` has the code). Valid Palindrome II (680) may delete one character: at the first mismatch, test whether `s[lo + 1..hi]` or `s[lo..hi - 1]` is a palindrome.

```python
def sorted_squares(nums):                    # nums sorted; returns the squares, sorted
    out = [0] * len(nums)
    lo, hi = 0, len(nums) - 1
    for write in range(len(nums) - 1, -1, -1):   # fill from the back: the biggest square first
        if abs(nums[lo]) > abs(nums[hi]):
            out[write] = nums[lo] ** 2       # RECORD
            lo += 1                          # STEP
        else:
            out[write] = nums[hi] ** 2
            hi -= 1
    return out


print(sorted_squares([-4, -1, 0, 3, 10]))   # [0, 1, 9, 16, 100]
print(sorted_squares([-7, -3, 2, 3, 11]))   # [4, 9, 9, 49, 121]
```

**Try it**
- Fill `out` from the front (`for write in range(len(nums))`) and run `[-4, -1, 0, 3, 10]`: `[100, 16, 9, 1, 0]`. The ends hold the biggest squares, so they belong at the back.
- Run `sorted_squares([-3, -2, -1])`: `[1, 4, 9]`. `lo` takes the first two squares; for the last item `lo == hi`, the `>` is False and the `else` branch takes it, so `hi` moves once.
- Change `>` to `>=` and rerun `[-7, -3, 2, 3, 11]`: the same output. On a tie both ends hold the same square, so either one may go to the back.

**Two inputs, one finger each.** Merge Sorted Array (88) gets `a` with m sorted items followed by n spare slots, and must merge `b` into it in place. Filling from the front would overwrite items of `a` before they are read; the spare slots are at the back, so fill from the back, taking the bigger of the two tails each time. The other two-input problems keep the same shape: Is Subsequence (392) advances the pattern finger only on a match, Interval List Intersections (986) advances the list whose interval ends first, and Backspace String Compare (844) walks both strings from the end, skipping characters that a later `#` deletes.

```python
def merge_into(a, m, b, n):                  # 88: a holds m sorted items + n spare slots; b holds n
    i, j = m - 1, n - 1                      # STATE: the last unmerged item of each input
    for write in range(m + n - 1, -1, -1):   # fill from the back: those slots are free
        if j < 0 or (i >= 0 and a[i] > b[j]):
            a[write] = a[i]                  # STEP + RECORD: the bigger tail goes last
            i -= 1
        else:
            a[write] = b[j]
            j -= 1
    return a


print(merge_into([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3))   # [1, 2, 2, 3, 5, 6]
```

**Try it**
- Drop `i >= 0 and` and run `merge_into([2, 0], 1, [1], 1)`: `[2, 2]`. Once `a` is used up, `a[-1]` quietly reads the last slot.
- Drop `j < 0 or` and run `merge_into([1], 1, [], 0)`: `IndexError`, because `b` is empty and `b[j]` with j = −1 fails.
- Merge from the front instead (`i = j = 0`, take the smaller head, `write` counting up): `[1, 2, 2, 2, 5, 6]`. `b`'s 2 overwrote the 3 before it was read.

**Read / write pointers.** `read` visits every item once; `write` marks where the next keeper goes. Move Zeroes swaps instead of copying, so the zeros travel to the back in the same pass. Remove Duplicates II keeps an item unless it would be a third copy, and because the array is sorted, a third copy is exactly an item equal to the one *two slots back in the output*.

```python
def move_zeroes(nums):
    write = 0                                # STATE: nums[:write] = the non-zeros so far, in order
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]   # STEP: the zero at write moves back to read
            write += 1


def remove_extra_copies(nums, k=2):          # sorted nums: keep at most k copies of each value
    write = 0
    for read in range(len(nums)):
        if write < k or nums[read] != nums[write - k]:   # look back k slots into the OUTPUT
            nums[write] = nums[read]         # STEP + RECORD
            write += 1
    return write


zeros = [0, 1, 0, 3, 12]
move_zeroes(zeros)
print(zeros)                                 # [1, 3, 12, 0, 0]
dupes = [1, 1, 1, 2, 2, 3]
kept = remove_extra_copies(dupes)
print(kept, dupes[:kept])                    # 5 [1, 1, 2, 2, 3]
```

**Try it**
- Look back into the input instead: change the condition to `read < k or nums[read] != nums[read - k]` and run `remove_extra_copies([1, 1, 1, 2, 2])`: 3 items instead of 4. The slot it looks back at was already overwritten.
- Print `nums` after each swap in `move_zeroes([0, 1, 0, 3, 12])`: `[1, 0, 0, 3, 12]`, `[1, 3, 0, 0, 12]`, `[1, 3, 12, 0, 0]`. The block of zeros slides to the right.
- Copy instead of swapping (`nums[write] = nums[read]`) in `move_zeroes`: you get `[1, 3, 12, 3, 12]`, and a second loop would have to write the zeros.

**Three pointers, four regions (Dutch flag).** One pass sorts 0s, 1s and 2s by keeping four regions: `[0s | 1s | unknown | 2s]`. `mid` looks at the first unknown item: a 0 is swapped down to `low`, a 1 stays, a 2 is swapped up to `high`. What comes back from `low` is a 1 that was already looked at, but what comes back from `high` is unknown, so after that swap `mid` stays put. [Sorting & Selection](#s23) runs the same loop around any pivot value.

```text
[ 0 0 | 1 1 | ? ? ? | 2 2 ]
        ^     ^   ^             nums[:low] are 0s, nums[low:mid] are 1s,
       low   mid high           nums[mid..high] are unknown, nums[high+1:] are 2s
```

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1     # STATE: the four regions above
    while mid <= high:                       # the unknown region nums[mid..high] is not empty
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low, mid = low + 1, mid + 1      # STEP: what came from low is a 1 (or low == mid): done with it
        elif nums[mid] == 1:
            mid += 1                         # STEP: a 1 is already in its region
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                        # STEP: what came from high is unknown, so mid stays to look at it


colors = [2, 0, 2, 1, 1, 0]
sort_colors(colors)
print(colors)                                # [0, 0, 1, 1, 2, 2]
```

**Try it**
- Print `nums[:low], nums[low:mid], nums[mid:high + 1], nums[high + 1:]` at the top of the loop for `[2, 0, 2, 1, 1, 0]`: the four regions, with the unknown one shrinking by exactly one item per round (6 rounds).
- Add `mid += 1` after `high -= 1` and sort `[1, 2, 2, 0]`: `[1, 0, 2, 2]`. The 0 that came from the right was never looked at.
- With the same print, run `[2, 2, 2]` and `[0, 0, 0]`: only `high` moves in the first; `low` and `mid` move together in the second.

#### Stretch (Hard)

**Two strings with a bookmark.** Wildcard Matching keeps one finger on the text and one on the pattern. A plain character or `?` moves both. A `*` is a safety net: bookmark it and let it match nothing for now. On a mismatch, go back to the latest bookmark and let that star swallow one more character. Only the latest star matters: anything an earlier star could swallow, the later one can swallow instead. The cost is O(|s|·|p|) in the worst case, because every mismatch can send the pattern finger back to the bookmark.

```python
def wildcard_match(s, p):                    # '?' = any one char, '*' = any run of chars (even none)
    i = j = 0
    star, mark = -1, 0                       # STATE: the last '*' in p, and where in s its match ends
    while i < len(s):
        if j < len(p) and p[j] in (s[i], "?"):
            i, j = i + 1, j + 1              # STEP: plain match, both fingers move
        elif j < len(p) and p[j] == "*":
            star, mark = j, i                # STEP: bookmark; the star matches nothing for now
            j += 1
        elif star != -1:
            mark += 1                        # FIX: on a mismatch the last star swallows one more char
            i, j = mark, star + 1
        else:
            return False                     # RETURN: a mismatch and no star to fall back on
    while j < len(p) and p[j] == "*":
        j += 1                               # leftover stars match the empty string
    return j == len(p)                       # RETURN


print(wildcard_match("adceb", "*a*b"), wildcard_match("acdcb", "a*c?b"))   # True False
```

**Try it**
- Delete the final `while` that skips leftover stars and run `wildcard_match("ab", "ab*")`: `False` instead of `True`.
- Print `i, j, star, mark` in the mismatch branch for `("adceb", "*a*b")`: three mismatches, with `mark` at 2, 3 and 4 as the second star swallows `"d"`, `"dc"` and `"dce"`; then `b` matches.
- Count the rounds of the main loop for `s = "a" * 100` and `p = "*" + "a" * 50 + "b"`: 2,601. Double both lengths: 10,201. Four times the work, the O(|s|·|p|) worst case.

### Say it in the interview

> "Brute force checks every pair: O(n²). The array is sorted, so the sum of the two ends tells me which end is hopeless: if it's too small, the left number can't reach the target even with the largest partner left; if it's too big, the right one can't even with the smallest. Each comparison deletes a whole row or column of the pair table, so it's at most n − 1 steps: O(n) time and O(1) space, plus O(n log n) if I have to sort first. For 3Sum I sort, fix the first number and run this on the rest: O(n²)."

Then point at each pointer move and say what it rules out ("everything in this row is too small"). For in-place problems, say the invariant out loud: "`nums[:write]` is the finished answer, and `write` never passes `read`." Follow-ups to have ready:

- *Count the pairs instead of finding one?* `count += hi - lo` when the pair fits, then `lo += 1`.
- *Closest sum instead of exact?* Record the best distance on every step; the moves stay the same.
- *Unsorted, and the original indices are the answer?* A hash map ([Arrays & Hashing](#s03)), or sort `(value, index)` pairs.
- *k-sum in general?* Fix k − 2 items in nested loops, two pointers inside: O(n^(k−1)).

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| 3Sum | `two_pointers/three_sum.py` · `practice/simple/06_three_sum.py` | sort; fix nums[i]; two-pointer the rest; skip equal neighbours for the anchor and after each hit |
| Container With Most Water | `two_pointers/container_with_most_water.py` · `practice/simple/07_container_with_most_water.py` | start widest; the shorter wall can't do better with a closer partner, so move it inward |
| Move Zeroes | `two_pointers/move_zeroes.py` | write = next slot for a non-zero; swapping keepers forward pushes the zeros to the back |
| Remove Duplicates from Sorted Array II | `two_pointers/remove_duplicates_from_sorted_array_ii.py` | keep nums[read] unless it equals nums[write − 2]: look back into the output |
| Sort Colors | `two_pointers/sort_colors.py` | Dutch flag: low / mid / high regions; after swapping with high, mid stays |
| Squares of a Sorted Array | `two_pointers/squares_of_a_sorted_array.py` | the biggest square is at one of the two ends; fill the output from the back |
| Trapping Rain Water | `two_pointers/trapping_rain_water.py` · `practice/simple/08_trapping_rain_water.py` | move the finger at the lower bar: its running max is at most the other bar, so it sets the level |
| Two Sum II - Input Array Is Sorted | `two_pointers/two_sum_ii_input_array_is_sorted.py` | ends of a sorted array: too small → lo += 1, too big → hi −= 1; answer is 1-based |
| Valid Palindrome | `two_pointers/valid_palindrome.py` | compare mirror characters moving inward; skip non-alphanumerics without running off the end |
| Wildcard Matching | `two_pointers/wildcard_matching.py` | greedy match with a bookmark at the last `*`; on a mismatch that star swallows one more char |

### Self-check

1. In Two Sum II, when `nums[lo] + nums[hi]` is too small you move `lo`. Why can that never skip the answer?
<details><summary>Answer</summary><code>nums[hi]</code> is the biggest value still in play, and even it is not enough for <code>nums[lo]</code>. Every other partner left is smaller, so no pair that uses <code>nums[lo]</code> can reach the target. Dropping it removes only hopeless pairs: one dead row of the pair table.</details>

2. In Trapping Rain Water, why is the water above `lo` settled when `height[lo] < height[hi]`, although the bars between the fingers have not been seen yet?
<details><summary>Answer</summary>The level at <code>lo</code> is min(tallest bar on its left, tallest bar on its right). A finger only ever moves off the <em>lower</em> of the two current bars, so every bar passed so far is no taller than the taller current bar. When <code>height[lo] < height[hi]</code>, that gives <code>left_max <= height[hi] <=</code> the tallest bar on the right, so the minimum is <code>left_max</code>. Unseen bars between the fingers could only make the right side taller, which does not change the minimum.</details>

3. In counting pairs below a target, why does one successful comparison add `hi - lo` pairs?
<details><summary>Answer</summary>The array is sorted, so every partner between <code>lo + 1</code> and <code>hi</code> is at most <code>nums[hi]</code>. If <code>nums[lo] + nums[hi]</code> is below the target, so is <code>nums[lo]</code> plus any of them: that is <code>hi - lo</code> pairs, the whole row, counted at once before <code>lo</code> moves on.</details>
