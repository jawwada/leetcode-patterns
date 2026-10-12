---
rank: 111
slug: candy
---

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

Two linear passes give `O(n)` time, with `O(n)` space for the counts. Reach for two opposite passes whenever each element's condition splits into a left half and a right half, each settled by a sweep in its own direction: the two wall arrays of Trapping Rain Water (#9), the prefix and suffix products of LC 238 and the run lengths of LC 2100 all have this shape. Equal neighbors impose nothing, so `[1, 2, 2]` needs only `4` candies, handed out as `[1, 2, 1]`. The classic mistake is a right pass that overwrites with `candies[i + 1] + 1` instead of taking the maximum: on `[1, 2, 3, 1]` it cuts the top child from 3 candies to 2, level with its lower left neighbor, and reports `6` instead of `7`.

*Practice:* LC 135 Candy · LC 42 Trapping Rain Water · LC 238 Product of Array Except Self · LC 2100 Find Good Days to Rob the Bank
