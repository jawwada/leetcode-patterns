---
title: "150 Algorithms"
subtitle: "in Python"
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

This book holds the same one hundred and fifty algorithms as *150 Algorithms in Pseudocode*, in the same order, as Python you can run. The order is importance for a coding interview. Tier 1, the first fifty, are the algorithms to know cold; Tier 2, the next fifty, are the ones to know well; Tier 3, the last fifty, are good to know. Inside a tier, related algorithms sit next to each other, and thirty-two of the entries are designs written as small classes.

Each entry states the problem with a tiny example and then shows one complete file. A file has up to three parts: the helpers, when the input is a tree or a linked list; the algorithm, where every function opens with a one-line docstring that gives the idea and its cost; and a try-it section of prints whose expected output follows `# ->` on the same line. Every file runs on its own, for example `python3 algorithm_books/python/001_two_sum.py`, and every printed line was checked against its comment. The variable names match the pseudocode book line for line, so the two books can be read side by side.

The Python is simple on purpose. Loops are written out instead of comprehensions, there are no lambdas or one-line tricks, and names say what they hold. The aim is that you read a function once, close the book and write it again. The toolbox is small.

```python
from collections import deque    # a queue: append() and popleft() are O(1)
import heapq                     # a min-heap on a list: heappush, heappop, heap[0]
import math                      # math.inf, math.sqrt, math.ceil
import random                    # random pivots and sampling
import bisect                    # ready-made binary search (search chapter only)

# sorted(items) returns a new sorted list; items.sort() sorts in place.
# Both are O(n log n) and stable, and tuples sort field by field.
```


## Standard Helpers

Entries whose input is a binary tree or a linked list build it from a plain Python list, so a test reads like the LeetCode example. `build_tree` takes a level-order list with `None` for a missing child, and `tree_to_list` turns a tree back into one; `build_list` and `to_list` do the same for linked lists. Every file carries its own copy so it runs on its own; the book prints them once, here, and each entry names the ones it uses.

```python
from collections import deque      # popleft is O(1)


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build a tree from a level-order list with None for missing children."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    """Level-order list with None for gaps, trailing Nones removed."""
    values = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while values and values[-1] is None:
        values.pop()
    return values


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def build_list(values):
    """Build a linked list from a Python list and return its head."""
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def to_list(head):
    """Read a linked list back into a Python list."""
    values = []
    while head is not None:
        values.append(head.val)
        head = head.next
    return values
```

# Topic Index {#topic-index}

```{=latex}
\markboth{Topic Index}{}
```

The book is ordered by importance. This index groups the same entries by topic; every number is a link.

| Topic | Entries |
|:--------------------|:------------------------------------------------------------------------|
| Arrays & Hashing | #1 Two Sum · #2 Prefix Sum + Hash Map · #3 Product of Array Except Self · #4 Longest Consecutive Sequence · #102 Boyer-Moore Majority Vote · #103 Next Permutation |
| Hash Map Internals | #51 Hash Map with Separate Chaining · #101 Hash Map with Open Addressing |
| Two Pointers | #6 Reverse a Linked List · #7 3Sum · #8 Container With Most Water · #9 Trapping Rain Water · #52 Dutch National Flag · #104 Reorder List |
| Sliding Window | #11 Longest Substring Without Repeating Characters · #12 Find All Anagrams in a String · #13 Minimum Window Substring · #53 Longest Repeating Character Replacement · #54 Minimum Size Subarray Sum |
| Binary Search | #14 Binary Search · #15 Binary Search on the Answer · #16 Search in a Rotated Sorted Array · #55 Median of Two Sorted Arrays · #56 Search a 2D Matrix · #57 Find Peak Element · #58 Longest Increasing Subsequence · #105 Median of K Sorted Arrays · #106 Random Pick with Weight |
| Sorting | #17 Merge Sort · #18 Quick Sort · #61 Bucket Sort · #108 Counting Sort · #109 Heap Sort |
| Heaps | #19 Top-K Elements · #20 Merge K Sorted Arrays · #59 Heapify · #60 Quickselect |
| Stacks | #22 Valid Parentheses · #23 Monotonic Stack · #25 Decode String · #62 Largest Rectangle in Histogram · #63 Basic Calculator |
| Queues | #64 Sliding Window Maximum · #110 Circular Queue |
| Intervals | #26 Merge Intervals · #27 Meeting Rooms II · #65 Insert Interval · #66 Interval List Intersections |
| Greedy | #28 Kadane's Algorithm · #29 Best Time to Buy and Sell Stock · #67 Jump Game · #68 Jump Game II · #69 Gas Station · #70 Interval Scheduling · #71 Task Scheduler · #72 Partition Labels · #111 Candy · #112 Hand of Straights |
| Backtracking | #30 Subsets · #31 Permutations · #73 Combination Sum · #74 Word Search · #113 N-Queens |
| Trees | #75 Construct Binary Tree from Preorder and Inorder |
| DFS | #33 Diameter and Max Path Sum · #34 Lowest Common Ancestor · #36 Serialize and Deserialize a Binary Tree · #37 Depth-First Search on a Graph · #38 Number of Islands |
| BFS | #32 Binary Tree Level-Order Traversal · #39 BFS Shortest Path · #78 Multi-Source BFS · #79 Word Ladder · #114 Bipartite Check |
| Graphs | #80 Clone Graph · #116 Critical Connections |
| Cycle Detection | #10 Floyd's Tortoise and Hare · #81 Cycle Detection in a Directed Graph · #115 Cycle Detection in an Undirected Graph |
| Topological Sort | #40 Kahn's Algorithm · #82 Topological Sort with DFS · #83 Alien Dictionary |
| Connected Components | #41 Union-Find · #84 Connected Components |
| Shortest Path | #42 Dijkstra's Algorithm · #117 Bellman-Ford |
| MST | #118 Kruskal's Minimum Spanning Tree · #119 Prim's Minimum Spanning Tree |
| BST | #35 Validate a Binary Search Tree · #76 BST Search, Insert, Delete · #77 BST Iterator |
| Tries | #43 Trie · #85 Word Search II |
| Range Queries | #107 Segment Tree |
| Strings | #5 Group Anagrams · #86 KMP String Matching · #87 Longest Palindromic Substring · #88 Encode and Decode Strings · #120 Rabin-Karp · #121 Longest Common Prefix · #122 Text Justification · #123 String Compression · #124 Reverse Words in a String · #125 Multiply Strings |
| Matrix | #89 Game of Life · #126 Spiral Matrix · #127 Rotate Image |
| Math | #90 Fibonacci · #128 GCD and LCM · #129 Sieve of Eratosthenes · #130 Fast Exponentiation · #131 Reservoir Sampling |
| Geometry | #132 Orientation and Segment Intersection · #133 Convex Hull · #134 Max Points on a Line |
| Bit Manipulation | #135 Single Number · #136 Count Set Bits · #137 Bitmask Subset Enumeration |
| Design | #21 Find Median from Data Stream · #24 Min Stack · #44 LRU Cache · #45 Design Hit Counter · #46 Design Twitter · #47 Snapshot Array · #48 Design Tic-Tac-Toe · #49 Flatten Nested List Iterator · #50 Key-Value Store with Transactions · #91 Insert Delete GetRandom O(1) · #92 Time-Based Key-Value Store · #93 LFU Cache · #94 Cache with Expiring Keys · #95 Design Browser History · #96 Design Underground System · #97 Design Search Autocomplete System · #98 My Calendar I and II · #99 Design Snake Game · #100 URL Shortener · #138 Rate Limiter · #139 Consistent Hashing · #140 Stock Price Tracker · #141 All O(1) Data Structure · #142 Range Module · #143 In-Memory File System · #144 Design a Text Editor · #145 Unique ID Generator · #146 Bloom Filter · #147 Count-Min Sketch · #148 Quadtree · #149 Job Scheduler · #150 Inverted Index |

# Tier 1 · Must Know Cold {#tier1}

```{=latex}
\markboth{Tier 1 · Must Know Cold}{}
```

These fifty algorithms are the core of the interview. Each one is the standard answer to a whole family of problems: hashing to remember the past, two pointers and sliding windows for sequences, binary search for anything monotone, sorting and heaps for order, stacks for nesting, BFS and DFS for every tree and graph, Kahn's algorithm, union-find and Dijkstra for dependencies, components and distances, the trie for prefixes, and the design classics that open every design-coding round: the LRU cache, the hit counter, the news feed, the snapshot array, the iterator and the transactional key-value store. Learn them until you can write each one from a blank page without hesitation.

```{=latex}
\clearpage
```

## 1. Two Sum {#a1}

```{=latex}
\markright{1. Two Sum}
```

[Hash Map of Complements · Arrays & Hashing · Tier 1 · python/001\_two\_sum.py]{.meta}

Given an array of integers and a target, return the indices of the two numbers that add up to the target (exactly one pair exists): \[2, 7, 11, 15\], target 9 → \[0, 1\].

```python
# --- algorithm ---
def two_sum(nums, target):
    """One pass; look up target - x before storing x. O(n) time and space."""
    seen = {}                       # value -> index
    for i in range(len(nums)):
        need = target - nums[i]
        if need in seen:            # partner appeared earlier
            return [seen[need], i]
        seen[nums[i]] = i           # store only after checking
    return []


# --- try it ---
print(two_sum([2, 7, 11, 15], 9))   # -> [0, 1]
print(two_sum([3, 2, 4], 6))        # -> [1, 2]
print(two_sum([3, 3], 6))           # -> [0, 1]
print(two_sum([1, 2], 7))           # -> []
```

```{=latex}
\clearpage
```

## 2. Prefix Sum + Hash Map {#a2}

```{=latex}
\markright{2. Prefix Sum + Hash Map}
```

[Subarray Sum Equals K · Arrays & Hashing · Tier 1 · python/002\_prefix\_sum\_hash\_map.py]{.meta}

Given an array of integers (negatives allowed) and an integer k, count the contiguous subarrays whose sum is exactly k: \[2, -1, 1, 2\], k 2 → 4.

```python
# --- algorithm ---
def subarray_sum(nums, k):
    """Count earlier prefix sums equal to prefix - k. O(n) time and space."""
    prefix_count = {}               # prefix sum -> how many times seen
    prefix_count[0] = 1             # the empty prefix, before index 0
    prefix = 0
    total = 0
    for x in nums:
        prefix += x                 # sum of nums up to and including x
        # each earlier prefix equal to prefix - k starts one subarray of sum k
        total += prefix_count.get(prefix - k, 0)
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1   # record last
    return total


# --- try it ---
print(subarray_sum([2, -1, 1, 2], 2))   # -> 4
print(subarray_sum([1, 1, 1], 2))       # -> 2
print(subarray_sum([1, 2, 3], 3))       # -> 2
print(subarray_sum([0, 0, 0], 0))       # -> 6
```

```{=latex}
\clearpage
```

## 3. Product of Array Except Self {#a3}

```{=latex}
\markright{3. Product of Array Except Self}
```

[Prefix and Suffix Products · Arrays & Hashing · Tier 1 · python/003\_product\_of\_array\_except\_self.py]{.meta}

Given an integer array, return an array whose entry i is the product of every element except nums\[i\], without using division: \[1, 2, 3, 4\] → \[24, 12, 8, 6\].

```python
# --- algorithm ---
def product_except_self(nums):
    """answer[i] = product left of i times product right of i, one pass each
    way. O(n) time, O(1) extra space besides the output."""
    n = len(nums)
    answer = [1] * n
    prefix = 1                      # product of nums[0..i-1]
    for i in range(n):
        answer[i] = prefix          # everything left of i
        prefix *= nums[i]           # only now let nums[i] in
    suffix = 1                      # product of nums[i+1..n-1]
    for i in range(n - 1, -1, -1):  # right to left
        answer[i] *= suffix         # times everything right of i
        suffix *= nums[i]
    return answer


# --- try it ---
print(product_except_self([1, 2, 3, 4]))        # -> [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))   # -> [0, 0, 9, 0, 0]
print(product_except_self([0, 0, 2]))           # -> [0, 0, 0]
print(product_except_self([2, -3, 4]))          # -> [-12, 8, -6]
```

```{=latex}
\clearpage
```

## 4. Longest Consecutive Sequence {#a4}

```{=latex}
\markright{4. Longest Consecutive Sequence}
```

[Count Only from the Start of a Run · Arrays & Hashing · Tier 1 · python/004\_longest\_consecutive\_sequence.py]{.meta}

Given an unsorted array of integers, return the length of the longest run of consecutive values, wherever they sit in the array: \[100, 4, 200, 1, 3, 2\] → 4 (the run 1, 2, 3, 4).

```python
# --- algorithm ---
def longest_consecutive(nums):
    """Walk up a run only from its start, a value whose num - 1 is missing.
    Each value is touched at most twice. O(n) time and space."""
    values = set(nums)              # O(1) lookups; duplicates collapse
    best = 0
    for num in values:              # the set, so each start walks once
        if num - 1 in values:
            continue                # inside a run: its start counts it
        length = 1
        while num + length in values:
            length += 1             # one more step up the run
        best = max(best, length)
    return best


# --- try it ---
print(longest_consecutive([100, 4, 200, 1, 3, 2]))           # -> 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))   # -> 9
print(longest_consecutive([-1, 5, -3, -2, 5, 0]))            # -> 4
print(longest_consecutive([7, 7, 7]))                        # -> 1
print(longest_consecutive([]))                               # -> 0
```

```{=latex}
\clearpage
```

## 5. Group Anagrams {#a5}

```{=latex}
\markright{5. Group Anagrams}
```

[Canonical-Key Hashing · Strings · Tier 1 · python/005\_group\_anagrams.py]{.meta}

Given a list of lowercase words, group the words that are anagrams of each other (same letters, same counts), groups in first-seen order: \["eat", "tea", "tan", "ate", "nat", "bat"\] → \[\["eat", "tea", "ate"\], \["tan", "nat"\], \["bat"\]\].

```python
# --- algorithm ---
def letter_counts(word):
    """The 26 letter counts of a word, as a tuple: anagrams share it. O(L)."""
    counts = [0] * 26
    for ch in word:
        slot = ord(ch) - ord('a')   # 'a' -> 0, 'b' -> 1, ..., 'z' -> 25
        counts[slot] += 1
    return tuple(counts)            # a tuple can be a dict key; a list cannot


def group_anagrams(words):
    """Bucket every word under its count key. O(n * L) time and space."""
    groups = {}                     # count key -> words with that key
    for word in words:
        key = letter_counts(word)
        if key not in groups:
            groups[key] = []        # first word of a new group
        groups[key].append(word)
    return list(groups.values())    # one list per key, in first-seen order


# --- try it ---
groups = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
print(groups)   # -> [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
print(group_anagrams(["", "b", ""]))    # -> [['', ''], ['b']]
print(group_anagrams(["aab", "abb"]))   # -> [['aab'], ['abb']]
print(group_anagrams(["ad", "bc"]))     # -> [['ad'], ['bc']]
```

```{=latex}
\clearpage
```

## 6. Reverse a Linked List {#a6}

```{=latex}
\markright{6. Reverse a Linked List}
```

[Three Pointers: prev, curr, next · Two Pointers · Tier 1 · python/006\_reverse\_linked\_list.py]{.meta}

Given the head of a singly linked list, reverse the list in place and return the new head. As values: \[1, 2, 3, 4, 5\] → \[5, 4, 3, 2, 1\].

```python
# --- helpers ---
# standard helpers ListNode, build_list, to_list: printed once under Standard Helpers


# --- algorithm ---
def reverse_list(head):
    """Turn every next arrow around in one walk. O(n) time, O(1) space."""
    prev = None                     # head of the reversed part
    curr = head                     # head of the part still to reverse
    while curr is not None:
        next_node = curr.next       # save the rest before the cut
        curr.next = prev            # turn this arrow around
        prev = curr                 # the reversed part gains curr
        curr = next_node            # step into the saved rest
    return prev                     # curr ran off the end: prev is the new head


# --- try it ---
head = build_list([1, 2, 3, 4, 5])
print(to_list(reverse_list(head)))                  # -> [5, 4, 3, 2, 1]
print(to_list(reverse_list(build_list([1, 2]))))    # -> [2, 1]
print(to_list(reverse_list(build_list([7]))))       # -> [7]
print(to_list(reverse_list(None)))                  # -> []
```

```{=latex}
\clearpage
```

## 7. 3Sum {#a7}

```{=latex}
\markright{7. 3Sum}
```

[Sort, Fix One, Converge Two Pointers · Two Pointers · Tier 1 · python/007\_three\_sum.py]{.meta}

Given an array of integers, return every triplet of values that sums to zero, each distinct triplet once: \[-1, 0, 1, 2, -1, -4\] → \[\[-1, -1, 2\], \[-1, 0, 1\]\].

```python
# --- algorithm ---
def three_sum(nums):
    """Sort; fix nums[i], two pointers find pairs summing to -nums[i]. O(n²)."""
    nums = sorted(nums)             # sorted copy: equal values sit together
    triplets = []
    n = len(nums)
    for i in range(n - 2):
        if nums[i] > 0:
            break                   # smallest of the three is positive: done
        if i > 0 and nums[i] == nums[i - 1]:
            continue                # same first value, same triplets
        left = i + 1
        right = n - 1
        while left < right:         # Two Sum II on nums[i+1..n-1]
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1           # too small: a bigger second value
            elif total > 0:
                right -= 1          # too big: a smaller third value
            else:
                triplets.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1       # skip repeats of the second value
    return triplets


# --- try it ---
print(three_sum([-1, 0, 1, 2, -1, -4]))     # -> [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0, 0]))              # -> [[0, 0, 0]]
print(three_sum([0, 1, 1]))                 # -> []
print(three_sum([-2, 0, 0, 2, 2]))          # -> [[-2, 0, 2]]
```

```{=latex}
\clearpage
```

## 8. Container With Most Water {#a8}

```{=latex}
\markright{8. Container With Most Water}
```

[Always Move the Shorter Wall · Two Pointers · Tier 1 · python/008\_container\_with\_most\_water.py]{.meta}

Vertical lines with the given heights stand at x = 0, 1, ..., n - 1. Return the most water two of them can hold together with the x-axis, where lines i and j hold min(height\[i\], height\[j\]) \* (j - i): \[1, 8, 6, 2, 5, 4, 8, 3, 7\] → 49.

```python
# --- algorithm ---
def max_area(height):
    """Start with the widest pair and move the shorter wall inward: it caps
    every narrower pair it belongs to. O(n) time, O(1) space."""
    left = 0
    right = len(height) - 1
    best = 0
    while left < right:
        width = right - left
        area = min(height[left], height[right]) * width
        best = max(best, area)
        if height[left] < height[right]:
            left += 1               # left wall is shorter: retire it
        else:
            right -= 1              # right wall is shorter or tied
    return best


# --- try it ---
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))    # -> 49
print(max_area([1, 1]))                         # -> 1
print(max_area([4, 3, 2, 1, 4]))                # -> 16
print(max_area([1, 2, 4, 3]))                   # -> 4
```

```{=latex}
\clearpage
```

## 9. Trapping Rain Water {#a9}

```{=latex}
\markright{9. Trapping Rain Water}
```

[Two Pointers with Running Walls · Two Pointers · Tier 1 · python/009\_trapping\_rain\_water.py]{.meta}

Given the heights of bars of width 1, return how many units of rain water they trap between them: \[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1\] → 6.

```python
# --- algorithm ---
def trap(height):
    """Water at i is min(tallest left, tallest right) - height[i]; the side
    with the lower running wall is settled, so move it. O(n), O(1) space."""
    left = 0
    right = len(height) - 1
    left_max = 0                    # tallest bar in height[0..left]
    right_max = 0                   # tallest bar in height[right..n-1]
    water = 0
    while left < right:
        left_max = max(left_max, height[left])
        right_max = max(right_max, height[right])
        if left_max < right_max:    # right wall taller: settle left
            water += left_max - height[left]
            left += 1
        else:                       # left wall as tall: settle right
            water += right_max - height[right]
            right -= 1
    return water


# --- try it ---
print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # -> 6
print(trap([4, 2, 0, 3, 2, 5]))                     # -> 9
print(trap([2, 0, 2]))                              # -> 2
print(trap([1, 2, 3]))                              # -> 0
print(trap([]))                                     # -> 0
```

```{=latex}
\clearpage
```

## 10. Floyd's Tortoise and Hare {#a10}

```{=latex}
\markright{10. Floyd's Tortoise and Hare}
```

[Detect a Cycle and Find Its Entry · Cycle Detection · Tier 1 · python/010\_floyd\_cycle\_detection.py]{.meta}

Given the head of a linked list whose tail may link back to an earlier node, return the node where the cycle begins (None if there is no cycle) in O(1) extra space: values 1..7, tail linked to index 2 → the node with value 3.

```python
# --- helpers ---
# standard helpers ListNode: printed once under Standard Helpers


def build_cycle_list(values, pos):
    """Build a list whose tail links back to index pos (-1: no cycle)."""
    if len(values) == 0:
        return None
    nodes = []
    for value in values:
        nodes.append(ListNode(value))
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]     # close the loop
    return nodes[0]


# --- algorithm ---
def meeting_point(head):
    """Slow steps 1, fast steps 2; they meet only inside a cycle. O(n)."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:            # the same node, not just an equal value
            return slow
    return None                     # fast fell off the end: no cycle


def cycle_entry(head):
    """From head and from the meeting point, 1 step each: they meet at the
    entry. O(n) time, O(1) space."""
    meet = meeting_point(head)
    if meet is None:
        return None
    from_head = head
    from_meet = meet
    while from_head is not from_meet:   # both are a steps from the entry
        from_head = from_head.next
        from_meet = from_meet.next
    return from_head


# --- try it ---
head = build_cycle_list([1, 2, 3, 4, 5, 6, 7], 2)
print(meeting_point(head).val)                          # -> 6
print(cycle_entry(head).val)                            # -> 3
print(cycle_entry(build_cycle_list([3, 2, 0, -4], 1)).val)  # -> 2
print(cycle_entry(build_cycle_list([1, 2, 3], -1)))     # -> None
```

```{=latex}
\clearpage
```

## 11. Longest Substring Without Repeating Characters {#a11}

```{=latex}
\markright{11. Longest Substring Without Repeating Characters}
```

[Variable Window with Last-Seen Index · Sliding Window · Tier 1 · python/011\_longest\_substring\_without\_repeating.py]{.meta}

Given a string, return the length of its longest substring in which no character appears twice: "abcbad" → 4 (the window "cbad").

```python
# --- algorithm ---
def length_of_longest_substring(s):
    """Window s[left..right] has no repeats; on a repeat inside it, jump left
    past the earlier copy. O(n) time, O(alphabet) space."""
    last_seen = {}                  # char -> index of its latest occurrence
    left = 0
    best = 0
    for right in range(len(s)):
        ch = s[right]
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1    # jump past the copy in the window
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


# --- try it ---
print(length_of_longest_substring("abcbad"))      # -> 4
print(length_of_longest_substring("abcabcbb"))    # -> 3
print(length_of_longest_substring("abba"))        # -> 2
print(length_of_longest_substring("bbbbb"))       # -> 1
print(length_of_longest_substring(""))            # -> 0
```

```{=latex}
\clearpage
```

## 12. Find All Anagrams in a String {#a12}

```{=latex}
\markright{12. Find All Anagrams in a String}
```

[Fixed-Size Window with Letter Counts · Sliding Window · Tier 1 · python/012\_find\_all\_anagrams.py]{.meta}

Given lowercase strings s and p, return the start index of every substring of s that is an anagram of p (the same letters, the same counts): s "cbaebabacd", p "abc" → \[0, 6\].

```python
# --- algorithm ---
def letter_counts(text):
    """The 26 letter counts of a lowercase string. O(len(text))."""
    counts = [0] * 26
    for ch in text:
        slot = ord(ch) - ord('a')   # 'a' -> 0, 'b' -> 1, ..., 'z' -> 25
        counts[slot] += 1
    return counts


def find_anagrams(s, p):
    """Slide a window of len(p) one letter in, one letter out; record a start
    whenever its 26 letter counts equal p's. O(26 n) time, O(26) space."""
    m = len(p)
    starts = []
    if m > len(s):
        return starts               # no window fits
    need = letter_counts(p)
    window = letter_counts(s[0:m])  # the first window, s[0..m-1]
    if window == need:
        starts.append(0)            # the first window counts too
    for right in range(m, len(s)):
        entering = ord(s[right]) - ord('a')
        leaving = ord(s[right - m]) - ord('a')
        window[entering] += 1       # s[right] slides in
        window[leaving] -= 1        # s[right - m] slides out
        if window == need:          # 26 slot comparisons
            starts.append(right - m + 1)
    return starts


# --- try it ---
print(find_anagrams("cbaebabacd", "abc"))   # -> [0, 6]
print(find_anagrams("abab", "ab"))          # -> [0, 1, 2]
print(find_anagrams("baa", "aa"))           # -> [1]
print(find_anagrams("ab", "abc"))           # -> []
```

```{=latex}
\clearpage
```

## 13. Minimum Window Substring {#a13}

```{=latex}
\markright{13. Minimum Window Substring}
```

[Expand Right, Shrink Left · Sliding Window · Tier 1 · python/013\_minimum\_window\_substring.py]{.meta}

Given strings s and t, return the shortest substring of s that contains every character of t, repeats included ("" if there is none): s "ADOBECODEBANC", t "ABC" → "BANC".

```python
# --- algorithm ---
def char_counts(text):
    """How many copies of each character text holds. O(len(text))."""
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def min_window(s, t):
    """Grow right to cover t, shrink left while covered. O(len(s) + len(t))."""
    if len(t) == 0:
        return ""                   # nothing to cover
    need = char_counts(t)           # char -> copies the window lacks
    missing = len(t)                # chars of t not yet covered, with repeats
    left = 0
    best_start = 0
    best_len = len(s) + 1           # longer than any real window
    for right in range(len(s)):
        ch = s[right]
        if need.get(ch, 0) > 0:
            missing -= 1            # this copy fills a real gap
        need[ch] = need.get(ch, 0) - 1  # below zero: a spare copy
        while missing == 0:         # covers t: record, then shrink
            if right - left + 1 < best_len:
                best_start = left
                best_len = right - left + 1
            drop = s[left]
            need[drop] += 1
            if need[drop] > 0:
                missing += 1        # dropped a copy the window needed
            left += 1
    if best_len > len(s):
        return ""                   # no window ever covered t
    return s[best_start:best_start + best_len]


# --- try it ---
print(min_window("ADOBECODEBANC", "ABC"))       # -> BANC
print(min_window("AAB", "AA"))                  # -> AA
print(min_window("a", "a"))                     # -> a
print(min_window("a", "aa") == "")              # -> True
```

```{=latex}
\clearpage
```

## 14. Binary Search {#a14}

```{=latex}
\markright{14. Binary Search}
```

[The Lower-Bound Template · Binary Search · Tier 1 · python/014\_binary\_search\_lower\_bound.py]{.meta}

Given a sorted array and a target, return the first index whose value is at least the target, or len(nums) if every value is smaller: \[1, 3, 3, 5, 8, 9\], target 3 → 1.

```python
# --- algorithm ---
def lower_bound(nums, target):
    """First index i with nums[i] >= target, len(nums) if none. O(log n)."""
    lo = 0
    hi = len(nums)              # half-open [lo, hi); len(nums) means "none"
    while lo < hi:              # the window still holds an unknown index
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1        # mid and everything left of it are too small
        else:
            hi = mid            # mid qualifies: the answer is mid or left of it
    return lo


def upper_bound(nums, target):
    """First i with nums[i] > target: the same loop, <= for <. O(log n)."""
    lo = 0
    hi = len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:     # equal values count as too small here
            lo = mid + 1
        else:
            hi = mid
    return lo


def search(nums, target):
    """Exact search: a present target sits at its lower bound. O(log n)."""
    i = lower_bound(nums, target)
    if i < len(nums) and nums[i] == target:
        return i
    return -1


def search_range(nums, target):
    """First and last index, [-1, -1] if absent: two searches, O(log n)."""
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    return [first, upper_bound(nums, target) - 1]


# --- try it ---
nums = [1, 3, 3, 5, 8, 9]
print(lower_bound(nums, 3))         # -> 1
print(lower_bound(nums, 4))         # -> 3
print(search(nums, 4))              # -> -1
print(search_range(nums, 3))        # -> [1, 2]
print(lower_bound(nums, 10))        # -> 6
```

```{=latex}
\clearpage
```

## 15. Binary Search on the Answer {#a15}

```{=latex}
\markright{15. Binary Search on the Answer}
```

[Search a Monotone Yes/No Predicate · Binary Search · Tier 1 · python/015\_binary\_search\_on\_answer.py]{.meta}

Koko eats k bananas per hour from a single pile; when fewer than k are left in that pile she still spends the whole hour on it. Return the smallest k that finishes every pile within h hours (h is at least the number of piles): piles \[3, 6, 7, 11\], h 8 → 4.

```python
import math                         # math.ceil rounds a division up


# --- algorithm ---
def can_finish(piles, h, speed):
    """The yes/no check: are all piles eaten within h hours? O(n)."""
    hours = 0
    for pile in piles:
        hours += math.ceil(pile / speed)    # a partial hour costs a full hour
    return hours <= h


def min_eating_speed(piles, h):
    """First speed in [1, max(piles)] where can_finish says yes.
    O(n log m) for m = max(piles)."""
    lo = 1                          # the slowest possible speed
    hi = max(piles)                 # one pile per hour: always fast enough
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(piles, h, mid):
            hi = mid                # mid works; a slower speed might too
        else:
            lo = mid + 1            # mid fails, and so does every speed below
    return lo


# --- try it ---
print(min_eating_speed([3, 6, 7, 11], 8))           # -> 4
print(min_eating_speed([30, 11, 23, 4, 20], 5))     # -> 30
print(min_eating_speed([30, 11, 23, 4, 20], 6))     # -> 23
print(can_finish([3, 6, 7, 11], 8, 3))              # -> False
```

```{=latex}
\clearpage
```

## 16. Search in a Rotated Sorted Array {#a16}

```{=latex}
\markright{16. Search in a Rotated Sorted Array}
```

[One Half Is Always Sorted · Binary Search · Tier 1 · python/016\_search\_rotated\_sorted\_array.py]{.meta}

A sorted array of distinct values was rotated at an unknown pivot. Return the index of the target, or -1 if it is absent, in O(log n) time: \[6, 7, 0, 1, 2, 4, 5\], target 0 → 2.

```python
# --- algorithm ---
def search_rotated(nums, target):
    """Binary search; the sorted half tells which side can hold the target.
    O(log n) time, O(1) space."""
    lo = 0
    hi = len(nums) - 1                          # closed window [lo, hi]
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:               # left half is sorted
            if nums[lo] <= target and target < nums[mid]:
                hi = mid - 1                    # target inside the left half
            else:
                lo = mid + 1                    # so it must be on the right
        else:                                   # right half is sorted
            if nums[mid] < target and target <= nums[hi]:
                lo = mid + 1                    # target inside the right half
            else:
                hi = mid - 1                    # so it must be on the left
    return -1


# --- try it ---
print(search_rotated([6, 7, 0, 1, 2, 4, 5], 0))     # -> 2
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))     # -> 4
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 3))     # -> -1
print(search_rotated([3, 1], 1))                    # -> 1
```

```{=latex}
\clearpage
```

## 17. Merge Sort {#a17}

```{=latex}
\markright{17. Merge Sort}
```

[Divide, Sort Halves, Merge · Sorting · Tier 1 · python/017\_merge\_sort.py]{.meta}

Sort an array of integers in ascending order and return the result as a new list: \[5, 2, 4, 7, 1, 3, 2, 6\] → \[1, 2, 2, 3, 4, 5, 6, 7\].

```python
# --- algorithm ---
def merge(left, right):
    """Two sorted lists into one: keep taking the smaller front. O(n) time."""
    merged = []
    i = 0                               # front of left
    j = 0                               # front of right
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:         # a tie takes the left one: stable
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    while i < len(left):                # one side is used up: copy the rest
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


def merge_sort(nums):
    """Sort each half recursively, then merge. O(n log n) time, O(n) space."""
    if len(nums) <= 1:
        return list(nums)               # 0 or 1 values: sorted already (copy)
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])       # nums[0..mid-1]
    right = merge_sort(nums[mid:])      # nums[mid..n-1]
    return merge(left, right)


# --- try it ---
print(merge_sort([5, 2, 4, 7, 1, 3, 2, 6]))   # -> [1, 2, 2, 3, 4, 5, 6, 7]
print(merge_sort([3, -1, 0, -1]))             # -> [-1, -1, 0, 3]
print(merge([1, 4], [2, 3]))                  # -> [1, 2, 3, 4]
print(merge_sort([]))                         # -> []
```

```{=latex}
\clearpage
```

## 18. Quick Sort {#a18}

```{=latex}
\markright{18. Quick Sort}
```

[Partition Around a Random Pivot · Sorting · Tier 1 · python/018\_quick\_sort.py]{.meta}

Sort an array of integers in place, without a second array: \[6, 3, 7, 4, 1, 5, 2\] → \[1, 2, 3, 4, 5, 6, 7\].

```python
import random   # random.randint(a, b) can return a or b too


# --- algorithm ---
def partition(nums, lo, hi):
    """Lomuto partition of nums[lo..hi] around a random pivot; return the
    pivot's final index. O(hi - lo) time."""
    pick = random.randint(lo, hi)
    nums[pick], nums[hi] = nums[hi], nums[pick]  # park the pivot at the end
    pivot = nums[hi]
    store = lo                        # invariant: nums[lo..store-1] < pivot
    for i in range(lo, hi):
        if nums[i] < pivot:           # a small value joins the left region
            nums[store], nums[i] = nums[i], nums[store]
            store += 1
    nums[store], nums[hi] = nums[hi], nums[store]  # pivot between the regions
    return store


def sort_range(nums, lo, hi):
    """Partition nums[lo..hi], then sort each side. Expected O(n log n) on
    distinct values; many equal values make it O(n^2), n levels deep."""
    if lo >= hi:                      # 0 or 1 values: sorted already
        return
    p = partition(nums, lo, hi)
    sort_range(nums, lo, p - 1)       # the pivot at p is final: skip it
    sort_range(nums, p + 1, hi)


def quick_sort(nums):
    """Sort the whole array in place and return it. Expected O(n log n)."""
    sort_range(nums, 0, len(nums) - 1)
    return nums


# --- try it ---
print(quick_sort([6, 3, 7, 4, 1, 5, 2]))   # -> [1, 2, 3, 4, 5, 6, 7]
print(quick_sort([2, -3, 2, 0, -3, 2]))    # -> [-3, -3, 0, 2, 2, 2]
print(quick_sort([1]))                     # -> [1]
print(quick_sort([]))                      # -> []
```

```{=latex}
\clearpage
```

## 19. Top-K Elements {#a19}

```{=latex}
\markright{19. Top-K Elements}
```

[Keep a Size-K Min-Heap · Heaps · Tier 1 · python/019\_top\_k\_heap.py]{.meta}

Given an unsorted array and k, return the kth largest value (duplicates count); the same heap also holds the k largest values themselves: \[3, 1, 5, 12, 2, 11\], k = 3 → 5 (the three largest are 12, 11 and 5).

```python
import heapq   # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def top_k(nums, k):
    """Min-heap of the k largest values so far. O(n log k) time, O(k) space."""
    heap = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:               # one too many: drop the smallest
            heapq.heappop(heap)
    return heap


def kth_largest(nums, k):
    """The top of the size-k min-heap is the kth largest. O(n log k)."""
    heap = top_k(nums, k)
    return heap[0]                      # the smallest of the k largest


# --- try it ---
print(kth_largest([3, 1, 5, 12, 2, 11], 3))          # -> 5
print(sorted(top_k([3, 1, 5, 12, 2, 11], 3)))        # -> [5, 11, 12]
print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # -> 4
print(kth_largest([-1, -1], 2))                      # -> -1
```

```{=latex}
\clearpage
```

## 20. Merge K Sorted Arrays {#a20}

```{=latex}
\markright{20. Merge K Sorted Arrays}
```

[A Heap of the Front Elements · Heaps · Tier 1 · python/020\_merge\_k\_sorted.py]{.meta}

Merge k sorted arrays of integers into one sorted array: \[\[1, 4, 7\], \[2, 5\], \[0, 3, 6\]\] → \[0, 1, 2, 3, 4, 5, 6, 7\].

```python
import heapq   # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def merge_k_sorted(arrays):
    """Heap of each array's front as (value, row, col); pop the smallest and
    push its successor. O(N log k) time for N values in k arrays."""
    heap = []                                   # of (value, row, col)
    for row in range(len(arrays)):
        if len(arrays[row]) > 0:                # an empty array has no front
            heapq.heappush(heap, (arrays[row][0], row, 0))
    merged = []
    while len(heap) > 0:
        value, row, col = heapq.heappop(heap)   # the smallest front of all
        merged.append(value)
        if col + 1 < len(arrays[row]):          # that row has a next value
            heapq.heappush(heap, (arrays[row][col + 1], row, col + 1))
    return merged


# --- try it ---
arrays = [[1, 4, 7], [2, 5], [0, 3, 6]]
print(merge_k_sorted(arrays))                  # -> [0, 1, 2, 3, 4, 5, 6, 7]
print(merge_k_sorted([[2, 2], [], [-1, 2]]))   # -> [-1, 2, 2, 2]
print(merge_k_sorted([[5]]))                   # -> [5]
print(merge_k_sorted([]))                      # -> []
```

```{=latex}
\clearpage
```

## 21. Find Median from Data Stream {#a21}

```{=latex}
\markright{21. Find Median from Data Stream}
```

[Two Heaps Meet in the Middle · Design · Tier 1 · python/021\_median\_from\_data\_stream.py]{.meta}

Numbers arrive one at a time; after any arrival, report the median of all the numbers so far (the mean of the two middle values when the count is even): add 5, 15, 1, 3 → medians 5, 10.0, 5, 4.0.

```python
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class MedianFinder:
    """Max-heap of the smaller half, min-heap of the larger half."""

    def __init__(self):
        self.low = []           # max-heap of the smaller half, stored negated
        self.high = []          # min-heap of the larger half

    def add_num(self, num):
        """Pass num through low into high, then rebalance. O(log n)."""
        heapq.heappush(self.low, -num)
        top_low = -heapq.heappop(self.low)    # the largest of low and num
        heapq.heappush(self.high, top_low)
        if len(self.high) > len(self.low):    # low may lead by one, not trail
            top_high = heapq.heappop(self.high)
            heapq.heappush(self.low, -top_high)

    def find_median(self):
        """Read the middle from the two tops. O(1)."""
        if len(self.low) > len(self.high):
            return -self.low[0]               # odd count: low holds the middle
        return (-self.low[0] + self.high[0]) / 2


# --- try it ---
finder = MedianFinder()
finder.add_num(5)
print(finder.find_median())     # -> 5
finder.add_num(15)
print(finder.find_median())     # -> 10.0
finder.add_num(1)
print(finder.find_median())     # -> 5
finder.add_num(3)
print(finder.find_median())     # -> 4.0
```

```{=latex}
\clearpage
```

## 22. Valid Parentheses {#a22}

```{=latex}
\markright{22. Valid Parentheses}
```

[The Matching Stack · Stacks · Tier 1 · python/022\_valid\_parentheses.py]{.meta}

Given a string of the brackets ()\[\]\{\}, decide whether every opener is closed by a bracket of the same kind, innermost first: "(\[\]\{\})" → True, "(\[)\]" → False.

```python
# --- algorithm ---
def is_valid(s):
    """Push openers; every closer must match the top. O(n) time and space."""
    partner = {")": "(", "]": "[", "}": "{"}     # closer -> its opener
    stack = []                                   # openers still waiting
    for ch in s:
        if ch in partner:
            if len(stack) == 0 or stack[-1] != partner[ch]:
                return False                     # nothing open, or wrong kind
            stack.pop()                          # the innermost opener closes
        else:
            stack.append(ch)
    return len(stack) == 0                       # leftovers never closed


# --- try it ---
print(is_valid("([]{})"))       # -> True
print(is_valid("([)]"))         # -> False
print(is_valid("(("))           # -> False
print(is_valid(")("))           # -> False
print(is_valid(""))             # -> True
```

```{=latex}
\clearpage
```

## 23. Monotonic Stack {#a23}

```{=latex}
\markright{23. Monotonic Stack}
```

[Next Greater Element · Stacks · Tier 1 · python/023\_monotonic\_stack.py]{.meta}

For each day's temperature, return how many days you must wait for a warmer one, or 0 if no warmer day comes: \[73, 74, 75, 71, 69, 72, 76, 73\] → \[1, 1, 4, 2, 1, 1, 0, 0\].

```python
# --- algorithm ---
def daily_temperatures(temperatures):
    """Stack of days still waiting; a warmer day answers them. O(n) time."""
    n = len(temperatures)
    answer = [0] * n                # 0 stays for days nothing beats
    stack = []                      # waiting indices, temps never rising
    for i in range(n):
        while len(stack) > 0 and temperatures[stack[-1]] < temperatures[i]:
            j = stack.pop()         # day i is the first warmer day after j
            answer[j] = i - j
        stack.append(i)             # day i waits for its own answer
    return answer


# --- try it ---
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
print(daily_temperatures(temperatures))     # -> [1, 1, 4, 2, 1, 1, 0, 0]
print(daily_temperatures([30, 40, 50]))     # -> [1, 1, 0]
print(daily_temperatures([70, 70, 71]))     # -> [2, 1, 0]
print(daily_temperatures([]))               # -> []
```

```{=latex}
\clearpage
```

## 24. Min Stack {#a24}

```{=latex}
\markright{24. Min Stack}
```

[Every Entry Remembers the Minimum Below It · Design · Tier 1 · python/024\_min\_stack.py]{.meta}

Design a stack whose push, pop, top and get\_min (the smallest value stored) all run in O(1); pop, top and get\_min are called only on a non-empty stack. push -2, push 0, push -3, get\_min, pop, top, get\_min → -3, 0, -2.

```python
# --- algorithm ---
class MinStack:
    """A stack of pairs (value, minimum of this entry and every entry below)."""

    def __init__(self):
        self.entries = []               # pairs, bottom to top

    def push(self, val):
        """Store val with the smaller of val and the minimum below it. O(1)."""
        current_min = val
        if len(self.entries) > 0:
            below_min = self.entries[-1][1]     # min of everything below
            current_min = min(val, below_min)
        self.entries.append((val, current_min))

    def pop(self):
        """Drop the top pair; the pair below keeps its own minimum. O(1)."""
        self.entries.pop()

    def top(self):
        """The value of the top pair. O(1)."""
        return self.entries[-1][0]

    def get_min(self):
        """The minimum recorded in the top pair. O(1)."""
        return self.entries[-1][1]


# --- try it ---
stack = MinStack()
stack.push(-2)
stack.push(0)
stack.push(-3)
print(stack.get_min(), stack.entries)   # -> -3 [(-2, -2), (0, -2), (-3, -3)]
stack.pop()                             # -3 leaves, and -2 is the min again
print(stack.top(), stack.get_min())     # -> 0 -2
stack.push(-2)                          # a second copy of the minimum
stack.pop()
print(stack.get_min(), stack.entries)   # -> -2 [(-2, -2), (0, -2)]
```

```{=latex}
\clearpage
```

## 25. Decode String {#a25}

```{=latex}
\markright{25. Decode String}
```

[One Stack Frame per Bracket · Stacks · Tier 1 · python/025\_decode\_string.py]{.meta}

Decode a string in which k\[text\] means text repeated k times; groups may nest, k is a positive integer that may have several digits, and digits appear only as repeat counts: "3\[a2\[c\]\]" → "accaccacc".

```python
# --- algorithm ---
def decode_string(s):
    """On '[' park (text before it, count); on ']' pop and repeat the group.
    One scan; each ']' builds a string no longer than the output."""
    stack = []                  # frames: (text before the '[', its count)
    current = ""                # decoded text of the innermost open level
    count = 0                   # the repeat count being read
    for ch in s:
        if ch.isdigit():
            count = count * 10 + int(ch)        # counts can have several digits
        elif ch == "[":
            stack.append((current, count))      # park the outer level
            current = ""                        # the inner level starts empty
            count = 0
        elif ch == "]":
            before, repeat = stack.pop()
            current = before + current * repeat     # resume the outer level
        else:
            current += ch
    return current


# --- try it ---
print(decode_string("3[a2[c]]"))           # -> accaccacc
print(decode_string("3[a]2[bc]"))          # -> aaabcbc
print(decode_string("2[abc]3[cd]ef"))      # -> abcabccdcdcdef
print(decode_string("12[x]"))              # -> xxxxxxxxxxxx
print(decode_string("leet"))               # -> leet
```

```{=latex}
\clearpage
```

## 26. Merge Intervals {#a26}

```{=latex}
\markright{26. Merge Intervals}
```

[Sort by Start, Sweep and Extend · Intervals · Tier 1 · python/026\_merge\_intervals.py]{.meta}

Given closed intervals \[start, end\] in any order, merge every group that overlaps or touches and return the result sorted by start: \[\[1, 3\], \[8, 12\], \[2, 6\], \[9, 10\], \[12, 14\]\] → \[\[1, 6\], \[8, 14\]\].

```python
# --- algorithm ---
def merge_intervals(intervals):
    """Sort by start; stretch the last merged interval or open a new one.
    O(n log n) time for the sort, O(n) space for the output."""
    merged = []
    for start, end in sorted(intervals):    # pairs sort by start first
        if len(merged) > 0 and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # overlap: stretch it
        else:
            merged.append([start, end])     # a gap: a new interval begins
    return merged


# --- try it ---
intervals = [[1, 3], [8, 12], [2, 6], [9, 10], [12, 14]]
print(merge_intervals(intervals))           # -> [[1, 6], [8, 14]]
print(merge_intervals([[1, 4], [4, 5]]))    # -> [[1, 5]]
print(merge_intervals([[1, 4], [5, 6]]))    # -> [[1, 4], [5, 6]]
print(merge_intervals([]))                  # -> []
```

```{=latex}
\clearpage
```

## 27. Meeting Rooms II {#a27}

```{=latex}
\markright{27. Meeting Rooms II}
```

[Minimum Rooms with a Heap of End Times · Intervals · Tier 1 · python/027\_meeting\_rooms\_ii.py]{.meta}

Given meetings as half-open intervals \[start, end), return the fewest rooms that can host them all; a meeting may start the moment another one ends: \[\[0, 30\], \[5, 10\], \[10, 20\], \[15, 25\]\] → 3.

```python
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def min_meeting_rooms(intervals):
    """Sort by start; a min-heap holds the time each room frees up.
    O(n log n) time, O(n) space."""
    ends = []                               # min-heap: one end time per room
    for start, end in sorted(intervals):    # earliest start first
        if len(ends) > 0 and ends[0] <= start:
            heapq.heappop(ends)             # the room that frees first is free
        heapq.heappush(ends, end)           # this room is busy until end
    return len(ends)


# --- try it ---
meetings = [[0, 30], [5, 10], [10, 20], [15, 25]]
print(min_meeting_rooms(meetings))                      # -> 3
print(min_meeting_rooms([[0, 30], [5, 10], [15, 20]]))  # -> 2
print(min_meeting_rooms([[7, 10], [2, 4]]))             # -> 1
print(min_meeting_rooms([]))                            # -> 0
```

```{=latex}
\clearpage
```

## 28. Kadane's Algorithm {#a28}

```{=latex}
\markright{28. Kadane's Algorithm}
```

[Maximum Subarray: Extend or Restart · Greedy · Tier 1 · python/028\_kadane.py]{.meta}

Given a non-empty array of integers, return the largest sum of a contiguous subarray together with its first and last index: \[-2, 1, -3, 4, -1, 2, 1, -5, 4\] → (6, 3, 6), the subarray \[4, -1, 2, 1\].

```python
# --- algorithm ---
def max_subarray(nums):
    """Extend the run ending here, or restart at x. O(n) time, O(1) space."""
    ending_here = nums[0]           # best sum of a subarray that ends at i
    start = 0                       # where that subarray begins
    best = nums[0]                  # not 0: all may be negative
    best_start = 0
    best_end = 0
    for i in range(1, len(nums)):
        if ending_here < 0:         # a negative run only drags x down: restart
            ending_here = nums[i]
            start = i
        else:
            ending_here = ending_here + nums[i]     # extend the run
        if ending_here > best:      # improved: copy the bounds
            best = ending_here
            best_start = start
            best_end = i
    return best, best_start, best_end


# --- try it ---
print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # -> (6, 3, 6)
print(max_subarray([5, 4, -1, 7, 8]))                  # -> (23, 0, 4)
print(max_subarray([-3, -1, -2]))                      # -> (-1, 1, 1)
print(max_subarray([7]))                               # -> (7, 0, 0)
```

```{=latex}
\clearpage
```

## 29. Best Time to Buy and Sell Stock {#a29}

```{=latex}
\markright{29. Best Time to Buy and Sell Stock}
```

[Track the Running Minimum · Greedy · Tier 1 · python/029\_best\_time\_stock.py]{.meta}

Given a stock's price on each day, buy on one day and sell on a later day to make the largest profit, or return 0 if no trade makes money: \[7, 1, 5, 3, 6, 4\] → 5 (buy at 1, sell at 6).

```python
import math                         # math.inf is higher than any price


# --- algorithm ---
def max_profit(prices):
    """Sell each day against the running minimum. O(n) time, O(1) space."""
    min_price = math.inf            # cheapest price so far
    best = 0                        # no trade at all earns 0
    for price in prices:
        if price < min_price:       # a cheaper day to have bought on
            min_price = price
        profit = price - min_price  # sell today, bought at the running minimum
        if profit > best:
            best = profit
    return best


# --- try it ---
print(max_profit([7, 1, 5, 3, 6, 4]))   # -> 5
print(max_profit([7, 6, 4, 3, 1]))      # -> 0
print(max_profit([2, 4, 1, 7]))         # -> 6
print(max_profit([]))                   # -> 0
```

```{=latex}
\clearpage
```

## 30. Subsets {#a30}

```{=latex}
\markright{30. Subsets}
```

[Choose, Recurse, Un-Choose · Backtracking · Tier 1 · python/030\_subsets.py]{.meta}

Given an array of distinct integers, return every subset (the power set), each exactly once, in any order: \[1, 2, 3\] → \[\[\], \[1\], \[1, 2\], \[1, 2, 3\], \[1, 3\], \[2\], \[2, 3\], \[3\]\].

```python
# --- algorithm ---
def backtrack(nums, start, path, result):
    """Record path, then extend it by each index from start on. 2^n calls."""
    result.append(path.copy())          # every node of the tree is a subset
    for i in range(start, len(nums)):
        path.append(nums[i])            # choose nums[i]
        backtrack(nums, i + 1, path, result)    # only later indices below
        path.pop()                      # un-choose: path is as it was


def subsets(nums):
    """Start-index backtracking, one tree node per subset. O(n * 2^n)."""
    result = []
    backtrack(nums, 0, [], result)
    return result


# --- try it ---
result = subsets([1, 2, 3])
print(result)   # -> [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
print(subsets([7]))                     # -> [[], [7]]
print(subsets([]))                      # -> [[]]
print(len(subsets([1, 2, 3, 4, 5])))    # -> 32
```

```{=latex}
\clearpage
```

## 31. Permutations {#a31}

```{=latex}
\markright{31. Permutations}
```

[Backtracking with a Used Array · Backtracking · Tier 1 · python/031\_permutations.py]{.meta}

Given an array of distinct integers, return all of its orderings, in any order: \[1, 2, 3\] → \[\[1, 2, 3\], \[1, 3, 2\], \[2, 1, 3\], \[2, 3, 1\], \[3, 1, 2\], \[3, 2, 1\]\].

```python
# --- algorithm ---
def backtrack(nums, used, path, result):
    """Fill the next slot with each unused value in turn. n! leaves."""
    if len(path) == len(nums):
        result.append(path.copy())      # every slot filled: one permutation
        return
    for i in range(len(nums)):
        if used[i]:
            continue                    # nums[i] already sits in the path
        used[i] = True                  # choose
        path.append(nums[i])
        backtrack(nums, used, path, result)
        path.pop()                      # un-choose, in reverse order
        used[i] = False


def permutations(nums):
    """Used-array backtracking over n slots. O(n * n!) time."""
    used = [False] * len(nums)
    result = []
    backtrack(nums, used, [], result)
    return result


# --- try it ---
result = permutations([1, 2, 3])
print(result[0:3])                  # -> [[1, 2, 3], [1, 3, 2], [2, 1, 3]]
print(result[3:6])                  # -> [[2, 3, 1], [3, 1, 2], [3, 2, 1]]
print(permutations([0, 1]))         # -> [[0, 1], [1, 0]]
print(permutations([5]))            # -> [[5]]
print(len(permutations([1, 2, 3, 4, 5])))   # -> 120
```

```{=latex}
\clearpage
```

## 32. Binary Tree Level-Order Traversal {#a32}

```{=latex}
\markright{32. Binary Tree Level-Order Traversal}
```

[BFS One Level at a Time · BFS · Tier 1 · python/032\_level\_order\_traversal.py]{.meta}

Given the root of a binary tree, return its values level by level, each level read left to right: the tree \[3, 9, 20, None, None, 15, 7\] → \[\[3\], \[9, 20\], \[15, 7\]\].

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
# standard helpers TreeNode, build_tree: printed once under Standard Helpers


# --- algorithm ---
def level_order(root):
    """BFS; the queue length at the top of each round is one level. O(n)."""
    levels = []
    if root is None:
        return levels
    queue = deque([root])
    while queue:
        size = len(queue)               # snapshot: exactly this level's nodes
        level = []
        for i in range(size):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:   # children join the back of the queue
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        levels.append(level)            # the level is complete
    return levels


# --- try it ---
root = build_tree([3, 9, 20, None, None, 15, 7])
print(level_order(root))                # -> [[3], [9, 20], [15, 7]]
root = build_tree([1, 2, 3, 4, None, None, 5])
print(level_order(root))                # -> [[1], [2, 3], [4, 5]]
print(level_order(build_tree([1])))     # -> [[1]]
print(level_order(build_tree([])))      # -> []
```

```{=latex}
\clearpage
```

## 33. Diameter and Max Path Sum {#a33}

```{=latex}
\markright{33. Diameter and Max Path Sum}
```

[Postorder DFS That Returns a Height · DFS · Tier 1 · python/033\_tree\_diameter\_max\_path\_sum.py]{.meta}

The diameter of a binary tree is the number of edges on its longest path; the max path sum is the largest total of values along any path of at least one node: \[1, 2, 3, 4, 5\] → diameter 3, \[-10, 9, 20, None, None, 15, 7\] → 42.

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
# standard helpers TreeNode, build_tree: printed once under Standard Helpers


# --- algorithm ---
def diameter(root):
    """Longest path in edges: every node offers left + right. O(n)."""
    best = [0]                              # a box every call can update
    height(root, best)
    return best[0]


def height(node, best):
    """Nodes on the longest downward path from node; record the bend here."""
    if node is None:
        return 0
    left = height(node.left, best)
    right = height(node.right, best)
    best[0] = max(best[0], left + right)    # the path that bends at node
    return 1 + max(left, right)             # only one arm continues upward


def max_path_sum(root):
    """Largest path sum in a non-empty tree; negative arms are cut. O(n)."""
    best = [root.val]                       # one node alone is a path
    gain(root, best)
    return best[0]


def gain(node, best):
    """Best sum of a downward path from node; record the bend here."""
    if node is None:
        return 0
    left = max(gain(node.left, best), 0)    # a negative arm is cut off
    right = max(gain(node.right, best), 0)
    best[0] = max(best[0], node.val + left + right)
    return node.val + max(left, right)


# --- try it ---
root = build_tree([1, 2, 3, 4, 5])
print(diameter(root))                       # -> 3
root = build_tree([-10, 9, 20, None, None, 15, 7])
print(max_path_sum(root))                   # -> 42
root = build_tree([1, 2, None, 3, 4, 5, None, None, 6])
print(diameter(root))                       # -> 4
print(max_path_sum(build_tree([-3, -1, -2])))   # -> -1
print(diameter(build_tree([7])))            # -> 0
```

```{=latex}
\clearpage
```

## 34. Lowest Common Ancestor {#a34}

```{=latex}
\markright{34. Lowest Common Ancestor}
```

[Postorder Search in a Binary Tree · DFS · Tier 1 · python/034\_lowest\_common\_ancestor.py]{.meta}

Given a binary tree and two of its nodes p and q, return the deepest node that has both in its subtree (a node counts as its own ancestor): \[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4\], p = 7, q = 8 → 3.

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
# standard helpers TreeNode, build_tree: printed once under Standard Helpers


def find(root, val):
    """Return the node holding val, or None (values are unique)."""
    if root is None or root.val == val:
        return root
    left = find(root.left, val)
    if left is not None:
        return left
    return find(root.right, val)


# --- algorithm ---
def lowest_common_ancestor(root, p, q):
    """Postorder; report p, q or their meeting point upward. O(n) time."""
    if root is None or root is p or root is q:
        return root                     # nothing here, or a target itself
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left is not None and right is not None:
        return root                     # one target on each side: the LCA
    if left is not None:
        return left                     # pass the single report upward
    return right


# --- try it ---
root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
answer = lowest_common_ancestor(root, find(root, 7), find(root, 8))
print(answer.val)                       # -> 3
answer = lowest_common_ancestor(root, find(root, 6), find(root, 4))
print(answer.val)                       # -> 5
answer = lowest_common_ancestor(root, find(root, 5), find(root, 4))
print(answer.val)                       # -> 5
```

```{=latex}
\clearpage
```

## 35. Validate a Binary Search Tree {#a35}

```{=latex}
\markright{35. Validate a Binary Search Tree}
```

[Carry the Allowed Range Down · BST · Tier 1 · python/035\_validate\_bst.py]{.meta}

Given the root of a binary tree, decide whether it is a valid BST: every value in a node's left subtree is strictly smaller, every value in its right subtree strictly larger. \[2, 1, 3\] → True, \[5, 4, 6, None, None, 3, 7\] → False.

```python
from collections import deque      # popleft is O(1)
import math                         # math.inf: no bound at the root


# --- helpers ---
# standard helpers TreeNode, build_tree: printed once under Standard Helpers


# --- algorithm ---
def is_valid_bst(root):
    """Start with no bounds; every node must fit its ancestors' range. O(n)."""
    return fits(root, -math.inf, math.inf)


def fits(node, low, high):
    """True if every value in this subtree is strictly between low and high."""
    if node is None:
        return True
    if node.val <= low or node.val >= high:
        return False                        # breaks a promise made higher up
    if not fits(node.left, low, node.val):  # left side: below node.val
        return False
    return fits(node.right, node.val, high)     # right side: above node.val


# --- try it ---
print(is_valid_bst(build_tree([2, 1, 3])))                      # -> True
print(is_valid_bst(build_tree([5, 4, 6, None, None, 3, 7])))    # -> False
print(is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6])))    # -> False
print(is_valid_bst(build_tree([2, 2, 2])))                      # -> False
print(is_valid_bst(build_tree([])))                             # -> True
```

```{=latex}
\clearpage
```

## 36. Serialize and Deserialize a Binary Tree {#a36}

```{=latex}
\markright{36. Serialize and Deserialize a Binary Tree}
```

[Preorder with Null Markers · DFS · Tier 1 · python/036\_serialize\_binary\_tree.py]{.meta}

Turn a binary tree into a string and the string back into the same tree: write the values in preorder, '\#' for every missing child, separated by commas: \[1, 2, 3, None, None, 4, 5\] → "1,2,\#,\#,3,4,\#,\#,5,\#,\#".

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
# standard helpers TreeNode, build_tree, tree_to_list: printed once under Standard Helpers


# --- algorithm ---
def serialize(root):
    """Preorder with '#' for each missing child, joined by commas. O(n)."""
    tokens = []
    write(root, tokens)
    return ",".join(tokens)


def write(node, tokens):
    """Append the node's value, then its left subtree, then its right."""
    if node is None:
        tokens.append("#")                  # the marker closes a branch
        return
    tokens.append(str(node.val))
    write(node.left, tokens)
    write(node.right, tokens)


def deserialize(data):
    """Read the tokens back in the same preorder with a moving index. O(n)."""
    tokens = data.split(",")
    index = [0]                             # one box all the calls share
    return read(tokens, index)


def read(tokens, index):
    """Build the subtree that starts at tokens[index[0]] and move past it."""
    token = tokens[index[0]]
    index[0] += 1
    if token == "#":
        return None
    node = TreeNode(int(token))
    node.left = read(tokens, index)         # the left subtree eats its tokens
    node.right = read(tokens, index)        # the right one starts after them
    return node


# --- try it ---
data = serialize(build_tree([1, 2, 3, None, None, 4, 5]))
print(data)                                 # -> 1,2,#,#,3,4,#,#,5,#,#
print(tree_to_list(deserialize(data)))      # -> [1, 2, 3, None, None, 4, 5]
print(serialize(build_tree([-7, None, 12])))    # -> -7,#,12,#,#
print(serialize(None))                      # -> #
print(tree_to_list(deserialize("#")))       # -> []
```

```{=latex}
\clearpage
```

## 37. Depth-First Search on a Graph {#a37}

```{=latex}
\markright{37. Depth-First Search on a Graph}
```

[Recursive and Iterative · DFS · Tier 1 · python/037\_graph\_dfs.py]{.meta}

Given an undirected graph with nodes 0..n-1 as an edge list, list the nodes in the order a depth-first search from start first reaches them: n = 5, edges \[\[0, 1\], \[0, 4\], \[0, 2\], \[1, 3\], \[3, 2\]\], start 0 → \[0, 1, 3, 2, 4\].

```python
# --- algorithm ---
def build_graph(n, edges):
    """Adjacency list: graph[u] lists u's neighbors in edge order. O(V + E)."""
    graph = []
    for i in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)                  # undirected: both directions
    return graph


def dfs_recursive(n, edges, start):
    """Visit a node, then dive into each unvisited neighbor. O(V + E)."""
    graph = build_graph(n, edges)
    visited = set()
    order = []
    visit(graph, start, visited, order)
    return order


def visit(graph, node, visited, order):
    """Mark node on entry, record it, recurse into unvisited neighbors."""
    visited.add(node)                       # mark first: cycles cannot re-enter
    order.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            visit(graph, neighbor, visited, order)


def dfs_iterative(n, edges, start):
    """Explicit stack; mark when popped to match the recursion. O(V + E)."""
    graph = build_graph(n, edges)
    visited = set()
    order = []
    stack = []
    stack.append(start)
    while stack:
        node = stack.pop()
        if node in visited:
            continue                        # a stale copy, reached another way
        visited.add(node)                   # mark when popped
        order.append(node)
        for neighbor in reversed(graph[node]):  # first neighbor ends on top
            if neighbor not in visited:
                stack.append(neighbor)
    return order


# --- try it ---
edges = [[0, 1], [0, 4], [0, 2], [1, 3], [3, 2]]
print(dfs_recursive(5, edges, 0))           # -> [0, 1, 3, 2, 4]
print(dfs_iterative(5, edges, 0))           # -> [0, 1, 3, 2, 4]
print(dfs_iterative(4, [[0, 1], [2, 3]], 0))    # -> [0, 1]
print(dfs_recursive(1, [], 0))              # -> [0]
```

```{=latex}
\clearpage
```

## 38. Number of Islands {#a38}

```{=latex}
\markright{38. Number of Islands}
```

[Grid Flood Fill · DFS · Tier 1 · python/038\_number\_of\_islands.py]{.meta}

Given a grid of "1" (land) and "0" (water), count the islands: groups of land cells joined up, down, left or right, never diagonally: \["11000", "11000", "00100", "00011"\] → 3.

```python
# --- helpers ---
def make_grid(rows):
    """Turn a list of strings into a grid of one-character cells."""
    grid = []
    for row in rows:
        grid.append(list(row))
    return grid


# --- algorithm ---
def num_islands(grid):
    """Each '1' the scan meets starts a fill that sinks its island. O(R * C)."""
    count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "1":
                count += 1                  # a new island starts here
                sink(grid, row, col)        # so it is never counted again
    return count


def sink(grid, start_row, start_col):
    """Explicit-stack DFS: turn every land cell of one island into water."""
    stack = []
    stack.append((start_row, start_col))
    while stack:
        row, col = stack.pop()
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            continue                        # stepped off the map
        if grid[row][col] != "1":
            continue                        # water, or land already sunk
        grid[row][col] = "0"                # sinking is the visited mark
        stack.append((row + 1, col))        # down, up, right, left
        stack.append((row - 1, col))
        stack.append((row, col + 1))
        stack.append((row, col - 1))


# --- try it ---
grid = make_grid(["11000", "11000", "00100", "00011"])
print(num_islands(grid))                    # -> 3
grid = make_grid(["11110", "11010", "11000", "00000"])
print(num_islands(grid))                    # -> 1
print(num_islands(make_grid(["101", "010", "101"])))    # -> 5
print(num_islands(make_grid(["0"])))        # -> 0
```

```{=latex}
\clearpage
```

## 39. BFS Shortest Path {#a39}

```{=latex}
\markright{39. BFS Shortest Path}
```

[Unweighted Graphs, Layer by Layer · BFS · Tier 1 · python/039\_bfs\_shortest\_path.py]{.meta}

Given an undirected graph on nodes 0..n-1 as an edge list, return a shortest path from source to target as a list of nodes, or \[\] if there is none: edges 0-1 1-2 2-3 3-4 0-5 5-4, source 0, target 4 → \[0, 5, 4\].

```python
from collections import deque      # popleft is O(1)


# --- algorithm ---
def shortest_path(n, edges, source, target):
    """BFS; the first time a node is reached is by a shortest path. O(V + E)."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)              # undirected: store both directions
        graph[v].append(u)
    dist = [-1] * n                     # -1 means not reached yet
    parent = [-1] * n                   # the node that first reached it
    dist[source] = 0
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if dist[neighbor] == -1:    # first visit is a shortest one
                dist[neighbor] = dist[node] + 1     # mark when enqueued
                parent[neighbor] = node
                queue.append(neighbor)
    if dist[target] == -1:
        return []                       # target is in another component
    return build_path(parent, target)


def build_path(parent, target):
    """Follow parent pointers back to the source, then reverse. O(V)."""
    path = []
    node = target
    while node != -1:                   # only the source has no parent
        path.append(node)
        node = parent[node]
    return path[::-1]


# --- try it ---
edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 4]]
print(shortest_path(6, edges, 0, 4))        # -> [0, 5, 4]
print(shortest_path(6, edges, 0, 3))        # -> [0, 1, 2, 3]
print(shortest_path(3, [[0, 1]], 0, 2))     # -> []
print(shortest_path(1, [], 0, 0))           # -> [0]
```

```{=latex}
\clearpage
```

## 40. Kahn's Algorithm {#a40}

```{=latex}
\markright{40. Kahn's Algorithm}
```

[Topological Sort by Peeling Indegree-Zero Nodes · Topological Sort · Tier 1 · python/040\_kahn\_topological\_sort.py]{.meta}

Courses are 0..n-1, and a pair \[a, b\] means course b must come before course a. Return an order that takes every course, or \[\] if the pairs form a cycle: n = 6, \[\[3, 0\], \[3, 1\], \[4, 3\], \[2, 3\], \[5, 4\], \[5, 2\]\] → \[0, 1, 3, 4, 2, 5\].

```python
from collections import deque      # popleft is O(1)


# --- algorithm ---
def find_order(num_courses, prerequisites):
    """Take courses whose prerequisites are all done; a cycle never frees up.
    O(V + E) time and space."""
    graph = []
    for _ in range(num_courses):
        graph.append([])
    indegree = [0] * num_courses        # prerequisites not yet taken
    for course, before in prerequisites:
        graph[before].append(course)    # [a, b] is the edge b -> a
        indegree[course] += 1
    queue = deque()
    for course in range(num_courses):
        if indegree[course] == 0:       # free to take right away
            queue.append(course)
    order = []
    while queue:
        course = queue.popleft()
        order.append(course)
        for next_course in graph[course]:
            indegree[next_course] -= 1  # one prerequisite of it is done
            if indegree[next_course] == 0:
                queue.append(next_course)
    if len(order) < num_courses:
        return []                       # the rest wait on each other: a cycle
    return order


# --- try it ---
pairs = [[3, 0], [3, 1], [4, 3], [2, 3], [5, 4], [5, 2]]
print(find_order(6, pairs))                             # -> [0, 1, 3, 4, 2, 5]
print(find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))  # -> [0, 1, 2, 3]
print(find_order(3, [[1, 0], [2, 1], [1, 2]]))          # -> []
print(find_order(2, []))                                # -> [0, 1]
```

```{=latex}
\clearpage
```

## 41. Union-Find {#a41}

```{=latex}
\markright{41. Union-Find}
```

[Path Compression + Union by Size · Connected Components · Tier 1 · python/041\_union\_find.py]{.meta}

Keep nodes 0..n-1 in disjoint groups: union(a, b) merges two groups, find(x) names the root of x's group, and a count tracks how many groups remain. Five nodes joined by \[0, 1\], \[2, 3\], \[0, 2\], \[3, 1\] (the last edge is redundant) form two groups: count\_components(5, edges) → 2.

```python
# --- algorithm ---
class UnionFind:
    """Each group is a tree of parent pointers, named by its root."""

    def __init__(self, n):
        self.parent = list(range(n))    # every node starts as its own root
        self.size = [1] * n             # tree sizes, read only at roots
        self.count = n                  # number of separate groups

    def find(self, x):
        """Root of x; repoint the path straight at it. Near O(1) amortized."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])    # path compression
        return self.parent[x]

    def union(self, a, b):
        """Hang the smaller tree under the bigger root; False if already one.
        Near O(1) amortized."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False                # already connected: a cycle edge
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a     # root_a is the bigger tree
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        self.count -= 1
        return True


def count_components(n, edges):
    """Union the ends of every edge; count what is left. Near O(n + E)."""
    uf = UnionFind(n)
    for a, b in edges:
        uf.union(a, b)
    return uf.count


def find_redundant_connection(edges):
    """Nodes are 1..n; the first edge inside one group closes the cycle.
    Near O(n) for n edges."""
    uf = UnionFind(len(edges) + 1)      # slot 0 is never used
    for a, b in edges:
        if not uf.union(a, b):
            return [a, b]
    return []


# --- try it ---
print(count_components(5, [[0, 1], [2, 3], [0, 2], [3, 1]]))    # -> 2
print(count_components(4, []))                                  # -> 4
print(find_redundant_connection([[1, 2], [1, 3], [2, 3]]))      # -> [2, 3]
edges = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
print(find_redundant_connection(edges))                         # -> [1, 4]
```

```{=latex}
\clearpage
```

## 42. Dijkstra's Algorithm {#a42}

```{=latex}
\markright{42. Dijkstra's Algorithm}
```

[Shortest Paths with Non-Negative Weights · Shortest Path · Tier 1 · python/042\_dijkstra.py]{.meta}

A signal leaves node k of a network with nodes 1..n, and times\[i\] = \[u, v, w\] says it takes w to cross the directed edge u → v. Return the time until every node has the signal, or -1 if some node never gets it: n = 4, k = 1, \[\[1, 2, 4\], \[1, 3, 1\], \[3, 2, 2\], \[2, 4, 1\], \[3, 4, 5\]\] → 4.

```python
import heapq            # heappush / heappop keep the smallest at index 0
import math             # math.inf: no route known yet


# --- algorithm ---
def dijkstra(graph, source):
    """Pop the closest unsettled node; its distance is final. Relax its edges.
    O((V + E) log V) time."""
    dist = [math.inf] * len(graph)
    dist[source] = 0
    heap = []
    heapq.heappush(heap, (0, source))   # (distance so far, node)
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                    # stale entry: node was settled closer
        for neighbor, weight in graph[node]:
            if d + weight < dist[neighbor]:     # relax: a shorter route
                dist[neighbor] = d + weight
                heapq.heappush(heap, (dist[neighbor], neighbor))
    return dist


def network_delay_time(times, n, k):
    """Each node hears the signal at its shortest distance; take the largest.
    O((V + E) log V)."""
    graph = []
    for _ in range(n + 1):              # nodes are 1..n; slot 0 is unused
        graph.append([])
    for u, v, w in times:
        graph[u].append((v, w))
    dist = dijkstra(graph, k)
    slowest = 0
    for node in range(1, n + 1):
        if dist[node] == math.inf:
            return -1                   # this node never gets the signal
        slowest = max(slowest, dist[node])
    return slowest


# --- try it ---
times = [[1, 2, 4], [1, 3, 1], [3, 2, 2], [2, 4, 1], [3, 4, 5]]
print(network_delay_time(times, 4, 1))                              # -> 4
print(network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2))  # -> 2
print(network_delay_time([[1, 2, 1]], 2, 2))                        # -> -1
graph = [[], [(2, 4), (3, 1)], [(4, 1)], [(2, 2), (4, 5)], []]
print(dijkstra(graph, 1))                           # -> [inf, 0, 3, 1, 4]
```

```{=latex}
\clearpage
```

## 43. Trie {#a43}

```{=latex}
\markright{43. Trie}
```

[Insert, Search, Starts With · Tries · Tier 1 · python/043\_trie.py]{.meta}

Store words so that search(word) says whether that exact word was inserted and starts\_with(prefix) whether any inserted word begins with prefix: after inserting apple, app, apt and bat, search("ap") → False and starts\_with("ap") → True.

```python
# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}              # letter -> TrieNode
        self.is_end = False             # True if a word ends at this node


# --- algorithm ---
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Walk down the letters, creating missing children. O(L)."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True              # flag the node where the word stops

    def walk(self, prefix):
        """Follow the letters of prefix; the last node, or None. O(L)."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None             # the path breaks off
            node = node.children[ch]
        return node

    def search(self, word):
        """The path must exist and end on a flagged node. O(L)."""
        node = self.walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """The path existing is enough. O(L)."""
        return self.walk(prefix) is not None


# --- try it ---
trie = Trie()
for word in ["apple", "app", "apt", "bat"]:
    trie.insert(word)
print(trie.search("app"))           # -> True
print(trie.search("ap"))            # -> False
print(trie.starts_with("ap"))       # -> True
print(trie.search("apl"))           # -> False
print(trie.starts_with("c"))        # -> False
```

```{=latex}
\clearpage
```

## 44. LRU Cache {#a44}

```{=latex}
\markright{44. LRU Cache}
```

[Hash Map + Doubly Linked List · Design · Tier 1 · python/044\_lru\_cache.py]{.meta}

Design a cache with a fixed capacity: get(key) returns the value or -1, and put(key, value) inserts or updates; a put that overflows the capacity evicts the least recently used key. Capacity 2: put(1, 10), put(2, 20), get(1), put(3, 30), get(2) → 10, -1.

```python
# --- helpers ---
class Node:
    def __init__(self, key, value):
        self.key = key              # kept so eviction can clean the map
        self.value = value
        self.prev = None
        self.next = None


# --- algorithm ---
class LRUCache:
    """Map key -> node; the list runs from most to least recently used."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}             # key -> node
        self.head = Node(0, 0)      # sentinel: head.next is most recent
        self.tail = Node(0, 0)      # sentinel: tail.prev is least recent
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node):
        """Unlink node: its two neighbors point past it. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def add_front(self, node):
        """Splice node in right after head, the most recent spot. O(1)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Return the value and make the key most recent; -1 if absent. O(1)."""
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self.remove(node)           # a read counts as a use
        self.add_front(node)
        return node.value

    def put(self, key, value):
        """Insert or update the key as most recent; if that overflows the
        capacity, evict the node before tail. O(1)."""
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self.remove(node)       # it moves to the front below
        else:
            node = Node(key, value)
            self.nodes[key] = node
        self.add_front(node)
        if len(self.nodes) > self.capacity:
            lru = self.tail.prev    # least recently used
            self.remove(lru)
            del self.nodes[lru.key]


# --- try it ---
cache = LRUCache(2)
cache.put(1, 10)
cache.put(2, 20)
print(cache.get(1))         # -> 10
cache.put(3, 30)            # evicts key 2
print(cache.get(2))         # -> -1
cache.put(4, 40)            # evicts key 1
print(cache.get(1))         # -> -1
print(cache.get(3))         # -> 30
print(cache.get(4))         # -> 40
```

```{=latex}
\clearpage
```

## 45. Design Hit Counter {#a45}

```{=latex}
\markright{45. Design Hit Counter}
```

[Circular Buckets over the Last 300 Seconds · Design · Tier 1 · python/045\_hit\_counter.py]{.meta}

Count recent hits: hit(t) records a hit at second t, and get\_hits(t) returns the hits at times s with t - 300 \< s \<= t (calls arrive in time order): hits at 1, 2, 2, 3, 300; get\_hits(300), get\_hits(301) → 5, 4.

```python
# --- algorithm ---
class HitCounter:
    """300 buckets, one per second of the window, reused round the clock."""

    def __init__(self):
        self.window = 300                   # seconds that get_hits looks back
        self.times = [0] * self.window      # bucket i: the second it counts
        self.counts = [0] * self.window     # bucket i: hits in that second

    def hit(self, timestamp):
        """Add the hit to bucket timestamp mod 300, reset if stale. O(1)."""
        slot = timestamp % self.window
        if self.times[slot] != timestamp:   # empty, or 300+ seconds old
            self.times[slot] = timestamp
            self.counts[slot] = 0
        self.counts[slot] += 1

    def get_hits(self, timestamp):
        """Add up the buckets whose second is under 300 seconds old. O(300)."""
        total = 0
        for slot in range(self.window):
            if timestamp - self.times[slot] < self.window:  # inside the window
                total += self.counts[slot]
        return total


# --- try it ---
counter = HitCounter()
counter.hit(1)
counter.hit(2)
counter.hit(2)
counter.hit(3)
print(counter.get_hits(4))                              # -> 4
counter.hit(300)
print(counter.get_hits(300), counter.get_hits(301))     # -> 5 4
counter.hit(301)                    # bucket 1 still holds second 1: reset
print(counter.get_hits(301))                            # -> 5
print(counter.get_hits(600), counter.get_hits(601))     # -> 1 0
```

```{=latex}
\clearpage
```

## 46. Design Twitter {#a46}

```{=latex}
\markright{46. Design Twitter}
```

[Merge the Followees' Feeds with a Heap · Design · Tier 1 · python/046\_design\_twitter.py]{.meta}

Users post tweets and follow each other; get\_news\_feed(user) returns the ids of the 10 most recent tweets by the user or anyone they follow, newest first. Users 1, 2, 3, 2, 1, 3 post 11, 21, 31, 22, 12, 32 and user 1 follows 2 and 3 → the feed of user 1 is \[32, 12, 22, 31, 21, 11\].

```python
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class Twitter:
    """Per-user tweet lists stamped by one global clock; a feed merges them."""

    def __init__(self):
        self.clock = 0              # stamps tweets: higher means newer
        self.tweets = {}            # user -> list of (time, tweet_id)
        self.following = {}         # user -> set of the users they follow

    def post_tweet(self, user, tweet_id):
        """Append the tweet, stamped with the next clock value. O(1)."""
        if user not in self.tweets:
            self.tweets[user] = []
        self.tweets[user].append((self.clock, tweet_id))    # oldest first
        self.clock += 1

    def follow(self, follower, followee):
        """Add followee to the follower's set. O(1)."""
        if follower == followee:
            return                  # your own tweets always count anyway
        if follower not in self.following:
            self.following[follower] = set()
        self.following[follower].add(followee)

    def unfollow(self, follower, followee):
        """Remove followee from the follower's set, if it is there. O(1)."""
        if follower in self.following:
            self.following[follower].discard(followee)  # no error if absent

    def get_news_feed(self, user):
        """Merge the sources' lists with a max-heap seeded with each newest
        tweet; stop after 10 pops. O(k log k) for k sources."""
        sources = [user]
        if user in self.following:
            for followee in self.following[user]:
                sources.append(followee)
        heap = []                   # max-heap by time: times go in negated
        for source in sources:
            if source in self.tweets:
                index = len(self.tweets[source]) - 1        # its newest tweet
                time, tweet_id = self.tweets[source][index]
                heapq.heappush(heap, (-time, tweet_id, source, index))
        feed = []
        while len(heap) > 0 and len(feed) < 10:
            neg_time, tweet_id, source, index = heapq.heappop(heap)
            feed.append(tweet_id)   # the newest tweet not yet taken
            if index > 0:           # that source has an older tweet
                time, older_id = self.tweets[source][index - 1]
                heapq.heappush(heap, (-time, older_id, source, index - 1))
        return feed


# --- try it ---
twitter = Twitter()
posts = [(1, 11), (2, 21), (3, 31), (2, 22), (1, 12), (3, 32)]
for user, tweet_id in posts:
    twitter.post_tweet(user, tweet_id)
print(twitter.get_news_feed(1))             # -> [12, 11]
twitter.follow(1, 2)
twitter.follow(1, 3)
print(twitter.get_news_feed(1))             # -> [32, 12, 22, 31, 21, 11]
twitter.unfollow(1, 3)
twitter.unfollow(1, 1)                      # cannot unfollow yourself
print(twitter.get_news_feed(1))             # -> [12, 22, 21, 11]
print(twitter.get_news_feed(2), twitter.get_news_feed(5))   # -> [22, 21] []
for tweet_id in range(40, 52):
    twitter.post_tweet(4, tweet_id)
feed = twitter.get_news_feed(4)
print(len(feed), feed[0], feed[9])          # -> 10 51 42
```

```{=latex}
\clearpage
```

## 47. Snapshot Array {#a47}

```{=latex}
\markright{47. Snapshot Array}
```

[Per-Index History + Binary Search · Design · Tier 1 · python/047\_snapshot\_array.py]{.meta}

An array of zeros with set(index, val), snap() that takes a snapshot and returns its id (0, 1, 2, ...), and get(index, snap\_id), the value at index in that snapshot: set(0, 5), snap() → 0, then set(0, 6); get(0, 0) → 5.

```python
# --- algorithm ---
class SnapshotArray:
    """Each index keeps its own history of (snap_id, value) pairs."""

    def __init__(self, length):
        self.history = []                   # index -> list of (snap_id, value)
        for i in range(length):
            self.history.append([])
        self.snap_id = 0                    # the id the next snap() returns

    def set(self, index, val):
        """Record val under the open snap id, rewriting a pair written since
        the last snap. O(1)."""
        pairs = self.history[index]
        last = len(pairs) - 1               # the newest pair, if any
        if last >= 0 and pairs[last][0] == self.snap_id:
            pairs[last] = (self.snap_id, val)   # same snapshot: rewrite it
        else:
            pairs.append((self.snap_id, val))

    def snap(self):
        """Close the open snapshot and return its id. O(1)."""
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index, snap_id):
        """The last pair at or before snap_id, by binary search. O(log w)."""
        pairs = self.history[index]
        left = 0
        right = len(pairs)
        while left < right:                 # find the first pair after snap_id
            mid = (left + right) // 2
            if pairs[mid][0] <= snap_id:
                left = mid + 1              # mid was written by then
            else:
                right = mid                 # mid is later: maybe the first
        if left == 0:
            return 0                        # not written by that snapshot
        return pairs[left - 1][1]


# --- try it ---
array = SnapshotArray(3)
array.set(0, 5)
print(array.snap())                         # -> 0
array.set(0, 6)
array.set(1, 4)
array.set(0, 8)                             # rewrites the 6: same snapshot
print(array.get(0, 0), array.history[0])    # -> 5 [(0, 5), (1, 8)]
print(array.snap(), array.snap())           # -> 1 2
array.set(1, 9)
print(array.snap(), array.history[1])       # -> 3 [(1, 4), (3, 9)]
print(array.get(0, 2), array.get(1, 2), array.get(1, 0))    # -> 8 4 0
print(array.get(1, 3), array.get(2, 3))     # -> 9 0
```

```{=latex}
\clearpage
```

## 48. Design Tic-Tac-Toe {#a48}

```{=latex}
\markright{48. Design Tic-Tac-Toe}
```

[Row, Column and Diagonal Counters · Design · Tier 1 · python/048\_tic\_tac\_toe.py]{.meta}

Two players alternate valid moves on an n x n board; move(row, col, player) returns the player who has just filled a whole row, column or diagonal, or 0. n = 3, moves (0,0,1) (0,2,2) (2,2,1) (1,1,2) (2,0,1) (1,0,2) (2,1,1) → 0 0 0 0 0 0 1.

```python
# --- algorithm ---
class TicTacToe:
    """One signed counter per row, per column and per long diagonal."""

    def __init__(self, n):
        self.n = n
        self.rows = [0] * n             # player 1 adds +1, player 2 adds -1
        self.cols = [0] * n
        self.diagonal = 0               # cells with row == col
        self.anti_diagonal = 0          # cells with row + col == n - 1

    def move(self, row, col, player):
        """Add the player's sign to each line through the cell; a counter at
        n or -n means a line full of that player's marks. O(1)."""
        sign = 1
        if player == 2:
            sign = -1
        self.rows[row] += sign
        self.cols[col] += sign
        if row == col:
            self.diagonal += sign
        if row + col == self.n - 1:     # not elif: the center is on both
            self.anti_diagonal += sign
        if abs(self.rows[row]) == self.n or abs(self.cols[col]) == self.n:
            return player
        if abs(self.diagonal) == self.n or abs(self.anti_diagonal) == self.n:
            return player
        return 0


# --- try it ---
game = TicTacToe(3)
moves = [(0, 0, 1), (0, 2, 2), (2, 2, 1), (1, 1, 2), (2, 0, 1), (1, 0, 2)]
results = []
for row, col, player in moves:
    results.append(game.move(row, col, player))
print(results)                              # -> [0, 0, 0, 0, 0, 0]
print(game.move(2, 1, 1))                   # -> 1
print(game.rows, game.cols)                 # -> [0, -2, 3] [1, 0, 0]
print(game.diagonal, game.anti_diagonal)    # -> 1 -1
game = TicTacToe(3)
for row, col, player in [(0, 0, 1), (0, 2, 2), (2, 2, 1), (1, 1, 2), (1, 0, 1)]:
    game.move(row, col, player)
print(game.move(2, 0, 2), game.anti_diagonal)   # -> 2 -3
print(TicTacToe(1).move(0, 0, 2))               # -> 2
```

```{=latex}
\clearpage
```

## 49. Flatten Nested List Iterator {#a49}

```{=latex}
\markright{49. Flatten Nested List Iterator}
```

[A Stack of List Positions · Design · Tier 1 · python/049\_flatten\_nested\_list\_iterator.py]{.meta}

Iterate over the integers of a nested list, where each item is an integer or another nested list: next() returns the next integer from left to right and has\_next() says whether one is left. \[1, \[4, \[6\]\], \[\], 8\] → 1, 4, 6, 8.

```python
# --- helpers ---
def drain(iterator):
    """Call next() while has_next() is true; return the values in order."""
    values = []
    while iterator.has_next():
        values.append(iterator.next())
    return values


# --- algorithm ---
class NestedIterator:
    """A stack of [list, index] frames, the innermost open list on top."""

    def __init__(self, nested):
        self.stack = []
        self.stack.append([nested, 0])      # frame: a list and its next index

    def has_next(self):
        """Move the top frame onto an integer: pop used-up lists, enter
        sub-lists. O(1) amortized."""
        while len(self.stack) > 0:
            frame = self.stack[-1]
            items = frame[0]
            index = frame[1]
            if index == len(items):
                self.stack.pop()            # this list is used up
            elif isinstance(items[index], list):
                frame[1] = index + 1        # step past the sub-list first
                self.stack.append([items[index], 0])    # then enter it
            else:
                return True                 # the top points at an integer
        return False

    def next(self):
        """Settle on an integer, return it and step past it. O(1) amortized."""
        self.has_next()
        frame = self.stack[-1]
        value = frame[0][frame[1]]
        frame[1] += 1
        return value


# --- try it ---
iterator = NestedIterator([1, [4, [6]], [], 8])
print(iterator.next(), iterator.has_next(), iterator.next())  # -> 1 True 4
print(iterator.next(), iterator.next(), iterator.has_next())  # -> 6 8 False
print(drain(NestedIterator([[1, 1], 2, [1, 1]])))     # -> [1, 1, 2, 1, 1]
print(drain(NestedIterator([[], [[]]])))              # -> []
```

```{=latex}
\clearpage
```

## 50. Key-Value Store with Transactions {#a50}

```{=latex}
\markright{50. Key-Value Store with Transactions}
```

[A Stack of Undo Logs · Design · Tier 1 · python/050\_kv\_store\_transactions.py]{.meta}

Design a key-value store with set, get and delete plus nested transactions: begin() opens one, rollback() undoes the innermost and commit() makes them all permanent: set a = 10, begin, set a = 20, rollback → get a is 10 again.

```python
# --- algorithm ---
class KeyValueStore:
    """The live dict plus a stack of undo logs, one per open transaction.
    set, get, delete, begin and commit O(1); rollback O(changes undone)."""

    def __init__(self):
        self.data = {}              # key -> value: the live state
        self.logs = []              # stack of undo logs, innermost last

    def record(self, key):
        """Log the key's value before its first change in this level. O(1)."""
        if len(self.logs) == 0:
            return                  # no transaction: nothing to undo
        log = self.logs[-1]         # the innermost transaction
        if key not in log:          # only the first change is kept
            log[key] = self.get(key)    # None: the key was absent

    def set(self, key, value):
        """Log the old value, then write the new one. O(1)."""
        self.record(key)
        self.data[key] = value

    def get(self, key):
        """The live value, or None when the key is absent. O(1)."""
        if key in self.data:
            return self.data[key]
        return None

    def delete(self, key):
        """Log the old value, then remove the key. O(1)."""
        if key in self.data:
            self.record(key)
            del self.data[key]

    def begin(self):
        """Open a nested transaction with an empty undo log. O(1)."""
        self.logs.append({})

    def rollback(self):
        """Pop the innermost log, write back its k saved values. O(k)."""
        if len(self.logs) == 0:
            return "NO TRANSACTION"
        log = self.logs.pop()       # undo the innermost level only
        for key in log:
            if log[key] is None:            # absent before the level began
                if key in self.data:
                    del self.data[key]
            else:
                self.data[key] = log[key]   # the value before the level
        return "OK"

    def commit(self):
        """Make every open transaction permanent by dropping the logs. O(1)."""
        if len(self.logs) == 0:
            return "NO TRANSACTION"
        self.logs = []              # nothing can be undone any more
        return "OK"


# --- try it ---
store = KeyValueStore()
store.set("a", 10)
store.begin()
store.set("a", 20)
store.set("b", 30)
store.begin()
store.delete("a")
store.set("b", 40)
store.set("b", 45)              # a second change: the log keeps b: 30
print(store.get("a"), store.get("b"))                     # -> None 45
print(store.rollback(), store.get("a"), store.get("b"))   # -> OK 20 30
print(store.rollback(), store.get("a"), store.get("b"))   # -> OK 10 None
print(store.rollback())                                   # -> NO TRANSACTION
store.begin()
store.set("a", 50)
store.begin()
store.set("c", 70)
print(store.commit(), store.get("a"), store.get("c"))     # -> OK 50 70
print(store.rollback(), store.get("a"))                   # -> NO TRANSACTION 50
```

# Tier 2 · Should Know Well {#tier2}

```{=latex}
\markboth{Tier 2 · Should Know Well}{}
```

The next fifty deepen every topic of the first tier and add the classic harder variants: partition-based selection, patience sorting, the histogram stack, expression evaluation, the greedy exchange arguments, grid backtracking, BFS on implicit graphs, topological order by DFS, KMP, and a second wave of designs: LFU, expiring caches, autocomplete, calendars, the snake game and the URL shortener. They come up often enough that each one deserves a careful read and a run of its code.

```{=latex}
\clearpage
```

## 51. Hash Map with Separate Chaining {#a51}

```{=latex}
\markright{51. Hash Map with Separate Chaining}
```

[Collisions Live in Buckets · Hash Map Internals · Tier 2 · python/051\_hash\_map\_chaining.py]{.meta}

Design a hash map without a built-in dict: put(key, value) inserts or overwrites, get(key) returns the value or -1, remove(key) deletes the key. With 8 buckets, keys 1 and 9 share bucket 1: put(1, 10), put(9, 90), get(9) → 90.

```python
# --- algorithm ---
class ChainedHashMap:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0                       # number of keys stored
        self.buckets = []
        for i in range(capacity):
            self.buckets.append([])         # one empty chain per bucket

    def bucket_of(self, key):
        """The chain that holds key: bucket hash(key) mod capacity. O(1)."""
        return self.buckets[hash(key) % self.capacity]

    def put(self, key, value):
        """Overwrite the key in its chain or append a new pair. Average O(1)."""
        bucket = self.bucket_of(key)
        for pair in bucket:
            if pair[0] == key:              # same key: overwrite the value
                pair[1] = value
                return
        bucket.append([key, value])         # new key: the chain grows by one
        self.size += 1
        if self.size / self.capacity > 0.75:
            self.resize()                   # load factor too high: grow

    def get(self, key):
        """Scan only the key's chain. Average O(1), worst O(n)."""
        bucket = self.bucket_of(key)
        for pair in bucket:
            if pair[0] == key:              # compare keys, not hashes
                return pair[1]
        return -1

    def remove(self, key):
        """Unlink the key's pair from its chain if present. Average O(1)."""
        bucket = self.bucket_of(key)
        for pair in bucket:
            if pair[0] == key:
                bucket.remove(pair)
                self.size -= 1
                return

    def resize(self):
        """Double the bucket array and rehash every pair. O(n), but rare."""
        old_buckets = self.buckets
        self.capacity = 2 * self.capacity
        self.buckets = []
        for i in range(self.capacity):
            self.buckets.append([])
        for bucket in old_buckets:
            for pair in bucket:
                new_bucket = self.bucket_of(pair[0])    # uses the new capacity
                new_bucket.append(pair)


# --- try it ---
table = ChainedHashMap()
table.put(1, 10)
table.put(9, 90)                            # 9 mod 8 = 1: same bucket as 1
table.put(1, 11)                            # overwrite
print(table.get(1), table.get(9), table.get(2))     # -> 11 90 -1
table.remove(9)
print(table.get(9), table.size)             # -> -1 1
for key in range(2, 8):
    table.put(key, key * 10)
print(table.capacity, table.size, table.get(7))     # -> 16 7 70
```

```{=latex}
\clearpage
```

## 52. Dutch National Flag {#a52}

```{=latex}
\markright{52. Dutch National Flag}
```

[Three-Way Partition in One Pass · Two Pointers · Tier 2 · python/052\_dutch\_national\_flag.py]{.meta}

Given an array holding only 0s, 1s and 2s (three colors), sort it in place in a single pass with O(1) extra space: \[2, 0, 2, 1, 1, 0\] → \[0, 0, 1, 1, 2, 2\].

```python
# --- algorithm ---
def sort_colors(nums):
    """Grow the 0s from the left and the 2s from the right; the 1s are left
    in the middle. One pass, O(n) time, O(1) space."""
    low = 0                         # nums[0..low-1] are 0s
    mid = 0                         # nums[low..mid-1] are 1s
    high = len(nums) - 1            # nums[high+1..n-1] are 2s
    while mid <= high:              # nums[mid..high] is still unseen
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1                # the block of 1s shifts right
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1               # mid stays: this value is unseen


# --- try it ---
colors = [2, 0, 2, 1, 1, 0]
sort_colors(colors)
print(colors)                       # -> [0, 0, 1, 1, 2, 2]
colors = [1, 2, 0]
sort_colors(colors)
print(colors)                       # -> [0, 1, 2]
colors = [2, 2, 0, 0]
sort_colors(colors)
print(colors)                       # -> [0, 0, 2, 2]
```

```{=latex}
\clearpage
```

## 53. Longest Repeating Character Replacement {#a53}

```{=latex}
\markright{53. Longest Repeating Character Replacement}
```

[Window Length Minus Top Count at Most k · Sliding Window · Tier 2 · python/053\_longest\_repeating\_character\_replacement.py]{.meta}

Given a string of uppercase letters and an integer k, return the length of the longest substring that becomes one repeated letter after replacing at most k of its characters: "AABABBA", k 1 → 4 ("AABA" becomes "AAAA").

```python
# --- algorithm ---
def character_replacement(s, k):
    """Grow the window s[left..right]; slide left while length - max_count > k.
    max_count, the top count so far, never drops. O(n) time, O(26) space."""
    count = [0] * 26                # letter counts inside the window
    max_count = 0                   # top single-letter count seen so far
    left = 0
    best = 0
    for right in range(len(s)):
        slot = ord(s[right]) - ord('A')
        count[slot] += 1
        max_count = max(max_count, count[slot])
        while right - left + 1 - max_count > k:     # too many to replace
            drop = ord(s[left]) - ord('A')
            count[drop] -= 1
            left += 1               # runs at most once per step
        best = max(best, right - left + 1)
    return best


# --- try it ---
print(character_replacement("AABABBA", 1))   # -> 4
print(character_replacement("ABAB", 2))      # -> 4
print(character_replacement("ABCDE", 1))     # -> 2
print(character_replacement("AAAA", 0))      # -> 4
print(character_replacement("", 2))          # -> 0
```

```{=latex}
\clearpage
```

## 54. Minimum Size Subarray Sum {#a54}

```{=latex}
\markright{54. Minimum Size Subarray Sum}
```

[Shrink While the Sum Is Enough · Sliding Window · Tier 2 · python/054\_minimum\_size\_subarray\_sum.py]{.meta}

Given an array of positive integers and a positive target, return the length of the shortest contiguous subarray whose sum is at least the target, or 0 if there is none: \[2, 3, 1, 2, 4, 3\], target 7 → 2 (the subarray \[4, 3\]).

```python
# --- algorithm ---
def min_subarray_len(nums, target):
    """Grow the window on the right; while its sum reaches the target, record
    its length and shrink it from the left. O(n) time, O(1) space."""
    left = 0
    window_sum = 0                  # sum of nums[left..right]
    best = len(nums) + 1            # longer than any real window
    for right in range(len(nums)):
        window_sum += nums[right]           # expand: take one more value
        while window_sum >= target:         # enough: record, then shrink
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1
    if best > len(nums):
        return 0                    # no window ever reached the target
    return best


# --- try it ---
print(min_subarray_len([2, 3, 1, 2, 4, 3], 7))      # -> 2
print(min_subarray_len([1, 4, 4], 4))               # -> 1
print(min_subarray_len([1, 1, 1, 1, 7], 7))         # -> 1
print(min_subarray_len([1, 1, 1, 1, 1], 11))        # -> 0
print(min_subarray_len([], 3))                      # -> 0
```

```{=latex}
\clearpage
```

## 55. Median of Two Sorted Arrays {#a55}

```{=latex}
\markright{55. Median of Two Sorted Arrays}
```

[Binary Search the Partition · Binary Search · Tier 2 · python/055\_median\_two\_sorted\_arrays.py]{.meta}

Given two sorted arrays with at least one value between them, return the median of all their values together in O(log(m + n)) time: \[1, 3, 8, 9, 15\] and \[7, 11, 18, 19, 21, 25\] → 11.

```python
import math                         # math.inf: a cut at the edge sees infinity


# --- algorithm ---
def value_at(arr, k):
    """arr[k], or -inf before the start and +inf past the end. O(1)."""
    if k < 0:
        return -math.inf
    if k >= len(arr):
        return math.inf
    return arr[k]


def find_median(a, b):
    """Binary search the cut i in the shorter array; b's cut j follows.
    O(log min(m, n)) time, O(1) space."""
    if len(a) > len(b):
        a, b = b, a                 # search the shorter array
    m = len(a)
    n = len(b)
    half = (m + n + 1) // 2         # size of the left part
    lo = 0
    hi = m
    while lo <= hi:
        i = (lo + hi) // 2          # a[:i] goes to the left part
        j = half - i                # b[:j] fills the rest of it
        a_left = value_at(a, i - 1)
        a_right = value_at(a, i)
        b_left = value_at(b, j - 1)
        b_right = value_at(b, j)
        if a_left <= b_right and b_left <= a_right:    # every left <= right
            if (m + n) % 2 == 1:
                return max(a_left, b_left)
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
        if a_left > b_right:
            hi = i - 1              # too much of a on the left: cut a earlier
        else:
            lo = i + 1              # too little of a on the left: cut a later


# --- try it ---
print(find_median([1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25]))    # -> 11
print(find_median([1, 3], [2]))                                 # -> 2
print(find_median([1, 2], [3, 4]))                              # -> 2.5
print(find_median([], [4]))                                     # -> 4
```

```{=latex}
\clearpage
```

## 56. Search a 2D Matrix {#a56}

```{=latex}
\markright{56. Search a 2D Matrix}
```

[Staircase from the Top-Right Corner · Binary Search · Tier 2 · python/056\_search\_2d\_matrix.py]{.meta}

Given a matrix whose rows are sorted left to right and whose columns are sorted top to bottom, report whether a target is present: \[\[1, 4, 7, 11, 15\], \[2, 5, 8, 12, 19\], \[3, 6, 9, 16, 22\], \[10, 13, 14, 17, 24\], \[18, 21, 23, 26, 30\]\], target 5 → True.

```python
# --- algorithm ---
def staircase_search(matrix, target):
    """Rows and columns sorted: start at the top-right corner; each step
    rules out a whole row or column. O(m + n) time, O(1) space."""
    if len(matrix) == 0:
        return False
    row = 0
    col = len(matrix[0]) - 1        # top-right: row's max, column's min
    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1                # the rest of this column is bigger still
        else:
            row += 1                # the rest of this row is smaller still
    return False


def flattened_search(matrix, target):
    """Each row starts above the previous row's end: one lower-bound search
    over the flat positions 0 .. m*n - 1. O(log(m n)) time, O(1) space."""
    if len(matrix) == 0:
        return False
    cols = len(matrix[0])
    lo = 0
    hi = len(matrix) * cols         # half-open [lo, hi) of flat positions
    while lo < hi:
        mid = (lo + hi) // 2
        value = matrix[mid // cols][mid % cols]     # fold into a cell
        if value < target:
            lo = mid + 1
        else:
            hi = mid
    if lo == len(matrix) * cols:
        return False                # every value is smaller than the target
    return matrix[lo // cols][lo % cols] == target


# --- try it ---
grid = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
print(staircase_search(grid, 5))            # -> True
print(staircase_search(grid, 20))           # -> False
rows = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
print(flattened_search(rows, 3))            # -> True
print(flattened_search(rows, 13))           # -> False
print(flattened_search(rows, 61))           # -> False
```

```{=latex}
\clearpage
```

## 57. Find Peak Element {#a57}

```{=latex}
\markright{57. Find Peak Element}
```

[Binary Search Uphill · Binary Search · Tier 2 · python/057\_find\_peak\_element.py]{.meta}

Given an array in which no two neighbors are equal, return the index of a peak, a value larger than both neighbors, where the positions just outside the array count as -infinity. Any peak will do: \[1, 2, 1, 3, 5, 6, 4\] → 5 (index 1 would be valid too).

```python
# --- algorithm ---
def find_peak_element(nums):
    """Climb toward the higher of nums[mid] and nums[mid + 1]: a peak lies
    that way, so half the range can go. O(log n) time, O(1) space."""
    lo = 0
    hi = len(nums) - 1              # closed window [lo, hi] holds a peak
    while lo < hi:
        mid = (lo + hi) // 2        # mid < hi, so nums[mid + 1] exists
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1            # rising: a peak lies right of mid
        else:
            hi = mid                # falling: a peak at mid or left of it
    return lo


# --- try it ---
print(find_peak_element([1, 2, 1, 3, 5, 6, 4]))    # -> 5
print(find_peak_element([1, 2, 3, 1]))             # -> 2
print(find_peak_element([0, 2, 5, 9, 7, 3]))       # -> 3
print(find_peak_element([5, 4, 3]))                # -> 0
print(find_peak_element([7]))                      # -> 0
```

```{=latex}
\clearpage
```

## 58. Longest Increasing Subsequence {#a58}

```{=latex}
\markright{58. Longest Increasing Subsequence}
```

[Patience Sorting with Binary Search · Binary Search · Tier 2 · python/058\_longest\_increasing\_subsequence.py]{.meta}

Given an array of integers, return the length of its longest strictly increasing subsequence (kept in order, not necessarily adjacent): \[10, 9, 2, 5, 3, 7, 101, 18\] → 4 (for example 2, 3, 7, 18).

```python
# --- algorithm ---
def lower_bound(values, target):
    """First index i with values[i] >= target, len(values) if none. O(log n)."""
    lo = 0
    hi = len(values)                # half-open [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def length_of_lis(nums):
    """tails[k] is the smallest tail of an increasing subsequence of length
    k + 1; each x replaces the first tail >= x or extends. O(n log n)."""
    tails = []
    for x in nums:
        i = lower_bound(tails, x)   # how many tails are smaller than x
        if i == len(tails):
            tails.append(x)         # x extends the longest subsequence
        else:
            tails[i] = x            # a smaller tail for length i + 1
    return len(tails)


# --- try it ---
print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))     # -> 4
print(length_of_lis([0, 1, 0, 3, 2, 3]))               # -> 4
print(length_of_lis([7, 7, 7, 7]))                     # -> 1
print(length_of_lis([4, 5, 6, 1]))                     # -> 3
print(length_of_lis([]))                               # -> 0
```

```{=latex}
\clearpage
```

## 59. Heapify {#a59}

```{=latex}
\markright{59. Heapify}
```

[Build a Heap in O(n) with Sift-Down · Heaps · Tier 2 · python/059\_heapify.py]{.meta}

Rearrange an array in place into a min-heap, a tree stored level by level in which every parent is at most its children, then push and pop on it by hand: \[9, 5, 6, 2, 3, 7, 1\] → \[1, 2, 6, 5, 3, 7, 9\].

```python
import heapq   # the library min-heap, used here only to compare


# --- algorithm ---
def sift_down(heap, i, n):
    """Swap heap[i] with its smaller child until no child is smaller; only
    heap[0..n-1] is the heap. O(log n)."""
    while True:
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right
        if smallest == i:               # no child is smaller: done
            return
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest


def heapify(heap):
    """Sift down every parent, the last parent first. O(n) in total."""
    n = len(heap)
    for i in range(n // 2 - 1, -1, -1):  # last parent, back to the root
        sift_down(heap, i, n)


def sift_up(heap, i):
    """Swap heap[i] with its parent while it is smaller. O(log n)."""
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:     # the parent is no larger: done
            return
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def heap_push(heap, value):
    """Add the value as the last leaf, then sift it up. O(log n)."""
    heap.append(value)
    sift_up(heap, len(heap) - 1)


def heap_pop(heap):
    """Swap the root with the last leaf, cut it off, sift down. O(log n)."""
    last = len(heap) - 1
    heap[0], heap[last] = heap[last], heap[0]
    top = heap.pop()                    # remove the last slot: the old root
    sift_down(heap, 0, len(heap))
    return top


# --- try it ---
nums = [9, 5, 6, 2, 3, 7, 1]
heapify(nums)
print(nums)                             # -> [1, 2, 6, 5, 3, 7, 9]
heap_push(nums, 4)
print(nums)                             # -> [1, 2, 6, 4, 3, 7, 9, 5]
print(heap_pop(nums))                   # -> 1
print(nums)                             # -> [2, 3, 6, 4, 5, 7, 9]
same = [9, 5, 6, 2, 3, 7, 1]
heapq.heapify(same)                     # the library: same array this time
print(same)                             # -> [1, 2, 6, 5, 3, 7, 9]
```

```{=latex}
\clearpage
```

## 60. Quickselect {#a60}

```{=latex}
\markright{60. Quickselect}
```

[Kth Largest in Expected O(n) · Heaps · Tier 2 · python/060\_quickselect.py]{.meta}

Find the kth largest value of an unsorted array (duplicates count) without sorting it; the array is reordered in place: \[3, 2, 1, 5, 6, 4\], k = 2 → 5.

```python
import random   # random.randint(a, b) can return a or b too


# --- algorithm ---
def partition(nums, lo, hi):
    """Lomuto partition of nums[lo..hi] around a random pivot; return the
    pivot's final index. O(hi - lo) time."""
    pick = random.randint(lo, hi)
    nums[pick], nums[hi] = nums[hi], nums[pick]  # park the pivot at the end
    pivot = nums[hi]
    store = lo                        # invariant: nums[lo..store-1] < pivot
    for i in range(lo, hi):
        if nums[i] < pivot:           # a small value joins the left region
            nums[store], nums[i] = nums[i], nums[store]
            store += 1
    nums[store], nums[hi] = nums[hi], nums[store]  # pivot between the regions
    return store


def kth_largest(nums, k):
    """Partition, then keep only the side that holds index n - k.
    Expected O(n) time on distinct values, O(1) extra space."""
    target = len(nums) - k            # the answer's index in sorted order
    lo = 0
    hi = len(nums) - 1
    while True:
        p = partition(nums, lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1                # the answer is right of the pivot
        else:
            hi = p - 1                # the answer is left of the pivot


# --- try it ---
print(kth_largest([3, 2, 1, 5, 6, 4], 2))            # -> 5
print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # -> 4
print(kth_largest([7], 1))                           # -> 7
print(kth_largest([-2, 0, -5], 3))                   # -> -5
```

```{=latex}
\clearpage
```

## 61. Bucket Sort {#a61}

```{=latex}
\markright{61. Bucket Sort}
```

[Top K Frequent by Frequency Buckets · Sorting · Tier 2 · python/061\_bucket\_sort.py]{.meta}

Return the k most frequent values of an array in any order (the answer is unique), in O(n) instead of sorting by frequency: \[1, 1, 1, 2, 2, 3\], k = 2 → \[1, 2\].

```python
# --- algorithm ---
def top_k_frequent(nums, k):
    """Put each value in the bucket of its frequency, then read the buckets
    from the highest frequency down. O(n) time and space."""
    count = {}                              # value -> frequency
    for value in nums:
        count[value] = count.get(value, 0) + 1
    buckets = []                            # index = frequency
    for freq in range(len(nums) + 1):       # a frequency is at most n
        buckets.append([])
    for value in count:
        buckets[count[value]].append(value)
    result = []
    for freq in range(len(nums), 0, -1):    # most frequent first
        for value in buckets[freq]:
            result.append(value)
            if len(result) == k:
                return result
    return result


# --- try it ---
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))        # -> [1, 2]
print(top_k_frequent([4, 1, -1, 2, -1, 2, 3], 2))   # -> [-1, 2]
print(top_k_frequent([7, 7, 7], 1))                 # -> [7]
print(top_k_frequent([5], 1))                       # -> [5]
```

```{=latex}
\clearpage
```

## 62. Largest Rectangle in Histogram {#a62}

```{=latex}
\markright{62. Largest Rectangle in Histogram}
```

[Monotonic Increasing Stack · Stacks · Tier 2 · python/062\_largest\_rectangle\_histogram.py]{.meta}

Given bar heights of a histogram whose bars all have width 1, return the area of the largest rectangle that fits inside it: \[2, 1, 5, 6, 2, 3\] → 10 (the bars 5 and 6, height 5, width 2).

```python
# --- algorithm ---
def largest_rectangle_area(heights):
    """Stack of indices with rising heights; a shorter bar ends the popped
    bar's rectangle on the right. O(n) time, O(n) space."""
    bars = heights + [0]            # the 0 sentinel flushes the stack
    stack = []                      # indices; heights never fall
    best = 0
    for i in range(len(bars)):
        while len(stack) > 0 and bars[stack[-1]] > bars[i]:
            height = bars[stack.pop()]      # its rectangle ends at i - 1
            if len(stack) > 0:
                left = stack[-1] + 1        # just right of the new stack top
            else:
                left = 0                    # empty stack: reaches index 0
            width = i - left
            best = max(best, height * width)
        stack.append(i)
    return best


# --- try it ---
print(largest_rectangle_area([2, 1, 5, 6, 2, 3]))  # -> 10
print(largest_rectangle_area([2, 4]))              # -> 4
print(largest_rectangle_area([1, 2, 3]))           # -> 4
print(largest_rectangle_area([3, 3, 3]))           # -> 9
```

```{=latex}
\clearpage
```

## 63. Basic Calculator {#a63}

```{=latex}
\markright{63. Basic Calculator}
```

[Evaluate + - \* / and Parentheses with a Stack · Stacks · Tier 2 · python/063\_basic\_calculator.py]{.meta}

Evaluate a valid expression of non-negative integers, + - \* /, parentheses and spaces, with the usual precedence; / truncates toward zero and a minus may open the expression or a group: "2\*(3+4)-10/3" → 11.

```python
# --- algorithm ---
def calculate(s):
    """Evaluate the whole string. O(n) time, O(n) space."""
    value, end = evaluate(s, 0)
    return value


def evaluate(s, i):
    """Evaluate from index i up to the matching ')' or the end of s.
    Returns (value, next index to read). Linear in what it reads."""
    stack = []                  # signed terms of this level; value = their sum
    num = 0
    op = "+"                    # the operator in front of num
    while i < len(s):
        ch = s[i]
        i += 1
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "(":
            num, i = evaluate(s, i)     # a whole group acts as one number
        elif ch in "+-*/)":
            apply_op(stack, op, num)
            if ch == ")":
                return sum(stack), i
            op = ch
            num = 0
    apply_op(stack, op, num)
    return sum(stack), i


def apply_op(stack, op, num):
    """Fold num into the terms using the operator in front of it. O(1)."""
    if op == "+":
        stack.append(num)
    elif op == "-":
        stack.append(-num)
    elif op == "*":
        stack.append(stack.pop() * num)     # * reaches back one term only
    else:
        stack.append(int(stack.pop() / num))    # int() truncates toward 0


# --- try it ---
print(calculate("2*(3+4)-10/3"))           # -> 11
print(calculate(" 3+5 / 2 "))              # -> 5
print(calculate("(1+(4+5+2)-3)+(6+8)"))    # -> 23
print(calculate("-(2 + 3)"))               # -> -5
```

```{=latex}
\clearpage
```

## 64. Sliding Window Maximum {#a64}

```{=latex}
\markright{64. Sliding Window Maximum}
```

[Monotonic Deque · Queues · Tier 2 · python/064\_sliding\_window\_maximum.py]{.meta}

Given an array and a window size k, return the maximum of every window of k consecutive values as the window slides from left to right: \[9, 7, 8, 3, 2, 5, 1\], k 3 → \[9, 8, 8, 5, 5\].

```python
from collections import deque      # popleft is O(1)


# --- algorithm ---
def max_sliding_window(nums, k):
    """Deque of indices whose values decrease from front to back; the front
    is the window max. Each index enters and leaves once: O(n) time."""
    window = deque()                # indices of the candidates
    result = []
    for i in range(len(nums)):
        while len(window) > 0 and nums[window[-1]] <= nums[i]:
            window.pop()            # older and no larger: never needed again
        window.append(i)
        if window[0] <= i - k:
            window.popleft()        # the front slid out of the window
        if i >= k - 1:
            result.append(nums[window[0]])  # the front holds the window max
    return result


# --- try it ---
print(max_sliding_window([9, 7, 8, 3, 2, 5, 1], 3))    # -> [9, 8, 8, 5, 5]
nums = [1, 3, -1, -3, 5, 3, 6, 7]
print(max_sliding_window(nums, 3))                     # -> [3, 3, 5, 5, 6, 7]
print(max_sliding_window([4, 4, 4], 2))                # -> [4, 4]
print(max_sliding_window([5], 1))                      # -> [5]
```

```{=latex}
\clearpage
```

## 65. Insert Interval {#a65}

```{=latex}
\markright{65. Insert Interval}
```

[Before, Overlapping, After · Intervals · Tier 2 · python/065\_insert\_interval.py]{.meta}

Given closed intervals sorted by start and pairwise disjoint, insert one more, merging it with every interval it overlaps or touches, so the list stays sorted and disjoint: \[\[1, 2\], \[3, 5\], \[6, 7\], \[8, 10\], \[12, 16\]\] with \[4, 8\] → \[\[1, 2\], \[3, 10\], \[12, 16\]\].

```python
# --- algorithm ---
def insert_interval(intervals, new_interval):
    """Copy what ends before it, absorb what overlaps it, copy the rest.
    One pass and no sort: O(n) time, O(n) space for the output."""
    result = []
    new_start = new_interval[0]
    new_end = new_interval[1]
    i = 0
    n = len(intervals)
    while i < n and intervals[i][1] < new_start:     # ends before it starts
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new_end:      # overlaps or touches it
        new_start = min(new_start, intervals[i][0])  # the new interval grows
        new_end = max(new_end, intervals[i][1])
        i += 1
    result.append([new_start, new_end])              # added exactly once
    while i < n:                                     # starts after it ends
        result.append(intervals[i])
        i += 1
    return result


# --- try it ---
intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
print(insert_interval(intervals, [4, 8]))      # -> [[1, 2], [3, 10], [12, 16]]
print(insert_interval([[1, 3], [6, 9]], [2, 5]))       # -> [[1, 5], [6, 9]]
print(insert_interval([[1, 4]], [4, 6]))               # -> [[1, 6]]
print(insert_interval([[1, 2], [5, 6]], [3, 4]))  # -> [[1, 2], [3, 4], [5, 6]]
print(insert_interval([], [5, 7]))                     # -> [[5, 7]]
```

```{=latex}
\clearpage
```

## 66. Interval List Intersections {#a66}

```{=latex}
\markright{66. Interval List Intersections}
```

[Two Pointers over Two Sorted Lists · Intervals · Tier 2 · python/066\_interval\_list\_intersections.py]{.meta}

Given two lists of closed intervals, each sorted and pairwise disjoint, return the intersection of the two lists: \[\[0, 2\], \[5, 10\], \[13, 23\], \[24, 25\]\] and \[\[1, 5\], \[8, 12\], \[15, 24\], \[25, 26\]\] → \[\[1, 2\], \[5, 5\], \[8, 10\], \[15, 23\], \[24, 24\], \[25, 25\]\].

```python
# --- algorithm ---
def interval_intersection(first, second):
    """Overlap of the two current intervals is [later start, earlier end];
    then drop whichever ends first. O(m + n) time, O(1) extra space."""
    result = []
    i = 0
    j = 0
    while i < len(first) and j < len(second):
        first_start, first_end = first[i]
        second_start, second_end = second[j]
        overlap_start = max(first_start, second_start)  # the later start
        overlap_end = min(first_end, second_end)        # the earlier end
        if overlap_start <= overlap_end:
            result.append([overlap_start, overlap_end])     # a point counts too
        if first_end < second_end:
            i += 1                  # first[i] can meet nothing further on
        else:
            j += 1                  # second[j] can meet nothing further on
    return result


# --- try it ---
first = [[0, 2], [5, 10], [13, 23], [24, 25]]
second = [[1, 5], [8, 12], [15, 24], [25, 26]]
result = interval_intersection(first, second)
print(result[0:3])                  # -> [[1, 2], [5, 5], [8, 10]]
print(result[3:6])                  # -> [[15, 23], [24, 24], [25, 25]]
print(interval_intersection([[0, 10]], [[1, 2], [3, 4]]))  # -> [[1, 2], [3, 4]]
print(interval_intersection([[1, 3], [5, 9]], []))         # -> []
print(interval_intersection([[1, 7]], [[3, 10]]))          # -> [[3, 7]]
```

```{=latex}
\clearpage
```

## 67. Jump Game {#a67}

```{=latex}
\markright{67. Jump Game}
```

[Track the Farthest Reach · Greedy · Tier 2 · python/067\_jump\_game.py]{.meta}

In a non-empty array, nums\[i\] is the longest jump allowed from index i (any shorter jump is allowed too). Starting at index 0, can you reach the last index? \[2, 3, 1, 1, 4\] → True, \[3, 2, 1, 0, 4\] → False.

```python
# --- algorithm ---
def can_jump(nums):
    """Grow the block [0, farthest] while i is in it. O(n) time, O(1) space."""
    farthest = 0                        # indices 0..farthest are reachable
    i = 0
    while i <= farthest:                # i is a spot we can really stand on
        farthest = max(farthest, i + nums[i])
        if farthest >= len(nums) - 1:   # the reach covers the last index
            return True
        i += 1
    return False                        # walked past the reach: a wall


# --- try it ---
print(can_jump([2, 3, 1, 1, 4]))    # -> True
print(can_jump([3, 2, 1, 0, 4]))    # -> False
print(can_jump([0]))                # -> True
print(can_jump([2, 0, 0]))          # -> True
print(can_jump([1, 0, 1]))          # -> False
```

```{=latex}
\clearpage
```

## 68. Jump Game II {#a68}

```{=latex}
\markright{68. Jump Game II}
```

[Greedy BFS over Reach Levels · Greedy · Tier 2 · python/068\_jump\_game\_ii.py]{.meta}

nums\[i\] is the longest jump allowed from index i, and the last index is known to be reachable. Return the fewest jumps from index 0 to the last index: \[2, 3, 1, 1, 4\] → 2 (index 0 → 1 → 4).

```python
# --- algorithm ---
def min_jumps(nums):
    """BFS whose levels are intervals; count levels. O(n) time, O(1) space."""
    jumps = 0
    current_end = 0                 # right edge of the current level
    farthest = 0                    # right edge of the next level
    for i in range(len(nums) - 1):  # never jump from the last index
        farthest = max(farthest, i + nums[i])
        if i == current_end:        # this level is used up: jump again
            jumps += 1
            current_end = farthest  # the next level ends here
    return jumps


# --- try it ---
print(min_jumps([2, 3, 1, 1, 4]))   # -> 2
print(min_jumps([2, 3, 0, 1, 4]))   # -> 2
print(min_jumps([1, 1, 1, 1]))      # -> 3
print(min_jumps([0]))               # -> 0
```

```{=latex}
\clearpage
```

## 69. Gas Station {#a69}

```{=latex}
\markright{69. Gas Station}
```

[Restart After Every Deficit · Greedy · Tier 2 · python/069\_gas\_station.py]{.meta}

Station i on a circle gives gas\[i\] fuel; driving on to the next one burns cost\[i\]. Starting with an empty tank, return the station a full lap can start from (the input promises at most one), or -1: gas \[4, 1, 2, 5, 1\], cost \[3, 3, 3, 1, 2\] → 3.

```python
# --- algorithm ---
def can_complete_circuit(gas, cost):
    """Check the totals, then skip past every deficit. O(n) time, O(1) space."""
    if sum(gas) < sum(cost):        # not enough fuel for any lap
        return -1
    start = 0
    tank = 0                        # fuel left since leaving start
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                # stranded: start..i are all out
            start = i + 1
            tank = 0
    return start


# --- try it ---
print(can_complete_circuit([4, 1, 2, 5, 1], [3, 3, 3, 1, 2]))   # -> 3
print(can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))   # -> 3
print(can_complete_circuit([2, 3, 4], [3, 4, 3]))               # -> -1
print(can_complete_circuit([5], [4]))                           # -> 0
```

```{=latex}
\clearpage
```

## 70. Interval Scheduling {#a70}

```{=latex}
\markright{70. Interval Scheduling}
```

[Sort by End, Keep What Fits · Greedy · Tier 2 · python/070\_interval\_scheduling.py]{.meta}

Keep as many intervals \[start, end\] as possible with no two overlapping (ends that only touch, like \[1, 3\] and \[3, 5\], are fine); the fewest removals is the rest: \[\[1, 3\], \[2, 4\], \[3, 5\], \[1, 8\], \[6, 7\]\] → keep 3, remove 2.

```python
import math                         # math.inf


# --- algorithm ---
def max_non_overlapping(intervals):
    """Sort by end, keep whatever fits after the last kept end. O(n log n)."""
    by_end = []
    for start, end in intervals:
        by_end.append((end, start))     # end first: the sort orders by end
    by_end.sort()
    kept = 0
    last_end = -math.inf            # end of the last kept interval
    for end, start in by_end:
        if start >= last_end:       # fits after the last kept one
            kept += 1
            last_end = end
    return kept


def min_removals(intervals):
    """Remove everything the greedy did not keep (LC 435). O(n log n)."""
    return len(intervals) - max_non_overlapping(intervals)


# --- try it ---
intervals = [[1, 3], [2, 4], [3, 5], [1, 8], [6, 7]]
print(max_non_overlapping(intervals))           # -> 3
print(min_removals(intervals))                  # -> 2
print(min_removals([[1, 2], [1, 2], [1, 2]]))   # -> 2
print(max_non_overlapping([]))                  # -> 0
```

```{=latex}
\clearpage
```

## 71. Task Scheduler {#a71}

```{=latex}
\markright{71. Task Scheduler}
```

[Frame the Most Frequent Task · Greedy · Tier 2 · python/071\_task\_scheduler.py]{.meta}

Each task takes one unit of time, and two runs of the same task need at least n units between them; the CPU may idle. Return the fewest units for all tasks: \["A", "A", "A", "B", "B", "B"\], n = 2 → 8 (A B idle A B idle A B).

```python
# --- algorithm ---
def least_interval(tasks, n):
    """The most frequent task frames the schedule. O(len(tasks)) time."""
    counts = {}
    for task in tasks:
        counts[task] = counts.get(task, 0) + 1
    max_count = 0
    for task in counts:
        max_count = max(max_count, counts[task])
    tied = 0                        # tasks that also reach max_count
    for task in counts:
        if counts[task] == max_count:
            tied += 1
    frame = (max_count - 1) * (n + 1) + tied    # full rows, then a last row
    return max(frame, len(tasks))   # overflow: rows widen, no idles


# --- try it ---
print(least_interval(["A", "A", "A", "B", "B", "B"], 2))      # -> 8
print(least_interval(["A", "A", "A", "B", "B", "B"], 0))      # -> 6
print(least_interval(["A", "A", "A", "B", "B", "C"], 2))      # -> 7
overflow = ["A", "A", "A", "B", "B", "B", "C", "C", "D", "D"]
print(least_interval(overflow, 2))                            # -> 10
```

```{=latex}
\clearpage
```

## 72. Partition Labels {#a72}

```{=latex}
\markright{72. Partition Labels}
```

[Extend to the Last Occurrence · Greedy · Tier 2 · python/072\_partition\_labels.py]{.meta}

Cut a string into as many parts as possible so that each letter appears in at most one part, and return the part sizes in order: "ababcbacadefegdehijhklij" → \[9, 7, 8\].

```python
# --- algorithm ---
def partition_labels(s):
    """Record each letter's last index; cut where i meets part_end. O(n)."""
    last = {}                       # letter -> index of its last copy
    for i in range(len(s)):
        last[s[i]] = i
    sizes = []
    start = 0                       # first index of the current part
    part_end = 0                    # the part must reach at least here
    for i in range(len(s)):
        part_end = max(part_end, last[s[i]])    # this letter drags it along
        if i == part_end:           # nothing inside reaches past i: cut
            sizes.append(i - start + 1)
            start = i + 1
    return sizes


# --- try it ---
print(partition_labels("ababcbacadefegdehijhklij"))   # -> [9, 7, 8]
print(partition_labels("eccbbbbdec"))                 # -> [10]
print(partition_labels("abac"))                       # -> [3, 1]
print(partition_labels(""))                           # -> []
```

```{=latex}
\clearpage
```

## 73. Combination Sum {#a73}

```{=latex}
\markright{73. Combination Sum}
```

[Unlimited Reuse with a Start Index · Backtracking · Tier 2 · python/073\_combination\_sum.py]{.meta}

Given distinct positive integers and a target, return every combination of them that sums to the target; a number may be used any number of times, and order does not matter: \[2, 3, 6, 7\], target 7 → \[\[2, 2, 3\], \[7\]\].

```python
# --- algorithm ---
def backtrack(candidates, start, remaining, path, result):
    """Extend path from index start on, reusing i; break at an overshoot."""
    if remaining == 0:
        result.append(path.copy())      # exact hit: one combination
        return
    for i in range(start, len(candidates)):
        if candidates[i] > remaining:
            break                       # sorted: every later one is bigger
        path.append(candidates[i])      # choose
        # pass i, not i + 1: the same candidate may be chosen again
        backtrack(candidates, i, remaining - candidates[i], path, result)
        path.pop()                      # un-choose


def combination_sum(candidates, target):
    """Sort, then start-index backtracking that may reuse i. Exponential."""
    candidates = sorted(candidates)     # makes the break above valid
    result = []
    backtrack(candidates, 0, target, [], result)
    return result


# --- try it ---
print(combination_sum([2, 3, 6, 7], 7))   # -> [[2, 2, 3], [7]]
print(combination_sum([2, 3, 5], 8))      # -> [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
print(combination_sum([7, 3, 2], 7))      # -> [[2, 2, 3], [7]]
print(combination_sum([2], 1))            # -> []
```

```{=latex}
\clearpage
```

## 74. Word Search {#a74}

```{=latex}
\markright{74. Word Search}
```

[Grid Backtracking with In-Place Marks · Backtracking · Tier 2 · python/074\_word\_search.py]{.meta}

Given a grid of letters and a word, decide whether the word can be spelled by a path of horizontally or vertically adjacent cells, each used at most once: grid ABCE / SFCS / ADEE, word "ABCCED" → True.

```python
# --- algorithm ---
def dfs(board, word, row, col, k):
    """Can word[k:] be spelled from cell (row, col) on? Marks its own path."""
    if k == len(word):
        return True                     # every letter matched
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return False                    # off the grid
    if board[row][col] != word[k]:
        return False                    # wrong letter, or a '#' on the path
    board[row][col] = "#"               # mark: this cell is on the path
    found = False
    for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if dfs(board, word, row + d_row, col + d_col, k + 1):
            found = True
            break
    board[row][col] = word[k]           # unmark on the way back
    return found


def exist(board, word):
    """Try every cell as the first letter. O(m * n * 3^L) worst case."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if dfs(board, word, row, col, 0):
                return True
    return False


# --- try it ---
board = [list("ABCE"), list("SFCS"), list("ADEE")]   # rows of letters
print(exist(board, "ABCCED"))   # -> True
print(exist(board, "SEE"))      # -> True
print(exist(board, "ABCB"))     # -> False
print(board[0])                 # -> ['A', 'B', 'C', 'E']
```

```{=latex}
\clearpage
```

## 75. Construct Binary Tree from Preorder and Inorder {#a75}

```{=latex}
\markright{75. Construct Binary Tree from Preorder and Inorder}
```

[Preorder Picks the Root, Inorder Splits the Rest · Trees · Tier 2 · python/075\_construct\_tree\_preorder\_inorder.py]{.meta}

Given the preorder and inorder traversals of a binary tree whose values are all different, rebuild the tree: preorder \[3, 9, 20, 15, 7\] and inorder \[9, 3, 15, 20, 7\] → \[3, 9, 20, None, None, 15, 7\] in level order.

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
# standard helpers TreeNode, tree_to_list: printed once under Standard Helpers


# --- algorithm ---
def construct_tree(preorder, inorder):
    """Map each value to its inorder index, then build the whole range.
    O(n) time and space."""
    position = {}                           # value -> index in inorder
    for i in range(len(inorder)):
        position[inorder[i]] = i
    pre_index = [0]                         # one box every call shares
    return build(preorder, position, pre_index, 0, len(inorder) - 1)


def build(preorder, position, pre_index, lo, hi):
    """Build the subtree holding inorder[lo..hi]; the next preorder value is
    its root."""
    if lo > hi:
        return None                         # empty range: no subtree here
    value = preorder[pre_index[0]]          # roots come in preorder
    pre_index[0] += 1
    root = TreeNode(value)
    mid = position[value]                   # the root splits inorder[lo..hi]
    root.left = build(preorder, position, pre_index, lo, mid - 1)
    root.right = build(preorder, position, pre_index, mid + 1, hi)
    return root


# --- try it ---
root = construct_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
print(tree_to_list(root))                   # -> [3, 9, 20, None, None, 15, 7]
root = construct_tree([1, 2, 4, 5, 3, 6], [4, 2, 5, 1, 6, 3])
print(tree_to_list(root))                   # -> [1, 2, 3, 4, 5, 6]
print(tree_to_list(construct_tree([1, 2], [2, 1])))     # -> [1, 2]
print(tree_to_list(construct_tree([1, 2], [1, 2])))     # -> [1, None, 2]
print(tree_to_list(construct_tree([], [])))             # -> []
```

```{=latex}
\clearpage
```

## 76. BST Search, Insert, Delete {#a76}

```{=latex}
\markright{76. BST Search, Insert, Delete}
```

[Delete with the In-Order Successor · BST · Tier 2 · python/076\_bst\_operations.py]{.meta}

Search, insert and delete values in a binary search tree while keeping its order (smaller to the left, larger to the right). Deleting 3 from \[5, 3, 6, 2, 4, None, 7\] → \[5, 4, 6, 2, None, None, 7\].

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
# standard helpers TreeNode, build_tree, tree_to_list: printed once under Standard Helpers


# --- algorithm ---
def search(root, val):
    """Walk down one path: left if smaller, right if larger. O(h)."""
    node = root
    while node is not None and node.val != val:
        if val < node.val:
            node = node.left
        else:
            node = node.right
    return node                             # the node holding val, or None


def insert(root, val):
    """Descend to the empty spot where val belongs; hang a leaf there. O(h)."""
    if root is None:
        return TreeNode(val)                # the empty spot: a new leaf
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root                             # equal: already present


def delete(root, val):
    """Remove val; a node with two children takes its successor. O(h)."""
    if root is None:
        return None                         # val is not in the tree
    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:
        if root.left is None:               # leaf, or right child only
            return root.right
        if root.right is None:              # left child only
            return root.left
        successor = root.right              # two children: leftmost node
        while successor.left is not None:   # of the right subtree
            successor = successor.left
        root.val = successor.val            # copy it up...
        root.right = delete(root.right, successor.val)  # ...and remove it
    return root


# --- try it ---
root = build_tree([5, 3, 6, 2, 4, None, 7])
print(tree_to_list(search(root, 3)))        # -> [3, 2, 4]
root = delete(root, 3)
print(tree_to_list(root))                   # -> [5, 4, 6, 2, None, None, 7]
print(search(root, 3))                      # -> None
root = insert(root, 1)
print(tree_to_list(root))                   # -> [5, 4, 6, 2, None, None, 7, 1]
```

```{=latex}
\clearpage
```

## 77. BST Iterator {#a77}

```{=latex}
\markright{77. BST Iterator}
```

[Controlled In-Order with a Stack · BST · Tier 2 · python/077\_bst\_iterator.py]{.meta}

Design an iterator over a binary search tree: next() returns the next smallest value and has\_next() says whether any are left. Five calls to next() on \[7, 3, 15, None, None, 9, 20\] → 3, 7, 9, 15, 20.

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
# standard helpers TreeNode, build_tree: printed once under Standard Helpers


# --- algorithm ---
class BSTIterator:
    """In-order iterator: the stack holds the nodes still waiting their turn."""

    def __init__(self, root):
        self.stack = []
        self.push_left(root)

    def push_left(self, node):
        """Push node and its left children; the smallest lands on top."""
        while node is not None:             # walk down the left spine
            self.stack.append(node)
            node = node.left

    def next(self):
        """Pop the smallest waiting node, then push the left spine of its
        right child. O(1) amortized, O(h) worst case."""
        node = self.stack.pop()             # the smallest value still waiting
        self.push_left(node.right)          # its successors live on the right
        return node.val

    def has_next(self):
        """True while some node is still waiting on the stack. O(1)."""
        return len(self.stack) > 0


def kth_smallest(root, k):
    """Call next() k times; the last value returned is the answer. O(h + k)."""
    iterator = BSTIterator(root)
    value = None
    for i in range(k):
        value = iterator.next()
    return value


# --- try it ---
iterator = BSTIterator(build_tree([7, 3, 15, None, None, 9, 20]))
print(iterator.next(), iterator.next(), iterator.has_next())   # -> 3 7 True
print(iterator.next(), iterator.next(), iterator.next())       # -> 9 15 20
print(iterator.has_next())                                     # -> False
root = build_tree([5, 3, 6, 2, 4, None, None, 1])
print(kth_smallest(root, 3))                                   # -> 3
```

```{=latex}
\clearpage
```

## 78. Multi-Source BFS {#a78}

```{=latex}
\markright{78. Multi-Source BFS}
```

[Rotting Oranges · BFS · Tier 2 · python/078\_multi\_source\_bfs.py]{.meta}

In a grid, 0 is empty, 1 is a fresh orange and 2 a rotten one. Every minute, each fresh orange next to a rotten one (up, down, left, right) rots. Return the minutes until no fresh orange is left, or -1 if one never rots: \[\[2, 1, 1, 1\], \[1, 0, 1, 1\], \[1, 1, 1, 2\]\] → 2.

```python
from collections import deque      # popleft is O(1)


# --- algorithm ---
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def oranges_rotting(grid):
    """BFS from every rotten orange at once; one layer per minute. O(R * C)."""
    rows = len(grid)
    cols = len(grid[0])
    queue = deque()
    fresh = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 2:
                queue.append((row, col))    # every source starts at minute 0
            elif grid[row][col] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh > 0:
        for _ in range(len(queue)):         # exactly the oranges of this layer
            row, col = queue.popleft()
            for d_row, d_col in DIRECTIONS:
                next_row = row + d_row
                next_col = col + d_col
                inside = 0 <= next_row < rows and 0 <= next_col < cols
                if inside and grid[next_row][next_col] == 1:
                    grid[next_row][next_col] = 2    # rot it now: enqueued once
                    fresh -= 1
                    queue.append((next_row, next_col))
        minutes += 1
    if fresh > 0:
        return -1                           # walled off from every rotten one
    return minutes


# --- try it ---
print(oranges_rotting([[2, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 2]]))  # -> 2
print(oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))           # -> 4
print(oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))           # -> -1
print(oranges_rotting([[0, 2]]))                                    # -> 0
```

```{=latex}
\clearpage
```

## 79. Word Ladder {#a79}

```{=latex}
\markright{79. Word Ladder}
```

[BFS on an Implicit Graph · BFS · Tier 2 · python/079\_word\_ladder.py]{.meta}

Turn begin\_word into end\_word one letter at a time, every word after the first taken from word\_list. Return the number of words in the shortest such ladder, or 0 if there is none: "hit" to "cog" with \["hot", "dot", "dog", "lot", "log", "cog"\] → 5.

```python
from collections import deque      # popleft is O(1)


# --- algorithm ---
def ladder_length(begin_word, end_word, word_list):
    """BFS over words; neighbors differ in one letter. O(n * 26 * L^2)."""
    unvisited = set(word_list)          # dictionary words not reached yet
    if end_word not in unvisited:
        return 0
    if begin_word in unvisited:
        unvisited.remove(begin_word)    # the start counts as reached
    queue = deque([(begin_word, 1)])    # (word, words in the ladder so far)
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        for i in range(len(word)):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                candidate = word[:i] + letter + word[i + 1:]
                if candidate in unvisited:          # a word not reached yet
                    unvisited.remove(candidate)     # mark when enqueued
                    queue.append((candidate, length + 1))
    return 0


# --- try it ---
words = ["hot", "dot", "dog", "lot", "log", "cog"]
print(ladder_length("hit", "cog", words))                       # -> 5
print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot"]))  # -> 0
print(ladder_length("a", "c", ["a", "b", "c"]))                 # -> 2
```

```{=latex}
\clearpage
```

## 80. Clone Graph {#a80}

```{=latex}
\markright{80. Clone Graph}
```

[The Old-to-New Map Doubles as Visited · Graphs · Tier 2 · python/080\_clone\_graph.py]{.meta}

Given one node of a connected undirected graph, where every node has a value and a list of neighbors, return a deep copy of the whole graph. Row i of the adjacency list holds the neighbors of node i + 1: \[\[2, 4\], \[1, 3\], \[2, 4\], \[1, 3\]\] → the same list, built from all-new nodes.

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []


def build_graph(adjacency):
    """Make node i + 1 for row i, link the listed neighbors, return node 1."""
    if not adjacency:
        return None
    nodes = []
    for i in range(len(adjacency)):
        nodes.append(Node(i + 1))
    for i in range(len(adjacency)):
        for value in adjacency[i]:
            nodes[i].neighbors.append(nodes[value - 1])
    return nodes[0]


def collect_nodes(node):
    """Every node reachable from node, in BFS order. O(V + E)."""
    if node is None:
        return []
    seen = set()
    seen.add(node)
    order = [node]
    queue = deque([node])
    while queue:
        current = queue.popleft()
        for neighbor in current.neighbors:
            if neighbor not in seen:
                seen.add(neighbor)
                order.append(neighbor)
                queue.append(neighbor)
    return order


def graph_to_list(node):
    """Adjacency list of the graph: row i lists node i + 1's neighbors."""
    nodes = collect_nodes(node)
    rows = []
    for i in range(len(nodes)):
        rows.append([])
    for current in nodes:
        for neighbor in current.neighbors:
            rows[current.val - 1].append(neighbor.val)
    return rows


def shares_a_node(first, second):
    """True if the two graphs have any node object in common."""
    originals = set(collect_nodes(first))
    for node in collect_nodes(second):
        if node in originals:
            return True
    return False


# --- algorithm ---
def clone_graph(node):
    """BFS; the map old -> copy makes each copy once and is the visited set.
    O(V + E) time, O(V) extra space."""
    if node is None:
        return None
    copies = {}                             # old node -> its copy
    copies[node] = Node(node.val)
    queue = deque([node])
    while queue:
        current = queue.popleft()
        for neighbor in current.neighbors:
            if neighbor not in copies:      # first sighting: copy, visit later
                copies[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            copies[current].neighbors.append(copies[neighbor])  # copy to copy
    return copies[node]


# --- try it ---
original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
clone = clone_graph(original)
print(graph_to_list(clone))                # -> [[2, 4], [1, 3], [2, 4], [1, 3]]
print(shares_a_node(original, clone))      # -> False
path = build_graph([[2], [1, 3], [2]])
print(graph_to_list(clone_graph(path)))    # -> [[2], [1, 3], [2]]
print(graph_to_list(clone_graph(build_graph([[]]))))    # -> [[]]
print(clone_graph(None))                   # -> None
```

```{=latex}
\clearpage
```

## 81. Cycle Detection in a Directed Graph {#a81}

```{=latex}
\markright{81. Cycle Detection in a Directed Graph}
```

[Three Colors: White, Gray, Black · Cycle Detection · Tier 2 · python/081\_directed\_cycle\_detection.py]{.meta}

Given n nodes 0..n-1 and directed edges \[u, v\] meaning u → v, report whether some path follows the arrows back to where it started: n = 5, \[\[0, 1\], \[0, 2\], \[1, 3\], \[2, 3\], \[2, 4\], \[4, 0\]\] → True.

```python
# --- algorithm ---
WHITE = 0                           # not visited yet
GRAY = 1                            # on the current DFS path
BLACK = 2                           # finished: no cycle is reachable from it


def has_cycle(n, edges):
    """DFS from every white node; an edge into a gray node closes a cycle.
    O(V + E) time."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
    color = [WHITE] * n
    for node in range(n):
        if color[node] == WHITE and dfs(graph, node, color):
            return True
    return False


def dfs(graph, node, color):
    """True if a cycle is reachable from node; paints node black otherwise.
    O(V + E) over all calls."""
    color[node] = GRAY                  # node joins the current path
    for neighbor in graph[node]:
        if color[neighbor] == GRAY:
            return True                 # back edge to a node on the path
        if color[neighbor] == WHITE and dfs(graph, neighbor, color):
            return True
    color[node] = BLACK                 # every path out of node is cycle-free
    return False


# --- try it ---
edges = [[0, 1], [0, 2], [1, 3], [2, 3], [2, 4], [4, 0]]
print(has_cycle(5, edges))                              # -> True
print(has_cycle(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))   # -> False
print(has_cycle(2, [[1, 1]]))                           # -> True
print(has_cycle(3, []))                                 # -> False
```

```{=latex}
\clearpage
```

## 82. Topological Sort with DFS {#a82}

```{=latex}
\markright{82. Topological Sort with DFS}
```

[Reverse Postorder · Topological Sort · Tier 2 · python/082\_dfs\_topological\_sort.py]{.meta}

Given n nodes 0..n-1 and directed edges \[u, v\] meaning u must come before v, return an order of all the nodes that respects every edge, or \[\] if a cycle makes that impossible: n = 6, \[\[0, 3\], \[1, 3\], \[3, 4\], \[3, 2\], \[4, 5\], \[2, 5\]\] → \[1, 0, 3, 2, 4, 5\].

```python
# --- algorithm ---
WHITE = 0                           # not visited yet
GRAY = 1                            # on the current DFS path
BLACK = 2                           # finished: placed after its descendants


def topological_sort(n, edges):
    """List nodes as they finish in a DFS, then reverse; [] on a cycle.
    O(V + E) time."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
    color = [WHITE] * n
    finished = []                       # nodes in the order they finish
    for node in range(n):
        if color[node] == WHITE and not dfs(graph, node, color, finished):
            return []                   # a cycle: no order exists
    return finished[::-1]


def dfs(graph, node, color, finished):
    """Finish node after everything it points to; False if a cycle is found.
    O(V + E) over all calls."""
    color[node] = GRAY                  # node joins the current path
    for neighbor in graph[node]:
        if color[neighbor] == GRAY:
            return False                # back edge: a cycle
        if color[neighbor] == WHITE:
            if not dfs(graph, neighbor, color, finished):
                return False
    color[node] = BLACK
    finished.append(node)               # its descendants are all in already
    return True


# --- try it ---
edges = [[0, 3], [1, 3], [3, 4], [3, 2], [4, 5], [2, 5]]
print(topological_sort(6, edges))                       # -> [1, 0, 3, 2, 4, 5]
print(topological_sort(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))  # -> [0, 2, 1, 3]
print(topological_sort(3, [[0, 1], [1, 2], [2, 0]]))    # -> []
print(topological_sort(2, []))                          # -> [1, 0]
```

```{=latex}
\clearpage
```

## 83. Alien Dictionary {#a83}

```{=latex}
\markright{83. Alien Dictionary}
```

[Letter Edges from Adjacent Words, Then Topological Sort · Topological Sort · Tier 2 · python/083\_alien\_dictionary.py]{.meta}

A list of words is sorted in an unknown alphabet. Return the letters that appear in an order that sorts the list, or '' if no alphabet can: \["wrt", "wrf", "er", "ett", "rftt"\] → "wertf".

```python
from collections import deque      # popleft is O(1)


# --- algorithm ---
def alien_order(words):
    """Collect the letters, add one edge per adjacent pair of words, then
    sort the letters topologically. O(C) time for C letters in all."""
    graph = {}                          # letter -> letters that come after it
    indegree = {}                       # letter -> letters still before it
    for word in words:
        for letter in word:
            if letter not in graph:
                graph[letter] = []
                indegree[letter] = 0
    for i in range(len(words) - 1):
        if not add_edge(words[i], words[i + 1], graph, indegree):
            return ""                   # a word came before its own prefix
    return topological_order(graph, indegree)


def add_edge(first, second, graph, indegree):
    """The first letters that differ give the edge before -> after; False
    if second is a proper prefix of first, which no alphabet allows."""
    for j in range(min(len(first), len(second))):
        before = first[j]
        after = second[j]
        if before != after:
            if after not in graph[before]:  # count each edge once
                graph[before].append(after)
                indegree[after] += 1
            return True                 # later letters say nothing
    return len(first) <= len(second)    # "abc" before "ab" is impossible


def topological_order(graph, indegree):
    """Kahn's algorithm: place a letter once nothing must come before it.
    O(V + E); '' if a cycle leaves letters unplaced."""
    queue = deque()
    for letter in sorted(indegree):     # sorted start: a repeatable answer
        if indegree[letter] == 0:
            queue.append(letter)
    order = []
    while queue:
        letter = queue.popleft()
        order.append(letter)
        for after in graph[letter]:
            indegree[after] -= 1        # one fewer before it
            if indegree[after] == 0:
                queue.append(after)
    if len(order) < len(indegree):
        return ""                       # the rest sit on a cycle
    return "".join(order)


# --- try it ---
print(repr(alien_order(["wrt", "wrf", "er", "ett", "rftt"])))   # -> 'wertf'
print(repr(alien_order(["ab", "ac", "d"])))         # -> 'abdc'
print(repr(alien_order(["z", "x", "z"])))           # -> ''
print(repr(alien_order(["abc", "ab"])))             # -> ''
print(repr(alien_order(["z", "z"])))                # -> 'z'
```

```{=latex}
\clearpage
```

## 84. Connected Components {#a84}

```{=latex}
\markright{84. Connected Components}
```

[Count and Label by Flood Fill · Connected Components · Tier 2 · python/084\_connected\_components.py]{.meta}

Given n nodes 0..n-1 and an undirected edge list, count the connected components and label every node with the number of its component: n = 7, \[\[0, 1\], \[1, 2\], \[3, 4\], \[3, 5\]\] → (3, \[0, 0, 0, 1, 1, 1, 2\]).

```python
# --- algorithm ---
def connected_components(n, edges):
    """Each unlabeled node floods its whole component with a new label.
    O(V + E) time."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)              # undirected: store both directions
        graph[v].append(u)
    label = [-1] * n                    # -1 means not reached yet
    count = 0
    for start in range(n):
        if label[start] == -1:          # not reached by any earlier flood
            flood(graph, start, count, label)
            count += 1
    return count, label


def flood(graph, start, mark, label):
    """Paint every node reachable from start with mark, using a stack.
    O(nodes + edges) of that component."""
    label[start] = mark
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if label[neighbor] == -1:
                label[neighbor] = mark  # label when pushed: pushed only once
                stack.append(neighbor)


# --- try it ---
edges = [[0, 1], [1, 2], [3, 4], [3, 5]]
print(connected_components(7, edges))       # -> (3, [0, 0, 0, 1, 1, 1, 2])
print(connected_components(3, []))          # -> (3, [0, 1, 2])
chain = [[3, 2], [1, 0], [2, 1]]
print(connected_components(4, chain))       # -> (1, [0, 0, 0, 0])
```

```{=latex}
\clearpage
```

## 85. Word Search II {#a85}

```{=latex}
\markright{85. Word Search II}
```

[Trie-Guided Grid Backtracking · Tries · Tier 2 · python/085\_word\_search\_ii.py]{.meta}

Given a grid of letters and a list of words, return every word that can be spelled along a path of adjacent cells (up, down, left, right), each cell used at most once per word: grid oaan / etae / ihkr / iflv with words oath, pea, eat, rain → \['oath', 'eat'\] (any order).

```python
# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}              # letter -> TrieNode
        self.word = None                # the whole word, at its last node


# --- algorithm ---
def build_trie(words):
    """Insert every word; its last node keeps the word. O(total letters)."""
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = word
    return root


def dfs(board, row, col, parent, found):
    """Step onto (row, col) only if the trie goes on with its letter."""
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return
    ch = board[row][col]
    if ch not in parent.children:
        return                          # no word goes this way (or a '#')
    node = parent.children[ch]
    if node.word is not None:
        found.append(node.word)
        node.word = None                # record each word only once
    board[row][col] = "#"               # mark: on the current path
    for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(board, row + d_row, col + d_col, node, found)
    board[row][col] = ch                # unmark on the way back
    if len(node.children) == 0:
        del parent.children[ch]         # prune: no word is left below


def find_words(board, words):
    """One trie, one DFS from every cell. O(m * n * 3^L), L the longest."""
    root = build_trie(words)
    found = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            dfs(board, row, col, root, found)
    return found


# --- try it ---
board = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
print(find_words(board, ["oath", "pea", "eat", "rain"]))  # -> ['oath', 'eat']
print(find_words(board, ["oat", "oath", "eath"]))  # -> ['oat', 'oath', 'eath']
print(find_words([list("ab")], ["ab", "ba", "aba"]))      # -> ['ab', 'ba']
print(find_words([list("ab"), list("cd")], ["abcb"]))     # -> []
```

```{=latex}
\clearpage
```

## 86. KMP String Matching {#a86}

```{=latex}
\markright{86. KMP String Matching}
```

[The Prefix Function Never Re-Reads the Text · Strings · Tier 2 · python/086\_kmp.py]{.meta}

Return every index where the pattern starts in the text, overlapping matches included: text "abababc", pattern "ababc" → \[2\].

```python
# --- algorithm ---
def build_lps(pattern):
    """lps[i] = length of the longest proper prefix of pattern[0..i] that is
    also its suffix; the search loop run on the pattern itself. O(m)."""
    lps = [0] * len(pattern)
    j = 0                               # length of the border being extended
    for i in range(1, len(pattern)):    # lps[0] = 0: a proper prefix is shorter
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]              # fall back to the next shorter border
        if pattern[i] == pattern[j]:
            j += 1
        lps[i] = j
    return lps


def kmp_search(text, pattern):
    """i never moves back; a mismatch slides the pattern by lps. O(n + m)."""
    if len(pattern) == 0:
        return []
    lps = build_lps(pattern)
    matches = []
    j = 0                               # pattern characters matched so far
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]              # slide the pattern; text[i] is retried
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)   # the match ends at i
            j = lps[j - 1]              # keep the border: overlaps are found
    return matches


# --- try it ---
print(build_lps("ababc"))               # -> [0, 0, 1, 2, 0]
print(kmp_search("abababc", "ababc"))   # -> [2]
print(build_lps("aabaaab"))             # -> [0, 1, 0, 1, 2, 2, 3]
print(kmp_search("aaaaa", "aa"))        # -> [0, 1, 2, 3]
print(kmp_search("abc", "abd"))         # -> []
```

```{=latex}
\clearpage
```

## 87. Longest Palindromic Substring {#a87}

```{=latex}
\markright{87. Longest Palindromic Substring}
```

[Expand Around Every Center · Strings · Tier 2 · python/087\_longest\_palindromic\_substring.py]{.meta}

Return the longest contiguous substring that reads the same forwards and backwards (the leftmost one on a tie): "babad" → "bab".

```python
# --- algorithm ---
def longest_palindrome(s):
    """Expand around all 2n - 1 centers (n chars, n - 1 gaps); keep the
    longest. O(n^2) time, O(1) space."""
    best_start = 0
    best_len = 0
    for center in range(2 * len(s) - 1):
        left = center // 2
        right = left + center % 2       # even center: a char; odd: a gap
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1                   # ends match: grow one step each way
            right += 1
        length = right - left - 1       # the loop stepped one past each end
        if length > best_len:           # strictly longer: ties keep the first
            best_start = left + 1
            best_len = length
    return s[best_start:best_start + best_len]


# --- try it ---
print(longest_palindrome("babad"))          # -> bab
print(longest_palindrome("cbbd"))           # -> bb
print(longest_palindrome("abacdfgdcaba"))   # -> aba
print(longest_palindrome("a"))              # -> a
```

```{=latex}
\clearpage
```

## 88. Encode and Decode Strings {#a88}

```{=latex}
\markright{88. Encode and Decode Strings}
```

[Length-Prefix Framing · Strings · Tier 2 · python/088\_encode\_decode\_strings.py]{.meta}

Pack a list of strings into one string and unpack it back to the same list; the strings may contain any character, '\#' and digits included: \["ab\#", "12", ""\] → "3\#ab\#2\#120\#" → \["ab\#", "12", ""\].

```python
# --- algorithm ---
def encode(strs):
    """Prefix each string with its length and a '#'. O(total length)."""
    parts = []
    for s in strs:
        parts.append(str(len(s)) + "#" + s)
    return "".join(parts)               # join once; += in a loop may recopy


def decode(data):
    """Read digits up to '#', then take exactly that many characters.
    O(total length)."""
    strs = []
    i = 0
    while i < len(data):
        j = i
        while data[j] != "#":           # the length ends at the first '#'
            j += 1
        length = int(data[i:j])
        strs.append(data[j + 1:j + 1 + length])
        i = j + 1 + length              # jump over the payload unread
    return strs


# --- try it ---
print(encode(["ab#", "12", ""]))                  # -> 3#ab#2#120#
print(decode("3#ab#2#120#"))                      # -> ['ab#', '12', '']
print(decode(encode(["hello world", "#4#"])))     # -> ['hello world', '#4#']
print(decode(encode([])), decode(encode([""])))   # -> [] ['']
```

```{=latex}
\clearpage
```

## 89. Game of Life {#a89}

```{=latex}
\markright{89. Game of Life}
```

[Update in Place with Two-Bit States · Matrix · Tier 2 · python/089\_game\_of\_life.py]{.meta}

Each cell is live (1) or dead (0). Live cells with 2 or 3 live neighbors (of 8) survive, dead cells with exactly 3 come alive, all other cells are dead next. Update the board in place: \[\[0, 1, 0\], \[0, 0, 1\], \[1, 1, 1\], \[0, 0, 0\]\] → \[\[0, 0, 0\], \[1, 0, 1\], \[0, 1, 1\], \[0, 1, 0\]\].

```python
# --- algorithm ---
def count_live_neighbors(board, row, col):
    """Live cells in the 3 x 3 block around (row, col), clipped at the edges,
    reading bit 0 only, which still holds the current state. O(1)."""
    live = 0
    for near_row in range(max(0, row - 1), min(len(board), row + 2)):
        for near_col in range(max(0, col - 1), min(len(board[0]), col + 2)):
            if near_row == row and near_col == col:
                continue            # a cell is not its own neighbor
            live += board[near_row][near_col] & 1   # bit 0: current state
    return live


def game_of_life(board):
    """Pass 1 writes each next state into bit 1, pass 2 shifts it down to
    bit 0. O(m n) time, O(1) extra space."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            live = count_live_neighbors(board, row, col)
            alive = board[row][col] & 1
            if live == 3 or (alive == 1 and live == 2):
                board[row][col] = board[row][col] | 2   # bit 1: live next
    for row in range(len(board)):
        for col in range(len(board[0])):
            board[row][col] = board[row][col] >> 1      # keep only the next


# --- try it ---
board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
game_of_life(board)
print(board)        # -> [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
blinker = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
game_of_life(blinker)
print(blinker)      # -> [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
block = [[1, 1], [1, 1]]
game_of_life(block)
print(block)        # -> [[1, 1], [1, 1]]
```

```{=latex}
\clearpage
```

## 90. Fibonacci {#a90}

```{=latex}
\markright{90. Fibonacci}
```

[Recursion, Memo, Iteration, Fast Doubling · Math · Tier 2 · python/090\_fibonacci.py]{.meta}

F(0) = 0, F(1) = 1, and every later term is the sum of the two before it: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55. Compute F(n): n = 10 → 55.

```python
# --- algorithm ---
def fib_naive(n):
    """Two calls per call: 2F(n + 1) - 1 calls, growing like 1.618^n."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, memo):
    """The same recursion, but each F(k) is solved once. O(n) time and space."""
    if n < 2:
        return n
    if n in memo:
        return memo[n]                  # solved before: skip the whole subtree
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_iter(n):
    """Slide a window of two neighbors n steps. O(n) time, O(1) space."""
    prev = 0
    curr = 1
    for i in range(n):                  # prev = F(i), curr = F(i + 1)
        nxt = prev + curr
        prev = curr
        curr = nxt
    return prev


def fib_pair(n):
    """Return (F(n), F(n + 1)) from the pair at n // 2. O(log n) calls."""
    if n == 0:
        return (0, 1)
    a, b = fib_pair(n // 2)             # a = F(k), b = F(k + 1) with k = n // 2
    even = a * (2 * b - a)              # F(2k)
    odd = a * a + b * b                 # F(2k + 1)
    if n % 2 == 0:
        return (even, odd)
    return (odd, even + odd)            # n = 2k + 1: one step further


def fib_fast(n):
    """Fast doubling: F(n) is the first value of the pair. O(log n) steps."""
    pair = fib_pair(n)
    return pair[0]


# --- try it ---
print(fib_naive(10))                    # -> 55
print(fib_memo(50, {}))                 # -> 12586269025
print(fib_iter(90))                     # -> 2880067194370816120
print(fib_fast(100))                    # -> 354224848179261915075
```

```{=latex}
\clearpage
```

## 91. Insert Delete GetRandom O(1) {#a91}

```{=latex}
\markright{91. Insert Delete GetRandom O(1)}
```

[Array + Index Map, Swap with Last · Design · Tier 2 · python/091\_randomized\_set.py]{.meta}

Design a set with insert, remove and get\_random in average O(1) time each, where get\_random returns every stored value with equal probability: insert 10, 20, 30, then remove 10 → values \[30, 20\].

```python
import random                       # randint(a, b) is uniform on a..b inclusive


# --- algorithm ---
class RandomizedSet:
    """Packed list for random picks, map value -> index for lookups. O(1)."""

    def __init__(self):
        self.values = []            # packed from index 0, no holes
        self.index_of = {}          # value -> its slot in values

    def insert(self, val):
        """Append at the end and remember the slot. O(1)."""
        if val in self.index_of:
            return False
        self.index_of[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val):
        """Move the last value into val's slot, then pop the end. O(1)."""
        if val not in self.index_of:
            return False
        i = self.index_of[val]
        last = self.values[-1]
        self.values[i] = last       # the last value fills the hole
        self.index_of[last] = i     # and learns its new slot
        self.values.pop()           # drop the tail slot
        del self.index_of[val]      # only now: last may be val
        return True

    def get_random(self):
        """Pick a uniform random slot of the packed list. O(1)."""
        i = random.randint(0, len(self.values) - 1)
        return self.values[i]


# --- try it ---
s = RandomizedSet()
s.insert(10)
s.insert(20)
s.insert(30)
print(s.insert(20), s.remove(10), s.remove(10))   # -> False True False
print(s.values, s.index_of)                       # -> [30, 20] {20: 1, 30: 0}
print(s.get_random() in (20, 30))                 # -> True
print(s.remove(20), s.values, s.index_of)         # -> True [30] {30: 0}
```

```{=latex}
\clearpage
```

## 92. Time-Based Key-Value Store {#a92}

```{=latex}
\markright{92. Time-Based Key-Value Store}
```

[Per-Key Timestamp Lists + Binary Search · Design · Tier 2 · python/092\_time\_based\_kv\_store.py]{.meta}

Keep every version of a key: set(key, value, t) records value at time t (the times of each key only grow), and get(key, t) returns the value set at the largest time \<= t, or "" if none: set status = draft at 1, review at 4, live at 9; get status at 5 → "review".

```python
# --- algorithm ---
class TimeMap:
    """Per key, parallel lists of times and values. set O(1), get O(log n)."""

    def __init__(self):
        self.times = {}             # key -> increasing list of set times
        self.values = {}            # key -> the values, in the same order

    def set(self, key, value, timestamp):
        """Append the version to both lists of the key. O(1) amortized."""
        if key not in self.times:
            self.times[key] = []
            self.values[key] = []
        self.times[key].append(timestamp)   # times only grow: stays sorted
        self.values[key].append(value)

    def get(self, key, timestamp):
        """First time > timestamp, minus one: the last time <= it. O(log n)."""
        if key not in self.times:
            return ""
        times = self.times[key]
        left = 0
        right = len(times)
        while left < right:             # find the first time > timestamp
            mid = (left + right) // 2
            if times[mid] <= timestamp:
                left = mid + 1          # mid is not after timestamp
            else:
                right = mid             # mid is after: maybe the first
        if left == 0:
            return ""                   # every version is newer
        return self.values[key][left - 1]


# --- try it ---
store = TimeMap()
store.set("status", "draft", 1)
store.set("status", "review", 4)
store.set("status", "live", 9)
print(store.get("status", 5), store.get("status", 9))    # -> review live
print(store.get("status", 4), store.get("status", 100))  # -> review live
print(repr(store.get("status", 0)), repr(store.get("owner", 5)))   # -> '' ''
```

```{=latex}
\clearpage
```

## 93. LFU Cache {#a93}

```{=latex}
\markright{93. LFU Cache}
```

[Frequency Buckets That Keep LRU Order · Design · Tier 2 · python/093\_lfu\_cache.py]{.meta}

Design a cache of fixed capacity whose get(key) and put(key, value) run in O(1); when full, it evicts the least frequently used key, the least recent on a tie. Capacity 2: put(1, 10), get(1), put(2, 20), put(3, 30), get(2) → -1.

```python
# --- helpers ---
class Node:
    def __init__(self, key, value):
        self.key = key              # kept so eviction can clean the map
        self.value = value
        self.freq = 1               # how many times the key was used
        self.prev = None
        self.next = None


# --- algorithm ---
class Bucket:
    """The keys used freq times, newest after head, oldest before tail."""

    def __init__(self):
        self.head = Node(0, 0)      # sentinel: head.next is the newest
        self.tail = Node(0, 0)      # sentinel: tail.prev is the oldest
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_front(self, node):
        """Splice node in right after head, the newest spot. O(1)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node):
        """Unlink node: its two neighbors point past it. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def is_empty(self):
        """True when only the two sentinels are left. O(1)."""
        return self.head.next is self.tail


class LFUCache:
    """Map key -> node, map freq -> bucket, and the smallest freq in use.
    get and put O(1)."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}             # key -> node
        self.buckets = {}           # freq -> bucket of the keys used freq times
        self.min_freq = 0           # the smallest freq that has a key

    def add(self, node):
        """Put node at the front of the bucket for its freq. O(1)."""
        if node.freq not in self.buckets:
            self.buckets[node.freq] = Bucket()
        self.buckets[node.freq].add_front(node)

    def touch(self, node):
        """One more use: move node from bucket f to bucket f + 1. O(1)."""
        bucket = self.buckets[node.freq]
        bucket.remove(node)
        if bucket.is_empty():
            del self.buckets[node.freq]
            if self.min_freq == node.freq:
                self.min_freq += 1      # node moves up to it
        node.freq += 1
        self.add(node)

    def get(self, key):
        """Return the value and count the use; -1 if absent. O(1)."""
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self.touch(node)
        return node.value

    def put(self, key, value):
        """Update and count a use, or evict when full, add at freq 1. O(1)."""
        if self.capacity == 0:
            return
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self.touch(node)
            return
        if len(self.nodes) == self.capacity:
            self.evict()                # before the new key is added
        node = Node(key, value)
        self.nodes[key] = node
        self.add(node)
        self.min_freq = 1               # a new key is the least used

    def evict(self):
        """Drop the oldest node of the least used bucket. O(1)."""
        bucket = self.buckets[self.min_freq]
        victim = bucket.tail.prev       # least used, then least recent
        bucket.remove(victim)
        if bucket.is_empty():
            del self.buckets[self.min_freq]
        del self.nodes[victim.key]


# --- try it ---
cache = LFUCache(2)
cache.put(1, 10)
print(cache.get(1))                 # -> 10
cache.put(2, 20)
cache.put(3, 30)                    # evicts 2: used once, key 1 twice
print(cache.get(2), cache.get(3))   # -> -1 30
cache.put(4, 40)                    # 1 and 3 tie at 2 uses: evicts 1, older
print(cache.get(1), cache.get(3), cache.get(4))     # -> -1 30 40
empty = LFUCache(0)
empty.put(1, 10)
print(empty.get(1))                 # -> -1
```

```{=latex}
\clearpage
```

## 94. Cache with Expiring Keys {#a94}

```{=latex}
\markright{94. Cache with Expiring Keys}
```

[Lazy Expiry + a Min-Heap of Deadlines · Design · Tier 2 · python/094\_ttl\_cache.py]{.meta}

Design a cache whose keys expire: put(key, value, ttl, now) keeps the value until time now + ttl, get(key, now) returns it only while now is earlier, and size(now) counts the live keys. After put(b, 2, 3, 1): get(b, 3), get(b, 4) → 2, None.

```python
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class TTLCache:
    """Map key -> (value, expire_at) plus a min-heap of (expire_at, key)
    pairs, some of them stale. get O(1), put O(log n)."""

    def __init__(self):
        self.entries = {}           # key -> (value, expire_at)
        self.deadlines = []         # min-heap of (expire_at, key), some stale

    def put(self, key, value, ttl, now):
        """Store until now + ttl; a rewrite replaces the deadline. O(log n)."""
        expire_at = now + ttl
        self.entries[key] = (value, expire_at)
        heapq.heappush(self.deadlines, (expire_at, key))   # old pair goes stale

    def get(self, key, now):
        """The value while now < expire_at; an expired key is removed. O(1)."""
        if key not in self.entries:
            return None
        value, expire_at = self.entries[key]
        if now >= expire_at:
            del self.entries[key]   # lazy expiry: found dead on a read
            return None
        return value

    def purge(self, now):
        """Pop every pair whose time has come; delete keys whose pair is
        current. O(log n) per popped pair."""
        while len(self.deadlines) > 0 and self.deadlines[0][0] <= now:
            expire_at, key = heapq.heappop(self.deadlines)  # earliest first
            if key in self.entries and self.entries[key][1] == expire_at:
                del self.entries[key]   # current pair: the key expired
            # any other pair is stale: the key was rewritten or removed

    def size(self, now):
        """Purge, then count the live keys. O(k log n) for k popped pairs."""
        self.purge(now)
        return len(self.entries)


# --- try it ---
cache = TTLCache()
cache.put("a", 1, 5, 0)             # a lives until 5
cache.put("b", 2, 3, 1)             # b lives until 4
cache.put("c", 3, 10, 2)            # c lives until 12
print(cache.get("b", 3), cache.get("b", 4))     # -> 2 None
cache.put("a", 7, 5, 4)             # rewrite: a lives until 9, (5, a) is stale
print(cache.size(6))                # -> 2
print(cache.get("a", 8), cache.get("a", 9))     # -> 7 None
print(cache.size(11), cache.size(12))           # -> 1 0
```

```{=latex}
\clearpage
```

## 95. Design Browser History {#a95}

```{=latex}
\markright{95. Design Browser History}
```

[One Array and a Cursor · Design · Tier 2 · python/095\_browser\_history.py]{.meta}

Start on a homepage; visit(url) opens a page and clears the forward history, and back(steps) and forward(steps) move at most steps pages and return the page shown: home, visit news, mail, maps, back(2), visit docs, forward(1) → docs.

```python
# --- algorithm ---
class BrowserHistory:
    """The pages in one array, a cursor and the last reachable index.
    back and forward O(1), visit amortized O(1)."""

    def __init__(self, homepage):
        self.pages = [homepage]     # pages[0..last] is live history
        self.current = 0            # index of the page on screen
        self.last = 0               # the newest page forward can reach

    def visit(self, url):
        """Write url after the cursor; drop the pages ahead. Amortized O(1)."""
        self.current += 1
        if self.current == len(self.pages):
            self.pages.append(url)              # the array grows by one
        else:
            self.pages[self.current] = url      # overwrite a dead slot
        self.last = self.current                # forward history ends here

    def back(self, steps):
        """Move back at most steps pages, never before index 0. O(1)."""
        self.current = max(0, self.current - steps)
        return self.pages[self.current]

    def forward(self, steps):
        """Move forward at most steps pages, never past last. O(1)."""
        self.current = min(self.last, self.current + steps)
        return self.pages[self.current]


# --- try it ---
history = BrowserHistory("home")
history.visit("news")
history.visit("mail")
history.visit("maps")
print(history.back(2))              # -> news
history.visit("docs")               # mail and maps are no longer reachable
print(history.forward(1))           # -> docs
print(history.pages, history.last)  # -> ['home', 'news', 'docs', 'maps'] 2
print(history.back(5), history.forward(9))  # -> home docs
```

```{=latex}
\clearpage
```

## 96. Design Underground System {#a96}

```{=latex}
\markright{96. Design Underground System}
```

[Open Trips and Route Totals in Two Maps · Design · Tier 2 · python/096\_underground\_system.py]{.meta}

Track a metro: check\_in(card\_id, station, t), check\_out(card\_id, station, t) and get\_average\_time(start, end), the mean time of the finished trips from start to end: Leyton-to-Waterloo trips from 3 to 15 and 10 to 20 → 11.0.

```python
# --- algorithm ---
class UndergroundSystem:
    """Map card -> open trip, map (start, end) -> [total_time, count].
    Every call O(1)."""

    def __init__(self):
        self.open_trips = {}        # card_id -> (start station, start time)
        self.routes = {}            # (start, end) -> [total_time, count]

    def check_in(self, card_id, station, t):
        """Remember where and when the card entered. O(1)."""
        self.open_trips[card_id] = (station, t)

    def check_out(self, card_id, station, t):
        """Close the card's trip and add it to its route's totals. O(1)."""
        start, start_time = self.open_trips[card_id]
        del self.open_trips[card_id]        # the trip is over
        route = (start, station)            # direction matters
        if route not in self.routes:
            self.routes[route] = [0, 0]     # [total_time, count]
        self.routes[route][0] += t - start_time     # aggregate on write
        self.routes[route][1] += 1

    def get_average_time(self, start, end):
        """Divide the route's total time by its trip count. O(1)."""
        total_time, count = self.routes[(start, end)]
        return total_time / count


# --- try it ---
metro = UndergroundSystem()
metro.check_in(45, "Leyton", 3)
metro.check_in(32, "Paradise", 8)
metro.check_in(27, "Leyton", 10)
metro.check_out(45, "Waterloo", 15)     # 12 minutes
metro.check_out(27, "Waterloo", 20)     # 10 minutes
metro.check_out(32, "Cambridge", 22)    # 14 minutes
print(metro.get_average_time("Paradise", "Cambridge"))  # -> 14.0
print(metro.get_average_time("Leyton", "Waterloo"))     # -> 11.0
metro.check_in(10, "Leyton", 24)        # an open trip changes no average
print(metro.get_average_time("Leyton", "Waterloo"))     # -> 11.0
metro.check_out(10, "Waterloo", 38)     # 14 minutes
print(metro.get_average_time("Leyton", "Waterloo"))     # -> 12.0
print(metro.routes[("Leyton", "Waterloo")], metro.open_trips)   # -> [36, 3] {}
```

```{=latex}
\clearpage
```

## 97. Design Search Autocomplete System {#a97}

```{=latex}
\markright{97. Design Search Autocomplete System}
```

[Walk a Trie, Rank the Top 3 · Design · Tier 2 · python/097\_search\_autocomplete.py]{.meta}

Seed past sentences with counts; input(c) takes one keystroke and returns the 3 hottest past sentences that start with everything typed so far (count first, ties in ASCII order), and '\#' records the sentence. With i love you 5, island 3, iroman 2, i love leetcode 2: input("i") → i love you, island, i love leetcode.

```python
# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}              # character -> TrieNode
        self.sentence = None            # the whole sentence, if one ends here


# --- algorithm ---
class AutocompleteSystem:
    """A trie of past sentences, their counts, and a cursor that follows the
    typing: one step per keystroke, then rank the m sentences below it."""

    def __init__(self, sentences, times):
        self.root = TrieNode()
        self.counts = {}                # sentence -> how often it was typed
        for i in range(len(sentences)):
            self.record(sentences[i], times[i])
        self.typed = ""                 # the sentence typed so far
        self.node = self.root           # trie node of typed; None: dead end

    def record(self, sentence, times):
        """Walk the sentence into the trie and add to its count. O(L)."""
        node = self.root
        for ch in sentence:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.sentence = sentence        # mark where the sentence ends
        self.counts[sentence] = self.counts.get(sentence, 0) + times

    def input(self, c):
        """Step the cursor one child down and rank what lies below it; '#'
        records the typed sentence and resets. O(1) step, then top_three."""
        if c == "#":
            self.record(self.typed, 1)  # it was typed once more
            self.typed = ""
            self.node = self.root
            return []
        self.typed = self.typed + c
        if self.node is None or c not in self.node.children:
            self.node = None            # dead end: stays dead until '#'
            return []
        self.node = self.node.children[c]   # one step down, no rescan
        return self.top_three(self.node)

    def collect(self, node, found):
        """Append every sentence in the subtree of node. O(subtree size)."""
        if node.sentence is not None:
            found.append(node.sentence)
        for ch in node.children:
            self.collect(node.children[ch], found)

    def top_three(self, node):
        """Collect the sentences below node, sort them by (-count, sentence)
        and keep the first 3. O(k + m log m) for k nodes, m sentences."""
        found = []
        self.collect(node, found)
        ranked = []
        for sentence in found:
            ranked.append((-self.counts[sentence], sentence))
        ranked.sort()                   # highest count first, ties by ASCII
        best = []
        for i in range(min(3, len(ranked))):
            best.append(ranked[i][1])
        return best


# --- try it ---
sentences = ["i love you", "island", "iroman", "i love leetcode"]
system = AutocompleteSystem(sentences, [5, 3, 2, 2])
print(system.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(system.input(" "))    # -> ['i love you', 'i love leetcode']
print(system.input("a"))    # -> []
print(system.input("#"))    # -> []
print(system.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(system.input(" "))    # -> ['i love you', 'i love leetcode', 'i a']
print(system.input("a"))    # -> ['i a']
print(system.input("#"), system.counts["i a"])     # -> [] 2
```

```{=latex}
\clearpage
```

## 98. My Calendar I and II {#a98}

```{=latex}
\markright{98. My Calendar I and II}
```

[Bookings Without Double or Triple Overlaps · Design · Tier 2 · python/098\_my\_calendar.py]{.meta}

Book half-open events \[start, end). MyCalendar rejects an event that overlaps any booking; MyCalendarTwo allows a double booking but rejects a triple one. MyCalendar: book(10, 20), book(15, 25), book(20, 30) → True, False, True.

```python
# --- algorithm ---
class MyCalendar:
    """Bookings sorted by start; only the two neighbors of the insertion slot
    can overlap a new event. O(log n) search, O(n) list insert."""

    def __init__(self):
        self.starts = []                # starts of the bookings, sorted
        self.ends = []                  # ends[i] goes with starts[i]

    def book(self, start, end):
        """Find the slot by binary search, check both neighbors. O(n)."""
        left = 0
        right = len(self.starts)
        while left < right:             # first booking with a start >= start
            mid = (left + right) // 2
            if self.starts[mid] < start:
                left = mid + 1
            else:
                right = mid
        if left < len(self.starts) and self.starts[left] < end:
            return False                # the next booking starts too soon
        if left > 0 and self.ends[left - 1] > start:
            return False                # the previous booking ends too late
        self.starts.insert(left, start)
        self.ends.insert(left, end)
        return True


class MyCalendarTwo:
    """Every booking plus the overlaps already booked twice; an event that
    meets an overlap would make a triple booking. O(n) per book."""

    def __init__(self):
        self.bookings = []              # every accepted (start, end)
        self.overlaps = []              # the parts that are booked twice

    def book(self, start, end):
        """Reject if the event meets an overlap; else record the overlaps it
        creates with the bookings. O(n)."""
        for overlap_start, overlap_end in self.overlaps:
            if overlap_start < end and start < overlap_end:
                return False            # that time would be booked 3 times
        for booked_start, booked_end in self.bookings:
            if booked_start < end and start < booked_end:
                low = max(start, booked_start)
                high = min(end, booked_end)
                self.overlaps.append((low, high))   # now booked twice
        self.bookings.append((start, end))
        return True


# --- try it ---
calendar = MyCalendar()
print(calendar.book(10, 20), calendar.book(15, 25))     # -> True False
print(calendar.book(20, 30), calendar.book(5, 10))      # -> True True
print(calendar.book(0, 6), calendar.starts)             # -> False [5, 10, 20]
two = MyCalendarTwo()
print(two.book(10, 20), two.book(50, 60))               # -> True True
print(two.book(10, 40), two.book(5, 15))                # -> True False
print(two.book(5, 10), two.book(25, 55))                # -> True True
print(two.overlaps)             # -> [(10, 20), (50, 55), (25, 40)]
```

```{=latex}
\clearpage
```

## 99. Design Snake Game {#a99}

```{=latex}
\markright{99. Design Snake Game}
```

[A Deque for the Body, a Set for Collisions · Design · Tier 2 · python/099\_snake\_game.py]{.meta}

A snake starts at cell (0, 0) of a width x height grid and food appears at the given (row, col) cells one piece at a time; move(direction) returns the score, or -1 once the head leaves the grid or hits the body. Grid 3 wide, 2 high, food (1, 2) then (0, 1): moves R, D, R, U, L, U → 0, 0, 1, 1, 2, -1.

```python
from collections import deque      # appendleft and pop are O(1)


# --- helpers ---
def play(game, moves):
    """Make each move in turn; return the list of results."""
    results = []
    for direction in moves:
        results.append(game.move(direction))
    return results


# --- algorithm ---
MOVES = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


class SnakeGame:
    """The body as a deque of cells, head first, plus a set of the same cells
    for O(1) collision tests. O(1) per move."""

    def __init__(self, width, height, food):
        self.width = width
        self.height = height
        self.food = food                # (row, col) cells, eaten in this order
        self.score = 0                  # pieces eaten = index of the next one
        self.body = deque()             # head at the front, tail at the back
        self.body.append((0, 0))
        self.occupied = set()           # the same cells, for O(1) lookups
        self.occupied.add((0, 0))
        self.over = False

    def move(self, direction):
        """New head; eat or let the tail go; then test the body. O(1)."""
        if self.over:
            return -1
        row, col = self.body[0]
        step_row, step_col = MOVES[direction]
        row = row + step_row
        col = col + step_col
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            self.over = True            # hit a wall
            return -1
        head = (row, col)
        if self.score < len(self.food) and head == self.food[self.score]:
            self.score += 1             # eat: the tail stays, the snake grows
        else:
            tail = self.body.pop()      # the tail leaves first, so the head
            self.occupied.remove(tail)  # may enter the cell it just left
        if head in self.occupied:
            self.over = True            # ran into its own body
            return -1
        self.body.appendleft(head)
        self.occupied.add(head)
        return self.score


# --- try it ---
game = SnakeGame(3, 2, [(1, 2), (0, 1)])
print(play(game, "RDRUL"))              # -> [0, 0, 1, 1, 2]
print(list(game.body))                  # -> [(0, 1), (0, 2), (1, 2)]
print(game.move("U"), game.move("D"))   # -> -1 -1
board = SnakeGame(2, 2, [(0, 1), (1, 1), (1, 0)])
print(play(board, "RDLU"))              # -> [1, 2, 3, 3]
print(list(board.body))                 # -> [(0, 0), (1, 0), (1, 1), (0, 1)]
print(board.move("D"))                  # -> -1
```

```{=latex}
\clearpage
```

## 100. URL Shortener {#a100}

```{=latex}
\markright{100. URL Shortener}
```

[Base62-Encode an Increasing ID · Design · Tier 2 · python/100\_url\_shortener.py]{.meta}

encode(long\_url) gives each new URL the next integer id and returns that id in base 62 (digits 0-9, a-z, A-Z) as its short code; a repeated URL keeps its code, and decode(code) returns the URL, or "" for an unknown code. Ids starting at 1000000: encode(first url) → 4c92, decode("4c92") → the url.

```python
# --- algorithm ---
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base62(n):
    """Take the last digit with n % 62, drop it with n // 62, repeat; the
    digits come out backwards. O(log n)."""
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(ALPHABET[n % 62])     # the last digit comes out first
        n = n // 62
    digits.reverse()                        # most significant digit first
    return "".join(digits)


def from_base62(code):
    """Shift left one digit (times 62) and add the next one. O(len(code))."""
    n = 0
    for ch in code:
        n = n * 62 + ALPHABET.index(ch)     # index = the digit's value
    return n


class URLShortener:
    """A counter hands out ids and base 62 writes each id as a short code;
    two maps remember the pairs both ways."""

    def __init__(self, first_id):
        self.next_id = first_id         # the start of this server's id range
        self.url_of = {}                # code -> long url
        self.code_of = {}               # long url -> code

    def encode(self, long_url):
        """A known url keeps its code; else base 62 of the next id. O(log n)."""
        if long_url in self.code_of:
            return self.code_of[long_url]   # seen before: same code
        code = to_base62(self.next_id)
        self.next_id += 1
        self.url_of[code] = long_url
        self.code_of[long_url] = code
        return code

    def decode(self, short_code):
        """Look the code up; "" if it was never handed out. O(1)."""
        if short_code not in self.url_of:
            return ""
        return self.url_of[short_code]


# --- try it ---
long_url = "https://example.com/articles/2026/how-base62-works"
other_url = "https://example.com/docs"
shortener = URLShortener(1000000)       # this server's ids start here
print(shortener.encode(long_url), shortener.encode(other_url))  # -> 4c92 4c93
print(shortener.encode(long_url), shortener.next_id)    # -> 4c92 1000002
print(shortener.decode("4c93"))         # -> https://example.com/docs
print(repr(shortener.decode("4c94")))   # -> ''
print(to_base62(0), to_base62(61), to_base62(62))       # -> 0 Z 10
print(from_base62("4c92"), from_base62("10"))           # -> 1000000 62
```

# Tier 3 · Good to Know {#tier3}

```{=latex}
\markboth{Tier 3 · Good to Know}{}
```

The last fifty round out the set: second implementations of ideas you already own (open addressing, heap sort, Prim), bridges in a graph, the segment tree, the string toolkit, number theory, geometry and bit tricks, and the system-design algorithms that anchor a distributed-systems discussion: rate limiting, consistent hashing, unique IDs, Bloom filters, count-min sketches, quadtrees, job scheduling and the inverted index. Read each one once, keep its picture in mind, and come back to it when a problem or a design discussion calls for it.

```{=latex}
\clearpage
```

## 101. Hash Map with Open Addressing {#a101}

```{=latex}
\markright{101. Hash Map with Open Addressing}
```

[Linear Probing and Tombstones · Hash Map Internals · Tier 3 · python/101\_hash\_map\_open\_addressing.py]{.meta}

Design a hash map without a built-in dict that stores every pair in one array of slots: put(key, value), get(key) (-1 if missing) and remove(key). With 8 slots, keys 3 and 11 both start at slot 3, so 11 moves on to slot 4: put(3, 30), put(11, 110), get(11) → 110.

```python
# --- algorithm ---
EMPTY = None                # never used: a search can stop here
DELETED = "DELETED"         # tombstone: used once, a search must go on


class ProbingHashMap:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0                       # live keys
        self.tombstones = 0                 # DELETED slots
        self.slots = [EMPTY] * capacity     # EMPTY, DELETED or [key, value]

    def find(self, key):
        """Index of key's slot or -1: probe until the key or an EMPTY slot.
        Expected O(1)."""
        index = hash(key) % self.capacity
        while self.slots[index] is not EMPTY:
            slot = self.slots[index]
            if slot != DELETED and slot[0] == key:
                return index
            index = (index + 1) % self.capacity     # taken: try the next slot
        return -1

    def put(self, key, value):
        """Overwrite if present, else fill the first free slot on the path.
        Expected O(1), amortized over the resizes."""
        index = self.find(key)
        if index != -1:
            self.slots[index][1] = value            # already stored: overwrite
            return
        index = hash(key) % self.capacity
        while self.slots[index] is not EMPTY and self.slots[index] != DELETED:
            index = (index + 1) % self.capacity     # skip live pairs
        if self.slots[index] == DELETED:
            self.tombstones -= 1                    # reuse the tombstone
        self.slots[index] = [key, value]
        self.size += 1
        if (self.size + self.tombstones) / self.capacity > 0.5:
            self.resize()

    def get(self, key):
        """Value of key or -1. Expected O(1) while the table is half empty."""
        index = self.find(key)
        if index == -1:
            return -1
        return self.slots[index][1]

    def remove(self, key):
        """Leave a tombstone so that searches step over it. Expected O(1)."""
        index = self.find(key)
        if index != -1:
            self.slots[index] = DELETED
            self.size -= 1
            self.tombstones += 1

    def resize(self):
        """Double the array and re-put the live pairs only. O(n)."""
        old_slots = self.slots
        self.capacity = 2 * self.capacity
        self.slots = [EMPTY] * self.capacity
        self.size = 0
        self.tombstones = 0
        for slot in old_slots:
            if slot is not EMPTY and slot != DELETED:
                self.put(slot[0], slot[1])          # tombstones are dropped


# --- try it ---
table = ProbingHashMap()
table.put(3, 30)
table.put(11, 110)                  # home slot 3 is taken: lands in slot 4
table.put(19, 190)                  # slots 3 and 4 are taken: slot 5
table.put(4, 40)                    # home slot 4 is inside the run: slot 6
table.remove(11)                    # slot 4 becomes a tombstone
print(table.get(19), table.get(11), table.tombstones)   # -> 190 -1 1
table.put(27, 270)                  # reuses the tombstone in slot 4
print(table.slots[4], table.tombstones)                 # -> [27, 270] 0
table.put(12, 120)                  # 5 of 8 slots used: grow to 16
print(table.capacity, table.size, table.get(12))        # -> 16 5 120
```

```{=latex}
\clearpage
```

## 102. Boyer-Moore Majority Vote {#a102}

```{=latex}
\markright{102. Boyer-Moore Majority Vote}
```

[Different Votes Cancel in Pairs · Arrays & Hashing · Tier 3 · python/102\_boyer\_moore\_majority\_vote.py]{.meta}

Given an array, return the value that appears more than n / 2 times, or None if no value does, in O(n) time and O(1) extra space: \[2, 2, 1, 1, 1, 2, 2\] → 2.

```python
# --- algorithm ---
def majority_candidate(nums):
    """Pair off different values; only a majority must survive. O(n), O(1)."""
    candidate = None
    count = 0                       # candidate votes not yet cancelled
    for x in nums:
        if count == 0:
            candidate = x           # nobody standing: x takes over
            count = 1
        elif x == candidate:
            count += 1              # one more vote for the candidate
        else:
            count -= 1              # x cancels one candidate vote
    return candidate


def majority_element(nums):
    """Second pass: the candidate wins only with more than n / 2 votes."""
    candidate = majority_candidate(nums)
    votes = 0
    for x in nums:
        if x == candidate:
            votes += 1
    if votes * 2 > len(nums):
        return candidate
    return None                     # no value holds a strict majority


# --- try it ---
print(majority_element([2, 2, 1, 1, 1, 2, 2]))  # -> 2
print(majority_element([3, 2, 3]))              # -> 3
print(majority_candidate([1, 2, 3]))            # -> 3
print(majority_element([1, 2, 3]))              # -> None
print(majority_element([1, 2]))                 # -> None
```

```{=latex}
\clearpage
```

## 103. Next Permutation {#a103}

```{=latex}
\markright{103. Next Permutation}
```

[Find the Pivot, Swap, Reverse the Suffix · Arrays & Hashing · Tier 3 · python/103\_next\_permutation.py]{.meta}

Rearrange an array in place into the next permutation in lexicographic order, or into the first (sorted) one if it is already the last; values may repeat: \[1, 3, 5, 4, 2\] → \[1, 4, 2, 3, 5\], and \[3, 2, 1\] → \[1, 2, 3\].

```python
# --- algorithm ---
def next_permutation(nums):
    """Find the pivot, swap it with the rightmost larger value, reverse the
    suffix. O(n) time, O(1) space, in place."""
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:    # walk past the falling suffix
        i -= 1
    if i >= 0:                                  # nums[i] is the pivot
        j = len(nums) - 1
        while nums[j] <= nums[i]:               # rightmost larger value
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    reverse(nums, i + 1, len(nums) - 1)         # falling suffix -> rising


def reverse(nums, left, right):
    """Reverse nums[left..right] in place, swapping the ends inward. O(n)."""
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


# --- try it ---
nums = [1, 3, 5, 4, 2]
next_permutation(nums)
print(nums)                         # -> [1, 4, 2, 3, 5]
nums = [3, 2, 1]
next_permutation(nums)
print(nums)                         # -> [1, 2, 3]
nums = [1, 5, 1]
next_permutation(nums)
print(nums)                         # -> [5, 1, 1]
nums = [7]
next_permutation(nums)
print(nums)                         # -> [7]
```

```{=latex}
\clearpage
```

## 104. Reorder List {#a104}

```{=latex}
\markright{104. Reorder List}
```

[Find the Middle, Reverse, Weave · Two Pointers · Tier 3 · python/104\_reorder\_list.py]{.meta}

Reorder a singly linked list L0 L1 ... Ln in place into L0 Ln L1 Ln-1 L2 ..., relinking the nodes rather than copying values. As values: \[1, 2, 3, 4, 5\] → \[1, 5, 2, 4, 3\].

```python
# --- helpers ---
# standard helpers ListNode, build_list, to_list: printed once under Standard Helpers


# --- algorithm ---
def reverse_list(head):
    """Turn every next arrow around in one walk. O(n) time, O(1) space."""
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next       # save the rest before the cut
        curr.next = prev
        prev = curr
        curr = next_node
    return prev


def reorder_list(head):
    """Find the middle, reverse the second half, weave the two halves.
    O(n) time, O(1) space."""
    if head is None:
        return
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next            # ends on the first half's last node
        fast = fast.next.next
    second = slow.next
    slow.next = None                # cut after the first half
    second = reverse_list(second)
    first = head
    while second is not None:       # the second half is never longer
        next_first = first.next     # save both rests before relinking
        next_second = second.next
        first.next = second
        second.next = next_first
        first = next_first
        second = next_second


# --- try it ---
head = build_list([1, 2, 3, 4, 5])
reorder_list(head)
print(to_list(head))                    # -> [1, 5, 2, 4, 3]
head = build_list([1, 2, 3, 4])
reorder_list(head)
print(to_list(head))                    # -> [1, 4, 2, 3]
head = build_list([7])
reorder_list(head)
print(to_list(head))                    # -> [7]
```

```{=latex}
\clearpage
```

## 105. Median of K Sorted Arrays {#a105}

```{=latex}
\markright{105. Median of K Sorted Arrays}
```

[Binary Search on the Value · Binary Search · Tier 3 · python/105\_median\_k\_sorted\_arrays.py]{.meta}

Given k sorted arrays of integers holding N \>= 1 values in total, return the median of all of them (the average of the two middle values when N is even): \[\[1, 4, 9\], \[2, 3, 7, 10\], \[5, 8\]\] → 5.

```python
import math                         # math.inf seeds the running min and max


# --- algorithm ---
def count_at_most(arr, value):
    """Upper bound (#14): how many values of sorted arr are <= value.
    O(log L)."""
    lo = 0
    hi = len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= value:
            lo = mid + 1
        else:
            hi = mid
    return lo


def kth_smallest(arrays, rank):
    """Smallest value v with at least rank values <= v, by binary search on
    v from the smallest to the largest value. O(k log L log R)."""
    lo = math.inf
    hi = -math.inf
    for arr in arrays:
        if len(arr) > 0:
            lo = min(lo, arr[0])        # smallest first element
            hi = max(hi, arr[-1])       # largest last element
    while lo < hi:
        mid = (lo + hi) // 2
        count = 0
        for arr in arrays:
            count += count_at_most(arr, mid)
        if count >= rank:
            hi = mid                    # mid already covers rank values
        else:
            lo = mid + 1                # too few values are <= mid
    return lo


def median_k_sorted(arrays):
    """One order statistic for odd N, the average of two for even N.
    O(k log L log R)."""
    total = 0
    for arr in arrays:
        total += len(arr)
    if total % 2 == 1:
        return kth_smallest(arrays, total // 2 + 1)
    low = kth_smallest(arrays, total // 2)
    high = kth_smallest(arrays, total // 2 + 1)
    return (low + high) / 2


# --- try it ---
arrays = [[1, 4, 9], [2, 3, 7, 10], [5, 8]]
print(median_k_sorted(arrays))                      # -> 5
print(kth_smallest(arrays, 6))                      # -> 7
print(median_k_sorted([[1, 2], [3, 4]]))            # -> 2.5
print(median_k_sorted([[-5, -1], [], [-3]]))        # -> -3
```

```{=latex}
\clearpage
```

## 106. Random Pick with Weight {#a106}

```{=latex}
\markright{106. Random Pick with Weight}
```

[Prefix Sums + Binary Search · Binary Search · Tier 3 · python/106\_random\_pick\_with\_weight.py]{.meta}

Given positive weights w, pick\_index returns index i with probability w\[i\] / sum(w): w = \[1, 3, 2\] → index 0, 1, 2 with chances 1/6, 3/6, 2/6.

```python
import random                       # randint(a, b) includes both ends


# --- algorithm ---
class WeightedPicker:
    """Prefix sums of the weights; a pick binary-searches a uniform target."""

    def __init__(self, w):
        self.prefix = []            # prefix[i] = w[0] + ... + w[i]
        running = 0
        for weight in w:
            running += weight
            self.prefix.append(running)
        self.total = running

    def lower_bound(self, target):
        """First index i with prefix[i] >= target: the owner of target.
        O(log n)."""
        lo = 0
        hi = len(self.prefix)       # half-open [lo, hi)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.prefix[mid] < target:
                lo = mid + 1        # mid's whole range lies below target
            else:
                hi = mid            # mid's range reaches target: keep it
        return lo

    def pick_index(self):
        """Draw a target uniformly from 1..total, return its owner. O(log n)."""
        target = random.randint(1, self.total)
        return self.lower_bound(target)


def is_fair(w, draws):
    """Index i should win about draws * w[i] / total picks. O(draws log n)."""
    picker = WeightedPicker(w)
    counts = [0] * len(w)
    for trial in range(draws):
        i = picker.pick_index()
        counts[i] += 1
    for i in range(len(w)):
        expected = draws * w[i] / picker.total
        if abs(counts[i] - expected) > 0.05 * expected:
            return False            # more than 5 percent off
    return True


# --- try it ---
picker = WeightedPicker([1, 3, 2])
print(picker.prefix, picker.total)          # -> [1, 4, 6] 6
owners = []
for target in range(1, 7):
    owners.append(picker.lower_bound(target))
print(owners)                               # -> [0, 1, 1, 1, 2, 2]
random.seed(7)
print(is_fair([1, 3, 2], 60000))            # -> True
print(is_fair([5, 1, 1, 10, 3], 60000))     # -> True
print(WeightedPicker([42]).pick_index())    # -> 0
```

```{=latex}
\clearpage
```

## 107. Segment Tree {#a107}

```{=latex}
\markright{107. Segment Tree}
```

[Range Sums with Point Updates · Range Queries · Tier 3 · python/107\_segment\_tree.py]{.meta}

Keep an array under two operations, update(index, value), which sets one element, and query(left, right), which sums nums\[left..right\], both O(log n): \[5, 8, 6, 3, 2, 7, 2, 6\], query(2, 6) → 20, then update(4, 9), query → 27.

```python
# --- algorithm ---
class SegmentTree:
    """Node 1 owns the whole array, and node i hands the two halves of its
    segment to nodes 2i and 2i + 1; every node stores its segment's sum."""

    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)      # 4n slots always suffice
        if self.n > 0:
            self.build(nums, 1, 0, self.n - 1)

    def build(self, nums, node, lo, hi):
        """Fill the sums of node's subtree, which owns nums[lo..hi]. O(n)."""
        if lo == hi:
            self.tree[node] = nums[lo]      # a leaf owns one element
            return
        mid = (lo + hi) // 2
        self.build(nums, 2 * node, lo, mid)
        self.build(nums, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, index, value):
        """Set nums[index] to value. O(log n)."""
        self.update_at(1, 0, self.n - 1, index, value)

    def update_at(self, node, lo, hi, index, value):
        """Walk down to the leaf of index, then redo the sums on the way up."""
        if lo == hi:
            self.tree[node] = value
            return
        mid = (lo + hi) // 2
        if index <= mid:                    # index lies in the left half
            self.update_at(2 * node, lo, mid, index, value)
        else:
            self.update_at(2 * node + 1, mid + 1, hi, index, value)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left, right):
        """Sum of nums[left..right], both ends included. O(log n)."""
        return self.query_at(1, 0, self.n - 1, left, right)

    def query_at(self, node, lo, hi, left, right):
        """Sum of the part of node's segment nums[lo..hi] inside left..right."""
        if right < lo or hi < left:
            return 0                        # no overlap
        if left <= lo and hi <= right:
            return self.tree[node]          # full overlap: the stored sum
        mid = (lo + hi) // 2                # partial overlap: both halves
        left_sum = self.query_at(2 * node, lo, mid, left, right)
        right_sum = self.query_at(2 * node + 1, mid + 1, hi, left, right)
        return left_sum + right_sum


# --- try it ---
tree = SegmentTree([5, 8, 6, 3, 2, 7, 2, 6])
print(tree.query(2, 6))                     # -> 20
tree.update(4, 9)                           # nums[4] becomes 9
print(tree.query(2, 6))                     # -> 27
print(tree.query(0, 7), tree.query(3, 3))   # -> 46 3
mixed = SegmentTree([-2, 0, 3, -5, 2, -1])
mixed.update(3, 4)
print(mixed.query(0, 2), mixed.query(2, 5))     # -> 1 8
```

```{=latex}
\clearpage
```

## 108. Counting Sort {#a108}

```{=latex}
\markright{108. Counting Sort}
```

[Count, Prefix-Sum, Place · Sorting · Tier 3 · python/108\_counting\_sort.py]{.meta}

Sort integers that lie in a small range \[low, high\], negatives included, without comparing them: \[2, -1, 3, 2, 0, -1\] → \[-1, -1, 0, 2, 2, 3\].

```python
# --- algorithm ---
def counting_sort(nums):
    """Count each value, turn the counts into end positions, place each value.
    O(n + k) time and space for k = high - low + 1 possible values."""
    if len(nums) == 0:
        return []
    low = min(nums)
    high = max(nums)
    count = [0] * (high - low + 1)          # count[v - low] is for value v
    for value in nums:
        count[value - low] += 1
    for slot in range(1, len(count)):       # now: how many values are <= it
        count[slot] += count[slot - 1]
    result = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):  # right to left keeps it stable
        value = nums[i]
        count[value - low] -= 1             # the last free seat
        result[count[value - low]] = value
    return result


# --- try it ---
print(counting_sort([2, -1, 3, 2, 0, -1]))   # -> [-1, -1, 0, 2, 2, 3]
print(counting_sort([5, 3, 5, 1]))           # -> [1, 3, 5, 5]
print(counting_sort([4]))                    # -> [4]
print(counting_sort([]))                     # -> []
```

```{=latex}
\clearpage
```

## 109. Heap Sort {#a109}

```{=latex}
\markright{109. Heap Sort}
```

[Build a Max-Heap, Swap the Max to the End · Sorting · Tier 3 · python/109\_heap\_sort.py]{.meta}

Sort an array of integers in place, with O(1) extra space and an O(n log n) bound even in the worst case: \[4, 10, 3, 5, 1\] → \[1, 3, 4, 5, 10\].

```python
# --- algorithm ---
def sift_down(nums, i, n):
    """Max-heap sift-down: swap nums[i] with its larger child until no child
    is larger; only nums[0..n-1] is the heap. O(log n)."""
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and nums[left] > nums[largest]:
            largest = left
        if right < n and nums[right] > nums[largest]:
            largest = right
        if largest == i:                # no child is larger: done
            return
        nums[i], nums[largest] = nums[largest], nums[i]
        i = largest


def heap_sort(nums):
    """Build a max-heap, then move the max to the end n - 1 times.
    O(n log n) time, O(1) extra space."""
    n = len(nums)
    for i in range(n // 2 - 1, -1, -1):          # build: last parent to root
        sift_down(nums, i, n)
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]  # the max joins the sorted tail
        sift_down(nums, 0, end)                  # the heap is nums[0..end-1]
    return nums


# --- try it ---
print(heap_sort([4, 10, 3, 5, 1]))    # -> [1, 3, 4, 5, 10]
print(heap_sort([2, -7, 2, 0, -7]))   # -> [-7, -7, 0, 2, 2]
print(heap_sort([9]))                 # -> [9]
print(heap_sort([]))                  # -> []
```

```{=latex}
\clearpage
```

## 110. Circular Queue {#a110}

```{=latex}
\markright{110. Circular Queue}
```

[Ring Buffer with Head and Count · Queues · Tier 3 · python/110\_circular\_queue.py]{.meta}

Design a FIFO queue of fixed capacity on one array whose end wraps around to its start: enqueue and dequeue return True or False, front and rear return -1 when empty. Capacity 3: enqueue 1, 2, 3, then enqueue 4 → False (full).

```python
# --- algorithm ---
class CircularQueue:
    def __init__(self, capacity):
        self.items = [0] * capacity
        self.capacity = capacity
        self.head = 0                   # index of the front value
        self.count = 0                  # how many values are stored

    def enqueue(self, value):
        """Write at tail = (head + count) mod capacity. O(1)."""
        if self.is_full():
            return False
        tail = (self.head + self.count) % self.capacity    # wraps to 0
        self.items[tail] = value
        self.count += 1
        return True

    def dequeue(self):
        """Drop the front value by moving head one step, wrapping. O(1)."""
        if self.is_empty():
            return False
        self.head = (self.head + 1) % self.capacity    # old value stays
        self.count -= 1
        return True

    def front(self):
        """The oldest value, or -1 if empty. O(1)."""
        if self.is_empty():
            return -1
        return self.items[self.head]

    def rear(self):
        """The newest value, at (head + count - 1) mod capacity. O(1)."""
        if self.is_empty():
            return -1
        return self.items[(self.head + self.count - 1) % self.capacity]

    def is_empty(self):
        """No values stored. O(1)."""
        return self.count == 0

    def is_full(self):
        """Every slot holds a value. O(1)."""
        return self.count == self.capacity


# --- try it ---
queue = CircularQueue(3)
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(queue.enqueue(4), queue.rear())               # -> False 3
print(queue.dequeue(), queue.enqueue(4))            # -> True True
print(queue.front(), queue.rear(), queue.items)     # -> 2 4 [4, 2, 3]
print(queue.is_full(), queue.head, queue.count)     # -> True 1 3
```

```{=latex}
\clearpage
```

## 111. Candy {#a111}

```{=latex}
\markright{111. Candy}
```

[Two Passes: Left, Then Right · Greedy · Tier 3 · python/111\_candy.py]{.meta}

Children stand in a line with ratings. Each gets at least one candy, and a child rated higher than a neighbor gets more candies than that neighbor. Return the fewest candies in total: \[1, 0, 2, 5, 4, 3, 1\] → 15.

```python
# --- algorithm ---
def candy(ratings):
    """Left pass for left neighbors, right pass for right ones. O(n) time."""
    n = len(ratings)
    candies = [1] * n               # everyone gets at least one
    for i in range(1, n):           # left to right
        if ratings[i] > ratings[i - 1]:     # beat a lower left neighbor
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):  # right to left
        if ratings[i] > ratings[i + 1]:     # also beat a lower right neighbor
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)


# --- try it ---
print(candy([1, 0, 2, 5, 4, 3, 1]))     # -> 15
print(candy([1, 0, 2]))                 # -> 5
print(candy([1, 2, 2]))                 # -> 4
print(candy([1, 2, 3, 1]))              # -> 7
```

```{=latex}
\clearpage
```

## 112. Hand of Straights {#a112}

```{=latex}
\markright{112. Hand of Straights}
```

[Start Every Group at the Smallest Card · Greedy · Tier 3 · python/112\_hand\_of\_straights.py]{.meta}

Can the cards be split into groups of group\_size consecutive values, every card used exactly once? \[1, 2, 3, 6, 2, 3, 4, 7, 8\], group\_size 3 → True (as \[1, 2, 3\], \[2, 3, 4\] and \[6, 7, 8\]).

```python
# --- algorithm ---
def can_form_straights(hand, group_size):
    """The smallest card left must start a group. O(n log n) for the sort."""
    if len(hand) % group_size != 0:
        return False
    count = {}
    for card in hand:
        count[card] = count.get(card, 0) + 1
    for card in sorted(count):          # distinct cards, smallest first
        starts = count[card]            # groups that must start at this card
        if starts > 0:
            for next_card in range(card, card + group_size):
                if count.get(next_card, 0) < starts:
                    return False        # a group would have a gap
                count[next_card] -= starts
    return True


# --- try it ---
print(can_form_straights([1, 2, 3, 6, 2, 3, 4, 7, 8], 3))   # -> True
print(can_form_straights([1, 2, 4, 5, 6, 7], 3))            # -> False
print(can_form_straights([1, 2, 3, 4, 5], 4))               # -> False
print(can_form_straights([2, 1, 3], 3))                     # -> True
```

```{=latex}
\clearpage
```

## 113. N-Queens {#a113}

```{=latex}
\markright{113. N-Queens}
```

[Columns and Diagonals as Sets · Backtracking · Tier 3 · python/113\_n\_queens.py]{.meta}

Place n queens on an n x n board so that no two share a row, a column or a diagonal, and return every such board as a list of row strings: n = 4 → two boards, \['.Q..', '...Q', 'Q...', '..Q.'\] and its mirror image.

```python
# --- helpers ---
def draw(queens):
    """queens[r] is the column of row r's queen; spell each row. O(n^2)."""
    n = len(queens)
    board = []
    for col in queens:
        board.append("." * col + "Q" + "." * (n - 1 - col))
    return board


# --- algorithm ---
def backtrack(n, row, queens, cols, diags, anti_diags, boards):
    """Try each safe column in this row, then fill the rows below it."""
    if row == n:
        boards.append(draw(queens))     # every row holds a queen
        return
    for col in range(n):
        if col in cols or (row - col) in diags or (row + col) in anti_diags:
            continue                    # attacked: a column or a diagonal
        queens.append(col)              # place the queen
        cols.add(col)
        diags.add(row - col)
        anti_diags.add(row + col)
        backtrack(n, row + 1, queens, cols, diags, anti_diags, boards)
        queens.pop()                    # remove it, undoing all four marks
        cols.remove(col)
        diags.remove(row - col)
        anti_diags.remove(row + col)


def solve_n_queens(n):
    """One queen per row; three sets make each safety check O(1)."""
    boards = []
    backtrack(n, 0, [], set(), set(), set(), boards)
    return boards


# --- try it ---
boards = solve_n_queens(4)
print(boards[0])                    # -> ['.Q..', '...Q', 'Q...', '..Q.']
print(boards[1])                    # -> ['..Q.', 'Q...', '...Q', '.Q..']
print(len(solve_n_queens(8)))       # -> 92
print(solve_n_queens(3))            # -> []
print(solve_n_queens(1))            # -> [['Q']]
```

```{=latex}
\clearpage
```

## 114. Bipartite Check {#a114}

```{=latex}
\markright{114. Bipartite Check}
```

[BFS Two-Coloring · BFS · Tier 3 · python/114\_bipartite\_check.py]{.meta}

Given an undirected graph as an adjacency list (graph\[u\] lists the neighbors of u), decide whether its nodes split into two sides with every edge running between the sides. A square 0-1-2-3 plus a separate triangle 4-5-6: \[\[1, 3\], \[0, 2\], \[1, 3\], \[0, 2\], \[5, 6\], \[4, 6\], \[4, 5\]\] → False.

```python
from collections import deque      # popleft is O(1)


# --- algorithm ---
def is_bipartite(graph):
    """BFS each component, giving every neighbor the opposite color; an edge
    inside one color means an odd cycle. O(V + E) time."""
    n = len(graph)
    color = [-1] * n                    # -1 uncolored, else side 0 or 1
    for start in range(n):
        if color[start] != -1:
            continue                    # colored by an earlier search
        color[start] = 0                # a new component: either side works
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]   # the other side
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False        # an edge inside one side
    return True


# --- try it ---
graph = [[1, 3], [0, 2], [1, 3], [0, 2], [5, 6], [4, 6], [4, 5]]
print(is_bipartite(graph))                                  # -> False
print(is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]))       # -> True
print(is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]))  # -> False
print(is_bipartite([[], [2], [1]]))                         # -> True
```

```{=latex}
\clearpage
```

## 115. Cycle Detection in an Undirected Graph {#a115}

```{=latex}
\markright{115. Cycle Detection in an Undirected Graph}
```

[DFS That Skips the Parent Edge · Cycle Detection · Tier 3 · python/115\_undirected\_cycle\_detection.py]{.meta}

Given n nodes and an undirected edge list (no repeated edges), decide whether the graph has a cycle; it may be disconnected: n = 6, edges 0-1, 2-3, 3-4, 4-5, 5-2 → True (2, 3, 4, 5 form a square).

```python
# --- algorithm ---
def has_cycle(n, edges):
    """DFS from every unvisited node; a visited neighbor that is not the
    parent closes a cycle. O(V + E) time, O(V + E) space."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)              # undirected: store both directions
    visited = [False] * n
    for start in range(n):              # a cycle can be in any component
        if visited[start]:
            continue
        visited[start] = True
        stack = []
        stack.append((start, -1))       # (node, the node we came from)
        while stack:
            node, parent = stack.pop()
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True    # mark when discovered
                    stack.append((neighbor, node))
                elif neighbor != parent:
                    return True         # reached again, not via parent
    return False


# --- try it ---
print(has_cycle(6, [[0, 1], [2, 3], [3, 4], [4, 5], [5, 2]]))   # -> True
print(has_cycle(5, [[0, 1], [0, 2], [0, 3], [1, 4]]))           # -> False
print(has_cycle(4, [[0, 1], [2, 3]]))                           # -> False
print(has_cycle(3, [[0, 1], [1, 2], [2, 0]]))                   # -> True
```

```{=latex}
\clearpage
```

## 116. Critical Connections {#a116}

```{=latex}
\markright{116. Critical Connections}
```

[Tarjan's Bridges: Discovery Time vs Low-Link · Graphs · Tier 3 · python/116\_critical\_connections.py]{.meta}

Given n nodes and an undirected edge list with no repeated edges, return every edge whose removal splits its component in two (a bridge), each pair sorted and the list sorted: n = 7, edges 0-1 1-2 2-0 1-3 3-4 4-5 5-3 5-6 → \[\[1, 3\], \[5, 6\]\].

```python
# --- algorithm ---
def critical_connections(n, connections):
    """One DFS stamps discovery times and low-links; tree edge u-v is a bridge
    when nothing below v reaches back to u or above. O(V + E) time and space."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)                  # undirected: both directions
    disc = [-1] * n                         # discovery time, -1 = not visited
    low = [0] * n                           # lowest disc the subtree reaches
    timer = [0]                             # next discovery time, one box
    bridges = []
    for start in range(n):                  # one DFS per component
        if disc[start] == -1:
            dfs(graph, start, -1, disc, low, timer, bridges)
    bridges.sort()                          # a deterministic order
    return bridges


def dfs(graph, u, parent, disc, low, timer, bridges):
    """Stamp u, explore below it, and record every bridge in its subtree."""
    disc[u] = timer[0]
    low[u] = timer[0]
    timer[0] += 1
    for v in graph[u]:
        if v == parent:
            continue                        # the tree edge we came down by
        if disc[v] == -1:                   # tree edge: explore v first
            dfs(graph, v, u, disc, low, timer, bridges)
            low[u] = min(low[u], low[v])
            if low[v] > disc[u]:            # nothing below v reaches u or above
                bridges.append([min(u, v), max(u, v)])
        else:
            low[u] = min(low[u], disc[v])   # back edge to an ancestor


# --- try it ---
edges = [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4], [4, 5], [5, 3], [5, 6]]
print(critical_connections(7, edges))       # -> [[1, 3], [5, 6]]
print(critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))   # -> [[1, 3]]
print(critical_connections(3, [[0, 1], [1, 2], [2, 0]]))           # -> []
forest = [[3, 2], [1, 0], [2, 4]]           # two trees: every edge is a bridge
print(critical_connections(5, forest))      # -> [[0, 1], [2, 3], [2, 4]]
```

```{=latex}
\clearpage
```

## 117. Bellman-Ford {#a117}

```{=latex}
\markright{117. Bellman-Ford}
```

[Relax Every Edge n - 1 Times · Shortest Path · Tier 3 · python/117\_bellman\_ford.py]{.meta}

Given n nodes, directed edges \[u, v, w\] whose weights may be negative, and a source, return the shortest distance to every node (inf if unreachable), or None if a negative cycle is reachable: n = 4, source 0, edges \[\[2, 3, 1\], \[1, 2, -3\], \[0, 1, 4\], \[0, 2, 2\]\] → \[0, 4, 1, 2\].

```python
import math                             # math.inf: no path found yet


# --- algorithm ---
def bellman_ford(n, edges, source):
    """Relax every edge, round after round, at most n - 1 rounds; a later
    improvement means a negative cycle. O(V * E) time, O(V) space."""
    dist = [math.inf] * n
    dist[source] = 0
    for _ in range(n - 1):              # a shortest path has <= n - 1 edges
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:   # inf + w stays inf: no false relax
                dist[v] = dist[u] + w   # a cheaper way into v, through u
                changed = True
        if not changed:
            break                       # quiet round: all distances final
    for u, v, w in edges:
        if dist[u] + w < dist[v]:       # still improving after n - 1 rounds
            return None                 # a negative cycle is reachable
    return dist


# --- try it ---
edges = [[2, 3, 1], [1, 2, -3], [0, 1, 4], [0, 2, 2]]
print(bellman_ford(4, edges, 0))                    # -> [0, 4, 1, 2]
print(bellman_ford(3, [[0, 1, 5]], 0))              # -> [0, 5, inf]
reachable_cycle = [[0, 1, 1], [1, 2, -1], [2, 1, -1]]
print(bellman_ford(3, reachable_cycle, 0))          # -> None
unreachable_cycle = [[0, 1, 2], [2, 3, -1], [3, 2, -1]]
print(bellman_ford(4, unreachable_cycle, 0))        # -> [0, 2, inf, inf]
```

```{=latex}
\clearpage
```

## 118. Kruskal's Minimum Spanning Tree {#a118}

```{=latex}
\markright{118. Kruskal's Minimum Spanning Tree}
```

[Sort Edges, Let Union-Find Reject Cycles · MST · Tier 3 · python/118\_kruskal\_mst.py]{.meta}

Given n nodes and undirected edges \[u, v, w\], return the total weight and the edges of a minimum spanning tree, or None if the graph is disconnected: n = 5, edges 0-1 (4), 0-2 (1), 1-2 (2), 1-3 (5), 2-3 (8), 3-4 (3) → (11, \[\[0, 2, 1\], \[1, 2, 2\], \[3, 4, 3\], \[1, 3, 5\]\]).

```python
# --- algorithm ---
def find(parent, x):
    """Root of x; repoint the path straight at it. Near O(1) amortized."""
    if parent[x] != x:
        parent[x] = find(parent, parent[x])     # path compression
    return parent[x]


def union(parent, size, a, b):
    """Merge the components of a and b; False if they are already one."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return False                    # already one component
    if size[root_a] < size[root_b]:
        root_a, root_b = root_b, root_a     # hang the smaller tree below
    parent[root_b] = root_a
    size[root_a] += size[root_b]
    return True


def kruskal(n, edges):
    """Take edges cheapest first; keep one only if it joins two components.
    O(E log E) for the sort."""
    order = []
    for u, v, w in edges:
        order.append((w, u, v))         # weight first: sort by weight
    order.sort()                        # cheapest edge first
    parent = list(range(n))             # every node is its own root
    size = [1] * n
    total = 0
    tree = []
    for w, u, v in order:
        if union(parent, size, u, v):   # two components: edge is safe
            total += w
            tree.append([u, v, w])
            if len(tree) == n - 1:
                break                   # n - 1 edges span all n nodes
    if len(tree) < n - 1:
        return None                     # the graph is disconnected
    return total, tree


# --- try it ---
edges = [[0, 1, 4], [0, 2, 1], [1, 2, 2], [1, 3, 5], [2, 3, 8], [3, 4, 3]]
total, tree = kruskal(5, edges)
print(total)                                # -> 11
print(tree)                 # -> [[0, 2, 1], [1, 2, 2], [3, 4, 3], [1, 3, 5]]
print(kruskal(4, [[0, 1, 1], [2, 3, 1]]))   # -> None
print(kruskal(1, []))                       # -> (0, [])
```

```{=latex}
\clearpage
```

## 119. Prim's Minimum Spanning Tree {#a119}

```{=latex}
\markright{119. Prim's Minimum Spanning Tree}
```

[Grow One Tree with a Min-Heap · MST · Tier 3 · python/119\_prim\_mst.py]{.meta}

Given n nodes and undirected edges \[u, v, w\], return the total weight of a minimum spanning tree, or None if the graph is disconnected: n = 5, edges 0-1 (4), 0-2 (1), 1-2 (2), 1-3 (5), 2-3 (8), 3-4 (3) → 11.

```python
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
def prim(n, edges):
    """Grow one tree from node 0, always adding the cheapest edge that
    leaves it. O(E log V) time, O(V + E) space."""
    graph = []
    for _ in range(n):
        graph.append([])
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))         # undirected: store both directions
    in_tree = [False] * n
    heap = []
    heapq.heappush(heap, (0, 0))        # (cost to attach, node): start at 0
    total = 0
    count = 0
    while heap and count < n:
        cost, node = heapq.heappop(heap)
        if in_tree[node]:
            continue                    # stale: joined by a cheaper edge
        in_tree[node] = True            # mark when popped, not when pushed
        total += cost
        count += 1
        for weight, neighbor in graph[node]:
            if not in_tree[neighbor]:
                heapq.heappush(heap, (weight, neighbor))
    if count < n:
        return None                     # some node was never reached
    return total


# --- try it ---
edges = [[0, 1, 4], [0, 2, 1], [1, 2, 2], [1, 3, 5], [2, 3, 8], [3, 4, 3]]
print(prim(5, edges))                               # -> 11
print(prim(4, [[0, 1, 1], [2, 3, 1]]))              # -> None
print(prim(3, [[0, 1, 5], [1, 2, -2], [0, 2, 1]]))  # -> -1
print(prim(1, []))                                  # -> 0
```

```{=latex}
\clearpage
```

## 120. Rabin-Karp {#a120}

```{=latex}
\markright{120. Rabin-Karp}
```

[Rolling Hash Pattern Matching · Strings · Tier 3 · python/120\_rabin\_karp.py]{.meta}

Return every index where the pattern starts in the text, comparing window hashes first and confirming each hash hit character by character: text "abracadabra", pattern "abra" → \[0, 7\].

```python
# --- algorithm ---
BASE = 256                              # one digit per character code
MOD = 1000000007                        # a large prime keeps collisions rare


def poly_hash(s):
    """s read as a number in base BASE, kept mod MOD. O(len(s))."""
    value = 0
    for ch in s:
        value = (value * BASE + ord(ch)) % MOD  # shift left, add a digit
    return value


def rabin_karp(text, pattern):
    """Roll one window hash across the text; compare characters only on a
    hash hit. Expected O(n + m) time when matches are few."""
    n = len(text)
    m = len(pattern)
    if m == 0 or m > n:
        return []
    high = pow(BASE, m - 1, MOD)        # leading digit weight: BASE^(m-1) % MOD
    pattern_hash = poly_hash(pattern)
    window_hash = poly_hash(text[0:m])
    matches = []
    for start in range(n - m + 1):
        if window_hash == pattern_hash and text[start:start + m] == pattern:
            matches.append(start)       # a hash hit, confirmed
        if start + m < n:               # roll the window one step right
            window_hash = (window_hash - ord(text[start]) * high) % MOD
            window_hash = (window_hash * BASE + ord(text[start + m])) % MOD
    return matches


# --- try it ---
print(rabin_karp("abracadabra", "abra"))                # -> [0, 7]
print(rabin_karp("aaaaa", "aa"))                        # -> [0, 1, 2, 3]
print(poly_hash("neonatus") == poly_hash("plumular"))   # -> True
print(rabin_karp("neonatus", "plumular"))               # -> []
print(rabin_karp("abc", "abcd"))                        # -> []
```

```{=latex}
\clearpage
```

## 121. Longest Common Prefix {#a121}

```{=latex}
\markright{121. Longest Common Prefix}
```

[Vertical Scan · Strings · Tier 3 · python/121\_longest\_common\_prefix.py]{.meta}

Return the longest string that is a prefix of every string in the list, or "" if they share none: \["flower", "flow", "flight"\] → "fl".

```python
# --- algorithm ---
def longest_common_prefix(strs):
    """Scan column by column; stop at the first mismatch or the end of the
    shortest string. O(n * (L + 1)) for n strings and answer length L."""
    if len(strs) == 0:
        return ""
    first = strs[0]
    for col in range(len(first)):
        ch = first[col]
        for word in strs:
            if col == len(word) or word[col] != ch:   # word ended, or mismatch
                return first[0:col]
    return first                        # first is a prefix of all the others


# --- try it ---
print(longest_common_prefix(["flower", "flow", "flight"]))      # -> fl
print(repr(longest_common_prefix(["dog", "racecar", "car"])))   # -> ''
print(longest_common_prefix(["inter", "internet", "interview"]))   # -> inter
print(longest_common_prefix(["flower", "flow"]))                # -> flow
```

```{=latex}
\clearpage
```

## 122. Text Justification {#a122}

```{=latex}
\markright{122. Text Justification}
```

[Greedy Line Packing, Then Spread the Spaces · Strings · Tier 3 · python/122\_text\_justification.py]{.meta}

Pack words greedily into lines of exactly max\_width characters, spreading the spaces evenly with the extras in the leftmost gaps; the last line and one-word lines are left-justified: \["What", "must", "be", "acknowledgment"\], 16 → \["What must be", "acknowledgment "\].

```python
# --- algorithm ---
def full_justify(words, max_width):
    """Take words while they fit, then justify the line.
    O(n + L * max_width) for n words and L lines."""
    lines = []
    i = 0
    while i < len(words):
        j = i + 1                       # the line is words[i..j-1]
        width = len(words[i])           # its letters plus one space per gap
        while j < len(words) and width + 1 + len(words[j]) <= max_width:
            width = width + 1 + len(words[j])
            j += 1
        is_last = (j == len(words))
        lines.append(justify_line(words, i, j, max_width, is_last))
        i = j
    return lines


def justify_line(words, i, j, max_width, is_last):
    """Lay words[i..j-1] into exactly max_width characters. O(max_width)."""
    if is_last or j - i == 1:           # left-justify, pad on the right
        line = " ".join(words[i:j])
        return line + " " * (max_width - len(line))
    letters = 0
    for k in range(i, j):
        letters += len(words[k])
    gaps = j - i - 1
    spaces = max_width - letters        # blanks to place in the gaps
    each = spaces // gaps
    extra = spaces % gaps               # leftmost gaps get one more
    pieces = [words[i]]
    for k in range(i + 1, j):
        gap = each
        if k - i <= extra:              # gap number k - i, from 1
            gap += 1
        pieces.append(" " * gap)
        pieces.append(words[k])
    return "".join(pieces)


# --- try it ---
words = ["This", "is", "an", "example", "of", "text", "justification."]
lines = full_justify(words, 16)
print("|" + lines[0] + "|")             # -> |This    is    an|
print("|" + lines[1] + "|")             # -> |example  of text|
print("|" + lines[2] + "|")             # -> |justification.  |
lines = full_justify(["What", "must", "be", "acknowledgment", "shall"], 16)
print("|" + lines[1] + "|")             # -> |acknowledgment  |
```

```{=latex}
\clearpage
```

## 123. String Compression {#a123}

```{=latex}
\markright{123. String Compression}
```

[Run-Length Encoding with Read and Write Pointers · Strings · Tier 3 · python/123\_string\_compression.py]{.meta}

Compress a list of characters in place: each run of one repeated character becomes the character, then the run length if it is more than 1, one digit per cell; return the new length: \["a", "a", "b", "b", "c", "c", "c"\] → 6, with \["a", "2", "b", "2", "c", "3"\].

```python
# --- algorithm ---
def compress(chars):
    """Read walks over each run, write lays down char + count digits.
    O(n) time, O(1) extra space."""
    write = 0
    read = 0
    while read < len(chars):
        ch = chars[read]
        start = read
        while read < len(chars) and chars[read] == ch:
            read += 1                   # walk to the end of the run
        chars[write] = ch
        write += 1
        count = read - start
        if count > 1:
            for digit in str(count):    # 12 is written as "1", "2"
                chars[write] = digit
                write += 1
    return write


# --- try it ---
chars = ["a", "a", "b", "b", "c", "c", "c"]
length = compress(chars)
print(length, chars[0:length])          # -> 6 ['a', '2', 'b', '2', 'c', '3']
chars = list("abbbbbbbbbbbb")
length = compress(chars)
print(length, chars[0:length])          # -> 4 ['a', 'b', '1', '2']
print(compress(["a"]), compress(list("abc")))   # -> 1 3
```

```{=latex}
\clearpage
```

## 124. Reverse Words in a String {#a124}

```{=latex}
\markright{124. Reverse Words in a String}
```

[Reverse All, Then Reverse Each Word · Strings · Tier 3 · python/124\_reverse\_words.py]{.meta}

Reverse the order of the words in a string. Words are separated by one or more spaces; the result uses single spaces and has none at either end: " the sky is blue " → "blue is sky the".

```python
# --- algorithm ---
def reverse_words(s):
    """Squeeze the spaces, reverse the whole array, then reverse each word.
    O(n) time; O(1) extra space on a mutable character array."""
    chars = list(s)                     # Python strings are immutable
    length = squeeze_spaces(chars)      # the words fill chars[0..length-1]
    reverse(chars, 0, length - 1)       # order flipped, letters backwards
    start = 0
    for i in range(length + 1):
        if i == length or chars[i] == " ":  # a word ends just before i
            reverse(chars, start, i - 1)    # spell it forwards again
            start = i + 1
    return "".join(chars[0:length])


def squeeze_spaces(chars):
    """Copy the words to the front, one space between them. O(n)."""
    write = 0
    for read in range(len(chars)):
        if chars[read] != " ":
            chars[write] = chars[read]
            write += 1
        elif write > 0 and chars[write - 1] != " ":
            chars[write] = " "          # keep one space after a word
            write += 1
    if write > 0 and chars[write - 1] == " ":
        write -= 1                      # drop the trailing space
    return write


def reverse(chars, i, j):
    """Reverse chars[i..j] in place, swapping the ends inward. O(j - i)."""
    while i < j:
        chars[i], chars[j] = chars[j], chars[i]
        i += 1
        j -= 1


# --- try it ---
print(reverse_words("  the sky   is blue "))   # -> blue is sky the
print(reverse_words("a good   example"))       # -> example good a
print(reverse_words("hello"))                  # -> hello
print(repr(reverse_words("    ")))             # -> ''
```

```{=latex}
\clearpage
```

## 125. Multiply Strings {#a125}

```{=latex}
\markright{125. Multiply Strings}
```

[Grade-School Multiplication into a Digit Array · Strings · Tier 3 · python/125\_multiply\_strings.py]{.meta}

Multiply two non-negative integers given as decimal strings (no leading zeros) and return the product as a string, without converting the whole inputs to numbers: "123", "456" → "56088".

```python
# --- algorithm ---
def multiply(num1, num2):
    """Each digit pair adds its product into slot i + j + 1 of an m + n
    digit array, carrying left. O(m * n) time, O(m + n) space."""
    if num1 == "0" or num2 == "0":
        return "0"
    m = len(num1)
    n = len(num2)
    digits = [0] * (m + n)              # the product has at most m + n digits
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            product = int(num1[i]) * int(num2[j])   # one digit times one digit
            total = digits[i + j + 1] + product
            digits[i + j + 1] = total % 10          # keep the ones digit
            digits[i + j] += total // 10            # carry one slot left
    start = 0
    if digits[0] == 0:                  # only m + n - 1 digits were needed
        start = 1
    result = []
    for k in range(start, m + n):
        result.append(str(digits[k]))
    return "".join(result)


# --- try it ---
print(multiply("123", "456"))           # -> 56088
print(multiply("2", "3"))               # -> 6
print(multiply("99", "99"))             # -> 9801
print(multiply("12345", "0"))           # -> 0
```

```{=latex}
\clearpage
```

## 126. Spiral Matrix {#a126}

```{=latex}
\markright{126. Spiral Matrix}
```

[Walk the Boundary, Then Shrink It · Matrix · Tier 3 · python/126\_spiral\_matrix.py]{.meta}

Given an m x n matrix, return all of its elements in clockwise spiral order, starting at the top-left corner and moving right: rows \[1, 2, 3, 4\], \[5, 6, 7, 8\], \[9, 10, 11, 12\] → \[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7\].

```python
# --- algorithm ---
def spiral_order(matrix):
    """Read the four sides of the outer ring, shrinking a bound after each
    side. O(m * n) time, O(1) extra space besides the output."""
    result = []
    if len(matrix) == 0:
        return result
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for col in range(left, right + 1):          # top row, left to right
            result.append(matrix[top][col])
        top += 1
        for row in range(top, bottom + 1):          # right column, downward
            result.append(matrix[row][right])
        right -= 1
        if top <= bottom:                           # a bottom row is unread
            for col in range(right, left - 1, -1):  # bottom row, leftward
                result.append(matrix[bottom][col])
            bottom -= 1
        if left <= right:                           # a left column is unread
            for row in range(bottom, top - 1, -1):  # left column, upward
                result.append(matrix[row][left])
            left += 1
    return result


# --- try it ---
matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(spiral_order(matrix))     # -> [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
square = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(spiral_order(square))     # -> [1, 2, 3, 6, 9, 8, 7, 4, 5]
print(spiral_order([[1, 2, 3]]))            # -> [1, 2, 3]
print(spiral_order([[1], [2], [3]]))        # -> [1, 2, 3]
print(spiral_order([]))                     # -> []
```

```{=latex}
\clearpage
```

## 127. Rotate Image {#a127}

```{=latex}
\markright{127. Rotate Image}
```

[Transpose, Then Reverse Each Row · Matrix · Tier 3 · python/127\_rotate\_image.py]{.meta}

Rotate an n x n matrix by 90 degrees clockwise in place, without allocating a second matrix: \[\[1, 2, 3\], \[4, 5, 6\], \[7, 8, 9\]\] → \[\[7, 4, 1\], \[8, 5, 2\], \[9, 6, 3\]\].

```python
# --- algorithm ---
def rotate(matrix):
    """Transpose, then reverse each row: the cell (r, c) lands on
    (c, n - 1 - r). O(n^2) time, O(1) extra space."""
    n = len(matrix)
    for row in range(n):                    # transpose: mirror on the diagonal
        for col in range(row + 1, n):       # above the diagonal only
            temp = matrix[row][col]
            matrix[row][col] = matrix[col][row]
            matrix[col][row] = temp
    for row in range(n):
        reverse_row(matrix[row])            # mirror left to right


def reverse_row(cells):
    """Reverse one row in place, swapping its ends inward. O(n)."""
    left = 0
    right = len(cells) - 1
    while left < right:
        cells[left], cells[right] = cells[right], cells[left]
        left += 1
        right -= 1


# --- try it ---
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate(matrix)
print(matrix)                   # -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
square = [[1, 2], [3, 4]]
rotate(square)
print(square)                   # -> [[3, 1], [4, 2]]
big = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
rotate(big)
print(big[0], big[3])           # -> [15, 13, 2, 5] [16, 7, 10, 11]
for turn in range(3):
    rotate(big)                 # three more quarter turns make a full turn
print(big[0], big[3])           # -> [5, 1, 9, 11] [15, 14, 12, 16]
```

```{=latex}
\clearpage
```

## 128. GCD and LCM {#a128}

```{=latex}
\markright{128. GCD and LCM}
```

[Euclid's Algorithm · Math · Tier 3 · python/128\_gcd\_lcm.py]{.meta}

The greatest common divisor of two integers is the largest number dividing both; the least common multiple is the smallest positive number both divide: gcd(48, 18) → 6, lcm(48, 18) → 144.

```python
# --- algorithm ---
def gcd(a, b):
    """Euclid: (a, b) becomes (b, a mod b) until b is 0. O(log min(a, b))."""
    a = abs(a)
    b = abs(b)
    while b != 0:
        remainder = a % b               # every common divisor survives the mod
        a = b
        b = remainder
    return a                            # gcd(a, 0) = a


def lcm(a, b):
    """Divide by the gcd before multiplying. O(log min(a, b))."""
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)  # exact division first


def gcd_list(nums):
    """Fold gcd over the list from 0, since gcd(0, x) = x. O(n log max)."""
    result = 0
    for x in nums:
        result = gcd(result, x)
        if result == 1:
            break                       # it can never go below 1
    return result


# --- try it ---
print(gcd(48, 18))                      # -> 6
print(lcm(48, 18))                      # -> 144
print(gcd(7, 0))                        # -> 7
print(gcd_list([12, 18, 30]))           # -> 6
```

```{=latex}
\clearpage
```

## 129. Sieve of Eratosthenes {#a129}

```{=latex}
\markright{129. Sieve of Eratosthenes}
```

[Cross Out Multiples Starting at p squared · Math · Tier 3 · python/129\_sieve\_of\_eratosthenes.py]{.meta}

List every prime below n, and test a single number for primality: n = 30 → \[2, 3, 5, 7, 11, 13, 17, 19, 23, 29\]; 91 → not prime (7 \* 13).

```python
# --- algorithm ---
def sieve(n):
    """Primes below n: each surviving p crosses out p*p, p*p + p, ...
    O(n log log n) time, O(n) space."""
    crossed = [False] * n           # True once a smaller prime divides i
    p = 2
    while p * p < n:
        if not crossed[p]:          # p is prime: nothing crossed it out
            multiple = p * p        # below p * p: already crossed
            while multiple < n:
                crossed[multiple] = True
                multiple += p
        p += 1
    primes = []
    for i in range(2, n):
        if not crossed[i]:
            primes.append(i)
    return primes


def is_prime(n):
    """Trial division by 2, 3, 4, ... while d * d <= n. O(sqrt(n))."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:               # d and n / d: one is at most sqrt(n)
        if n % d == 0:
            return False
        d += 1
    return True


# --- try it ---
print(sieve(30))                # -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print(len(sieve(10)))           # -> 4
print(is_prime(91))             # -> False
print(is_prime(97))             # -> True
```

```{=latex}
\clearpage
```

## 130. Fast Exponentiation {#a130}

```{=latex}
\markright{130. Fast Exponentiation}
```

[Square and Multiply · Math · Tier 3 · python/130\_fast\_exponentiation.py]{.meta}

Compute x to the power n with O(log n) multiplications, for a negative n as well, and the same power modulo m: 3\^13 → 1594323, 2\^-2 → 0.25.

```python
# --- algorithm ---
def power(x, n):
    """Square x once per bit of n; multiply it in where the bit is 1.
    O(log |n|) multiplications."""
    if n < 0:
        x = 1 / x                       # x^-n = (1 / x)^n
        n = -n
    result = 1
    while n > 0:
        if n % 2 == 1:                  # lowest bit is 1: this square counts
            result = result * x
        x = x * x                       # x, x^2, x^4, x^8, ...
        n = n // 2                      # drop the lowest bit
    return result


def mod_power(x, n, m):
    """The same loop with every product reduced mod m. O(log n)."""
    result = 1 % m                      # 0 when m is 1
    x = x % m
    while n > 0:
        if n % 2 == 1:
            result = result * x % m
        x = x * x % m                   # numbers stay below m * m
        n = n // 2
    return result


# --- try it ---
print(power(3, 13))                     # -> 1594323
print(power(2, -2))                     # -> 0.25
print(power(7, 0))                      # -> 1
print(mod_power(3, 13, 1000))           # -> 323
print(mod_power(2, 100, 1000000007))    # -> 976371285
```

```{=latex}
\clearpage
```

## 131. Reservoir Sampling {#a131}

```{=latex}
\markright{131. Reservoir Sampling}
```

[Keep the i-th Item with Probability k / i · Math · Tier 3 · python/131\_reservoir\_sampling.py]{.meta}

Choose k items uniformly at random from a stream of unknown length, in one pass with O(k) memory, so that every item is kept with the same chance k / n: stream 10, 20, 30, 40, 50 with k = 2 → each item kept 2 / 5 of the time.

```python
import random                           # randint(a, b) includes both ends


# --- algorithm ---
def reservoir_sample(stream, k):
    """Keep the first k items; item i then replaces a random slot with
    probability k / i. O(n) time, O(k) space."""
    reservoir = []
    i = 0
    for item in stream:
        i += 1                          # item is the i-th seen (1-based)
        if i <= k:
            reservoir.append(item)      # fill phase
        else:
            j = random.randint(1, i)    # uniform over 1..i
            if j <= k:                  # chance k / i
                reservoir[j - 1] = item  # evict a uniform slot
    return reservoir


def is_uniform(stream, k, trials):
    """Each item should be kept about trials * k / n times. O(trials * n)."""
    counts = {}
    for t in range(trials):
        sample = reservoir_sample(stream, k)
        for item in sample:
            counts[item] = counts.get(item, 0) + 1
    expected = trials * k / len(stream)
    for item in stream:
        if abs(counts.get(item, 0) - expected) > 0.1 * expected:
            return False                # more than 10 percent off
    return True


# --- try it ---
random.seed(7)
print(len(reservoir_sample(range(1000), 10)))           # -> 10
print(reservoir_sample([7, 8, 9], 5))                   # -> [7, 8, 9]
print(is_uniform([10, 20, 30, 40, 50], 2, 20000))       # -> True
print(is_uniform([1, 2, 3, 4, 5, 6, 7, 8], 1, 20000))   # -> True
```

```{=latex}
\clearpage
```

## 132. Orientation and Segment Intersection {#a132}

```{=latex}
\markright{132. Orientation and Segment Intersection}
```

[The Cross Product Decides Left or Right · Geometry · Tier 3 · python/132\_orientation\_segment\_intersection.py]{.meta}

Decide whether the path o → a → b turns left, turns right or runs straight, and whether two segments share a point. Points are (x, y) integer pairs: segments (0, 0)-(4, 4) and (0, 4)-(4, 0) → True, they cross at (2, 2).

```python
# --- algorithm ---
def cross(o, a, b):
    """Cross product of o->a and o->b: > 0 left turn, < 0 right turn,
    0 straight. O(1)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p, q, r):
    """For r on the line pq: is r inside the box spanned by p and q? O(1)."""
    inside_x = min(p[0], q[0]) <= r[0] <= max(p[0], q[0])
    inside_y = min(p[1], q[1]) <= r[1] <= max(p[1], q[1])
    return inside_x and inside_y


def segments_intersect(p1, p2, q1, q2):
    """Each segment's ends lie on opposite sides of the other's line, or an
    end touches the other segment. O(1)."""
    d1 = cross(q1, q2, p1)              # side of p1 seen from q1 -> q2
    d2 = cross(q1, q2, p2)
    d3 = cross(p1, p2, q1)              # side of q1 seen from p1 -> p2
    d4 = cross(p1, p2, q2)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True                     # both pairs straddle: a clean crossing
    if d1 == 0 and on_segment(q1, q2, p1):
        return True                     # p1 lies on segment q1 q2
    if d2 == 0 and on_segment(q1, q2, p2):
        return True
    if d3 == 0 and on_segment(p1, p2, q1):
        return True
    if d4 == 0 and on_segment(p1, p2, q2):
        return True
    return False


# --- try it ---
print(cross((0, 0), (4, 0), (2, 3)))                        # -> 12
print(segments_intersect((0, 0), (4, 4), (0, 4), (4, 0)))   # -> True
print(segments_intersect((0, 0), (2, 2), (3, 3), (5, 5)))   # -> False
print(segments_intersect((0, 0), (4, 0), (2, 0), (2, 3)))   # -> True
print(segments_intersect((0, 0), (4, 0), (0, 1), (4, 2)))   # -> False
```

```{=latex}
\clearpage
```

## 133. Convex Hull {#a133}

```{=latex}
\markright{133. Convex Hull}
```

[Andrew's Monotone Chain · Geometry · Tier 3 · python/133\_convex\_hull.py]{.meta}

Return the corners of the smallest convex polygon containing every (x, y) point, counter-clockwise from the leftmost one (the lowest on a tie): (0, 0) (1, 3) (2, 1) (2, 2) (3, 2) (4, 0) (4, 4) → (0, 0) (4, 0) (4, 4) (1, 3)

```python
# --- algorithm ---
def cross(o, a, b):
    """> 0 when o -> a -> b turns left (counter-clockwise), as in #132. O(1)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def half_hull(pts):
    """One chain: a stack that keeps only left turns. O(n), since every
    point is pushed once and popped at most once."""
    chain = []                          # used as a stack: chain[-1] is the top
    for p in pts:
        while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
            chain.pop()                 # last turn is not counter-clockwise
        chain.append(p)
    return chain


def convex_hull(points):
    """Sort by (x, y); the lower chain runs left to right, the upper chain
    right to left. O(n log n) for the sort."""
    pts = sorted(set(points))           # by x, then y; duplicates dropped
    if len(pts) <= 2:
        return pts
    lower = half_hull(pts)
    upper = half_hull(pts[::-1])
    return lower[:-1] + upper[:-1]      # each chain ends where the other starts


# --- try it ---
pts = [(0, 0), (1, 3), (2, 1), (2, 2), (3, 2), (4, 0), (4, 4)]
print(convex_hull(pts))                 # -> [(0, 0), (4, 0), (4, 4), (1, 3)]
print(convex_hull([(0, 0), (1, 1), (2, 2), (1, 1)]))    # -> [(0, 0), (2, 2)]
print(convex_hull([(5, 5)]))            # -> [(5, 5)]
square = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1), (1, 0)]
print(convex_hull(square))              # -> [(0, 0), (2, 0), (2, 2), (0, 2)]
```

```{=latex}
\clearpage
```

## 134. Max Points on a Line {#a134}

```{=latex}
\markright{134. Max Points on a Line}
```

[Slopes as Reduced Fractions · Geometry · Tier 3 · python/134\_max\_points\_on\_a\_line.py]{.meta}

Given distinct points with integer coordinates, return the largest number of them that lie on one straight line: (1, 1) (3, 2) (5, 3) (4, 1) (2, 3) (1, 4) → 4, the line x + y = 5.

```python
import math                             # gcd is Euclid's algorithm, #128


# --- algorithm ---
def slope_key(p, q):
    """Direction p -> q as a reduced fraction (dy, dx) with dx > 0;
    every vertical pair gets (1, 0). O(log C) for the gcd."""
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    if dx == 0:
        return (1, 0)                   # vertical line
    if dx < 0:
        dx = -dx                        # p -> q and q -> p: the same line
        dy = -dy
    g = math.gcd(dy, dx)                # positive, since dx > 0
    return (dy // g, dx // g)           # exact divisions


def max_points(points):
    """Anchor each point and group the later points by slope; the biggest
    group plus the anchor is a line. O(n^2) slopes."""
    n = len(points)
    if n <= 2:
        return n
    best = 0
    for i in range(n):
        counts = {}                     # slope key -> points on that line
        for j in range(i + 1, n):
            key = slope_key(points[i], points[j])
            counts[key] = counts.get(key, 0) + 1
            if counts[key] + 1 > best:
                best = counts[key] + 1  # + 1 for the anchor itself
    return best


# --- try it ---
pts = [(1, 1), (3, 2), (5, 3), (4, 1), (2, 3), (1, 4)]
print(max_points(pts))                          # -> 4
print(max_points([(1, 1), (2, 2), (3, 3)]))     # -> 3
print(max_points([(0, 0), (0, 5), (0, -2), (3, 1)]))  # -> 3
print(slope_key((3, 2), (1, 4)))                # -> (-1, 1)
```

```{=latex}
\clearpage
```

## 135. Single Number {#a135}

```{=latex}
\markright{135. Single Number}
```

[XOR Cancels Pairs · Bit Manipulation · Tier 3 · python/135\_single\_number\_xor.py]{.meta}

Every element of a non-empty array appears twice except one, which appears once; find it in O(n) time and O(1) extra space: \[4, 1, 2, 1, 2\] → 4.

```python
# --- algorithm ---
def single_number(nums):
    """XOR everything: each pair cancels to 0, the single survives. O(n)."""
    result = 0
    for value in nums:
        result ^= value                 # x ^ x = 0 and x ^ 0 = x
    return result


def missing_number(nums):
    """nums holds 0..n with one value missing; XOR indices and values. O(n)."""
    result = len(nums)                  # index n has no slot of its own
    for i in range(len(nums)):
        result ^= i                     # value v cancels against index v
        result ^= nums[i]
    return result


# --- try it ---
print(single_number([4, 1, 2, 1, 2]))     # -> 4
print(single_number([-3, 7, 7]))          # -> -3
print(missing_number([3, 0, 1]))          # -> 2
print(missing_number([0, 1]))             # -> 2
```

```{=latex}
\clearpage
```

## 136. Count Set Bits {#a136}

```{=latex}
\markright{136. Count Set Bits}
```

[Brian Kernighan's n & (n - 1) · Bit Manipulation · Tier 3 · python/136\_count\_set\_bits.py]{.meta}

Count the 1 bits in the binary form of a non-negative integer, test for a power of two, and count the 1 bits of every number from 0 to n: 44 = 101100 → 3 set bits.

```python
# --- algorithm ---
def count_set_bits(n):
    """Kernighan: n & (n - 1) clears the lowest set bit. O(set bits)."""
    count = 0
    while n > 0:
        n = n & (n - 1)                 # the lowest 1 becomes 0
        count += 1
    return count


def is_power_of_two(n):
    """A power of two has exactly one set bit. O(1)."""
    return n > 0 and (n & (n - 1)) == 0


def count_bits_up_to(n):
    """bits[i] = bits[i >> 1] + (i & 1) for every i in 0..n. O(n)."""
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)    # i >> 1 drops i's last bit
    return bits


# --- try it ---
print(count_set_bits(44))           # -> 3
print(count_set_bits(0))            # -> 0
print(is_power_of_two(64))          # -> True
print(is_power_of_two(0))           # -> False
print(count_bits_up_to(5))          # -> [0, 1, 1, 2, 1, 2]
```

```{=latex}
\clearpage
```

## 137. Bitmask Subset Enumeration {#a137}

```{=latex}
\markright{137. Bitmask Subset Enumeration}
```

[Every Integer from 0 to 2\^n - 1 Is a Subset · Bit Manipulation · Tier 3 · python/137\_bitmask\_subsets.py]{.meta}

List every subset of n distinct elements by counting in binary (bit j of the mask says whether element j is in), and list every submask of a mask: \[1, 2, 3\] → \[\[\], \[1\], \[2\], \[1, 2\], \[3\], \[1, 3\], \[2, 3\], \[1, 2, 3\]\].

```python
# --- algorithm ---
def subsets_by_mask(nums):
    """Mask m picks nums[j] when bit j of m is set. O(n * 2^n)."""
    n = len(nums)
    result = []
    for mask in range(1 << n):          # 1 << n is 2^n: one mask per subset
        subset = []
        for j in range(n):
            if (mask >> j) & 1:         # bit j is set: nums[j] is in
                subset.append(nums[j])
        result.append(subset)
    return result


def submasks(mask):
    """Every submask of mask, largest first. O(2^k) for k set bits."""
    result = []
    sub = mask
    while sub > 0:
        result.append(sub)
        sub = (sub - 1) & mask          # borrow, then keep only mask's bits
    result.append(0)                    # the empty submask ends the walk
    return result


# --- try it ---
result = subsets_by_mask([1, 2, 3])
print(result)   # -> [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
print(subsets_by_mask([]))              # -> [[]]
print(submasks(13))                     # -> [13, 12, 9, 8, 5, 4, 1, 0]
print(submasks(0))                      # -> [0]
```

```{=latex}
\clearpage
```

## 138. Rate Limiter {#a138}

```{=latex}
\markright{138. Rate Limiter}
```

[Token Bucket and Sliding Log · Design · Tier 3 · python/138\_rate\_limiter.py]{.meta}

Decide for each request at time t (in seconds) whether to let it through, so a client gets at most a fixed rate: with 3 requests per 6 seconds, requests at times 0, 0, 0, 0, 6 → allowed, allowed, allowed, rejected, allowed.

```python
from collections import deque      # popleft is O(1)


# --- helpers ---
def allowed_times(limiter, times):
    """Send one request at each time, in order; return the times let through."""
    allowed = []
    for t in times:
        if limiter.allow(t):
            allowed.append(t)
    return allowed


# --- algorithm ---
class TokenBucket:
    """Up to capacity tokens, refilled at rate per second; a request spends
    one. O(1) time per request and O(1) memory."""

    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate                # tokens added per second
        self.tokens = capacity          # start full: a burst may pass
        self.last = 0                   # time of the last refill

    def allow(self, t):
        """Refill for the time since the last call, then spend a token. O(1)."""
        refill = (t - self.last) * self.rate    # earned since the last call
        self.tokens = min(self.capacity, self.tokens + refill)
        self.last = t
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class SlidingLog:
    """The times of the requests allowed in the last window seconds.
    O(1) amortized time per request, O(limit) memory."""

    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.log = deque()              # allowed times, oldest first

    def allow(self, t):
        """Drop expired times; allow if under the limit. O(1) amortized."""
        while len(self.log) > 0 and self.log[0] <= t - self.window:
            self.log.popleft()          # older than the window: expired
        if len(self.log) < self.limit:
            self.log.append(t)
            return True
        return False


# --- try it ---
times = [0, 0, 0, 0, 1, 2, 4, 6, 6, 7]
print(allowed_times(TokenBucket(3, 0.5), times))  # -> [0, 0, 0, 2, 4, 6]
print(allowed_times(SlidingLog(3, 6), times))     # -> [0, 0, 0, 6, 6, 7]
print(allowed_times(SlidingLog(1, 10), [1, 3, 10, 11]))   # -> [1, 11]
```

```{=latex}
\clearpage
```

## 139. Consistent Hashing {#a139}

```{=latex}
\markright{139. Consistent Hashing}
```

[A Hash Ring with Virtual Nodes · Design · Tier 3 · python/139\_consistent\_hashing.py]{.meta}

Place keys on servers so that adding or removing a server moves few keys: servers and keys hash to points on a ring, and a key belongs to the first server point clockwise from it. 1000 keys, a 4th server joins 3 → 235 keys move, all to the new server (hash mod n would move 738).

```python
# --- algorithm ---
RING = 2 ** 32                          # ring positions are 0 .. 2^32 - 1


def ring_hash(text):
    """FNV-1a, then MurmurHash3's finalizer: a 32-bit position that is the
    same in every run (Python's hash() of a string is not). O(len(text))."""
    h = 2166136261                      # FNV-1a offset basis
    for ch in text:
        h = h ^ ord(ch)
        h = (h * 16777619) % RING       # FNV prime, keep 32 bits
    h = h ^ (h >> 16)                   # avalanche: names one letter apart
    h = (h * 2246822507) % RING         # end up far apart on the ring
    h = h ^ (h >> 13)
    h = (h * 3266489909) % RING
    h = h ^ (h >> 16)
    return h


class HashRing:
    """Sorted (position, server) points, several per server; a key belongs
    to the first point clockwise from its hash. Lookup O(log(n * v))."""

    def __init__(self, replicas):
        self.replicas = replicas        # virtual nodes per server
        self.points = []                # (position, server), sorted

    def lower_bound(self, position):
        """First index whose point is at or after position. O(log(n * v))."""
        lo = 0
        hi = len(self.points)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.points[mid][0] < position:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def add_server(self, server):
        """Insert v points, keeping the list sorted. O(v * n * v): each
        insert shifts the list."""
        for i in range(self.replicas):
            position = ring_hash(server + "#" + str(i))
            index = self.lower_bound(position)
            self.points.insert(index, (position, server))

    def remove_server(self, server):
        """Drop every point of the server; its arcs pass clockwise. O(n * v)."""
        kept = []
        for point in self.points:
            if point[1] != server:
                kept.append(point)
        self.points = kept

    def get_server(self, key):
        """The first point clockwise from the key's hash. O(log(n * v))."""
        if len(self.points) == 0:
            return None
        index = self.lower_bound(ring_hash(key))
        if index == len(self.points):
            index = 0                   # past the last point: wrap to the first
        return self.points[index][1]


def ring_owners(ring, keys):
    """The server of every key on the ring, in key order. O(k log(n * v))."""
    owners = []
    for key in keys:
        owners.append(ring.get_server(key))
    return owners


def mod_n_owners(keys, servers):
    """The naive placement to compare: server number hash mod n. O(k)."""
    owners = []
    for key in keys:
        owners.append(servers[ring_hash(key) % len(servers)])
    return owners


def count_moved(before, after):
    """How many keys changed server between two placements. O(k)."""
    moved = 0
    for i in range(len(before)):
        if before[i] != after[i]:
            moved += 1
    return moved


# --- try it ---
keys = []
for i in range(1000):
    keys.append("key" + str(i))
ring = HashRing(100)
ring.add_server("A")
ring.add_server("B")
ring.add_server("C")
before = ring_owners(ring, keys)
ring.add_server("D")
after = ring_owners(ring, keys)
print(count_moved(before, after), after.count("D"))    # -> 235 235
old_mod = mod_n_owners(keys, ["A", "B", "C"])
new_mod = mod_n_owners(keys, ["A", "B", "C", "D"])
print(count_moved(old_mod, new_mod))                   # -> 738
ring.remove_server("D")
print(ring_owners(ring, keys) == before)               # -> True
print(len(ring.points), ring.get_server("key7"))       # -> 300 A
print(HashRing(3).get_server("key7"))                  # -> None
```

```{=latex}
\clearpage
```

## 140. Stock Price Tracker {#a140}

```{=latex}
\markright{140. Stock Price Tracker}
```

[Hash Map + Heaps with Lazy Deletion · Design · Tier 3 · python/140\_stock\_price\_tracker.py]{.meta}

Prices arrive as (timestamp, price) records, and a later record may correct an earlier timestamp; report the latest price and the maximum and minimum of the current prices. update(1, 10), update(2, 5), update(1, 3) → current 5, maximum 5, minimum 3.

```python
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class StockPrice:
    """Map timestamp -> price, plus a max-heap and a min-heap of records
    whose stale tops are discarded lazily. Amortized O(log n) per call."""

    def __init__(self):
        self.prices = {}            # timestamp -> its current price
        self.latest = 0             # the largest timestamp seen so far
        self.max_heap = []          # (-price, timestamp): highest on top
        self.min_heap = []          # (price, timestamp): lowest on top

    def update(self, timestamp, price):
        """Record or correct one price; older records go stale. O(log n)."""
        self.prices[timestamp] = price
        if timestamp > self.latest:
            self.latest = timestamp
        heapq.heappush(self.max_heap, (-price, timestamp))
        heapq.heappush(self.min_heap, (price, timestamp))

    def current(self):
        """The price at the latest timestamp. O(1)."""
        return self.prices[self.latest]

    def maximum(self):
        """Pop stale tops until the top agrees with the map. Amortized
        O(log n)."""
        while True:
            price = -self.max_heap[0][0]
            timestamp = self.max_heap[0][1]
            if self.prices[timestamp] == price:
                return price                # the record is still true
            heapq.heappop(self.max_heap)    # stale: corrected since

    def minimum(self):
        """The mirror image of maximum on the min-heap. Amortized O(log n)."""
        while True:
            price = self.min_heap[0][0]
            timestamp = self.min_heap[0][1]
            if self.prices[timestamp] == price:
                return price
            heapq.heappop(self.min_heap)


# --- try it ---
tracker = StockPrice()
tracker.update(1, 10)
tracker.update(2, 5)
print(tracker.current(), tracker.maximum())     # -> 5 10
tracker.update(1, 3)                            # time 1 was wrong: now 3
print(tracker.maximum(), tracker.minimum())     # -> 5 3
tracker.update(4, 2)
print(tracker.current(), tracker.minimum())     # -> 2 2
print(len(tracker.max_heap), len(tracker.min_heap))     # -> 3 4
```

```{=latex}
\clearpage
```

## 141. All O(1) Data Structure {#a141}

```{=latex}
\markright{141. All O(1) Data Structure}
```

[A Linked List of Count Buckets · Design · Tier 3 · python/141\_all\_o1\_data\_structure.py]{.meta}

Count string keys: inc(key) adds one, dec(key) subtracts one (a key at 0 disappears), and get\_max\_key() and get\_min\_key() return a key with the largest or smallest count, or "" when empty, all in O(1). inc hello twice, inc leet: get\_max\_key() → hello, get\_min\_key() → leet.

```python
# --- helpers ---
class Bucket:
    def __init__(self, count):
        self.count = count
        self.keys = set()               # every key with exactly this count
        self.prev = None
        self.next = None


def any_key(keys):
    """Some key of a non-empty set: the first one a loop meets. O(1)."""
    for key in keys:
        return key


def bucket_list(counter):
    """The buckets from head to tail as [count, sorted keys] pairs."""
    result = []
    bucket = counter.head.next
    while bucket is not counter.tail:
        result.append([bucket.count, sorted(bucket.keys)])
        bucket = bucket.next
    return result


# --- algorithm ---
class AllOne:
    """Buckets of keys in increasing count between two sentinels, plus
    key -> bucket. Every operation is O(1)."""

    def __init__(self):
        self.head = Bucket(0)           # sentinel before the smallest count
        self.tail = Bucket(0)           # sentinel after the largest count
        self.head.next = self.tail
        self.tail.prev = self.head
        self.bucket_of = {}             # key -> the bucket that holds it

    def insert_after(self, bucket, count):
        """Splice a new empty bucket for count right after bucket. O(1)."""
        fresh = Bucket(count)
        fresh.prev = bucket
        fresh.next = bucket.next
        bucket.next.prev = fresh
        bucket.next = fresh
        return fresh

    def remove_key(self, bucket, key):
        """Take key out of bucket; unlink the bucket once it is empty. O(1)."""
        bucket.keys.remove(key)
        if len(bucket.keys) == 0:       # empty: unlink the bucket
            bucket.prev.next = bucket.next
            bucket.next.prev = bucket.prev

    def inc(self, key):
        """Move key to the count + 1 bucket just after its own. O(1)."""
        if key in self.bucket_of:
            current = self.bucket_of[key]
        else:
            current = self.head         # a new key comes from count 0
        target = current.next
        if target is self.tail or target.count != current.count + 1:
            target = self.insert_after(current, current.count + 1)
        target.keys.add(key)
        self.bucket_of[key] = target
        if current is not self.head:
            self.remove_key(current, key)   # only after target is linked

    def dec(self, key):
        """Move key to the count - 1 bucket just before its own; at count 0
        the key is gone. O(1)."""
        if key not in self.bucket_of:
            return
        current = self.bucket_of[key]
        if current.count == 1:
            del self.bucket_of[key]     # count 0: the key disappears
        else:
            target = current.prev
            if target is self.head or target.count != current.count - 1:
                target = self.insert_after(current.prev, current.count - 1)
            target.keys.add(key)
            self.bucket_of[key] = target
        self.remove_key(current, key)

    def get_max_key(self):
        """A key of the last bucket, before tail; "" when empty. O(1)."""
        if self.tail.prev is self.head:
            return ""
        return any_key(self.tail.prev.keys)

    def get_min_key(self):
        """A key of the first bucket, after head; "" when empty. O(1)."""
        if self.head.next is self.tail:
            return ""
        return any_key(self.head.next.keys)


# --- try it ---
counter = AllOne()
counter.inc("hello")
counter.inc("hello")
print(counter.get_max_key(), counter.get_min_key())     # -> hello hello
counter.inc("leet")
print(counter.get_max_key(), counter.get_min_key())     # -> hello leet
print(bucket_list(counter))         # -> [[1, ['leet']], [2, ['hello']]]
counter.inc("leet")
print(bucket_list(counter))         # -> [[2, ['hello', 'leet']]]
counter.dec("hello")
print(counter.get_max_key(), counter.get_min_key())     # -> leet hello
counter.dec("hello")                # count 0: hello disappears
counter.dec("leet")
print(bucket_list(counter), counter.get_max_key())  # -> [[1, ['leet']]] leet
counter.dec("leet")
print(repr(counter.get_max_key()), repr(counter.get_min_key()))   # -> '' ''
```

```{=latex}
\clearpage
```

## 142. Range Module {#a142}

```{=latex}
\markright{142. Range Module}
```

[A Sorted List of Disjoint Intervals · Design · Tier 3 · python/142\_range\_module.py]{.meta}

Track half-open ranges \[left, right), left \< right: add\_range marks a range, remove\_range unmarks it and query\_range asks whether all of \[left, right) is tracked. add\_range(10, 20), remove\_range(14, 16), then query\_range(10, 14), query\_range(13, 15), query\_range(16, 17) → True, False, True.

```python
# --- algorithm ---
class RangeModule:
    """Sorted, disjoint, non-touching [start, end) pairs. Updates O(n),
    queries O(log n)."""

    def __init__(self):
        self.intervals = []         # sorted [start, end), gaps between

    def add_range(self, left, right):
        """Copy the intervals before, absorb every one that overlaps or
        touches [left, right), copy the rest. O(n)."""
        merged = []
        i = 0
        n = len(self.intervals)
        while i < n and self.intervals[i][1] < left:    # ends before: keep
            merged.append(self.intervals[i])
            i += 1
        while i < n and self.intervals[i][0] <= right:  # overlaps or touches
            left = min(left, self.intervals[i][0])
            right = max(right, self.intervals[i][1])
            i += 1
        merged.append([left, right])
        while i < n:                                    # starts after: keep
            merged.append(self.intervals[i])
            i += 1
        self.intervals = merged

    def remove_range(self, left, right):
        """Keep what lies outside [left, right); a cut interval leaves one
        or two pieces. O(n)."""
        kept = []
        for start, end in self.intervals:
            if end <= left or start >= right:
                kept.append([start, end])       # no overlap: untouched
            else:
                if start < left:
                    kept.append([start, left])  # the piece on the left
                if end > right:
                    kept.append([right, end])   # the piece on the right
        self.intervals = kept

    def query_range(self, left, right):
        """Find the last interval starting at or before left; it must reach
        right. O(log n)."""
        lo = 0
        hi = len(self.intervals)
        while lo < hi:                  # first interval starting after left
            mid = (lo + hi) // 2
            if self.intervals[mid][0] <= left:
                lo = mid + 1
            else:
                hi = mid
        if lo == 0:
            return False                # every interval starts after left
        return self.intervals[lo - 1][1] >= right


# --- try it ---
module = RangeModule()
module.add_range(10, 20)
module.remove_range(14, 16)
print(module.intervals)                             # -> [[10, 14], [16, 20]]
print(module.query_range(10, 14), module.query_range(13, 15))  # -> True False
print(module.query_range(16, 17))                   # -> True
module.add_range(14, 16)            # touches both pieces: one block again
print(module.intervals, module.query_range(10, 20))  # -> [[10, 20]] True
module.add_range(25, 30)
module.add_range(5, 8)
print(module.intervals)             # -> [[5, 8], [10, 20], [25, 30]]
print(module.query_range(8, 10), module.query_range(26, 29))  # -> False True
```

```{=latex}
\clearpage
```

## 143. In-Memory File System {#a143}

```{=latex}
\markright{143. In-Memory File System}
```

[A Trie of Path Components · Design · Tier 3 · python/143\_in\_memory\_file\_system.py]{.meta}

Support ls(path), mkdir(path), add\_content\_to\_file(path, content) and read\_content\_from\_file(path) on absolute paths like "/a/b/c". After mkdir("/a/b/c") and add\_content\_to\_file("/a/b/c/d", "hello"): ls("/") → \["a"\], ls("/a/b/c/d") → \["d"\], read "/a/b/c/d" → "hello".

```python
# --- helpers ---
class FileNode:
    def __init__(self):
        self.children = {}          # name -> FileNode
        self.is_file = False
        self.content = ""


def split_path(path):
    """'/a/b/c' -> ['a', 'b', 'c']: split on '/', skip empty parts. O(len)."""
    names = []
    for part in path.split("/"):
        if part != "":              # '/' at the start or end leaves ''
            names.append(part)
    return names


# --- algorithm ---
class FileSystem:
    """One node per directory or file; children are keyed by name.
    O(path length) per call, plus sorting the names for ls."""

    def __init__(self):
        self.root = FileNode()

    def walk(self, path, create):
        """Follow the names from the root; make missing nodes if create,
        else return None. O(path length)."""
        node = self.root
        for name in split_path(path):
            if name not in node.children:
                if not create:
                    return None         # the path does not exist
                node.children[name] = FileNode()
            node = node.children[name]
        return node

    def ls(self, path):
        """A file lists its own name, a directory its sorted children.
        O(path length + k log k) for k children."""
        node = self.walk(path, False)
        if node is None:
            return []
        if node.is_file:
            names = split_path(path)
            return [names[-1]]          # the last name in the path
        return sorted(node.children)    # the child names, in order

    def mkdir(self, path):
        """Create every missing directory on the path. O(path length)."""
        self.walk(path, True)

    def add_content_to_file(self, path, content):
        """Create the file (and its directories) if needed, then append.
        O(path length + file length): the string is copied."""
        node = self.walk(path, True)
        node.is_file = True
        node.content = node.content + content

    def read_content_from_file(self, path):
        """The file's content, or "" if there is no such file.
        O(path length)."""
        node = self.walk(path, False)
        if node is None:
            return ""
        return node.content


# --- try it ---
fs = FileSystem()
print(fs.ls("/"))                                   # -> []
fs.mkdir("/a/b/c")
fs.add_content_to_file("/a/b/c/d", "hello")
print(fs.ls("/"), fs.ls("/a/b/c"), fs.ls("/a/b/c/d"))   # -> ['a'] ['d'] ['d']
fs.add_content_to_file("/a/b/c/d", " world")        # appends
print(fs.read_content_from_file("/a/b/c/d"))        # -> hello world
fs.mkdir("/a/b/apps")
fs.add_content_to_file("/a/notes", "todo")
print(fs.ls("/a/b"), fs.ls("/a"))       # -> ['apps', 'c'] ['b', 'notes']
```

```{=latex}
\clearpage
```

## 144. Design a Text Editor {#a144}

```{=latex}
\markright{144. Design a Text Editor}
```

[Two Stacks Around the Cursor · Design · Tier 3 · python/144\_text\_editor.py]{.meta}

Edit text at a cursor: add\_text(text) types there, delete\_text(k) backspaces up to k characters and returns how many went, cursor\_left(k) / cursor\_right(k) move it and return the last min(10, len) characters to its left. Add "leetcode", delete\_text(4) → 4, add "practice", cursor\_left(8) → "leet".

```python
# --- algorithm ---
class TextEditor:
    """Characters left of the cursor on one stack, characters right of it on
    another, nearest on top of both. O(k) per call."""

    def __init__(self):
        self.left = []              # text before the cursor, top = nearest
        self.right = []             # text after the cursor, reversed

    def add_text(self, text):
        """Type at the cursor: push every character onto left. O(len(text))."""
        for ch in text:
            self.left.append(ch)

    def delete_text(self, k):
        """Backspace up to k times; return how many were deleted. O(k)."""
        deleted = 0
        while deleted < k and len(self.left) > 0:
            self.left.pop()
            deleted += 1
        return deleted

    def cursor_left(self, k):
        """Move up to k characters from left to right. O(k)."""
        while k > 0 and len(self.left) > 0:
            ch = self.left.pop()
            self.right.append(ch)       # it is now just after the cursor
            k -= 1
        return self.last_ten()

    def cursor_right(self, k):
        """Move up to k characters from right back to left. O(k)."""
        while k > 0 and len(self.right) > 0:
            ch = self.right.pop()
            self.left.append(ch)        # it is now just before the cursor
            k -= 1
        return self.last_ten()

    def last_ten(self):
        """The last min(10, len(left)) characters before the cursor. O(1)."""
        start = max(0, len(self.left) - 10)
        return "".join(self.left[start:])


# --- try it ---
editor = TextEditor()
editor.add_text("leetcode")
print(editor.delete_text(4))                # -> 4
editor.add_text("practice")
print(editor.cursor_right(3))               # -> etpractice
print(editor.cursor_left(8))                # -> leet
print(editor.delete_text(10))               # -> 4
print(repr(editor.cursor_left(2)))          # -> ''
print(editor.cursor_right(6), editor.right)  # -> practi ['e', 'c']
```

```{=latex}
\clearpage
```

## 145. Unique ID Generator {#a145}

```{=latex}
\markright{145. Unique ID Generator}
```

[Snowflake: Time, Machine and Sequence Bits · Design · Tier 3 · python/145\_snowflake\_id.py]{.meta}

Hand out 64-bit ids, unique across machines and roughly sorted by time, with no coordination: 41 bits of milliseconds since a custom epoch, 10 bits of machine id, 12 bits of sequence. Machine 5, two ids in millisecond 1000 after the epoch, one in 1001 → 4194324480, 4194324481, 4198518784.

```python
# --- algorithm ---
SEQUENCE_BITS = 12                          # 4096 ids per millisecond
MACHINE_BITS = 10                           # 1024 machines
TIME_SHIFT = SEQUENCE_BITS + MACHINE_BITS   # time starts at bit 22
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1     # 4095: twelve 1 bits
MAX_MACHINE = (1 << MACHINE_BITS) - 1       # 1023: ten 1 bits


class SnowflakeGenerator:
    """Time | machine | sequence packed into one integer. O(1) per id."""

    def __init__(self, machine_id, epoch_ms):
        self.machine_id = machine_id    # 0..1023, different on every machine
        self.epoch_ms = epoch_ms        # custom epoch: time 0 for these ids
        self.last_clock = -1            # the latest time a caller passed
        self.last_ms = -1               # the millisecond in the latest id
        self.sequence = 0               # the latest id's number in last_ms

    def next_id(self, now_ms):
        """New millisecond: sequence 0; same one: sequence + 1, borrowing
        the next millisecond after 4096 ids. O(1)."""
        if now_ms < self.last_clock:
            raise ValueError("clock moved backwards")
        self.last_clock = now_ms
        if now_ms > self.last_ms:
            self.last_ms = now_ms       # a new millisecond: restart at 0
            self.sequence = 0
        else:
            self.sequence += 1          # the same millisecond: next number
            if self.sequence > MAX_SEQUENCE:
                self.last_ms += 1       # 4096 ids used: move to the next ms
                self.sequence = 0
        elapsed = self.last_ms - self.epoch_ms
        time_part = elapsed << TIME_SHIFT                   # bits 22..62
        machine_part = self.machine_id << SEQUENCE_BITS     # bits 12..21
        return time_part | machine_part | self.sequence     # bits 0..11


def decode_id(snowflake_id):
    """Shift and mask the three fields back out: [ms since the epoch,
    machine, sequence]. O(1)."""
    sequence = snowflake_id & MAX_SEQUENCE                  # low 12 bits
    machine_id = (snowflake_id >> SEQUENCE_BITS) & MAX_MACHINE
    elapsed = snowflake_id >> TIME_SHIFT                    # the rest
    return [elapsed, machine_id, sequence]


# --- try it ---
EPOCH_MS = 1700000000000            # 2023-11-14 22:13:20 UTC
gen = SnowflakeGenerator(5, EPOCH_MS)
first = gen.next_id(EPOCH_MS + 1000)
second = gen.next_id(EPOCH_MS + 1000)       # same millisecond: sequence 1
third = gen.next_id(EPOCH_MS + 1001)        # new millisecond: sequence 0
print(first, second, third)         # -> 4194324480 4194324481 4198518784
print(decode_id(second), decode_id(third))  # -> [1000, 5, 1] [1001, 5, 0]
burst = SnowflakeGenerator(7, EPOCH_MS)
for i in range(4097):               # one more id than a millisecond holds
    last = burst.next_id(EPOCH_MS + 50)
print(decode_id(last))              # -> [51, 7, 0]
try:
    gen.next_id(EPOCH_MS + 999)     # earlier than the last call
except ValueError as error:
    print(error)                    # -> clock moved backwards
```

```{=latex}
\clearpage
```

## 146. Bloom Filter {#a146}

```{=latex}
\markright{146. Bloom Filter}
```

[k Hash Functions into One Bit Array · Design · Tier 3 · python/146\_bloom\_filter.py]{.meta}

Remember a set in m bits: add(item) sets k bits and might\_contain(item) checks them, so False is always right and True is probably right. With 19 bits and 3 hashes, add cat, dog and fish → might\_contain("owl") is False and might\_contain("colt") is True, a false positive.

```python
import math                         # exp for the error formula
import random                       # random words to measure the error


# --- algorithm ---
MOD = 1000000007                    # a large prime, as in Rabin-Karp


def string_hash(word, base):
    """The word read as a number in the given base, mod MOD. O(len(word))."""
    h = 0
    for ch in word:
        h = (h * base + ord(ch)) % MOD
    return h


class BloomFilter:
    """m bits and k probes per item; bits are set and never cleared."""

    def __init__(self, m, k):
        self.m = m                  # number of bits, best a prime
        self.k = k                  # number of hash functions
        self.bits = [0] * m

    def positions(self, item):
        """The item's k bits, (h1 + i * step) mod m for i = 0..k-1. O(L + k)."""
        h1 = string_hash(item, 31)
        h2 = string_hash(item, 37)          # a second, different hash
        step = 1 + h2 % (self.m - 1)        # 1..m-1: the probes always move
        result = []
        for i in range(self.k):
            result.append((h1 + i * step) % self.m)
        return result

    def add(self, item):
        """Set the item's k bits to 1. O(L + k)."""
        for p in self.positions(item):
            self.bits[p] = 1

    def might_contain(self, item):
        """False: never added. True: added, or a false positive. O(L + k)."""
        for p in self.positions(item):
            if self.bits[p] == 0:
                return False                # adding it would have set this bit
        return True                         # added, or a false positive


def expected_rate(m, n, k):
    """False-positive rate after n adds, (1 - e^(-k n / m))^k. O(1)."""
    return (1 - math.exp(-k * n / m)) ** k


def random_word(length):
    """Random lowercase letters; seed random to repeat a run. O(length)."""
    word = ""
    for i in range(length):
        word += chr(ord("a") + random.randint(0, 25))
    return word


def measured_rate(m, k, n, trials):
    """Add n random words, then return the share of trials fresh random words
    the filter wrongly reports as present. O((n + trials) * (L + k))."""
    bloom = BloomFilter(m, k)
    added = set()
    for i in range(n):
        word = random_word(8)
        bloom.add(word)
        added.add(word)
    false_positives = 0
    tested = 0
    for i in range(trials):
        word = random_word(8)
        if word not in added:               # only never-added words count
            tested += 1
            if bloom.might_contain(word):
                false_positives += 1
    return false_positives / tested


# --- try it ---
bloom = BloomFilter(19, 3)                  # 19 bits (a prime), 3 hashes
for word in ["cat", "dog", "fish"]:
    bloom.add(word)
print(bloom.positions("cat"))               # -> [13, 1, 8]
print(bloom.positions("dog"))               # -> [8, 17, 7]
print(bloom.might_contain("cat"), bloom.might_contain("fish"))  # -> True True
print(bloom.might_contain("owl"))           # -> False
print(bloom.might_contain("colt"))          # -> True
random.seed(1)
rate = measured_rate(997, 7, 100, 10000)    # about 10 bits per word
print(round(expected_rate(997, 100, 7), 4), round(rate, 4))   # -> 0.0083 0.0093
print(rate < 2 * expected_rate(997, 100, 7))    # -> True
```

```{=latex}
\clearpage
```

## 147. Count-Min Sketch {#a147}

```{=latex}
\markright{147. Count-Min Sketch}
```

[Approximate Counts for Heavy Hitters · Design · Tier 3 · python/147\_count\_min\_sketch.py]{.meta}

Count a stream in a fixed grid of depth rows by width counters: add bumps one counter per row and estimate returns the smallest, never below the true count. Width 5, depth 3, seed 6, stream cat dog cat fish cat dog bird cat dog → estimate("bird") = 2 (true 1), top 2 = \[(4, 'cat'), (3, 'dog')\].

```python
import heapq                # heappush / heappop keep the smallest at index 0
import random               # a seeded generator picks the row hashes


# --- algorithm ---
MOD = 1000000007                    # a large prime


def string_hash(word):
    """The word read as a base-31 number, mod MOD. O(len(word))."""
    h = 0
    for ch in word:
        h = (h * 31 + ord(ch)) % MOD
    return h


class CountMinSketch:
    """depth rows of width counters; each row has its own hash."""

    def __init__(self, width, depth, seed):
        self.width = width
        self.depth = depth
        self.table = []             # depth rows of width counters
        self.a = []                 # row r sends x to column
        self.b = []                 # ((a[r] * x + b[r]) mod MOD) mod width
        rng = random.Random(seed)   # the same seed gives the same hashes
        for row in range(depth):
            self.table.append([0] * width)
            self.a.append(rng.randint(1, MOD - 1))
            self.b.append(rng.randint(0, MOD - 1))

    def columns(self, item):
        """The item's column in each row. O(L + depth)."""
        x = string_hash(item)
        result = []
        for row in range(self.depth):
            h = (self.a[row] * x + self.b[row]) % MOD
            result.append(h % self.width)
        return result

    def add(self, item, count):
        """Add count to the item's counter in every row. O(L + depth)."""
        cols = self.columns(item)
        for row in range(self.depth):
            self.table[row][cols[row]] += count

    def estimate(self, item):
        """The smallest of the item's counters, never below its true count.
        O(L + depth)."""
        cols = self.columns(item)
        best = self.table[0][cols[0]]
        for row in range(1, self.depth):
            best = min(best, self.table[row][cols[row]])
        return best                 # collisions only ever add


class HeavyHitters:
    """The sketch counts every item; a size-k min-heap keeps the leaders."""

    def __init__(self, k, width, depth, seed):
        self.k = k
        self.sketch = CountMinSketch(width, depth, seed)
        self.counts = {}            # leader -> its estimate when last seen
        self.heap = []              # (estimate, leader), one entry per leader

    def add(self, item):
        """Count the item, then keep the k largest estimates as in Top-K.
        O(L + depth + log k) amortized."""
        self.sketch.add(item, 1)
        estimate = self.sketch.estimate(item)
        if item in self.counts:
            self.counts[item] = estimate        # its heap entry is now stale
            return
        self.counts[item] = estimate
        heapq.heappush(self.heap, (estimate, item))
        if len(self.heap) > self.k:             # one too many: drop the weakest
            estimate, weakest = heapq.heappop(self.heap)
            while estimate != self.counts[weakest]:     # stale: it grew since
                heapq.heappush(self.heap, (self.counts[weakest], weakest))
                estimate, weakest = heapq.heappop(self.heap)
            del self.counts[weakest]

    def top(self):
        """The leaders as (estimate, item), largest first. O(k log k)."""
        pairs = []
        for item in self.counts:
            pairs.append((self.counts[item], item))
        pairs.sort()
        return pairs[::-1]                      # largest estimate first


# --- try it ---
stream = ["cat", "dog", "cat", "fish", "cat", "dog", "bird", "cat", "dog"]
sketch = CountMinSketch(5, 3, 6)                # width 5, depth 3, seed 6
for word in stream:
    sketch.add(word, 1)
print(sketch.table)     # -> [[0, 7, 0, 0, 2], [4, 3, 2, 0, 0], [0, 0, 1, 5, 3]]
print(sketch.estimate("cat"), sketch.estimate("dog"))       # -> 4 3
print(sketch.estimate("fish"), sketch.estimate("bird"))     # -> 1 2
print(sketch.estimate("emu"), sketch.estimate("owl"))       # -> 0 1
hitters = HeavyHitters(2, 5, 3, 6)
for word in stream:
    hitters.add(word)
print(hitters.top())                            # -> [(4, 'cat'), (3, 'dog')]
big = HeavyHitters(3, 200, 4, 1)                # 800 counters
for i in range(3000):                           # 3003 distinct words in all
    big.add("w" + str(i))                       # 3000 words, once each
    if i % 10 == 0:
        big.add("hot")                          # 300 times
    if i % 15 == 0:
        big.add("warm")                         # 200 times
    if i % 25 == 0:
        big.add("mild")                         # 120 times
print(big.top())        # -> [(308, 'hot'), (213, 'warm'), (132, 'mild')]
```

```{=latex}
\clearpage
```

## 148. Quadtree {#a148}

```{=latex}
\markright{148. Quadtree}
```

[Points in Squares, Split When Full · Design · Tier 3 · python/148\_quadtree.py]{.meta}

Store points so that a box query reads only the part of the map it covers, as when an app looks for the drivers near a rider: 9 drivers in a 16 x 16 square, box from (2, 2) to (6, 6) → \[(3, 5), (5, 6), (6, 3)\].

```python
# --- algorithm ---
CAPACITY = 4                        # points a leaf holds before it splits
MIN_SIZE = 1                        # a leaf this small never splits


class QuadTree:
    """A square [x, x + size) by [y, y + size); a leaf holds up to CAPACITY
    points and a full leaf splits into four half-size squares."""

    def __init__(self, x, y, size):
        self.x = x                  # lower-left corner
        self.y = y
        self.size = size
        self.points = []            # only leaves hold points
        self.children = None        # SW, SE, NW, NE once split

    def contains(self, px, py):
        """Left and bottom edges belong to the square, right and top do not.
        O(1)."""
        inside_x = self.x <= px < self.x + self.size
        inside_y = self.y <= py < self.y + self.size
        return inside_x and inside_y

    def insert(self, px, py):
        """Put the point in the leaf whose square holds it. O(depth)."""
        if not self.contains(px, py):
            return False                    # not in this square
        if self.children is None:
            if len(self.points) < CAPACITY or self.size <= MIN_SIZE:
                self.points.append((px, py))
                return True
            self.split()                    # a full leaf becomes four leaves
        for child in self.children:
            if child.insert(px, py):        # exactly one child holds it
                return True
        return False

    def split(self):
        """Make four half-size children and pass this leaf's points down.
        O(CAPACITY): each point drops into a child with room."""
        half = self.size / 2
        self.children = []                  # SW, SE, NW, NE
        for dx, dy in [(0, 0), (half, 0), (0, half), (half, half)]:
            self.children.append(QuadTree(self.x + dx, self.y + dy, half))
        old_points = self.points
        self.points = []
        for px, py in old_points:
            self.insert(px, py)                 # now lands in a child

    def range_query(self, left, bottom, right, top):
        """Points with left <= x <= right and bottom <= y <= top; a square that
        misses the box is skipped whole. O(nodes visited + points read)."""
        found = []
        if left >= self.x + self.size or right < self.x:
            return found                    # no overlap in x: prune
        if bottom >= self.y + self.size or top < self.y:
            return found                    # no overlap in y: prune
        for px, py in self.points:
            if left <= px <= right and bottom <= py <= top:
                found.append((px, py))
        if self.children is not None:
            for child in self.children:
                found.extend(child.range_query(left, bottom, right, top))
        return found


# --- try it ---
tree = QuadTree(0, 0, 16)                   # a 16 x 16 square of city blocks
drivers = [(1, 2), (3, 5), (6, 1), (2, 7), (5, 6), (12, 3), (10, 12), (14, 9),
           (6, 3)]
for point in drivers:
    tree.insert(point[0], point[1])
print(sorted(tree.range_query(2, 2, 6, 6)))     # -> [(3, 5), (5, 6), (6, 3)]
print(sorted(tree.range_query(9, 8, 16, 16)))   # -> [(10, 12), (14, 9)]
# children are SW, SE, NW, NE: this is the NW quarter of the SW quarter
print(tree.children[0].children[2].points)      # -> [(3, 5), (2, 7)]
# no driver in this box; (16, 4) sits on the right edge, outside the root
print(tree.range_query(7, 13, 9, 15), tree.insert(16, 4))   # -> [] False
```

```{=latex}
\clearpage
```

## 149. Job Scheduler {#a149}

```{=latex}
\markright{149. Job Scheduler}
```

[A Min-Heap of Next Run Times · Design · Tier 3 · python/149\_job\_scheduler.py]{.meta}

Run jobs at given times: schedule(name, run\_at, interval) runs a job at run\_at and then every interval (0 = once), cancel(name) drops it, and run\_due(now) returns every run due by now, earliest first: ping every 5 from 5, save once at 10 → run\_due(10) = \[\[5, 'ping'\], \[10, 'save'\], \[10, 'ping'\]\].

```python
import heapq            # heappush / heappop keep the smallest at index 0


# --- algorithm ---
class JobScheduler:
    """A min-heap of (run_at, seq, name); a map marks each name's live
    entry. O(log n) per push or pop, O(1) to cancel."""

    def __init__(self):
        self.heap = []          # (run_at, seq, name), earliest on top
        self.interval = {}      # name -> repeat interval, 0 for one-off
        self.live = {}          # name -> seq of its one live heap entry
        self.seq = 0            # insertion counter: breaks ties in time

    def push(self, name, run_at):
        """Add a fresh heap entry for name and make it the live one.
        O(log n)."""
        self.seq += 1
        self.live[name] = self.seq
        heapq.heappush(self.heap, (run_at, self.seq, name))

    def schedule(self, name, run_at, interval):
        """Run name at run_at, then every interval (0 = once). O(log n)."""
        self.interval[name] = interval
        self.push(name, run_at)         # an older entry for name goes stale

    def cancel(self, name):
        """Forget name; its heap entry is skipped when it surfaces. O(1)."""
        if name not in self.live:
            return False
        del self.live[name]
        del self.interval[name]
        return True

    def run_due(self, now):
        """Pop every live entry with run_at <= now in time order; a recurring
        job goes back in at run_at + interval. O(log n) per pop."""
        ran = []
        while len(self.heap) > 0 and self.heap[0][0] <= now:
            run_at, seq, name = heapq.heappop(self.heap)
            if name not in self.live or self.live[name] != seq:
                continue                # cancelled or replaced: stale
            ran.append([run_at, name])
            interval = self.interval[name]
            if interval > 0:
                self.push(name, run_at + interval)  # if still due: catch up
            else:
                del self.live[name]     # a one-off job is done
                del self.interval[name]
        return ran


# --- try it ---
scheduler = JobScheduler()
scheduler.schedule("ping", 5, 5)        # every 5 time units from 5
scheduler.schedule("save", 10, 0)       # once, at 10
scheduler.schedule("mail", 12, 0)
print(scheduler.run_due(10))    # -> [[5, 'ping'], [10, 'save'], [10, 'ping']]
print(scheduler.cancel("mail"), scheduler.run_due(12))      # -> True []
print(scheduler.run_due(26))    # -> [[15, 'ping'], [20, 'ping'], [25, 'ping']]
scheduler.cancel("ping")                # its entry for 30 stays, now stale
scheduler.schedule("ping", 35, 0)       # same name, new seq
print(scheduler.run_due(40), len(scheduler.heap))   # -> [[35, 'ping']] 0
```

```{=latex}
\clearpage
```

## 150. Inverted Index {#a150}

```{=latex}
\markright{150. Inverted Index}
```

[Postings Lists and Sorted Intersection · Design · Tier 3 · python/150\_inverted\_index.py]{.meta}

Map each word to the sorted ids of the documents that contain it, so a query walks a few short lists instead of reading every document. Six documents → search\_and(\["quick", "dog"\]) = \[3, 4, 6\] and search\_or(\["fox", "lazy"\]) = \[1, 2, 4\].

```python
# --- algorithm ---
def intersect(a, b):
    """Ids in both sorted lists, by two pointers. O(len(a) + len(b))."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])             # in both: keep it
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1                          # a[i] is not in b
        else:
            j += 1                          # b[j] is not in a
    return result


def union(a, b):
    """Ids in either sorted list, each once. O(len(a) + len(b))."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])             # in both: keep one copy
            i += 1
            j += 1
        elif a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])                    # one list ran out: copy the rest
    result.extend(b[j:])
    return result


class InvertedIndex:
    """term -> increasing list of the ids of the documents that contain it."""

    def __init__(self):
        self.postings = {}                  # term -> sorted doc ids

    def add_document(self, doc_id, text):
        """Append doc_id once to the list of every word in text; ids must grow
        from call to call. O(words in text)."""
        lowered = text.lower()
        for word in lowered.split():
            if word not in self.postings:
                self.postings[word] = []
            ids = self.postings[word]
            if len(ids) == 0 or ids[-1] != doc_id:  # once per document
                ids.append(doc_id)

    def search_and(self, terms):
        """Ids of the documents holding every term: intersect the lists,
        shortest first. O(total length of the lists)."""
        lists = []
        for term in terms:
            word = term.lower()
            if word not in self.postings:
                return []                   # a missing term matches nothing
            lists.append(self.postings[word])
        if len(lists) == 0:
            return []
        lists.sort(key=len)                 # shortest list first
        result = list(lists[0])             # a copy: the index stays intact
        for k in range(1, len(lists)):
            result = intersect(result, lists[k])
        return result

    def search_or(self, terms):
        """Ids of the documents holding any term: merge the lists pairwise.
        O(terms * total length)."""
        result = []
        for term in terms:
            word = term.lower()
            if word in self.postings:
                result = union(result, self.postings[word])
        return result


# --- try it ---
index = InvertedIndex()
index.add_document(1, "the quick brown fox")
index.add_document(2, "the lazy dog")
index.add_document(3, "a quick brown dog")
index.add_document(4, "the dog chased the quick fox")
index.add_document(5, "my dog sleeps")
index.add_document(6, "quick thinking saved the dog")
print(index.postings["the"])                         # -> [1, 2, 4, 6]
print(index.postings["dog"])                         # -> [2, 3, 4, 5, 6]
print(index.search_and(["quick", "dog"]))            # -> [3, 4, 6]
print(index.search_and(["The", "QUICK", "dog"]))     # -> [4, 6]
print(index.search_or(["fox", "lazy"]))              # -> [1, 2, 4]
print(index.search_and(["quick", "cat"]), index.search_or(["cat"]))  # -> [] []
```
