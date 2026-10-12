# Top K Frequent Words

*LeetCode 692 · Medium · Pattern: Size-k heap (keep the k best) · Reading time ~7 min*

## The problem

Given a list of words and an integer k, return the k most frequent words sorted by frequency descending; words with
equal frequency are sorted lexicographically ascending.

```text
Example: ["i","love","leetcode","i","love","coding"], k=2 ->
  ["i","love"].
```

## What the problem is really asking

You get a list of words and a number k. Return the k most frequent words, ordered from most frequent to least. When two
words have the same count, the alphabetically earlier one comes first.

The answer is an ordered list of k words. Two things make it harder than the earlier "top k" problems. First, there is a
count step before any ranking. Second, the ranking has two keys pulling in opposite directions: count wants **bigger
first**, while the word wants **smaller first**.

```text
words = [i, love, leetcode, i, love, coding]    k = 2

count:   i 2   love 2   leetcode 1   coding 1

rank by (count desc, word asc):
  1. i        (2)   <- "i" < "love" alphabetically
  2. love     (2)
  3. coding   (1)   <- "coding" < "leetcode"
  4. leetcode (1)
answer: [i, love]
```

## Do it by hand first

First you tally. You would walk the list and make tick marks: i ||, love ||, leetcode |, coding |.

Then, with k = 2 seats, you go through the tallies.

- i (2): seat it.
- love (2): seat it. Both seats full.
- leetcode (1): who is the weakest seated word? Both have 2. On a tie the word that would be listed later is weaker, so
  "love" is the weakest. leetcode has only 1, so it loses to "love" and leaves.
- coding (1): same story. It loses to "love" and leaves.

Then you write the seated words from best to worst: i, love.

You kept track of a k-seat podium and, at every step, the identity of its weakest occupant. Weakest means lowest count,
and among equal counts, alphabetically **latest**. That second clause is the part people get wrong.

## The first honest attempt

Count with a hash map, then sort all m distinct words by `(-count, word)` and take the first k. O(n + m log m). It is a
perfectly good answer and the reference brute force.

The waste, as in the last two problems, is ordering the losers:

```text
sorted:  i 2 | love 2 || coding 1 | leetcode 1
               k=2    ^^ ^^^^^^^^^^^^^^^^^^^^^^
                         m-k losers, ordered for nothing
```

When m is large and k is small, the m log m sort is mostly spent arranging words that will never be printed.

## The turning point

**Claim: a word can be discarded as soon as k words that beat it have been seen, so a size-k heap whose root is the
weakest kept word does the job in O(m log k).**

That is the same club argument as the stream and the points problems. What is new is defining "weakest" so that
`heapq`, a min-heap, puts it at the root. The root of a min-heap is the item that compares smallest, so we need an
ordering where **worse means smaller**:

- lower count is smaller (worse);
- equal count: the alphabetically **larger** word is smaller (worse).

For numbers we would negate to flip a direction. The first key is fine as it is: `count` ascending already puts low
counts at the root. The second key needs flipping, and you cannot negate a string. Here is the trap in a tiny case,
`[i, love]`, k = 1:

```text
plain tuples (count, word), size-1 heap
push (1,"i")     heap [(1,i)]
push (1,"love")  heap [(1,i), (1,love)]  size 2 > 1
pop root  ->  (1,"i")  leaves      WRONG: "i" should win
kept: love
```

Python's tuple compare says `"i" < "love"`, so "i" becomes the root and gets evicted. The fix is a tiny class whose `__lt__`
encodes the real meaning of worse. `heapq` only ever uses `<`, so one method is enough:

```python
def __lt__(self, other):
    if self.count != other.count:
        return self.count < other.count   # fewer = worse
    return self.word > other.word         # later word = worse
```

With that ordering the algorithm is the familiar one: for each `(word, count)` push an entry, and pop the root whenever the
size exceeds k. At the end the heap holds the k winners, but in heap order, worst at the root. Popping them one by one
yields worst first, so reverse that list.

Why not the other famous trick, `(-count, word)` tuples? Those order best-first, which is exactly what you want if you
push **all** m words, heapify, and pop k times: O(m + k log m), also correct. What fails is combining best-first keys with
a size-k heap, because then the root is the best word and you would evict the champion.

## Watch it work

`words = [i, love, leetcode, i, love, coding]`, k = 2. Counter yields `i 2, love 2, leetcode 1, coding 1` in first-seen
order. Entries are shown as `word count`; the root is the worst kept word.

```text
Frame 1: push i2
     i2              array [i2]
                     size 1 <= 2
```

The podium has one occupant.

```text
Frame 2: push love2
     love2           array [love2, i2]
      /              tie on 2; "love" > "i" -> love is worse,
    i2               so love sifts up to the root
```

The custom `__lt__` made love compare smaller, so it became the doorman.

```text
Frame 3: push leetcode1 -> size 3, pop root
   before pop:          after pop:
     leetcode1            love2
      /     \              /
    i2     love2         i2
popped: leetcode1        array [love2, i2]
```

leetcode1 had the lowest count, so it sifted all the way to the root and was popped straight away.

```text
Frame 4: push coding1 -> size 3, pop root
   before pop:          after pop:
      coding1             love2
      /     \              /
    i2     love2         i2
popped: coding1          array [love2, i2]
```

Same as frame 3. Neither 1-count word ever displaced a 2-count word.

```text
Frame 5: drain the heap, then reverse
pop -> love      pop -> i
drained:  [love, i]     (worst first)
reversed: [i, love]     <- answer
```

At every frame the root was the word you would evict next under the problem's ranking, and the heap held the best
`min(seen, k)` words. The drain order is the exact reverse of the answer order because each pop takes the current worst.

## Why it is correct

Define `a beats b` when `a.count > b.count`, or the counts are equal and `a.word < b.word`. This is a strict total order on
distinct words, and the answer is the first k words under it.

Invariant: **after processing some distinct words, the heap holds the min(seen, k) best of them.** Pushing a word and,
if the size is k+1, popping the worst of the k+1, leaves the k best of those, since the popped word is beaten by k others
already seen. A word discarded earlier was beaten by k words seen before it; each of those is either still in the
heap or was displaced by an even better word, so the discarded word stays beaten by at least k words and can never
belong to the top k. When all words are processed, the heap holds exactly the top k. Popping from a
min-heap returns items in increasing order of the custom `<`, that is, worst to best, so reversing gives best to worst,
which is the required output order.

## Cost

- **Size-k heap:** counting is O(n) for n words. Each of the m distinct words does O(log k) heap work, so O(n + m log k)
  time. Space O(m) for the counter plus O(k) for the heap.
- **Heapify all, pop k:** O(n + m + k log m) time with `(-count, word)` tuples, O(m) space.
- **Sort:** O(n + m log m) time, O(m) space.
- **Bucket by count:** counts range from 1 to n, so put words in buckets by count, sort each bucket alphabetically, and
  read buckets from high to low until k words are collected. Close to linear when buckets are small.

## Variations you will meet

- **Top K Frequent Elements (LeetCode 347).** Integers, any order, no tie rule. Plain `(count, value)` tuples in a size-k
  heap work, or bucket sort in O(n).
- **Ties broken the other way (later word wins).** Then plain `(count, word)` tuples are already "worse is smaller" and
  no wrapper is needed. Always ask which direction the tie goes before choosing the key.
- **Streaming words with k fixed.** Counts change over time, and a word's entry inside the heap goes stale. Push a fresh
  entry on every change and skip stale ones when they surface (lazy deletion), or keep counts in a sorted container.
- **Sort Characters by Frequency.** Every character is printed, so there is no club to bound; a full sort or buckets is
  the right tool.

## What to carry forward

Decide what "worst" means, then make it compare smallest, writing `__lt__` when a string key must run backwards. The next
problem keeps counts in a heap but stops using it as a filter: it becomes a greedy chooser that always spends the most
frequent task, with a queue holding tasks that are cooling down.
