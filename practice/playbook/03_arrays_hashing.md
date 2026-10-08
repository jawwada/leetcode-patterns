## Arrays & Hashing

> A hash map is a notebook with instant recall. Walk the array once. At each item, first ask the notebook the one question the brute force would answer with a rescan: "is my partner in here?", "how many of these so far?", "which group is this?" Then write the item down. Each question costs O(1) on average, so the whole walk is O(n).

**Reach for it when** the brute force has an inner loop that only *searches* for a value: a partner, an earlier copy, a matching group. The problem says pairs, duplicates, frequency, anagrams or "group by", or it wants O(n) on unsorted data. The surest sign is that the brute force compares items only by value, whether they are equal, sum to a target or hold the same letters, and never by where they sit.

### The picture

Two Sum asks for the indices of the two numbers that add up to a target: `[3, 5, 2, 7, 11]` with target 9 gives `[2, 3]`, because 2 + 7 = 9. The walk below shows the notebook at every step.

```text
nums = 3  5  2  7  11      target = 9           ask the notebook first, then write yourself in

i=0   [3] 5  2  7  11      need 6   notebook {}                no  -> write 3:0
i=1    3 [5] 2  7  11      need 4   notebook {3:0}             no  -> write 5:1
i=2    3  5 [2] 7  11      need 7   notebook {3:0, 5:1}        no  -> write 2:2
i=3    3  5  2 [7] 11      need 2   notebook {3:0, 5:1, 2:2}   YES -> answer [2, 3]
       '-----'
       everything left of the cursor is already in the notebook; 11 is never read
```

**Why it is fast.** Once the brute force fixes `v`, it rescans the other numbers to find `target - v`, a value it *already knows*. A search by value is exactly what a hash map does in O(1) on average: it turns the value into a slot number, called its hash, and jumps straight there. n items × O(1) = O(n) time, paid for with O(n) memory.

**Why it is correct.** A pair (i, j) with i < j is caught exactly when j arrives, because by then the value at i is already in the notebook.

The notebook does not always hold positions. To group items, its key is a **fingerprint**: anything that is equal for items that belong together and different otherwise. Group Anagrams asks to put the words made of the same letters together, `["eat", "tea", "tan"] → [["eat", "tea"], ["tan"]]`, and its fingerprint is the letter counts:

```text
word   fingerprint            bucket
eat    a:1 e:1 t:1     --->   [eat, tea]
tea    a:1 e:1 t:1     --->   (same bucket)
tan    a:1 n:1 t:1     --->   [tan]
```

### From idea to code

**The idea in one sentence:** *walk once; for the current item, first ask the map the question the brute force would rescan for, then store what a later item will need to ask about.*

The seven decisions follow from that sentence. The **State** is one dict or set, keyed by what you will look up later: value → index for pairs, value → count for frequencies, fingerprint → list for groups. Its **Definition** is a comment where it is created, `seen[v] = index of an earlier v`, and it decides every other line. The **Invariant** depends on when you write: with *ask, then store* the map holds exactly `nums[0..i-1]` at the top of step `i`, and with *build first* it holds the whole input.

A **Step** stores the item: `seen[v] = i`, `count[v] += 1`, `groups[key].append(w)`. The **Record** happens the moment a lookup succeeds: return the pair, add to a count, report a repeat. **Init** is an empty map, seeded only when the empty prefix counts, like the `{0: 1}` of [Prefix Sums](#s04). The **Return** is the pair, the count or `list(groups.values())`, and `[]`, `-1` or `False` when nothing matched.

**From the question to the code.** Two decisions settle every hashing solution: the key, which is what a later lookup asks about, and when you write. When an item pairs with an **earlier** item, ask, then store. Two Sum maps each value to its index. Pairs of Songs With Total Durations Divisible by 60 (1010), the pairs of songs whose lengths add up to a multiple of 60, maps each remainder `t % 60` to a count and adds `seen[(60 - r) % 60]` at every song.

Questions about distance and place keep the same order. Contains Duplicate II (219) asks whether an equal value sits within k positions: it maps each value to its **last** index and hits when `i - last[v] <= k`. Valid Sudoku (36) asks whether a digit repeats in a row, a column or a 3×3 box: it keeps one set of `(unit, digit)` pairs and answers `False` at the first repeat.

When the question is about the whole collection, build first, because an item's answer depends on items still to come. Top K Frequent Elements (347) wants the k values that appear most often: it counts every value, then buckets the values by count and reads from the top. Longest Consecutive Sequence (128) wants the longest run of consecutive values: it builds a set and walks up from run starts.

4Sum II (454) mixes the two. It counts the ways to pick one number from each of four lists so that `a + b + c + d == 0`: it builds one half first, a count per sum `a + b`, then asks with the other half for `-(c + d)`. Group Anagrams (49) never asks at all: it only stores, fingerprint → members, because the groups themselves are the answer.

The two templates are Two Sum, which asks and then stores, and Group Anagrams, which only stores. Two Sum wants the indices of the two numbers that add up to target, `[3, 5, 2, 7, 11], 9 → [2, 3]`, and its words become lines: "the partner I need" is `need = target - v`, "have I seen it?" is `if need in seen:`, and "now remember me" is `seen[v] = i`. The RECORD line comes *before* the STEP, because the lookup may only see earlier items.

Group Anagrams wants the words made of the same letters grouped together: `["eat", "tea", "tan", "ate", "nat", "bat"] → [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`. "How many of each letter" is a list of 26 counts, and "a key made of that list" is `tuple(counts)`, because a list cannot be a key and a tuple can. Storing the word *is* the answer, so STEP and RECORD are one line, `groups[key].append(w)`.

```python
def two_sum(nums, target):
    seen = {}                                # STATE + INIT: seen[v] = index of an earlier v (left of i)
    for i, v in enumerate(nums):
        need = target - v                    # the one partner that completes the sum
        if need in seen:                     # RECORD: ask the past first ...
            return [seen[need], i]
        seen[v] = i                          # STEP: ... then join it
    return []                                # RETURN: no pair


def group_anagrams(words):
    groups = defaultdict(list)               # STATE + INIT: fingerprint -> words with that fingerprint
    for w in words:
        counts = [0] * 26                    # the fingerprint: how many a's, b's, ..., z's (lowercase a-z only)
        for ch in w:
            counts[ord(ch) - ord("a")] += 1
        groups[tuple(counts)].append(w)      # STEP + RECORD: same letters, same key (a tuple can be a key)
    return list(groups.values())             # RETURN


print(two_sum([3, 5, 2, 7, 11], 9))          # [2, 3]
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

**Try it**
- Use `frozenset(w)` as the key and run `group_anagrams(["aab", "abb"])`: `[['aab', 'abb']]`. A set forgets how many copies of each letter there are, so it is not a fingerprint.
- Replace `tuple(counts)` with `counts` and run `group_anagrams(["ab"])`: `TypeError: unhashable type: 'list'`. Dict keys must be hashable, and a list is not (it can change).
- Run `group_anagrams(["Zt", "tt"])`: `[['Zt', 'tt']]`. `ord("Z") - ord("a")` is −7, and `counts[-7]` is the slot of `t`. The fingerprint silently assumes lowercase a-z.

### Watch it work

The trace runs Two Sum on `[4, 1, 4, 6]` with target 7, where the answer is `[1, 3]`, because 1 + 6 = 7. Each line is one step, and `seen` is printed *before* the current item is stored, so every row shows exactly the items to the left of `i`. Watch the second 4: a dict keeps one entry per key, so the 4 overwrites its old index instead of adding a second entry.

```python
def trace_two_sum(nums, target):
    seen = {}
    for i, v in enumerate(nums):
        need = target - v
        found = need in seen
        action = f"found at index {seen[need]}" if found else f"store {v}: {i}"
        print(f"i={i}  v={v:<3} need={need:<3} seen={str(seen):<24} {action}")
        if found:
            return [seen[need], i]
        seen[v] = i
    return []


print(trace_two_sum([4, 1, 4, 6], 7))   # [1, 3]
```

**Try it**
- Change `seen[v] = i` to `seen.setdefault(v, i)`, which keeps the first copy's index, and rerun: the last row shows `seen={4: 0, 1: 1}` and the answer is still `[1, 3]`. Two Sum does not care which copy it keeps; Contains Duplicate II, which needs the nearest copy, does (trap 4).
- Run `trace_two_sum([1, 2, 3], 100)`: every row stores, and the result is `[]`. With no pair, the notebook ends up holding all n values: that is the O(n) space.
- Predict the rows for `trace_two_sum([2, 7, 11, 15], 9)` before running it (one store, then "found at index 0").

### Where it goes wrong

1. **Storing before asking.** The item finds itself ([From Idea to Code](#s01) shows the swap).
2. **A list as a key.** `groups[counts]` raises `TypeError: unhashable type: 'list'`. Use `tuple(counts)` or `"".join(sorted(w))`.
3. **A fingerprint that forgets something.** `frozenset(w)` drops the counts, so `"aab"` and `"abb"` collide. `ord(ch) - ord("a")` assumes lowercase: it sends `"Z"` into the slot of `t` and `"A"` out of range. The key must be equal *exactly* when the items belong together.
4. **First or last index?** Contains Duplicate II, an equal value within k positions, needs the *last* index (overwrite): keeping the first answers `False` for `[1, 0, 1, 1]`, k = 1. "Longest" questions need the *first* (store only when absent).
5. **Walking every member of a run.** In Longest Consecutive Sequence, counting up from every value costs 499,500 steps on `range(1000)`. Start only where `x - 1` is missing, and loop over the set (copies in the list would re-walk the run).
6. **Swapping with a computed index**, as in First Missing Positive, the smallest positive integer missing from an array. `nums[i], nums[nums[i] - 1] = nums[nums[i] - 1], nums[i]` builds the right side first and then assigns the targets left to right, so `nums[nums[i] - 1]` is computed with the *new* `nums[i]`: on `[2, 1]` it never ends. Compute `home = nums[i] - 1` first ([Python Toolkit](#s02)).
7. **`int(x / w)` for buckets**, as in Contains Duplicate III, two indices at most k apart whose values are at most t apart. It rounds toward zero, so −3 and 3 share bucket 0 when `w = 5`. Floor division `x // w` keeps negatives in their own buckets.
8. **Voting without a guarantee.** Majority Element asks for the value that fills more than half the array. `[1, 2, 3]` has no majority, yet the Boyer-Moore vote returns 3. Unless a majority is promised, count the candidate in a second pass.

### Edge cases to say out loud

Empty input · one item · no pair or no group mate · equal values (`[3, 3]`) · an item that would be its own partner · negatives and zero · the empty string as a word · same letters, different counts. The asserts below run each case through the two templates.

```python
assert two_sum([], 5) == []
assert two_sum([1, 2], 7) == []                     # no pair
assert two_sum([3, 3], 6) == [0, 1]                 # equal values, two different indices
assert two_sum([4, 1, 5, 3], 8) == [2, 3]           # the 4 needs a second 4, and there is none
assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]  # negatives are just values
assert group_anagrams([]) == []
assert group_anagrams([""]) == [[""]]               # the empty word has a key too (26 zeros)
assert group_anagrams(["ab", "ba", "abc"]) == [["ab", "ba"], ["abc"]]
assert group_anagrams(["aab", "abb"]) == [["aab"], ["abb"]]   # same letters, different counts
print("edge cases pass")
```

**Try it**
- Add `assert two_sum([0, 4, 3, 0], 0) == [0, 3]`: here `need == v`, and the first 0 is stored before the second one asks.
- Predict, then add: `assert two_sum([5], 10) == []` (one item cannot be its own partner).
- Add `assert group_anagrams(["a", "a"]) == [["a", "a"]]`: equal words share a key, so they land in one group.

### Variations

Every variation still turns a search into a lookup; what changes is the key, what is stored, or where it is stored. The table is the overview, and the cells after it follow its order.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Another question, another key** | read the key, the value and when to write off "From the question to the code" above | Contains Duplicate II (219), Valid Sudoku (36) |
| **Neighbours by value** | build a set; count up only from run starts (`x - 1` missing) | Longest Consecutive Sequence (128) |
| **Count, then bucket by count** | `Counter`, then `buckets[f]` for f in 1..n, read from high to low | Top K Frequent Elements (347) |
| **Vote instead of count** | Boyer-Moore: a candidate and its votes; for "more than n/3", two candidates, then verify | Majority Element (169); Majority Element II (229): every value that appears more than n/3 times |
| **Encoding** | frame each string as `len#payload`; the decoder jumps, never scans | Encode and Decode Strings (271): pack a list of strings into one string and back |
| **Count pairs, meet in the middle** | `pairs += seen[partner]` before `seen[key] += 1`; or count one half's sums, ask with the other's | Pairs of Songs With Total Durations Divisible by 60 (1010), 4Sum II (454) |
| *Second pass:* **The array is the hash table** | value v belongs at index v − 1: swap values home, or mark v by negating `nums[abs(v) - 1]` | First Missing Positive (41); Find All Duplicates in an Array (442): every value of 1..n that appears twice; Find All Numbers Disappeared in an Array (448): every value of 1..n that never appears |
| *Second pass:* **Value buckets, pigeonhole** | bucket = `x // width`; close values share a bucket or sit next door | Contains Duplicate III (220); Maximum Gap (164): the largest gap between neighbours in sorted order |
| *Second pass:* **Counting with order** | "how many earlier / later items are smaller": a Fenwick tree over values, or count while merging ([Sorting & Selection](#s23)) | Count of Smaller Numbers After Self (315): how many later items are smaller than each; Reverse Pairs (493): the pairs i < j with `nums[i] > 2 · nums[j]`; Create Sorted Array through Instructions (1649): the cost of inserting each number into a sorted list |

**Neighbours by value.** The first variation changes only the key: a plain set of values, built before the walk. Longest Consecutive Sequence asks for the longest run of consecutive values hiding in an unsorted array, in O(n): `[100, 4, 200, 1, 3, 2] → 4`, the run 1, 2, 3, 4. "Consecutive" is about values, not positions, so sorting looks necessary. A set answers "is x + 1 here?" in O(1) instead.

The trick that keeps it O(n) is to count a run only from its smallest member, the `x` whose `x - 1` is missing. Every value then belongs to exactly one walk, so all the walks together take at most n steps.

```text
values:       1 2 3 4 . . . . 100 . . . 200
run starts:   ^                 ^          ^        (x - 1 is missing)
walks:        1->2->3->4        100        200      each value is walked exactly once
```

So the code puts every value in a set, and for each value whose `x - 1` is missing it walks up `x + 1, x + 2, ...` while the set still has them, keeping the longest walk.

```python
def longest_consecutive(nums):
    values = set(nums)                       # STATE: O(1) "is x here?" (built first; drops copies)
    best = 0
    for x in values:
        if x - 1 in values:                  # x sits inside a run: its run start will count it
            continue
        length = 1
        while x + length in values:          # walk up from the run start
            length += 1
        best = max(best, length)             # RECORD
    return best


print(longest_consecutive([100, 4, 200, 1, 3, 2]))            # 4  (1, 2, 3, 4)
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))    # 9  (0 .. 8)
```

**Try it**
- Add `steps = 0` at the top, `steps += 1` inside the `while`, and print it at the end; run `longest_consecutive(list(range(1000)))`: 999 steps. Now delete the two lines of the `if x - 1 in values` check: 499,500 steps. That `if` is the O(n).
- Loop over `nums` instead of `values` with `[1, 1, 1, 2, 3]`: the answer is still 3, but the run 1-2-3 is walked three times. Many copies of a run start make it quadratic again.
- Predict `longest_consecutive([5, 5, 5])`, `longest_consecutive([])` and `longest_consecutive([-2, -1, 0, 1])` (1, 0 and 4).

**Count, then bucket by count; or vote.** Next, the map stores counts, `count = Counter(nums)` or `count[v] += 1`, and the twist is how to read its top without sorting. Top K Frequent Elements asks for the k values that appear most often: `[1, 1, 1, 2, 2, 3], k = 2 → [1, 2]`. Frequencies are whole numbers from 1 to n, so they can be list indices: `buckets[f]` holds the values seen exactly f times, and reading the buckets from the top gives the most frequent first.

Majority Element asks for the value that fills *more than half* the array, and promises that one exists: `[2, 2, 1, 1, 1, 2, 2] → 2`. It needs no counts at all. Picture the items cancelling in pairs of *different* values: each cancellation removes at most one copy of the majority, and the majority outnumbers all the others together, so it survives. Majority Element II (229) wants every value above n/3; at most two can exist, so keep two candidates and verify both in a second pass.

In code, `top_k_frequent` counts, drops each value on the shelf numbered by its count, and reads the shelves from the top. `majority` keeps one candidate and a vote count: a match adds a vote, a different value cancels one, and at zero votes the next item becomes the candidate.

```python
def top_k_frequent(nums, k):
    count = Counter(nums)                    # STATE: value -> frequency (built first)
    buckets = [[] for _ in range(len(nums) + 1)]   # buckets[f] = values seen exactly f times
    for value, f in count.items():
        buckets[f].append(value)
    out = []
    for f in range(len(nums), 0, -1):        # highest frequency first
        for value in buckets[f]:
            out.append(value)                # RECORD
            if len(out) == k:
                return out
    return out


def majority(nums):                          # assumes some value occurs more than n / 2 times
    candidate, votes = None, 0               # STATE: votes = copies of candidate not yet cancelled
    for v in nums:
        if votes == 0:
            candidate = v                    # everything so far cancelled out: start over with v
        votes += 1 if v == candidate else -1 # STEP: a match adds a vote, anything else cancels one
    return candidate                         # RETURN


print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))   # [1, 2]
print(majority([2, 2, 1, 1, 1, 2, 2]))         # 2
```

**Try it**
- Size `buckets` with `range(len(nums))` instead of `range(len(nums) + 1)` and run `top_k_frequent([7, 7], 1)`: `IndexError`, because a value can appear n times.
- Run `majority([1, 2, 3])`: it returns 3, yet nothing is a majority. Without the guarantee, count the candidate in a second pass.
- Print `v, candidate, votes` after each step for `[2, 2, 1, 1, 1, 2, 2]`: the votes drop to 0 after the 4th and the 6th item; 1 takes over at the 5th, and 2 takes it back at the 7th.

**Encoding.** Encoding is the odd one out: no map, but the same habit of writing something down so that a later reader never has to search. Encode and Decode Strings asks to pack a list of strings into one string and unpack it again, any characters allowed: `["lint", "code"] → "4#lint4#code" → ["lint", "code"]`. Joining with a delimiter breaks as soon as a string contains the delimiter.

Writing each string's length first tells the decoder how far to jump, so it never looks inside a payload; the `#` only marks where the length's digits end. So `encode` writes `length#text` for each string, back to back, and `decode` reads the digits up to `#`, copies exactly that many characters, and jumps past them to the next frame.

```python
def encode(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)      # frame = length, '#', payload


def decode(data):
    out, i = [], 0                           # STATE: i = start of the next frame
    while i < len(data):
        j = data.index("#", i)               # the length's digits end at the first '#' from i
        size = int(data[i:j])
        out.append(data[j + 1:j + 1 + size]) # RECORD: exactly `size` chars, whatever they are
        i = j + 1 + size                     # STEP: jump to the next frame
    return out                               # RETURN


packed = encode(["4#a", "", "hi"])
print(packed)                                # 3#4#a0#2#hi
print(decode(packed))                        # ['4#a', '', 'hi']
```

**Try it**
- Try the delimiter idea: `",".join(["a,b", "c"]).split(",")` gives `['a', 'b', 'c']`, three strings instead of two.
- Print `i` at the top of the decode loop for `encode(["lint", "code"])`: 0, then 6. The pointer lands only on frame starts, never inside a payload.
- Check that `decode(encode([]))` is `[]` while `decode(encode([""]))` is `['']`: the empty list and the list holding one empty string stay different.

**Count pairs, or meet in the middle.** Back to the Two Sum loop, now *counting*: ask as before, but add up the answers, since every earlier partner is one more pair. Pairs of Songs With Total Durations Divisible by 60 counts the pairs of songs whose total length is a multiple of 60: `[30, 20, 150, 100, 40] → 3`. Remainder `r` pairs with remainder `(60 - r) % 60`, so each song adds the count of its partner remainder, then joins the counts itself.

4Sum II asks in how many ways one number from each of four lists can sum to 0: `a = [1, 2], b = [-2, -1], c = [-1, 2], d = [0, 2] → 2`. The brute force is n⁴. Counting the n² sums of the first two lists, then asking with the n² sums of the other two, is the same lookup with the map built first, in O(n²): `four_sum_count` counts every `a + b`, then adds up how many of them cancel each `c + d`.

```python
def count_pairs_divisible_by_60(times):      # 1010
    seen = Counter()                         # STATE: seen[r] = earlier songs with remainder r
    pairs = 0
    for t in times:
        r = t % 60
        pairs += seen[(60 - r) % 60]         # RECORD: every earlier partner makes one more pair
        seen[r] += 1                         # STEP: join the past AFTER asking
    return pairs


def four_sum_count(a, b, c, d):              # 454: build one half, ask with the other
    sums = Counter(x + y for x in a for y in b)       # STATE: a sum from a and b -> how many pairs give it
    return sum(sums[-(x + y)] for x in c for y in d)  # RECORD: each pair from c and d asks for its negation


print(count_pairs_divisible_by_60([30, 20, 150, 100, 40]), count_pairs_divisible_by_60([60, 60, 60]))   # 3 3
print(four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2]))                                               # 2
```

**Try it**
- Drop the outer `% 60` (look up `seen[60 - r]`) and run `count_pairs_divisible_by_60([60, 60, 60])`: 0 instead of 3. Remainder 0 needs a partner with remainder 0, not 60.
- Swap the two lines in the loop: `[60, 60, 60]` gives 6 and `[30, 20, 150, 100, 40]` gives 5. Every song whose remainder is its own partner (0 or 30) now pairs with itself.
- Print `Counter(x + y for x in [1, 2] for y in [-2, -1])`: three keys for four pairs, because two pairs share the sum 0. The dict holds at most n² sums, so 454 costs O(n²) time and space instead of O(n⁴).

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

**The array is the hash table.** The first of them turns a search into a lookup with no map at all. First Missing Positive asks for the smallest positive integer that is not in the array, in O(n) time and O(1) extra space: `[3, 4, -1, 1] → 2`. The O(1) extra space rules out a set.

But the answer is in 1..n+1, because n values can cover at most 1..n, and there are exactly n slots. So let slot `v - 1` say "v is present": swap every value 1..n into its home slot, and the first slot without its own value names the answer.

```text
[3, 4, -1, 1]    3 goes to slot 2, 4 to slot 3, 1 to slot 0; -1 has no home and stays where it lands
[1, -1, 3, 4]    slot 1 should hold 2 but doesn't   ->  answer 2
```

At each index the code keeps swapping the value there into its home slot until the slot holds something that cannot move; then the first index `i` whose slot does not hold `i + 1` is the answer.

```python
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        # nums[i] can't move when it is out of range, already home, or a copy of what its home holds
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:   # FIX: send nums[i] home
            home = nums[i] - 1               # compute the slot BEFORE swapping
            nums[i], nums[home] = nums[home], nums[i]
    for i in range(n):
        if nums[i] != i + 1:                 # RECORD: the first slot without its own value
            return i + 1
    return n + 1                             # RETURN: 1..n are all present


print(first_missing_positive([3, 4, -1, 1]))   # 2
print(first_missing_positive([1, 2, 0]))       # 3
print(first_missing_positive([7, 8, 9]))       # 1
```

**Try it**
- Print `nums` after the first loop for `[3, 4, -1, 1]`: `[1, -1, 3, 4]`. Every value 1..n sits at index value − 1, and the hole at index 1 names the answer 2.
- Change the `while` to `if` and rerun `[3, 4, -1, 1]`: 1 instead of 2. The 1 that was swapped into slot 1 never got sent home.
- Count the swaps for `[2, 3, 4, 5, 1]`: 4. Each swap puts one value home for good, so there are at most n swaps in total, even with a loop inside a loop.

Two cousins use the same slots with a lighter touch. Find All Duplicates in an Array (442) wants every value that appears twice among values 1..n, and Find All Numbers Disappeared in an Array (448) wants every value of 1..n that is missing. Mark v as present by negating `nums[abs(v) - 1]`: a slot that is already negative means v was seen before, and a slot still positive at the end means its value never came.

**Value buckets.** Next, the map hashes by *closeness* instead of equality. Contains Duplicate III asks for two indices at most k apart whose values are at most t apart: `[1, 2, 3, 1], k = 3, t = 0 → True`. The index part is a window of the last k items. The value part cuts the number line into buckets of width t + 1: two values in one bucket are at most t apart, an instant yes, and a close value elsewhere sits in a bucket next door.

```text
t = 3, width 4:   | 0 1 2 3 | 4 5 6 7 | 8 9 10 11 |
                    bucket 0  bucket 1   bucket 2
x = 5 is in bucket 1: a partner within 3 is in bucket 1 (sure hit) or in bucket 0 / 2 (check the one value there)
```

`nearby_almost_duplicate` keeps one value per bucket for the last k items. A new value checks its own bucket and the two next door, stores itself, and evicts the value that just fell out of the window.

```python
def nearby_almost_duplicate(nums, k, t):     # i, j at most k apart with |nums[i] - nums[j]| <= t?
    width = t + 1                            # same bucket  =>  values differ by at most t
    bucket = {}                              # STATE: bucket id -> the one value from the last k indices
                                             # (never two: a second value in a bucket returns True first)
    for i, x in enumerate(nums):
        b = x // width                       # floor division: right for negatives too
        if b in bucket:
            return True                      # RECORD: same bucket
        for nb in (b - 1, b + 1):            # a close value can only live next door
            if nb in bucket and abs(bucket[nb] - x) <= t:
                return True                  # RECORD: a close neighbour
        bucket[b] = x                        # STEP
        if i >= k:
            del bucket[nums[i - k] // width] # FIX: index i - k leaves the window
    return False                             # RETURN


print(nearby_almost_duplicate([1, 2, 3, 1], 3, 0))          # True
print(nearby_almost_duplicate([1, 5, 9, 1, 5, 9], 2, 3))    # False
```

**Try it**
- Change both `x // width` and `nums[i - k] // width` to `int(... / width)` and run `nearby_almost_duplicate([-3, 3], 2, 4)`: `True`, although |−3 − 3| = 6 > 4. `int()` turns −0.6 into 0, so −3 and 3 share bucket 0.
- Print `bucket` at the end of each step for `[1, 5, 9, 1, 5, 9], 2, 3`: it never holds more than k = 2 values, one per bucket.
- Widen the buckets to `width = t + 2` and run `nearby_almost_duplicate([0, 4], 1, 3)`: `True`, although |0 − 4| = 4 > 3. Width t + 1 is the widest that keeps "same bucket ⇒ at most t apart", and unlike `t` it also works for t = 0.

The same buckets crack Maximum Gap (164), which asks for the largest gap between neighbours in sorted order, in O(n): `[3, 6, 9, 1] → 3`, from the sorted 1, 3, 6, 9. It uses the pigeonhole idea: the n − 1 sorted gaps add up to max − min, so the largest gap is at least their average. Buckets narrower than that average cannot hold the largest gap inside them, so each bucket keeps only its min and max, and the answer runs between neighbouring non-empty buckets.

**Counting with order.** The last twist asks the map a question about *order*: "how many inserted values are smaller than x?" A Counter cannot answer that fast; a **Fenwick tree** can. It is a Counter over the values 1..V whose prefix counts cost O(log V): `tree[i]` counts the block of values `(i - lowbit(i), i]`, where `lowbit(i) = i & -i`, so any prefix is a sum of O(log V) blocks.

```text
values 1..8:   tree[8] counts 1..8   tree[4] counts 1..4   tree[6] counts 5..6   tree[7] counts 7
"how many values <= 7" = tree[7] + tree[6] + tree[4]          (7 -> 6 -> 4 -> 0: drop the lowest set bit)
```

Count of Smaller Numbers After Self (315) asks, for each item, how many later items are smaller, `[5, 2, 6, 1] → [2, 1, 1, 0]`: walk from the right and ask the tree before each insert. Reverse Pairs (493) counts the pairs i < j with `nums[i] > 2 · nums[j]`, `[1, 3, 2, 3, 1] → 2`. Merge sort counts such pairs too: see *count while merging* in [Sorting & Selection](#s23).

The code solves Create Sorted Array through Instructions (1649), which inserts numbers one by one into a sorted list, each insert costing the smaller of "how many present values are smaller" and "how many are larger": `[1, 5, 6, 2] → 1`, since only the 2 pays, with one smaller and two larger. `add(v)` adds one to every block that covers v, and `count_upto(v)` adds up the blocks that tile 1..v. Each instruction is priced with two of those counts, and only then added.

```python
def create_sorted_array_cost(instructions):  # 1649: inserting x costs min(# smaller, # larger) so far
    size = max(instructions)
    tree = [0] * (size + 1)                  # STATE: Fenwick tree over values 1..size (index 0 unused)

    def add(v):                              # one more copy of v
        while v <= size:
            tree[v] += 1
            v += v & -v                      # the next block that also covers v

    def count_upto(v):                       # how many inserted values are <= v
        total = 0
        while v > 0:
            total += tree[v]
            v -= v & -v                      # drop the lowest set bit: the block to the left
        return total

    cost = 0
    for inserted, x in enumerate(instructions):          # `inserted` values are in the tree
        cost += min(count_upto(x - 1), inserted - count_upto(x))   # RECORD: smaller vs larger
        add(x)                               # STEP: x joins AFTER it is priced
    return cost                              # RETURN (LeetCode wants it modulo 10**9 + 7)


print(create_sorted_array_cost([1, 5, 6, 2]))                  # 1  (2 has one smaller, two larger)
print(create_sorted_array_cost([1, 3, 3, 3, 2, 4, 2, 1, 2]))   # 4
```

**Try it**
- Use `count_upto(x)` for the smaller side and rerun the second example: 8 instead of 4. Copies of x were counted as smaller.
- Print `tree` before the `return` for `create_sorted_array_cost(list(range(1, 9)))`: `[0, 1, 2, 1, 4, 1, 2, 1, 8]`. Each entry counts a block that ends at its index, `i & -i` values long.
- For 315, number the distinct values 1..m (`rank`), walk `nums` from the right, record `count_upto(rank[x] - 1)` and then `add(rank[x])`: `[5, 2, 6, 1]` gives `[2, 1, 1, 0]`.

### Say it in the interview

> "The brute force fixes one number and scans the rest for its partner: O(n²). But that scan is a search for one known value, target − v, and a hash map answers 'is this value here, and where?' in O(1) on average. So I'll walk once with a dict from value to index: for each number I look up its partner, and only then store the number. O(n) time on average, O(n) space."

Then say what the map means ("value to the index of an earlier copy") and point at the two lines whose order matters: the lookup, then the store. For grouping problems, name the fingerprint and why equal fingerprints mean "same group". Follow-ups to have ready:

- *Sorted input, or O(1) extra space?* [Two Pointers](#s05). To keep the original indices, sort `(value, index)` pairs: O(n log n).
- *Count all pairs instead of finding one?* `pairs += seen[need]` before `seen[v] += 1`.
- *Worst case?* If every key collides, one lookup degrades to O(n); with Python's hashing of numbers and strings that is rare.
- *Group Anagrams cost?* O(n·k) with the count key, O(n·k log k) with the sorted key, for n words of length k.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Contains Duplicate II | `arrays_hashing/contains_duplicate_ii.py` | store each value's last index; only the nearest earlier copy can be within k |
| Contains Duplicate III | `arrays_hashing/contains_duplicate_iii.py` | buckets of width t + 1 over the last k values: same bucket is a hit, else check both neighbours |
| Count of Smaller Numbers After Self | `arrays_hashing/count_of_smaller_numbers_after_self.py` | count, from the right, the smaller values already seen: a Fenwick tree over ranks, or count while merging |
| Create Sorted Array through Instructions | `arrays_hashing/create_sorted_array_through_instructions.py` | Fenwick tree over values: cost of x = min(prefix(x − 1), inserted − prefix(x)) |
| Encode and Decode Strings | `arrays_hashing/encode_and_decode_strings.py` | frame each string as `len#payload`; the decoder jumps over payloads, so any character is safe |
| First Missing Positive | `arrays_hashing/first_missing_positive.py` | the answer is in 1..n+1: swap each v into slot v − 1, then find the first wrong slot |
| Group Anagrams | `arrays_hashing/group_anagrams.py` · `practice/simple/02_group_anagrams.py` | fingerprint = 26 letter counts as a tuple (or the sorted word); bucket words by it |
| Longest Consecutive Sequence | `arrays_hashing/longest_consecutive_sequence.py` · `practice/simple/04_longest_consecutive_sequence.py` | set of values; count up only from run starts (x − 1 missing), so each value is walked once |
| Majority Element | `arrays_hashing/majority_element.py` | Boyer-Moore: different values cancel in pairs and the majority survives |
| Maximum Gap | `arrays_hashing/maximum_gap.py` | buckets narrower than the average gap: the max gap runs between neighbouring non-empty buckets |
| Reverse Pairs | `arrays_hashing/reverse_pairs.py` | merge sort: on two sorted halves, count x > 2r with a forward-only pointer, then merge |
| Top K Frequent Elements | `arrays_hashing/top_k_frequent_elements.py` | count, then bucket values by frequency (1..n) and read the buckets from high to low |
| Two Sum | `arrays_hashing/two_sum.py` · `practice/simple/01_two_sum.py` | dict value → index; look up target − v before storing v |
| Valid Sudoku | `arrays_hashing/valid_sudoku.py` | one set of (unit, digit) pairs, or a set per row, column and box; box id = (r // 3, c // 3) |

### Self-check

1. When do you build the whole map first instead of asking, then storing, item by item?
<details><summary>Answer</summary>When the question is about the whole collection (frequencies, the k most frequent, runs of consecutive values): an item's answer depends on items that come after it, so the map must be complete before you read it. Ask-then-store fits questions that pair an item with an <em>earlier</em> one, like Two Sum.</details>

2. Longest Consecutive Sequence has a `while` inside a `for`. Why is it still O(n)?
<details><summary>Answer</summary>The <code>while</code> runs only from run starts (values whose <code>x - 1</code> is missing), and each run is walked once from its start. Every value belongs to exactly one run, so all the walks together take at most n steps.</details>

3. When does Boyer-Moore voting give a wrong answer, and how do you protect against it?
<details><summary>Answer</summary>When no value occurs more than n / 2 times it still returns some candidate (<code>[1, 2, 3]</code> gives 3). If a majority is not guaranteed, make a second pass that counts the candidate and checks <code>count > n // 2</code>.</details>

4. In First Missing Positive, why is it safe to leave values ≤ 0 and values > n wherever they land?
<details><summary>Answer</summary>The answer is the smallest of 1..n+1 that is missing. Values outside 1..n can never fill one of the slots for 1..n, so they cannot change which of those numbers is missing first; they just occupy slots that will be reported as holes.</details>
