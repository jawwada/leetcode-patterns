---
title: "100 Algorithms"
subtitle: "in Pseudocode"
date: "Ordered by importance for coding interviews"
documentclass: scrbook
classoption: [oneside, 11pt, openany]
papersize: letter
geometry: [margin=0.9in, headheight=14pt]
toc: true
toc-depth: 1
colorlinks: true
linkcolor: accent
urlcolor: accent
toccolor: ink
---


# How to Read This Book {#how-to-read}

```{=latex}
\markboth{How to Read This Book}{}
```

This book holds one hundred algorithms in the order to learn them. The order is importance for a coding interview: how often the idea appears, how many other problems it unlocks, and how much it costs to be missing it. Tier 1, the first thirty-five, are the algorithms to know cold. Tier 2, the next thirty-five, come up often enough that you should know them well. Tier 3, the last thirty, are good to know and separate a prepared candidate from a strong one. Inside a tier, related algorithms sit next to each other, so each tier is one pass over every topic and the next tier deepens it.

Every entry fits on a page or two and always reads in the same order. It opens with the problem in plain words and a tiny example. Then comes the idea: when a brute force exists, one sentence names it and its cost, and the rest explains the insight that beats it as a picture of the data and the motion of the algorithm. A framed picture traces the algorithm on the example, and every number in it was produced by running the code. The pseudocode follows, then a closing paragraph on the cost, the signals in a problem statement that call for the algorithm, and the classic mistake, and finally a few LeetCode problems to practise on. A reference such as #41 points to entry 41 and is a link.

The companion book, *100 Algorithms in Python*, has the same entries in the same order, each one a short runnable file whose variable names match this pseudocode line for line.

## Notation

The pseudocode reads like careful English. Indentation alone marks a block, so there are no END lines. Keywords are in capitals, `←` assigns and `=` compares, so no line ever has to be read twice. Ranges are inclusive at both ends, arrays start at index 0, and containers are written with the operation you would say out loud.

```pseudo
FUNCTION Name(a, b)               // RETURN hands back a value
    x ← 0                         // assignment
    IF x = 0 AND b ≠ null         // comparison: = ≠ < ≤ > ≥
        ...
    ELSE IF x > 0 OR NOT done
        ...
    ELSE
        ...
    FOR i FROM 0 TO n - 1         // inclusive at both ends
    FOR i FROM n - 1 DOWNTO 0     // counting down
    FOR EACH x IN items
    WHILE lo < hi
    floor(a / b), a mod b, ∞      // integer division, remainder, infinity
    seen ← empty map              // also: empty set, list, stack, queue, min-heap
    seen[key] ← value             // write; "key IN seen" tests membership
    stack.push(x), stack.pop(), stack.top()
    queue.enqueue(x), queue.dequeue()
    heap.push(x), heap.pop(), heap.top()
    a[i..j]                       // the slice from i to j, both included
```

# Topic Index {#topic-index}

```{=latex}
\markboth{Topic Index}{}
```

The book is ordered by importance. This index groups the same entries by topic; every number is a link.

| Topic | Entries |
|:--------------------|:------------------------------------------------------------------------|
| Arrays & Hashing | #1 Two Sum · #2 Prefix Sum + Hash Map · #72 Boyer-Moore Majority Vote |
| Hash Map Internals | #36 Hash Map with Separate Chaining · #71 Hash Map with Open Addressing |
| Two Pointers | #4 Reverse a Linked List · #5 3Sum · #37 Trapping Rain Water · #38 Dutch National Flag |
| Sliding Window | #7 Longest Substring Without Repeating Characters · #8 Minimum Window Substring |
| Binary Search | #9 Binary Search · #10 Binary Search on the Answer · #39 Search in a Rotated Sorted Array · #40 Median of Two Sorted Arrays · #73 Median of K Sorted Arrays |
| Sorting | #11 Merge Sort · #12 Quick Sort · #43 Bucket Sort · #74 Counting Sort · #75 Heap Sort |
| Heaps | #13 Top-K Elements · #14 Merge K Sorted Arrays · #41 Heapify · #42 Quickselect |
| Stacks | #16 Valid Parentheses · #17 Monotonic Stack · #44 Largest Rectangle in Histogram · #45 Basic Calculator |
| Queues | #46 Sliding Window Maximum · #76 Circular Queue |
| Intervals | #18 Merge Intervals · #19 Meeting Rooms II |
| Greedy | #20 Kadane's Algorithm · #21 Best Time to Buy and Sell Stock · #47 Jump Game · #48 Jump Game II · #49 Gas Station · #50 Interval Scheduling · #51 Task Scheduler · #52 Partition Labels · #77 Candy · #78 Hand of Straights |
| Backtracking | #22 Subsets · #23 Permutations · #53 Combination Sum · #54 Word Search · #79 N-Queens |
| DFS | #25 Diameter and Max Path Sum · #26 Lowest Common Ancestor · #28 Depth-First Search on a Graph · #29 Number of Islands · #55 Serialize and Deserialize a Binary Tree |
| BFS | #24 Binary Tree Level-Order Traversal · #30 BFS Shortest Path · #58 Multi-Source BFS · #59 Word Ladder · #80 Bipartite Check |
| Cycle Detection | #6 Floyd's Tortoise and Hare · #60 Cycle Detection in a Directed Graph · #81 Cycle Detection in an Undirected Graph |
| Topological Sort | #31 Kahn's Algorithm · #61 Topological Sort with DFS |
| Connected Components | #32 Union-Find · #62 Connected Components |
| Shortest Path | #33 Dijkstra's Algorithm · #82 Bellman-Ford |
| MST | #83 Kruskal's Minimum Spanning Tree · #84 Prim's Minimum Spanning Tree |
| BST | #27 Validate a Binary Search Tree · #56 BST Search, Insert, Delete · #57 BST Iterator |
| Tries | #34 Trie · #63 Word Search II |
| Strings | #3 Group Anagrams · #64 KMP String Matching · #65 Longest Palindromic Substring · #66 Encode and Decode Strings · #85 Rabin-Karp · #86 Longest Common Prefix · #87 Text Justification · #88 String Compression · #89 Reverse Words in a String · #90 Multiply Strings |
| Math | #67 Fibonacci · #91 GCD and LCM · #92 Sieve of Eratosthenes · #93 Fast Exponentiation · #94 Reservoir Sampling |
| Geometry | #95 Orientation and Segment Intersection · #96 Convex Hull · #97 Max Points on a Line |
| Bit Manipulation | #68 Single Number · #98 Count Set Bits · #99 Bitmask Subset Enumeration |
| Design | #15 Find Median from Data Stream · #35 LRU Cache · #69 Insert Delete GetRandom O(1) · #70 Time-Based Key-Value Store · #100 Rate Limiter |

# Tier 1 · Must Know Cold {#tier1}

```{=latex}
\markboth{Tier 1 · Must Know Cold}{}
```

These thirty-five algorithms are the core of the interview. Each one is the standard answer to a whole family of problems: hashing to remember the past, two pointers and sliding windows for sequences, binary search for anything monotone, sorting and heaps for order, stacks for nesting, BFS and DFS for every tree and graph, Kahn's algorithm, union-find and Dijkstra for dependencies, components and distances, the trie for prefixes and the LRU cache for design. Learn them until you can write each one from a blank page without hesitation.

```{=latex}
\clearpage
```

## 1. Two Sum {#a1}

```{=latex}
\markright{1. Two Sum}
```

[Hash Map of Complements · Arrays & Hashing · Tier 1]{.meta}

Given an array of integers and a target, return the indices of the two numbers that add up to the target; exactly one such pair exists. In `[2, 7, 11, 15]` with target `9` the answer is `[0, 1]`, because `2 + 7 = 9`.

The brute force tries every pair, `n(n - 1) / 2` of them, for `O(n²)` time. Its waste is that every number keeps asking the same question, "did my partner appear earlier?", and answers it by rescanning the past. A hash map answers that question in `O(1)`. Walk the array once; at index `i` the partner the current number needs is `target - nums[i]`. If that value is already a key in the map, the pair is complete. If not, store the current number with its index and move on, so that a later number can find it.

Picture the map as the memory of everything to the left of the pointer. Each number looks backward exactly once, through the map, instead of across the whole prefix. Checking before storing is what stops a number from pairing with itself when the target is twice its value.

```text
target = 9
  i   nums[i]   need = 9 - nums[i]   need in seen?   seen after the step
  0      2              7                 no          {2: 0}
  1      7              2              yes → 0        stop: answer [0, 1]
```

```pseudo
FUNCTION TwoSum(nums, target)
    seen ← empty map                       // value → index
    FOR i FROM 0 TO len(nums) - 1
        need ← target - nums[i]
        IF need IN seen                    // partner appeared earlier
            RETURN [seen[need], i]
        seen[nums[i]] ← i                  // store only after checking
    RETURN empty list
```

One pass with constant-time lookups gives `O(n)` time, and the map costs `O(n)` space. Reach for this pattern whenever a problem asks for a pair with a fixed sum, difference or other exact relationship and the input is unsorted: the map turns "search the past" into a single lookup. When the array is sorted, two pointers closing in from both ends do the same job in `O(1)` space; that loop is the heart of 3Sum (#5). The classic mistake is storing `nums[i]` before the lookup, which pairs `3` with itself for target `6` in `[3, 2, 4]` and returns `[0, 0]`.

*Practice:* LC 1 Two Sum · LC 167 Two Sum II - Input Array Is Sorted · LC 454 4Sum II · LC 15 3Sum

```{=latex}
\clearpage
```

## 2. Prefix Sum + Hash Map {#a2}

```{=latex}
\markright{2. Prefix Sum + Hash Map}
```

[Subarray Sum Equals K · Arrays & Hashing · Tier 1]{.meta}

Given an array of integers, negatives allowed, and a target `k`, count the contiguous subarrays whose sum is exactly `k`. In `[2, -1, 1, 2]` with `k = 2` the answer is `4`: `[2]`, `[2, -1, 1]`, `[-1, 1, 2]` and the final `[2]`.

The brute force fixes every start, extends every end with a running sum and pays `O(n²)`. The insight is that every subarray sum is a difference of two prefix sums. If `prefix` is the sum of everything up to the current index and some earlier prefix equals `prefix - k`, the stretch between them sums to exactly `k`. The question at each index becomes Two Sum (#1) looking backward: how many earlier prefixes equal `prefix - k`? A map from prefix sum to the number of times it has occurred answers it in one lookup. The map is seeded with `0 → 1`, the empty prefix before index 0, so that a subarray starting at index 0 has a partner to find.

Picture the prefix sums as a walk of heights, `0, 2, 1, 2, 4` here. Every subarray is a step from an earlier height to a later one, and the algorithm counts the steps that climb exactly `k`. The map stores counts, not indices, because a height can come back: `2` occurs twice, and both visits pair with the final `4`. That return is why a sliding window fails. With only positive numbers the walk climbs strictly, so each right end has at most one matching left end, and a window that shrinks whenever its sum passes `k` finds it. A negative number lets the walk fall back, the window sum stops being monotone, and the window cannot tell which end to move; on this array it finds only 3 of the 4.

```text
k = 2; prefix_count starts as {0: 1} for the empty prefix
  x   prefix   prefix - k   found   total   prefix_count after
  2      2          0         1       1     {0: 1, 2: 1}
 -1      1         -1         0       1     {0: 1, 2: 1, 1: 1}
  1      2          0         1       2     {0: 1, 2: 2, 1: 1}
  2      4          2         2       4     {0: 1, 2: 2, 1: 1, 4: 1}
the four subarrays:  [2]   [2, -1, 1]   [-1, 1, 2]   [2]
```

```pseudo
FUNCTION SubarraySum(nums, k)
    prefix_count ← empty map               // prefix sum → how many times seen
    prefix_count[0] ← 1                    // the empty prefix, before index 0
    prefix ← 0
    total ← 0
    FOR EACH x IN nums
        prefix ← prefix + x                // sum of nums up to and including x
        // each earlier prefix equal to prefix - k starts one subarray of sum k
        total ← total + prefix_count.get(prefix - k, 0)
        prefix_count[prefix] ← prefix_count.get(prefix, 0) + 1   // record last
    RETURN total
```

One pass with constant-time map operations gives `O(n)` time, and the map costs `O(n)` space. Reach for this pattern whenever a problem asks about subarrays with an exact sum, especially when negative numbers rule out a window. Key the map by `prefix mod k` to count sums divisible by `k`, or store each prefix's first index instead of a count to find the longest such subarray, as in Contiguous Array with every `0` read as `-1`. The classic mistakes are forgetting the seed, which misses every subarray that starts at index 0 (2 of the 4 here), and recording the current prefix before counting, which pairs a prefix with itself when `k = 0`: on `[0, 0, 0]` that reports 9 subarrays instead of 6.

*Practice:* LC 560 Subarray Sum Equals K · LC 974 Subarray Sums Divisible by K · LC 523 Continuous Subarray Sum · LC 525 Contiguous Array

```{=latex}
\clearpage
```

## 3. Group Anagrams {#a3}

```{=latex}
\markright{3. Group Anagrams}
```

[Canonical-Key Hashing · Strings · Tier 1]{.meta}

Given a list of lowercase words, group together the words that are anagrams of each other, words that use the same letters the same number of times. `["eat", "tea", "tan", "ate", "nat", "bat"]` becomes `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`, with the groups in the order they first appear.

The brute force tests every pair of words for being anagrams, `O(n²)` tests at `O(L)` each for words of length `L`. The insight is to stop comparing words with one another and give each word a canonical key: a value that comes out identical for two words exactly when they are anagrams. Grouping then becomes a single pass that files each word in a hash map under its key. Two keys work. The sorted letters, `"aet"` for eat, tea and ate, cost `O(L log L)` per word. The 26 letter counts cost `O(L)`, and that is the key the code uses, frozen into a tuple because a map key must be immutable to be hashed.

Picture each key as a barcode of 26 slots, one per letter from `a` to `z`. Shuffling a word's letters never changes its barcode, so anagrams print the same stripes and the map only has to drop equal barcodes into the same bucket. The order of the letters is forgotten; how many of each letter there are survives.

```text
          abcdefghijklmnopqrstuvwxyz    (letter counts, "." for zero)
"eat"  →  1...1..............1......    new key: group 0
"tea"  →  1...1..............1......    same key: group 0
"tan"  →  1............1.....1......    new key: group 1
"ate"  →  1...1..............1......    same key: group 0
"nat"  →  1............1.....1......    same key: group 1
"bat"  →  11.................1......    new key: group 2
result: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

```pseudo
FUNCTION LetterCounts(word)
    counts ← array of 26 zeros
    FOR EACH ch IN word
        slot ← ord(ch) - ord('a')          // 'a' → 0, 'b' → 1, ..., 'z' → 25
        counts[slot] ← counts[slot] + 1
    RETURN tuple(counts)                   // immutable, so it can be a map key

FUNCTION GroupAnagrams(words)
    groups ← empty map                     // count key → words with that key
    FOR EACH word IN words
        key ← LetterCounts(word)
        IF key NOT IN groups
            groups[key] ← empty list       // first word of a new group
        groups[key].append(word)
    RETURN groups.values()                 // one list per key, first-seen order
```

Each word costs `O(L)` to count plus a constant 26 to hash its key, so grouping `n` words takes `O(n · L)` time, and the groups take `O(n · L)` space. Reach for a canonical key whenever a problem says group, or treats two inputs as equal up to some rearrangement. The same count array decides Valid Anagram with one comparison and, slid along a string as a fixed-width window, finds every anagram of a pattern. The classic mistake is a key that throws information away: `set(word)` forgets multiplicity and merges `"aab"` with `"abb"`, and the sum of the character codes collides on `"ad"` and `"bc"`. A plain list as the key fails outright, because a list cannot be hashed.

*Practice:* LC 49 Group Anagrams · LC 242 Valid Anagram · LC 438 Find All Anagrams in a String

```{=latex}
\clearpage
```

## 4. Reverse a Linked List {#a4}

```{=latex}
\markright{4. Reverse a Linked List}
```

[Three Pointers: prev, curr, next · Two Pointers · Tier 1]{.meta}

Given the head of a singly linked list, reverse the list in place and return the new head. `1 → 2 → 3 → 4 → 5` becomes `5 → 4 → 3 → 2 → 1`, built from the same five nodes.

There is no index to swap by, and copying the values into a new list wastes `O(n)` space. The insight is that reversing a list means turning every `next` arrow around, and an arrow can be turned the moment we stand on its node, provided we first save where it pointed. So walk the list once with three pointers. `curr` is the node being processed, `prev` is the node it must now point back to, and `next_node` holds the rest of the list for the instant its link is cut. Every step saves, turns and advances: `next_node ← curr.next`, then `curr.next ← prev`, then `prev` and `curr` each move one node forward.

Picture two chains. `prev` heads the reversed part, `curr` heads the part still in its original order, and each step lifts the front node off the second chain and lays it on the front of the first, like moving plates from one stack to another. The invariant is that the two chains together hold every node, none lost and none repeated. When `curr` runs off the end, the first chain is the whole list reversed, and `prev` is its head.

```text
step   prev (reversed part)         curr (still to reverse)
start  null                         1 → 2 → 3 → 4 → 5 → null
1      1 → null                     2 → 3 → 4 → 5 → null
2      2 → 1 → null                 3 → 4 → 5 → null
3      3 → 2 → 1 → null             4 → 5 → null
4      4 → 3 → 2 → 1 → null         5 → null
5      5 → 4 → 3 → 2 → 1 → null     null            return prev
```

```pseudo
FUNCTION ReverseList(head)
    prev ← null                            // head of the reversed part
    curr ← head                            // head of the part still to reverse
    WHILE curr ≠ null
        next_node ← curr.next              // save the rest before the cut
        curr.next ← prev                   // turn this arrow around
        prev ← curr                        // the reversed part gains curr
        curr ← next_node                   // step into the saved rest
    RETURN prev                            // curr ran off the end
```

Each node is visited once and only three pointers are kept, so the reversal costs `O(n)` time and `O(1)` space. The recursive version reverses everything after the head first, then hooks the head behind its old neighbor with `head.next.next ← head` and `head.next ← null`; it is shorter but holds `O(n)` frames on the call stack, which overflows on a long enough list. Reach for this loop whenever a problem reverses a list or a stretch of one: between two positions, in groups of `k`, or the second half of a list to compare it with the first. The classic mistake is writing `curr.next ← prev` before saving `curr.next`, which cuts the rest of the list loose; the runner-up is returning `curr`, which is `null` at the end, instead of `prev`.

*Practice:* LC 206 Reverse Linked List · LC 92 Reverse Linked List II · LC 25 Reverse Nodes in k-Group · LC 234 Palindrome Linked List

```{=latex}
\clearpage
```

## 5. 3Sum {#a5}

```{=latex}
\markright{5. 3Sum}
```

[Sort, Fix One, Converge Two Pointers · Two Pointers · Tier 1]{.meta}

Given an array of integers, return every unique triplet of values that sums to zero; the same triplet must not appear twice, whichever positions it comes from. In `[-1, 0, 1, 2, -1, -4]` the answer is `[[-1, -1, 2], [-1, 0, 1]]`.

The brute force tries all `n(n - 1)(n - 2) / 6` triples of positions, `O(n^3)`, and still needs a set to strip repeated triplets. Sorting first changes the shape of the problem. Fix the first value `nums[i]`; what remains is a pair in the sorted suffix that sums to `-nums[i]`, which is Two Sum II, solved by two pointers converging from the ends of the suffix. If the sum is too small, only moving `left` rightward can raise it, because every value to the left of `right` pairs with `nums[left]` for a sum no larger. If it is too big, only moving `right` leftward can lower it. Each comparison retires one value for good, so one sweep is `O(n)` and the whole search is `O(n²)`.

Sorting also tames the duplicates, because equal values now sit side by side. An `i` whose value equals the one before it would rediscover the same triplets, so it is skipped; after a hit, `left` steps past every copy of the value just used. The early exit comes free: once `nums[i] > 0`, all three values are positive and nothing later can reach zero. Picture `i` pinned at the left end while `left` and `right` squeeze the rest of the line from both sides.

```text
index      0    1    2    3    4    5
sorted    -4   -1   -1    0    1    2
 i  nums[i]  left  right   sum   action
 0    -4       1     5     -3    too small: left + 1
 0    -4       2     5     -3    too small: left + 1
 0    -4       3     5     -2    too small: left + 1
 0    -4       4     5     -1    too small: left + 1, pointers meet
 1    -1       2     5      0    record [-1, -1, 2], move both
 1    -1       3     4      0    record [-1, 0, 1], move both, pointers cross
 2    -1                         same value as nums[1]: skip
 3     0       4     5      3    too big: right - 1, pointers meet
```

```pseudo
FUNCTION ThreeSum(nums)
    nums ← sorted(nums)                    // equal values now sit together
    triplets ← empty list
    n ← len(nums)
    FOR i FROM 0 TO n - 3
        IF nums[i] > 0
            BREAK                          // smallest of the three is positive
        IF i > 0 AND nums[i] = nums[i - 1]
            CONTINUE                       // same first value, same triplets
        left ← i + 1
        right ← n - 1
        WHILE left < right                 // Two Sum II on nums[i+1..n-1]
            total ← nums[i] + nums[left] + nums[right]
            IF total < 0
                left ← left + 1            // too small: a bigger second value
            ELSE IF total > 0
                right ← right - 1          // too big: a smaller third value
            ELSE
                triplets.append([nums[i], nums[left], nums[right]])
                left ← left + 1
                right ← right - 1
                WHILE left < right AND nums[left] = nums[left - 1]
                    left ← left + 1        // skip repeats of the second value
    RETURN triplets
```

The sort costs `O(n log n)` and is dominated by the `n` linear sweeps, so the total is `O(n²)` time, and the only extra memory besides the output is the sorted copy. Reach for sort, fix one, converge two whenever a problem asks for pairs, triplets or quadruplets with a target sum and wants values rather than indices: 3Sum Closest keeps the nearest total instead of exact hits, and 4Sum wraps one more fixed loop around the same sweep. The classic mistake is skipping duplicates by looking ahead, `nums[i] = nums[i + 1]`, instead of back. On the example it skips the first `-1` and loses `[-1, -1, 2]`, whose second `-1` was needed at `left`.

*Practice:* LC 15 3Sum · LC 167 Two Sum II - Input Array Is Sorted · LC 16 3Sum Closest · LC 18 4Sum

```{=latex}
\clearpage
```

## 6. Floyd's Tortoise and Hare {#a6}

```{=latex}
\markright{6. Floyd's Tortoise and Hare}
```

[Detect a Cycle and Find Its Entry · Cycle Detection · Tier 1]{.meta}

Given the head of a linked list whose last node may link back to an earlier node, decide whether there is a cycle and return the node where it begins, using `O(1)` extra space. In the list `1 → 2 → … → 7` whose tail links back to node `3`, the answer is node `3`.

The brute force keeps a hash set of visited nodes and returns the first node seen twice: `O(n)` time, but `O(n)` space. Floyd's idea replaces the memory with a difference in speed. A slow pointer moves one step at a time and a fast pointer two. Without a cycle, fast runs off the end. With one, both pointers end up circling the loop, and because fast gains exactly one node per step, the gap between them shrinks by one each step and closes on a meeting instead of jumping over it.

Finding the entry takes one more observation. Say the tail holds `a` nodes before the entry, the cycle holds `c`, and the pointers meet `b` steps past the entry. Fast has walked twice as far as slow and stands on the same node, so the extra distance, which equals slow's whole walk, is a whole number of laps. Slow's walk is `a` steps of tail plus `b` steps into the cycle, plus any full laps, so `a + b = k·c` for some whole `k`, that is `a = k·c - b`. Walking `a` steps from the meeting point therefore lands exactly on the entry, and so does walking `a` steps from the head. Restart one pointer at the head, step both by one, and they meet at the entry.

```text
1 → 2 → 3 → 4 → 5          tail: a = 2 nodes (1, 2), entry 3
        ↑       │          cycle: c = 5 nodes (3, 4, 5, 6, 7)
        │       ↓
        7 ←──── 6
phase 1   slow  fast        phase 2   from_head  from_meet
start      1     1          start         1          6
step 1     2     3          step 1        2          7
step 2     3     5          step 2        3          3    meet at the entry
step 3     4     7
step 4     5     4
step 5     6     6    meet at 6, b = 3 steps past the entry (3 → 4 → 5 → 6)
a + b = 2 + 3 = 5 = 1·c, so a = 1·5 - 3: two steps from 6 reach 3
```

```pseudo
FUNCTION MeetingPoint(head)
    slow ← head
    fast ← head
    WHILE fast ≠ null AND fast.next ≠ null
        slow ← slow.next
        fast ← fast.next.next
        IF slow = fast                     // the same node, not an equal value
            RETURN slow
    RETURN null                            // fast fell off the end: no cycle

FUNCTION CycleEntry(head)
    meet ← MeetingPoint(head)
    IF meet = null
        RETURN null
    from_head ← head
    from_meet ← meet
    WHILE from_head ≠ from_meet            // both are a steps from the entry
        from_head ← from_head.next
        from_meet ← from_meet.next
    RETURN from_head
```

Slow takes at most `n` steps before the meeting and the second phase takes `a` more, so the search is `O(n)` time with `O(1)` space. The same two pointers work on any sequence where each value determines the next, an implicit linked list. In Find the Duplicate Number, index `i` points to `nums[i]`; the duplicate is the only node with more than one arrow coming in, so it is the entry of the cycle. In Happy Number, each number points to the sum of the squares of its digits, and the number is happy exactly when the cycle its walk falls into is `1 → 1`. The classic mistake is testing `slow = fast` before the first move, where both sit on the head, or comparing values instead of nodes, which finds a cycle in `5 → 5 → 5`.

*Practice:* LC 141 Linked List Cycle · LC 142 Linked List Cycle II · LC 287 Find the Duplicate Number · LC 202 Happy Number

```{=latex}
\clearpage
```

## 7. Longest Substring Without Repeating Characters {#a7}

```{=latex}
\markright{7. Longest Substring Without Repeating Characters}
```

[Variable Window with Last-Seen Index · Sliding Window · Tier 1]{.meta}

Given a string, return the length of its longest substring in which no character appears twice. In `"abcbad"` the answer is `4`, the window `"cbad"`.

The brute force starts a scan at every index and extends it until a character repeats, `O(n²)` work. The insight is that neighboring answers overlap: when the window `s[left..right]` meets a repeat, the next valid window only has to drop the stretch up to the earlier copy, never start over. So keep one window and slide both of its edges forward. `right` advances one character per step; `left` moves only when the new character already sits inside the window, and then it jumps straight past the earlier copy, because no window that still holds both copies can be valid. A map from each character to the index of its latest occurrence makes that jump a single lookup.

Picture the window as an elastic band on the string: the right edge moves steadily, the left edge waits and then leaps. The one subtlety is a stale entry. The map still remembers characters that have already left the window, so the jump happens only when `last_seen[ch] ≥ left`; otherwise `left` would move backward and readmit a repeat. Below, the `a` at index 4 was last seen at index 0, already outside the window, so `left` stays at 2.

```text
          a b c b a d     last_seen[ch]          left  best
right 0   a               -                        0    1
right 1   a b             -                        0    2
right 2   a b c           -                        0    3
right 3       c b         1, inside: left = 2      2    3
right 4       c b a       0, left of window        2    3
right 5       c b a d     -                        2    4
```

```pseudo
FUNCTION LengthOfLongestSubstring(s)
    last_seen ← empty map                  // char → index of latest occurrence
    left ← 0
    best ← 0
    FOR right FROM 0 TO len(s) - 1
        ch ← s[right]
        IF ch IN last_seen AND last_seen[ch] ≥ left
            left ← last_seen[ch] + 1       // jump past the copy in the window
        last_seen[ch] ← right
        best ← max(best, right - left + 1)
    RETURN best
```

Each index enters the window once and `left` only moves forward, so the scan is `O(n)` time, and the map holds one entry per distinct character. Reach for a variable window whenever a problem asks for the longest contiguous stretch whose condition survives shrinking: no repeats, at most `k` distinct characters, at most `k` replacements. When the condition depends on counts rather than positions, keep a count map and advance `left` one step at a time instead of jumping, as Minimum Window Substring (#8) does. The classic mistake is dropping the `last_seen[ch] ≥ left` test: on `"abba"` the final `a` drags `left` back to index 1 and the answer comes out 3 instead of 2.

*Practice:* LC 3 Longest Substring Without Repeating Characters · LC 159 Longest Substring with At Most Two Distinct Characters · LC 340 Longest Substring with At Most K Distinct Characters · LC 424 Longest Repeating Character Replacement

```{=latex}
\clearpage
```

## 8. Minimum Window Substring {#a8}

```{=latex}
\markright{8. Minimum Window Substring}
```

[Expand Right, Shrink Left · Sliding Window · Tier 1]{.meta}

Given strings `s` and `t`, return the shortest substring of `s` that contains every character of `t`, repeats included, or `""` if there is none. For `s = "ADOBECODEBANC"` and `t = "ABC"` the answer is `"BANC"`.

The brute force tests every substring against the counts of `t`, `O(n²)` windows before any checking. The insight is that the windows worth testing form a chain. For each right end only the shortest covering window that ends there matters, and as the right end moves forward, the left end of that window never moves back. So one window slides with two edges: `right` expands until the window covers `t`, then `left` shrinks it for as long as it still covers `t`, recording each covering window on the way. The first character whose loss breaks the cover hands control back to `right`. Unlike the jumping left edge of #7, `left` here advances one step at a time, because coverage depends on counts rather than positions.

Re-checking the cover at every step would cost a loop over the characters of `t`, so the window keeps two pieces of bookkeeping. `need[ch]` is how many more copies of `ch` the window lacks, and it goes negative when the window holds spares. `missing` counts the characters of `t` still uncovered, repeats included, and drops only when an arriving character fills a real gap, that is, when its `need` was positive. The window covers `t` exactly when `missing = 0`, a constant-time test.

```text
                 A D O B E C O D E B A N C     t = "ABC"
right  5 covers  └─────────┘                 ADOBEC
        shrinks  └─────────┘                 ADOBEC  best ADOBEC
right 10 covers    └─────────────────┘       DOBECODEBA
        shrinks            └─────────┘       CODEBA  best ADOBEC
right 12 covers              └───────────┘   ODEBANC
        shrinks                    └─────┘   BANC    best BANC
```

```pseudo
FUNCTION CharCounts(text)
    counts ← empty map
    FOR EACH ch IN text
        counts[ch] ← counts.get(ch, 0) + 1
    RETURN counts

FUNCTION MinWindow(s, t)
    IF len(t) = 0
        RETURN ""                          // nothing to cover
    need ← CharCounts(t)                   // char → copies the window lacks
    missing ← len(t)                       // chars of t not yet covered
    left ← 0
    best_start ← 0
    best_len ← len(s) + 1                  // longer than any real window
    FOR right FROM 0 TO len(s) - 1
        ch ← s[right]
        IF need.get(ch, 0) > 0
            missing ← missing - 1          // this copy fills a real gap
        need[ch] ← need.get(ch, 0) - 1     // below zero: a spare copy
        WHILE missing = 0                  // covers t: record, then shrink
            IF right - left + 1 < best_len
                best_start ← left
                best_len ← right - left + 1
            drop ← s[left]
            need[drop] ← need[drop] + 1
            IF need[drop] > 0
                missing ← missing + 1      // dropped a copy the window needed
            left ← left + 1
    IF best_len > len(s)
        RETURN ""                          // no window ever covered t
    RETURN s[best_start..best_start + best_len - 1]
```

Each index enters the window once and leaves it at most once, so the work is `O(len(s) + len(t))` time, and the map holds one count per distinct character. Reach for expand-right, shrink-left whenever a problem asks for the shortest window that contains something; with the width pinned to `len(t)`, the same counts find every permutation or anagram of a pattern inside a string. The classic mistake is decrementing `missing` for every arriving character of `t`, spares included: with `s = "AAB"` and `t = "AB"`, the second `A` claims the slot meant for `B`, `missing` reaches 0 on `"AA"`, and the answer comes back without a `B`.

*Practice:* LC 76 Minimum Window Substring · LC 567 Permutation in String · LC 438 Find All Anagrams in a String · LC 30 Substring with Concatenation of All Words

```{=latex}
\clearpage
```

## 9. Binary Search {#a9}

```{=latex}
\markright{9. Binary Search}
```

[The Lower-Bound Template · Binary Search · Tier 1]{.meta}

Given an array sorted in non-decreasing order and a target, return the first index whose value is at least the target, or `len(nums)` if every value is smaller. In `[1, 3, 3, 5, 8, 9]` the answer for target `3` is `1`, the first of the two 3s; for target `4` it is `3`, the slot where 4 would be inserted; for target `10` it is `6`, one past the end.

A linear scan finds the answer in `O(n)` and ignores the order. Sorted order turns the question "is `nums[i] ≥ target`?" into a row of answers that reads ✗ ✗ ✗ then ✓ ✓ ✓, because once a value is big enough, every value to its right is too. The lower bound is the boundary between the two runs, and binary search finds a boundary by halving the unknown part. Keep a half-open window `[lo, hi)` with one invariant: every index left of `lo` is a ✗ and every index from `hi` on is a ✓, with the position `len(nums)` counting as a ✓. Probe the middle. A ✗ at `mid` condemns `mid` and everything left of it, so `lo ← mid + 1`. A ✓ at `mid` might be the first ✓, so it becomes the new right edge: `hi ← mid`. When `lo = hi` the window is empty and `lo` sits exactly on the boundary.

Every other search falls out of this template. Exact search checks whether the lower bound actually holds the target. The insert position is the lower bound itself. The upper bound, the first index whose value is greater than the target, is the same loop with `<` replaced by `≤`, so that equal values count as too small. The last occurrence sits just before the upper bound, so first and last position take two searches, and upper bound minus lower bound is the number of copies. First Bad Version is the template with the comparison replaced by a call to `isBadVersion(mid)`.

```text
index            0    1    2    3    4    5    6
nums             1    3    3    5    8    9
nums[i] ≥ 3?     ✗    ✓    ✓    ✓    ✓    ✓    (end counts as ✓)
                      ▲ lower bound = 1

   lo   hi   mid   nums[mid]   < 3?   move
    0    6     3       5        no    hi ← 3     mid is a ✓: keep it
    0    3     1       3        no    hi ← 1     mid is a ✓: keep it
    0    1     0       1        yes   lo ← 1     mid is a ✗: drop it
    1    1   window empty: return lo = 1
```

```pseudo
FUNCTION LowerBound(nums, target)        // first i with nums[i] ≥ target
    lo ← 0
    hi ← len(nums)                       // half-open [lo, hi)
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF nums[mid] < target
            lo ← mid + 1                 // mid and its left are too small
        ELSE
            hi ← mid                     // mid qualifies: keep it in play
    RETURN lo

FUNCTION UpperBound(nums, target)        // first i with nums[i] > target
    lo ← 0
    hi ← len(nums)
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF nums[mid] ≤ target            // equal values count as too small
            lo ← mid + 1
        ELSE
            hi ← mid
    RETURN lo

FUNCTION Search(nums, target)
    i ← LowerBound(nums, target)
    IF i < len(nums) AND nums[i] = target
        RETURN i
    RETURN -1

FUNCTION SearchRange(nums, target)
    first ← LowerBound(nums, target)
    IF first = len(nums) OR nums[first] ≠ target
        RETURN [-1, -1]
    RETURN [first, UpperBound(nums, target) - 1]
```

Each probe halves the window, so a search costs `O(log n)` time and `O(1)` space. Reach for it when the input is sorted and the question is "first", "last", "how many" or "where would it go", and more generally whenever a yes/no question about an index flips exactly once from no to yes, which is binary search on the answer (#10). Python's `bisect_left` and `bisect_right` compute exactly `lower_bound` and `upper_bound`; mention them, but write the loop by hand in an interview. The classic mistake is mixing conventions: `hi ← mid - 1` in this half-open template can jump past the answer, and `WHILE lo ≤ hi` with `hi ← mid` either spins forever once `lo = hi` or reads `nums[len(nums)]`.

*Practice:* LC 704 Binary Search · LC 35 Search Insert Position · LC 34 Find First and Last Position of Element in Sorted Array · LC 278 First Bad Version

```{=latex}
\clearpage
```

## 10. Binary Search on the Answer {#a10}

```{=latex}
\markright{10. Binary Search on the Answer}
```

[Search a Monotone Yes/No Predicate · Binary Search · Tier 1]{.meta}

Koko has piles of bananas and `h` hours. She picks one eating speed `k`; each hour she eats `k` bananas from a single pile, and when fewer than `k` are left in that pile she still spends the whole hour on it. Return the smallest `k` that finishes every pile within `h` hours; `h` is at least the number of piles, so some speed always works. For piles `[3, 6, 7, 11]` and `h = 8` the answer is `4`: at speed 4 the piles take `1 + 2 + 2 + 3 = 8` hours, while at speed 3 they take `1 + 2 + 3 + 4 = 10`.

Nothing here is sorted, yet binary search applies, because the search runs over the answer instead of over the array. Trying every speed from 1 upward costs `O(n · m)` for the largest pile `m`. The insight is that feasibility is monotone: if Koko finishes at speed `k`, she finishes at every faster speed, so the question "can she finish at speed `k`?" reads ✗ ✗ ✗ then ✓ ✓ ✓ along the number line of speeds. The answer is the first ✓, exactly the boundary that the lower-bound template of #9 finds. Only the probe changes: instead of comparing `nums[mid]` with a target, it simulates a whole meal at speed `mid` in one pass, summing `ceil(pile / mid)` hours.

Every problem of this kind has the same three parts. The range `[lo, hi]` holds every candidate answer, with `lo` the smallest conceivable value and `hi` a value that surely works; here they are `1` and `max(piles)`, since at that speed every pile takes one hour. The check `feasible(x)` is a simple simulation, usually `O(n)`, whose answer flips once from no to yes. The loop keeps a ✓ at `mid` with `hi ← mid`, drops a ✗ with `lo ← mid + 1`, and stops when `lo = hi`. "Largest value that still works" is the mirror image: search for the first value that fails and step back one.

```text
speed          1   2   3   4   5   6   7   8   9  10  11
hours         27  15  10   8   8   6   5   5   5   5   4
hours ≤ 8?     ✗   ✗   ✗   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓
                           ▲ the answer: the first ✓

   lo   hi   mid   hours at mid   ≤ 8?   move
    1   11     6         6         yes   hi ← 6
    1    6     3        10         no    lo ← 4
    4    6     5         8         yes   hi ← 5
    4    5     4         8         yes   hi ← 4
    4    4   lo = hi: the smallest speed is 4
```

```pseudo
FUNCTION CanFinish(piles, h, speed)      // the yes/no check
    hours ← 0
    FOR EACH pile IN piles
        hours ← hours + ceil(pile / speed)   // a partial hour costs a full one
    RETURN hours ≤ h

FUNCTION MinEatingSpeed(piles, h)
    lo ← 1                               // the slowest possible speed
    hi ← max(piles)                      // one pile per hour: always enough
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF CanFinish(piles, h, mid)
            hi ← mid                     // mid works; a slower speed might too
        ELSE
            lo ← mid + 1                 // mid fails, so does every slower one
    RETURN lo
```

The check runs once per halving of the speed range, so the cost is `O(n log m)` time and `O(1)` space. The signals are phrases such as "minimum capacity", "smallest speed", "minimize the largest" or "maximize the minimum", together with a check that is easy for any fixed answer and flips only once as the answer grows. The classic mistakes sit in the check and in the range: `pile // mid` rounds down and forgets the partial last hour, which makes slow speeds look feasible, and starting `lo` at `0` can divide by zero.

*Practice:* LC 875 Koko Eating Bananas · LC 1011 Capacity To Ship Packages Within D Days · LC 410 Split Array Largest Sum · LC 1482 Minimum Number of Days to Make m Bouquets

```{=latex}
\clearpage
```

## 11. Merge Sort {#a11}

```{=latex}
\markright{11. Merge Sort}
```

[Divide, Sort Halves, Merge · Sorting · Tier 1]{.meta}

Sort an array of integers into ascending order and return the result as a new list. `[5, 2, 4, 7, 1, 3, 2, 6]` becomes `[1, 2, 2, 3, 4, 5, 6, 7]`.

Insertion sort, the brute force, slides each value left past every larger one and costs `O(n²)` on reversed input. Merge sort starts from a cheaper fact: two lists that are already sorted combine into one sorted list in a single pass, because the smallest value not yet taken always sits at the front of one of them. So cut the array in half, sort each half by the same method, and merge the two sorted halves. The recursion bottoms out at lists of zero or one value, which are sorted by definition, and all the real work happens on the way back up, in the merges.

The merge is two fingers, one on the front of each half: compare the two fronts, take the smaller, advance that finger, and when one half runs out, copy the rest of the other. Taking the left front on a tie, `≤` rather than `<`, keeps equal values in their original order, which is what makes merge sort stable. Picture the recursion as a tree of cuts. Every row of the tree holds all n values, cut into more and more pieces, and after about `log2 n` rounds of cutting the pieces are single values. On the way back up each row is merged with `O(n)` work in total, because every value is copied once per row.

```text
split  [5 2 4 7 1 3 2 6]                          one list of 8
       [5 2 4 7]           [1 3 2 6]              2 lists of 4
       [5 2]     [4 7]     [1 3]     [2 6]        4 lists of 2
       [5] [2]   [4] [7]   [1] [3]   [2] [6]      8 lists of 1: sorted
merge  [2 5]     [4 7]     [1 3]     [2 6]        8 values copied
       [2 4 5 7]           [1 2 3 6]              8 values copied
       [1 2 2 3 4 5 6 7]                          8 values copied
```

```pseudo
FUNCTION Merge(left, right)
    merged ← empty list
    i ← 0                                  // front of left
    j ← 0                                  // front of right
    WHILE i < len(left) AND j < len(right)
        IF left[i] ≤ right[j]              // a tie takes the left one: stable
            merged.append(left[i])
            i ← i + 1
        ELSE
            merged.append(right[j])
            j ← j + 1
    WHILE i < len(left)                    // one side is used up: copy the rest
        merged.append(left[i])
        i ← i + 1
    WHILE j < len(right)
        merged.append(right[j])
        j ← j + 1
    RETURN merged

FUNCTION MergeSort(nums)
    IF len(nums) ≤ 1
        RETURN copy of nums                // 0 or 1 values: sorted already
    mid ← floor(len(nums) / 2)
    left ← MergeSort(nums[0..mid - 1])
    right ← MergeSort(nums[mid..len(nums) - 1])
    RETURN Merge(left, right)
```

There are `log2 n` levels of merging, rounded up, each costing `O(n)`, so the time is `O(n log n)` in every case, plus `O(n)` extra space for the merged lists. Reach for merge sort when the sort must be stable, when the data is a linked list (LC 148 splits at the middle with slow and fast pointers and needs no random access), and when a problem counts pairs `i < j` with `nums[i] > nums[j]`. That inversion count is the classic extension: when the merge takes `right[j]` while `len(left) - i` left values still wait, all of them are larger and came earlier in the array, so adding `len(left) - i` at that step counts every inversion; LC 315 and LC 493 are this count with a twist. The classic mistake is stopping when the main loop ends: `Merge([1, 4], [2, 3])` runs out of right values at `[1, 2, 3]` and loses the `4`.

*Practice:* LC 912 Sort an Array · LC 148 Sort List · LC 315 Count of Smaller Numbers After Self · LC 493 Reverse Pairs

```{=latex}
\clearpage
```

## 12. Quick Sort {#a12}

```{=latex}
\markright{12. Quick Sort}
```

[Partition Around a Random Pivot · Sorting · Tier 1]{.meta}

Sort an array of integers in place, rearranging it without a second array. `[6, 3, 7, 4, 1, 5, 2]` becomes `[1, 2, 3, 4, 5, 6, 7]`.

Merge sort (#11) does its work after the recursive calls, merging sorted halves into a new list. Quick sort does its work before them, in place. Partition the range around one value, the pivot: every smaller value moves to its left and every other value to its right. The pivot now sits in its final position, and the two sides are independent problems that never need to be combined. Sort each side the same way and the whole range is sorted.

The Lomuto partition is a single pass. Pick a random index, swap that value to the end and call it `pivot`. Then `i` scans the range from left to right while `store` marks where the next small value goes, under the invariant that `nums[lo..store-1]` holds only values less than the pivot. When `nums[i]` is smaller, swap it into `nums[store]` and advance `store`. At the end one swap moves the pivot to `store`, right between the two regions. Picture a wall that slides to the right: everything left of the wall is smaller than the pivot, everything between the wall and `i` is not.

```text
random pick: index 3, pivot 4, parked at the end: 6 3 7 2 1 5 4
  i   nums[i]   < 4?   nums after the step (│ = store)   store
  0      6       no    │6 3 7 2 1 5 4                      0
  1      3       yes    3│6 7 2 1 5 4                      1
  2      7       no     3│6 7 2 1 5 4                      1
  3      2       yes    3 2│7 6 1 5 4                      2
  4      1       yes    3 2 1│6 7 5 4                      3
  5      5       no     3 2 1│6 7 5 4                      3
pivot swapped to store: 3 2 1 4 7 5 6, so p = 3
then sort 3 2 1 and 7 5 6; the 4 never moves again
```

```pseudo
FUNCTION Partition(nums, lo, hi)
    pick ← RandomInt(lo, hi)            // lo ≤ pick ≤ hi
    swap(nums[pick], nums[hi])          // park the pivot at the end
    pivot ← nums[hi]
    store ← lo                          // invariant: nums[lo..store-1] < pivot
    FOR i FROM lo TO hi - 1
        IF nums[i] < pivot              // a small value joins the left region
            swap(nums[store], nums[i])
            store ← store + 1
    swap(nums[store], nums[hi])         // pivot between the regions
    RETURN store

FUNCTION SortRange(nums, lo, hi)
    IF lo ≥ hi                          // 0 or 1 values: sorted already
        RETURN
    p ← Partition(nums, lo, hi)
    SortRange(nums, lo, p - 1)          // the pivot at p is final: skip it
    SortRange(nums, p + 1, hi)

FUNCTION QuickSort(nums)
    SortRange(nums, 0, len(nums) - 1)
    RETURN nums
```

A balanced split gives `log2 n` levels of `O(n)` partitioning, so `O(n log n)` time. A pivot that is always the smallest or largest value peels off one element per level and costs `O(n²)`; with a fixed last-element pivot, an already sorted array does exactly that. A random pivot makes no input order bad: on distinct values the expected time is `O(n log n)` and the expected stack depth `O(log n)`. Quick sort is not stable, because a long swap can carry a value past an equal one. Hoare's original partition moves two indices inward from both ends and swaps each misplaced pair; it makes fewer swaps and splits a run of equal values down the middle. Reach for quick sort when the sort must be in place and fast on average, and for its partition alone in kth largest (#42). The classic mistake is ignoring duplicates, and this two-way partition makes it: with the `<` test, an array of equal values leaves the left side empty at every level, so even a random pivot goes quadratic and the recursion runs n levels deep; the three-way partition of #38 fixes it.

*Practice:* LC 912 Sort an Array · LC 215 Kth Largest Element in an Array · LC 75 Sort Colors

```{=latex}
\clearpage
```

## 13. Top-K Elements {#a13}

```{=latex}
\markright{13. Top-K Elements}
```

[Keep a Size-K Min-Heap · Heaps · Tier 1]{.meta}

Given an unsorted array and an integer `k`, return the kth largest value, where duplicates count as separate values; the same method returns the k largest values themselves. In `[3, 1, 5, 12, 2, 11]` with `k = 3` the three largest are `12`, `11` and `5`, so the answer is `5`.

Sorting answers it in `O(n log n)` but orders all n values when only k of them matter. Keep instead a min-heap of the k largest values seen so far. Push each value; when the heap grows to `k + 1` values, pop its smallest. The popped value can never be among the k largest, because the k values still in the heap are all at least as large. After the last value the heap holds exactly the k largest, and its top, the smallest of them, is the kth largest.

A min-heap for a question about the largest feels backwards, and that is the point. The top of the heap is the weakest member of the current top k, the gatekeeper at the door: a newcomer that cannot beat it is popped right back out, and one that can beat it pushes the gatekeeper out instead. The heap never holds more than `k + 1` values, so each push and pop costs `O(log k)`, not `O(log n)`.

```text
k = 3; heap contents listed smallest first, so the top comes first
  value   after the push   size > 3?   popped   heap kept
    3     3                no                   3
    1     1 3              no                   1 3
    5     1 3 5            no                   1 3 5
   12     1 3 5 12         yes           1      3 5 12
    2     2 3 5 12         yes           2      3 5 12
   11     3 5 11 12        yes           3      5 11 12
heap top 5 is the 3rd largest; the heap holds the top three
```

```pseudo
FUNCTION TopK(nums, k)
    heap ← empty min-heap
    FOR EACH value IN nums
        heap.push(value)
        IF len(heap) > k                   // one too many: drop the smallest
            heap.pop()
    RETURN heap

FUNCTION KthLargest(nums, k)
    heap ← TopK(nums, k)
    RETURN heap.top()                      // the smallest of the k largest
```

Each of the n values costs one push and at most one pop on a heap of at most `k + 1` values, so the time is `O(n log k)` and the space `O(k)`. That beats sorting when k is small, and it works on an endless stream: LC 703 keeps this heap alive and answers after every new value. Signals: k largest, k most frequent, k closest. K Closest Points to Origin is the same loop with a distance key in the opposite direction: keeping the k smallest distances needs a max-heap, which `heapq` gives when you push `(-(x² + y²), x, y)`, so the popped point is the farthest so far. Top K Frequent Elements counts first and runs the loop on `(count, value)` pairs, or uses the buckets of #43. Quickselect (#42) is expected `O(n)` but reorders the array and needs all of it at once. The classic mistake is reaching for a max-heap because the problem says largest: a size-k max-heap evicts the biggest values, exactly the ones to keep.

*Practice:* LC 215 Kth Largest Element in an Array · LC 703 Kth Largest Element in a Stream · LC 347 Top K Frequent Elements · LC 973 K Closest Points to Origin

```{=latex}
\clearpage
```

## 14. Merge K Sorted Arrays {#a14}

```{=latex}
\markright{14. Merge K Sorted Arrays}
```

[A Heap of the Front Elements · Heaps · Tier 1]{.meta}

Given k arrays, each sorted in ascending order, merge them into one sorted array. `[[1, 4, 7], [2, 5], [0, 3, 6]]` becomes `[0, 1, 2, 3, 4, 5, 6, 7]`.

Concatenating and sorting costs `O(N log N)` for N values in total and throws away the order the arrays already have. Merging the arrays one at a time into a growing result recopies that result k times, `O(Nk)`. The insight is that the next value of the output is always the smallest of the k fronts, one front per array, and a min-heap is the structure that hands back the smallest of a changing set. Put each array's first value in the heap; then pop the smallest front, append it to the output, and push the next value of the same array in its place.

Picture the arrays as k rows with a finger on the front of each. The heap holds what the fingers point at, never more than k values. Each pop moves exactly one finger one step to the right, and a row whose finger falls off the end simply stops taking part. A heap entry is the tuple `(value, row, col)`: the value orders the heap, and `row` and `col` say where the successor lives, at `arrays[row][col + 1]`.

```text
rows: 0 → [1 4 7]   1 → [2 5]   2 → [0 3 6]; the heap starts with 0 1 2
  pop (value, row, col)   then push      heap after   merged
  (0, 2, 0)               (3, 2, 1)      1 2 3        0
  (1, 0, 0)               (4, 0, 1)      2 3 4        0 1
  (2, 1, 0)               (5, 1, 1)      3 4 5        0 1 2
  (3, 2, 1)               (6, 2, 2)      4 5 6        0 1 2 3
  (4, 0, 1)               (7, 0, 2)      5 6 7        0 1 2 3 4
  (5, 1, 1)               row 1 done     6 7          0 1 2 3 4 5
  (6, 2, 2)               row 2 done     7            0 1 2 3 4 5 6
  (7, 0, 2)               row 0 done     empty        0 1 2 3 4 5 6 7
```

```pseudo
FUNCTION MergeKSorted(arrays)
    heap ← empty min-heap                  // of (value, row, col)
    FOR row FROM 0 TO len(arrays) - 1
        IF len(arrays[row]) > 0            // an empty array has no front
            heap.push((arrays[row][0], row, 0))
    merged ← empty list
    WHILE len(heap) > 0
        (value, row, col) ← heap.pop()     // the smallest front of all
        merged.append(value)
        IF col + 1 < len(arrays[row])      // that row has a next value
            heap.push((arrays[row][col + 1], row, col + 1))
    RETURN merged
```

Every value enters and leaves the heap once, and the heap never holds more than k entries, so the time is `O(N log k)` and the extra space `O(k)` beyond the output. Merging the arrays in pairs, level by level as in merge sort (#11), reaches the same `O(N log k)` without a heap. Signals: several sorted sources, k sorted lists, the kth smallest across sorted rows, or a range that must touch every list. LC 23 is this loop on linked lists: push `(node.val, i, node)` for the head of list `i`, and after a pop push `node.next` if it exists. A sorted matrix (LC 378) is a stack of sorted rows: seed the heap with every row's first value, pop k times, and the kth pop is the kth smallest. The classic mistake in Python is pushing `(node.val, node)`: when two values tie, the heap compares the nodes themselves and raises a `TypeError`, so put the list index in the middle as a tie-breaker.

*Practice:* LC 23 Merge k Sorted Lists · LC 378 Kth Smallest Element in a Sorted Matrix · LC 632 Smallest Range Covering Elements from K Lists · LC 373 Find K Pairs with Smallest Sums

```{=latex}
\clearpage
```

## 15. Find Median from Data Stream {#a15}

```{=latex}
\markright{15. Find Median from Data Stream}
```

[Two Heaps Meet in the Middle · Design · Tier 1]{.meta}

Numbers arrive one at a time, and after any arrival we must report the median of everything seen so far: the middle value when the count is odd, the mean of the two middle values when it is even. The stream 5, 15, 1, 3 has medians 5, 10, 5 and 4 after each arrival.

The brute force keeps a sorted list and inserts each number in its place, which costs `O(n)` per arrival because the tail has to shift. But the median never needs the full order. It needs only the cut through the middle of the sorted stream and the one or two values touching that cut. So keep the smaller half in a max-heap `low`, whose top is its largest value, and the larger half in a min-heap `high`, whose top is its smallest. The two heaps are the two halves of the sorted stream, and their tops face each other across the cut. Two invariants hold after every call: every value in `low` is at most every value in `high`, and `low` holds as many values as `high` or exactly one more. With an odd count the median is the top of `low`; with an even count it is the mean of the two tops.

Adding a number keeps both invariants without ever asking which half it belongs to. Push it into `low`, pop the largest value of `low` and push that into `high`. The value that crosses is the largest of the old smaller half and the newcomer, so the order between the halves survives. The crossing makes `high` one bigger; if it is now larger than `low`, its smallest value walks back, which is safe for the same reason in mirror image.

```text
stream 5, 15, 1, 3              low = max-heap ]│[ high = min-heap

add   low → high   high → low      low ]│[ high          median
  5        5            5            5 ]│[                    5
 15       15            -            5 ]│[ 15               10.0
  1        5            5          1 5 ]│[ 15                  5
  3        5            -          1 3 ]│[ 5 15              4.0

the values touching the wall are the two heap tops
```

```pseudo
CLASS MedianFinder
    FUNCTION Init()
        self.low ← empty max-heap          // the smaller half
        self.high ← empty min-heap         // the larger half

    FUNCTION AddNum(num)
        self.low.push(num)
        top_low ← self.low.pop()           // the largest of low and num
        self.high.push(top_low)
        IF len(self.high) > len(self.low)  // low may lead by one, not trail
            top_high ← self.high.pop()
            self.low.push(top_high)

    FUNCTION FindMedian()
        IF len(self.low) > len(self.high)
            RETURN self.low.top()          // odd count: low holds the middle
        RETURN (self.low.top() + self.high.top()) / 2
```

Each `AddNum` makes at most three pushes and two pops, so it costs `O(log n)`; `FindMedian` reads two tops in `O(1)`, and the heaps hold all `n` values. Reach for two heaps when a problem asks for the median or any middle rank of a collection that keeps changing, or when items move from a waiting pool into a chosen pool ranked the opposite way, as in IPO with a min-heap of capital and a max-heap of profit. The sliding-window median adds removals, handled lazily: count the values that have left the window and discard them only when they surface at a top. The classic mistake lives in Python, where `heapq` builds only min-heaps: `low` stores negated values, so a number goes in as `-num` and comes out with a second minus, and dropping either sign silently mixes the halves. A close second is `//` in the even case, which turns the median 1.5 of `[1, 2]` into 1.

*Practice:* LC 295 Find Median from Data Stream · LC 480 Sliding Window Median · LC 502 IPO

```{=latex}
\clearpage
```

## 16. Valid Parentheses {#a16}

```{=latex}
\markright{16. Valid Parentheses}
```

[The Matching Stack · Stacks · Tier 1]{.meta}

Given a string made of the brackets `()[]{}`, decide whether it is valid: every opener is closed by a bracket of the same kind, and the bracket opened most recently closes first. `"([]{})"` is valid; `"([)]"` is not, even though each kind is opened once and closed once.

The brute force deletes adjacent matched pairs such as `()` until nothing changes and checks that the string vanished, which costs `O(n²)` when the nesting is deep. The better view is geometric. Draw an arc from every opener to the closer that ends it. A valid string is a set of arcs that nest like boxes inside boxes, never crossing, each joining two brackets of the same kind. Nesting means that a closer always ends the innermost arc still open, the one opened most recently, and "most recent first" is exactly a stack.

So walk the string once. Push every opener. When a closer arrives, the top of the stack must be its partner; popping it closes that arc. A closer that meets an empty stack has no arc to close, and a closer that meets the wrong kind on top would cross an arc that is still open, so either way the answer is `false` on the spot. At the end the stack must be empty, because any opener left on it is an arc that never closed.

```text
 ( [ ] { } )       ch   action                stack after
 │ └─┘ └─┘ │       (    push                  (
 └─────────┘       [    push                  ( [
 arcs nest ✓       ]    top [ matches, pop    (
                   {    push                  ( {
                   }    top { matches, pop    (
                   )    top ( matches, pop    empty  → true

 ( [ ) ]           (    push                  (
 │ └─┼─┘           [    push                  ( [
 └───┘             )    top is [, needs (     → false
 arcs cross ✗
```

```pseudo
FUNCTION IsValid(s)
    partner ← map {')' → '(', ']' → '[', '}' → '{'}  // closer → its opener
    stack ← empty stack                         // openers still waiting
    FOR EACH ch IN s
        IF ch IN partner
            IF len(stack) = 0 OR stack.top() ≠ partner[ch]
                RETURN false                    // nothing open, or wrong kind
            stack.pop()                         // the innermost opener closes
        ELSE
            stack.push(ch)
    RETURN len(stack) = 0                       // leftovers never closed
```

Each character is pushed or popped at most once, so the scan takes `O(n)` time, and the stack can hold all `n` openers, `O(n)` space. Reach for the matching stack whenever things must close in the reverse order of opening: brackets, HTML tags, nested function calls, an encoded string such as `3[a2[c]]`, the groups of an arithmetic expression (#45). With a single bracket kind the stack shrinks to a counter of open brackets, and Minimum Add to Make Parentheses Valid just adds the closers that find the counter at zero to the openers left at the end. Minimum Remove to Make Valid Parentheses pushes indices instead of characters, so it knows exactly which unmatched brackets to delete, and Longest Valid Parentheses also keeps indices, measuring each valid run from the last unmatched index left on the stack. The classic mistakes are returning `true` without checking that the stack is empty, which accepts `"(("`, and reading the top of an empty stack on a leading closer as in `")("`, which crashes instead of returning `false`. Keeping one counter per kind is the third: the counts of `"([)]"` balance perfectly and the crossing goes unseen.

*Practice:* LC 20 Valid Parentheses · LC 921 Minimum Add to Make Parentheses Valid · LC 1249 Minimum Remove to Make Valid Parentheses · LC 32 Longest Valid Parentheses

```{=latex}
\clearpage
```

## 17. Monotonic Stack {#a17}

```{=latex}
\markright{17. Monotonic Stack}
```

[Next Greater Element · Stacks · Tier 1]{.meta}

Given daily temperatures, return for each day how many days you must wait for a strictly warmer one, or 0 if none comes. For `[73, 74, 75, 71, 69, 72, 76, 73]` the answer is `[1, 1, 4, 2, 1, 1, 0, 0]`: the 75 on day 2 waits four days for the 76.

The brute force scans right from every day until something warmer appears, `O(n²)` on a falling sequence. Its waste is that a cold day gets rescanned by every earlier day still waiting behind it. Turn the question around: instead of each day searching forward, let each new day answer everyone it beats. The days still waiting form a staircase that never rises from left to right, because a warmer later day would already have answered the earlier one. Keep that staircase on a stack of indices. A new day knocks down every step colder than itself, starting at the top, and each fallen day `j` learns its answer, `i - j`. The first step that is not colder stops the pops, and the new day becomes the top step, waiting for its own answer.

The stack holds indices, not temperatures, because the answer is a distance and a temperature is one lookup away. Only a strictly warmer day pops, so equal temperatures sit side by side and keep waiting together.

```text
 i  temp   pops: answer[j] = i - j          stack after (index:temp)
 0   73    -                                0:73
 1   74    answer[0] = 1                    1:74
 2   75    answer[1] = 1                    2:75
 3   71    -                                2:75  3:71
 4   69    -                                2:75  3:71  4:69
 5   72    answer[4] = 1, answer[3] = 2     2:75  5:72
 6   76    answer[5] = 1, answer[2] = 4     6:76
 7   73    -                                6:76  7:73
 end: days 6 and 7 never pop and keep 0 → [1, 1, 4, 2, 1, 1, 0, 0]
```

```pseudo
FUNCTION DailyTemperatures(temperatures)
    n ← len(temperatures)
    answer ← array of n zeros           // 0 stays for days nothing beats
    stack ← empty stack                 // waiting indices, temps never rising
    FOR i FROM 0 TO n - 1
        WHILE len(stack) > 0 AND temperatures[stack.top()] < temperatures[i]
            j ← stack.pop()             // day i is the first warmer day after j
            answer[j] ← i - j
        stack.push(i)                   // day i waits for its own answer
    RETURN answer
```

Every index is pushed once and popped at most once, so the nested loops do `O(n)` work in total, plus `O(n)` space for the stack. Reach for a monotonic stack whenever each element needs its nearest greater or smaller neighbor on one side: the next warmer day, the next greater element, a stock span, the walls of the largest rectangle in a histogram (#44). The variants change only the comparison and the direction. For the previous smaller element, keep values rising on the stack, pop everything greater than or equal to the new value, and the top that remains is the answer. For a circular array, walk the indices twice with `i mod n`, so elements near the end find their answer near the front. Online Stock Span is the previous-greater variant run as a stream, where each popped day's span is added to the new one. The classic mistakes are pushing temperatures instead of indices, which loses the distance, and popping on `≤` instead of `<`, which answers a day with an equal one that is not warmer and turns `[70, 70, 71]` into `[1, 1, 0]` instead of `[2, 1, 0]`.

*Practice:* LC 739 Daily Temperatures · LC 496 Next Greater Element I · LC 503 Next Greater Element II · LC 901 Online Stock Span

```{=latex}
\clearpage
```

## 18. Merge Intervals {#a18}

```{=latex}
\markright{18. Merge Intervals}
```

[Sort by Start, Sweep and Extend · Intervals · Tier 1]{.meta}

Given closed intervals `[start, end]` in any order, merge every group that overlaps or touches and return the result sorted by start. `[[1, 3], [8, 12], [2, 6], [9, 10], [12, 14]]` becomes `[[1, 6], [8, 14]]`: `[2, 6]` overlaps `[1, 3]`, `[9, 10]` lies inside `[8, 12]`, and `[12, 14]` touches it at 12.

The brute force compares every pair and merges any two that overlap, repeating until nothing changes, which is at least `O(n²)`. Sorting by start removes all of that searching. Lay the sorted intervals on a number line and sweep from left to right. Each interval starts at or after every interval before it, so the only one it can reach is the merged interval being built at the right end of the output, `merged[-1]`. One comparison settles it. If the new start is at most the last merged end, the two share a point and the last interval stretches to cover the new one. Otherwise there is a gap on the line, and no later interval can bridge it, because every later interval starts no earlier than the new one. The last merged interval is final, and a new one begins.

The stretch takes the larger of the two ends, not the new end, because a short interval can sit entirely inside the current one, as `[9, 10]` sits inside `[8, 12]`. The test is `≤` rather than `<` because closed intervals that touch share a point, so `[8, 12]` and `[12, 14]` become one.

```text
           0   2   4   6   8   10  12  14
[1, 3]       ├───┤
[2, 6]         ├───────┤
[8, 12]                    ├───────┤
[9, 10]                      ├─┤
[12, 14]                           ├───┤
merged       ├─────────┤   ├───────────┤

sorted     start ≤ last merged end?            merged after
[1, 3]     merged is empty → append            [1, 3]
[2, 6]     2 ≤ 3 → end ← max(3, 6) = 6         [1, 6]
[8, 12]    8 > 6 → append                      [1, 6] [8, 12]
[9, 10]    9 ≤ 12 → end ← max(12, 10) = 12     [1, 6] [8, 12]
[12, 14]   12 ≤ 12 → end ← max(12, 14) = 14    [1, 6] [8, 14]
```

```pseudo
FUNCTION MergeIntervals(intervals)
    merged ← empty list                     // merged[-1] is its last interval
    FOR EACH [start, end] IN sorted(intervals)          // by start
        IF len(merged) > 0 AND start ≤ merged[-1][1]
            merged[-1][1] ← max(merged[-1][1], end)     // overlap: stretch it
        ELSE
            merged.append([start, end])                 // a gap: a new interval
    RETURN merged
```

The sort costs `O(n log n)` and the sweep `O(n)`, with `O(n)` space for the output. Reach for sort-then-sweep whenever a problem hands you ranges, bookings or segments and asks for their union, their overlaps or the gaps between them. When the list is already sorted and disjoint, as in Insert Interval, skip the sort: copy the intervals that end before the new one starts, absorb every interval that overlaps it by taking the smaller start and the larger end, then copy the rest, all in `O(n)`. Interval List Intersections walks two sorted lists with two pointers instead, and Meeting Rooms needs only the comparison: after sorting, any start before the previous end is a conflict. The classic mistake is stretching to `end` instead of `max(merged[-1][1], end)`: on the example, `[9, 10]` shrinks `[8, 12]` to `[8, 10]`, and `[12, 14]` is wrongly left on its own.

*Practice:* LC 56 Merge Intervals · LC 57 Insert Interval · LC 986 Interval List Intersections · LC 252 Meeting Rooms

```{=latex}
\clearpage
```

## 19. Meeting Rooms II {#a19}

```{=latex}
\markright{19. Meeting Rooms II}
```

[Minimum Rooms with a Heap of End Times · Intervals · Tier 1]{.meta}

Given meetings as half-open intervals `[start, end)`, return the fewest rooms that can host them all; a meeting may start the moment another one ends. For `[[0, 30], [5, 10], [10, 20], [15, 25]]` the answer is 3: at time 15 the meetings `[0, 30)`, `[10, 20)` and `[15, 25)` are all running, while `[10, 20)` can take over the room that `[5, 10)` frees at 10.

The brute force stands at every meeting's start, counts the meetings in progress and keeps the maximum, `O(n²)`. That peak overlap is the answer, and a heap finds it in `O(n log n)`. Take the meetings in order of start and keep one entry per room in a min-heap: the time that room becomes free. Only the top matters, the room that frees up first. If it is free by the new meeting's start, the meeting takes it over: pop the old end, push the new one. If even that room is busy, every room is busy, and the meeting opens a new room with a push alone. The heap never shrinks, so its final size is the number of rooms, and none of them is wasted: a room opens only when every existing room holds a meeting that began no later and ends after `start`, so all of them overlap the newcomer at that instant.

The same number falls out of a sweep line. Turn each meeting into two events, `+1` at its start and `-1` at its end, sort them by time and run a counter across them; the counter's peak is the answer. At equal times the ends must come first, since a meeting that ends at 10 hands its room to one that starts at 10, and sorting `(time, delta)` pairs does that because `-1` sorts before `+1`.

```text
time     0    5    10   15   20   25   30
room 1   ├─────────────────────────────┤      [0, 30)
room 2        ├────┼─────────┤                [5, 10) then [10, 20)
room 3                  ├─────────┤           [15, 25)

meeting    earliest end ≤ start?        end times in the heap
[0, 30)    heap empty → new room 1      [30]
[5, 10)    30 > 5 → new room 2          [10, 30]
[10, 20)   10 ≤ 10 → reuse room 2       [20, 30]
[15, 25)   20 > 15 → new room 3         [20, 25, 30]
rooms = size of the heap = 3
```

```pseudo
FUNCTION MinMeetingRooms(intervals)
    ends ← empty min-heap                   // one end time per room
    FOR EACH [start, end] IN sorted(intervals)  // earliest start first
        IF len(ends) > 0 AND ends.top() ≤ start
            ends.pop()                      // the room that frees first is free
        ends.push(end)                      // this room is busy until end
    RETURN len(ends)
```

Sorting costs `O(n log n)` and each meeting makes at most one pop and one push, so the run is `O(n log n)` time and `O(n)` space. Reach for it whenever a problem asks how many things run at once: rooms, platforms, servers, bookings. Car Pooling is the sweep with passenger counts in place of `+1`; Divide Intervals Into Minimum Number of Groups is this problem with closed intervals, so a group frees up only when its end is strictly less than the new start; My Calendar III keeps the sweep in a sorted map. The classic mistake is testing `<` instead of `≤`, which treats `[1, 5)` and `[5, 10)` as a clash and answers 2 instead of 1. Another is popping every finished meeting in a loop and returning the final heap size, which has shrunk by then: `[[1, 10], [2, 3], [11, 12]]` answers 1 instead of 2.

*Practice:* LC 253 Meeting Rooms II · LC 1094 Car Pooling · LC 2406 Divide Intervals Into Minimum Number of Groups · LC 732 My Calendar III

```{=latex}
\clearpage
```

## 20. Kadane's Algorithm {#a20}

```{=latex}
\markright{20. Kadane's Algorithm}
```

[Maximum Subarray: Extend or Restart · Greedy · Tier 1]{.meta}

Given a non-empty array of integers, find the contiguous subarray with the largest sum and report that sum with the subarray's first and last index. In `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` the answer is `6`, from `[4, -1, 2, 1]` at indices `3` to `6`.

The brute force tries every subarray, and even with a running total per start that is `O(n²)` work. Kadane's insight is to ask a smaller question at each index: what is the best sum of a subarray that ends exactly here? That subarray either extends the best one ending one step earlier or starts fresh at the current number, so `ending_here = max(x, ending_here + x)`. Extending loses exactly when the run behind is negative, because a negative prefix can only drag `x` down, so the choice is a sign test: restart when `ending_here < 0`, extend otherwise. The answer is the best `ending_here` seen anywhere, and one pass carries just two numbers, the run that ends at the pointer and the best run so far.

Picture the prefix sums as a mountain profile, point `k` standing at the sum of the first `k` numbers; the sum of `nums[i..j]` is then the climb from point `i` to point `j + 1`. The run turns negative exactly when the profile dips to a new low, so every restart moves the base camp to the lowest point so far, and the best subarray is the biggest climb from a low to a later peak: the stock problem of #21 run on prefix sums, except that a trade is compulsory, because the subarray cannot be empty. The bounds come almost free. `start` jumps to `i` on every restart, and whenever `best` improves, the current `start` and `i` are copied into `best_start` and `best_end`.

```text
  i    x    extend or restart    ending_here   start   best   best bounds
  0   -2    first element             -2          0      -2      [0, 0]
  1    1    restart: -2 < 0            1          1       1      [1, 1]
  2   -3    extend                    -2          1       1      [1, 1]
  3    4    restart: -2 < 0            4          3       4      [3, 3]
  4   -1    extend                     3          3       4      [3, 3]
  5    2    extend                     5          3       5      [3, 5]
  6    1    extend                     6          3       6      [3, 6]
  7   -5    extend                     1          3       6      [3, 6]
  8    4    extend                     5          3       6      [3, 6]

  prefix sums   0  -2  -1  -4   0  -1   1   2  -3   1
                            ▲ new low       ▲ peak: 2 - (-4) = 6
```

```pseudo
FUNCTION MaxSubarray(nums)
    ending_here ← nums[0]                  // best sum of a subarray ending at i
    start ← 0                              // where that subarray begins
    best ← nums[0]                         // not 0: all may be negative
    best_start ← 0
    best_end ← 0
    FOR i FROM 1 TO len(nums) - 1
        IF ending_here < 0                 // a negative run only drags x down
            ending_here ← nums[i]          // restart at x
            start ← i
        ELSE
            ending_here ← ending_here + nums[i]        // extend the run
        IF ending_here > best              // improved: copy the bounds
            best ← ending_here
            best_start ← start
            best_end ← i
    RETURN (best, best_start, best_end)
```

One pass with constant work per element gives `O(n)` time and `O(1)` space. Reach for Kadane when a problem asks for the best contiguous stretch, a largest sum or gain over consecutive elements, and the best stretch ending at `i` can be built from the best one ending at `i - 1`. The variants change what is carried. A circular array (LC 918) takes the larger of the plain answer and the total minus the minimum subarray sum, unless every number is negative; a product (LC 152) carries both the largest and the smallest product ending here, because a negative factor swaps them; the largest absolute sum (LC 1749) is the larger of the maximum sum and the negated minimum sum. The classic mistake is starting `best` at `0`, which answers `0` for `[-3, -1, -2]` instead of `-1`: the empty subarray is not a choice.

*Practice:* LC 53 Maximum Subarray · LC 918 Maximum Sum Circular Subarray · LC 152 Maximum Product Subarray · LC 1749 Maximum Absolute Sum of Any Subarray

```{=latex}
\clearpage
```

## 21. Best Time to Buy and Sell Stock {#a21}

```{=latex}
\markright{21. Best Time to Buy and Sell Stock}
```

[Track the Running Minimum · Greedy · Tier 1]{.meta}

Given a stock's price on each day, buy on one day and sell on a later day so that the profit is as large as possible, or return `0` when no trade makes money. For `[7, 1, 5, 3, 6, 4]` the answer is `5`: buy at `1` on day 1 and sell at `6` on day 4.

The brute force pairs every buy day with every later sell day, `O(n²)` pairs. Yet a sale on a given day does not care about all the earlier days, only about the cheapest of them: the best trade that sells today bought at the minimum price so far. So walk the days once, carry that running minimum, and price each day as a sale against it; the answer is the largest of those daily profits. The running minimum is the whole memory of the past. It is updated before today's sale, which at worst prices a same-day trade at `0`, the same as not trading.

Picture the price chart as a mountain range. A trade is a climb from one point to a later, higher point, and the answer is the tallest such climb. The running minimum is a floor that only ever drops, sitting at the lowest valley behind the walker, and each day's profit is the height of that day's point above the floor. A new low never hurts, because it lowers the floor for every later day. When transactions are unlimited (LC 122), the answer is instead the sum of every positive day-to-day rise: a long climb earns exactly the sum of its steps, and every step up can be taken on its own.

```text
price
  7      ●
  6                              ●   best sale: 6 - 1 = 5
  5                  ●           │
  4                  │           │     ●
  3                  │     ●     │     │
  2                  │     │     │     │
  1            ●─────┴─────┴─────┴─────┴   floor = running minimum
         d0    d1    d2    d3    d4    d5
  min    7     1     1     1     1     1
  profit 0     0     4     2     5     3
  best   0     0     4     4     5     5
```

```pseudo
FUNCTION MaxProfit(prices)
    min_price ← ∞                          // cheapest price so far
    best ← 0                               // no trade at all earns 0
    FOR EACH price IN prices
        IF price < min_price               // a cheaper day to have bought on
            min_price ← price
        profit ← price - min_price         // sell today, bought at the minimum
        IF profit > best
            best ← profit
    RETURN best
```

One pass with constant work per day gives `O(n)` time and `O(1)` space. Reach for the running minimum whenever a problem asks for the best `a[j] - a[i]` with `i < j`: the best partner for every `j` is one number carried forward. Run on the day-to-day price differences, this is Kadane's algorithm (#20) with `best` started at `0`, the mistake there but correct here, because not trading is allowed. The fee and cooldown versions (LC 714, LC 309) carry a few running balances instead of one minimum, the best cash while holding a share and while not holding one, plus a resting state for the cooldown. The classic mistake is answering `max(prices) - min(prices)`, which ignores the order of the days: on `[7, 6, 4, 3, 1]` it reports `6`, but the price only falls and the answer is `0`.

*Practice:* LC 121 Best Time to Buy and Sell Stock · LC 122 Best Time to Buy and Sell Stock II · LC 714 Best Time to Buy and Sell Stock with Transaction Fee · LC 309 Best Time to Buy and Sell Stock with Cooldown

```{=latex}
\clearpage
```

## 22. Subsets {#a22}

```{=latex}
\markright{22. Subsets}
```

[Choose, Recurse, Un-Choose · Backtracking · Tier 1]{.meta}

Given an array of distinct integers, return all of its subsets, the power set, each exactly once and in any order. For `[1, 2, 3]` there are `2^3 = 8` of them: `[]`, `[1]`, `[1, 2]`, `[1, 2, 3]`, `[1, 3]`, `[2]`, `[2, 3]` and `[3]`.

Each element faces one yes-or-no decision, so there are `2^n` subsets, and any method that lists them pays at least that much. Backtracking grows them as a tree. The root is the empty subset, and each child appends one more element, always one that lies to the right of everything its parent holds. That rule is what makes every subset appear exactly once, in index order: `[1, 2]` is built, `[2, 1]` never is. The recursion carries the rule as a `start` index. At a node the loop tries each `i` from `start` on: append `nums[i]` (choose), recurse with `start = i + 1`, then pop it again (un-choose), so the next sibling begins from the same path its parent had.

Unlike permutations (#23), where only the leaves are answers, every node of this tree is a subset, so a call records its path the moment it begins, before the loop. One shared list, `path`, carries the whole search: it grows on the way down and shrinks on the way up, a stack that always spells the route from the root to the current node.

```text
                       []
         ┌─────────────┼─────────────┐
        [1]           [2]           [3]
     ┌───┴───┐         │
   [1,2]   [1,3]     [2,3]
     │
  [1,2,3]

recorded in preorder: [] [1] [1,2] [1,2,3] [1,3] [2] [2,3] [3]
below [2] the loop starts at index 2, so only 3 may follow: no [2,1]
```

```pseudo
FUNCTION Backtrack(nums, start, path, result)
    result.append(path.copy())             // every node is a subset
    FOR i FROM start TO len(nums) - 1
        path.append(nums[i])               // choose
        Backtrack(nums, i + 1, path, result)   // only later indices below
        path.pop()                         // un-choose

FUNCTION Subsets(nums)
    result ← empty list
    Backtrack(nums, 0, empty list, result)
    RETURN result
```

The tree has `2^n` nodes and copying a path costs up to `O(n)`, so the time is `O(n · 2^n)`; beyond the output, the space is the `O(n)` path and recursion depth. Reach for this template when a problem asks for all subsets or all combinations of a small input (n up to about 20), or when a search has to try every selection. With duplicates in the input (LC 90), sort first and skip `nums[i]` when `i > start` and `nums[i] = nums[i - 1]`: equal values then sit side by side, and on one level only the first of a run may open a branch, which stops `[1, 2, 2]` from producing `[1, 2]` twice. The same `2^n` subsets also come out of a plain loop over bitmasks (#99). The classic mistake is `result.append(path)` without the copy: every entry is then the same list object, and for `[1, 2, 3]` the search ends with eight references to one empty list.

*Practice:* LC 78 Subsets · LC 90 Subsets II · LC 1863 Sum of All Subset XOR Totals

```{=latex}
\clearpage
```

## 23. Permutations {#a23}

```{=latex}
\markright{23. Permutations}
```

[Backtracking with a Used Array · Backtracking · Tier 1]{.meta}

Given an array of distinct integers, return every ordering of its elements, in any order. `[1, 2, 3]` has `3! = 6` permutations: `[1, 2, 3]`, `[1, 3, 2]`, `[2, 1, 3]`, `[2, 3, 1]`, `[3, 1, 2]` and `[3, 2, 1]`.

A permutation fills n slots from left to right: n choices for the first slot, `n - 1` for the second, down to one for the last. Backtracking walks exactly that decision tree. The `path` holds the slots filled so far, and a `used` array of booleans remembers which indices already sit in it, so every level loops over all the indices from 0 again and skips only the used ones. That is the difference from subsets (#22): there is no start index, because order matters here and `2` may come before `1`, as long as it has not been placed already. Each choice is undone in reverse, pop the value and then clear its flag, so the next sibling sees exactly the state its parent saw.

Only a full path is an answer. The tree is a fan that narrows by one at every level, n branches at the root and `n - 1` under each child, and its `n!` leaves are the permutations, each recorded as a copy when the length of the path reaches n.

```text
                          []                             3 choices
         ┌─────────────────┼─────────────────┐
        [1]               [2]               [3]          2 choices each
     ┌───┴───┐         ┌───┴───┐         ┌───┴───┐
   [1,2]   [1,3]     [2,1]   [2,3]     [3,1]   [3,2]     1 choice each
     │       │         │       │         │       │
  [1,2,3] [1,3,2]   [2,1,3] [2,3,1]   [3,1,2] [3,2,1]    6 leaves = 3 × 2 × 1

at [2,1] used = [T, T, F]: the loop skips indices 0 and 1 and appends 3
```

```pseudo
FUNCTION Backtrack(nums, used, path, result)
    IF len(path) = len(nums)
        result.append(path.copy())          // every slot is filled
        RETURN
    FOR i FROM 0 TO len(nums) - 1
        IF used[i]
            CONTINUE                        // already in the path
        used[i] ← true                      // choose
        path.append(nums[i])
        Backtrack(nums, used, path, result)
        path.pop()                          // un-choose, in reverse order
        used[i] ← false

FUNCTION Permutations(nums)
    used ← array of len(nums) copies of false
    result ← empty list
    Backtrack(nums, used, empty list, result)
    RETURN result
```

There are `n!` leaves and fewer than `e · n!` nodes in all, and each node scans at most n flags, so the time is `O(n · n!)`; the space beyond the output is `O(n)` for the path, the flags and the recursion. Reach for it when a problem wants every ordering or arrangement, which is only feasible for small n: `8!` is 40,320, while `12!` is already about 479 million. With duplicates in the input (LC 47), sort first and also skip `i` when `nums[i] = nums[i - 1]` and `used[i - 1]` is false: equal values must then enter the path from left to right, so each distinct ordering is built once. When only the next ordering in lexicographic order is needed (LC 31), it can be found in place in `O(n)` without any tree. The classic mistake is forgetting `used[i] ← false` on the way back: the flags stay set after the first leaf, and `[1, 2, 3]` returns only `[[1, 2, 3]]`.

*Practice:* LC 46 Permutations · LC 47 Permutations II · LC 31 Next Permutation

```{=latex}
\clearpage
```

## 24. Binary Tree Level-Order Traversal {#a24}

```{=latex}
\markright{24. Binary Tree Level-Order Traversal}
```

[BFS One Level at a Time · BFS · Tier 1]{.meta}

Given the root of a binary tree, return its values level by level, each level read from left to right. Writing the tree in level order with `null` for a missing child, `[3, 9, 20, null, null, 15, 7]` is a root `3` with children `9` and `20`, and `20` has children `15` and `7`; the answer is `[[3], [9, 20], [15, 7]]`.

A queue already visits a tree in level order. The root goes in, and every node that comes out sends its children to the back, so all of depth `d` leaves the queue before anything of depth `d + 1`. What a plain breadth-first search loses is the boundary: it produces one flat stream and forgets where one level ends and the next begins. The fix is a snapshot. At the top of each round the queue holds exactly one complete level, nothing more and nothing less, so `size ← len(queue)` freezes that count and the inner loop pops exactly `size` nodes. The children those pops enqueue pile up behind them and become the next level, untouched until the next round takes its own snapshot.

Picture the tree peeled from the top, one horizontal layer per round: the front of the queue is the layer being stripped off, the back is the layer being laid down. Left-to-right order comes for free, because parents leave the queue left to right and each one enqueues its left child before its right.

```text
        3         round   queue at start   size   popped    enqueued
       / \          1     [3]                1    3         9, 20
      9   20        2     [9, 20]            2    9, 20     15, 7
         /  \       3     [15, 7]            2    15, 7     nothing
        15   7            []                      the queue is empty: stop
levels = [[3], [9, 20], [15, 7]]
```

```pseudo
FUNCTION LevelOrder(root)
    levels ← empty list
    IF root = null
        RETURN levels
    queue ← empty queue
    queue.enqueue(root)
    WHILE queue is not empty
        size ← len(queue)                  // snapshot: exactly this level
        level ← empty list
        FOR i FROM 0 TO size - 1
            node ← queue.dequeue()
            level.append(node.val)
            IF node.left ≠ null            // children join the back
                queue.enqueue(node.left)
            IF node.right ≠ null
                queue.enqueue(node.right)
        levels.append(level)               // the level is complete
    RETURN levels
```

Every node is enqueued and dequeued once, so the traversal takes `O(n)` time; the queue never holds more than one level plus part of the next, `O(w)` space for the widest level `w`, which reaches about `n / 2` in a complete tree. Reach for it whenever a problem says level, depth, row, layer or "seen from the side". The variants differ only in what each finished level contributes: the right side view keeps its last value, zigzag order reverses every other `level` before appending it, and the average of each level divides its sum by `size`. On a general graph the same loop needs a visited set and becomes BFS shortest path (#30). The classic mistake is looping against the live queue length instead of the snapshot: the children enqueued during the round grow the queue, and the next level leaks into this one.

*Practice:* LC 102 Binary Tree Level Order Traversal · LC 199 Binary Tree Right Side View · LC 103 Binary Tree Zigzag Level Order Traversal · LC 637 Average of Levels in Binary Tree

```{=latex}
\clearpage
```

## 25. Diameter and Max Path Sum {#a25}

```{=latex}
\markright{25. Diameter and Max Path Sum}
```

[Postorder DFS That Returns a Height · DFS · Tier 1]{.meta}

The diameter of a binary tree is the number of edges on its longest path between two nodes, and the maximum path sum is the largest total of node values along any path of at least one node. In `[1, 2, 3, 4, 5]` the diameter is `3`, along `4 → 2 → 1 → 3`; in `[-10, 9, 20, null, null, 15, 7]` the best sum is `42`, along `15 → 20 → 7`.

The brute force takes every pair of endpoints and walks the path between them: `O(n²)` pairs at up to `O(n)` steps each, cubic time in all. The insight is that every path has exactly one highest node, where it bends: it climbs up one arm and comes down the other. So skip the endpoints and ask each node a single question, "what is the best path that bends here?", and answer it from two numbers its children already know, the best downward arm on each side. That makes the recursion postorder, children before parent, and gives it two jobs. It returns the best single arm upward, because a parent can extend only one arm. It writes the bent path, left arm plus right arm, into a shared `best`, because a path that bends here is finished and no ancestor can use it.

For the diameter the arm is a height: `Height(node)` counts the nodes on the longest downward path, so an empty subtree has height `0` and the path bending at a node has exactly `left + right` edges. For the path sum the arm is a gain, the node's value plus its better child gain, and a gain below zero is clipped to `0`: do not take that arm at all. Negatives are also why `best` starts at `root.val` instead of `0`: a path holds at least one node, so when every value is negative the answer is the largest single value.

```text
      1          node  left  right  left + right  best  returns
     / \           4     0     0         0          0      1
    2   3          5     0     0         0          0      1
   / \             2     1     1         2          2      2
  4   5            3     0     0         0          2      1
                   1     2     1         3          3      3    diameter 3

    -10          node  left  right  val + left + right  best  returns
    /  \           9     0     0            9             9      9
   9    20        15     0     0           15            15     15
       /  \        7     0     0            7            15      7
      15   7      20    15     7           42            42     35
                 -10     9    35           34            42     25    sum 42
```

```pseudo
FUNCTION Diameter(root)
    best ← [0]                             // a box every call can update
    Height(root, best)
    RETURN best[0]

FUNCTION Height(node, best)
    IF node = null
        RETURN 0
    left ← Height(node.left, best)
    right ← Height(node.right, best)
    best[0] ← max(best[0], left + right)   // the path that bends at node
    RETURN 1 + max(left, right)            // only one arm continues upward

FUNCTION MaxPathSum(root)
    best ← [root.val]                      // one node alone is a path
    Gain(root, best)
    RETURN best[0]

FUNCTION Gain(node, best)
    IF node = null
        RETURN 0
    left ← max(Gain(node.left, best), 0)   // a negative arm is cut off
    right ← max(Gain(node.right, best), 0)
    best[0] ← max(best[0], node.val + left + right)
    RETURN node.val + max(left, right)
```

Each node is visited once with constant work, so both run in `O(n)` time and `O(h)` space for the recursion stack, where `h` is the tree's height, `O(n)` on a chain. Recognize the pattern when the answer is a path that may lie anywhere in the tree: return what a parent can extend, record what only this node can complete. The same skeleton checks balance by returning the height or `-1` once a subtree is lopsided, and finds the longest univalue path by letting an arm continue only into a child with the same value. The classic mistake is passing the bent path upward, `1 + left + right` instead of `1 + max(left, right)`: the parent then extends something that is no longer a path, and `[1, 2, 3, 4, 5]` reports a diameter of `4`.

*Practice:* LC 543 Diameter of Binary Tree · LC 124 Binary Tree Maximum Path Sum · LC 110 Balanced Binary Tree · LC 687 Longest Univalue Path

```{=latex}
\clearpage
```

## 26. Lowest Common Ancestor {#a26}

```{=latex}
\markright{26. Lowest Common Ancestor}
```

[Postorder Search in a Binary Tree · DFS · Tier 1]{.meta}

Given a binary tree and two of its nodes `p` and `q`, both present, return their lowest common ancestor: the deepest node that has both of them in its subtree, where a node counts as an ancestor of itself. In `[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4]` the LCA of `7` and `8` is the root `3`, the LCA of `6` and `4` is `5`, and the LCA of `5` and `4` is `5` itself.

One way is to record the path from the root to `p` and the path to `q` and keep the last node they share, which costs two searches and two stored paths. The postorder search does it in a single pass by letting every subtree send up one report: `null` if it holds neither target, the target itself if it holds one, and the meeting point once it holds both. A call that lands on `p` or `q` returns at once without looking below, and that is safe: if the other target sits underneath, this node is the answer anyway, and if it does not, the other target lives elsewhere and an ancestor will collect both reports. The first node that hears a report from its left subtree and another from its right is where the two root paths split, so it is the lowest common ancestor. From there up, every ancestor hears from one side only and simply forwards it.

Picture two flares fired from `p` and `q`. Each climbs toward the root through its ancestors, and the first node lit from both sides is the answer; it swallows both flares and sends up a single one, itself.

```text
              3                 node   left   right   returns
            /   \                 6    null   null    null
          5       1               7    is p, stops    7
         / \     / \              4    null   null    null
        6   2   0   8             2    7      null    7
           / \                    5    null   7       7
          7   4                   0    null   null    null
                                  8    is q, stops    8
     p = 7, q = 8                 1    null   8       8
                                  3    7      8       3   both sides: the LCA
```

```pseudo
FUNCTION LowestCommonAncestor(root, p, q)
    IF root = null OR root = p OR root = q
        RETURN root                    // nothing here, or a target itself
    left ← LowestCommonAncestor(root.left, p, q)
    right ← LowestCommonAncestor(root.right, p, q)
    IF left ≠ null AND right ≠ null
        RETURN root                    // one target on each side: the LCA
    IF left ≠ null
        RETURN left                    // pass the single report upward
    RETURN right
```

Every node is visited at most once, so the search costs `O(n)` time and `O(h)` space for the recursion. Reach for it whenever a question involves two nodes and where their paths to the root meet; the distance between two nodes, for instance, is `depth(p) + depth(q) - 2 * depth(lca)`. In a binary search tree the values do the steering: walk down from the root, going left while both values are smaller and right while both are larger, and the first node that separates them, or equals one of them, is the LCA, in `O(h)`. With parent pointers it turns into the intersection of two linked lists: climb from both nodes, restart each pointer at the other node when it passes the root, and the two meet at the LCA after equal distances. The classic mistake is forgetting the promise that both nodes exist: when only `p` is in the tree, the search still returns `p`, so a version without that promise must confirm that both targets were seen.

*Practice:* LC 236 Lowest Common Ancestor of a Binary Tree · LC 235 Lowest Common Ancestor of a Binary Search Tree · LC 1650 Lowest Common Ancestor of a Binary Tree III

```{=latex}
\clearpage
```

## 27. Validate a Binary Search Tree {#a27}

```{=latex}
\markright{27. Validate a Binary Search Tree}
```

[Carry the Allowed Range Down · BST · Tier 1]{.meta}

Given the root of a binary tree, decide whether it is a valid binary search tree: for every node, all values in its left subtree are strictly smaller than the node's value and all values in its right subtree are strictly larger. `[2, 1, 3]` is valid. `[5, 4, 6, null, null, 3, 7]` is not, even though every child sits on the correct side of its own parent, because `3` lives in the right subtree of `5`.

The tempting check compares each node only with its children, and that second tree is exactly why it fails: `3 < 6` is fine locally, yet the root promised that everything on its right exceeds `5`. The BST rule is a promise about whole subtrees, and promises pile up on the way down. Each time the path turns left at a node, everything below is capped by that node's value; each time it turns right, everything below is floored by it. So carry the promises as one open interval `(low, high)`. The root may hold anything, `(-∞, ∞)`; a left child keeps its parent's `low` and takes the parent's value as its `high`; a right child keeps `high` and takes the parent's value as its `low`. A node passes when its value lies strictly inside its interval, and the tree is valid when every node passes.

Geometrically, each node cuts the number line at its value, and stepping into a subtree keeps only one side of the cut. The window at a node is the gap between two ancestors: the nearest one it hangs to the right of and the nearest one it hangs to the left of. The search stops at the first node outside its window, so `7` below is never looked at.

```text
           5                 node   allowed range   verdict
         /   \                 5      (-∞, ∞)         inside
        4     6                4      (-∞, 5)         inside
             / \               6      (5, ∞)          inside
            3   7              3      (5, 6)          3 ≤ 5: outside → false
                               7      never checked
each parent-child pair looks fine (4 < 5, 6 > 5, 3 < 6, 7 > 6), yet 3 < 5
```

```pseudo
FUNCTION IsValidBST(root)
    RETURN Fits(root, -∞, ∞)

FUNCTION Fits(node, low, high)
    IF node = null
        RETURN true
    IF node.val ≤ low OR node.val ≥ high
        RETURN false                       // breaks a promise made higher up
    IF NOT Fits(node.left, low, node.val)  // left side: below node.val
        RETURN false
    RETURN Fits(node.right, node.val, high)    // right side: above node.val
```

Each node is checked once, so validation costs `O(n)` time and `O(h)` space for the recursion. The equivalent test is an inorder traversal: a tree is a BST exactly when its inorder sequence is strictly increasing, so walk it while remembering the previous value and fail on the first value that is not larger. The same inorder walk, stopped at the `k`-th value, finds the `k`-th smallest element. Strict inequalities make duplicates invalid, as the definition demands. Reach for the interval whenever a constraint flows from ancestors to descendants rather than from parent to child. The classic mistake is the parent-versus-child check; the runner-up is seeding the bounds with the smallest and largest 32-bit integers, which rejects a lone root holding exactly one of those values, a trap that `-∞` and `∞` avoid.

*Practice:* LC 98 Validate Binary Search Tree · LC 230 Kth Smallest Element in a BST · LC 99 Recover Binary Search Tree

```{=latex}
\clearpage
```

## 28. Depth-First Search on a Graph {#a28}

```{=latex}
\markright{28. Depth-First Search on a Graph}
```

[Recursive and Iterative · DFS · Tier 1]{.meta}

Given an undirected graph with nodes `0` to `n - 1` and a list of edges, list the nodes in the order a depth-first search from `start` first reaches them, trying each node's neighbors in the order its edges appear. With `n = 5`, edges `[[0, 1], [0, 4], [0, 2], [1, 3], [3, 2]]` and `start = 0` the order is `[0, 1, 3, 2, 4]`.

Depth-first search is the maze walker's rule: always step to an unvisited neighbor of the node you stand on, and only when there is none, back up to the previous junction and try its next corridor. The recursion is that rule written down. Entering a node marks it visited, records it, and calls itself on every neighbor not yet visited; the call stack is the trail back to the start, and returning from a call is the step back. Marking on entry is what makes cycles harmless: the square `0, 1, 3, 2` leads back to `0`, but `0` is already marked, so the walk turns away instead of circling forever.

The iterative version swaps the call stack for an explicit one, and where it marks decides whether it is still depth-first. Marking a node when it is popped, and skipping the stale copies of nodes pushed twice, reproduces the recursion exactly, as long as the neighbors go on in reverse so the first one ends on top. Marking a node when it is pushed looks tidier, since nothing is pushed twice, but it is a different search: whoever sees a node first claims it, even when a deeper node would have stepped into it sooner. Here `0` claims `2`, so `3` cannot step to it and the walk retreats to `4`, giving `[0, 1, 3, 4, 2]`, an order no depth-first search can produce.

```text
  4 ─── 0 ─── 1      pop   action                stack after   order
        │     │       0    visit, push 2, 4, 1   [2, 4, 1]     [0]
        2 ─── 3       1    visit, push 3         [2, 4, 3]     [0, 1]
                      3    visit, push 2         [2, 4, 2]     [0, 1, 3]
  the top of the      2    visit, push nothing   [2, 4]        [0, 1, 3, 2]
  stack is on the     4    visit, push nothing   [2]           [0, 1, 3, 2, 4]
  right               2    stale copy: skip      []
marking on push instead: [0, 1, 3, 4, 2], since 2 was already claimed by 0
```

```pseudo
FUNCTION BuildGraph(n, edges)
    graph ← empty list
    FOR i FROM 0 TO n - 1
        graph.append(empty list)
    FOR EACH (u, v) IN edges
        graph[u].append(v)
        graph[v].append(u)                 // undirected: both directions
    RETURN graph

FUNCTION DfsRecursive(n, edges, start)
    graph ← BuildGraph(n, edges)
    visited ← empty set
    order ← empty list
    Visit(graph, start, visited, order)
    RETURN order

FUNCTION Visit(graph, node, visited, order)
    visited.add(node)                      // mark first: cycles cannot re-enter
    order.append(node)
    FOR EACH neighbor IN graph[node]
        IF neighbor NOT IN visited
            Visit(graph, neighbor, visited, order)

FUNCTION DfsIterative(n, edges, start)
    graph ← BuildGraph(n, edges)
    visited ← empty set
    order ← empty list
    stack ← empty stack
    stack.push(start)
    WHILE stack is not empty
        node ← stack.pop()
        IF node IN visited
            CONTINUE                       // a stale copy, reached another way
        visited.add(node)                  // mark when popped
        order.append(node)
        FOR EACH neighbor IN reversed(graph[node])   // first one ends on top
            IF neighbor NOT IN visited
                stack.push(neighbor)
    RETURN order
```

Every node is entered once and every edge is examined from both ends, so both versions run in `O(V + E)` time; the recursion can be `V` frames deep, and the explicit stack can hold one entry per edge end, `O(E)`. Reach for it whenever the question is about reachability, connectivity or exploring paths: counting components (#62), flood fill on a grid (#29), cycle detection (#60) and topological order (#61) are all this walk with something recorded on the way in or out. A directed graph drops the second `append`. In Python the recursive form dies on deep graphs, because the default recursion limit is 1000 frames and a path of a thousand nodes raises `RecursionError`, so the iterative version is the safe default. The classic mistake is marking a node only after its neighbors are explored, which lets a cycle walk back into it until the stack overflows.

*Practice:* LC 547 Number of Provinces · LC 841 Keys and Rooms · LC 797 All Paths From Source to Target · LC 133 Clone Graph

```{=latex}
\clearpage
```

## 29. Number of Islands {#a29}

```{=latex}
\markright{29. Number of Islands}
```

[Grid Flood Fill · DFS · Tier 1]{.meta}

Given a grid of `"1"` for land and `"0"` for water, count the islands: groups of land cells joined up, down, left or right, never diagonally. The grid with rows `11000`, `11000`, `00100` and `00011` has `3` islands, a two-by-two block at the top left, a single cell in the middle and a pair at the bottom right.

Read the grid as a graph whose nodes are land cells and whose edges join horizontal and vertical neighbors. An island is a connected component, so counting islands is counting components. A scan walks every cell in reading order; whenever it meets a `"1"`, that cell belongs to an island nobody has counted yet, so the count goes up by one. Then a flood fill sinks the whole island, turning every land cell reachable from that start into `"0"`. Sinking is the visited mark, written straight into the grid: when the scan later reaches another cell of the same island it finds water and moves on, so each island is counted exactly once, at its first cell in reading order.

The flood fill is the depth-first search of #28 on a graph that is never built. The four neighbors of `(row, col)` are one step down, up, right and left, computed on the fly. This version pushes all four without looking and lets the pop decide: a position off the map, on water or on land already sunk is thrown away, and a land cell is sunk and pushes its own four neighbors. Only the set of cells reached matters here, not their order, so this simplest form is enough.

```text
the grid      sink order     the scan
1 1 0 0 0     1 2 . . .      (0, 0) is land: count 1, sink 4 cells in 17 pops
1 1 0 0 0     4 3 . . .
0 0 1 0 0     . . 1 . .      (2, 2) is land: count 2, sink 1 cell in 5 pops
0 0 0 1 1     . . . 1 2      (3, 3) is land: count 3, sink 2 cells in 9 pops
every other cell is water by the time the scan reaches it → 3 islands
```

```pseudo
FUNCTION NumIslands(grid)
    count ← 0
    FOR row FROM 0 TO len(grid) - 1
        FOR col FROM 0 TO len(grid[0]) - 1
            IF grid[row][col] = "1"
                count ← count + 1          // a new island starts here
                Sink(grid, row, col)       // so it is never counted again
    RETURN count

FUNCTION Sink(grid, start_row, start_col)
    stack ← empty stack
    stack.push((start_row, start_col))
    WHILE stack is not empty
        (row, col) ← stack.pop()
        IF row < 0 OR row ≥ len(grid) OR col < 0 OR col ≥ len(grid[0])
            CONTINUE                       // stepped off the map
        IF grid[row][col] ≠ "1"
            CONTINUE                       // water, or land already sunk
        grid[row][col] ← "0"               // sinking is the visited mark
        stack.push((row + 1, col))         // down, up, right, left
        stack.push((row - 1, col))
        stack.push((row, col + 1))
        stack.push((row, col - 1))
```

Every cell is scanned once and sunk at most once, and each sinking pushes four positions, so the count costs `O(R × C)` time for `R` rows and `C` columns, and the stack can reach `O(R × C)` on solid land. The recursive form reads the same, with `Sink` calling itself on the four neighbors instead of pushing them, but on a 300 by 300 grid of land it snakes through every cell and goes 90,000 calls deep, far past Python's recursion limit; the explicit stack has no such ceiling. When the caller's grid must survive, keep a visited set of positions instead of sinking. Signals are a grid and "how many groups"; the same fill measures the largest island by counting cells as it sinks them, recolors a region in flood fill, and solves surrounded regions by first marking everything connected to the border. The classic mistake in Python is dropping the `row < 0` or `col < 0` test: `grid[-1]` silently reads the last row, so an island on the top edge leaks into one on the bottom edge.

*Practice:* LC 200 Number of Islands · LC 695 Max Area of Island · LC 733 Flood Fill · LC 130 Surrounded Regions

```{=latex}
\clearpage
```

## 30. BFS Shortest Path {#a30}

```{=latex}
\markright{30. BFS Shortest Path}
```

[Unweighted Graphs, Layer by Layer · BFS · Tier 1]{.meta}

Given an unweighted graph, find a shortest path from a source node to a target node, where the length of a path is its number of edges. On six nodes with the undirected edges `0-1`, `1-2`, `2-3`, `3-4`, `0-5` and `5-4`, the shortest path from `0` to `4` is `[0, 5, 4]`, two edges, while the long way round, `0-1-2-3-4`, takes four.

The brute force lets a depth-first search enumerate every simple path and keeps the shortest, and the number of simple paths can grow exponentially with the graph. Breadth-first search never compares routes, because it explores in order of distance. The queue is first in, first out, so every node at distance `d` leaves it before any node at distance `d + 1`, and a node is first discovered by a neighbor from the lowest possible layer: the distance it receives at that moment is final. Two arrays hold the whole answer. `dist[v]` doubles as the visited mark, with `-1` for not reached yet, and `parent[v]` records which node discovered `v`. Following parents back from the target walks a shortest path in reverse.

Picture a stone dropped on the source. The ripples are the layers, `{0}`, then `{1, 5}`, then `{2, 4}`, then `{3}`, and each node belongs to the first ripple that touches it. Node `4` is touched at distance 2 by the ripple through `5`, while the wave along the top is still two steps away, and its parent pointer remembers the route it came by.

```text
  0 ── 1 ── 2 ── 3         layer 0: 0
  │              │         layer 1: 1, 5
  5 ──────────── 4         layer 2: 2, 4
                           layer 3: 3
pop  dist  newly reached: node (dist, parent)    queue after
 0    0    1 (1, 0)   5 (1, 0)                   [1, 5]
 1    1    2 (2, 1)                              [5, 2]
 5    1    4 (2, 5)                              [2, 4]
 2    2    3 (3, 2)                              [4, 3]
 4    2    none: 3 and 5 are already marked      [3]
 3    3    none                                  []
dist   = [0, 1, 2, 3, 2, 1]
parent = [-1, 0, 1, 2, 5, 0]
path: 4 → 5 → 0 by parents, reversed: [0, 5, 4]
```

```pseudo
FUNCTION ShortestPath(n, edges, source, target)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)                 // undirected: both directions
        graph[v].append(u)
    dist ← array of n copies of -1         // -1 means not reached yet
    parent ← array of n copies of -1       // the node that first reached it
    dist[source] ← 0
    queue ← empty queue
    queue.enqueue(source)
    WHILE queue is not empty
        node ← queue.dequeue()
        FOR EACH neighbor IN graph[node]
            IF dist[neighbor] = -1         // first visit is a shortest one
                dist[neighbor] ← dist[node] + 1     // mark when enqueued
                parent[neighbor] ← node
                queue.enqueue(neighbor)
    IF dist[target] = -1
        RETURN empty list                  // target is in another component
    RETURN BuildPath(parent, target)

FUNCTION BuildPath(parent, target)
    path ← empty list
    node ← target
    WHILE node ≠ -1                        // only the source has no parent
        path.append(node)
        node ← parent[node]
    RETURN reverse(path)
```

Every node enters the queue at most once and every edge is examined once from each end, so the search costs `O(V + E)` time and `O(V)` space beyond the graph. Reach for it whenever a problem asks for the fewest steps, moves, hops or edits and every step costs the same; weighted edges need Dijkstra (#33). A grid is the same graph in disguise: in LC 1091 the nodes are the open cells, the neighbors are the eight cells around each one, and the loop runs unchanged on `(row, col)` pairs, though that problem counts the cells on the path, one more than its edges. When only one target matters, the loop may stop the moment the target is marked. The classic mistake is marking a node when it leaves the queue instead of when it enters. Until it leaves, every frontier node that touches it enqueues it again and rewrites its `dist`, so a longer route can overwrite the right answer: searching from `0` over the edges `0-1`, `0-2`, `1-3`, `2-4`, `3-4`, node `4` ends at distance 3 instead of 2.

*Practice:* LC 1091 Shortest Path in Binary Matrix · LC 1971 Find if Path Exists in Graph · LC 433 Minimum Genetic Mutation · LC 286 Walls and Gates

```{=latex}
\clearpage
```

## 31. Kahn's Algorithm {#a31}

```{=latex}
\markright{31. Kahn's Algorithm}
```

[Topological Sort by Peeling Indegree-Zero Nodes · Topological Sort · Tier 1]{.meta}

There are `n` courses numbered `0` to `n - 1`, and a prerequisite pair `[a, b]` means course `b` must be taken before course `a`. Return an order that takes every course, or an empty list if no order exists. With six courses and the pairs `[3, 0]`, `[3, 1]`, `[4, 3]`, `[2, 3]`, `[5, 4]`, `[5, 2]`, one valid order is `[0, 1, 3, 4, 2, 5]`.

Read each pair as an arrow `b → a`. An order is valid when every arrow points forward, which makes it a topological order of the graph. The brute force tries all `n!` orders and checks each one. Kahn's insight is that a graph without a cycle always has a free course, one with no arrow coming in. Take a free course, erase its outgoing arrows, and what remains is a smaller copy of the same problem. An indegree array makes the erasing cheap: `indegree[c]` counts the prerequisites of `c` not yet taken, taking a course subtracts one from each course it unlocks, and a course whose count reaches zero joins the queue of free courses. The queue holds exactly the courses that are free and not yet taken.

Picture the drawing eaten from the left. The courses with nothing pointing at them form its left edge; taking one erases its arrows, and any course that loses its last incoming arrow joins the new left edge. Course `3` sits behind two arrows, so it surfaces only after both `0` and `1` are taken, and `5` only after `4` and `2`. If the queue runs dry with courses left over, each of them still has an arrow coming in from another leftover course, and walking those arrows backward must eventually revisit a course. So a cycle exists, and `len(order) < num_courses` is the entire cycle test.

```text
    0 ──┐            ┌──→ 4 ──┐
        ├──→ 3 ──────┤        ├──→ 5
    1 ──┘            └──→ 2 ──┘

take   indegree of 0..5     queue     order
 -     [0, 0, 1, 2, 1, 2]   [0, 1]    []
 0     [0, 0, 1, 1, 1, 2]   [1]       [0]
 1     [0, 0, 1, 0, 1, 2]   [3]       [0, 1]
 3     [0, 0, 0, 0, 0, 2]   [4, 2]    [0, 1, 3]
 4     [0, 0, 0, 0, 0, 1]   [2]       [0, 1, 3, 4]
 2     [0, 0, 0, 0, 0, 0]   [5]       [0, 1, 3, 4, 2]
 5     [0, 0, 0, 0, 0, 0]   []        [0, 1, 3, 4, 2, 5]
```

```pseudo
FUNCTION FindOrder(num_courses, prerequisites)
    graph ← array of num_courses empty lists
    indegree ← array of num_courses zeros  // prerequisites not yet taken
    FOR EACH (course, before) IN prerequisites
        graph[before].append(course)       // [a, b] is the edge b → a
        indegree[course] ← indegree[course] + 1
    queue ← empty queue
    FOR course FROM 0 TO num_courses - 1
        IF indegree[course] = 0            // free to take right away
            queue.enqueue(course)
    order ← empty list
    WHILE queue is not empty
        course ← queue.dequeue()
        order.append(course)
        FOR EACH next_course IN graph[course]
            indegree[next_course] ← indegree[next_course] - 1    // one done
            IF indegree[next_course] = 0
                queue.enqueue(next_course)
    IF len(order) < num_courses            // the rest wait on each other
        RETURN empty list
    RETURN order
```

Each course enters the queue at most once and each arrow is erased at most once, so Kahn's algorithm runs in `O(V + E)` time and `O(V + E)` space for the graph. Reach for it whenever a problem speaks of prerequisites, dependencies, build steps or "must come before", or only asks whether an order exists at all, as Course Schedule (LC 207) does. It bends easily: processing the queue one level at a time counts the semesters in Parallel Courses (LC 1136), and in Alien Dictionary each arrow comes from the first differing letter of two adjacent words. Topological Sort with DFS (#61) builds an order from the other end. The classic mistake is reversing the pair: `[a, b]` is the arrow `b → a`, and building `a → b` instead returns an order that breaks every prerequisite.

*Practice:* LC 207 Course Schedule · LC 210 Course Schedule II · LC 269 Alien Dictionary · LC 1136 Parallel Courses

```{=latex}
\clearpage
```

## 32. Union-Find {#a32}

```{=latex}
\markright{32. Union-Find}
```

[Path Compression + Union by Size · Connected Components · Tier 1]{.meta}

Keep `n` nodes in disjoint groups under two operations: `union(a, b)` merges the groups of `a` and `b`, and `find(x)` returns the representative of the group of `x`, so two nodes are connected exactly when they share a representative. Feed it the edges `[0, 1]`, `[2, 3]`, `[0, 2]`, `[3, 1]` on five nodes. The first three each merge two groups; the fourth joins two nodes that are already connected, closing the cycle `0-1-3-2-0`, so it is redundant, and two groups remain, `{0, 1, 2, 3}` and `{4}`.

The brute force stores a group label per node and relabels a whole group on every merge, `O(n)` per union. Union-find stores each group as a tree of parent pointers instead. Every node points toward its root, and the root points at itself and names the group; `find` climbs to the root, and `union` hangs one root under the other with a single pointer write. Two rules keep the trees flat. Union by size hangs the smaller tree under the root of the bigger one, so a node sinks one level deeper only when its tree at least doubles, and no tree grows taller than `log2 n`. Path compression makes `find` repoint every node it climbs past straight at the root, so the next climb takes one step.

Picture a forest of small trees that only ever merge. In the trace, the last union finds `3` two levels below root `0`, and the recursion flattens that path on its way back. The union then returns `false`, because both ends already share root `0`: that `false` is the redundant edge of LC 684, and `count`, which drops by one on every successful union, is the number of components.

```text
edge     roots   what happens                      parent            count
 -                                                 [0, 1, 2, 3, 4]     5
[0, 1]   0, 1    1 hangs under 0, size[0] = 2      [0, 0, 2, 3, 4]     4
[2, 3]   2, 3    3 hangs under 2, size[2] = 2      [0, 0, 2, 2, 4]     3
[0, 2]   0, 2    tie: 2 hangs under 0, size 4      [0, 0, 0, 2, 4]     2
[3, 1]   0, 0    same root: false, redundant       [0, 0, 0, 0, 4]     2

the find(3) inside the last union:
       0                       0
      / \                    / | \
     1   2        ──→       1  2  3         4 stays alone
         |
         3
```

```pseudo
CLASS UnionFind
    FUNCTION Init(n)
        self.parent ← [0, 1, …, n - 1]     // every node starts as its own root
        self.size ← array of n copies of 1 // tree sizes, read only at roots
        self.count ← n                     // number of separate groups

    FUNCTION Find(x)
        IF self.parent[x] ≠ x
            self.parent[x] ← self.Find(self.parent[x])    // path compression
        RETURN self.parent[x]

    FUNCTION Union(a, b)
        root_a ← self.Find(a)
        root_b ← self.Find(b)
        IF root_a = root_b
            RETURN false                   // already connected: a cycle edge
        IF self.size[root_a] < self.size[root_b]
            swap(root_a, root_b)           // root_a is the bigger tree
        self.parent[root_b] ← root_a
        self.size[root_a] ← self.size[root_a] + self.size[root_b]
        self.count ← self.count - 1
        RETURN true

FUNCTION CountComponents(n, edges)
    uf ← UnionFind(n)
    FOR EACH (a, b) IN edges
        uf.Union(a, b)
    RETURN uf.count

FUNCTION FindRedundantConnection(edges)
    uf ← UnionFind(len(edges) + 1)         // nodes are 1..n; slot 0 unused
    FOR EACH (a, b) IN edges
        IF NOT uf.Union(a, b)              // first edge inside one group
            RETURN [a, b]
    RETURN empty list
```

With both rules, `m` operations on `n` nodes cost `O(m · alpha(n))`, where `alpha` is the inverse Ackermann function, at most 4 for any `n` a computer can hold: constant time in practice, and `O(n)` space. Reach for union-find when edges or equivalences arrive one at a time and the questions are "are these two connected?" and "how many groups are there now?": redundant connections, accounts that share an email, islands that appear one cell at a time, and the cycle test inside Kruskal's minimum spanning tree (#83). A flood fill (#62) answers the same questions for a graph given all at once but must search again after every new edge; union-find absorbs each edge in near-constant time, though it can never split a group. The classic mistake is comparing parents instead of roots: before the last union `parent[3]` is `2` and `parent[1]` is `0`, so the redundant edge `[3, 1]` would pass for a new connection.

*Practice:* LC 684 Redundant Connection · LC 547 Number of Provinces · LC 323 Number of Connected Components in an Undirected Graph · LC 721 Accounts Merge

```{=latex}
\clearpage
```

## 33. Dijkstra's Algorithm {#a33}

```{=latex}
\markright{33. Dijkstra's Algorithm}
```

[Shortest Paths with Non-Negative Weights · Shortest Path · Tier 1]{.meta}

A signal leaves node `k` of a network with nodes `1` to `n`, and each directed edge `[u, v, w]` takes `w ≥ 0` units of time to cross. Return the time until every node has the signal, or `-1` if some node never gets it. Each node hears the signal at its shortest distance from `k`, so the answer is the largest of those distances. With `k = 1` and the edges `1→2 (4)`, `1→3 (1)`, `3→2 (2)`, `2→4 (1)` and `3→4 (5)`, the distances to nodes `1` to `4` are `0, 3, 1, 4`, and the answer is `4`.

Relaxing every edge again and again until nothing improves works, and it is Bellman-Ford (#82), at `O(V · E)`. Dijkstra relaxes each edge once, by settling nodes in order of distance, the way BFS (#30) settles them in order of hop count, with a min-heap in place of the queue. The heap holds candidate distances `(d, node)`, and the first entry it pops for a node is final. Any other route to that node must leave the settled region somewhere, and by the time it does it already costs at least `d`, since every node just outside the region waits in the heap at a distance no smaller than `d`; non-negative weights can only add to that. Settling a node relaxes its edges: when `d + w` beats the best known distance to a neighbor, the neighbor's distance drops and a new entry goes on the heap. A plain binary heap cannot lower an entry in place, so the old entry stays behind, and when it surfaces later its `d` is larger than `dist[node]` and it is skipped. That is lazy deletion, and its whole cost is a heap that can hold one entry per edge.

Picture a frontier that only ever moves outward, always at its nearest point. Node `2` first hears of the direct route at distance 4, then the detour through `3` lowers it to 3 and the entry `(4, 2)` goes stale. A negative edge is exactly what breaks this picture, because a step outside the frontier can now lead back to a shorter route. With edges `1→2 (2)`, `1→3 (3)`, `3→2 (-2)` and `2→4 (1)`, node `2` is settled at 2 and hands 3 on to node `4` before the route through `3` shows that `2` is really at 1 and `4` at 2. A version that never reopens a settled node answers 3 for node `4`. The lazy version below reopens `2` and recovers, but nodes can then be popped many times, the time bound is gone, and a negative cycle keeps improving forever: negative weights need Bellman-Ford.

```text
   1 ──(4)──→ 2 ──(1)──→ 4
   │          ↑          ↑
  (1)        (2)        (5)
   ↓          │          │
   3 ─────────┴──────────┘

pop      what happens                     dist of 1..4    heap after, sorted
(0, 1)   settle 1: 2 ← 4, 3 ← 1           [0, 4, 1, ∞]    (1,3) (4,2)
(1, 3)   settle 3: 2 ← 3, 4 ← 6           [0, 3, 1, 6]    (3,2) (4,2) (6,4)
(3, 2)   settle 2: 4 ← 4                  [0, 3, 1, 4]    (4,2) (4,4) (6,4)
(4, 2)   stale: 4 > dist[2] = 3, skip     [0, 3, 1, 4]    (4,4) (6,4)
(4, 4)   settle 4: no edges out           [0, 3, 1, 4]    (6,4)
(6, 4)   stale: 6 > dist[4] = 4, skip     [0, 3, 1, 4]    empty
answer: the largest distance, 4
```

```pseudo
FUNCTION Dijkstra(graph, source)
    dist ← array of len(graph) copies of ∞
    dist[source] ← 0
    heap ← empty min-heap
    heap.push((0, source))                 // (distance so far, node)
    WHILE heap is not empty
        (d, node) ← heap.pop()
        IF d > dist[node]
            CONTINUE                       // stale entry: node settled closer
        FOR EACH (neighbor, weight) IN graph[node]
            IF d + weight < dist[neighbor]         // relax: a shorter route
                dist[neighbor] ← d + weight
                heap.push((dist[neighbor], neighbor))
    RETURN dist

FUNCTION NetworkDelayTime(times, n, k)
    graph ← array of n + 1 empty lists     // nodes are 1..n; slot 0 unused
    FOR EACH (u, v, w) IN times
        graph[u].append((v, w))
    dist ← Dijkstra(graph, k)
    slowest ← 0
    FOR node FROM 1 TO n
        IF dist[node] = ∞
            RETURN -1                      // this node never gets the signal
        slowest ← max(slowest, dist[node])
    RETURN slowest
```

Each node is settled once, so each edge pushes at most one entry; at most `E + 1` pushes and pops at `O(log E) = O(log V)` each give `O((V + E) log V)` time and `O(V + E)` space. Reach for Dijkstra when edges carry non-negative costs, times or distances and the question is the cheapest route. The variants change what a route costs: Path With Minimum Effort minimizes the largest single step, Path with Maximum Probability multiplies probabilities and pops the largest first, and Number of Ways to Arrive at Destination carries a count of shortest routes beside each distance. The classic mistake is borrowing BFS's habit of finalizing a node when it is first pushed: here node `2` would keep distance 4 instead of 3, and node `4` would get 6.

*Practice:* LC 743 Network Delay Time · LC 1514 Path with Maximum Probability · LC 1631 Path With Minimum Effort · LC 1976 Number of Ways to Arrive at Destination

```{=latex}
\clearpage
```

## 34. Trie {#a34}

```{=latex}
\markright{34. Trie}
```

[Insert, Search, Starts With · Tries · Tier 1]{.meta}

Build a prefix tree with three operations: `insert(word)`; `search(word)`, which asks whether that exact word was inserted; and `starts_with(prefix)`, which asks whether any inserted word begins with the prefix. After inserting `apple`, `app`, `apt` and `bat`, `search("ap")` is false but `starts_with("ap")` is true.

A hash set of the words answers `search` in `O(L)` for a word of length L, but a prefix question would have to compare against all n words, `O(n · L)`. A trie stores the words letter by letter along paths from the root, so words that share a prefix share the path that spells it: `app`, `apple` and `apt` all hang below the single path `a → p`. Each node holds a map from letter to child and one flag, `is_end`, that marks where an inserted word stops. Inserting walks down the letters and creates any missing child on the way; both queries walk down the same way and give up the moment a letter has no child.

The path is the prefix, and the subtree below a node holds every word that starts with it. That makes `starts_with` a pure walk: if the letters can be followed, some inserted word starts with them, because every node lies on the path of a word that was inserted. `search` asks one thing more, that the walk ends on a flagged node, and that flag is the whole difference between a prefix and a word.

```text
root                      ● = is_end, a word stops here
├── a
│   └── p
│       ├── p ●           app
│       │   └── l
│       │       └── e ●   apple
│       └── t ●           apt
└── b
    └── a
        └── t ●           bat

search("app")        a → p → p, flagged        → true
search("ap")         a → p, not flagged        → false
starts_with("ap")    a → p, the path exists    → true
search("apl")        a → p, no child 'l'       → false
```

```pseudo
CLASS TrieNode
    FUNCTION Init()
        self.children ← empty map            // letter → TrieNode
        self.is_end ← false                  // true if a word ends here

CLASS Trie
    FUNCTION Init()
        self.root ← new TrieNode()

    FUNCTION Insert(word)
        node ← self.root
        FOR EACH ch IN word
            IF ch NOT IN node.children
                node.children[ch] ← new TrieNode()
            node ← node.children[ch]
        node.is_end ← true                   // the word stops here

    FUNCTION Walk(prefix)
        node ← self.root
        FOR EACH ch IN prefix
            IF ch NOT IN node.children
                RETURN null                  // the path breaks off
            node ← node.children[ch]
        RETURN node

    FUNCTION Search(word)
        node ← self.Walk(word)
        RETURN node ≠ null AND node.is_end

    FUNCTION StartsWith(prefix)
        RETURN self.Walk(prefix) ≠ null
```

Each operation touches one node per letter, so all three run in `O(L)` no matter how many words are stored, and the trie holds at most one node per inserted letter, `O(total letters)` space. Reach for a trie when a problem asks many questions about the prefixes of a fixed set of strings. Autocomplete walks to the prefix node, then runs a DFS below it in alphabetical order to collect suggestions (LC 1268); Replace Words swaps each word for the shortest root met on its walk down (LC 648); a grid search for many words at once follows the trie instead of each word in turn (#63). A wildcard `.` that matches any letter (LC 211) turns the walk into a DFS that tries every child at each dot. The classic mistake is a `search` that returns true as soon as the path exists, which finds `ap` in a trie holding only `apple`.

*Practice:* LC 208 Implement Trie (Prefix Tree) · LC 211 Design Add and Search Words Data Structure · LC 1268 Search Suggestions System · LC 648 Replace Words

```{=latex}
\clearpage
```

## 35. LRU Cache {#a35}

```{=latex}
\markright{35. LRU Cache}
```

[Hash Map + Doubly Linked List · Design · Tier 1]{.meta}

Design a cache with a fixed capacity. `get(key)` returns the value or -1, `put(key, value)` inserts or updates, and when the cache grows past its capacity it evicts the least recently used key, the one whose last `get` or `put` is oldest. Both operations must run in `O(1)`. With capacity 2, after `put(1, 10)` and `put(2, 20)`, `get(1)` returns 10 and makes key 1 the most recent, so `put(3, 30)` evicts key 2 and `get(2)` returns -1.

The brute force keeps the keys in a list ordered by recency, and every operation scans the list to find a key and shift it to the front, `O(n)` each time. The cache needs two abilities at once. Finding a key in `O(1)` is a hash map's job. Keeping the keys in order of recency, moving any one of them to the front and dropping the oldest, each in `O(1)`, is a doubly linked list's job, because a node that knows both of its neighbors can unlink itself without a search. So use both. The list orders the nodes from the most recent, next to `head`, to the least recent, next to `tail`, and the map sends each key straight to its node: its values are arrows into the chain.

Every use of a key is the same two moves: unlink its node and splice it back in right after `head`. Eviction unlinks the node just before `tail` and deletes its key from the map, which is why a node stores its key as well as its value. The two sentinels sit at the ends forever, so the list is never empty, every real node has two neighbors, and the unlink and splice code needs no special cases.

```text
       nodes[3]      nodes[1]          the map holds an arrow to each node
          │             │
          ▼             ▼
head ─── 3:30 ──────── 1:10 ─── tail   after put(3, 30), key 2 is gone
         most recent   least recent

operation        list from head to tail             note
put(1, 10)       head ─ 1:10 ─ tail
put(2, 20)       head ─ 2:20 ─ 1:10 ─ tail
get(1) → 10      head ─ 1:10 ─ 2:20 ─ tail          1 moves to the front
put(3, 30)       head ─ 3:30 ─ 1:10 ─ tail          over capacity: evict 2
get(2) → -1      head ─ 3:30 ─ 1:10 ─ tail          a miss moves nothing
put(4, 40)       head ─ 4:40 ─ 3:30 ─ tail          over capacity: evict 1
get(1) → -1      head ─ 4:40 ─ 3:30 ─ tail
get(3) → 30      head ─ 3:30 ─ 4:40 ─ tail
get(4) → 40      head ─ 4:40 ─ 3:30 ─ tail
```

```pseudo
CLASS Node
    FUNCTION Init(key, value)
        self.key ← key                  // kept so eviction can clean the map
        self.value ← value
        self.prev ← null
        self.next ← null

CLASS LRUCache
    FUNCTION Init(capacity)
        self.capacity ← capacity
        self.nodes ← empty map          // key → node
        self.head ← Node(0, 0)          // sentinel: head.next is most recent
        self.tail ← Node(0, 0)          // sentinel: tail.prev is least recent
        self.head.next ← self.tail
        self.tail.prev ← self.head

    FUNCTION Remove(node)
        node.prev.next ← node.next
        node.next.prev ← node.prev

    FUNCTION AddFront(node)
        node.prev ← self.head
        node.next ← self.head.next
        self.head.next.prev ← node
        self.head.next ← node

    FUNCTION Get(key)
        IF key NOT IN self.nodes
            RETURN -1
        node ← self.nodes[key]
        self.Remove(node)               // a read counts as a use
        self.AddFront(node)
        RETURN node.value

    FUNCTION Put(key, value)
        IF key IN self.nodes
            node ← self.nodes[key]
            node.value ← value
            self.Remove(node)           // it moves to the front below
        ELSE
            node ← Node(key, value)
            self.nodes[key] ← node
        self.AddFront(node)
        IF len(self.nodes) > self.capacity
            lru ← self.tail.prev        // least recently used
            self.Remove(lru)
            self.nodes.remove(lru.key)
```

Each operation is one map lookup plus a fixed number of pointer changes, so `get` and `put` run in `O(1)`, and the cache holds at most `capacity` nodes. Reach for this pairing whenever a problem needs fast lookup plus an order that changes on every access: caches, recently used lists, an eviction policy inside a larger design. Python's `OrderedDict` is this very structure, a hash map threaded with a doubly linked list, and `move_to_end` with `popitem(last=False)` gives a dozen-line solution, but interviewers usually want the list built by hand. LFU Cache extends the idea to one list per use count plus the smallest count in play. The classic mistake is creating a second node when `put` updates an existing key: the map points at the new node, the old one stays in the list, and when that ghost reaches the tail its eviction deletes the live key. Forgetting that `get` also moves its key to the front is the other one.

*Practice:* LC 146 LRU Cache · LC 460 LFU Cache · LC 707 Design Linked List

# Tier 2 · Should Know Well {#tier2}

```{=latex}
\markboth{Tier 2 · Should Know Well}{}
```

The next thirty-five deepen every topic of the first tier and add the classic harder variants: partition-based selection, the histogram stack, expression evaluation, the greedy exchange arguments, grid backtracking, BFS on implicit graphs, topological order by DFS, KMP. They come up often enough that each one deserves a careful read and a run of its code.

```{=latex}
\clearpage
```

## 36. Hash Map with Separate Chaining {#a36}

```{=latex}
\markright{36. Hash Map with Separate Chaining}
```

[Collisions Live in Buckets · Hash Map Internals · Tier 2]{.meta}

Design a hash map without a built-in dictionary: `put(key, value)` inserts a key or overwrites its value, `get(key)` returns the value or `-1` when the key is missing, and `remove(key)` deletes the key. With 8 buckets and integers hashing to themselves, `put(1, 10)` and `put(9, 90)` send both keys to bucket 1, because `1 mod 8 = 9 mod 8 = 1`, and `get(9)` must still return `90`.

A plain list of pairs works, but every call scans all of it, `O(n)` per operation. A hash map splits that one long list into many short ones. It keeps an array of `capacity` buckets and sends each key to bucket `hash(key) mod capacity`, so an operation computes one index and touches only that bucket. Different keys can land in the same bucket; that is a collision, and separate chaining simply lets it happen: each bucket is a small list, a chain, of `[key, value]` pairs. The hash chooses the chain and comparing keys inside the chain chooses the pair, so a `put` of an existing key overwrites in place, a new key is appended, and `remove` unlinks its pair.

The load factor `size / capacity` is the average chain length. With a hash that spreads keys evenly, a lookup scans about that many pairs, so keeping the load factor at most 0.75 makes every operation `O(1)` on average. When a `put` pushes it past 0.75, the map doubles the bucket array and rehashes every pair, because the bucket index depends on the capacity: each old chain splits between bucket `b` and bucket `b + old capacity`.

```text
8 buckets, bucket = key mod 8; put keys 1, 9, 17, 2, 10, 4 with value 10 × key
  bucket 0     ·
  bucket 1     1:10 → 9:90 → 17:170      1, 9 and 17 collide
  bucket 2     2:20 → 10:100             2 and 10 collide
  bucket 3     ·
  bucket 4     4:40
  bucket 5-7   ·                         load = 6 / 8 = 0.75, no resize yet

get(17): bucket 17 mod 8 = 1; compare keys 1 ✗, 9 ✗, 17 ✓ → 170

put(25): bucket 1 again; load 7 / 8 = 0.875 > 0.75 → 16 buckets, rehash
  bucket 1     1:10 → 17:170             the old chain 1 splits
  bucket 9     9:90 → 25:250             between buckets 1 and 9
  bucket 2     2:20                      and chain 2 between
  bucket 10    10:100                    buckets 2 and 10
  bucket 4     4:40                      every other bucket is empty
```

```pseudo
CLASS ChainedHashMap
    FUNCTION Init(capacity)
        self.capacity ← capacity
        self.size ← 0                           // number of keys stored
        self.buckets ← empty list
        FOR i FROM 0 TO capacity - 1
            self.buckets.append(empty list)     // one empty chain per bucket

    FUNCTION BucketOf(key)                      // the chain that holds key
        RETURN self.buckets[hash(key) mod self.capacity]

    FUNCTION Put(key, value)
        bucket ← self.BucketOf(key)
        FOR EACH pair IN bucket
            IF pair[0] = key                    // same key: overwrite the value
                pair[1] ← value
                RETURN
        bucket.append([key, value])             // new key: the chain grows
        self.size ← self.size + 1
        IF self.size / self.capacity > 0.75
            self.Resize()                       // load factor too high: grow

    FUNCTION Get(key)
        bucket ← self.BucketOf(key)
        FOR EACH pair IN bucket
            IF pair[0] = key                    // compare keys, not hashes
                RETURN pair[1]
        RETURN -1

    FUNCTION Remove(key)
        bucket ← self.BucketOf(key)
        FOR EACH pair IN bucket
            IF pair[0] = key
                bucket.remove(pair)
                self.size ← self.size - 1
                RETURN

    FUNCTION Resize()
        old_buckets ← self.buckets
        self.capacity ← 2 * self.capacity
        self.buckets ← empty list
        FOR i FROM 0 TO self.capacity - 1
            self.buckets.append(empty list)
        FOR EACH bucket IN old_buckets
            FOR EACH pair IN bucket
                new_bucket ← self.BucketOf(pair[0])   // uses the new capacity
                new_bucket.append(pair)
```

Every operation costs `O(1)` on average and `O(n)` in the worst case, when all keys hash to the same bucket and the map degenerates into one long chain; Java's `HashMap` turns a long chain into a balanced tree for exactly that reason. A resize costs `O(n)`, but the next one waits until the key count has nearly doubled, so the rehashing over `n` puts adds up to `O(n)`, amortized `O(1)` per put. The space is `O(n + capacity)`. The signals are a request to design a hash map or hash set, or a question about how a dictionary works inside; a good answer names the bucket index, collisions, the load factor and resizing. The classic mistake is copying each old chain to the same index of the bigger array instead of rehashing: key 9 stays in bucket 1, while `get(9)` now looks in bucket `9 mod 16 = 9` and misses it.

*Practice:* LC 706 Design HashMap · LC 705 Design HashSet

```{=latex}
\clearpage
```

## 37. Trapping Rain Water {#a37}

```{=latex}
\markright{37. Trapping Rain Water}
```

[Two Pointers with Running Walls · Two Pointers · Tier 2]{.meta}

Given the heights of bars of width 1 standing side by side, return how many units of rain water they trap between them. `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` traps `6`.

Look at one column at a time. The water above bar `i` rises to the lower of the two walls around it, the tallest bar on its left and the tallest bar on its right, bar `i` itself included, so the column holds `min(max left, max right) - height[i]` units. The brute force rescans both sides for every column, `O(n²)`. Two arrays, prefix maxima from the left and suffix maxima from the right, precompute both walls in `O(n)` time at the price of `O(n)` extra space.

The two-pointer version needs neither array, because a column only needs its lower wall exactly. Walk `left` and `right` inward, with `left_max` the tallest bar seen from the left end and `right_max` the tallest seen from the right end. If `left_max < right_max`, the true right wall of column `left` is at least `right_max` and so already taller; the lower wall is `left_max`, and the column is settled. Add its water and move `left`. Otherwise the mirror argument settles column `right`. The pointer behind the lower wall always moves, so the two meet on a tallest bar, which holds no water.

```text
3                      #                  # bar   ~ water
2              # ~ ~ ~ # # ~ #
1          # ~ # # ~ # # # # # #
height   0 1 0 2 1 0 1 3 2 1 2 1
water    0 0 1 0 1 2 1 0 0 1 0 0   total 6
by       L L L L L L L · R R R R   (· where the pointers meet)
left right  left_max right_max   settles    water  total
  0   11       0        1        left  0     +0      0
  1   11       1        1        right 11    +0      0
  1   10       1        2        left  1     +0      0
  2   10       1        2        left  2     +1      1
  3   10       2        2        right 10    +0      1
  3    9       2        2        right 9     +1      2
  3    8       2        2        right 8     +0      2
  3    7       2        3        left  3     +0      2
  4    7       2        3        left  4     +1      3
  5    7       2        3        left  5     +2      5
  6    7       2        3        left  6     +1      6
```

```pseudo
FUNCTION Trap(height)
    left ← 0
    right ← len(height) - 1
    left_max ← 0                           // tallest bar in height[0..left]
    right_max ← 0                          // tallest bar in height[right..n-1]
    water ← 0
    WHILE left < right
        left_max ← max(left_max, height[left])
        right_max ← max(right_max, height[right])
        IF left_max < right_max            // right wall taller: settle left
            water ← water + left_max - height[left]
            left ← left + 1
        ELSE                               // left wall as tall: settle right
            water ← water + right_max - height[right]
            right ← right - 1
    RETURN water
```

Each step settles one column, so the scan is `O(n)` time with `O(1)` extra space. Reach for this whenever the answer at a position depends on the extremes on both sides of it: the lower side decides, so the lower side moves. Container With Most Water is the cousin, where the area between two lines is capped by the shorter line and the pointer at the shorter line moves. Trapping Rain Water II lifts the problem onto a grid, where a min-heap of boundary cells plays the lower wall. The classic mistake is adding `left_max - height[left]` before raising `left_max` to include the current bar, which goes negative whenever that bar is a new tallest.

*Practice:* LC 42 Trapping Rain Water · LC 11 Container With Most Water · LC 407 Trapping Rain Water II

```{=latex}
\clearpage
```

## 38. Dutch National Flag {#a38}

```{=latex}
\markright{38. Dutch National Flag}
```

[Three-Way Partition in One Pass · Two Pointers · Tier 2]{.meta}

Given an array that holds only `0`, `1` and `2`, the three colors of the Dutch flag, sort it in place in a single pass with `O(1)` extra space. `[2, 0, 2, 1, 1, 0]` becomes `[0, 0, 1, 1, 2, 2]`.

Counting sort already does it in two passes: count the three values, then overwrite the array. The one-pass idea is to keep the array split into four regions at all times, with three pointers on the borders: `nums[0..low-1]` holds 0s, `nums[low..mid-1]` holds 1s, `nums[mid..high]` is still unseen, and `nums[high+1..n-1]` holds 2s. Each step classifies `nums[mid]`, the first unseen value. A `0` swaps with the first 1 at `low`, which grows the 0s and slides the block of 1s one step right, so `low` and `mid` both advance. A `1` is already in place, so only `mid` advances. A `2` swaps with the last unseen value at `high`, and `high` retreats.

The asymmetry is the whole subtlety. After a `0` swap, the value that comes back from `low` is a 1 that `mid` has already passed, or the 0 itself when there are no 1s yet, so `mid` may move on. After a `2` swap, the value that comes back from `high` has never been looked at, so `mid` must stay and examine it. The unseen middle shrinks by exactly one every step, and when it is empty the flag is sorted.

```text
 0s  │ 1s  │ unseen      │ 2s    low mid high   action
     │     │ 2 0 2 1 1 0 │        0   0    5    2: swap to high, high - 1
     │     │ 0 0 2 1 1   │ 2      0   0    4    0: swap to low, low + 1, mid + 1
 0   │     │ 0 2 1 1     │ 2      1   1    4    0: swap to low, low + 1, mid + 1
 0 0 │     │ 2 1 1       │ 2      2   2    4    2: swap to high, high - 1
 0 0 │     │ 1 1         │ 2 2    2   2    3    1: mid + 1
 0 0 │ 1   │ 1           │ 2 2    2   3    3    1: mid + 1
 0 0 │ 1 1 │             │ 2 2    2   4    3    mid > high: done
```

```pseudo
FUNCTION SortColors(nums)
    low ← 0                                // nums[0..low-1] are 0s
    mid ← 0                                // nums[low..mid-1] are 1s
    high ← len(nums) - 1                   // nums[high+1..n-1] are 2s
    WHILE mid ≤ high                       // nums[mid..high] is still unseen
        IF nums[mid] = 0
            swap(nums[low], nums[mid])
            low ← low + 1
            mid ← mid + 1                  // the block of 1s shifts right
        ELSE IF nums[mid] = 1
            mid ← mid + 1
        ELSE
            swap(nums[mid], nums[high])
            high ← high - 1                // mid stays: this value is unseen
```

The unseen region loses one element per step, so the sort takes exactly `n` steps, `O(n)` time with `O(1)` space and at most one swap per step. This is the three-way partition that rescues quicksort (#12) from repeated pivots: values less than, equal to and greater than the pivot play 0, 1 and 2, and the equal block never needs sorting again. Reach for it whenever an array must be split in place into two or three classes whose inner order does not matter, by parity, by sign or around a pivot; Partition Array According to Given Pivot keeps each class in its original order, which these swaps would scramble, so it fills the regions in separate passes instead. The classic mistake is advancing `mid` after swapping a `2` to the back: on `[1, 2, 0]` the `0` that comes forward is never examined, and the result is `[1, 0, 2]`.

*Practice:* LC 75 Sort Colors · LC 905 Sort Array By Parity · LC 2161 Partition Array According to Given Pivot

```{=latex}
\clearpage
```

## 39. Search in a Rotated Sorted Array {#a39}

```{=latex}
\markright{39. Search in a Rotated Sorted Array}
```

[One Half Is Always Sorted · Binary Search · Tier 2]{.meta}

A sorted array of distinct values was rotated at an unknown pivot, so `[0, 1, 2, 4, 5, 6, 7]` may now read `[6, 7, 0, 1, 2, 4, 5]`. Return the index of a target, or `-1` if it is absent, in `O(log n)` time. In `[6, 7, 0, 1, 2, 4, 5]` the target `0` sits at index `2`.

A linear scan costs `O(n)`. Finding the rotation point first and then binary searching the correct side reaches `O(log n)` in two passes, but one pass is enough. Picture the array as two ascending ramps with a cliff between them. Cut the window at any `mid` and the cliff falls into at most one of the two halves, so the other half is a single ramp, fully sorted. One comparison tells which: if `nums[lo] ≤ nums[mid]`, the left half climbs without a break, because a cliff inside it would leave `nums[mid]` below `nums[lo]`; otherwise the cliff is on the left and the right half is sorted. A sorted half answers "could the target be in here?" with two comparisons against its ends. If the target lies inside its range, search there; if not, it can only be in the other half. Either way half the window disappears, exactly as in plain binary search. The window is the closed `[lo, hi]` of an exact search, since the loop reads `nums[hi]` as a real element.

Two relatives use the same picture. To find the minimum (LC 153), compare `nums[mid]` with `nums[hi]`: if `nums[mid] > nums[hi]`, the cliff and the minimum just after it lie to the right of `mid`, so `lo ← mid + 1`; otherwise `hi ← mid`. With duplicates (LC 81), `nums[lo] = nums[mid] = nums[hi]` hides which half is sorted: `[1, 1, 1, 0, 1]` and `[1, 0, 1, 1, 1]` look identical at those three probes. The safe move is to drop one copy from each end, which makes the worst case `O(n)`.

```text
value
  7        ●                         a cliff after index 1 splits the
  6     ●                            array into two ascending ramps
  5                       ●
  4                    ●
  2                 ●
  1              ●
  0           ●
        0  1  2  3  4  5  6   index

  lo  hi  mid  nums[mid]  sorted half      target 0 in it?   move
   0   6    3       1     right: 1 .. 5    no                hi ← 2
   0   2    1       7     left:  6 .. 7    no                lo ← 2
   2   2    2       0     nums[mid] = target: return 2
```

```pseudo
FUNCTION SearchRotated(nums, target)
    lo ← 0
    hi ← len(nums) - 1                      // closed window [lo, hi]
    WHILE lo ≤ hi
        mid ← floor((lo + hi) / 2)
        IF nums[mid] = target
            RETURN mid
        IF nums[lo] ≤ nums[mid]             // left half is sorted
            IF nums[lo] ≤ target AND target < nums[mid]
                hi ← mid - 1                // target inside the left half
            ELSE
                lo ← mid + 1                // so it must be on the right
        ELSE                                // right half is sorted
            IF nums[mid] < target AND target ≤ nums[hi]
                lo ← mid + 1                // target inside the right half
            ELSE
                hi ← mid - 1                // so it must be on the left
    RETURN -1
```

Each step discards half of the window, so the search takes `O(log n)` time and `O(1)` space. The signals are words like "rotated" or "shifted" next to "sorted", together with a demand for `O(log n)`. The classic mistake is writing `nums[lo] < nums[mid]` instead of `≤`: when the window shrinks to two elements, `lo = mid` and the left half is the single element `nums[mid]`, which is sorted, but the strict test calls the right half sorted instead; on `[3, 1]` with target `1` it discards the `1` and returns `-1`.

*Practice:* LC 33 Search in Rotated Sorted Array · LC 153 Find Minimum in Rotated Sorted Array · LC 81 Search in Rotated Sorted Array II · LC 154 Find Minimum in Rotated Sorted Array II

```{=latex}
\clearpage
```

## 40. Median of Two Sorted Arrays {#a40}

```{=latex}
\markright{40. Median of Two Sorted Arrays}
```

[Binary Search the Partition · Binary Search · Tier 2]{.meta}

Given two sorted arrays `a` and `b` of lengths `m` and `n`, with at least one value between them, return the median of all `m + n` values in `O(log(m + n))` time. For `[1, 3, 8, 9, 15]` and `[7, 11, 18, 19, 21, 25]` the eleven values in order are `1 3 7 8 9 11 15 18 19 21 25`, so the median is `11`; with an even total it is the average of the two middle values.

The brute force merges the two arrays with two pointers up to the middle, `O(m + n)`. The logarithmic idea stops thinking about positions in the merged array and thinks about one cut through both arrays. The median splits all values into a left part of `half = ⌊(m + n + 1) / 2⌋` values and a right part, with every left value at most every right value. If the cut takes `i` values from `a`, it must take `j = half - i` from `b`, so the single number `i` describes the whole split. Each array is sorted on its own, so the cut is valid exactly when the two cross pairs agree: `a[i-1] ≤ b[j]` and `b[j-1] ≤ a[i]`, reading a missing neighbor at an edge as `-∞` or `∞`. The same tests say which way to move. When `a[i-1] > b[j]`, `a` gave too many values to the left and `i` must shrink; when `b[j-1] > a[i]`, it gave too few and `i` must grow. That is a binary search over `i` in `[0, m]`.

Search the shorter array: then `j = half - i` stays inside `[0, n]` for every `i`, which a cut through the longer array cannot promise. At the valid cut the median is the largest left value when the total is odd, because the left part holds the extra value, and the average of the largest left value and the smallest right value when the total is even.

```text
m = 5, n = 6, half = ⌊(5 + 6 + 1) / 2⌋ = 6 values in the left part
                   left │ right
step 1   lo = 0, hi = 5, i = 2, j = 4
   a:             1   3 │  8   9  15
   b:     7  11  18  19 │ 21  25
   a_left 3 ≤ b_right 21 ✓    b_left 19 ≤ a_right 8 ✗    → lo ← 3
step 2   lo = 3, hi = 5, i = 4, j = 2
   a:     1   3   8   9 │ 15
   b:             7  11 │ 18  19  21  25
   a_left 9 ≤ b_right 18 ✓    b_left 11 ≤ a_right 15 ✓   → valid cut
   11 values, odd: median = max(a_left, b_left) = max(9, 11) = 11
```

```pseudo
FUNCTION ValueAt(arr, k)                // -∞ before the start, ∞ past the end
    IF k < 0
        RETURN -∞
    IF k ≥ len(arr)
        RETURN ∞
    RETURN arr[k]

FUNCTION FindMedian(a, b)
    IF len(a) > len(b)
        swap(a, b)                      // search the shorter array
    m ← len(a)
    n ← len(b)
    half ← floor((m + n + 1) / 2)       // size of the left part
    lo ← 0
    hi ← m
    WHILE lo ≤ hi
        i ← floor((lo + hi) / 2)        // a[0..i-1] goes to the left part
        j ← half - i                    // b[0..j-1] fills the rest of it
        a_left ← ValueAt(a, i - 1)
        a_right ← ValueAt(a, i)
        b_left ← ValueAt(b, j - 1)
        b_right ← ValueAt(b, j)
        IF a_left ≤ b_right AND b_left ≤ a_right    // every left ≤ right
            IF (m + n) mod 2 = 1
                RETURN max(a_left, b_left)
            RETURN (max(a_left, b_left) + min(a_right, b_right)) / 2
        IF a_left > b_right
            hi ← i - 1                  // too much of a on the left
        ELSE
            lo ← i + 1                  // too little of a on the left
```

The range of `i` halves at every step, so the search costs `O(log min(m, n))` time and `O(1)` space, even better than the `O(log(m + n))` the problem demands. The signal is a median or a k-th smallest value across two sorted arrays under a logarithmic bound; across many sorted arrays, binary search on the value instead (#73). The classic mistakes are searching the longer array, which pushes `j` below `0` or past `n`, and dropping the infinities, which crashes or misjudges every cut at an edge, such as `i = 0` when all of `a` belongs on the right.

*Practice:* LC 4 Median of Two Sorted Arrays · LC 88 Merge Sorted Array · LC 295 Find Median from Data Stream

```{=latex}
\clearpage
```

## 41. Heapify {#a41}

```{=latex}
\markright{41. Heapify}
```

[Build a Heap in O(n) with Sift-Down · Heaps · Tier 2]{.meta}

Rearrange an array in place into a min-heap: a complete binary tree stored level by level, in which every parent is at most its children. The children of index `i` sit at `2i + 1` and `2i + 2`, and its parent at `floor((i - 1) / 2)`. `[9, 5, 6, 2, 3, 7, 1]` becomes `[1, 2, 6, 5, 3, 7, 9]`. Then push and pop on that heap by hand.

Pushing the n values one at a time builds a heap in `O(n log n)`. Heapify builds it in `O(n)` by working from the bottom up with sift-down. A node whose two subtrees are already heaps is repaired by swapping it with its smaller child until neither child is smaller, and then its whole subtree is a heap. Leaves are heaps of one value, so start at the last parent, `floor(n / 2) - 1`, and walk back to the root: every node is sifted after both of its subtrees, so they are heaps by the time its turn comes.

A sift-down costs at most the height of its node, the distance to the bottom, and most nodes live near the bottom. Half of them are leaves and cost nothing, a quarter sit one level up and cost at most one swap, an eighth cost at most two, and the sum `n/4 · 1 + n/8 · 2 + n/16 · 3 + …` stays below n. Building by pushes uses sift-up, whose cost is the depth instead, the distance to the top, and the deep nodes are the many: that is where the extra `log n` comes from.

```text
     start            i = 2            i = 1            i = 0
       9                9                9                1
   5       6        5       1        2       1        2       6
 2   3   7   1    2   3   7   6    5   3   7   6    5   3   7   9
[9 5 6 2 3 7 1]  [9 5 1 2 3 7 6]  [9 2 1 5 3 7 6]  [1 2 6 5 3 7 9]
                 6 swaps with 1   5 swaps with 2   9 sinks 2 levels
```

```pseudo
FUNCTION SiftDown(heap, i, n)              // heap[0..n-1] is the heap
    WHILE true
        smallest ← i
        left ← 2 * i + 1
        right ← 2 * i + 2
        IF left < n AND heap[left] < heap[smallest]
            smallest ← left
        IF right < n AND heap[right] < heap[smallest]
            smallest ← right
        IF smallest = i                    // no child is smaller: done
            RETURN
        swap(heap[i], heap[smallest])
        i ← smallest

FUNCTION Heapify(heap)
    n ← len(heap)
    FOR i FROM floor(n / 2) - 1 DOWNTO 0   // last parent, back to the root
        SiftDown(heap, i, n)

FUNCTION SiftUp(heap, i)
    WHILE i > 0
        parent ← floor((i - 1) / 2)
        IF heap[parent] ≤ heap[i]          // the parent is no larger: done
            RETURN
        swap(heap[i], heap[parent])
        i ← parent

FUNCTION HeapPush(heap, value)
    heap.append(value)
    SiftUp(heap, len(heap) - 1)

FUNCTION HeapPop(heap)
    last ← len(heap) - 1
    swap(heap[0], heap[last])
    top ← heap.removeLast()                // remove the last slot: the old root
    SiftDown(heap, 0, len(heap))
    RETURN top
```

Heapify takes `O(n)` time and `O(1)` extra space; push and pop take `O(log n)`, the height of the tree. Push appends the value as the last leaf and sifts it up, swapping with its parent while it is smaller. Pop swaps the root with the last leaf, removes that last slot, which now holds the old minimum, and sifts the new root down. Every heap in this book rests on these two moves, from Top-K (#13) to Heap Sort (#75), which runs the same build as a max-heap. Reach for heapify when all the values are present at the start: Last Stone Weight heapifies the stones once and then only pops and pushes. The classic mistake is running `i` upward from the root instead of backward from the last parent: the root is sifted before its subtrees are heaps, and the example ends as `[5, 2, 1, 9, 3, 7, 6]`, with 5 sitting above 1.

*Practice:* LC 912 Sort an Array · LC 215 Kth Largest Element in an Array · LC 1046 Last Stone Weight

```{=latex}
\clearpage
```

## 42. Quickselect {#a42}

```{=latex}
\markright{42. Quickselect}
```

[Kth Largest in Expected O(n) · Heaps · Tier 2]{.meta}

Find the kth largest value of an unsorted array, where duplicates count as separate values. In `[3, 2, 1, 5, 6, 4]` with `k = 2` the answer is `5`.

Sorting finds it in `O(n log n)`, and the size-k heap of #13 in `O(n log k)`. Quickselect reaches expected `O(n)` with one fact about the partition of Quick Sort (#12): after partitioning, the pivot sits at its final sorted index `p`, with only smaller values to its left. In ascending order the kth largest lives at index `target = n - k`. If `p = target`, the pivot is the answer. If `p < target`, the answer lies to the right of the pivot and everything from `lo` to `p` can be forgotten; if `p > target`, it lies to the left. Quick sort recurses into both sides; quickselect keeps only one, so it needs no recursion at all, just a loop that narrows the window `[lo, hi]`.

Picture the window closing in on index `target`, which never leaves it. With distinct values, a random pivot lands in the middle half of the window half of the time, and such a pivot cuts the window to at most three quarters of its size. So it takes two rounds on average to shrink the window by a quarter, and the expected work is at most twice the geometric series `n + 3n/4 + 9n/16 + …`, that is at most 8n.

```text
k = 2, n = 6, so the answer sits at index target = 6 - 2 = 4
one run; the pivots are random picks
  window   pivot   nums after partitioning the window   p   next
  [0, 5]     2     [1 2 3 5 6 4]                         1   1 < 4: lo ← 2
  [2, 5]     6      1 2 [3 5 4 6]                        5   5 > 4: hi ← 4
  [2, 4]     5      1 2 [3 4 5] 6                        4   4 = 4: return 5
```

```pseudo
FUNCTION Partition(nums, lo, hi)
    pick ← RandomInt(lo, hi)            // lo ≤ pick ≤ hi
    swap(nums[pick], nums[hi])          // park the pivot at the end
    pivot ← nums[hi]
    store ← lo                          // invariant: nums[lo..store-1] < pivot
    FOR i FROM lo TO hi - 1
        IF nums[i] < pivot              // a small value joins the left region
            swap(nums[store], nums[i])
            store ← store + 1
    swap(nums[store], nums[hi])         // pivot between the regions
    RETURN store

FUNCTION KthLargest(nums, k)
    target ← len(nums) - k              // the answer's index in sorted order
    lo ← 0
    hi ← len(nums) - 1
    WHILE true
        p ← Partition(nums, lo, hi)
        IF p = target
            RETURN nums[p]
        ELSE IF p < target
            lo ← p + 1                  // the answer is right of the pivot
        ELSE
            hi ← p - 1                  // the answer is left of the pivot
```

On distinct values the expected time is `O(n)` and the extra space `O(1)`; a run of unlucky pivots still costs `O(n²)`. Against the heap of #13, quickselect is faster on average but reorders the input, needs all of it in memory and keeps that quadratic tail; the heap works on a stream at `O(n log k)` every time. Signals: kth largest or smallest, k closest, top k in any order, since when the loop stops `nums[target..n-1]` holds the k largest values, unsorted, just as aiming at index `k - 1` leaves the k smallest in `nums[0..k-1]`; that is how it answers K Closest Points to Origin on squared distances and Top K Frequent Elements on counts. Many equal values are its weak spot: they all land on one side of the `<` test, so an array of identical values goes quadratic unless k is close to n; the three-way partition of #38 groups them in the middle and stops as soon as the target falls among them. The classic mistake is aiming at index `k - 1`, which finds the kth smallest: on the example it returns 2 instead of 5.

*Practice:* LC 215 Kth Largest Element in an Array · LC 973 K Closest Points to Origin · LC 347 Top K Frequent Elements

```{=latex}
\clearpage
```

## 43. Bucket Sort {#a43}

```{=latex}
\markright{43. Bucket Sort}
```

[Top K Frequent by Frequency Buckets · Sorting · Tier 2]{.meta}

Given an array and an integer `k`, return the `k` most frequent values in any order; the answer is guaranteed to be unique. In `[1, 1, 1, 2, 2, 3]` with `k = 2` the answer is `[1, 2]`.

Counting the frequencies with a map is the easy part. Ordering the distinct values by count with a sort costs `O(d log d)` for d distinct values, and the size-k heap of #13 costs `O(d log k)`. Bucket sort removes the comparisons altogether: a frequency is a whole number between 1 and n, so it can serve directly as an array index. Make `n + 1` empty buckets, drop each distinct value into `buckets[count[value]]`, and walk the buckets from n down to 1, collecting values until k of them are in hand. The bucket index already is the order, so nothing inside a bucket needs sorting.

Picture a shelf with one slot per possible frequency. Every distinct value lands in the slot of its own count, and reading the shelf from the right end reads the values from most to least frequent.

```text
nums = [1, 1, 1, 2, 2, 3], k = 2      count = {1: 3, 2: 2, 3: 1}
  freq      0     1     2     3     4     5     6
  bucket   [ ]   [3]   [2]   [1]   [ ]   [ ]   [ ]
           ←────────────────────────────────────── read from freq 6 down
  freq 6, 5, 4: empty
  freq 3: take 1      result [1]
  freq 2: take 2      result [1, 2]      k values: return
```

```pseudo
FUNCTION TopKFrequent(nums, k)
    count ← empty map                       // value → frequency
    FOR EACH value IN nums
        count[value] ← count.get(value, 0) + 1
    buckets ← empty list                    // index = frequency
    FOR freq FROM 0 TO len(nums)            // a frequency is at most n
        buckets.append(empty list)
    FOR EACH value IN count
        buckets[count[value]].append(value)
    result ← empty list
    FOR freq FROM len(nums) DOWNTO 1        // most frequent first
        FOR EACH value IN buckets[freq]
            result.append(value)
            IF len(result) = k
                RETURN result
    RETURN result
```

Counting takes `O(n)`, filling the buckets `O(d)`, and the walk visits at most `n + 1` buckets and takes k values, so the whole job is `O(n)` time and `O(n)` space. Signals: top k frequent, sort by frequency, and in general any sort key that is a small whole number bounded by n. General bucket sort spreads values over equal-width ranges instead of exact keys: n numbers spread evenly over `[low, high)` go into n buckets of width `(high - low) / n`, each bucket catches about one value, a tiny sort inside each bucket is cheap, and reading the buckets in order gives the sorted array in expected `O(n)`. Maximum Gap (LC 164) uses such buckets for a pigeonhole argument: the largest gap between sorted neighbors is at least the average gap `(max - min) / (n - 1)`, so with buckets no wider than that it never falls inside one bucket, and only each bucket's minimum and maximum matter. The classic mistake is making n buckets instead of `n + 1`: when one value fills the whole array, as in `[7, 7, 7]`, its frequency is 3 and `buckets[3]` does not exist.

*Practice:* LC 347 Top K Frequent Elements · LC 451 Sort Characters By Frequency · LC 692 Top K Frequent Words · LC 164 Maximum Gap

```{=latex}
\clearpage
```

## 44. Largest Rectangle in Histogram {#a44}

```{=latex}
\markright{44. Largest Rectangle in Histogram}
```

[Monotonic Increasing Stack · Stacks · Tier 2]{.meta}

Given the heights of a histogram whose bars all have width 1, return the area of the largest rectangle that fits inside it. For `[2, 1, 5, 6, 2, 3]` the answer is 10: the bars 5 and 6 together hold a rectangle of height 5 and width 2.

The brute force tries every pair of left and right edges while carrying the minimum height between them, `O(n²)`. Look at it per bar instead. The widest rectangle at exactly one bar's height spreads left and right until it meets a lower bar on each side, so every bar needs its nearest lower neighbor on both sides, and the monotonic stack of #17 finds both in a single pass. Keep a stack of indices whose heights never fall from bottom to top. When bar `i` arrives lower than the top, the top's rectangle stops at `i - 1`, since every bar between them is at least as tall or it would have popped the top sooner. Pop it and measure. Its left edge sits just right of the new top, because every bar between those two was popped earlier, and only by a lower bar, so all of them are taller than the bar being measured. The area is the height times `i - left`, and the best area wins.

Two details complete the loop. A 0 appended to the heights is lower than every bar of positive height, so at the end it pops each of them still on the stack and measures it against the right edge of the histogram. When a pop empties the stack, nothing lower lies to the left, and the rectangle reaches index 0. Equal heights may stand side by side; the leftmost of them is popped last and measures the full width.

```text
 6           #               # = bar, ● = the largest rectangle,
 5        ●  ●               height 5 × width 2 = 10
 4        ●  ●
 3        ●  ●     #
 2  #     ●  ●  #  #
 1  #  #  ●  ●  #  #
    2  1  5  6  2  3   + sentinel 0 at index 6

 i  bar   pops: height × width               stack after (index:height)
 0   2    -                                  0:2
 1   1    2 × 1 = 2                          1:1
 2   5    -                                  1:1  2:5
 3   6    -                                  1:1  2:5  3:6
 4   2    6 × 1 = 6, 5 × 2 = 10              1:1  4:2
 5   3    -                                  1:1  4:2  5:3
 6   0    3 × 1 = 3, 2 × 4 = 8, 1 × 6 = 6    6:0
```

```pseudo
FUNCTION LargestRectangleArea(heights)
    bars ← heights + [0]                // the 0 sentinel flushes the stack
    stack ← empty stack                 // indices; heights never fall
    best ← 0
    FOR i FROM 0 TO len(bars) - 1
        WHILE len(stack) > 0 AND bars[stack.top()] > bars[i]
            height ← bars[stack.pop()]          // its rectangle ends at i - 1
            IF len(stack) > 0
                left ← stack.top() + 1          // just right of the new top
            ELSE
                left ← 0                        // empty stack: reaches index 0
            width ← i - left
            best ← max(best, height * width)
        stack.push(i)
    RETURN best
```

Each index is pushed once and popped at most once, so the run is `O(n)` time with `O(n)` space for the stack. The signal is a largest rectangle, or any "minimum times width" score, over contiguous bars or subarrays. Maximal Rectangle in a binary matrix reduces to this: treat each row as the floor of a histogram whose heights count the consecutive 1s running up from it, and run this loop once per row, `O(rows × cols)` in all. Maximum Score of a Good Subarray is the same rectangle with the extra rule that it must cover index `k`. The classic mistakes are measuring the width as `i - j` from the popped index `j` instead of from the new top, which ignores the taller bars popped earlier on the left and returns 3 instead of 4 for `[1, 3, 2]`, and forgetting the sentinel, which leaves a rising histogram such as `[1, 2, 3]` unmeasured on the stack and returns 0 instead of 4.

*Practice:* LC 84 Largest Rectangle in Histogram · LC 85 Maximal Rectangle · LC 1793 Maximum Score of a Good Subarray

```{=latex}
\clearpage
```

## 45. Basic Calculator {#a45}

```{=latex}
\markright{45. Basic Calculator}
```

[Evaluate + - \* / and Parentheses with a Stack · Stacks · Tier 2]{.meta}

Evaluate a valid expression made of non-negative integers, the operators `+ - * /`, parentheses and spaces, with the usual precedence. Division truncates toward zero, and a minus sign may also open the expression or a group, as in `-(2 + 3)`. For `"2*(3+4)-10/3"` the answer is 11: the group gives 7, `2 * 7 = 14`, and `10 / 3` truncates to 3.

Precedence looks like it needs a parser, but one level of an expression without parentheses is just a sum of signed terms, and a stack of those terms evaluates it in one pass. Read each number and remember the operator in front of it. When the next operator, a `)` or the end of the string finishes the number, fold it in by that remembered operator: after `+` push it, after `-` push its negation, after `*` or `/` pop the top term, combine it with the number and push the result back. Multiplication and division reach back exactly one term, because the terms on the stack are separated by `+` and `-`, which bind more loosely. When the level ends, its value is the sum of the stack.

Parentheses are recursion. Seen from outside, a group is a single number, so on `(` the function calls itself on the text that follows. The call evaluates that level with its own stack and returns the group's value and the index just past its `)`, where the caller resumes as if it had read one long number. A leading minus needs no special case: `op` starts as `+` and `num` as 0, so the minus in `-(2 + 3)` finishes an invisible 0, and the group's 5 then arrives behind a `-`, giving `0 - 5`.

```text
s = "2*(3+4)-10/3"     (indices 0 to 11)

level 0   '*' ends 2     op in front +   push 2              stack [2]
level 0   '(' at 2       recurse from index 3
level 1     '+' ends 3   op in front +   push 3              stack [3]
level 1     ')' ends 4   op in front +   push 4              stack [3, 4]
level 1     return (3 + 4, 7): value 7, resume at index 7
level 0   '-' ends 7     op in front *   top 2 * 7 = 14      stack [14]
level 0   '/' ends 10    op in front -   push -10            stack [14, -10]
level 0   end ends 3     op in front /   top -10 / 3 = -3    stack [14, -3]
level 0   return 14 + (-3) = 11
```

```pseudo
FUNCTION Calculate(s)
    value, end ← Evaluate(s, 0)
    RETURN value

FUNCTION Evaluate(s, i)             // returns (value, next index to read)
    stack ← empty stack             // signed terms of this level; value = sum
    num ← 0
    op ← '+'                        // the operator in front of num
    WHILE i < len(s)
        ch ← s[i]
        i ← i + 1
        IF ch is a digit
            num ← num * 10 + int(ch)
        ELSE IF ch = '('
            num, i ← Evaluate(s, i)         // a whole group acts as one number
        ELSE IF ch IN "+-*/)"
            ApplyOp(stack, op, num)
            IF ch = ')'
                RETURN (sum(stack), i)
            op ← ch
            num ← 0
    ApplyOp(stack, op, num)
    RETURN (sum(stack), i)

FUNCTION ApplyOp(stack, op, num)
    IF op = '+'
        stack.push(num)
    ELSE IF op = '-'
        stack.push(-num)
    ELSE IF op = '*'
        stack.push(stack.pop() * num)       // * reaches back one term only
    ELSE
        stack.push(truncate(stack.pop() / num))     // toward zero
```

Every character is read once, by the level that owns it, so the run is `O(n)` time, and the stacks plus the recursion hold `O(n)` at worst. Reach for this whenever a string encodes arithmetic or other nesting to resolve from the inside out. Basic Calculator II is one level without parentheses, the stack alone; the original Basic Calculator has only `+ - ( )`, and Basic Calculator III has everything, as here. The recursion is as deep as the nesting, so the original problem is often solved iteratively instead, pushing the running total and sign at `(` and popping them at `)`. Evaluate Reverse Polish Notation is the same stack with precedence already settled by the notation: push numbers and let each operator pop two. The classic mistake is Python's `//`, which rounds toward negative infinity: `-10 // 3` is -4 and turns the example's 11 into 10, while `int(-10 / 3)` truncates to -3. The other is folding a number only when an operator arrives, which loses the last number of the string and the one just before each `)`.

*Practice:* LC 224 Basic Calculator · LC 227 Basic Calculator II · LC 772 Basic Calculator III · LC 150 Evaluate Reverse Polish Notation

```{=latex}
\clearpage
```

## 46. Sliding Window Maximum {#a46}

```{=latex}
\markright{46. Sliding Window Maximum}
```

[Monotonic Deque · Queues · Tier 2]{.meta}

Given an array and a window size `k`, return the maximum of every window of `k` consecutive values as the window slides one step at a time from left to right. For `[9, 7, 8, 3, 2, 5, 1]` and `k = 3` the windows are `[9, 7, 8]`, `[7, 8, 3]`, `[8, 3, 2]`, `[3, 2, 5]` and `[2, 5, 1]`, so the answer is `[9, 8, 8, 5, 5]`.

The brute force rescans every window, `O(n · k)`, and a max-heap that lazily discards expired indices still pays `O(n log n)`. The linear solution rests on one observation: when a new value arrives, every older value in the window that it matches or beats is never needed again, because the newcomer is at least as large and stays in the window longer. Throw those losers away and the survivors, read from oldest to newest, form a strictly decreasing staircase of candidates. Keep their indices in a deque. The newcomer enters at the back after popping every value at the back that is no larger than itself. The oldest survivor sits at the front and is the largest, so it is the window's maximum, unless its index has slid out of the window, in which case it leaves through the front.

Each index is pushed once and popped at most once, from one end or the other, so the total work is `O(n)` even though a single step may pop several values. The deque stores indices rather than values because the index is what tells the front that it has expired.

```text
k = 3; the deque holds index:value, front on the left
  i   nums[i]   popped from back   popped from front   deque after     max
  0      9                                             [0:9]
  1      7                                             [0:9 1:7]
  2      8      1:7                                    [0:9 2:8]        9
  3      3                         0:9 (expired)       [2:8 3:3]        8
  4      2                                             [2:8 3:3 4:2]    8
  5      5      4:2 3:3            2:8 (expired)       [5:5]            5
  6      1                                             [5:5 6:1]        5
```

```pseudo
FUNCTION MaxSlidingWindow(nums, k)
    window ← empty deque                 // indices of the candidates
    result ← empty list
    FOR i FROM 0 TO len(nums) - 1
        WHILE len(window) > 0 AND nums[window.back()] ≤ nums[i]
            window.pop_back()            // older and no larger: never needed
        window.push_back(i)
        IF window.front() ≤ i - k
            window.pop_front()           // the front slid out of the window
        IF i ≥ k - 1
            result.append(nums[window.front()])   // front is the window max
    RETURN result
```

The cost is `O(n)` time and `O(k)` space for the deque, plus the output. The signals are a window that slides while its maximum or minimum is needed, and dynamic programming whose next state takes the best of the last `k` states, as in Jump Game VI; for a minimum, flip the comparison so the staircase climbs instead. It is the monotonic stack of #17 with a second exit at the front. The classic mistakes are storing values instead of indices, which leaves the front no way to know that it has expired, and popping the back with `IF` instead of `WHILE`: a large newcomer must clear every smaller value, or on `[3, 1, 2, 5]` with `k = 4` the `3` stays in front of the larger `5` and is reported instead of it.

*Practice:* LC 239 Sliding Window Maximum · LC 1438 Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit · LC 862 Shortest Subarray with Sum at Least K · LC 1696 Jump Game VI

```{=latex}
\clearpage
```

## 47. Jump Game {#a47}

```{=latex}
\markright{47. Jump Game}
```

[Track the Farthest Reach · Greedy · Tier 2]{.meta}

Each `nums[i]` is the longest jump allowed from index `i`, and any shorter jump is allowed too. Starting at index `0`, decide whether the last index can be reached. `[2, 3, 1, 1, 4]` can be crossed, one step to index 1 and then three to the end, while `[3, 2, 1, 0, 4]` cannot, because every path lands on the `0` at index 3.

The brute force explores jump sequences, exponentially many by plain recursion, or `O(n²)` with a reachable flag per index. The insight is that the reachable indices always form one solid block `[0, farthest]`: whoever can stand on `i` can also stand on every index from `i` to `i + nums[i]`, and those stretches overlap into a single interval. So the whole state is one number. Scan left to right while `i` stays inside the block, stretch the block to `i + nums[i]`, and answer yes the moment it covers the last index. If the scan steps past `farthest`, index `i` is unreachable, and so is everything beyond it, since no reachable index jumps that far.

Picture every index casting a shadow forward over the spots it can jump to. The walk begins under the shadow of index 0, and every index under the shadow extends it with its own, so the reachable region grows as one bar. A zero inside the bar is harmless while some earlier shadow passes over it; it becomes a wall only when no shadow reaches beyond it, which is exactly what happens at index 3 below.

```text
nums = [2, 3, 1, 1, 4]          index   0   1   2   3   4
  i = 0 reaches 2, farthest = 2         ●───────┤
  i = 1 reaches 4, farthest = 4             ●───────────┤   4 ≥ 4: true ✓
nums = [3, 2, 1, 0, 4]          index   0   1   2   3   4
  i = 0 reaches 3, farthest = 3         ●───────────┤
  i = 1 reaches 3, farthest = 3             ●───────┤
  i = 2 reaches 3, farthest = 3                 ●───┤
  i = 3 reaches 3, farthest = 3                     ●
  i = 4 > farthest = 3: the loop ends, false ✗
```

```pseudo
FUNCTION CanJump(nums)
    farthest ← 0                           // indices 0..farthest are reachable
    i ← 0
    WHILE i ≤ farthest                     // i is a spot we can really stand on
        farthest ← max(farthest, i + nums[i])
        IF farthest ≥ len(nums) - 1        // the reach covers the last index
            RETURN true
        i ← i + 1
    RETURN false                           // walked past the reach: a wall
```

Each index is visited at most once with constant work, so the scan costs `O(n)` time and `O(1)` space. Reach for the farthest reach whenever moves go forward along a line and every spot up to a move's length is a legal landing: reachability collapses to one number. When jumps are exact, as in Jump Game III (LC 1306) where index `i` leads only to `i + arr[i]` and `i - arr[i]`, the block argument fails and the problem becomes a graph search over indices, the BFS of #30. Counting the fewest jumps is #48, which reads this same scan level by level. The classic mistake is dropping the `i ≤ farthest` guard and scanning every index: on `[3, 2, 1, 0, 4]` the scan then reads index 4, where it can never stand, stretches the reach to `8` and wrongly answers true.

*Practice:* LC 55 Jump Game · LC 45 Jump Game II · LC 1306 Jump Game III

```{=latex}
\clearpage
```

## 48. Jump Game II {#a48}

```{=latex}
\markright{48. Jump Game II}
```

[Greedy BFS over Reach Levels · Greedy · Tier 2]{.meta}

`nums[i]` is again the longest jump allowed from index `i`, and this time the last index is known to be reachable. Return the fewest jumps from index 0 to the last index. For `[2, 3, 1, 1, 4]` the answer is `2`: one step to index 1, then three steps to the end.

Fewest moves in an unweighted graph is BFS (#30), and the brute force runs it literally, enqueuing every index each jump can land on, `O(n²)` edges in the worst case. The insight is that every BFS level here is a contiguous interval. Level 0 is `[0, 0]`, and if level `k` ends at `b`, level `k + 1` is `[b + 1, farthest]`, where `farthest` is the largest `i + nums[i]` seen so far, because every spot up to a reach is a legal landing. So the queue collapses to two numbers: `current_end`, the right edge of the level being scanned, and `farthest`, the right edge of the next one. Walk `i` forward, pushing `farthest` out; when `i` reaches `current_end`, the level is used up, so count one more jump and move `current_end` to `farthest`.

Picture the indices tiled into consecutive bands, each band one jump farther from the start than the band before it. The scan reads each band once, measuring how far its best launcher reaches, and that reach is where the next band ends. The answer is the level number of the band that holds the last index. The loop stops just before the last index, because standing there needs no further jump.

```text
index        0    1    2    3    4
nums         2    3    1    1    4
level 0      ●                              [0, 0]  the start
level 1           ●────●                    [1, 2]  up to 0 + 2 = 2
level 2                     ●────●          [3, 4]  up to max(1 + 3, 2 + 1) = 4

  i   i + nums[i]   farthest   i = current_end?   jumps   current_end
  0        2            2         yes, jump         1          2
  1        4            4         no                1          2
  2        3            4         yes, jump         2          4
  3        4            4         no                2          4
  the loop stops before index 4: 2 jumps
```

```pseudo
FUNCTION MinJumps(nums)
    jumps ← 0
    current_end ← 0                        // right edge of the current level
    farthest ← 0                           // right edge of the next level
    FOR i FROM 0 TO len(nums) - 2          // never jump from the last index
        farthest ← max(farthest, i + nums[i])
        IF i = current_end                 // this level is used up
            jumps ← jumps + 1
            current_end ← farthest         // the next level ends here
    RETURN jumps
```

Every index is read once, so the cost is `O(n)` time and `O(1)` space, against `O(n²)` for the explicit BFS. Reach for this level-by-interval BFS whenever the positions reachable in `k` steps always form a contiguous range: covering a line with jumps, with video clips (LC 1024) or with garden taps (LC 1326), once each clip or tap is recorded as a reach from its left end. When the end might be unreachable, check at the end of each level whether `farthest` is still `i`; if so, nothing beyond can be reached, so return `-1`. The classic mistake is letting the loop run over the last index too: when the last index closes a level, the scan counts a jump it never takes, and `[2, 3, 1, 1, 4]` reports `3`.

*Practice:* LC 45 Jump Game II · LC 1024 Video Stitching · LC 1326 Minimum Number of Taps to Open to Water a Garden

```{=latex}
\clearpage
```

## 49. Gas Station {#a49}

```{=latex}
\markright{49. Gas Station}
```

[Restart After Every Deficit · Greedy · Tier 2]{.meta}

Stations sit on a circle. Station `i` gives `gas[i]` fuel, and the drive on to the next station burns `cost[i]`. Starting with an empty tank, return the station from which a full lap is possible, or `-1` if there is none; the input promises at most one such station. With `gas = [4, 1, 2, 5, 1]` and `cost = [3, 3, 3, 1, 2]` the answer is `3`.

The brute force simulates a lap from every station, `O(n²)`. Two facts make one pass enough. First, a lap exists exactly when the total gas covers the total cost, so `sum(gas) < sum(cost)` answers `-1` at once. Second, a failed attempt rules out a whole stretch, not just its first station. Say the tank, started empty at `start`, first runs dry on the drive out of station `i`. Every station `k` in between was reached from `start` with a non-negative tank, because no deficit had happened yet. Starting fresh at `k` means arriving there with an empty tank instead, which is never better, so that attempt also runs dry by station `i`. Every station from `start` to `i` is out, and the next candidate is `i + 1`, with the tank reset to zero.

Picture the running sum of `gas[i] - cost[i]` as a profile over the stations, the bottom row of the picture. A car that starts at station `s` carries exactly the profile's rise since the point just before `s`, so starting right after the lowest point keeps the tank non-negative all the way to the end of the array. Past the wrap, the profile repeats lifted by the total, which is non-negative, so the tank stays non-negative there too. Each deficit in the scan is the profile hitting a new low, and moving `start` to `i + 1` simply follows the low point down.

```text
gas  = [4, 1, 2, 5, 1]   sum 13
cost = [3, 3, 3, 1, 2]   sum 12   13 ≥ 12, so a lap exists

  i   gas - cost   tank   start
  0       1           1     0
  1      -2          -1     0 → 2     deficit: stations 0 and 1 are out
  2      -1          -1     2 → 3     deficit: station 2 is out
  3       4           4     3
  4      -1           3     3         answer 3

running sum   1  -1  -2   2   1
                      ▲ lowest, after station 2: start at 3
```

```pseudo
FUNCTION CanCompleteCircuit(gas, cost)
    IF sum(gas) < sum(cost)                // not enough fuel for any lap
        RETURN -1
    start ← 0
    tank ← 0                               // fuel left since leaving start
    FOR i FROM 0 TO len(gas) - 1
        tank ← tank + gas[i] - cost[i]
        IF tank < 0                        // stranded: start..i are all out
            start ← i + 1
            tank ← 0
    RETURN start
```

One pass plus the two sums gives `O(n)` time and `O(1)` space. Reach for this pattern when a running balance around a loop or along a route must never go negative and the question is where to begin: the answer sits right after the lowest point of the prefix sums. It is the restart of Kadane's algorithm (#20) in another costume, where a run that turned negative is dropped whole. The classic mistake is trusting the scan without the total check: for `gas = [2, 3, 4]` and `cost = [3, 4, 3]` the scan ends on station 2 with fuel to spare, yet no lap is possible, because the total gas `9` is less than the total cost `10`.

*Practice:* LC 134 Gas Station · LC 1413 Minimum Value to Get Positive Step by Step Sum · LC 918 Maximum Sum Circular Subarray

```{=latex}
\clearpage
```

## 50. Interval Scheduling {#a50}

```{=latex}
\markright{50. Interval Scheduling}
```

[Sort by End, Keep What Fits · Greedy · Tier 2]{.meta}

Given intervals `[start, end]` with `start < end`, keep as many as possible so that no two overlap; ends that only touch, such as `[1, 3]` and `[3, 5]`, do not count as overlapping. The fewest removals that leave the rest non-overlapping is then everything not kept. From `[[1, 3], [2, 4], [3, 5], [1, 8], [6, 7]]` three can stay, `[1, 3]`, `[3, 5]` and `[6, 7]`, so two must go.

The brute force tries every subset, `O(2^n)` of them. The greedy question is which interval to keep first, and the answer is the one that ends earliest, because it leaves the most room for everything after it. Sort by end, then sweep once: keep an interval if it starts at or after `last_end`, the end of the last kept one, and skip it otherwise. Merge Intervals (#18) sorts by start because it wants to glue overlaps together; scheduling sorts by end because it wants to leave room.

The exchange argument shows that the earliest end is a safe first choice. Take any optimal selection and its first interval by end. The earliest-ending interval overall ends no later, so swapping it in keeps every other chosen interval compatible: each of them starts at or after the old first one's end, hence at or after the new one's end too. The optimum keeps its size and now begins with the greedy choice, and the same argument repeats on the intervals that start after it. On the timeline, `last_end` is a finish line that only moves right, and each kept interval pushes it as little as possible.

```text
sorted by end    1   2   3   4   5   6   7   8
[1, 3]           ├───────┤                       keep, last_end = 3
[2, 4]               ├───────┤                   drop, 2 < 3
[3, 5]                   ├───────┤               keep, 3 ≥ 3, last_end = 5
[6, 7]                               ├───┤       keep, 6 ≥ 5, last_end = 7
[1, 8]           ├───────────────────────────┤   drop, 1 < 7
kept 3, removed 2
```

```pseudo
FUNCTION MaxNonOverlapping(intervals)
    by_end ← empty list
    FOR EACH (start, end) IN intervals
        by_end.append((end, start))        // end first: the sort orders by end
    by_end.sort()
    kept ← 0
    last_end ← -∞                          // end of the last kept interval
    FOR EACH (end, start) IN by_end
        IF start ≥ last_end                // fits after the last kept one
            kept ← kept + 1
            last_end ← end
    RETURN kept

FUNCTION MinRemovals(intervals)            // LC 435
    RETURN len(intervals) - MaxNonOverlapping(intervals)
```

Sorting costs `O(n log n)` and the sweep `O(n)`, plus `O(n)` space for the sorted copy. Reach for the earliest end when a problem asks for the most non-overlapping intervals, the fewest removals to get there (LC 435), the longest chain of pairs (LC 646) or the fewest arrows that burst every balloon (LC 452), whose count equals the number kept when touching counts as overlapping. Attending one event per day (LC 1353) runs the same earliest-deadline idea day by day with a min-heap of end days. Read the touching rule carefully: `start ≥ last_end` keeps touching intervals, while balloons and pair chains need `start > last_end`. The classic mistake is sorting by start: on `[[1, 10], [2, 3], [4, 5]]` the long `[1, 10]` comes first, is kept, and blocks both short intervals inside it, keeping one where two fit.

*Practice:* LC 435 Non-overlapping Intervals · LC 452 Minimum Number of Arrows to Burst Balloons · LC 646 Maximum Length of Pair Chain · LC 1353 Maximum Number of Events That Can Be Attended

```{=latex}
\clearpage
```

## 51. Task Scheduler {#a51}

```{=latex}
\markright{51. Task Scheduler}
```

[Frame the Most Frequent Task · Greedy · Tier 2]{.meta}

Each task takes one unit of time, and two runs of the same task need at least `n` units between them; the CPU may sit idle. Return the fewest units that run every task. For `["A", "A", "A", "B", "B", "B"]` with `n = 2` the answer is `8`: `A B idle A B idle A B`.

Simulating unit by unit works, but the answer is a formula, because the most frequent task is the bottleneck. Its `max_count` copies need a gap of `n` units after every copy but the last, so they frame a grid: `max_count - 1` full rows of width `n + 1`, each starting with that task, and then a last row. Every other task drops into the gaps column by column, most frequent first, an order that keeps each task's copies at least a full row, `n + 1` units, apart. The tasks tied at `max_count` also need a slot in the last row, so `frame = (max_count - 1) * (n + 1) + tied`. Nothing beats the frame, because the last copies of the tied tasks cannot start before the last row and each needs a unit of its own.

Picture the grid filling up. While gaps remain, the leftover gaps become idles and the answer is the frame. Once the other tasks overflow the gaps, the rows simply widen past `n + 1`; the copies of each task are still a full row apart, so no idle is needed at all and the answer is `len(tasks)`, which no schedule can beat either. Both cases fold into `max(frame, len(tasks))`.

```text
tasks A A A B B B, n = 2      counts A 3, B 3: max_count = 3, tied = 2
            ┌─ n + 1 = 3 ─┐
   row 1    A    B    idle
   row 2    A    B    idle
   row 3    A    B            last row: only the tied tasks
   frame = (3 - 1) * 3 + 2 = 8 ≥ len(tasks) = 6: answer 8

add C C D D                   counts A 3, B 3, C 2, D 2: frame still 8
   row 1    A    B    C    D  rows widen past n + 1
   row 2    A    B    C    D
   row 3    A    B
   frame = 8 < len(tasks) = 10: answer 10, no idles
```

```pseudo
FUNCTION LeastInterval(tasks, n)
    counts ← empty map
    FOR EACH task IN tasks
        counts[task] ← counts.get(task, 0) + 1
    max_count ← 0
    FOR EACH task IN counts
        max_count ← max(max_count, counts[task])
    tied ← 0                               // tasks that also reach max_count
    FOR EACH task IN counts
        IF counts[task] = max_count
            tied ← tied + 1
    frame ← (max_count - 1) * (n + 1) + tied       // full rows, then a last row
    RETURN max(frame, len(tasks))          // overflow: rows widen, no idles
```

Counting takes `O(len(tasks))` time, and the map holds one entry per distinct task, `O(1)` for a fixed alphabet such as the 26 letters of LC 621. Reach for the frame when a problem spaces out repeats with a cooldown and asks only for a length or a yes-or-no answer. When the actual order is needed, simulate instead: a max-heap of remaining counts picks the most frequent ready task each unit, and a queue holds the tasks that are cooling down. Reorganize String (LC 767) is the case `n = 1` with no idle allowed, so an arrangement exists exactly when `frame ≤ len(s)`; LC 358 is the same with cooldown `k - 1`. The classic mistake is forgetting `tied` and adding just `1` for the last row, which answers `7` on the example, while `B` needs a slot in that row too and the answer is `8`.

*Practice:* LC 621 Task Scheduler · LC 767 Reorganize String · LC 358 Rearrange String k Distance Apart

```{=latex}
\clearpage
```

## 52. Partition Labels {#a52}

```{=latex}
\markright{52. Partition Labels}
```

[Extend to the Last Occurrence · Greedy · Tier 2]{.meta}

Cut a string into as many parts as possible so that each letter appears in at most one part, and return the part sizes in order. `"ababcbacadefegdehijhklij"` splits into `"ababcbaca"`, `"defegde"` and `"hijhklij"`, so the answer is `[9, 7, 8]`.

A part that contains a letter must stretch to that letter's last occurrence, and every letter swept up on the way can stretch it further. The brute force grows a part one character at a time and rescans the rest of the string for its letters, `O(n²)`. Instead, one pass records `last[c]`, the final index of every letter. A second pass carries `part_end`, the farthest last occurrence among the letters of the current part: each character pushes `part_end` to `max(part_end, last[c])`, and when `i` catches up with `part_end`, no letter inside reaches further, so the part closes and the next one starts at `i + 1`. Cutting at the first such moment is what makes the count maximal, because every earlier position inside the part has some letter crossing it, so no valid cut is ever skipped.

Picture each letter as an interval from its first copy to its last. The parts are exactly the groups of overlapping intervals, so this is Merge Intervals (#18) without the sort: scanning the string meets the intervals in order of their starts for free, and `part_end` is the right edge of the group being merged. In the picture, `a` alone drags the first part to index 8, while `e` and `j` set the ends of the other two.

```text
last     a 8, b 5, c 7, d 14, e 15, f 11, g 13, h 19, i 22, j 23, k 20, l 21

i         0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
s         a  b  a  b  c  b  a  c  a  d  e  f  e  g  d  e  h  i  j  h  k  l  i  j
part_end  8  8  8  8  8  8  8  8  8 14 15 15 15 15 15 15 19 22 23 23 23 23 23 23
cut                               ▲                    ▲                       ▲
parts    └────────── 9 ───────────┘ └─────── 7 ────────┘ └───────── 8 ─────────┘
```

```pseudo
FUNCTION PartitionLabels(s)
    last ← empty map                       // letter → index of its last copy
    FOR i FROM 0 TO len(s) - 1
        last[s[i]] ← i
    sizes ← empty list
    start ← 0                              // first index of the current part
    part_end ← 0                           // the part must reach at least here
    FOR i FROM 0 TO len(s) - 1
        part_end ← max(part_end, last[s[i]])       // this letter drags it along
        IF i = part_end                    // nothing inside reaches past i
            sizes.append(i - start + 1)
            start ← i + 1
    RETURN sizes
```

Two passes give `O(n)` time, and `last` holds one entry per distinct letter, `O(1)` for the 26 lowercase letters. Reach for this pattern when a sequence must be cut so that no item, a letter, a value or an id, crosses a cut: record how far each item reaches, and cut wherever the running maximum reach meets the scan. Max Chunks To Make Sorted (LC 769) is the same scan, with the running maximum of the values as the reach. The classic mistake is `part_end = last[s[i]]` without the `max`, which lets a short-lived letter pull the end back: on `"abac"` it cuts after `"ab"` although `a` returns at index 2, answering `[2, 1, 1]` instead of `[3, 1]`.

*Practice:* LC 763 Partition Labels · LC 56 Merge Intervals · LC 769 Max Chunks To Make Sorted

```{=latex}
\clearpage
```

## 53. Combination Sum {#a53}

```{=latex}
\markright{53. Combination Sum}
```

[Unlimited Reuse with a Start Index · Backtracking · Tier 2]{.meta}

Given an array of distinct positive integers `candidates` and a `target`, return every combination of candidates that sums to the target. A candidate may be used any number of times, and order does not matter, so `[2, 2, 3]` and `[3, 2, 2]` are the same combination. For `[2, 3, 6, 7]` and target `7` the answer is `[[2, 2, 3], [7]]`.

This is the subsets tree of #22 with two changes. First, a chosen candidate may be chosen again, so the recursion passes `start = i` instead of `i + 1`: the next pick may repeat the current candidate or move right, but it never moves left. Every path is therefore non-decreasing, one canonical order per combination, so each combination is built exactly once. Second, each call also carries what is still missing, `remaining`, and a node records its path only when `remaining` hits 0 exactly.

Sorting first turns overshooting into a wall. Scanning left to right, the first candidate larger than `remaining` proves that every later one is larger too, so the loop breaks instead of continuing, and a whole fan of hopeless branches is never entered. In the tree below each node shows its path and what is still missing; the whole search takes ten calls.

```text
[]  7 left                    candidates sorted: [2, 3, 6, 7]
├── [2]  5 left
│   ├── [2,2]  3 left
│   │   ├── [2,2,2]  1 left   then 2 > 1: break
│   │   ├── [2,2,3]  0 left   ✓ record
│   │   └── 6 > 3: break
│   ├── [2,3]  2 left         loop starts at 3 (start = 1); 3 > 2: break
│   └── 6 > 5: break
├── [3]  4 left
│   ├── [3,3]  1 left         then 3 > 1: break
│   └── 6 > 4: break
├── [6]  1 left               then 6 > 1: break
└── [7]  0 left               ✓ record
```

```pseudo
FUNCTION Backtrack(candidates, start, remaining, path, result)
    IF remaining = 0
        result.append(path.copy())          // exact hit: one combination
        RETURN
    FOR i FROM start TO len(candidates) - 1
        IF candidates[i] > remaining
            BREAK                           // sorted: the rest are bigger
        path.append(candidates[i])          // choose
        // pass i, not i + 1: the same candidate may be chosen again
        Backtrack(candidates, i, remaining - candidates[i], path, result)
        path.pop()                          // un-choose

FUNCTION CombinationSum(candidates, target)
    candidates ← sorted(candidates)         // makes the BREAK valid
    result ← empty list
    Backtrack(candidates, 0, target, empty list, result)
    RETURN result
```

The tree is at most `t / m` levels deep, for target t and smallest candidate m, and branches at most n ways, so it has `O(n^(t/m + 1))` nodes: exponential, which the small constraints keep in check; the extra space is the `O(t / m)` depth. Signals: all combinations that reach a sum, an unlimited supply of each item, and a request to list them rather than count them. Two neighbors change a line or two. LC 40 uses each candidate at most once and may contain duplicates, so it recurses with `i + 1` and skips `candidates[i]` when `i > start` and `candidates[i] = candidates[i - 1]`, the rule from Subsets II; LC 216 picks exactly k distinct digits from 1 to 9. LC 377 only looks similar: it counts ordered sequences, which is a counting DP rather than a listing. Recursing with `i + 1` here loses `[2, 2, 3]`. The classic mistake goes the other way, recursing with `start = 0`: the path may then move left, and `[2, 2, 3]`, `[2, 3, 2]` and `[3, 2, 2]` come back as three different answers.

*Practice:* LC 39 Combination Sum · LC 40 Combination Sum II · LC 216 Combination Sum III · LC 377 Combination Sum IV

```{=latex}
\clearpage
```

## 54. Word Search {#a54}

```{=latex}
\markright{54. Word Search}
```

[Grid Backtracking with In-Place Marks · Backtracking · Tier 2]{.meta}

Given a grid of letters and a word, decide whether the word can be spelled along a path of horizontally or vertically adjacent cells, using each cell at most once. In the grid with rows `ABCE`, `SFCS` and `ADEE`, the word `ABCCED` is there, while `ABCB` is not, because its second `B` would have to reuse a cell.

A path is a sequence of choices, so this is backtracking on the grid. Every cell is tried as the start. From a cell that matches `word[k]`, the search steps to each of the four neighbors looking for `word[k + 1]`, and it succeeds when k reaches the length of the word. The path must not cross itself, so before stepping on, the cell is overwritten with `#`, a character no word contains, and once the search from that cell is over, the letter is written back. The mark replaces a visited set, and it folds the visited test into the letter test, because `#` never equals `word[k]`.

Picture a snake growing through the grid. Its body is the marked cells, its head tries the neighbors in a fixed order (down, up, right, left), and when the head is stuck the snake pulls back one cell and unmarks it, so that a different path may use that cell later.

```text
board       "ABCCED": k on its path       "ABCB": the board when k = 3
A B C E     0 1 2 .                       # # # E    the C at (0,2) needs a B,
S F C S     . . 3 .                       S F C S    and its only B neighbor
A D E E     . 5 4 .                       A D E E    is '#': dead end

ABCCED at k = 5: down is off the grid, up is '#', right is E, left is D ✓
ABCB: unmark C, B, A in turn; the other A, at (2,0), fails at once: false
```

```pseudo
FUNCTION Dfs(board, word, row, col, k)
    IF k = len(word)
        RETURN true                          // every letter matched
    IF row < 0 OR row ≥ len(board) OR col < 0 OR col ≥ len(board[0])
        RETURN false                         // off the grid
    IF board[row][col] ≠ word[k]
        RETURN false                         // wrong letter, or a '#'
    board[row][col] ← '#'                    // mark: on the path now
    found ← false
    FOR EACH (d_row, d_col) IN [(1, 0), (-1, 0), (0, 1), (0, -1)]
        IF Dfs(board, word, row + d_row, col + d_col, k + 1)
            found ← true
            BREAK
    board[row][col] ← word[k]                // unmark on the way back
    RETURN found

FUNCTION Exist(board, word)
    FOR row FROM 0 TO len(board) - 1
        FOR col FROM 0 TO len(board[0]) - 1
            IF Dfs(board, word, row, col, 0)
                RETURN true
    RETURN false
```

Each of the `m · n` starts grows paths of up to L cells, and after the first step the cell behind the head is always marked, so at most three ways lead on: the worst case is `O(m · n · 3^L)`, usually quoted as the looser `O(m · n · 4^L)`, with `O(L)` recursion depth. Two cheap prunes help in practice. Count the letters of the grid first and answer false if the word needs more of some letter than the grid holds; and if the word's last letter is rarer in the grid than its first, search for the reversed word instead, so fewer starts pass the first test. Signals: a grid, a path through adjacent cells, no reuse, one word. For many words at once, the trie-guided version is #63. The classic mistake is forgetting to write the letter back: the `#` stays behind and blocks later paths, and on this grid a failed search for `ABCB` would leave every `A` marked, so a following search for `ABCCED` would wrongly say false.

*Practice:* LC 79 Word Search · LC 212 Word Search II

```{=latex}
\clearpage
```

## 55. Serialize and Deserialize a Binary Tree {#a55}

```{=latex}
\markright{55. Serialize and Deserialize a Binary Tree}
```

[Preorder with Null Markers · DFS · Tier 2]{.meta}

Turn a binary tree into a string, and turn that string back into the very same tree. For `[1, 2, 3, null, null, 4, 5]`, a root `1` with children `2` and `3` where `3` has children `4` and `5`, writing the values in preorder with `#` for every missing child gives `"1,2,#,#,3,4,#,#,5,#,#"`, and reading that string rebuilds the tree.

A bare preorder listing is ambiguous: `1, 2` could be a root with a left child `2` or a root with a right child `2`, and nothing in the list tells them apart. What is lost is where each subtree ends, and the null marker puts it back. With a `#` for every empty child, a value token is always followed by exactly two complete subtrees and a `#` is a complete subtree on its own, so the two trees above become the different strings `1,2,#,#,#` and `1,#,2,#,#`. A tree with `n` nodes has `n + 1` empty children, so the string holds `2n + 1` tokens.

Decoding replays the encoding. A shared index moves left to right through the tokens; each call reads one token, returns null for `#`, and otherwise builds the node and calls itself twice, first for the left subtree, then for the right. The left call eats exactly the tokens of the left subtree and stops, leaving the index on the first token of the right subtree, and that is the whole trick: in preorder every subtree is one unbroken block of tokens, its value first, then its left block, then its right block.

```text
      1     tokens  1  2  #  #  3  4  #  #  5  #  #
     / \    index   0  1  2  3  4  5  6  7  8  9 10
    2   3                          └──4──┘  └──5──┘
       / \             └──2──┘  └────────3────────┘
      4   5         └──────────────1──────────────┘
the read for 3 starts at index 4 because the read for 2 stopped after index 3
```

```pseudo
FUNCTION Serialize(root)
    tokens ← empty list
    Write(root, tokens)
    RETURN join(tokens, ",")

FUNCTION Write(node, tokens)
    IF node = null
        tokens.append("#")                 // the marker closes a branch
        RETURN
    tokens.append(str(node.val))
    Write(node.left, tokens)
    Write(node.right, tokens)

FUNCTION Deserialize(data)
    tokens ← split(data, ",")
    index ← [0]                            // one box all the calls share
    RETURN Read(tokens, index)

FUNCTION Read(tokens, index)
    token ← tokens[index[0]]
    index[0] ← index[0] + 1
    IF token = "#"
        RETURN null
    node ← new TreeNode(int(token))
    node.left ← Read(tokens, index)        // the left subtree eats its tokens
    node.right ← Read(tokens, index)       // the right one starts after them
    RETURN node
```

Both directions handle each node and each marker once, so they run in `O(n)` time, with an `O(n)` string and `O(h)` recursion depth. The commas matter: they keep `12` apart from `1` and `2` and let negative values parse with no extra rule. Reach for this whenever a tree must leave memory, to a file, across a network, or into a hash map that spots duplicate subtrees. A binary search tree needs no markers, because its values already say where the left subtree ends, at the first value larger than the root. Without markers a general tree needs a second traversal, which is how it is rebuilt from its preorder and inorder sequences together. The classic mistake is passing the index as a plain integer: each call advances its own copy, the caller never learns how many tokens its left subtree consumed, and the right subtree reads them all over again.

*Practice:* LC 297 Serialize and Deserialize Binary Tree · LC 449 Serialize and Deserialize BST · LC 105 Construct Binary Tree from Preorder and Inorder Traversal

```{=latex}
\clearpage
```

## 56. BST Search, Insert, Delete {#a56}

```{=latex}
\markright{56. BST Search, Insert, Delete}
```

[Delete with the In-Order Successor · BST · Tier 2]{.meta}

A binary search tree keeps every value in a node's left subtree smaller than the node and every value in its right subtree larger. Search for a value, insert a new one and delete an existing one, keeping that order intact. Deleting `3` from `[5, 3, 6, 2, 4, null, 7]` gives `[5, 4, 6, 2, null, null, 7]`: the successor `4` moves up into the gap.

All three operations ride on one move. At each node a single comparison throws away an entire subtree, so the walk follows one path from the root toward a leaf. Search loops down that path until it meets the value or falls off the tree. Insert follows the same path to the empty spot where the value would have been and hangs a new leaf there. Written recursively, each call returns the root of its subtree and the parent reattaches whatever comes back, so the one new link is made without any special case, not even for an empty tree.

Delete is the operation with cases, sorted by the number of children the doomed node has. A leaf simply disappears, and its parent receives null. A node with one child is spliced out and the child takes its place; the order survives because that whole subtree already sat on the correct side of the parent. A node with two children cannot leave without orphaning one of them, so it keeps its place and changes its value instead. The standard replacement is the in-order successor, the smallest value of the right subtree, found by stepping right once and then left as far as possible: it is larger than everything on the left and smaller than everything else on the right. Copy it up, then delete it from the right subtree, where it has no left child and so falls into an easy case.

```text
3 < 5: go left, then 3     successor: right once,     copy 4 up; deleting the
is found with 2 children   then left to the end: 4    old 4 is the leaf case
      5                          5                          5
    /   \                      /   \                      /   \
   3     6                    3     6                    4     6
  / \     \                  / \     \                  /       \
 2   4     7                2  (4)    7                2         7
```

```pseudo
FUNCTION Search(root, val)
    node ← root
    WHILE node ≠ null AND node.val ≠ val
        IF val < node.val
            node ← node.left
        ELSE
            node ← node.right
    RETURN node                            // the node holding val, or null

FUNCTION Insert(root, val)
    IF root = null
        RETURN new TreeNode(val)           // the empty spot: a new leaf
    IF val < root.val
        root.left ← Insert(root.left, val)
    ELSE IF val > root.val
        root.right ← Insert(root.right, val)
    RETURN root                            // equal: already present

FUNCTION Delete(root, val)
    IF root = null
        RETURN null                        // val is not in the tree
    IF val < root.val
        root.left ← Delete(root.left, val)
    ELSE IF val > root.val
        root.right ← Delete(root.right, val)
    ELSE
        IF root.left = null                // leaf, or right child only
            RETURN root.right
        IF root.right = null               // left child only
            RETURN root.left
        successor ← root.right             // two children: leftmost node
        WHILE successor.left ≠ null        // of the right subtree
            successor ← successor.left
        root.val ← successor.val           // copy it up...
        root.right ← Delete(root.right, successor.val)   // ...and remove it
    RETURN root
```

Each operation walks a single path, so all three cost `O(h)`: `O(log n)` while the tree stays balanced, `O(n)` once sorted insertions have stretched it into a chain, which is why the ordered maps of standard libraries are self-balancing trees. Reach for a BST when data must stay sorted while it changes: the next larger value, every value in a range, the `k`-th smallest (#57 walks a BST in order). The in-order predecessor, the largest value of the left subtree, works just as well as the replacement. The classic mistake is deleting the original value from the right subtree after copying the successor up, instead of the successor's value: the original is no longer there, nothing is removed, and the tree ends up holding the successor twice.

*Practice:* LC 700 Search in a Binary Search Tree · LC 701 Insert into a Binary Search Tree · LC 450 Delete Node in a BST

```{=latex}
\clearpage
```

## 57. BST Iterator {#a57}

```{=latex}
\markright{57. BST Iterator}
```

[Controlled In-Order with a Stack · BST · Tier 2]{.meta}

Design an iterator over a binary search tree that hands out its values in ascending order: `next()` returns the next smallest value and `has_next()` says whether any are left. For `[7, 3, 15, null, null, 9, 20]`, five calls to `next()` return `3`, `7`, `9`, `15` and `20`, and `has_next()` turns false after the last one.

The easy answer runs an inorder traversal up front and stores all `n` values in a list, paying `O(n)` memory before the first call. A real iterator does the traversal lazily, one step per call, which means pausing an inorder walk in the middle. A recursive walk knows where it is through the ancestors whose values are still owed, the ones it left by going down into their left subtrees; keep exactly those on an explicit stack and pausing is free. Start by pushing the root and its whole left spine, so the top of the stack is the leftmost node, the smallest value. Each `next()` pops the top, the smallest value not yet returned, and before handing it out pushes the left spine of the popped node's right child, because the values just above the popped one live in that right subtree, smallest first along its spine.

The stack always holds a chain of nodes, each in the left subtree of the one below it. Everything inside the right subtree being explored is smaller than every ancestor still waiting underneath, which is why the order never breaks.

```text
       7          call         returns   stack after (top on the right)
      / \         init                   [7, 3]
     3   15       next()          3      [7]
        /  \      next()          7      [15, 9]
       9    20    has_next()     true    [15, 9]
                  next()          9      [15]
                  next()         15      [20]
                  next()         20      []
                  has_next()     false   []
```

```pseudo
CLASS BSTIterator
    FUNCTION Init(root)
        self.stack ← empty stack
        self.PushLeft(root)

    FUNCTION PushLeft(node)
        WHILE node ≠ null                  // walk down the left spine
            self.stack.push(node)
            node ← node.left

    FUNCTION Next()
        node ← self.stack.pop()            // the smallest value still waiting
        self.PushLeft(node.right)          // its successors live on the right
        RETURN node.val

    FUNCTION HasNext()
        RETURN len(self.stack) > 0

FUNCTION KthSmallest(root, k)
    iterator ← new BSTIterator(root)
    value ← null
    FOR i FROM 0 TO k - 1
        value ← iterator.Next()
    RETURN value
```

A single `next()` can push a long spine, but over the whole iteration every node is pushed once and popped once, so `n` calls cost `O(n)` in total, `O(1)` amortized each, and `has_next()` is always `O(1)`. The stack holds at most one node per level, `O(h)` space instead of `O(n)`. The `k`-th smallest value is just `k` calls to `next()`, `O(h + k)` time. Reach for this whenever a tree must be consumed in sorted order one value at a time: merging two BSTs by advancing two iterators like two sorted lists, finding a pair with a given sum with one ascending and one descending iterator, or finding an in-order successor. The classic mistake is pushing only the popped node's right child instead of its whole left spine; on this tree the iterator then returns `3, 7, 15, 20` and never sees `9`.

*Practice:* LC 173 Binary Search Tree Iterator · LC 230 Kth Smallest Element in a BST · LC 285 Inorder Successor in BST · LC 1305 All Elements in Two Binary Search Trees

```{=latex}
\clearpage
```

## 58. Multi-Source BFS {#a58}

```{=latex}
\markright{58. Multi-Source BFS}
```

[Rotting Oranges · BFS · Tier 2]{.meta}

In a grid, `0` is an empty cell, `1` a fresh orange and `2` a rotten one. Every minute, each fresh orange next to a rotten one, up, down, left or right, turns rotten. Return the number of minutes until no fresh orange is left, or `-1` if some orange can never rot. In `[[2, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 2]]` the two rotten corners infect everything in `2` minutes.

Rot that spreads one step a minute is BFS (#30) on a graph whose nodes are the orange cells: the minute an orange rots is its distance to the nearest rotten orange, and the answer is the largest of those distances. The brute force runs a separate BFS from each of the `k` rotten oranges and keeps the minimum per cell, `O(k · rows · cols)`. One BFS does it all if every rotten orange enters the queue at minute 0. Imagine an extra node joined to every rotten orange: a single BFS from it reaches each cell through the nearest rotten orange, and seeding the queue with all of them is that same BFS with its first step already taken. The layer loop of level-order traversal (#24) counts the minutes, because each pass pops exactly the oranges that rotted in the minute before.

Picture several stones dropped into a pond at the same moment. Their ripples spread in lockstep, and wherever two meet, a cell belongs to whichever ripple arrived first. In the example each corner alone would need 5 minutes, but the two waves meet in the middle, and the combined map is the cell-by-cell minimum of the two single-source maps. Counting `fresh` up front gives both the stop condition and the `-1` test: the loop ends the moment the last fresh orange rots, and an orange still fresh when the queue runs dry is walled off from every rotten one.

```text
the minute each cell rots (· is empty)

grid        both at once     only (0,0)     only (2,3)
2 1 1 1     0 1 2 2          0 1 2 3        5 4 3 2
1 · 1 1     1 · 2 1          1 · 3 4        4 · 2 1
1 1 1 2     2 2 1 0          2 3 4 5        3 2 1 0
            answer 2         answer 5       answer 5

minute 0: the queue holds (0,0) (2,3)             fresh 9
minute 1: rots (1,0) (0,1) (1,3) (2,2)            fresh 5
minute 2: rots (2,0) (0,2) (0,3) (1,2) (2,1)      fresh 0: stop, 2 minutes
```

```pseudo
DIRECTIONS ← [(1, 0), (-1, 0), (0, 1), (0, -1)]

FUNCTION OrangesRotting(grid)
    rows ← len(grid)
    cols ← len(grid[0])
    queue ← empty queue
    fresh ← 0
    FOR row FROM 0 TO rows - 1
        FOR col FROM 0 TO cols - 1
            IF grid[row][col] = 2
                queue.enqueue((row, col))  // every source starts at minute 0
            ELSE IF grid[row][col] = 1
                fresh ← fresh + 1
    minutes ← 0
    WHILE queue is not empty AND fresh > 0
        FOR i FROM 1 TO len(queue)         // len read once: this layer only
            (row, col) ← queue.dequeue()
            FOR EACH (d_row, d_col) IN DIRECTIONS
                next_row ← row + d_row
                next_col ← col + d_col
                inside ← 0 ≤ next_row < rows AND 0 ≤ next_col < cols
                IF inside AND grid[next_row][next_col] = 1
                    grid[next_row][next_col] ← 2   // rot now: enqueued once
                    fresh ← fresh - 1
                    queue.enqueue((next_row, next_col))
        minutes ← minutes + 1
    IF fresh > 0
        RETURN -1                          // walled off from every rotten one
    RETURN minutes
```

Each cell enters the queue at most once and is looked at from at most four neighbors, so the search takes `O(rows · cols)` time and space. Reach for multi-source BFS whenever a problem asks for each cell's distance to the nearest of many sources, or how long something takes to spread from several starting points at once: the distance to the nearest `0` (LC 542), to the nearest gate (LC 286), or the water cell farthest from any land (LC 1162). The classic mistake is looping while the queue is non-empty and counting the final pass, in which the last oranges to rot infect nobody: that answers 3 here instead of 2. The `fresh > 0` condition stops the clock on the right minute.

*Practice:* LC 994 Rotting Oranges · LC 542 01 Matrix · LC 286 Walls and Gates · LC 1162 As Far from Land as Possible

```{=latex}
\clearpage
```

## 59. Word Ladder {#a59}

```{=latex}
\markright{59. Word Ladder}
```

[BFS on an Implicit Graph · BFS · Tier 2]{.meta}

Turn `begin_word` into `end_word` by changing one letter at a time, where every word after the first must come from `word_list`. Return the number of words in the shortest such ladder, or `0` if there is none. From `hit` to `cog` with the list `hot, dot, dog, lot, log, cog`, one shortest ladder is `hit → hot → dot → dog → cog`, so the answer is `5`.

The words are the nodes of a graph that is never written down: two words are joined when they differ in exactly one letter, and the question is a shortest path in that graph, which is BFS (#30). Building the graph by comparing every pair of words costs `O(n² · L)` for `n` words of length `L`. Generating neighbors on demand is cheaper for a large dictionary: change each of the `L` positions to each of the 26 letters and keep the candidates that are unvisited dictionary words. The set of unvisited words does double duty. It is the dictionary, so a string that is not a word never becomes a neighbor, and it is the visited mark, because a word is removed the moment it is enqueued and can never enter the queue twice. Each queue entry carries the length of the ladder that reached it, and the first time `end_word` leaves the queue, that length is the answer.

Picture BFS rings around `hit`, one ring per changed letter. The pattern beside each step names the position that changed: `hot` and `dot` and `lot` all match `*ot`, which is why they sit one step apart. Grouping the dictionary by such patterns ahead of time, `*ot → [hot, dot, lot]`, is the other standard way to find neighbors.

```text
  hit ── hot ─┬─ dot ── dog ── cog      cog is end_word
              └─ lot ── log
   1      2       3      4      5       words in the ladder

pop (hit, 1)   h*t → hot          queue (hot, 2)
pop (hot, 2)   *ot → dot, lot     queue (dot, 3) (lot, 3)
pop (dot, 3)   do* → dog          queue (lot, 3) (dog, 4)
pop (lot, 3)   lo* → log          queue (dog, 4) (log, 4)
pop (dog, 4)   *og → cog          queue (log, 4) (cog, 5)
pop (log, 4)   nothing new        queue (cog, 5)
pop (cog, 5)   it is end_word: return 5
```

```pseudo
FUNCTION LadderLength(begin_word, end_word, word_list)
    unvisited ← set(word_list)             // dictionary words not reached yet
    IF end_word NOT IN unvisited
        RETURN 0
    IF begin_word IN unvisited
        unvisited.remove(begin_word)       // the start counts as reached
    queue ← empty queue
    queue.enqueue((begin_word, 1))         // (word, words in the ladder)
    WHILE queue is not empty
        (word, length) ← queue.dequeue()
        IF word = end_word
            RETURN length
        FOR i FROM 0 TO len(word) - 1
            FOR EACH letter IN "abcdefghijklmnopqrstuvwxyz"
                candidate ← word with position i replaced by letter
                IF candidate IN unvisited          // a word not reached yet
                    unvisited.remove(candidate)    // mark when enqueued
                    queue.enqueue((candidate, length + 1))
    RETURN 0
```

Each word is enqueued at most once and tries `26 · L` candidates that each cost `O(L)` to build and look up, so the search takes `O(n · 26 · L²)` time and `O(n · L)` space. Reach for BFS on an implicit graph whenever the states are strings, lock combinations or board positions and one move changes a state a little: Open the Lock turns one wheel per move, and Minimum Genetic Mutation changes one gene letter. Bidirectional BFS grows one frontier from each end, always expanding the smaller, and stops when they touch; with `b` neighbors per word and a ladder of `d` steps it explores about `2 · b^(d/2)` words instead of `b^d`. Word Ladder II wants every shortest ladder, so it records each word's parents from the previous layer and walks them back from `end_word`. The classic mistake is counting changes instead of words: starting the length at 0 answers 4.

*Practice:* LC 127 Word Ladder · LC 126 Word Ladder II · LC 752 Open the Lock · LC 433 Minimum Genetic Mutation

```{=latex}
\clearpage
```

## 60. Cycle Detection in a Directed Graph {#a60}

```{=latex}
\markright{60. Cycle Detection in a Directed Graph}
```

[Three Colors: White, Gray, Black · Cycle Detection · Tier 2]{.meta}

Given a directed graph on nodes `0` to `n - 1`, decide whether it contains a cycle, a path that follows the arrows back to where it started. With the edges `0→1`, `0→2`, `1→3`, `2→3`, `2→4` and `4→0` the answer is yes, `0 → 2 → 4 → 0`. Without `4→0` the answer is no, even though node `3` can be reached two ways.

In an undirected graph, running into an already visited node signals a cycle, as long as it is not the parent just left (#81). In a directed graph it signals nothing: the diamond `0→1→3`, `0→2→3` reaches `3` twice and has no cycle. What matters is whether that node is still on the current path. The brute force asks every node whether it can reach itself, one search per node, `O(V · (V + E))`. A single DFS with three colors does better. White means not visited yet. Gray means entered but not finished: exactly the current recursion path. Black means finished: everything reachable from the node has been explored and holds no cycle. An edge into a gray node points back at an ancestor on the current path, and that back edge plus the path down from the ancestor is a cycle. An edge into a black node is harmless and never followed, which keeps the search linear.

Picture the gray nodes as a rope paid out behind the search: entering a node adds it to the rope, and finishing it reels it back in and paints it black. A cycle is an edge that lands back on the rope. In the trace, `2→3` lands on black `3`, finished and off the rope, where a plain visited set would wrongly report a cycle. Then `4→0` lands on `0`, still on the rope, and the rope from `0` to `4` plus that edge is the cycle.

```text
  ┌──────────────┐
  ↓              │       event       gray: the current path   black
  0 ──→ 1 ──→ 3  │       enter 0     0                        -
  │           ↑  │       enter 1     0 1                      -
  └──→ 2 ─────┘  │       enter 3     0 1 3                    -
       │         │       finish 3    0 1                      3
       └──→ 4 ───┘       finish 1    0                        3 1
                         enter 2     0 2                      3 1
                         edge 2→3    3 is black: skip it
                         enter 4     0 2 4                    3 1
                         edge 4→0    0 is gray: cycle 0 → 2 → 4 → 0 ✓
```

```pseudo
WHITE ← 0                                  // not visited yet
GRAY ← 1                                   // on the current DFS path
BLACK ← 2                                  // finished: no cycle reachable

FUNCTION HasCycle(n, edges)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)
    color ← array of n copies of WHITE
    FOR node FROM 0 TO n - 1
        IF color[node] = WHITE AND DFS(graph, node, color)
            RETURN true
    RETURN false

FUNCTION DFS(graph, node, color)
    color[node] ← GRAY                     // node joins the current path
    FOR EACH neighbor IN graph[node]
        IF color[neighbor] = GRAY
            RETURN true                    // back edge to a node on the path
        IF color[neighbor] = WHITE AND DFS(graph, neighbor, color)
            RETURN true
    color[node] ← BLACK                    // every path out of node is safe
    RETURN false
```

Every node and every edge is handled once, so the search costs `O(V + E)` time and `O(V)` space beyond the graph, for the colors and the recursion. Reach for three colors whenever dependencies, prerequisites or state transitions must be checked for a loop, or when the nodes that can never reach a cycle are wanted: in Find Eventual Safe States those are exactly the nodes that end black. Kahn's algorithm (#31) answers the same question without recursion, since a cycle exists exactly when fewer than `n` nodes get peeled; that matters in Python, where a chain of about a thousand nodes overflows the default recursion limit. The classic mistake is the plain visited set, which calls the diamond a cycle. Never painting finished nodes black is the same mistake in disguise: they stay gray, and any later visit looks like a cycle.

*Practice:* LC 207 Course Schedule · LC 802 Find Eventual Safe States · LC 1059 All Paths from Source Lead to Destination

```{=latex}
\clearpage
```

## 61. Topological Sort with DFS {#a61}

```{=latex}
\markright{61. Topological Sort with DFS}
```

[Reverse Postorder · Topological Sort · Tier 2]{.meta}

Given `n` nodes `0` to `n - 1` and directed edges `[u, v]` meaning `u` must come before `v`, return an order of all the nodes that respects every edge, or an empty list if a cycle makes that impossible. On the graph of Kahn's example (#31), with edges `0→3`, `1→3`, `3→4`, `3→2`, `4→5` and `2→5`, one valid order is `[1, 0, 3, 2, 4, 5]`.

Kahn's algorithm builds the order from the front, by repeatedly taking a node that nothing points to. Depth-first search builds it from the back. In a graph without cycles, a DFS finishes a node only after everything reachable from it has finished, so the order in which nodes finish, the postorder, lists every node after all of its descendants, and reversing it lists every node before them. The proof takes one edge at a time. When the search examines `u → v`, the node `v` is white, and is then entered and finished before `u` is; or black, and finished already; or gray, which makes `v` an ancestor of `u` on the current path and the edge part of a cycle. In every acyclic case `v` finishes before `u`, so in the reversed list `u` comes first. The colors are those of cycle detection (#60), and the same gray test triggers the `[]`.

Picture the answer being written from right to left. The first node to finish is a dead end, `5`, which belongs at the far right; each later finisher goes to the left of everything placed so far, because everything it leads to is already placed. Node `1` finishes last; its only edge leads into the black `3`. The result differs from Kahn's `[0, 1, 3, 4, 2, 5]` and is just as valid, since a graph can have many topological orders.

```text
    0 ──┐            ┌──→ 4 ──┐
        ├──→ 3 ──────┤        ├──→ 5
    1 ──┘            └──→ 2 ──┘

enter 0, 3, 4, 5
finish 5                                finished [5]
finish 4                                finished [5, 4]
enter 2; edge 2→5: 5 is black, skip
finish 2                                finished [5, 4, 2]
finish 3                                finished [5, 4, 2, 3]
finish 0                                finished [5, 4, 2, 3, 0]
enter 1; edge 1→3: 3 is black, skip
finish 1                                finished [5, 4, 2, 3, 0, 1]
reverse                                 order    [1, 0, 3, 2, 4, 5]
```

```pseudo
WHITE ← 0                                  // not visited yet
GRAY ← 1                                   // on the current DFS path
BLACK ← 2                                  // finished: after its descendants

FUNCTION TopologicalSort(n, edges)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)
    color ← array of n copies of WHITE
    finished ← empty list                  // nodes in the order they finish
    FOR node FROM 0 TO n - 1
        IF color[node] = WHITE AND NOT DFS(graph, node, color, finished)
            RETURN empty list              // a cycle: no order exists
    RETURN reverse(finished)

FUNCTION DFS(graph, node, color, finished)
    color[node] ← GRAY                     // node joins the current path
    FOR EACH neighbor IN graph[node]
        IF color[neighbor] = GRAY
            RETURN false                   // back edge: a cycle
        IF color[neighbor] = WHITE
            IF NOT DFS(graph, neighbor, color, finished)
                RETURN false
    color[node] ← BLACK
    finished.append(node)                  // its descendants are all in already
    RETURN true
```

Every node and every edge is handled once, so the sort costs `O(V + E)` time and `O(V)` extra space. Choose between the two sorts by the shape of the problem. Kahn's needs no recursion, which matters in Python on long chains, hands out the order front to back, and peels the graph level by level, which counting semesters needs. The DFS version fits when a DFS is already running, as in Longest Increasing Path in a Matrix, which computes each cell only after the cells it can step to: exactly this postorder. Sort Items by Groups Respecting Dependencies needs either sort twice, once for the groups and once for the items inside each group. The classic mistake is recording a node when the search enters it instead of when it finishes: the entry order here is `[0, 3, 4, 5, 2, 1]`, which puts `3` before its prerequisite `1`.

*Practice:* LC 210 Course Schedule II · LC 269 Alien Dictionary · LC 1203 Sort Items by Groups Respecting Dependencies · LC 329 Longest Increasing Path in a Matrix

```{=latex}
\clearpage
```

## 62. Connected Components {#a62}

```{=latex}
\markright{62. Connected Components}
```

[Count and Label by Flood Fill · Connected Components · Tier 2]{.meta}

Given `n` nodes `0` to `n - 1` and a list of undirected edges, count the connected components, the groups of nodes that can reach one another, and label each node with the number of its component. With seven nodes and the edges `0-1`, `1-2`, `3-4` and `3-5` there are 3 components, `{0, 1, 2}`, `{3, 4, 5}` and the lone `{6}`, so the labels are `[0, 0, 0, 1, 1, 1, 2]`.

The brute force asks for every pair of nodes whether a path joins them, a search per pair, `O(V² · (V + E))`. The insight is that one search from a node reaches exactly its own component, all of it and nothing else. So scan the nodes in order: each node that is still unlabeled starts a flood fill that paints its entire component with a fresh label, and every node the flood paints is skipped when the scan reaches it. The number of floods is the number of components. The flood keeps an explicit stack, like the iterative DFS of #28, but paints each node the moment it is pushed, so no node enters the stack twice. As #28 points out, that order is no longer strictly depth-first, and here it does not matter: BFS would serve equally well, because all that counts is that every reachable node gets painted. `label` doubles as the visited mark, with `-1` for unpainted.

Picture paint poured on a node. It runs along the edges and stops at the border of the component, because no edge leaves it. The scan then walks past the painted nodes until it finds a dry one and pours the next color. On a grid the same loop counts islands (#29), with the four neighboring land cells as the edges.

```text
  0 ── 1 ── 2        3 ── 4        6
                     │
                     5

start   label[start]   action                     label after
  0         -1         flood with 0: 0, 1, 2      [0, 0, 0, -1, -1, -1, -1]
  1, 2     0, 0        already painted: skip
  3         -1         flood with 1: 3, 4, 5      [0, 0, 0, 1, 1, 1, -1]
  4, 5     1, 1        already painted: skip
  6         -1         flood with 2: 6            [0, 0, 0, 1, 1, 1, 2]
count = 3
```

```pseudo
FUNCTION ConnectedComponents(n, edges)
    graph ← array of n empty lists
    FOR EACH (u, v) IN edges
        graph[u].append(v)                 // undirected: both directions
        graph[v].append(u)
    label ← array of n copies of -1        // -1 means not reached yet
    count ← 0
    FOR start FROM 0 TO n - 1
        IF label[start] = -1               // not reached by any earlier flood
            Flood(graph, start, count, label)
            count ← count + 1
    RETURN (count, label)

FUNCTION Flood(graph, start, mark, label)
    label[start] ← mark
    stack ← empty stack
    stack.push(start)
    WHILE stack is not empty
        node ← stack.pop()
        FOR EACH neighbor IN graph[node]
            IF label[neighbor] = -1
                label[neighbor] ← mark     // label when pushed: pushed once
                stack.push(neighbor)
```

Each node is painted once and each edge is examined from both ends, so the whole labeling costs `O(V + E)` time and space. Reach for it when a problem asks how many groups, networks, provinces or islands there are, whether two nodes are connected, or how big each group is; Count Unreachable Pairs needs only the component sizes, adding `size × (n - size)` over the components and halving the total. When the edges arrive one at a time and the count must stay current, union-find (#32) absorbs each new edge in near-constant time instead of flooding again. The classic mistake is storing each edge in one direction only: a flood from `0` can then never cross an edge written `[1, 0]`, and two nodes joined by that edge are counted as two components.

*Practice:* LC 323 Number of Connected Components in an Undirected Graph · LC 547 Number of Provinces · LC 1971 Find if Path Exists in Graph · LC 2316 Count Unreachable Pairs of Nodes in an Undirected Graph

```{=latex}
\clearpage
```

## 63. Word Search II {#a63}

```{=latex}
\markright{63. Word Search II}
```

[Trie-Guided Grid Backtracking · Tries · Tier 2]{.meta}

Given a grid of letters and a list of words, return every word that can be spelled along a path of horizontally or vertically adjacent cells, each cell used at most once per word. On the grid with rows `oaan`, `etae`, `ihkr` and `iflv`, of the words `oath`, `pea`, `eat` and `rain`, the answer is `oath` and `eat`.

Running Word Search (#54) once per word repeats work: every search starts again at every cell, and words that share a prefix, like `oat` and `oath`, walk the same cells once each. Put all the words into a trie (#34) instead and search once. The DFS carries a trie node along with the cell, steps onto a neighbor only if the node has a child for that neighbor's letter, and dies the moment its letters stop being a prefix of any word. Each grid path is matched against every word at the same time, a path never grows longer than the longest word, and the number of words no longer multiplies the work.

The node at the end of a word stores the word itself, so a hit is recorded without rebuilding the string, and the word is then cleared, so a second path that spells it adds nothing. After a node's subtree has been searched, a node left with no children is deleted from its parent: every word below it has been found, and later starts skip that branch in one lookup. The trie shrinks as the answer grows. The `#` mark from #54 needs no test of its own here, because `#` is never a child in the trie.

```text
board       trie of the words (● keeps a word)
o a a n     root ─┬─ o ─ a ─ t ─ h ●    oath
e t a e           ├─ p ─ e ─ a ●        pea
i h k r           ├─ e ─ a ─ t ●        eat
i f l v           └─ r ─ a ─ i ─ n ●    rain

start (0,0) o: o → a(0,1) → t(1,1) → h(2,1) ●  record oath, prune o-a-t-h
start (1,0) e: no neighbor is an a, dead after one cell
start (1,3) e: e → a(1,2) → t(1,1) ●  record eat, prune e-a-t
start (2,3) r: no neighbor is an a, dead after one cell
every other start: its letter is not a child of the root (no p on the board)
```

```pseudo
FUNCTION BuildTrie(words)
    root ← new TrieNode()                    // no children yet, word null
    FOR EACH word IN words
        node ← root
        FOR EACH ch IN word
            IF ch NOT IN node.children
                node.children[ch] ← new TrieNode()
            node ← node.children[ch]
        node.word ← word                     // the last node keeps the word
    RETURN root

FUNCTION Dfs(board, row, col, parent, found)
    IF row < 0 OR row ≥ len(board) OR col < 0 OR col ≥ len(board[0])
        RETURN
    ch ← board[row][col]
    IF ch NOT IN parent.children
        RETURN                               // no word goes this way
    node ← parent.children[ch]
    IF node.word ≠ null
        found.append(node.word)
        node.word ← null                     // record each word only once
    board[row][col] ← '#'                    // mark: on the current path
    FOR EACH (d_row, d_col) IN [(1, 0), (-1, 0), (0, 1), (0, -1)]
        Dfs(board, row + d_row, col + d_col, node, found)
    board[row][col] ← ch                     // unmark on the way back
    IF len(node.children) = 0
        parent.children.remove(ch)           // prune: no word left below

FUNCTION FindWords(board, words)
    root ← BuildTrie(words)
    found ← empty list
    FOR row FROM 0 TO len(board) - 1
        FOR col FROM 0 TO len(board[0]) - 1
            Dfs(board, row, col, root, found)
    RETURN found
```

Building the trie costs `O(total letters)`. The search is `O(m · n · 3^L)` in the worst case, for L the longest word, because each start grows paths of at most L cells with at most three ways on after the first step, and that bound does not grow with the number of words; the extra space is the trie plus `O(L)` recursion. Reach for this whenever one grid, or one text, must be searched for many words: the trie merges k searches into one walk that shares every common prefix. The classic mistake, carried over from #54, is returning as soon as a word is found. Here the search must go on, because `oat` and `oath` lie on the same path, and stopping at `oat` loses `oath`.

*Practice:* LC 212 Word Search II · LC 79 Word Search · LC 208 Implement Trie (Prefix Tree)

```{=latex}
\clearpage
```

## 64. KMP String Matching {#a64}

```{=latex}
\markright{64. KMP String Matching}
```

[The Prefix Function Never Re-Reads the Text · Strings · Tier 2]{.meta}

Given a text and a pattern, return every index where the pattern starts in the text, overlapping matches included. In the text `abababc` the pattern `ababc` starts only at index `2`, so the answer is `[2]`.

The brute force tries every start and compares up to `m` characters there, `O(n · m)` time; on `aaa…ab` against `aaab` it re-reads almost the whole window at every start. Its waste is forgetting what it has already read. When a mismatch comes after `j` characters matched, those `j` text characters are known: they are `pattern[0..j - 1]`. The next start that can still succeed therefore depends on the pattern alone. Slide the pattern right until the longest border of the matched part, its longest proper prefix that is also a suffix, lines up with that suffix in the text, and keep comparing at the same text position. `lps[i]` stores that border length for every prefix `pattern[0..i]`, so a mismatch at length `j` falls back to `j ← lps[j - 1]` and tries the same text character again, until it matches or `j` reaches 0.

Picture the text pointer `i` as a ratchet that only turns forward while the pattern jumps right underneath it. The table is built by the same loop run on the pattern against itself: `j` is the border being extended, a match grows it by one, a mismatch falls back to the next shorter border. After a full match, `j ← lps[j - 1]` keeps the overlap, which is how `aa` is found at 0, 1, 2 and 3 in `aaaaa`.

```text
pattern   a b a b c
lps       0 0 1 2 0    lps[3] = 2: "ab" is a prefix and a suffix of "abab"

index     0 1 2 3 4 5 6
text      a b a b a b c
start 0   a b a b c        i = 4: text 'a' ≠ pattern 'c' with j = 4
start 2       a b a b c    j ← lps[3] = 2: "ab" stays matched, i stays 4
                  ↑
matched   1 2 3 4 3 4 5    j = 5 = len(pattern) at i = 6 → match at 2
```

```pseudo
FUNCTION BuildLPS(pattern)
    lps ← array of len(pattern) zeros
    j ← 0                                   // length of the border so far
    FOR i FROM 1 TO len(pattern) - 1        // lps[0] = 0: proper prefixes only
        WHILE j > 0 AND pattern[i] ≠ pattern[j]
            j ← lps[j - 1]                  // fall back to a shorter border
        IF pattern[i] = pattern[j]
            j ← j + 1
        lps[i] ← j
    RETURN lps

FUNCTION KMPSearch(text, pattern)
    IF len(pattern) = 0
        RETURN empty list
    lps ← BuildLPS(pattern)
    matches ← empty list
    j ← 0                                   // pattern characters matched
    FOR i FROM 0 TO len(text) - 1
        WHILE j > 0 AND text[i] ≠ pattern[j]
            j ← lps[j - 1]                  // slide the pattern, retry text[i]
        IF text[i] = pattern[j]
            j ← j + 1
        IF j = len(pattern)
            matches.append(i - j + 1)       // the match ends at i
            j ← lps[j - 1]                  // keep the border for overlaps
    RETURN matches
```

Every step of `i` raises `j` by at most one and every fallback lowers it, so the fallbacks never outnumber the steps: `O(n)` for the search and `O(m)` for the table, `O(n + m)` time and `O(m)` space in all. Reach for KMP when exact matching needs a worst-case guarantee, or when the question is about borders themselves: the longest prefix that is also a suffix is `lps[m - 1]`, a string of length `m` is one block repeated exactly when `lps[m - 1] > 0` and `m` is divisible by `m - lps[m - 1]`, and the table of `s + "#" + reverse(s)` gives the longest palindromic prefix behind the shortest palindrome. Rabin-Karp (#85) reaches expected linear time with a rolling hash instead. The classic mistakes are an `IF` where the fallback needs a `WHILE` (the shorter border can mismatch too), starting the table loop at `i = 0`, which lets every prefix count itself as its own border, and resetting `j` to 0 after a match, which misses overlapping matches.

*Practice:* LC 28 Find the Index of the First Occurrence in a String · LC 1392 Longest Happy Prefix · LC 459 Repeated Substring Pattern · LC 214 Shortest Palindrome

```{=latex}
\clearpage
```

## 65. Longest Palindromic Substring {#a65}

```{=latex}
\markright{65. Longest Palindromic Substring}
```

[Expand Around Every Center · Strings · Tier 2]{.meta}

Given a string, return its longest substring that reads the same forwards and backwards, the leftmost one on a tie. For `babad` the answer is `bab`; `aba` is just as long but starts later.

The brute force tests every substring, `O(n²)` of them at `O(n)` each, for cubic time. Turn the test inside out: a palindrome is symmetric about its middle, so grow palindromes outward from every possible middle instead of checking substrings one by one. A middle is either a character (odd length, like `aba`) or the gap between two neighbors (even length, like `abba`), which makes `n + (n - 1) = 2n - 1` centers. Number them so that even centers sit on characters and odd centers on gaps: center `c` starts with `left = floor(c / 2)` and `right = left + c mod 2`.

From each center, two arms swing outward in step while they land on equal characters. The moment they differ, or one runs off the string, the window just inside the arms is the longest palindrome around that center, and nothing wider around it can be one, since a wider window would contain the mismatched pair at mirror positions. Keep the longest window seen; a strict comparison leaves ties with the earlier center.

```text
s          b   a   b   a   d
index      0   1   2   3   4
center     0 1 2 3 4 5 6 7 8     even center: a char, odd center: a gap

center   (left, right)   grows to   stops at      best so far
  0         (0, 0)        "b"        left edge     "b"
  1         (0, 1)        ""         b ≠ a         "b"
  2         (1, 1)        "bab"      left edge     "bab"
  3         (1, 2)        ""         a ≠ b         "bab"
  4         (2, 2)        "aba"      b ≠ d         "bab"  (tie keeps first)
  5         (2, 3)        ""         b ≠ a         "bab"
  6         (3, 3)        "a"        b ≠ d         "bab"
  7         (3, 4)        ""         a ≠ d         "bab"
  8         (4, 4)        "d"        right edge    "bab"
```

```pseudo
FUNCTION LongestPalindrome(s)
    best_start ← 0
    best_len ← 0
    FOR center FROM 0 TO 2 * len(s) - 2
        left ← floor(center / 2)
        right ← left + center mod 2           // even: a char, odd: a gap
        WHILE left ≥ 0 AND right < len(s) AND s[left] = s[right]
            left ← left - 1                   // ends match: grow both ways
            right ← right + 1
        length ← right - left - 1             // one step past each end
        IF length > best_len                  // strict: ties keep the first
            best_start ← left + 1
            best_len ← length
    RETURN s[best_start..best_start + best_len - 1]
```

Each of the `2n - 1` centers expands at most about `n / 2` times, so the scan is `O(n²)` time in the worst case (one letter repeated) and `O(1)` extra space. Reach for it when a problem says palindromic substring: contiguous, with `n` in the low thousands. The same loop counts every palindromic substring if it adds one per successful expansion step, because each step uncovers exactly one new palindrome. Manacher's algorithm gets to `O(n)` by starting each expansion part of the way out, using the mirror image of a palindrome already found; it is rarely expected in an interview. A palindromic subsequence is not contiguous and needs dynamic programming instead. The classic mistake is expanding only around characters, which misses every even-length palindrome and returns `c` for `cbbd` instead of `bb`; the other is an off-by-one when turning the overshot arms back into a window.

*Practice:* LC 5 Longest Palindromic Substring · LC 647 Palindromic Substrings · LC 516 Longest Palindromic Subsequence

```{=latex}
\clearpage
```

## 66. Encode and Decode Strings {#a66}

```{=latex}
\markright{66. Encode and Decode Strings}
```

[Length-Prefix Framing · Strings · Tier 2]{.meta}

Design `encode`, which packs a list of strings into a single string, and `decode`, which recovers exactly the same list. The strings may contain any character, `#` and digits included. `["ab#", "12", ""]` encodes to `3#ab#2#120#` and decodes back to the same three strings.

The obvious scheme puts a delimiter between the strings and splits on it, and it breaks the moment a string contains the delimiter: joining with `#` turns `["ab#", "12", ""]` into `ab##12#`, which splits back into four strings. It cannot even tell `[]` from `[""]`, since both join to the empty string. Escaping can patch it, at the price of inspecting and rewriting every character on both sides. Framing sidesteps the question. Write each string's length in front of it, then a `#` that ends the length field, then the string itself. The decoder reads digits up to the first `#`, which is unambiguous because a length is made only of digits, and then takes exactly that many characters without looking at them.

Picture the encoded string as a train of boxes, each with a label on its front that says how long the box is. The decoder reads a label, steps over the whole box, and lands on the next label. A `#` or a digit inside a payload is never read as structure, because the decoder jumps over payloads instead of scanning them.

```text
encode   "ab#" → 3#ab#      "12" → 2#12      "" → 0#

data     3 # a b # 2 # 1 2 0 #
index    0 1 2 3 4 5 6 7 8 9 10

i = 0    digits "3", '#' at j = 1    take data[2..4] = "ab#"   next i = 5
i = 5    digits "2", '#' at j = 6    take data[7..8] = "12"    next i = 9
i = 9    digits "0", '#' at j = 10   take nothing      = ""    next i = 11
i = 11 = len(data): stop             → ["ab#", "12", ""]

the '#' at index 4 sits inside a payload: the decoder steps over it unread
```

```pseudo
FUNCTION Encode(strs)
    parts ← empty list
    FOR EACH s IN strs
        parts.append(str(len(s)) + "#" + s)   // length, '#', then s itself
    RETURN join(parts)                        // concatenate once at the end

FUNCTION Decode(data)
    strs ← empty list
    i ← 0
    WHILE i < len(data)
        j ← i
        WHILE data[j] ≠ "#"                   // the length ends at a '#'
            j ← j + 1
        length ← int(data[i..j - 1])
        strs.append(data[j + 1..j + length])  // exactly length characters
        i ← j + 1 + length                    // jump over the payload unread
    RETURN strs
```

Both directions touch every character a constant number of times, so encoding and decoding take `O(total length)` time and space; collect the pieces in a list and join once, because `+=` in a loop can recopy the growing string every time. Reach for length-prefix framing whenever several values must travel through one string or one stream and come back intact: serializing a list or a record, or messages on a network socket. Serializing a binary tree (#55) is the same contract with the shape recorded by null markers, and the TinyURL design meets it with a counter and a map. The classic mistake is a pure delimiter, which passes the examples until a string contains it; the subtler one is reading a single digit as the length, which breaks on the first string of ten or more characters.

*Practice:* LC 271 Encode and Decode Strings · LC 535 Encode and Decode TinyURL · LC 297 Serialize and Deserialize Binary Tree

```{=latex}
\clearpage
```

## 67. Fibonacci {#a67}

```{=latex}
\markright{67. Fibonacci}
```

[Recursion, Memo, Iteration, Fast Doubling · Math · Tier 2]{.meta}

The Fibonacci numbers start with `F(0) = 0` and `F(1) = 1`, and every later term is the sum of the two before it: `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55`. Given `n`, compute `F(n)`; for example `F(5) = 5` and `F(10) = 55`.

The definition is already an algorithm, and a famously slow one. Each call makes two more calls, so the calls form a binary tree with `2F(n + 1) - 1` nodes, a count that grows like `1.618^n`, and the same subproblems sit in it over and over: computing `F(5)` solves `F(3)` twice and `F(2)` three times. Memoization stores each answer the first time it is computed, and every later request becomes a lookup. The tree collapses to its left edge, with each `F(k)` computed once, at the cost of an `O(n)` map and a call stack `n` frames deep.

The loop keeps only what the recurrence still needs. Every new term reads just the two before it, so a window of two numbers slides along the sequence: `(prev, curr) = (F(i), F(i + 1))` becomes `(F(i + 1), F(i + 2))` in each step, and after `n` steps `prev` is `F(n)`. Fast doubling stops walking and starts jumping. From the pair `(F(k), F(k + 1))` the identities `F(2k) = F(k)(2F(k + 1) - F(k))` and `F(2k + 1) = F(k)² + F(k + 1)²` land directly on position `2k` or `2k + 1`, so the recursion halves `n` on the way down and rebuilds one bit of `n` per level on the way back up. Both identities fall out of squaring a power of the matrix `[[1, 1], [1, 0]]`, whose powers hold consecutive Fibonacci numbers, which makes this the same halving trick as fast exponentiation (#93).

```text
plain recursion for F(5): 15 calls, F(3) twice, F(2) three times
                         F(5)
               ┌──────────┴───────────┐
              F(4)                   F(3)
        ┌──────┴──────┐           ┌───┴────┐
       F(3)          F(2)        F(2)     F(1)
    ┌───┴────┐     ┌──┴──┐     ┌──┴──┐
   F(2)     F(1)  F(1)  F(0)  F(1)  F(0)
 ┌──┴──┐
F(1)  F(0)

memo      9 calls: 5 4 3 2 1 0 1 2 3 (the second 2 and 3 are lookups)
loop      (prev, curr) = (0,1) (1,1) (1,2) (2,3) (3,5) (5,8) → F(5) = 5
doubling  n = 10 → 5 → 2 → 1 → 0, then (F(k), F(k + 1)) climbs back:
          (0,1) → (1,1) → (1,2) → (5,8) → (55,89) → F(10) = 55
```

```pseudo
FUNCTION FibNaive(n)
    IF n < 2
        RETURN n
    RETURN FibNaive(n - 1) + FibNaive(n - 2)  // two calls per call

FUNCTION FibMemo(n, memo)
    IF n < 2
        RETURN n
    IF n IN memo
        RETURN memo[n]                  // solved before: skip the whole subtree
    memo[n] ← FibMemo(n - 1, memo) + FibMemo(n - 2, memo)
    RETURN memo[n]

FUNCTION FibIter(n)
    prev ← 0
    curr ← 1
    FOR i FROM 0 TO n - 1               // prev = F(i), curr = F(i + 1)
        nxt ← prev + curr
        prev ← curr
        curr ← nxt
    RETURN prev

FUNCTION FibPair(n)                     // returns (F(n), F(n + 1))
    IF n = 0
        RETURN (0, 1)
    (a, b) ← FibPair(floor(n / 2))      // a = F(k), b = F(k + 1)
    even ← a * (2 * b - a)              // F(2k)
    odd ← a * a + b * b                 // F(2k + 1)
    IF n mod 2 = 0
        RETURN (even, odd)
    RETURN (odd, even + odd)            // n = 2k + 1: one step further

FUNCTION FibFast(n)
    pair ← FibPair(n)
    RETURN pair[0]
```

The plain recursion costs exponential time, memoization `O(n)` time and space, the loop `O(n)` time and `O(1)` space, and fast doubling `O(log n)` arithmetic steps, one per bit of `n`; `F(n)` has about `0.69n` bits, so for huge `n` the big-integer multiplications set the real cost. Reach for the two-variable loop whenever each state depends only on the previous two: Climbing Stairs counts the ways to reach step `n` as the ways to reach `n - 1` plus the ways to reach `n - 2`, which is `F(n + 1)`, and Tribonacci slides a window of three. The classic mistake is presenting the plain recursion as the answer in an interview, where `F(50)` already takes about 40 billion calls; the second is memoizing in Python and hitting the default recursion limit near `n = 1000`, which the loop never touches.

*Practice:* LC 509 Fibonacci Number · LC 70 Climbing Stairs · LC 1137 N-th Tribonacci Number

```{=latex}
\clearpage
```

## 68. Single Number {#a68}

```{=latex}
\markright{68. Single Number}
```

[XOR Cancels Pairs · Bit Manipulation · Tier 2]{.meta}

Every element of a non-empty integer array appears exactly twice except one, which appears once; find that one in linear time with constant extra space. In `[4, 1, 2, 1, 2]` the answer is `4`.

Counting with a hash map works but costs `O(n)` space, and sorting to find the element without a twin costs `O(n log n)` time. XOR does it in one pass with one integer, thanks to three facts: `x XOR x = 0`, `x XOR 0 = x`, and XOR is commutative and associative, so the order of the terms does not matter. XOR the whole array together. The terms can be regrouped so that each pair sits side by side, every pair collapses to 0, and the lone element is all that remains. In Python the operator is `^`.

Geometrically, stack the numbers in binary, one per row. XOR works on each bit column separately: a column's result is 1 exactly when it holds an odd number of ones. A pair adds two ones or none to every column, so it never changes a column's parity, and the parities that remain spell out the single number.

```text
               bit 2 1 0   result after the XOR
value 4            1 0 0   100
value 1            0 0 1   101
value 2            0 1 0   111
value 1            0 0 1   110
value 2            0 1 0   100
ones per column    1 2 2   odd, even, even: the single is 100 = 4

missing number in [3, 0, 1], starting from n = 3:
XOR in   i=0  v=3  i=1  v=0  i=2  v=1
result    3    0    1    1    3    2      0, 1 and 3 cancel; 2 is left
```

```pseudo
FUNCTION SingleNumber(nums)
    result ← 0
    FOR EACH value IN nums
        result ← result XOR value          // a pair cancels to 0
    RETURN result

FUNCTION MissingNumber(nums)
    result ← len(nums)                     // index n has no slot of its own
    FOR i FROM 0 TO len(nums) - 1
        result ← result XOR i              // value v cancels against index v
        result ← result XOR nums[i]
    RETURN result
```

One pass, `O(n)` time and `O(1)` space. The same cancellation finds the missing number in an array that holds `0..n` with one value absent (LC 268): XOR every index and every value, starting from n, the one index without a slot; each present value cancels against the index equal to it, wherever it sits, and the missing one has no partner. Find the Difference (LC 389) is the same trick on character codes. When two numbers are single (LC 260), the XOR of everything is `a XOR b`, which is not 0; its lowest set bit (`x & -x`, from #98) is a bit where a and b differ, so splitting the array by that bit puts them in different halves, and XOR-ing each half yields each one. XOR cancels pairs only: when the others appear three times (LC 137), count each bit modulo 3 instead. The classic mistake in Missing Number is starting from 0 instead of n: the result is then the missing value XOR n, so `[3, 0, 1]` gives `1` instead of `2`.

*Practice:* LC 136 Single Number · LC 268 Missing Number · LC 389 Find the Difference · LC 260 Single Number III

```{=latex}
\clearpage
```

## 69. Insert Delete GetRandom O(1) {#a69}

```{=latex}
\markright{69. Insert Delete GetRandom O(1)}
```

[Array + Index Map, Swap with Last · Design · Tier 2]{.meta}

Design a set of integers with three operations, `insert(val)`, `remove(val)` and `get_random()`, each in average `O(1)` time. Insert and remove return whether the set changed, and `get_random` returns every stored value with the same probability. After inserting `10`, `20` and `30` and removing `10`, the set holds `30` and `20`, and `get_random` returns each of them half the time.

Neither familiar structure delivers all three. A hash set inserts and removes in `O(1)` but cannot pick a random member without walking to it, `O(n)`; a plain list picks a random index in `O(1)` but needs an `O(n)` search to refuse a duplicate or to find a value, and deleting from its middle shifts the whole tail left, `O(n)` again. The design keeps both. A list `values` stays packed from index `0` with no holes, so a uniformly random index is a uniformly random value, and a map `index_of` sends each value to its slot, so finding a value is one lookup. Insertion appends and records the new slot. Removal is the one clever step: deleting from the middle would open a hole, and closing it by shifting is exactly the cost to avoid, so the last value jumps into the hole, its map entry is corrected, and the tail slot is popped. A set has no order to preserve, which is what makes the jump legal.

Picture the list as a row of tiles. A removal never slides the row; the rightmost tile fills the gap and the row shrinks by one from the right. After every operation `index_of[values[i]] = i` holds for every slot `i`, and there is exactly one slot per key.

```text
                         values          index_of
insert 10, 20, 30        [10, 20, 30]    {10: 0, 20: 1, 30: 2}
remove(10)               i = 0 (the slot of 10), last = 30
  last into slot 0       [30, 20, 30]    {10: 0, 20: 1, 30: 0}
  pop tail, delete 10    [30, 20]        {20: 1, 30: 0}
get_random               RandomInt(0, 1) → slot 0 or 1 → 30 or 20, half each
```

```pseudo
CLASS RandomizedSet
    FUNCTION Init()
        self.values ← empty list              // packed from index 0, no holes
        self.index_of ← empty map             // value → its slot in values

    FUNCTION Insert(val)
        IF val IN self.index_of
            RETURN false
        self.index_of[val] ← len(self.values)
        self.values.append(val)
        RETURN true

    FUNCTION Remove(val)
        IF val NOT IN self.index_of
            RETURN false
        i ← self.index_of[val]
        last ← self.values[len(self.values) - 1]
        self.values[i] ← last                 // the last value fills the hole
        self.index_of[last] ← i               // and learns its new slot
        self.values.pop()                     // drop the tail slot
        self.index_of.remove(val)             // only now: last may be val
        RETURN true

    FUNCTION GetRandom()
        i ← RandomInt(0, len(self.values) - 1)    // uniform, both ends included
        RETURN self.values[i]
```

Every operation is a constant number of hash-map steps plus work at the end of the list, so each costs `O(1)` on average (hashing gives the average; appending and popping the end are amortized `O(1)`), and the structure takes `O(n)` space. Reach for it whenever a problem wants uniform random sampling from a collection that changes, or an `O(1)` delete from an array whose order does not matter; it is the same pairing of a map with a structure the map points into that powers the LRU cache of #35. With duplicates allowed (LC 381) the map holds a set of slots for each value and removal takes any one of them, with the same jump of the last tile. The classic mistake is deleting `val` from the map before correcting the moved value's slot: when `val` is itself the last value, the correction writes it straight back, leaving a ghost key that points past the end of the list, and a later `insert(val)` wrongly returns false.

*Practice:* LC 380 Insert Delete GetRandom O(1) · LC 381 Insert Delete GetRandom O(1) - Duplicates allowed · LC 710 Random Pick with Blacklist

```{=latex}
\clearpage
```

## 70. Time-Based Key-Value Store {#a70}

```{=latex}
\markright{70. Time-Based Key-Value Store}
```

[Per-Key Timestamp Lists + Binary Search · Design · Tier 2]{.meta}

Design a store that keeps every version of a key. `set(key, value, timestamp)` records a value at a time, with the timestamps of each key arriving in increasing order, and `get(key, timestamp)` returns the value set at the largest time `≤ timestamp`, or the empty string if the key had no value yet. After setting `status` to `draft` at time `1`, `review` at `4` and `live` at `9`, `get("status", 5)` is `"review"` and `get("status", 0)` is `""`.

The brute force keeps one log of every `set` call and scans all of it on each `get`, `O(n)` per query. The order in which versions arrive is the gift: because the timestamps of a key only grow, appending to that key's list keeps it sorted for free, and a sorted list answers "the last time at or before `t`" by binary search. Each key therefore owns two parallel lists, the times and the values set at those times; `set` appends to both and `get` searches the times. The search finds the first time strictly after `t`, the upper bound, and steps one slot to the left, where the newest version that already existed at time `t` sits. If the upper bound is slot `0`, every version is newer than `t` and the answer is empty.

Picture each key as a timeline with a dot at every version. A query drops a pin at time `t` and walks left to the nearest dot. The binary search keeps every slot before `left` at or before `t` and every slot from `right` on after it, and halves the unknown gap between them until it closes.

```text
           draft          review                   live
time ─┼────●──────────────●────┼───────────────────●─────────→
      0    1              4    5                   9
                               ▲ get("status", 5) walks left to the dot at 4
get("status", 5): left = 0, right = 3
  mid = 1: time 4 ≤ 5 → left = 2
  mid = 2: time 9 > 5 → right = 2
  the first time after 5 is slot 2, so the answer is slot 1 → "review"
get("status", 0): every time is after 0, left stays 0 → ""
```

```pseudo
CLASS TimeMap
    FUNCTION Init()
        self.times ← empty map                // key → increasing set times
        self.values ← empty map               // key → values, in the same order

    FUNCTION Set(key, value, timestamp)
        IF key NOT IN self.times
            self.times[key] ← empty list
            self.values[key] ← empty list
        self.times[key].append(timestamp)     // times only grow: stays sorted
        self.values[key].append(value)

    FUNCTION Get(key, timestamp)
        IF key NOT IN self.times
            RETURN ""
        times ← self.times[key]
        left ← 0
        right ← len(times)
        WHILE left < right                    // find the first time > timestamp
            mid ← floor((left + right) / 2)
            IF times[mid] ≤ timestamp
                left ← mid + 1                // mid is not after timestamp
            ELSE
                right ← mid                   // mid is after: maybe the first
        IF left = 0
            RETURN ""                         // every version is newer
        RETURN self.values[key][left - 1]
```

`set` costs amortized `O(1)` and `get` costs `O(log n)` for a key with `n` versions, because each step halves the gap; the store keeps every version, so space is linear in the number of `set` calls. The signals are values that change over time and questions asked "as of" a moment: versioned configs, snapshots, prices or election leaders at a time. The search is the lower-bound template of #9 with `≤` in place of `<`, which turns lower bound into upper bound, and Snapshot Array (LC 1146) is the same structure with one timeline per index and snapshot ids as times. If timestamps could arrive out of order, appending would break the sorting and each key would need a balanced search tree (a `TreeMap` in Java) instead of a list. The classic mistake is forgetting the `left = 0` case: Python then reads `values[-1]` and silently returns the newest version for a time before the first one.

*Practice:* LC 981 Time Based Key-Value Store · LC 1146 Snapshot Array · LC 911 Online Election

# Tier 3 · Good to Know {#tier3}

```{=latex}
\markboth{Tier 3 · Good to Know}{}
```

The last thirty round out the set: second implementations of ideas you already own (open addressing, heap sort, Prim), the string toolkit, number theory, geometry, bit tricks and the designs that turn up in senior loops. Read each one once, keep its picture in mind, and come back to it when a problem calls for it.

```{=latex}
\clearpage
```

## 71. Hash Map with Open Addressing {#a71}

```{=latex}
\markright{71. Hash Map with Open Addressing}
```

[Linear Probing and Tombstones · Hash Map Internals · Tier 3]{.meta}

Design a hash map without a built-in dictionary that stores every pair directly in one array of slots, with no chains: `put(key, value)`, `get(key)` returning `-1` for a missing key, and `remove(key)`. With 8 slots and integers hashing to themselves, key `3` lives in slot `3`; key `11` also hashes to slot `3`, finds it taken and settles in slot `4`, so after `put(3, 30)` and `put(11, 110)` the call `get(11)` returns `110`.

Separate chaining (#36) hangs a list off every bucket. Open addressing keeps one flat array and resolves a collision, a slot already holding a different key, by probing: try the home slot `hash(key) mod capacity`, then the next slot, and the next, wrapping around the end. A key therefore sits somewhere on the unbroken run of non-empty slots that starts at its home, and a search walks that run until it meets the key or an EMPTY slot. An EMPTY slot ends the search, because an insert of the key would have stopped there; the key cannot lie beyond it.

Deletion is the subtle part. Emptying a slot would cut a run in two and strand every key whose path crosses the gap, so `remove` writes a DELETED marker, a tombstone, that searches step over and inserts may reuse: once a full search has shown that a key is absent, `put` takes the first tombstone or EMPTY slot on its path. Tombstones lengthen searches just like live keys, so the load counts both, and when `(size + tombstones) / capacity` passes 0.5 the table doubles and re-puts only its live pairs, which sweeps the tombstones away. The table stays half empty because of primary clustering: occupied slots merge into runs, a key whose home falls anywhere inside a run lands at its end, and so long runs catch more keys and grow faster still. A miss inspects about 2.5 slots on average at load 0.5, but dozens at load 0.9.

```text
8 slots, home = key mod 8                · EMPTY     X tombstone
               slot   0    1    2    3    4    5    6    7
put 3                 ·    ·    ·    3    ·    ·    ·    ·    home 3
put 11                ·    ·    ·    3   11    ·    ·    ·    3 taken → 4
put 19                ·    ·    ·    3   11   19    ·    ·    3, 4 taken → 5
put 4                 ·    ·    ·    3   11   19    4    ·    home 4 → 6
remove 11             ·    ·    ·    3    X   19    4    ·
get 19:    slot 3 holds 3, slot 4 is X so keep going, slot 5 holds 19 → 190
put 27:    the search passes 3, X, 19, 4 and stops at EMPTY slot 7: absent;
           the first free slot on its path is the tombstone in slot 4
put 27                ·    ·    ·    3   27   19    4    ·
put 12:    lands in slot 7; load (5 + 0) / 8 = 0.625 > 0.5 → 16 slots,
           live keys re-put: 3 → 3, 19 → 4, 4 → 5, 27 → 11, 12 → 12
```

```pseudo
CLASS ProbingHashMap                // a slot: EMPTY, DELETED or [key, value]
    FUNCTION Init(capacity)
        self.capacity ← capacity
        self.size ← 0                       // live keys
        self.tombstones ← 0                 // DELETED slots
        self.slots ← array of capacity copies of EMPTY

    FUNCTION Find(key)                      // index of key's slot, or -1
        index ← hash(key) mod self.capacity
        WHILE self.slots[index] ≠ EMPTY
            slot ← self.slots[index]
            IF slot ≠ DELETED AND slot[0] = key
                RETURN index
            index ← (index + 1) mod self.capacity    // taken: try the next
        RETURN -1

    FUNCTION Put(key, value)
        index ← self.Find(key)
        IF index ≠ -1
            self.slots[index][1] ← value             // already stored
            RETURN
        index ← hash(key) mod self.capacity
        WHILE self.slots[index] ≠ EMPTY AND self.slots[index] ≠ DELETED
            index ← (index + 1) mod self.capacity    // skip live pairs
        IF self.slots[index] = DELETED
            self.tombstones ← self.tombstones - 1    // reuse the tombstone
        self.slots[index] ← [key, value]
        self.size ← self.size + 1
        IF (self.size + self.tombstones) / self.capacity > 0.5
            self.Resize()

    FUNCTION Get(key)
        index ← self.Find(key)
        IF index = -1
            RETURN -1
        RETURN self.slots[index][1]

    FUNCTION Remove(key)
        index ← self.Find(key)
        IF index ≠ -1
            self.slots[index] ← DELETED     // later searches step over it
            self.size ← self.size - 1
            self.tombstones ← self.tombstones + 1

    FUNCTION Resize()
        old_slots ← self.slots
        self.capacity ← 2 * self.capacity
        self.slots ← array of self.capacity copies of EMPTY
        self.size ← 0
        self.tombstones ← 0
        FOR EACH slot IN old_slots
            IF slot ≠ EMPTY AND slot ≠ DELETED
                self.Put(slot[0], slot[1])  // tombstones are dropped
```

With a good hash and the load capped at one half, every operation takes `O(1)` expected time; the worst case is `O(n)`, one run through the whole table, and a resize costs `O(n)` but is amortized away as in #36. One flat array of pairs and no pointers keeps the table compact and friendly to the cache; CPython's `dict` is an open-addressing table too, though it scrambles the probe order instead of stepping by one. The signals are a design question about hash map internals, or a follow-up asking how a map works without linked lists. The classic mistake is a `remove` that writes EMPTY: after removing `11` from the cluster in the picture, `get(19)` stops at the hole in slot 4 and reports `-1`.

*Practice:* LC 706 Design HashMap · LC 705 Design HashSet

```{=latex}
\clearpage
```

## 72. Boyer-Moore Majority Vote {#a72}

```{=latex}
\markright{72. Boyer-Moore Majority Vote}
```

[Different Votes Cancel in Pairs · Arrays & Hashing · Tier 3]{.meta}

Given an array, return the value that appears more than `n / 2` times, or report that none does, using `O(n)` time and `O(1)` extra space. In `[2, 2, 1, 1, 1, 2, 2]` the answer is `2`, with 4 of the 7 votes.

A hash map of counts finds it in `O(n)` time but `O(n)` space, and sorting puts it at the middle index in `O(n log n)`. Boyer-Moore needs two variables. Treat every element as a vote and let any two different votes cancel each other. A majority value has more votes than all the other values combined, so even if every other vote is spent cancelling one of its own, some of its votes survive. The scan keeps a `candidate` and the `count` of its uncancelled votes: when `count` is 0 the current value takes over as candidate, an equal value adds a vote, and a different value cancels one.

The count is a walk that returns to zero whenever the votes seen so far pair off completely. Cut the array at those points. In every closed piece the candidate holds exactly half the votes, so the true majority, which holds more than half of the whole array, must hold more than half of the final open piece, and there it is the candidate. The guarantee runs one way only: without a majority the survivor is just the last value standing, and `[1, 2, 3]` returns `3`. So when the problem does not promise a majority, a second pass counts the candidate's votes and accepts it only above `n / 2`.

```text
x            2  2  1  1  │  1  2  │  2
candidate    2  2  2  2  │  1  1  │  2
count        1  2  1  0  │  1  0  │  1
cut where count hits 0: each closed piece is half candidate, half others
survivor 2; second pass: 2 appears 4 times, 4 > 7 / 2, so 2 is the majority
```

```pseudo
FUNCTION MajorityCandidate(nums)
    candidate ← null
    count ← 0                              // candidate votes not yet cancelled
    FOR EACH x IN nums
        IF count = 0
            candidate ← x                  // nobody standing: x takes over
            count ← 1
        ELSE IF x = candidate
            count ← count + 1              // one more vote for the candidate
        ELSE
            count ← count - 1              // x cancels one candidate vote
    RETURN candidate

FUNCTION MajorityElement(nums)
    candidate ← MajorityCandidate(nums)
    votes ← 0
    FOR EACH x IN nums
        IF x = candidate
            votes ← votes + 1
    IF votes * 2 > len(nums)
        RETURN candidate
    RETURN null                            // no value holds a strict majority
```

Two linear passes give `O(n)` time with `O(1)` space. Reach for vote cancelling when a problem asks for a value that dominates an array or a stream in constant memory. The idea generalizes: at most two values can each appear more than `n / 3` times, so Majority Element II keeps two candidates with two counts, lets a value that matches neither and finds no empty slot cancel one vote from each, and verifies both at the end. The classic mistake is trusting the candidate without the second pass when no majority is promised; the check must also demand strictly more than half, since in `[1, 2]` neither value is a majority.

*Practice:* LC 169 Majority Element · LC 229 Majority Element II · LC 1150 Check If a Number Is Majority Element in a Sorted Array

```{=latex}
\clearpage
```

## 73. Median of K Sorted Arrays {#a73}

```{=latex}
\markright{73. Median of K Sorted Arrays}
```

[Binary Search on the Value · Binary Search · Tier 3]{.meta}

Given `k` sorted arrays of integers holding `N ≥ 1` values in total, return the median of all of them: the middle value when `N` is odd, the average of the two middle values when `N` is even. For `[1, 4, 9]`, `[2, 3, 7, 10]` and `[5, 8]` the nine values in order are `1 2 3 4 5 7 8 9 10`, so the median is `5`.

The brute force merges the arrays with a min-heap of their front elements (#14) and pops until it reaches the middle, `O(N log k)`. The faster idea stops hunting for a position and searches for a value instead. Ask of any integer `v`: how many values are at most `v`? Each array answers with one upper-bound binary search (#9), and the sum over all arrays is a count that never shrinks as `v` grows. So the question "are at least `r` values at most `v`?" reads ✗ ✗ ✗ then ✓ ✓ ✓ along the number line, and the `r`-th smallest value is the first ✓, found by binary search on the answer (#10) between the smallest first element and the largest last element.

That first ✓ is always a real element of some array, because the count changes only at values that appear in the arrays: if `v` were absent, `v - 1` would have the same count and would be an earlier ✓. The median then takes one or two of these order statistics, counted from 1: rank `⌊N / 2⌋ + 1` when `N` is odd, and the average of ranks `⌊N / 2⌋` and `⌊N / 2⌋ + 1` when it is even.

```text
[1, 4, 9]  [2, 3, 7, 10]  [5, 8]: N = 9, so the median is the 5th smallest
value v          1   2   3   4   5   6   7   8   9  10
count(≤ v)       1   2   3   4   5   5   6   7   8   9
count ≥ 5?       ✗   ✗   ✗   ✗   ✓   ✓   ✓   ✓   ✓   ✓
                                 ▲ the first ✓ is 5, a real element

   lo   hi   mid   count(≤ mid), per array   ≥ 5?   move
    1   10     5    2 + 2 + 1 = 5             yes   hi ← 5
    1    5     3    1 + 2 + 0 = 3             no    lo ← 4
    4    5     4    2 + 2 + 0 = 4             no    lo ← 5
    5    5   lo = hi: the 5th smallest value is 5
```

```pseudo
FUNCTION CountAtMost(arr, value)        // upper bound (#9): values ≤ value
    lo ← 0
    hi ← len(arr)
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        IF arr[mid] ≤ value
            lo ← mid + 1
        ELSE
            hi ← mid
    RETURN lo

FUNCTION KthSmallest(arrays, rank)      // smallest v with count(≤ v) ≥ rank
    lo ← ∞
    hi ← -∞
    FOR EACH arr IN arrays
        IF len(arr) > 0
            lo ← min(lo, arr[0])                // smallest first element
            hi ← max(hi, arr[len(arr) - 1])     // largest last element
    WHILE lo < hi
        mid ← floor((lo + hi) / 2)
        count ← 0
        FOR EACH arr IN arrays
            count ← count + CountAtMost(arr, mid)
        IF count ≥ rank
            hi ← mid                    // mid already covers rank values
        ELSE
            lo ← mid + 1                // too few values are ≤ mid
    RETURN lo

FUNCTION MedianKSorted(arrays)
    total ← 0
    FOR EACH arr IN arrays
        total ← total + len(arr)
    IF total mod 2 = 1
        RETURN KthSmallest(arrays, floor(total / 2) + 1)
    low ← KthSmallest(arrays, floor(total / 2))
    high ← KthSmallest(arrays, floor(total / 2) + 1)
    RETURN (low + high) / 2
```

Each probe of the value search runs `k` binary searches of `O(log L)`, where `L` is the longest array, and the search halves the value range `R` every time, so the cost is `O(k log L log R)` time and `O(1)` extra space, no matter how many values sit before the middle. With few long arrays it beats the heap merge by far; for exactly two arrays, the partition search of #40 is tighter still. The same count-then-search pattern works on any sorted structure that can count the values at most `v` quickly, such as a sorted matrix, a multiplication table or the pairwise distances of a sorted array. The classic mistake is an off-by-one in the ranks: they count from 1, so the median of an odd `N` is rank `⌊N / 2⌋ + 1`, and rank `⌊N / 2⌋` returns the value just before it.

*Practice:* LC 4 Median of Two Sorted Arrays · LC 378 Kth Smallest Element in a Sorted Matrix · LC 719 Find K-th Smallest Pair Distance · LC 668 Kth Smallest Number in Multiplication Table

```{=latex}
\clearpage
```

## 74. Counting Sort {#a74}

```{=latex}
\markright{74. Counting Sort}
```

[Count, Prefix-Sum, Place · Sorting · Tier 3]{.meta}

Sort an array of integers whose values lie in a small range `[low, high]`, negatives included. `[2, -1, 3, 2, 0, -1]` becomes `[-1, -1, 0, 2, 2, 3]`.

Any sort that only compares pairs of values needs on the order of `n log n` comparisons in the worst case. Counting sort never compares: it uses each value as an array index. Count how often each value occurs in an array of `high - low + 1` slots, shifting by `low` so that the smallest value lands in slot 0 and negatives work. Then turn the counts into running totals: after the prefix sum, the slot of value v holds how many values are `≤ v`, which is exactly one past the last position v occupies in the sorted output. Finally walk the input from right to left; for each value, decrement its slot and write the value at that position.

Picture the output as a row of reserved seats. The prefix sums mark where each value's block of seats ends, and the copies of a value fill their block from the back. Because the input is read from the right, the last copy takes the last seat, so equal values keep their input order. That stability does not matter for bare integers, but it matters as soon as the integers are keys of larger records, and it is the whole reason radix sort works.

```text
nums = [2, -1, 3, 2, 0, -1]; low = -1, high = 3, so slot = value + 1
  value          -1    0    1    2    3
  count           2    1    0    2    1
  prefix sums     2    3    3    5    6      how many values are ≤ value
place from the right: decrement the slot, then write at it
  i = 5   -1    2 → 1   result[1] = -1      · -1  ·  ·  ·  ·
  i = 4    0    3 → 2   result[2] =  0      · -1  0  ·  ·  ·
  i = 3    2    5 → 4   result[4] =  2      · -1  0  ·  2  ·
  i = 2    3    6 → 5   result[5] =  3      · -1  0  ·  2  3
  i = 1   -1    1 → 0   result[0] = -1     -1 -1  0  ·  2  3
  i = 0    2    4 → 3   result[3] =  2     -1 -1  0  2  2  3
the 2 from index 0 sits before the 2 from index 3: input order kept
```

```pseudo
FUNCTION CountingSort(nums)
    IF len(nums) = 0
        RETURN empty list
    low ← min(nums)
    high ← max(nums)
    count ← array of high - low + 1 zeros  // count[v - low] is for value v
    FOR EACH value IN nums
        count[value - low] ← count[value - low] + 1
    FOR slot FROM 1 TO len(count) - 1      // now: how many values are ≤ it
        count[slot] ← count[slot] + count[slot - 1]
    result ← array of len(nums) zeros
    FOR i FROM len(nums) - 1 DOWNTO 0      // right to left keeps it stable
        value ← nums[i]
        count[value - low] ← count[value - low] - 1   // the last free seat
        result[count[value - low]] ← value
    RETURN result
```

A few passes over the n values and one over the `k = high - low + 1` slots give `O(n + k)` time and `O(n + k)` space. That beats `O(n log n)` only when k is not much larger than n; values spread over a range of a billion make the count array the bottleneck. Signals: small integer keys such as ages, grades or heights, or a tightly bounded value range in the constraints. Radix sort extends the idea to large keys: run a stable counting sort on the last digit, then on the next digit, up to the first. After the pass on digit d the numbers are sorted by their last d digits, because stability keeps the earlier order among numbers that tie on the new digit; with d digits in base b it costs `O(d(n + b))`, and it is the linear-time answer to Maximum Gap (LC 164). The classic mistake is forgetting the offset, sizing the count array `high + 1` and indexing it by the value itself: in Python a negative index does not fail, `count[-1]` silently counts into the last slot, and `[2, -1, 3, 2, 0, -1]` comes back as `[0, 2, 2, -1, 3, -1]`.

*Practice:* LC 912 Sort an Array · LC 1051 Height Checker · LC 274 H-Index · LC 164 Maximum Gap

```{=latex}
\clearpage
```

## 75. Heap Sort {#a75}

```{=latex}
\markright{75. Heap Sort}
```

[Build a Max-Heap, Swap the Max to the End · Sorting · Tier 3]{.meta}

Sort an array of integers in place, with `O(1)` extra space and an `O(n log n)` bound even in the worst case. `[4, 10, 3, 5, 1]` becomes `[1, 3, 4, 5, 10]`.

Selection sort finds the maximum, moves it to the end and repeats on the rest; each search is a linear scan, so it costs `O(n²)`. Heap sort is selection sort with a max-heap doing the search. First turn the array into a max-heap in place with the bottom-up build of Heapify (#41), mirrored so that every parent is at least its children and the maximum sits at index 0. Then repeat: swap `nums[0]` with `nums[end]`, the last slot of the heap, which drops the maximum into its final place; shrink the heap to `nums[0..end-1]`; and sift the new root down to restore the heap.

Picture a wall inside the array. Left of it is a max-heap that loses one slot per step; right of it is the sorted tail, which gains one. Each swap carries the largest value still in the heap across the wall, so the tail fills from the right in decreasing order. The heap lives in the very array it sorts, which is why no extra space is needed.

```text
build, i = 1 then 0:   4 10 3 5 1  →  10 5 3 4 1     max-heap, max at 0
  end   swap        after the swap     after the sift-down   (│ = wall)
   4    10 and 1    1 5 3 4 │ 10       5 4 3 1 │ 10
   3     5 and 1    1 4 3 │ 5 10       4 1 3 │ 5 10
   2     4 and 3    3 1 │ 4 5 10       3 1 │ 4 5 10
   1     3 and 1    1 │ 3 4 5 10       1 │ 3 4 5 10
```

```pseudo
FUNCTION SiftDown(nums, i, n)              // max-heap on nums[0..n-1]
    WHILE true
        largest ← i
        left ← 2 * i + 1
        right ← 2 * i + 2
        IF left < n AND nums[left] > nums[largest]
            largest ← left
        IF right < n AND nums[right] > nums[largest]
            largest ← right
        IF largest = i                     // no child is larger: done
            RETURN
        swap(nums[i], nums[largest])
        i ← largest

FUNCTION HeapSort(nums)
    n ← len(nums)
    FOR i FROM floor(n / 2) - 1 DOWNTO 0   // build: last parent to root
        SiftDown(nums, i, n)
    FOR end FROM n - 1 DOWNTO 1
        swap(nums[0], nums[end])           // the max joins the sorted tail
        SiftDown(nums, 0, end)             // the heap is nums[0..end-1]
    RETURN nums
```

The build is `O(n)` and each of the n - 1 sift-downs costs `O(log n)`, so heap sort is `O(n log n)` in the worst case, with `O(1)` extra space because sift-down is a loop. It is not stable: the swap from the root to the end carries a value past others equal to it. In practice it loses to quick sort (#12), because sift-down jumps from `i` to `2i + 1` across memory and caches dislike that; its niche is the guarantee, which is why introsort, behind most C++ `std::sort` implementations, switches to heap sort when quick sort recurses too deep. Signals: an in-place sort with a worst-case bound, or only the top of the order, since after k swaps the tail holds the k largest values in sorted order. The classic mistake is sifting with `n` instead of `end` after the swap: the sift sees the maximum just parked at `nums[end]` as a child and pulls it back into the heap, and the example comes back as `[10, 5, 3, 4, 1]`, still a heap and not sorted.

*Practice:* LC 912 Sort an Array · LC 215 Kth Largest Element in an Array

```{=latex}
\clearpage
```

## 76. Circular Queue {#a76}

```{=latex}
\markright{76. Circular Queue}
```

[Ring Buffer with Head and Count · Queues · Tier 3]{.meta}

Design a first-in, first-out queue of fixed capacity on a single array: `enqueue(value)` and `dequeue()` return `true` or `false` for success, `front()` and `rear()` return the oldest and the newest value or `-1` when the queue is empty, and `is_empty()` and `is_full()` report the state. With capacity 3, after enqueueing 1, 2 and 3 the queue is full and enqueueing 4 fails; after one dequeue the 4 fits, and then `front()` is `2` and `rear()` is `4`.

An array queue that shifts every value left on each dequeue pays `O(n)` per dequeue, and one that only moves its start forward runs off the end of the array while the slots behind it sit empty. The ring buffer bends the array into a circle: slot `capacity - 1` is followed by slot `0`, and every index is taken modulo the capacity. Two numbers describe the whole queue: `head`, the slot of the oldest value, and `count`, how many values are stored. The values fill `count` consecutive slots of the circle starting at `head`, so the next free slot is `tail = (head + count) mod capacity` and the newest value sits just before it. Enqueue writes at the tail and increments `count`. Dequeue steps `head` forward one slot and decrements `count`, leaving the old value behind to be overwritten later. Nothing ever moves.

Storing `count` instead of a second index is the heart of this design. With only `head` and `tail`, an empty queue and a full queue look identical, `head = tail`, as the start and the third enqueue below show; the usual alternatives are exactly this count or one slot left permanently unused.

```text
capacity 3       slot  0    1    2    head  count   tail
start                  ·    ·    ·       0      0      0    empty: head = tail
enqueue 1 → true       1    ·    ·       0      1      1
enqueue 2 → true       1    2    ·       0      2      2
enqueue 3 → true       1    2    3       0      3      0    full: head = tail
enqueue 4 → false      1    2    3       0      3      0    count = capacity
dequeue   → true      (1)   2    3       1      2      0    head steps on
enqueue 4 → true       4    2    3       1      3      1    4 wrapped to slot 0
front = items[1] = 2    rear = items[(1 + 3 - 1) mod 3] = items[0] = 4
· never written    (1) an old value left behind, free to overwrite
```

```pseudo
CLASS CircularQueue
    FUNCTION Init(capacity)
        self.items ← array of capacity zeros
        self.capacity ← capacity
        self.head ← 0                       // slot of the front value
        self.count ← 0                      // how many values are stored

    FUNCTION Enqueue(value)
        IF self.IsFull()
            RETURN false
        tail ← (self.head + self.count) mod self.capacity    // wraps to 0
        self.items[tail] ← value
        self.count ← self.count + 1
        RETURN true

    FUNCTION Dequeue()
        IF self.IsEmpty()
            RETURN false
        self.head ← (self.head + 1) mod self.capacity    // old value stays
        self.count ← self.count - 1
        RETURN true

    FUNCTION Front()
        IF self.IsEmpty()
            RETURN -1
        RETURN self.items[self.head]

    FUNCTION Rear()
        IF self.IsEmpty()
            RETURN -1
        RETURN self.items[(self.head + self.count - 1) mod self.capacity]

    FUNCTION IsEmpty()
        RETURN self.count = 0

    FUNCTION IsFull()
        RETURN self.count = self.capacity
```

Each operation is a constant amount of arithmetic, so all six run in `O(1)` time, and the queue takes `O(capacity)` space allocated once. The signals are a fixed-size buffer, a stream where only the last `k` items matter, such as a moving average, or a request to build a queue or deque without linked nodes. A circular deque adds insertion at the front by stepping `head` backward to `(head - 1 + capacity) mod capacity`, and Java's `ArrayDeque` is a ring buffer of the same kind that grows when it fills. The classic mistake is dropping a modulo: `tail = head + count` runs off the end of the array exactly when the ring should wrap, as in the last enqueue above, where `1 + 2 = 3` must become slot `0`.

*Practice:* LC 622 Design Circular Queue · LC 641 Design Circular Deque · LC 346 Moving Average from Data Stream

```{=latex}
\clearpage
```

## 77. Candy {#a77}

```{=latex}
\markright{77. Candy}
```

[Two Passes: Left, Then Right · Greedy · Tier 3]{.meta}

Children stand in a line, each with a rating. Every child gets at least one candy, and a child rated higher than a neighbor must get more candies than that neighbor. Return the fewest candies in total. For ratings `[1, 0, 2, 5, 4, 3, 1]` the answer is `15`, handed out as `[2, 1, 2, 4, 3, 2, 1]`.

Every rule looks at one side: a child against a lower neighbor on its left, or against a lower neighbor on its right. The brute force starts everyone at one candy and keeps sweeping, raising any child who breaks a rule, until a sweep changes nothing, which takes `O(n²)` time on a long slope. Two directed passes do it in linear time. Left to right, a child rated above its left neighbor gets one more candy than that neighbor; the neighbor was settled a step earlier, so every left rule holds after one pass. Right to left, a child rated above its right neighbor needs `candies[i + 1] + 1`, but it must keep what the left pass demanded, so it takes the larger of the two.

Why does the right pass not undo the left one? It raises `candies[i]` only when child `i` outranks its right neighbor. Raising `i` can only help the left rule at `i`, and the left rule at `i + 1` is silent, because that child is the lower one. The one rule a raise can disturb, between `i - 1` and `i`, is a right rule, repaired on the very next step of the same pass. Geometrically, read the ratings as a mountain profile: a child's count is the longer of the two strictly rising runs that climb to it, one from each side, so a peak takes the longer of its slopes. Every valid assignment needs at least those run lengths, so the sum is the minimum.

```text
rating 5                    ●           peak: max(3, 3 + 1) = 4
rating 4                         ●
rating 3                              ●
rating 2               ●
rating 1     ●                             ●
rating 0          ●
child        0    1    2    3    4    5    6
left pass    1    1    2    3    1    1    1    beat a lower left neighbor
right pass   2    1    2    4    3    2    1    max with right neighbor + 1
total 15
```

```pseudo
FUNCTION Candy(ratings)
    n ← len(ratings)
    candies ← array of n copies of 1       // everyone gets at least one
    FOR i FROM 1 TO n - 1                  // left to right
        IF ratings[i] > ratings[i - 1]     // beat a lower left neighbor
            candies[i] ← candies[i - 1] + 1
    FOR i FROM n - 2 DOWNTO 0              // right to left
        IF ratings[i] > ratings[i + 1]     // also beat a lower right neighbor
            candies[i] ← max(candies[i], candies[i + 1] + 1)
    RETURN sum(candies)
```

Two linear passes give `O(n)` time, with `O(n)` space for the counts. Reach for two opposite passes whenever each element's condition splits into a left half and a right half, each settled by a sweep in its own direction: the two wall arrays of Trapping Rain Water (#37), the prefix and suffix products of LC 238 and the run lengths of LC 2100 all have this shape. Equal neighbors impose nothing, so `[1, 2, 2]` needs only `4` candies, handed out as `[1, 2, 1]`. The classic mistake is a right pass that overwrites with `candies[i + 1] + 1` instead of taking the maximum: on `[1, 2, 3, 1]` it cuts the top child from 3 candies to 2, level with its lower left neighbor, and reports `6` instead of `7`.

*Practice:* LC 135 Candy · LC 42 Trapping Rain Water · LC 238 Product of Array Except Self · LC 2100 Find Good Days to Rob the Bank

```{=latex}
\clearpage
```

## 78. Hand of Straights {#a78}

```{=latex}
\markright{78. Hand of Straights}
```

[Start Every Group at the Smallest Card · Greedy · Tier 3]{.meta}

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

```{=latex}
\clearpage
```

## 79. N-Queens {#a79}

```{=latex}
\markright{79. N-Queens}
```

[Columns and Diagonals as Sets · Backtracking · Tier 3]{.meta}

Place n queens on an n × n chessboard so that no two attack each other along a row, a column or a diagonal, and return every such board as a list of strings, `Q` for a queen and `.` for an empty square. For `n = 4` there are two boards, `[".Q..", "...Q", "Q...", "..Q."]` and its mirror image `["..Q.", "Q...", "...Q", ".Q.."]`.

No two queens may share a row, so place exactly one queen per row, from top to bottom; the search only chooses a column for each row, and the row rule holds by construction. A square is safe when no earlier queen sits in its column, on its diagonal or on its anti-diagonal. Comparing against the earlier queens one by one costs `O(n)` per square; the trick is that every diagonal has a name. Along a down-right diagonal `r - c` stays constant, and along a down-left anti-diagonal `r + c` stays constant, so three sets, `cols`, `diags` and `anti_diags`, answer "is this square attacked?" with three lookups. Placing a queen adds its three names to the sets; backtracking removes them again.

The two grids below are the whole geometry of the problem. Every square carries two diagonal names, and two queens share a diagonal exactly when they share a name. Under them, the first board is built row by row, with the sets as the code holds them after each placement.

```text
r - c: one name per \ diagonal    r + c: one name per / diagonal
  c= 0  1  2  3                     c= 0  1  2  3
r=0  0 -1 -2 -3                   r=0  0  1  2  3
r=1  1  0 -1 -2                   r=1  1  2  3  4
r=2  2  1  0 -1                   r=2  2  3  4  5
r=3  3  2  1  0                   r=3  3  4  5  6

n = 4: row 0 col 0 dead-ends twice, then row 0 col 1 leads to a board
. Q . .   row 0 col 1   cols {1}           r-c {-1}            r+c {1}
. . . Q   row 1 col 3   cols {1, 3}        r-c {-2, -1}        r+c {1, 4}
Q . . .   row 2 col 0   cols {0, 1, 3}     r-c {-2, -1, 2}     r+c {1, 2, 4}
. . Q .   row 3 col 2   cols {0, 1, 2, 3}  r-c {-2, -1, 1, 2}  r+c {1, 2, 4, 5}
```

```pseudo
FUNCTION Draw(queens)
    n ← len(queens)
    board ← empty list
    FOR EACH col IN queens
        board.append("." × col + "Q" + "." × (n - 1 - col))
    RETURN board

FUNCTION Backtrack(n, row, queens, cols, diags, anti_diags, boards)
    IF row = n
        boards.append(Draw(queens))          // every row holds a queen
        RETURN
    FOR col FROM 0 TO n - 1
        IF col IN cols OR (row - col) IN diags OR (row + col) IN anti_diags
            CONTINUE                         // attacked
        queens.append(col)                   // place the queen
        cols.add(col)
        diags.add(row - col)
        anti_diags.add(row + col)
        Backtrack(n, row + 1, queens, cols, diags, anti_diags, boards)
        queens.pop()                         // remove it, undo all four marks
        cols.remove(col)
        diags.remove(row - col)
        anti_diags.remove(row + col)

FUNCTION SolveNQueens(n)
    boards ← empty list
    Backtrack(n, 0, empty list, empty set, empty set, empty set, boards)
    RETURN boards
```

With the column set alone, row r has at most `n - r` free columns, so the tree has at most `n!` leaves and the search is bounded by `O(n · n!)`, plus `O(n²)` to draw each board found; the diagonal sets prune far below that bound, and for n = 8 the search makes only 2,057 calls to find all 92 boards. The extra space is `O(n)` besides the output. When only the number of boards is asked (LC 52), keep the recursion and add 1 at `row = n` instead of drawing. The same idea of constraint sets, one per row, column and 3 × 3 box, drives Sudoku Solver (LC 37), and the three sets can also be three integers used as bitmasks (#99). The classic mistake is naming both diagonal directions with `r - c`: the anti-diagonals then go unchecked, and n = 4 returns 7 boards instead of 2.

*Practice:* LC 51 N-Queens · LC 52 N-Queens II · LC 37 Sudoku Solver

```{=latex}
\clearpage
```

## 80. Bipartite Check {#a80}

```{=latex}
\markright{80. Bipartite Check}
```

[BFS Two-Coloring · BFS · Tier 3]{.meta}

Given an undirected graph as an adjacency list, `graph[u]` holding the neighbors of `u`, decide whether its nodes can be split into two sides so that every edge runs between the sides and none runs inside one. A square is bipartite, with `{0, 2}` on one side and `{1, 3}` on the other; a triangle is not, because its three corners cannot alternate between two sides. So the graph made of a square `0-1-2-3` and a triangle `4-5-6`, `[[1, 3], [0, 2], [1, 3], [0, 2], [5, 6], [4, 6], [4, 5]]`, is not bipartite.

The brute force tries all `2^n` ways to assign the sides. But within a connected piece one choice forces all the others: once a node is put on side 0, each neighbor must go on side 1, and each of their neighbors on side 0. BFS spreads that forced choice layer by layer, giving every newly reached node `1 - color[node]`, the opposite of the node that reached it. An edge to a node already on the other side is consistent. An edge to a node on the same side is a contradiction that no recoloring can fix, because every color in the component was forced by the first one. The graph may be disconnected, so the outer loop starts a fresh BFS from every node still uncolored, and each component gets its own free first choice.

Picture the BFS layers as rings around the start, colored alternately. In the square the rings are `0`, then `1` and `3`, then `2`, and every edge joins two neighboring rings. In the triangle, `5` and `6` land on the same ring, and the edge between them stays inside it. That edge betrays an odd cycle, and bipartite means exactly no odd cycle: walking around any cycle switches sides at every step, so it returns home only after an even number of steps, while a same-colored edge plus the two BFS paths back to the start closes a walk of odd length, which always contains an odd cycle.

```text
  0 ── 1          4
  │    │         / \
  3 ── 2        5 ─ 6

start 0: color[0] ← 0
  pop 0   1 ← 1   3 ← 1
  pop 1   0 is 0 ✓   2 ← 0
  pop 3   0 is 0 ✓   2 is 0 ✓
  pop 2   1 is 1 ✓   3 is 1 ✓          the square splits {0, 2} | {1, 3}
start 4: color[4] ← 0
  pop 4   5 ← 1   6 ← 1
  pop 5   4 is 0 ✓   6 is 1, the same as 5 ✗   return false
```

```pseudo
FUNCTION IsBipartite(graph)
    n ← len(graph)
    color ← array of n copies of -1        // -1 uncolored, else side 0 or 1
    FOR start FROM 0 TO n - 1
        IF color[start] ≠ -1
            CONTINUE                       // colored by an earlier search
        color[start] ← 0                   // new component: either side
        queue ← empty queue
        queue.enqueue(start)
        WHILE queue is not empty
            node ← queue.dequeue()
            FOR EACH neighbor IN graph[node]
                IF color[neighbor] = -1
                    color[neighbor] ← 1 - color[node]   // the other side
                    queue.enqueue(neighbor)
                ELSE IF color[neighbor] = color[node]
                    RETURN false           // an edge inside one side
    RETURN true
```

Each node is colored once and each edge is examined from both ends, so the check costs `O(V + E)` time and `O(V)` space. Reach for two-coloring whenever a problem splits things into two groups under "these two must differ" constraints, such as the dislikes of Possible Bipartition, or asks whether a graph has an odd cycle. Flower Planting With No Adjacent is the many-color cousin: every garden has at most three neighbors, so choosing any flower its neighbors do not use always succeeds with four. The classic mistake is searching only from node `0`: that colors the square, never visits the triangle, and returns `true` for this graph.

*Practice:* LC 785 Is Graph Bipartite? · LC 886 Possible Bipartition · LC 1042 Flower Planting With No Adjacent

```{=latex}
\clearpage
```

## 81. Cycle Detection in an Undirected Graph {#a81}

```{=latex}
\markright{81. Cycle Detection in an Undirected Graph}
```

[DFS That Skips the Parent Edge · Cycle Detection · Tier 3]{.meta}

Given `n` nodes and a list of undirected edges with no edge repeated, decide whether the graph contains a cycle. The graph may be disconnected. With 6 nodes and edges `0-1, 2-3, 3-4, 4-5, 5-2` the answer is `true`: nodes 2, 3, 4 and 5 form a square, even though the component `0-1` is a plain tree.

A DFS marks each node the moment it discovers it and remembers the node it came from, its parent. The discovery edges form a spanning tree of each component, and a tree has no cycle, so a cycle must use some edge outside that tree. Such an edge joins two nodes that the tree already connects, and together with the tree path between them it closes a loop. So while a node scans its neighbors, there are three cases. An unmarked neighbor is discovered through a new tree edge. The parent is reached through the tree edge the search walked in on, seen again from the other end, because an undirected edge sits in both endpoints' lists. Any other neighbor that is already marked is an extra edge, and that is a cycle.

Picture unrolling a thread through the graph. Each edge out of the current node leads either to fresh ground, where the thread goes next, or to a node the thread already reaches. The edge you arrived on always leads back, so it proves nothing; any other edge to a marked node means the graph loops back on itself. An outer loop starts a fresh search from every unmarked node, because the cycle can sit in any component.

```text
  0 ─ 1          2 ─ 3
                 │   │
                 5 ─ 4

start   pop (node, parent)   neighbors   action
  0         (0, -1)          1           discover 1
            (1, 0)           0           0 is the parent: skip
  1     already visited
  2         (2, -1)          3, 5        discover 3, discover 5
            (5, 2)           4, 2        discover 4; 2 is the parent: skip
            (4, 5)           3, 5        3 is marked and is not the parent:
                                         edge 4-3 closes the square → true
```

```pseudo
FUNCTION HasCycle(n, edges)
    graph ← array of n empty lists
    FOR EACH [u, v] IN edges
        graph[u].append(v)
        graph[v].append(u)                    // undirected: both directions
    visited ← array of n copies of false
    FOR start FROM 0 TO n - 1                 // a cycle can be in any component
        IF visited[start]
            CONTINUE
        visited[start] ← true
        stack ← empty stack
        stack.push((start, -1))               // (node, the node we came from)
        WHILE stack is not empty
            (node, parent) ← stack.pop()
            FOR EACH neighbor IN graph[node]
                IF NOT visited[neighbor]
                    visited[neighbor] ← true  // mark when discovered
                    stack.push((neighbor, node))
                ELSE IF neighbor ≠ parent
                    RETURN true               // reached again, not via parent
    RETURN false
```

Each node is pushed once and each edge is scanned twice, once from each end, so the check runs in `O(V + E)` time and `O(V + E)` space for the lists. The explicit stack replaces recursion, whose depth reaches `n` on a long path and overflows Python's default limit; the recursive DFS makes exactly the same test. Union-find (#32) answers the question edge by edge instead: an edge whose two ends already share a root closes a cycle, and that edge is the answer to Redundant Connection. A graph is a valid tree exactly when it has `n - 1` edges and no cycle, or equivalently `n - 1` edges and a single component. In a directed graph a marked neighbor does not prove a cycle, which is why #60 needs three colors. The classic mistake is forgetting to skip the parent, which reports a cycle on the first tree edge seen from its child; the other is searching only from node 0 and missing a cycle in another component.

*Practice:* LC 261 Graph Valid Tree · LC 684 Redundant Connection · LC 1559 Detect Cycles in 2D Grid

```{=latex}
\clearpage
```

## 82. Bellman-Ford {#a82}

```{=latex}
\markright{82. Bellman-Ford}
```

[Relax Every Edge n - 1 Times · Shortest Path · Tier 3]{.meta}

Given `n` nodes, directed edges with weights that may be negative, and a source, return the shortest distance from the source to every node, `∞` for nodes it cannot reach, or report that a negative cycle is reachable, since circling it forever makes "shortest" meaningless. With edges `2→3 (1)`, `1→2 (-3)`, `0→1 (4)`, `0→2 (2)` and source 0 the answer is `[0, 4, 1, 2]`: the cheapest way to 2 detours through 1 and the negative edge.

Dijkstra (#33) settles nodes greedily, nearest first, which is only safe when no edge is negative, since a negative edge found later can undercut a node already settled. Bellman-Ford gives up on order and relies on counting instead. Relaxing an edge `u → v` asks whether going through `u` beats the best known way into `v`, and takes it if so. One round relaxes every edge once, in any order. After round `k`, every node whose shortest path has at most `k` edges holds its final distance, because each round relaxes the next edge of that path at the latest. Without a negative cycle, a shortest path never needs to repeat a node, so it has at most `n - 1` edges, and `n - 1` rounds settle everything.

Picture correct distances spreading out from the source like a wave, at least one edge further every round, whatever order the edges are scanned in. A round that changes nothing means the wave has stopped, so the loop ends early. If an extra round after `n - 1` still lowers a distance, some path keeps getting cheaper as it grows longer, and only a negative cycle can do that.

```text
scan order:  2→3 (1)   1→2 (-3)   0→1 (4)   0→2 (2)           source 0

          dist:  0    1    2    3     relaxed in this round
start            0    ∞    ∞    ∞
round 1          0    4    2    ∞     0→1 to 4, 0→2 to 2
round 2          0    4    1    3     2→3 to 2 + 1 = 3, then 1→2 to 4 - 3 = 1
round 3          0    4    1    2     2→3 to 1 + 1 = 2
check            no edge still improves: no negative cycle → [0, 4, 1, 2]
```

```pseudo
FUNCTION BellmanFord(n, edges, source)
    dist ← array of n copies of ∞
    dist[source] ← 0
    FOR round FROM 1 TO n - 1             // a shortest path has ≤ n - 1 edges
        changed ← false
        FOR EACH [u, v, w] IN edges
            IF dist[u] + w < dist[v]      // ∞ + w stays ∞: no false relax
                dist[v] ← dist[u] + w     // a cheaper way into v, through u
                changed ← true
        IF NOT changed
            BREAK                         // quiet round: all distances final
    FOR EACH [u, v, w] IN edges
        IF dist[u] + w < dist[v]          // still improving after n - 1 rounds
            RETURN null                   // a negative cycle is reachable
    RETURN dist
```

The work is at most `n - 1` rounds over all `E` edges, `O(V · E)` time and `O(V)` space: slower than Dijkstra, but indifferent to negative weights. Reach for it when weights can be negative, when the question is whether a negative cycle exists (an arbitrage loop in exchange rates), or when a path may use only a limited number of edges. That last case is the flights-within-`k`-stops problem: run exactly `k + 1` rounds, one per flight, and relax each round from a copy of the previous round's distances, so that a round extends paths by at most one edge. Relaxing in place there lets one round chain several edges and break the stop limit; in plain Bellman-Ford the same chaining is harmless and only speeds things up. The classic mistake in plain Bellman-Ford is an integer such as `10^9` standing in for `∞`: then `10^9 - 3 < 10^9`, so unreachable nodes relax their neighbors and a negative cycle the source cannot reach gets reported. Use a true infinity, or skip edges whose start is still unreached.

*Practice:* LC 787 Cheapest Flights Within K Stops · LC 743 Network Delay Time · LC 1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance

```{=latex}
\clearpage
```

## 83. Kruskal's Minimum Spanning Tree {#a83}

```{=latex}
\markright{83. Kruskal's Minimum Spanning Tree}
```

[Sort Edges, Let Union-Find Reject Cycles · MST · Tier 3]{.meta}

Given `n` nodes and weighted undirected edges, choose `n - 1` edges that connect every node with the smallest possible total weight: a minimum spanning tree. Return its weight and its edges, or nothing if the graph is disconnected. With edges `0-1 (4)`, `0-2 (1)`, `1-2 (2)`, `1-3 (5)`, `2-3 (8)`, `3-4 (3)` the tree is `0-2, 1-2, 3-4, 1-3` with weight `11`.

The cut property makes greed safe. Split the nodes into any two groups: the cheapest edge crossing between them belongs to some minimum spanning tree. If a tree left it out, adding it would close a cycle, that cycle would cross the split a second time through another edge that is no cheaper, and swapping the two gives a tree that is no heavier. Kruskal applies this one edge at a time. Sort the edges by weight and scan them cheapest first. An edge whose ends already lie in the same component would close a cycle, so it is rejected. An edge that joins two different components is the cheapest edge leaving either of them, because every cheaper edge has already been scanned and either merged its ends or found them together; by the cut property it is safe, so take it.

Picture the nodes as islands and the sorted edges as bridges offered cheapest first. Union-find (#32) remembers which islands are already linked, so each offer costs two near-constant finds: the same root means reject, different roots means build the bridge and merge. Once `n - 1` bridges stand, every island is linked and the scan stops; if the offers run out first, the graph is disconnected.

```text
sorted   edge   w   components before       action                 total
  1      0-2    1   {0} {1} {2} {3} {4}     take                     1
  2      1-2    2   {0,2} {1} {3} {4}       take                     3
  3      3-4    3   {0,1,2} {3} {4}         take                     6
  4      0-1    4   {0,1,2} {3,4}           skip: same component     6
  5      1-3    5   {0,1,2} {3,4}           take                    11
  6      2-3    8   never examined: n - 1 = 4 edges already taken

tree    0 ─(1)─ 2 ─(2)─ 1 ─(5)─ 3 ─(3)─ 4          total 11
```

```pseudo
FUNCTION Find(parent, x)
    IF parent[x] ≠ x
        parent[x] ← Find(parent, parent[x])   // path compression
    RETURN parent[x]

FUNCTION Union(parent, size, a, b)
    root_a ← Find(parent, a)
    root_b ← Find(parent, b)
    IF root_a = root_b
        RETURN false                          // already one component
    IF size[root_a] < size[root_b]
        swap(root_a, root_b)                  // hang the smaller tree below
    parent[root_b] ← root_a
    size[root_a] ← size[root_a] + size[root_b]
    RETURN true

FUNCTION Kruskal(n, edges)
    order ← empty list
    FOR EACH [u, v, w] IN edges
        order.append((w, u, v))               // weight first: sort by weight
    order.sort()                              // cheapest edge first
    parent ← [0, 1, …, n - 1]                 // every node is its own root
    size ← array of n copies of 1
    total ← 0
    tree ← empty list
    FOR EACH (w, u, v) IN order
        IF Union(parent, size, u, v)          // two components: edge is safe
            total ← total + w
            tree.append([u, v, w])
            IF len(tree) = n - 1
                BREAK                         // n - 1 edges span all n nodes
    IF len(tree) < n - 1
        RETURN null                           // the graph is disconnected
    RETURN (total, tree)
```

Sorting dominates: `O(E log E)` time, the same as `O(E log V)`, plus near-constant union-find work per edge and `O(V)` space beyond the edges. Reach for Kruskal when the graph arrives as an edge list, when the question is the cheapest way to connect everything (cities, points, network links), or when single edges must be forced in or kept out: finding the critical edges of a minimum spanning tree means rerunning Kruskal with one edge banned or taken first. On a dense graph given as points, the array version of Prim (#84) avoids building and sorting all `O(n²)` edges. The classic mistakes are sorting `[u, v, w]` triples as they come, which orders them by `u` instead of by weight, and returning the weight of a forest without checking that `n - 1` edges were taken.

*Practice:* LC 1584 Min Cost to Connect All Points · LC 1135 Connecting Cities With Minimum Cost · LC 1489 Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree

```{=latex}
\clearpage
```

## 84. Prim's Minimum Spanning Tree {#a84}

```{=latex}
\markright{84. Prim's Minimum Spanning Tree}
```

[Grow One Tree with a Min-Heap · MST · Tier 3]{.meta}

Given `n` nodes and weighted undirected edges, return the total weight of a minimum spanning tree, the cheapest set of edges that connects every node, or nothing if the graph is disconnected. For the edges `0-1 (4)`, `0-2 (1)`, `1-2 (2)`, `1-3 (5)`, `2-3 (8)`, `3-4 (3)` the answer is `11`.

Kruskal (#83) grows a forest whose pieces slowly merge; Prim grows a single tree from node 0 and never lets go of it. At every moment the tree and the rest of the graph form a cut, and by the cut property the cheapest edge crossing it is safe to add. So the whole algorithm is one repeated question: what is the cheapest edge from the tree to a node outside it? A min-heap answers it. Whenever a node joins the tree, push each of its edges to an outside node as `(weight, neighbor)`. Pop the smallest entry. If its node is already in the tree, the entry is stale, left over from before a cheaper edge pulled that node in, so skip it; otherwise the node joins the tree at that cost.

Picture an ink blot spreading over the graph, always seeping along the cheapest edge on its rim. The heap is the rim: every edge that leaves the blot, plus a few old ones that now point back inside, which the in-tree check throws away as they surface. This lazy deletion spares the heap any removal from its middle. The popped costs are not sorted, either: edge `3-4 (3)` comes after `1-3 (5)`, because it only touches the rim once node 3 is in.

```text
popped    action                     total   heap after the step
(0, 0)    add 0, push (4,1) (1,2)       0    (1,2) (4,1)
(1, 2)    add 2, push (2,1) (8,3)       1    (2,1) (4,1) (8,3)
(2, 1)    add 1, push (5,3)             3    (4,1) (5,3) (8,3)
(4, 1)    skip: 1 is already in         3    (5,3) (8,3)
(5, 3)    add 3, push (3,4)             8    (3,4) (8,3)
(3, 4)    add 4: all 5 nodes in        11    (8,3) is never popped

entries are (weight, node); the heap is listed smallest first
```

```pseudo
FUNCTION Prim(n, edges)
    graph ← array of n empty lists
    FOR EACH [u, v, w] IN edges
        graph[u].append((w, v))
        graph[v].append((w, u))               // undirected: both directions
    in_tree ← array of n copies of false
    heap ← empty min-heap
    heap.push((0, 0))                         // (cost to attach, node)
    total ← 0
    count ← 0
    WHILE heap is not empty AND count < n
        (cost, node) ← heap.pop()
        IF in_tree[node]
            CONTINUE                          // stale: joined by a cheaper edge
        in_tree[node] ← true                  // mark when popped, not pushed
        total ← total + cost
        count ← count + 1
        FOR EACH (weight, neighbor) IN graph[node]
            IF NOT in_tree[neighbor]
                heap.push((weight, neighbor))
    IF count < n
        RETURN null                           // some node was never reached
    RETURN total
```

Each edge enters the heap at most once, from whichever end joins the tree first, and a push or pop costs `O(log E) = O(log V)`, so Prim runs in `O(E log V)` time and `O(V + E)` space. It has the shape of Dijkstra's loop (#33), but the heap key is the weight of the single edge into the node, not a distance summed from the start, so negative weights do no harm. On a dense graph, such as points on a plane where every pair is an edge, drop the heap: keep an array `best[v]` of the cheapest edge from the tree to each outside node, pick the next node by an `O(V)` scan, refresh `best` from it in `O(V)`, and finish in `O(V²)` without ever listing the edges, the standard answer to Min Cost to Connect All Points. The classic mistake is marking a node as in the tree when it is pushed rather than popped, which freezes the first edge found to it instead of the cheapest.

*Practice:* LC 1584 Min Cost to Connect All Points · LC 1135 Connecting Cities With Minimum Cost · LC 1168 Optimize Water Distribution in a Village

```{=latex}
\clearpage
```

## 85. Rabin-Karp {#a85}

```{=latex}
\markright{85. Rabin-Karp}
```

[Rolling Hash Pattern Matching · Strings · Tier 3]{.meta}

Given a text and a pattern, return every index where the pattern starts in the text. In `abracadabra` the pattern `abra` starts at `0` and at `7`, so the answer is `[0, 7]`.

The brute force compares the pattern with every window of `m` characters, `O(n · m)` time in the worst case. Rabin-Karp compares numbers instead. Read a string as a number written in base 256, one digit per character, so `abra` is the four digits `97 98 114 97`; kept modulo a large prime, that number is the string's hash. Equal strings always have equal hashes, so a window whose hash differs from the pattern's is dismissed by one integer comparison. Equal hashes almost always mean equal strings, but not always, so every hash hit is confirmed by comparing the characters.

The trick that makes it fast is the roll. Sliding a window over the decimal digits of `31415926` from `31415` to `14159` means removing the leading 3, worth 30000, shifting left by multiplying by 10, and adding the 9. A window of text slides the same way in base 256: subtract the leading character times `BASE^(m - 1)`, multiply by `BASE`, add the incoming character, all modulo the prime. Each slide costs `O(1)`, however long the pattern is.

```text
"abra" = base-256 digits 97 98 114 97 → pattern_hash 633841754 (MOD 10^9 + 7)

start   window   window_hash   hash hit?   compare characters
  0      abra     633841754      yes        abra = abra ✓   match at 0
  1      brac     651663196      no
  2      raca     918985050      no
  3      acad     633902941      no
  4      cada     667327066      no
  5      adab     633968475      no
  6      dabr     684103787      no
  7      abra     633841754      yes        abra = abra ✓   match at 7

roll 0 → 1:  drop 'a': (633841754 - 97 × 16777216) mod MOD = 6451809
             add 'c':  (6451809 × 256 + 99) mod MOD = 651663196
```

```pseudo
BASE ← 256                    // one digit per character code
MOD ← 1000000007              // a large prime keeps collisions rare

FUNCTION PolyHash(s)
    value ← 0
    FOR EACH ch IN s
        value ← (value * BASE + code(ch)) mod MOD   // shift left, add a digit
    RETURN value

FUNCTION RabinKarp(text, pattern)
    n ← len(text)
    m ← len(pattern)
    IF m = 0 OR m > n
        RETURN empty list
    high ← BASE^(m - 1) mod MOD               // weight of the leading digit
    pattern_hash ← PolyHash(pattern)
    window_hash ← PolyHash(text[0..m - 1])
    matches ← empty list
    FOR start FROM 0 TO n - m
        IF window_hash = pattern_hash AND text[start..start + m - 1] = pattern
            matches.append(start)             // a hash hit, confirmed
        IF start + m < n                      // roll the window one step right
            window_hash ← (window_hash - code(text[start]) * high) mod MOD
            window_hash ← (window_hash * BASE + code(text[start + m])) mod MOD
    RETURN matches
```

Hashing the pattern and the first window costs `O(m)`, each of the `n - m` rolls costs `O(1)`, and each hash hit costs `O(m)` to verify, so the expected time is `O(n + m)` when matches are few; many true matches, or a modulus small enough to collide often, push it toward `O(n · m)`. Collisions are real: with these constants `neonatus` and `plumular` share the hash 7749640, which is why the compare stays. KMP (#64) guarantees `O(n + m)` without luck, so Rabin-Karp earns its place where hashing many substrings is the point. Repeated DNA Sequences hashes every length-10 window into a set. Longest Duplicate Substring binary searches the length (#10), since a repeat of length `L` contains a repeat of length `L - 1`, and tests each length with a set of rolling hashes. The classic mistakes are trusting a hash hit without the compare and, outside Python, letting the subtraction go negative: `%` in Java or C++ keeps the sign, so add `MOD` back before reducing.

*Practice:* LC 28 Find the Index of the First Occurrence in a String · LC 187 Repeated DNA Sequences · LC 1044 Longest Duplicate Substring · LC 1316 Distinct Echo Substrings

```{=latex}
\clearpage
```

## 86. Longest Common Prefix {#a86}

```{=latex}
\markright{86. Longest Common Prefix}
```

[Vertical Scan · Strings · Tier 3]{.meta}

Given a list of strings, return the longest string that is a prefix of every one of them, or the empty string if they share none. For `["flower", "flow", "flight"]` the answer is `"fl"`, and for `["dog", "racecar", "car"]` it is `""`.

Stack the strings on top of each other, left-aligned, and read them as columns. The common prefix is the run of columns, from the left, in which every row shows the same character. The vertical scan walks those columns one at a time, takes the character of the first string in the current column and checks every string against it. It stops at the first column where some string holds a different character or has already ended, and returns the first string cut just before that column; if nothing stops it, the first string is a prefix of all the others and is the answer. Because it stops at the first bad column, the scan never reads past the prefix plus one column. Folding the list pairwise instead (the prefix of the first two, then of that and the third) is linear too, but it can spend its time matching long early strings that a short later one cuts down at once.

Two other views are worth knowing. Sorting puts the lexicographically smallest and largest strings at the two ends, and the common prefix of the whole list equals the common prefix of just those two, because any string that sits between them in sorted order must agree with both on that prefix; `min` and `max` find the two ends in linear time, so the sort itself is unnecessary. A trie (#34) built from all the strings turns the answer into the path from the root that never branches and never passes the end of a word, which pays off when many queries ask about one fixed set of strings.

```text
column →      0   1   2   3   4   5
"flower"      f   l   o   w   e   r
"flow"        f   l   o   w
"flight"      f   l   i   g   h   t
              ✓   ✓   ✗
                      ↑ col 2: ch = 'o' from "flower", but "flight" has 'i'
answer: first[0..1] = "fl"     9 comparisons, columns 3 to 5 never touched
```

```pseudo
FUNCTION LongestCommonPrefix(strs)
    IF len(strs) = 0
        RETURN ""
    first ← strs[0]
    FOR col FROM 0 TO len(first) - 1
        ch ← first[col]
        FOR EACH word IN strs
            IF col = len(word) OR word[col] ≠ ch    // word ended, or mismatch
                RETURN first[0..col - 1]
    RETURN first                              // first is a prefix of all
```

The scan reads at most `n` characters in each of `L + 1` columns, where `L` is the length of the answer, so it costs `O(n × (L + 1))`, at most linear in the size of the input, with `O(1)` extra space besides the answer. The signals are a prefix shared by every string, autocomplete, and grouping strings by how they start; when one fixed set is queried many times, build the trie instead. The classic mistake is reading `word[col]` before checking that `word` is long enough: the end of the shortest string is a stopping condition just like a mismatch, which is why the test `col = len(word)` comes first, and it is also what makes a list containing `""` return `""`.

*Practice:* LC 14 Longest Common Prefix · LC 3043 Find the Length of the Longest Common Prefix · LC 2416 Sum of Prefix Scores of Strings

```{=latex}
\clearpage
```

## 87. Text Justification {#a87}

```{=latex}
\markright{87. Text Justification}
```

[Greedy Line Packing, Then Spread the Spaces · Strings · Tier 3]{.meta}

Given a list of words and a width, lay the words out as lines of exactly `max_width` characters. Each line takes as many words as fit with at least one space between neighbors, and its leftover spaces are spread across the gaps as evenly as possible, the leftmost gaps taking one extra when they do not divide evenly. The last line, and any line that holds a single word, is left-justified instead: single spaces between words, then padding on the right. With width `16`, the words `["This", "is", "an", "example", "of", "text", "justification."]` become `"This    is    an"`, `"example  of text"` and `"justification.  "`.

The problem splits into two independent decisions. Which words go on a line is greedy, and the statement demands it: starting from the first word not yet placed, keep taking the next word while the letters so far, plus one space per gap, plus the new word still fit. The running `width` counts exactly that, so the test is `width + 1 + len(words[j]) ≤ max_width`, where the `1` is the space the new word brings with it. How to spread the spaces is arithmetic, not search. A line with `letters` letters and `gaps` gaps must place `spaces = max_width - letters` blanks, so every gap gets `floor(spaces / gaps)` and the first `spaces mod gaps` gaps get one more. A brute force that adds one space at a time, cycling through the gaps and remeasuring the line, reaches the same layout slowly; one division does it at once.

Picture a ruler of length `max_width`. Lay the words of a line end to end and the rest of the ruler is `spaces`; cut it into `gaps` equal pieces and drop the remainder, one unit each, into the leftmost gaps. The last line and a lonely word skip the cutting: the words sit flush left and the remainder becomes one block of trailing spaces.

```text
max_width = 16                                            (· marks a space)
pack: This is an        width 10; adding example → 18 > 16, the line closes
      letters 8, gaps 2, spaces 8 → each 4, extra 0
      This····is····an
pack: example of text   width 15; adding justification. → 30 > 16, it closes
      letters 13, gaps 2, spaces 3 → each 1, extra 1 to the leftmost gap
      example··of·text
pack: justification.    last line: single spaces, pad 2 on the right
      justification.··
```

```pseudo
FUNCTION FullJustify(words, max_width)
    lines ← empty list
    i ← 0
    WHILE i < len(words)
        j ← i + 1                             // the line is words[i..j-1]
        width ← len(words[i])                 // letters plus one space per gap
        WHILE j < len(words) AND width + 1 + len(words[j]) ≤ max_width
            width ← width + 1 + len(words[j])
            j ← j + 1
        is_last ← (j = len(words))
        lines.append(JustifyLine(words, i, j, max_width, is_last))
        i ← j
    RETURN lines

FUNCTION JustifyLine(words, i, j, max_width, is_last)
    IF is_last OR j - i = 1                   // left-justify, pad on the right
        line ← join(words[i..j-1], " ")
        RETURN line + " " × (max_width - len(line))
    letters ← 0
    FOR k FROM i TO j - 1
        letters ← letters + len(words[k])
    gaps ← j - i - 1
    spaces ← max_width - letters              // blanks to place in the gaps
    each ← floor(spaces / gaps)
    extra ← spaces mod gaps                   // leftmost gaps get one more
    pieces ← [words[i]]
    FOR k FROM i + 1 TO j - 1
        gap ← each
        IF k - i ≤ extra                      // gap number k - i, from 1
            gap ← gap + 1
        pieces.append(" " × gap)
        pieces.append(words[k])
    RETURN join(pieces, "")
```

Packing looks at every word a constant number of times and each line is built in `O(max_width)`, so the time is `O(n + L × max_width)` for `n` words and `L` lines, linear in the size of the output. The signals are fixed-width layout of any kind: wrapping text, padding columns, or dealing a total out as evenly as possible. That last move, `each = floor(total / parts)` with the first `total mod parts` parts taking one more, appears far beyond text. The classic mistakes are forgetting to count the separating space when testing whether the next word fits, dividing by zero gaps on a one-word line instead of treating it like the last line, and fully justifying the last line instead of padding it on the right.

*Practice:* LC 68 Text Justification · LC 1592 Rearrange Spaces Between Words · LC 418 Sentence Screen Fitting

```{=latex}
\clearpage
```

## 88. String Compression {#a88}

```{=latex}
\markright{88. String Compression}
```

[Run-Length Encoding with Read and Write Pointers · Strings · Tier 3]{.meta}

Compress an array of characters in place with run-length encoding: every maximal run of one repeated character becomes the character, followed by the length of the run when that length is more than `1`, written one digit per cell. Return the new length; whatever lies beyond it does not matter. `["a", "a", "b", "b", "c", "c", "c"]` becomes `["a", "2", "b", "2", "c", "3"]` with length `6`, and a run of twelve `b`s becomes `"b", "1", "2"`.

Building the answer in a second list is easy and costs `O(n)` extra space; the in-place version runs two pointers left to right over the same array. The read pointer finds runs: from `read` it walks forward while the character repeats, so the run is `chars[start..read - 1]` and its length is `read - start`. The write pointer lays down the encoding of each finished run, the character and then the digits of the count. Writing over the input is safe because the encoding of a run is never longer than the run itself: one cell for a single character, and `1 + d` cells for a run of length `k ≥ 2` whose count has `d` digits, where `1 + d ≤ k`. So `write` never passes `read`, and every cell it overwrites has already been read.

Picture the read pointer as a scout running ahead to the end of each run and the write pointer as a scribe following behind, compacting the ground the scout has covered. The gap between them grows only when a run of three or more shrinks into fewer cells, and the scribe never steps onto a cell the scout has not yet passed.

```text
slot             0   1   2   3   4   5   6
start            a   a   b   b   c   c   c
run a × 2        a   2   b   b   c   c   c      write → 2, read → 2
run b × 2        a   2   b   2   c   c   c      write → 4, read → 4
run c × 3        a   2   b   2   c   3   c      write → 6, read → 7
                                         ↑ past the new length: ignored
return 6: the compressed text is chars[0..5] = a 2 b 2 c 3
```

```pseudo
FUNCTION Compress(chars)
    write ← 0
    read ← 0
    WHILE read < len(chars)
        ch ← chars[read]
        start ← read
        WHILE read < len(chars) AND chars[read] = ch
            read ← read + 1                   // walk to the end of the run
        chars[write] ← ch
        write ← write + 1
        count ← read - start
        IF count > 1
            FOR EACH digit IN ToString(count)     // 12 is written as "1", "2"
                chars[write] ← digit
                write ← write + 1
    RETURN write
```

Each cell is passed once by the scout and written at most once by the scribe, so the time is `O(n)`, and the only extra memory is the handful of digits of the current count. The signals are runs of equal neighbors, "in place" paired with "return the new length", and any pair of encode and decode formats. Decoding is the mirror image: read a character, read digits while they are digits to rebuild the count (no digits means `1`), and emit the character that many times. That works only when the characters themselves are never digits; text that may contain digits needs an unambiguous frame such as the length prefix of #66. Count and Say (LC 38) applies run-length encoding, with the count first and `1`s written out, to its own output again and again. The classic mistakes are writing the count into one cell (`"12"` instead of `"1"`, `"2"`), writing a `"1"` after single characters, and, in the version that flushes a run only when the character changes, forgetting to flush the final run.

*Practice:* LC 443 String Compression · LC 38 Count and Say · LC 271 Encode and Decode Strings

```{=latex}
\clearpage
```

## 89. Reverse Words in a String {#a89}

```{=latex}
\markright{89. Reverse Words in a String}
```

[Reverse All, Then Reverse Each Word · Strings · Tier 3]{.meta}

Given a string, return its words in reverse order. Words are separated by one or more spaces and the string may start or end with spaces; the result separates the words by single spaces and has none at either end. `"  the sky   is blue "` becomes `"blue is sky the"`.

In Python the library answers in one line, `" ".join(reversed(s.split()))`: `split()` with no argument drops every run of spaces, so trimming and squeezing come for free. That is the answer to give first. The follow-up asks for `O(1)` extra space on a mutable character array (LC 186), and there the trick is two reversals. Reversing the whole array puts the words in the right order but spells each one backwards; reversing each word where it lies then repairs the spelling. Before that, one compaction pass with a read and a write pointer copies the characters forward, keeps only the first space after each word and drops the trailing one, so the words sit at the front separated by single spaces.

Picture the sentence as a strip of tape. Flipping the whole strip end over end carries the last word to the front, but every word now reads mirrored; flipping each word back in place fixes its letters without moving it. The outer flip reverses both the order and the letters, and the inner flips undo the letters alone.

```text
start            "  the sky   is blue "     20 characters
squeeze spaces   "the sky is blue"          length 15
reverse 0..14    "eulb si yks eht"          order flipped, letters backwards
reverse 0..3     "blue si yks eht"
reverse 5..6     "blue is yks eht"
reverse 8..10    "blue is sky eht"
reverse 12..14   "blue is sky the"          every word reads forwards again
```

```pseudo
FUNCTION ReverseWords(s)
    chars ← the characters of s as an array
    length ← SqueezeSpaces(chars)         // the words fill chars[0..length-1]
    Reverse(chars, 0, length - 1)         // order flipped, letters backwards
    start ← 0
    FOR i FROM 0 TO length
        IF i = length OR chars[i] = " "   // a word ends just before i
            Reverse(chars, start, i - 1)  // spell it forwards again
            start ← i + 1
    RETURN chars[0..length - 1] as a string

FUNCTION SqueezeSpaces(chars)
    write ← 0
    FOR read FROM 0 TO len(chars) - 1
        IF chars[read] ≠ " "
            chars[write] ← chars[read]
            write ← write + 1
        ELSE IF write > 0 AND chars[write - 1] ≠ " "
            chars[write] ← " "            // keep one space after a word
            write ← write + 1
    IF write > 0 AND chars[write - 1] = " "
        write ← write - 1                 // drop the trailing space
    RETURN write

FUNCTION Reverse(chars, i, j)
    WHILE i < j
        swap(chars[i], chars[j])
        i ← i + 1
        j ← j - 1
```

Squeezing moves each character once and each of the two reversal passes swaps it at most once, so the time is `O(n)`; on a mutable array the extra space is `O(1)`, while in Python `list(s)` and the final join cost `O(n)` because strings are immutable. The signals are "reverse the order of the words" and in-place rotation: rotating an array right by `k` is the same trick, reversing the whole array and then its first `k` and remaining elements separately. Reversing the letters of each word without moving it (LC 557) is the second pass alone. The classic mistakes are forgetting the last word, which no space follows (the loop runs to `i = length` for exactly that reason), and leaving a trailing space after squeezing, which the full reversal then moves to the front.

*Practice:* LC 151 Reverse Words in a String · LC 186 Reverse Words in a String II · LC 557 Reverse Words in a String III · LC 189 Rotate Array

```{=latex}
\clearpage
```

## 90. Multiply Strings {#a90}

```{=latex}
\markright{90. Multiply Strings}
```

[Grade-School Multiplication into a Digit Array · Strings · Tier 3]{.meta}

Multiply two non-negative integers given as decimal strings with no leading zeros and return the product as a string, without converting the inputs to numbers; they can be far longer than any machine integer. `"123"` times `"456"` is `"56088"`.

The method is the one from school, minus the partial rows written out on paper. Index both strings from the left. Digit `i` of `num1` is worth `10^(m-1-i)` and digit `j` of `num2` is worth `10^(n-1-j)`, so their product is worth `10^(m+n-2-i-j)`. A product of an `m`-digit and an `n`-digit number has at most `m + n` digits, so it fits in an array `digits` of `m + n` slots, where slot `p` is worth `10^(m+n-1-p)`; matching the two powers lands the product of digits `i` and `j` in slot `i + j + 1`. Walk both strings from the right, add each digit product into its slot, keep the ones digit there and push the tens into slot `i + j`, one to the left. The textbook alternative builds one shifted partial product per digit of `num2` and adds them up with the Add Strings loop; it makes the same digit multiplications but also allocates `n` intermediate strings and adds them one by one.

Picture the `m × n` grid of digit pairs. Every cell on one anti-diagonal, where `i + j` is constant, has the same place value, so the whole anti-diagonal pours into the same slot, and carries ripple right to left like the column sums on paper. No final carry pass is needed: every slot except the leftmost is last touched by its own `mod 10`, and the leftmost cannot overflow because the product fits in `m + n` digits.

```text
 i  j   num1[i] * num2[j]   slot i+j+1   total   digits after the step
 2  2     3 * 6 = 18            5          18     [0, 0, 0, 0, 1, 8]
 2  1     3 * 5 = 15            4          16     [0, 0, 0, 1, 6, 8]
 2  0     3 * 4 = 12            3          13     [0, 0, 1, 3, 6, 8]
 1  2     2 * 6 = 12            4          18     [0, 0, 1, 4, 8, 8]
 1  1     2 * 5 = 10            3          14     [0, 0, 2, 4, 8, 8]
 1  0     2 * 4 =  8            2          10     [0, 1, 0, 4, 8, 8]
 0  2     1 * 6 =  6            3          10     [0, 1, 1, 0, 8, 8]
 0  1     1 * 5 =  5            2           6     [0, 1, 6, 0, 8, 8]
 0  0     1 * 4 =  4            1           5     [0, 5, 6, 0, 8, 8]
digits[0] is 0 (the product needs only 5 digits), so the answer is "56088"
```

```pseudo
FUNCTION Multiply(num1, num2)
    IF num1 = "0" OR num2 = "0"
        RETURN "0"
    m ← len(num1)
    n ← len(num2)
    digits ← array of m + n zeros          // the product has at most m + n
    FOR i FROM m - 1 DOWNTO 0
        FOR j FROM n - 1 DOWNTO 0
            product ← ToInt(num1[i]) * ToInt(num2[j])
            total ← digits[i + j + 1] + product
            digits[i + j + 1] ← total mod 10                    // ones digit
            digits[i + j] ← digits[i + j] + floor(total / 10)   // carry left
    start ← 0
    IF digits[0] = 0                       // only m + n - 1 digits needed
        start ← 1
    result ← empty list
    FOR k FROM start TO m + n - 1
        result.append(ToString(digits[k]))
    RETURN join(result, "")
```

The double loop does `m × n` digit multiplications, so the time is `O(m × n)` and the space is the `O(m + n)` digit array. The signals are numbers given as strings or digit arrays, "without converting to integers", or values too big for 64 bits. The same right-to-left carry loop with `total = a + b + carry` is all of Add Strings (LC 415), and Add Binary (LC 67) is that loop in base `2`; Karatsuba multiplies faster, in `O(n^1.585)`, but no interview expects it. The classic mistakes are forgetting the `"0"` case, which otherwise returns a string of zeros or nothing at all, adding the carry into slot `i + j + 1` instead of `i + j`, and keeping the leading zero when the product needs only `m + n - 1` digits.

*Practice:* LC 43 Multiply Strings · LC 415 Add Strings · LC 67 Add Binary

```{=latex}
\clearpage
```

## 91. GCD and LCM {#a91}

```{=latex}
\markright{91. GCD and LCM}
```

[Euclid's Algorithm · Math · Tier 3]{.meta}

The greatest common divisor of two integers is the largest number that divides both, and the least common multiple is the smallest positive number that both divide. For `48` and `18` the gcd is `6` and the lcm is `144`.

The brute force tries every candidate from `min(a, b)` down to `1`, which costs `O(min(a, b))` divisions. Euclid's insight is that the remainder keeps every common divisor. Since `a mod b = a - q · b`, any number that divides `a` and `b` also divides `a mod b`, and any number that divides `b` and `a mod b` divides `a` back. So `gcd(a, b) = gcd(b, a mod b)`: the pair shrinks at every step while its common divisors stay exactly the same, and when the second number reaches `0` the first one is the answer, because `gcd(a, 0) = a`.

Picture an `a × b` rectangle. Taking `a mod b` cuts as many `b × b` squares as fit off its long side and leaves a thinner rectangle, and Euclid repeats the cut on the leftover until the squares tile it exactly. The side of that last square is the gcd: the largest square that tiles the original rectangle with no gap. The lcm then follows from `gcd · lcm = a · b`. Dividing before multiplying, `a / gcd · b`, keeps every intermediate value no larger than the answer, which matters in languages where `a · b` overflows. The gcd of a whole list folds the pair version across it, starting from `0` because `gcd(0, x) = x`, and stops early once it reaches `1`.

```text
  a    b    a = q × b + r      cut q squares of side b off the a × b block
 48   18   48 = 2 × 18 + 12    two 18 × 18, leaving 12 × 18
 18   12   18 = 1 × 12 + 6     one 12 × 12, leaving 12 × 6
 12    6   12 = 2 × 6  + 0     two 6 × 6, nothing left
  6    0   b = 0: gcd = 6      lcm = 48 / 6 × 18 = 144

┌─────────────────┬─────────────────┬───────────┐
│                 │                 │           │
│                 │                 │  12 × 12  │
│     18 × 18     │     18 × 18     │           │
│                 │                 ├─────┬─────┤
│                 │                 │ 6×6 │ 6×6 │
└─────────────────┴─────────────────┴─────┴─────┘
```

```pseudo
FUNCTION Gcd(a, b)
    a ← abs(a)
    b ← abs(b)
    WHILE b ≠ 0
        remainder ← a mod b             // every common divisor survives the mod
        a ← b
        b ← remainder
    RETURN a                            // gcd(a, 0) = a

FUNCTION Lcm(a, b)
    IF a = 0 OR b = 0
        RETURN 0
    RETURN (abs(a) / Gcd(a, b)) * abs(b)  // exact division first

FUNCTION GcdList(nums)
    result ← 0
    FOR EACH x IN nums
        result ← Gcd(result, x)
        IF result = 1
            BREAK                       // it can never go below 1
    RETURN result
```

Every two steps at least halve the larger number: if `b ≤ a / 2` the remainder is below `b`, and otherwise it is `a - b < a / 2`. Within two steps the larger number is at most `min(a, b)`, so Euclid runs in `O(log min(a, b))` steps, and the slowest inputs are consecutive Fibonacci numbers (#67), where almost every step cuts off a single square. Reach for the gcd when a problem asks for a common period or block size, for equal groups that must divide every count, or for a canonical key for a fraction: dividing `(dy, dx)` by their gcd is how Max Points on a Line (#97) compares slopes exactly. Strings follow the same logic: two strings are built from a common repeating block exactly when `s + t = t + s`, and then the longest such block has length `gcd(len(s), len(t))`. The classic mistake is overwriting `a` before taking the remainder, `a ← b` then `b ← a mod b`, which computes `b mod b = 0` and returns `b` after a single step.

*Practice:* LC 1979 Find Greatest Common Divisor of Array · LC 1071 Greatest Common Divisor of Strings · LC 914 X of a Kind in a Deck of Cards · LC 2413 Smallest Even Multiple

```{=latex}
\clearpage
```

## 92. Sieve of Eratosthenes {#a92}

```{=latex}
\markright{92. Sieve of Eratosthenes}
```

[Cross Out Multiples Starting at p squared · Math · Tier 3]{.meta}

List every prime below `n`, and decide whether a single number is prime. For `n = 30` the primes are `2, 3, 5, 7, 11, 13, 17, 19, 23, 29`, and `91` is not prime because `91 = 7 × 13`.

Testing each number on its own with trial division costs `O(√k)` for the number `k`, so `O(n√n)` for the whole range. The sieve turns the question around: instead of every number searching for a divisor, every prime announces its multiples. Lay out the numbers `2` to `n - 1` and walk upward. The first number that is not yet crossed out has no smaller prime factor, so it is prime, and it crosses out its multiples. Whatever survives the walk is prime.

Two bounds make the walk short. A prime `p` starts crossing at `p²`, not at `2p`: every multiple `k · p` with `2 ≤ k < p` has the smaller factor `k`, so a smaller prime has already crossed it out, which is why `5` finds `10`, `15` and `20` gone and starts at `25`. And the outer loop stops once `p² ≥ n`, because a composite below `n` always has a prime factor of at most `√n`; by then every composite is crossed out and the survivors need no more work. Trial division for a single number rests on the same square root: divisors come in pairs `d` and `n / d`, and one of the two is at most `√n`, so testing `d` while `d · d ≤ n` is enough.

```text
n = 30: p runs 2, 3, 4, 5 and the loop stops at p = 6, since 6 × 6 ≥ 30
p = 2  crosses 4 6 8 10 12 14 16 18 20 22 24 26 28
p = 3  crosses 9 (12) 15 (18) 21 (24) 27       (12) = crossed again
p = 4  skipped: already crossed, its multiples are multiples of 2
p = 5  crosses 25                  10, 15, 20 fell to 2 and 3 earlier

       +0  +1  +2  +3  +4  +5  +6  +7  +8  +9     ×p = first crossed by p
   0    ·   ·   2   3  ×2   5  ×2   7  ×2  ×3      · = 0 and 1, never prime
  10   ×2  11  ×2  13  ×2  ×3  ×2  17  ×2  19
  20   ×2  ×3  ×2  23  ×2  ×5  ×2  ×3  ×2  29
survivors: 2 3 5 7 11 13 17 19 23 29, the ten primes below 30
```

```pseudo
FUNCTION Sieve(n)
    crossed ← array of n copies of false  // true once a smaller prime divides i
    p ← 2
    WHILE p * p < n
        IF NOT crossed[p]                 // p is prime: nothing crossed it out
            multiple ← p * p              // below p * p: already crossed
            WHILE multiple < n
                crossed[multiple] ← true
                multiple ← multiple + p
        p ← p + 1
    primes ← empty list
    FOR i FROM 2 TO n - 1
        IF NOT crossed[i]
            primes.append(i)
    RETURN primes

FUNCTION IsPrime(n)
    IF n < 2
        RETURN false
    d ← 2
    WHILE d * d ≤ n                       // d and n / d: one is at most √n
        IF n mod d = 0
            RETURN false
        d ← d + 1
    RETURN true
```

The sieve runs in `O(n log log n)` time, because the prime `p` crosses out at most `n / p` numbers and the sum of `1 / p` over the primes grows only like `log log n`; the array costs `O(n)` space. Trial division is `O(√n)` for one number. Reach for the sieve when a problem asks about many numbers in a range, such as counting the primes below `n` or finding the closest pair of primes in `[left, right]`, and store the smallest prime factor instead of a boolean when every value in an array must be factored. Reach for trial division when the question is about one number. The classic mistake is `d · d < n` in trial division, which declares `49` prime because its only small factor is exactly `√49 = 7`; the sieve's version of the slip is counting up to `n` inclusive when Count Primes asks for the primes strictly below `n`.

*Practice:* LC 204 Count Primes · LC 2523 Closest Prime Numbers in Range · LC 952 Largest Component Size by Common Factor

```{=latex}
\clearpage
```

## 93. Fast Exponentiation {#a93}

```{=latex}
\markright{93. Fast Exponentiation}
```

[Square and Multiply · Math · Tier 3]{.meta}

Compute `x` raised to the power `n`, where `n` may be negative, and compute `x^n mod m` for a huge `n` without ever building the full number. For example `3^13 = 1594323`, `2^-2 = 0.25`, and `3^13 mod 1000 = 323`.

Multiplying `x` into the result `n` times costs `O(n)` multiplications, hopeless when `n` is in the billions. Squaring is the shortcut: `x · x = x^2`, `x^2 · x^2 = x^4`, and `k` squarings climb to `x^(2^k)`. Every exponent is a sum of powers of two, which are its binary digits, so `x^n` is the product of the rungs of that ladder where `n` has a 1 bit: `13 = 8 + 4 + 1` gives `3^13 = 3^8 · 3^4 · 3^1`. The loop reads the bits of `n` from the lowest. While `x` climbs `x, x^2, x^4, x^8, …`, the test `n mod 2 = 1` asks whether the current rung belongs in the product, and halving `n` throws away the bit just read.

A negative exponent flips the base once at the start, since `x^-n = (1 / x)^n`, and from then on the loop sees only a non-negative `n`. The modular version is the same loop with `mod m` after every product. That is legal because remainders multiply like the numbers they came from, `(a · b) mod m = ((a mod m) · (b mod m)) mod m`, and it keeps every intermediate value below `m²`: `3^1000000 mod 1000000007` takes 20 squarings of small numbers instead of building a number with 477,122 digits.

```text
13 = 8 + 4 + 1 = 1101 in binary, so 3^13 = 3^1 · 3^4 · 3^8
  n   n mod 2   result after the step     x after squaring
 13      1      1 · 3 = 3                 3^2  = 9
  6      0      3          (bit 0: skip)  3^4  = 81
  3      1      3 · 81 = 243              3^8  = 6561
  1      1      243 · 6561 = 1594323      3^16 = 43046721
  0             stop: 4 squarings and 3 multiplies instead of 12 multiplies

mod 1000, the same walk on remainders:
  result 3 → 3 → 243 → 243 · 561 mod 1000 = 323     x 9 → 81 → 561 → 721
```

```pseudo
FUNCTION Power(x, n)
    IF n < 0
        x ← 1 / x                       // x^-n = (1 / x)^n
        n ← -n
    result ← 1
    WHILE n > 0
        IF n mod 2 = 1                  // lowest bit is 1: this square counts
            result ← result * x
        x ← x * x                       // x, x^2, x^4, x^8, …
        n ← floor(n / 2)                // drop the lowest bit
    RETURN result

FUNCTION ModPower(x, n, m)
    result ← 1 mod m                    // 0 when m is 1
    x ← x mod m
    WHILE n > 0
        IF n mod 2 = 1
            result ← (result * x) mod m
        x ← (x * x) mod m               // numbers stay below m * m
        n ← floor(n / 2)
    RETURN result
```

The loop runs once per bit of `n`, one squaring each time plus one multiply per 1 bit, so it costs `O(log n)` multiplications and `O(1)` space. Reach for it when an exponent is huge, when an answer is requested modulo `10^9 + 7`, or when independent choices multiply: Count Good Numbers is `5^ceil(n / 2) · 4^floor(n / 2)`, and Super Pow feeds in an exponent given as a digit array through `a^(10k + d) = (a^k)^10 · a^d`. Replacing the product of numbers by a product of matrices gives matrix powers, the source of fast Fibonacci (#67). The classic mistake is negating `n` in a language with 32-bit integers, where `-(-2^31)` overflows back to `-2^31`; widen to 64 bits before negating. Its modular twin is reducing only the result and not the squared base, which lets `x` grow without bound.

*Practice:* LC 50 Pow(x, n) · LC 372 Super Pow · LC 1922 Count Good Numbers

```{=latex}
\clearpage
```

## 94. Reservoir Sampling {#a94}

```{=latex}
\markright{94. Reservoir Sampling}
```

[Keep the i-th Item with Probability k / i · Math · Tier 3]{.meta}

A stream delivers items one at a time, and its length `n` is unknown until it ends. Keep a random sample of `k` items in one pass and `O(k)` memory, so that every item ends up in the sample with the same chance `k / n`. For the stream `10, 20, 30, 40, 50` with `k = 2`, each of the five items must be kept two times in five.

Storing the whole stream and choosing at the end costs `O(n)` memory, which a stream too large to store cannot pay. The reservoir keeps the sample current instead: after `i` items it is a uniform sample of those `i`. The first `k` items fill it. From then on item `i` draws `j` uniformly from `1..i` and enters only if `j ≤ k`, which gives it probability `k / i`, exactly its fair share of the first `i`. The same draw names the slot it overwrites, and that slot is uniform over the `k` slots. A newcomer that loses the draw is simply forgotten.

The proof for `k = 1` is a telescoping product. Item `i` wins its own draw with probability `1 / i`. Each later item `m` takes the single slot with probability `1 / m`, so item `i` survives step `m` with probability `(m - 1) / m`. Its chance of being the final answer is `1/i · i/(i + 1) · (i + 1)/(i + 2) · … · (n - 1)/n`, where every numerator cancels the denominator before it, leaving `1 / n` for every `i`. For a general `k`, the newcomer at step `m` evicts one particular slot with probability `k/m · 1/k = 1/m`, so the same product starts at `k / i`, or at `1` for the first `k` items, and ends at `k / n`.

```text
k = 2, stream 10 20 30 40 50, one run with random.seed(0)
  i   item   chance k/i   j = randint(1, i)   j ≤ k?          reservoir
  1    10        -               -            fill            [10]
  2    20        -               -            fill            [10, 20]
  3    30       2/3              2            ✓ into slot 2   [10, 30]
  4    40       2/4              4            ✗ forgotten     [10, 30]
  5    50       2/5              1            ✓ into slot 1   [50, 30]

item 30 lasts to the end: enters 2/3 · survives 3/4 · survives 4/5 = 2/5
20000 runs with random.seed(1), times each item was kept (expected 8000):
  10 → 8145    20 → 7898    30 → 7904    40 → 7953    50 → 8100
```

```pseudo
FUNCTION ReservoirSample(stream, k)
    reservoir ← empty list
    i ← 0
    FOR EACH item IN stream
        i ← i + 1                       // item is the i-th seen (1-based)
        IF i ≤ k
            reservoir.append(item)      // fill phase
        ELSE
            j ← RandomInt(1, i)         // uniform over 1..i
            IF j ≤ k                    // chance k / i
                reservoir[j - 1] ← item  // evict a uniform slot
    RETURN reservoir
```

Each item costs `O(1)` work, so the pass takes `O(n)` time and `O(k)` memory. Reach for it whenever a uniform choice must come from something walked once or of unknown length: Linked List Random Node is `k = 1` over the nodes, and Random Pick Index is `k = 1` over the positions holding the target, so the `c`-th match replaces the pick with probability `1 / c`. The weighted form, where each rectangle enters with probability equal to its point count over the running total, solves Random Point in Non-overlapping Rectangles in one pass, and the same product telescopes. The classic mistake is an off-by-one in the draw: `randint(1, i - 1)` gives item `i` the chance `k / (i - 1)`, and a 0-based `randint(0, i)` gives `k / (i + 1)`, so late items come out over- or under-represented. The uniformity check in the Python book catches both slips.

*Practice:* LC 382 Linked List Random Node · LC 398 Random Pick Index · LC 497 Random Point in Non-overlapping Rectangles

```{=latex}
\clearpage
```

## 95. Orientation and Segment Intersection {#a95}

```{=latex}
\markright{95. Orientation and Segment Intersection}
```

[The Cross Product Decides Left or Right · Geometry · Tier 3]{.meta}

Given three points, decide whether the path `o → a → b` turns left, turns right or runs straight; given two segments, decide whether they share a point. Coordinates are integers. The path `(0, 0) → (4, 0) → (2, 3)` turns left, the segments `(0, 0)-(4, 4)` and `(0, 4)-(4, 0)` cross at `(2, 2)`, while `(0, 0)-(2, 2)` and `(3, 3)-(5, 5)` lie on one line without touching.

Slopes bring division, a special case for vertical lines and rounding error; the cross product needs none of them. For the vectors `o → a` and `o → b`, `cross(o, a, b) = (a.x - o.x)(b.y - o.y) - (a.y - o.y)(b.x - o.x)` is the signed area of the parallelogram they span. It is positive when `b` lies to the left of the ray from `o` through `a`, a counter-clockwise turn; negative when `b` lies to the right, a clockwise turn; and zero when the three points are collinear. On integers it is exact.

Two segments cross cleanly when each straddles the other's line: `p1` and `p2` lie on opposite sides of the line `q1 q2`, and `q1` and `q2` on opposite sides of the line `p1 p2`. Opposite sides means opposite signs, so the test is `d1 · d2 < 0` and `d3 · d4 < 0`. One straddle is not enough: `(5, -1)-(5, 1)` straddles the line `y = 0` yet misses `(0, 0)-(2, 0)`. The sign test misses the touching cases, where an endpoint sits exactly on the other segment: its cross product is `0`, and it lies on the segment rather than on the line beyond it exactly when it falls inside the box spanned by the segment's ends. One such check per endpoint covers T-junctions, shared endpoints and collinear overlaps.

```text
 y                                p1 = (0,0)   p2 = (4,4)
 4  q1 .  .  .  p2                q1 = (0,4)   q2 = (4,0)
 3  .  \  .  /  .
 2  .  .  X  .  .                 d1 = cross(q1, q2, p1) = -16   right
 1  .  /  .  \  .                 d2 = cross(q1, q2, p2) =  16   left
 0  p1 .  .  .  q2                d3 = cross(p1, p2, q1) =  16   left
    0  1  2  3  4  x              d4 = cross(p1, p2, q2) = -16   right
                                  d1 · d2 < 0 and d3 · d4 < 0 → true

(0,0)-(2,2) and (3,3)-(5,5): d1 = d2 = d3 = d4 = 0, no straddle, and no
endpoint lies inside the other segment's box → false
from o = (0,0) toward a = (4,0): b = (2,3) gives 12 (left turn),
b = (2,-3) gives -12 (right turn), b = (6,0) gives 0 (straight)
```

```pseudo
FUNCTION Cross(o, a, b)                 // > 0 left turn, < 0 right, 0 straight
    RETURN (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

FUNCTION OnSegment(p, q, r)             // r is on the line pq: inside the box?
    inside_x ← min(p.x, q.x) ≤ r.x ≤ max(p.x, q.x)
    inside_y ← min(p.y, q.y) ≤ r.y ≤ max(p.y, q.y)
    RETURN inside_x AND inside_y

FUNCTION SegmentsIntersect(p1, p2, q1, q2)
    d1 ← Cross(q1, q2, p1)              // side of p1 seen from q1 → q2
    d2 ← Cross(q1, q2, p2)
    d3 ← Cross(p1, p2, q1)              // side of q1 seen from p1 → p2
    d4 ← Cross(p1, p2, q2)
    IF d1 * d2 < 0 AND d3 * d4 < 0
        RETURN true                     // both pairs straddle: a clean crossing
    IF d1 = 0 AND OnSegment(q1, q2, p1)
        RETURN true                     // p1 lies on segment q1 q2
    IF d2 = 0 AND OnSegment(q1, q2, p2)
        RETURN true
    IF d3 = 0 AND OnSegment(p1, p2, q1)
        RETURN true
    IF d4 = 0 AND OnSegment(p1, p2, q2)
        RETURN true
    RETURN false
```

Each test is a handful of multiplications, so both questions cost `O(1)`. With coordinates between `-10^9` and `10^9` the cross product can reach `4 · 10^18`, which fits a signed 64-bit integer but overflows 32 bits; the product `d1 · d2` overflows even 64 bits, so outside Python compare the signs instead of multiplying. Reach for the cross product whenever a problem asks about turns, sides, collinearity or convexity: three points are collinear exactly when it is `0`, which decides Check If It Is a Straight Line and Valid Boomerang, and the convex hull (#96) is built by popping every point that does not turn left. The classic mistake is comparing slopes as floating-point numbers, which divides by zero on vertical lines and rounds the distinct slopes `10^9 / (10^9 - 1)` and `(10^9 + 1) / 10^9` to the same double; Minimum Lines to Represent a Line Chart is known for inputs that break exactly that. The second is skipping the touching checks, which calls segments that share only an endpoint disjoint.

*Practice:* LC 1232 Check If It Is a Straight Line · LC 1037 Valid Boomerang · LC 2280 Minimum Lines to Represent a Line Chart · LC 587 Erect the Fence

```{=latex}
\clearpage
```

## 96. Convex Hull {#a96}

```{=latex}
\markright{96. Convex Hull}
```

[Andrew's Monotone Chain · Geometry · Tier 3]{.meta}

Given points in the plane, return the corners of the smallest convex polygon that contains them all, in counter-clockwise order. Picture a rubber band snapped around nails: it bends only at the hull's corners. For the points `(0, 0), (1, 3), (2, 1), (2, 2), (3, 2), (4, 0), (4, 4)` the hull is `(0, 0), (4, 0), (4, 4), (1, 3)`, and the other three lie inside it.

The brute force tests every pair of points as a candidate edge and keeps it when all other points lie on one side, which costs `O(n^3)`. Andrew's monotone chain sorts once and then walks. Sorted by `x`, the points run from the leftmost to the rightmost, and those two extremes split the hull into a lower chain and an upper chain. Walking the lower chain from left to right, a convex boundary turns left at every corner, which is exactly what the cross product of #95 measures. So the chain is a stack: before pushing a new point, pop the top while the two top points and the new point fail to turn left, `cross ≤ 0`. A popped point sits on or above the segment that now skips it, so it cannot be a corner of the lower boundary, and it never comes back.

The upper chain is the same walk from right to left, where a convex top boundary also turns left at every corner, so the same function builds it. The two chains share their endpoints, the leftmost and the rightmost points, so dropping the last point of each before joining them lists every corner exactly once, counter-clockwise from the leftmost point, the lowest one on a tie.

```text
 y                      sorted: (0,0) (1,3) (2,1) (2,2) (3,2) (4,0) (4,4)
 4  .  .  .  .  ●
 3  .  ●  .  .  .       lower   pops (cross ≤ 0)   stack after the push
 2  .  .  ○  ○  .       (0,0)                      (0,0)
 1  .  .  ○  .  .       (1,3)                      (0,0) (1,3)
 0  ●  .  .  .  ●       (2,1)   (1,3)              (0,0) (2,1)
    0  1  2  3  4  x    (2,2)                      (0,0) (2,1) (2,2)
                        (3,2)   (2,2)              (0,0) (2,1) (3,2)
 ● corner of the hull   (4,0)   (3,2) (2,1)        (0,0) (4,0)
 ○ inside the hull      (4,4)                      (0,0) (4,0) (4,4)

upper, right to left: pops (4,0) (3,2) (2,1) (2,2), keeps (4,4) (1,3) (0,0)
hull = lower minus its last + upper minus its last = (0,0) (4,0) (4,4) (1,3)
```

```pseudo
FUNCTION Cross(o, a, b)                 // > 0 when o → a → b turns left
    RETURN (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

FUNCTION HalfHull(pts)
    chain ← empty list                  // used as a stack: chain[-1] is the top
    FOR EACH p IN pts
        WHILE len(chain) ≥ 2 AND Cross(chain[-2], chain[-1], p) ≤ 0
            chain.pop()                 // last turn is not counter-clockwise
        chain.append(p)
    RETURN chain

FUNCTION ConvexHull(points)
    pts ← sorted(set(points))           // by x, then y; duplicates dropped
    IF len(pts) ≤ 2
        RETURN pts
    lower ← HalfHull(pts)
    upper ← HalfHull(reversed(pts))
    RETURN lower[0..len(lower) - 2] + upper[0..len(upper) - 2]
```

Sorting costs `O(n log n)`, and each chain is `O(n)` because every point is pushed once and popped at most once; the stacks take `O(n)` space. Reach for the hull when a problem asks for a fence or an enclosing boundary, for the extreme points of a set, or for the farthest pair, which always sits on the hull. The popping rule decides what happens to collinear points: `cross ≤ 0` drops a point in the middle of an edge, while Erect the Fence wants such points kept, so it pops only when `cross < 0` and then removes duplicates, because when all the points are collinear both chains contain every one of them. The classic mistake is joining the chains without dropping their last points, which lists the leftmost and rightmost corners twice; the second is sorting by `x` alone, which lets points that share an `x` arrive in any order: if the input `(3, 3), (3, 0), (3, 1)` arrives in that order, the chains keep the middle point `(3, 1)` and lose the corner `(3, 0)`.

*Practice:* LC 587 Erect the Fence · LC 1924 Erect the Fence II

```{=latex}
\clearpage
```

## 97. Max Points on a Line {#a97}

```{=latex}
\markright{97. Max Points on a Line}
```

[Slopes as Reduced Fractions · Geometry · Tier 3]{.meta}

Given distinct points with integer coordinates, return the largest number of them that lie on one straight line. For `(1, 1), (3, 2), (5, 3), (4, 1), (2, 3), (1, 4)` the answer is `4`, because `(1, 4), (2, 3), (3, 2), (4, 1)` all lie on the line `x + y = 5`.

The brute force takes every pair of points as a line and counts the points on it with the cross product of #95, which costs `O(n^3)`. The faster view fixes one anchor point at a time. Every line through the anchor is pinned down by its direction alone, so the other points fall into groups by their slope from the anchor, and the biggest group plus the anchor itself is the best line through that anchor. A hash map from slope to count does the grouping in one pass, and the best over all anchors is the answer. Pairing each anchor only with the points after it is enough, because every line is counted in full from its first point.

Everything rests on the slope key being exact. A floating slope `dy / dx` fails twice: vertical lines divide by zero, and distinct slopes can round to the same double, as `94911150 / 94911151` and `94911151 / 94911152` do. A reduced fraction is exact and canonical. Dividing `dy` and `dx` by their gcd (#91) turns `2/4` and `1/2` into the same key `(1, 2)`. Flipping both signs when `dx < 0` makes the two directions along a line agree, so points on either side of the anchor share a key. Every vertical pair gets the single key `(1, 0)`, and horizontal pairs come out as `(0, 1)` with no special case, because `gcd(0, dx) = dx`.

```text
 y                       ● on the line x + y = 5    ○ elsewhere
 4  ●  .  .  .  .
 3  .  ●  .  .  ○
 2  .  .  ●  .  .
 1  ○  .  .  ●  .
    1  2  3  4  5  x

anchor (1,1)  to (3,2)  dy,dx =  1, 2                   key (1, 2)
              to (5,3)  dy,dx =  2, 4   / gcd 2         key (1, 2)
              to (4,1)  dy,dx =  0, 3   / gcd 3         key (0, 1)
              to (2,3)  dy,dx =  2, 1                   key (2, 1)
              to (1,4)  dx = 0, vertical                key (1, 0)
              biggest group: (1, 2) with 2 points → a line of 3
anchor (3,2)  to (5,3)  dy,dx =  1, 2                   key (1, 2)
              to (4,1)  dy,dx = -1, 1                   key (-1, 1)
              to (2,3)  dy,dx =  1,-1   flip            key (-1, 1)
              to (1,4)  dy,dx =  2,-2   flip, / gcd 2   key (-1, 1)
              biggest group: (-1, 1) with 3 points → a line of 4
later anchors find at most a line of 3, so the answer is 4
```

```pseudo
FUNCTION SlopeKey(p, q)
    dx ← q.x - p.x
    dy ← q.y - p.y
    IF dx = 0
        RETURN (1, 0)                   // vertical line
    IF dx < 0
        dx ← -dx                        // p → q and q → p: the same line
        dy ← -dy
    g ← Gcd(dy, dx)                     // Euclid (#91), positive since dx > 0
    RETURN (dy / g, dx / g)             // exact divisions

FUNCTION MaxPoints(points)
    n ← len(points)
    IF n ≤ 2
        RETURN n
    best ← 0
    FOR i FROM 0 TO n - 1
        counts ← empty map              // slope key → points on that line
        FOR j FROM i + 1 TO n - 1
            key ← SlopeKey(points[i], points[j])
            counts[key] ← counts.get(key, 0) + 1
            IF counts[key] + 1 > best
                best ← counts[key] + 1  // + 1 for the anchor itself
    RETURN best
```

The two loops visit `n(n - 1) / 2` pairs, each with a gcd that costs `O(log C)` for coordinates up to `C`, so the time is `O(n^2 log C)`, and one anchor's map holds fewer than `n` keys, so the space is `O(n)`. Reach for slope keys whenever points, segments or vectors must be grouped by direction: deciding whether points are collinear, merging the pieces of a line chart that share a slope, or counting the lines through a point. The classic mistake, besides the floating key, is skipping the sign normalization, which files `(1, -1)` and `(-1, 1)` under different keys although they are the same slope. Max Points on a Line promises distinct points; with duplicates, a copy of the anchor lies on every line through it and needs its own counter, added to the biggest group.

*Practice:* LC 149 Max Points on a Line · LC 1232 Check If It Is a Straight Line · LC 2280 Minimum Lines to Represent a Line Chart

```{=latex}
\clearpage
```

## 98. Count Set Bits {#a98}

```{=latex}
\markright{98. Count Set Bits}
```

[Brian Kernighan's n & (n - 1) · Bit Manipulation · Tier 3]{.meta}

Count the 1 bits in the binary form of a non-negative integer, its popcount or Hamming weight. `44` is `101100` in binary, so the answer is `3`.

The obvious loop tests the last bit with `n & 1` (bitwise AND) and shifts right with `n >> 1`, once per bit position: 32 rounds for a 32-bit number, however few ones it holds. Brian Kernighan's trick loops once per set bit instead. Subtracting 1 from n turns its lowest 1 into 0 and every 0 below it into 1, and leaves the higher bits alone; AND-ing that with n keeps the higher bits and wipes the flipped block. So `n & (n - 1)` is n with its lowest set bit cleared, and the number of times it can be applied before n reaches 0 is the number of ones.

Two more facts fall out of the same picture. A power of two has exactly one set bit, so n is a power of two exactly when `n > 0` and `n & (n - 1) = 0`. And `n & -n` keeps only the lowest set bit, because in two's complement `-n` is `NOT n` plus 1, which matches n at that bit and below it and disagrees with n everywhere above. For the counts of every number from 0 to n (LC 338) a one-line recurrence beats running the loop n times: `i >> 1` is i with its last bit dropped, and its count is already known, so `bits[i] = bits[i >> 1] + (i & 1)`.

```text
     n       n - 1    n & (n - 1)   count
  101100    101011      101000        1      n = 44
  101000    100111      100000        2
  100000    011111      000000        3      n is 0: three set bits
n - 1 flips the lowest 1 and every 0 below it; the AND wipes that block

44 = ...00101100, -44 = ...11010100, 44 & -44 = 00000100 = 4

i               1   2   3   4   5
bits[i >> 1]    0   1   1   1   1
i & 1           1   0   1   0   1
bits[i]         1   1   2   1   2      bits for 0..5: [0, 1, 1, 2, 1, 2]
```

```pseudo
FUNCTION CountSetBits(n)
    count ← 0
    WHILE n > 0
        n ← n & (n - 1)                     // the lowest 1 becomes 0
        count ← count + 1
    RETURN count

FUNCTION IsPowerOfTwo(n)
    RETURN n > 0 AND (n & (n - 1)) = 0      // exactly one set bit

FUNCTION CountBitsUpTo(n)
    bits ← array of n + 1 zeros
    FOR i FROM 1 TO n
        bits[i] ← bits[i >> 1] + (i & 1)    // i >> 1 drops i's last bit
    RETURN bits
```

Kernighan's loop runs once per set bit, `O(k)` for k ones and never more than the number of bits, in `O(1)` space; the table for `0..n` takes `O(n)`, one step per number. Signals: popcount, Hamming weight, Hamming distance (LC 461 is the popcount of `x XOR y`), power-of-two tests, and the bitmask loops of #99. Python integers have no fixed width, so a negative number behaves as if it had infinitely many leading ones; when a problem means the 32-bit pattern of a negative number, mask it with `n & 0xFFFFFFFF` first. The classic mistake is dropping `n > 0` from the power-of-two test: `0 & (0 - 1)` is `0 & -1 = 0`, so the bare test calls 0 a power of two.

*Practice:* LC 191 Number of 1 Bits · LC 231 Power of Two · LC 338 Counting Bits · LC 461 Hamming Distance

```{=latex}
\clearpage
```

## 99. Bitmask Subset Enumeration {#a99}

```{=latex}
\markright{99. Bitmask Subset Enumeration}
```

[Every Integer from 0 to 2\^n - 1 Is a Subset · Bit Manipulation · Tier 3]{.meta}

List every subset of an array of n distinct elements, this time without recursion. For `[1, 2, 3]` the eight subsets come out as `[]`, `[1]`, `[2]`, `[1, 2]`, `[3]`, `[1, 3]`, `[2, 3]` and `[1, 2, 3]`.

A subset is n yes-or-no answers, and n yes-or-no answers are an n-bit number. Let bit j of an integer `mask` say whether `nums[j]` is in. Then the integers from 0 to `2^n - 1`, written `(1 << n) - 1`, are exactly the `2^n` subsets, each once, and counting upward in binary walks the whole power set. Decoding a mask is a loop over j that tests `(mask >> j) & 1`, bit j shifted down to position 0. Compared with the backtracking tree of #22 this is flat: no recursion and no path to restore, just two loops, and each subset is an integer that can index an array or key a map.

The same view gives a second, subtler loop, over the submasks of a mask: every subset of a subset. Start from `sub = mask` and step with `sub = (sub - 1) & mask`. Subtracting 1 clears the lowest set bit of sub and sets every bit below it; the AND then throws away the bits that are not in mask, which leaves exactly the next smaller submask. The walk visits all `2^k` submasks of a mask with k set bits, each once and in decreasing order, and the empty submask, 0, is added after the loop stops.

```text
nums = [1, 2, 3]    bit j of the mask says whether nums[j] is in
mask   bit 2 1 0    subset
  0        0 0 0    []
  1        0 0 1    [1]
  2        0 1 0    [2]
  3        0 1 1    [1, 2]
  4        1 0 0    [3]
  5        1 0 1    [1, 3]
  6        1 1 0    [2, 3]
  7        1 1 1    [1, 2, 3]

submasks of 13 = 1101, each step sub ← (sub - 1) & 1101:
1101 → 1100 → 1001 → 1000 → 0101 → 0100 → 0001 → 0000
e.g. 1100 - 1 = 1011, and & 1101 drops bit 1, which is not in the mask: 1001
```

```pseudo
FUNCTION SubsetsByMask(nums)
    n ← len(nums)
    result ← empty list
    FOR mask FROM 0 TO (1 << n) - 1         // 2^n masks, one per subset
        subset ← empty list
        FOR j FROM 0 TO n - 1
            IF (mask >> j) & 1 = 1          // bit j is set: nums[j] is in
                subset.append(nums[j])
        result.append(subset)
    RETURN result

FUNCTION Submasks(mask)
    result ← empty list
    sub ← mask
    WHILE sub > 0
        result.append(sub)
        sub ← (sub - 1) & mask              // borrow, keep only mask's bits
    result.append(0)                        // the empty submask ends the walk
    RETURN result
```

Listing all subsets costs `O(n · 2^n)`, `2^n` masks with n bit tests each, the same as backtracking. Walking the submasks of one mask costs `O(2^k)`, and walking them for every mask of n bits costs `O(3^n)` in total, because each element is outside the mask, in the mask but not the submask, or in both. Signals: n up to about 20, all subsets, a set used as a key, or states that are sets of chosen items. Count Number of Maximum Bitwise-OR Subsets (LC 2044) runs the plain loop; Number of Valid Words for Each Puzzle (LC 1178) turns every word into a 26-bit letter mask and enumerates the submasks of each puzzle's mask. The classic mistake is testing membership with `mask & j`, which looks at the bits of the number j, instead of `(mask >> j) & 1` or `mask & (1 << j)`: `nums[0]` is then never picked, because `mask & 0` is always 0.

*Practice:* LC 78 Subsets · LC 2044 Count Number of Maximum Bitwise-OR Subsets · LC 1178 Number of Valid Words for Each Puzzle

```{=latex}
\clearpage
```

## 100. Rate Limiter {#a100}

```{=latex}
\markright{100. Rate Limiter}
```

[Token Bucket and Sliding Log · Design · Tier 3]{.meta}

A rate limiter decides, for each request arriving at time `t`, whether to let it through, so that a client cannot exceed an agreed rate; the two classic designs are the token bucket and the sliding log. With a budget of `3` requests per `6` seconds, four requests at time `0` and one at time `6` come out as allowed, allowed, allowed, rejected, allowed.

The token bucket holds up to `capacity` tokens and gains `rate` tokens per second; a request that finds a whole token spends it and passes, and one that does not is rejected. No timer is needed: each call first credits the tokens earned since the previous call, `(t - last) × rate`, caps the total at `capacity`, and only then decides, so the refill is lazy and the state is two numbers. A full bucket lets a burst of `capacity` requests through at once, and after that requests pass at the refill rate.

The sliding log keeps the times of the requests it allowed during the last `window` seconds in a queue, oldest at the front. A new request first drops every front time `≤ t - window`, which has left the window for good, and passes only if fewer than `limit` remain. Times arrive in order, so the expired ones always sit at the front; each is enqueued once and dequeued at most once, which makes the cost `O(1)` amortized. The log never holds more than `limit` times, so a ring buffer of that size (#76) can replace the queue.

Picture the bucket as a tank refilling at a constant trickle and the log as a frame sliding along the time axis. At the same long-run rate of half a request per second, the bucket spreads requests out after its burst, while the log refuses everything until its first three times slide out of the frame, then admits a fresh burst.

```text
          token bucket: capacity 3,        sliding log: limit 3,
          rate 0.5 per second              window 6 seconds
   t      tokens after refill              log after expiry
   0      3     ✓                          []          ✓
   0      2     ✓                          [0]         ✓
   0      1     ✓                          [0, 0]      ✓
   0      0     ✗                          [0, 0, 0]   ✗
   1      0.5   ✗                          [0, 0, 0]   ✗
   2      1     ✓                          [0, 0, 0]   ✗
   4      1     ✓                          [0, 0, 0]   ✗
   6      1     ✓                          []          ✓   0 ≤ 6 - 6: expired
   6      0     ✗                          [6]         ✓
   7      0.5   ✗                          [6, 6]      ✓
allowed   0 0 0 2 4 6                      0 0 0 6 6 7
          a burst, then a steady trickle   a burst, a wall, a new burst
```

```pseudo
CLASS TokenBucket
    FUNCTION Init(capacity, rate)
        self.capacity ← capacity
        self.rate ← rate                      // tokens added per second
        self.tokens ← capacity                // start full: a burst may pass
        self.last ← 0                         // time of the last refill

    FUNCTION Allow(t)
        refill ← (t - self.last) * self.rate  // earned since the last call
        self.tokens ← min(self.capacity, self.tokens + refill)
        self.last ← t
        IF self.tokens ≥ 1
            self.tokens ← self.tokens - 1
            RETURN true
        RETURN false

CLASS SlidingLog
    FUNCTION Init(limit, window)
        self.limit ← limit
        self.window ← window
        self.log ← empty queue                // allowed times, oldest first

    FUNCTION Allow(t)
        WHILE len(self.log) > 0 AND self.log.front() ≤ t - self.window
            self.log.dequeue()                // older than the window: expired
        IF len(self.log) < self.limit
            self.log.enqueue(t)
            RETURN true
        RETURN false
```

Both limiters cost `O(1)` per request, amortized for the log; the bucket stores two numbers per client and the log up to `limit` times. The trade-off is burst against precision. The bucket is cheap and smooth in the long run but admits up to `capacity + rate × T` requests in a span of `T` seconds, so a short span can beat the nominal rate: five requests pass before time `6` above, where the log lets only three through. The log enforces at most `limit` per window exactly and pays with memory that grows with the limit; a fixed-window counter is cheaper still but lets twice the limit through across a window boundary. The signals are "at most k per window", logger and hit-counter designs, and API throttling, where every client key gets a limiter of its own. The classic mistakes are refilling without the cap, so an idle client banks unlimited tokens, and an off-by-one at the window edge: a time `s` has expired exactly when `s ≤ t - window`.

*Practice:* LC 359 Logger Rate Limiter · LC 362 Design Hit Counter · LC 933 Number of Recent Calls · LC 1396 Design Underground System
