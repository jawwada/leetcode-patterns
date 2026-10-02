"""
Top K Frequent Words (LeetCode 692)  — Medium
Pattern: Size-k heap (keep the k best)

Problem
-------
Given a list of words and an integer k, return the k most frequent words, sorted by frequency
descending; words with equal frequency are sorted lexicographically ascending.
Example: ["i","love","leetcode","i","love","coding"], k=2 -> ["i","love"].

Brute force
-----------
Count every word, then sort all distinct words by (-count, word) and take the first k.
O(m log m) time for m distinct words, O(m) space. The waste: the sort fully orders all m words
even though only k of them are reported; the relative order of the m-k losers is discarded.

From brute force to optimal
---------------------------
The redundancy is ordering the losers. Observation: a word is irrelevant as soon as k "better"
words have been seen, where "better" means higher count, or equal count and lexicographically
smaller. Keep a heap of size k whose root is the current WORST kept word, so every new word only
has to beat the root. Python's heapq is a min-heap, so the root must be the minimum under an
ordering where "worse" is "smaller": lower count is smaller, and for equal counts a
lexicographically LARGER word is smaller. A tiny wrapper class with __lt__ encodes that;
negating a string is impossible, which is exactly why the wrapper is needed.

Intuition
---------
Hold a k-seat podium whose doorman is the weakest occupant: the least frequent word, and among
ties the alphabetically latest. Each candidate word only competes with the doorman. At the end,
popping the heap yields the words worst-first, so reverse.

Geometric view
--------------
A triangle of k (count, word) pairs with the weakest at the apex. Candidates fall in one at a
time; when the triangle has k+1 members the apex is popped. Finally the triangle is drained apex
first, producing the answer in reverse, like unstacking plates.

Steps
-----
1. Count words with Counter.
2. Define Entry(count, word) with __lt__: smaller count is "less"; equal counts compare words in
   reverse (larger word is "less").
3. Push each Entry; pop the root whenever the heap exceeds k.
4. Pop everything, collect words, reverse.

Complexity: O(m log k) time after an O(n) count, O(m + k) space — heap bounded by k.
Pitfalls: Trying (-count, word) in a size-k min-heap (tie order is wrong: it evicts the
alphabetically LARGER word's rival); forgetting to reverse the drained heap; sorting ties by
word descending instead of ascending.
"""
import heapq
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        class Entry:
            __slots__ = ("count", "word")

            def __init__(self, count: int, word: str):
                self.count, self.word = count, word

            def __lt__(self, other: "Entry") -> bool:
                if self.count != other.count:
                    return self.count < other.count     # fewer occurrences = worse
                return self.word > other.word           # same count: later word = worse

        heap: List[Entry] = []
        for word, count in Counter(words).items():
            heapq.heappush(heap, Entry(count, word))
            if len(heap) > k:                           # evict the current worst
                heapq.heappop(heap)
        out = [heapq.heappop(heap).word for _ in range(len(heap))]
        return out[::-1]                                # popped worst-first, so reverse


def brute_force(words: List[str], k: int) -> List[str]:
    counts = Counter(words)
    return sorted(counts, key=lambda w: (-counts[w], w))[:k]   # orders ALL distinct words


if __name__ == "__main__":
    s = Solution()
    w1 = ["i", "love", "leetcode", "i", "love", "coding"]
    w2 = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"]
    assert s.topKFrequent(w1, 2) == ["i", "love"]
    assert s.topKFrequent(w2, 4) == ["the", "is", "sunny", "day"]
    assert s.topKFrequent(["a"], 1) == ["a"]                      # single word
    assert s.topKFrequent(["b", "a", "c"], 2) == ["a", "b"]      # all ties -> alphabetical
    for words, k in [(w1, 2), (w2, 4), (["a"], 1), (["b", "a", "c"], 2), (w2, 1)]:
        assert s.topKFrequent(words, k) == brute_force(words, k), (words, k)
    print("ok")
