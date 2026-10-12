---
rank: 52
slug: partition_labels
---

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
