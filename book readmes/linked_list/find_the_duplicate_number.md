# Find the Duplicate Number
*LeetCode 287 · Medium · Pattern: Floyd's tortoise and hare (fast/slow pointers) · Reading time ~9 min*

## The problem

nums has n + 1 integers, each in [1, n], and exactly one value repeats (possibly many times). Return it without
modifying nums and with O(1) extra space.

```text
Example: nums = [1,3,4,2,2] -> 2; nums = [3,1,3,4,2] -> 3.
```

## What the problem is really asking

You get an array of n + 1 integers. Every value lies between 1 and n. Since there are n + 1 slots and only n possible values, at least one value must appear twice (pigeonhole). The problem promises exactly one value repeats, though it may repeat many times. Return that value.

The catch is in the rules: you may not modify the array (so no sorting, no marking cells negative), and you may use only O(1) extra memory (so no hash set). The answer is a single integer, and what makes it hard is that the two obvious tools for "find a repeat" are both forbidden.

```text
  index:  0  1  2  3  4
  nums:  [1, 3, 4, 2, 2]        n = 4, values in 1..4
                   ^  ^
                   two cells hold 2  ->  answer 2
```

## Do it by hand first

By hand you would scan and keep a tally of seen values, a *set*, which is exactly what we may not store. So try a procedure that remembers one number at a time: treat each value as an instruction "go to that index", start at index 0, and follow.

```text
  at 0, nums[0]=1  -> go to 1
  at 1, nums[1]=3  -> go to 3
  at 3, nums[3]=2  -> go to 2
  at 2, nums[2]=4  -> go to 4
  at 4, nums[4]=2  -> go to 2    (been here before!)
```

You arrived at 2 once from index 3 and once from index 4, and both cells hold the value 2. The place where the walk first repeats is the duplicate. Your hand kept track of only *where it was standing*: the seed of a pointer.

## The first honest attempt

The strong candidate's first answer: compare every pair of positions (i, j) and return nums[i] when the two match. That is O(n^2) time, O(1) space, and it obeys both rules. It is also slow for n = 100,000.

The second answer, the clever one: binary search on the *value*. Guess mid; count how many entries are <= mid. If there were no duplicate among 1..mid, at most mid entries could be <= mid, so a count above mid means the duplicate is in 1..mid. This is O(n log n) time and O(1) space.

Both waste the same thing: they re-read the array over and over without learning anything structural from it.

```text
  pairs:   i=0 vs 1,2,3,4
           i=1 vs   2,3,4      each value is read
           i=2 vs     3,4      again for every
           i=3 vs       4      earlier position

  binary search on value, n = 4:
           mid=2: scan all 5 cells, count(<=2) = 3 > 2
           mid=1: scan all 5 cells, count(<=1) = 1
           -> answer 2, after reading every cell twice
```

Each scan collapses the whole array into one count and throws away which cell points where. The hand-walk above used that "points where" information and found the answer in a handful of steps.

## The turning point

**Claim: if you read the array as a linked list where index i has a next pointer to index nums[i], the duplicate value is exactly the entrance of the cycle reached from index 0.**

*It is a list.* Each index has exactly one outgoing arrow, i -> nums[i]. Every value is between 1 and n, which is a valid index, so no arrow falls off the array. Following arrows from any start is just following `next` pointers.

```text
  the array as an implicit linked list

  index:  0    1    2    3    4
  nums:  [1,   3,   4,   2,   2]

     0 --> 1 --> 3 --> 2 --> 4
                       ^     |
                       +-----+
            (4 -> 2 closes the loop)
```

*There must be a cycle.* There are only n + 1 nodes and every node has a next. A walk can never stop, so it must eventually revisit a node. Once it revisits one, it loops forever. The walk from 0 traces the shape of the Greek letter rho: a tail, then a loop.

*Index 0 is on the tail, never in the loop.* No value is 0, so no arrow points into index 0. Something with no incoming arrow cannot be part of a loop. So the tail has length at least one.

*The entrance has two incoming arrows.* The node where the tail meets the loop is entered once from the last tail node and once from the last loop node. Those are two different indices i and j with nums[i] = nums[j] = entrance. Two cells holding the same value: that value is the duplicate. And because only one value repeats, there is only one such node.

So "find the duplicate" has become "find where the cycle begins, with O(1) memory and no writes": Linked List Cycle II, with `node.next` translated to `nums[i]`.

Recap of Floyd. Let the tail have a steps, let the slow and fast pointers meet b steps into the loop, and let the loop have length c. Slow walked a + b; fast walked twice that; fast's extra distance is whole laps, so a + b is a multiple of c. Therefore walking a more steps from the meeting point lands exactly on the entrance (you complete those laps). A second pointer starting at index 0 also needs a steps to reach the entrance. Move both one step at a time and they meet there.

In our example: tail 0, 1, 3 gives a = 3; loop {2, 4} has c = 2; the meeting point will be index 4, so b = 1. Check: a + b = 4, a multiple of 2.

## Watch it work

`nums = [1, 3, 4, 2, 2]`. Phase 1 moves slow one hop (`slow = nums[slow]`) and fast two hops (`fast = nums[nums[fast]]`) per round.

Frame 1 — start.

```text
     0 --> 1 --> 3 --> 2 --> 4
     S                 ^     |
     F                 +-----+
  slow = 0   fast = 0   (phase 1)
```

Both pointers stand on index 0; the loop moves before it compares, so this equality does not count.

Frame 2 — round 1.

```text
     0 --> 1 --> 3 --> 2 --> 4
           S     F     ^     |
                       +-----+
  slow = nums[0] = 1    fast = nums[nums[0]] = nums[1] = 3
```

Slow took one arrow, fast took two.

Frame 3 — round 2.

```text
     0 --> 1 --> 3 --> 2 --> 4
                 S     ^     F
                       +-----+
  slow = 3    fast = nums[nums[3]] = nums[2] = 4
```

Fast has entered the loop; slow is still on the tail.

Frame 4 — rounds 3 and 4.

```text
  round 3: slow = 2, fast = nums[nums[4]] = nums[2] = 4
  round 4: slow = 4, fast = nums[nums[4]] = 4

     0 --> 1 --> 3 --> 2 --> 4
                       ^     S F
                       +-----+   meet at index 4
```

In round 3 fast lapped the 2-node loop and returned to 4; in round 4 slow arrived, so they meet at 4, which is not yet the answer.

Frame 5 — phase 2.

```text
  slow restarts at 0; both move 1 hop per step
     step 1: slow = 1    fast = nums[4] = 2
     step 2: slow = 3    fast = nums[2] = 4
     step 3: slow = 2    fast = nums[4] = 2   equal!

     0 --> 1 --> 3 --> 2 --> 4
                       S
                       F    return 2
```

After a = 3 steps each, slow walked the tail and fast walked from the meeting point around to the entrance; they collide at index 2, and 2 is the duplicate.

The only state was two indices, and the array was only read. Phase 1 put both pointers inside the loop; phase 2 relied on "tail length equals the distance from meeting point to entrance, modulo the loop length".

## Why it is correct

Structure: the walk from 0 is infinite on a finite set, so it enters a cycle; 0 has no incoming arrow, so the cycle entrance e is reached from two distinct indices, both holding e. Only one value repeats, so e is the answer.

Algorithm (Floyd). Phase 1: once both pointers are in the loop, the gap between them shrinks by exactly one each round (fast gains one hop per round), so they meet within c rounds after slow enters. Phase 2: with a + b = k*c, a pointer at the meeting point that walks a steps ends at position b + a = k*c past the entrance, which is the entrance. A pointer starting at 0 that walks a steps ends at the entrance by definition. They cannot meet earlier, because before step a the restarted pointer is still on the tail, where the other pointer never is.

## Cost

- **Time: O(n).** Phase 1 ends within a + c rounds and phase 2 takes a steps; both a and c are at most n + 1.
- **Space: O(1).** Two integer indices; the array is never copied or changed.
- The earlier level, binary search on value, is O(n log n) time and O(1) space; sorting or a hash set gives O(n) time but breaks a rule.

## Variations you will meet

- **"You may use O(n) space" or "you may modify the array".** Then a set, or marking `nums[abs(v)]` negative, or cyclic sort (put value v at index v) is simpler.
- **First Missing Positive / Find All Duplicates (LeetCode 41, 442).** Same "values are indices" view, but with permission to modify, so you swap or negate cells instead of walking.
- **Happy Number (LeetCode 202).** Another implicit list: the next node of x is the sum of the squares of its digits. Floyd's phase 1 decides whether the walk reaches 1 or loops.
- **Values in 0..n-1 instead of 1..n.** Then index 0 can be pointed to and the walk may start inside a loop; the argument breaks. Always check that your start node has no incoming arrow.

## What to carry forward

Whenever every element names another element, you have an implicit linked list, and "a value appears twice" means "a node has two incoming arrows", which is a cycle entrance. The next problem, Intersection of Two Linked Lists, is about a different kind of node with two incoming arrows: two separate lists that merge into one shared tail.
