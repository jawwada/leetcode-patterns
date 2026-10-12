---
rank: 21
slug: median_from_data_stream
---

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
