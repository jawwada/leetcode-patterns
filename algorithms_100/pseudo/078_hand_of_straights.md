---
rank: 78
slug: hand_of_straights
---

Given a hand of cards and a group size, decide whether the cards can be split into groups of `group_size` consecutive values, every card used exactly once. `[1, 2, 3, 6, 2, 3, 4, 7, 8]` with `group_size = 3` can, as `[1, 2, 3]`, `[2, 3, 4]` and `[6, 7, 8]`; `[1, 2, 4, 5, 6, 7]` cannot, because the group that `1` must start needs a `3` that is not there.

The brute force deals the cards into groups every possible way, an exponential search. One fact collapses it: the smallest card left in the hand cannot sit in the middle or at the end of a group, because nothing smaller remains to come before it, so it must start one. If it has `starts` copies, all of them start groups, and each of the next `group_size - 1` values must supply `starts` copies too. So count the cards, walk the distinct values in increasing order, and whenever a value still has copies left, peel off its `starts` groups at once; a value that runs short is a gap, and the answer is false.

Picture the counts as a histogram over the number line. A group is a horizontal strip `group_size` columns wide, and the question is whether such strips tile the histogram exactly. The leftmost column can only be covered by strips that start there, so its height says how many strips to lay down, and laying them lowers the columns to its right. When a later column is too short for the strips that must cross it, no tiling exists. Checking `len(hand) mod group_size` first rejects the hopeless hands before any counting.

```text
count 2               ●   ●
count 1           ●   ●   ●   ●       ●   ●   ●
card              1   2   3   4   5   6   7   8

count             1   2   2   1   -   1   1   1
1 starts 1        0   1   1   1   -   1   1   1   takes 1, 2, 3
2 starts 1        0   0   0   0   -   1   1   1   takes 2, 3, 4
  3 and 4 left at 0, skipped
6 starts 1        0   0   0   0   -   0   0   0   takes 6, 7, 8
  7 and 8 left at 0, skipped
every count reaches 0: true ✓
```

```pseudo
FUNCTION CanFormStraights(hand, group_size)
    IF len(hand) mod group_size ≠ 0
        RETURN false
    count ← empty map
    FOR EACH card IN hand
        count[card] ← count.get(card, 0) + 1
    FOR EACH card IN sorted(count)         // distinct cards, smallest first
        starts ← count[card]               // groups that must start at card
        IF starts > 0
            FOR next_card FROM card TO card + group_size - 1
                IF count.get(next_card, 0) < starts
                    RETURN false           // a group would have a gap
                count[next_card] ← count[next_card] - starts
    RETURN true
```

Sorting the distinct values costs `O(n log n)`, while the peeling is only `O(n)`: every value that starts groups starts at least one, so at most `n / group_size` values do, and each costs `group_size` steps. The map takes `O(n)` space. Reach for smallest-first peeling when a multiset must be split into runs of consecutive values. LC 1296 is the same problem, and Split Array into Consecutive Subsequences (LC 659) is its cousin with runs of length at least 3, where each card first extends a run that ends just below it and only otherwise opens a new one. The classic mistake is starting a group at a card that is not the smallest left: walking the hand in input order, `[2, 1, 3]` with `group_size = 3` tries `2, 3, 4` first and fails, although `[1, 2, 3]` is a valid group.

*Practice:* LC 846 Hand of Straights · LC 1296 Divide Array in Sets of K Consecutive Numbers · LC 659 Split Array into Consecutive Subsequences
