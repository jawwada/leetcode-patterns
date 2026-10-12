---
rank: 102
slug: boyer_moore_majority_vote
---

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
