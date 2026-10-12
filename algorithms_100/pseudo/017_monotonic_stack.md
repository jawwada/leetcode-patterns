---
rank: 17
slug: monotonic_stack
---

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
