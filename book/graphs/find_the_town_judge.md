# Find the Town Judge

*LeetCode 997 · Easy · Pattern: Degree counting (in-degree minus out-degree) · Reading time ~5 min*

## What the problem is really asking

People are labelled 1 to n. A pair `[a, b]` in `trust` says "a trusts b". The judge trusts nobody and is trusted by everybody else. Return the judge's label, or -1.

Direction is the whole point: "a trusts b" is not "b trusts a". Draw each pair as an arrow `a -> b` and the question is about arrows arriving at a node and arrows leaving it.

```text
 n = 4, trust = [1,3] [1,4] [2,3] [2,4] [4,3]

     1 ---------> 3 <--------- 2
      \           ^           /
       \          | (4 -> 3) /
        +-------> 4 <-------+

 stored as out-lists:
   1: [3, 4]   2: [3, 4]   3: []   4: [3]
```

Person 3 has an arrow from each of the other three and none leaving. The answer is one integer. The problem is easy, but it introduces the two numbers the next stretch of the chapter lives on: **in-degree** (arrows arriving) and **out-degree** (arrows leaving).

## Do it by hand first

Check each person by counting arrows in and out.

```text
 person   arrows in   arrows out   judge?
   1          0           2         no
   2          0           2         no
   3          3           0         YES  (3 == n-1, 0 out)
   4          2           1         no
```

Notice how the table gets filled: an arrow `a -> b` adds one to b's "in" cell and one to a's "out" cell, and touches nothing else. Your hand kept two tallies per person, filled one arrow at a time. That is the seed.

## The first honest attempt

For each candidate j, scan the whole trust list: if j appears on the left of any pair, reject; otherwise count the distinct people pointing at j and compare with n - 1. That is O(n · t).

```text
 candidate 1: read [1,3] [1,4] [2,3] [2,4] [4,3]
 candidate 2: read [1,3] [1,4] [2,3] [2,4] [4,3]
 candidate 3: read [1,3] [1,4] [2,3] [2,4] [4,3]
 candidate 4: read [1,3] [1,4] [2,3] [2,4] [4,3]
               \_____ same five arrows, four times ____/
```

Each arrow matters to exactly two people, its tail and its head, yet every candidate re-reads every arrow.

## The turning point

**Claim: one pass over the arrows tallies everyone's degrees, and the single number `score = in - out` equals n - 1 only for the judge.**

Flip the loop: instead of "for each person, read all arrows", do "for each arrow, update its two people". All degrees cost O(t).

Folding two tallies into one is safe because of a bound. Nobody trusts themselves and pairs are distinct, so `in <= n - 1`. Then `in - out = n - 1` forces `in = n - 1` and `out = 0`. One outgoing arrow, or one missing incoming arrow, drops the score below n - 1.

```text
 each arrow a -> b:   score[a] -= 1    score[b] += 1

      a ----------> b
     -1            +1
```

The structure is just a degree array. The next problems keep it, as pure in-degree, and put a queue on top.

## Watch it work

Example above. State: `score` for persons 1..4. Target is n - 1 = 3.

**Frame 1.** Arrow `1 -> 3`.

```text
 person:   1    2    3    4
 score:   -1    0   +1    0
          tail      head
```

**Frame 2.** Arrow `1 -> 4`. Person 1, trusting twice, sinks to -2.

```text
 score:   -2    0   +1   +1
```

**Frame 3.** Arrows `2 -> 3` and `2 -> 4`. Persons 3 and 4 are tied.

```text
 score:   -2   -2   +2   +2
```

**Frame 4.** Arrow `4 -> 3` breaks the tie both ways: 4 loses a point, 3 gains one.

```text
 score:   -2   -2   +3   +1
                     ^ == n-1
```

**Frame 5.** Scan 1..4 for score 3: person 3. Return 3.

Throughout, each arrow changed exactly two cells and the scores always summed to zero. A judge needs n - 1 of that zero total, which hints that at most one person can reach it.

## Why it is correct

After all arrows, `score[p] = in(p) - out(p)`, since each arrow gave +1 to its head and -1 to its tail.

The judge has `in = n - 1`, `out = 0`, so score n - 1: found. Conversely, score n - 1 with `in <= n - 1` and `out >= 0` makes both bounds tight, which is the definition of the judge.

Two people cannot both qualify: if p is the judge, every other q trusts p, so `out(q) >= 1` and q's score is at most n - 2.

Edge case n = 1, no pairs: score[1] = 0 = n - 1, so person 1 is the judge, correctly.

## Cost

- Time O(n + t): one pass over the arrows, one over the people.
- Space O(n): one integer per person, versus O(n · t) time for the brute force.

## Variations you will meet

- **Find the Celebrity (LeetCode 277).** The arrows are hidden behind `knows(a, b)`. Each question eliminates one person (if a knows b, a is out; otherwise b is out), so n - 1 questions leave one candidate; verify it with O(n) more.
- **Duplicate pairs allowed.** The bound `in <= n - 1` breaks and the folded score can lie; count distinct trusters and keep in and out separately.
- **All sources or sinks.** "Who has nothing arriving?" is the same single pass, and it is precisely the question that drives the next problem.

## What to carry forward

An arrow `a -> b` touches only out(a) and in(b), so all degrees cost one pass; count degrees before building anything else. Course Schedule keeps the in-degree array and asks what happens when you repeatedly remove the nodes whose in-degree is zero.
