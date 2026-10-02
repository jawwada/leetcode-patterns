"""
Maximum Frequency Stack (LeetCode 895)  — Hard
Pattern: Frequency buckets as stacks + max-frequency pointer

Problem
-------
Design FreqStack with push(val) and pop(): pop removes and returns the MOST FREQUENT element; on
a tie, the one closest to the top of the stack (pushed most recently among the tied values).
Example: push 5,7,5,7,4,5 then pop -> 5 (freq 3), pop -> 7 (5 and 7 tie at 2; 7 is more recent),
pop -> 5, pop -> 4.

Brute force
-----------
Keep a plain list in push order. pop counts every element (Counter), finds the maximum count,
then scans from the right for the first element whose count equals that maximum and deletes it.
push is O(1) but pop is O(n) time, O(n) space. The wasted work: the counts are rebuilt from
scratch on every pop even though a single push changes exactly one of them, and the right-to-left
scan re-examines elements that can never win because their frequency is below the maximum.

From brute force to optimal
---------------------------
Two things are recomputed: the frequency of each value, and "which value with maximal frequency
was pushed most recently". The first is fixed by a persistent dict freq[val], updated by +-1 per
operation. For the second, observe that when a value reaches frequency f it is, at that moment,
the most recent element to have frequency f. So keep one stack per frequency: group[f] holds the
values in the order they REACHED frequency f. The element to pop is the top of group[maxfreq],
and after popping, that value's frequency becomes f-1, which is already represented by its
earlier copy in group[f-1]. If group[maxfreq] empties, maxfreq decrements by exactly one
(frequencies are reached one step at a time, so group[maxfreq-1] is non-empty). Everything is
O(1).

Intuition
---------
A value pushed three times lives in three buckets: group[1], group[2], group[3], in that order.
The highest bucket a value occupies is its current frequency. Popping removes the value from its
highest bucket only, which is precisely "decrement frequency by one". Within a bucket, LIFO
order is the tie-break the problem asks for: the most recent arrival at that frequency.

Geometric view
--------------
Picture a staircase of stacks, one per frequency level. Each push lifts a value one step higher
by placing a copy on the next level's stack. pop always takes from the highest occupied step and
the staircase can only shrink by one step at a time, so a single pointer (maxfreq) tracks the
top.

Steps
-----
1. freq = {}, group = {frequency: [values]}, maxfreq = 0.
2. push(val): freq[val] += 1; f = freq[val]; group[f].append(val); maxfreq = max(maxfreq, f).
3. pop(): val = group[maxfreq].pop(); if group[maxfreq] is now empty: maxfreq -= 1;
   freq[val] -= 1; return val.

Complexity: O(1) time per operation, O(n) space — one dict update and one list push/pop; every
pushed element occupies exactly one bucket slot.
Pitfalls: storing only the latest copy of a value in its top bucket and forgetting that lower
buckets must still hold it; using a heap with (freq, time) instead (works, but O(log n)); not
decrementing maxfreq when its bucket empties.
"""
import random
from collections import Counter, defaultdict


class FreqStack:
    def __init__(self):
        self.freq = defaultdict(int)             # val -> current frequency
        self.group = defaultdict(list)           # frequency -> stack of vals that reached it
        self.maxfreq = 0

    def push(self, val: int) -> None:
        self.freq[val] += 1
        f = self.freq[val]
        self.group[f].append(val)                # val is now the newest at frequency f
        self.maxfreq = max(self.maxfreq, f)

    def pop(self) -> int:
        val = self.group[self.maxfreq].pop()     # most recent among the most frequent
        if not self.group[self.maxfreq]:
            self.maxfreq -= 1                    # group[maxfreq-1] is guaranteed non-empty
        self.freq[val] -= 1
        return val


class BruteForce:
    """Plain list in push order; pop recounts everything and scans from the top, O(n)."""

    def __init__(self):
        self.items = []

    def push(self, val: int) -> None:
        self.items.append(val)

    def pop(self) -> int:
        counts = Counter(self.items)             # rebuilt from scratch on every pop
        top = max(counts.values())
        for i in range(len(self.items) - 1, -1, -1):
            if counts[self.items[i]] == top:     # rightmost among the most frequent
                return self.items.pop(i)


if __name__ == "__main__":
    fs = FreqStack()
    for v in (5, 7, 5, 7, 4, 5):
        fs.push(v)
    assert [fs.pop() for _ in range(4)] == [5, 7, 5, 4]
    fs.push(7)                                   # 7 still has freq 1 from the earlier push
    assert fs.pop() == 7 and fs.pop() == 7

    fs = FreqStack()                             # edge: single element pushed and popped twice
    fs.push(1)
    assert fs.pop() == 1
    fs.push(2)
    assert fs.pop() == 2

    random.seed(0)
    for _ in range(20):
        fast, slow, size = FreqStack(), BruteForce(), 0
        for _ in range(300):
            if size == 0 or random.random() < 0.6:
                v = random.randint(0, 5)
                fast.push(v)
                slow.push(v)
                size += 1
            else:
                assert fast.pop() == slow.pop()
                size -= 1
    print("ok")
