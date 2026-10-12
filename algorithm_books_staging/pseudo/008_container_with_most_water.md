---
rank: 8
slug: container_with_most_water
---

Vertical lines with the given heights stand at positions `0, 1, ..., n - 1`. Choose two of them so that, together with the x-axis, they hold the most water, and return that amount: lines `i` and `j` hold `min(height[i], height[j]) × (j - i)`, the shorter line times the distance between them. For `[1, 8, 6, 2, 5, 4, 8, 3, 7]` the answer is `49`, from the lines at positions 1 and 8, `min(8, 7) × 7`.

The brute force measures all `n(n - 1) / 2` pairs, `O(n²)`. Two pointers start from the widest container, `left = 0` and `right = n - 1`, and narrow it one wall at a time, and the whole argument is about which wall moves. Suppose `height[left]` is the shorter. Every other container still in play that keeps the line at `left` pairs it with a line strictly between the two, so it is narrower, and its water level is still capped by `height[left]`, so it is no taller. None of them can beat the area just measured, and `left` can be retired for good. Moving the taller wall instead keeps the same cap and only loses width. On a tie both walls are spent, and the code simply moves `right`.

Picture all the pairs as a triangle of candidates, one row per left line and one column per right line. Each comparison measures one pair and crosses off every other pair that uses the retired wall, a whole row or column of the triangle at once. After `n - 1` steps the pointers meet, and every pair has been measured or ruled out. In the drawing the best container spans positions 1 to 8, and the lines in between stand in the water without holding any of it back, because a line has no width.

```text
8      │              │                    │ line   ~ the best container
7      │~~~~~~~~~~~~~~│~~~~~│              min(8, 7) × (8 - 1) = 49
6      │~~│~~~~~~~~~~~│~~~~~│
5      │~~│~~~~~│~~~~~│~~~~~│
4      │~~│~~~~~│~~│~~│~~~~~│
3      │~~│~~~~~│~~│~~│~~│~~│
2      │~~│~~│~~│~~│~~│~~│~~│
1   │  │~~│~~│~~│~~│~~│~~│~~│
    0  1  2  3  4  5  6  7  8
left right   heights   width   area   best   move
  0    8     1 vs 7      8       8      8    left, the shorter
  1    8     8 vs 7      7      49     49    right
  1    7     8 vs 3      6      18     49    right
  1    6     8 vs 8      5      40     49    right, a tie
  1    5     8 vs 4      4      16     49    right
  1    4     8 vs 5      3      15     49    right
  1    3     8 vs 2      2       4     49    right
  1    2     8 vs 6      1       6     49    right, and the pointers meet
```

```pseudo
FUNCTION MaxArea(height)
    left ← 0
    right ← len(height) - 1
    best ← 0
    WHILE left < right
        width ← right - left
        area ← min(height[left], height[right]) * width
        best ← max(best, area)
        IF height[left] < height[right]
            left ← left + 1                // left wall is shorter: retire it
        ELSE
            right ← right - 1              // right wall is shorter or tied
    RETURN best
```

Each step moves one pointer inward, so the scan is `O(n)` time with `O(1)` space. Reach for converging pointers whenever a pair is scored by its distance and by the smaller of its two ends, or by their sum, so that one comparison proves a whole side useless; Two Sum II on a sorted array is the same squeeze with sums. Trapping Rain Water (#9) looks similar but turns the geometry around: there every bar is a floor holding its own column of water, the answer is a sum over all columns, and the pointer behind the lower running maximum moves; here only the two chosen lines matter, and the answer is a single rectangle. The classic mistake is moving the taller wall: on the example `left` never leaves the line of height 1, and the scan returns `8` instead of `49`.

*Practice:* LC 11 Container With Most Water · LC 42 Trapping Rain Water · LC 167 Two Sum II - Input Array Is Sorted · LC 881 Boats to Save People
