# Insert Delete GetRandom O(1)

*LeetCode 380 · Medium · Pattern: Array + index map (swap-with-last delete) · Reading time ~7 min*

## The problem

Implement RandomizedSet with insert(val) -> bool (False if already present), remove(val) -> bool (False if absent) and
getRandom() -> a uniformly random element, each in average O(1).

```text
Example: insert(1) True, remove(2) False, insert(2) True,
  getRandom() in {1, 2}, remove(1) True, insert(2) False,
  getRandom() == 2.
```

## What the problem is really asking

Build a set of integers with three operations, each O(1) on average:

- `insert(val)` adds val and returns True, or returns False if it was already there;
- `remove(val)` deletes val and returns True, or returns False if it was absent;
- `getRandom()` returns one of the current elements, each with equal probability.

Each answer is a boolean or a value. The difficulty is that the three operations want different structures. Membership wants a hash set. A uniform random pick wants positions 0..n-1 with no holes, so you can draw a random index. No single built-in gives both.

```text
 insert(5) insert(8) insert(2) insert(9)
 set = {5, 8, 2, 9}
 getRandom(): each of 5, 8, 2, 9 with probability 1/4
 remove(8) -> True;  remove(4) -> False
```

## Do it by hand first

Imagine the elements written on numbered cards laid in a row: slot 0, 1, 2, 3. To pick uniformly, roll a 4-sided die and take that slot. Fine. Now remove 8, which sits in slot 1. If you slide every card right of it one step left, the row stays gapless, but that is a lot of sliding for a long row. A lazier person picks up the *last* card, 9, and drops it into the hole. The row is gapless again; the order changed, but nobody asked for order.

```text
 slots:  0   1   2   3
        [5] [8] [2] [9]
             ^ remove
        [5] [9] [2]          9 moved from slot 3 to slot 1
```

To do that quickly, your hand had to know *which slot 8 was in* without scanning. So next to the row you would keep a little index card: 5 is in slot 0, 8 in slot 1, and so on. When 9 moved, you corrected its line on the index card. That index card is a hash map from value to position.

## The first honest attempt

Use a plain Python list. `insert` checks `val in list` (O(n) scan) then appends. `remove` checks membership (O(n)) then `list.remove(val)`, which scans again and shifts every later element left (O(n)). `getRandom` is `random.choice(list)`, O(1). Space O(n).

```text
 remove(8) on [5, 8, 2, 9, 4, 7, 1]
   scan:   5? 8! found at 1          (search work)
   shift:  [5, _, 2, 9, 4, 7, 1]
           [5, 2, 9, 4, 7, 1]        5 elements move one slot
                                     left (shift work)
```

The two kinds of waste are visible: searching for a value whose location could have been remembered, and shifting a whole suffix only to preserve an order nobody uses.

The alternative brute force — a hash set — has the opposite gap: insert and remove are O(1), but a set has no positions, so a uniform random pick means converting it to a list first: O(n).

## The turning point

**Claim: the array only needs to be dense, not ordered, so deleting from the middle can be done by moving the last element into the hole and popping the tail.**

Justification: `getRandom` draws a uniform index in `[0, n)` and is correct as long as each current element occupies exactly one slot in that range. Which slot does not matter. Moving the last element to the victim's slot keeps every element in exactly one slot, and popping the tail shrinks the range by one — the same effect as deletion, at the cost of one copy instead of a shift.

The combined structure follows from the method of the chapter. List the questions:

- "Is val present, and where?" — a dict `idx: val -> slot`.
- "Give me a uniform random element" — a dense list `vals`.
- "Delete val in O(1)" — the dict tells us the slot; swap-with-last plus pop keeps the list dense.

Then check every write against both structures. `insert` appends to `vals` and records `idx[val] = len(vals) - 1`. `remove` must change *both* structures in *both* places that moved: the victim's entry disappears, and the moved element's slot changes. The order of these updates matters in one case: when the victim *is* the last element. Then "last" and "victim" are the same value, and the self-swap is harmless only if we write `idx[last] = i` before we `del idx[val]`. Do it in the other order and you re-create the deleted key.

```text
 i, last = idx[val], vals[-1]
 vals[i] = last; idx[last] = i     # fill the hole
 vals.pop(); del idx[val]          # drop tail, then victim
```

What the tracker remembers: each value's slot. What it forgets: insertion order, completely.

## Watch it work

Operations: insert 5, 8, 2, 9; insert(8); remove(8); remove(2); remove(4); remove(5); getRandom().

```text
Frame 1  insert 5, 8, 2, 9 -> True x4
 slot:  0   1   2   3
 vals: [5] [8] [2] [9]
 idx:  {5:0, 8:1, 2:2, 9:3}
```
Each insert appends and records the new slot.

```text
Frame 2  insert(8) -> False
 vals: [5] [8] [2] [9]       (unchanged)
 idx:  {5:0, 8:1, 2:2, 9:3}
```
8 is already a key in idx, so nothing is written.

```text
Frame 3  remove(8) -> True
 i = idx[8] = 1, last = 9
 vals[1] = 9      [5] [9] [2] [9]   idx[9] = 1
 pop tail         [5] [9] [2]       del idx[8]
 idx:  {5:0, 9:1, 2:2}
```
The hole at slot 1 is filled by the old tail; only 9's index changes.

```text
Frame 4  remove(2) -> True     (victim is the last element)
 i = idx[2] = 2, last = 2
 vals[2] = 2, idx[2] = 2   (self-swap, no change)
 pop tail, del idx[2]
 vals: [5] [9]     idx: {5:0, 9:1}
```
The edge case: because idx[last] was written before deleting idx[val], 2 is truly gone.

```text
Frame 5  remove(4) -> False ; remove(5) -> True
 remove(5): i=0, last=9
 vals[0] = 9, idx[9] = 0, pop, del idx[5]
 vals: [9]     idx: {9:0}
```
4 was never present; removing 5 moves 9 to the front.

```text
Frame 6  getRandom() -> 9
 random index in [0, 1) = 0  -> vals[0] = 9
```
One element, one slot, so the uniform pick must return 9.

In every frame, `vals` has no holes, `len(idx) == len(vals)`, and `vals[idx[v]] == v` for every key v.

## Why it is correct

The invariant is the two-way agreement drawn in the last line above: `vals` holds each current element exactly once, in slots `0..n-1`, and `idx` maps each element to its slot. `insert` preserves it trivially. For `remove(val)` with `i = idx[val]` and `last = vals[-1]`: after `vals[i] = last; idx[last] = i`, the element `last` sits at slot i and idx agrees; the tail slot now holds a duplicate, which `pop` removes; deleting `idx[val]` removes the victim from the map. If `val == last`, the first line writes val over itself and the final delete removes it, so the result is still correct. Given the invariant, `random.choice(vals)` picks each element with probability 1/n because each occupies exactly one of n slots.

## Cost

- **Time:** O(1) average for all three — dict lookups, one list write, one pop from the end, and `random.choice` on a list.
- **Space:** O(n) — each element stored once in the list and once as a dict key.

## Variations you will meet

- **Duplicates allowed (LeetCode 381).** `idx` becomes `val -> set of slots`. Remove takes any slot from the set, swaps the last element in, and updates the moved element's slot set: discard its old slot (n-1), add the new one. The self-swap order trap is sharper here.
- **Weighted random pick.** Uniform-by-slot no longer works; you need prefix sums with binary search (static) or a Fenwick tree (dynamic weights).
- **Random pick from a hash map you cannot modify.** Sample random buckets until one is non-empty — expected O(1) only if load is bounded; this is the hashmap problem's buckets reappearing.
- **getRandom without repeats until all are seen.** Fisher–Yates on the fly: swap a random slot in `[0, k)` to position k-1 and shrink k — the same swap-with-last idea.

## What to carry forward

When order does not matter, delete from an array by moving the last element into the hole, and keep a value-to-slot map so every element can be found and every move can be recorded. The next problem keeps an array but cares deeply about order: browser history is a line of pages and a cursor on it.
