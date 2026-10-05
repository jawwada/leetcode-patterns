# Alien Dictionary

*LeetCode 269 · Hard · Pattern: Topological sort (Kahn's BFS) / cycle detection · Reading time ~10 min*

## The problem

Given a list of words sorted lexicographically according to an unknown alphabet, return a string of the unique letters
in a valid alphabet order, or "" if the ordering is contradictory. Any valid order is accepted.

```text
Example: ["wrt","wrf","er","ett","rftt"] -> "wertf";
  ["z","x","z"] -> "".
```

## What the problem is really asking

You are handed a dictionary from an alien language. The words are already sorted, but by an alphabet you do not know. Recover an alphabet consistent with that sorting: a string containing every letter that appears, each once, in an order that would make the list sorted. If the list contradicts itself, return `""`. Any valid alphabet is accepted.

```text
 words (sorted in the unknown alphabet):

   0: w r t
   1: w r f
   2: e r
   3: e t t
   4: r f t t

 answer: "wertf"   (w < e < r < t < f)
```

The answer is a string, an ordering of letters. That makes it the previous problem in disguise: letters are courses, and "x comes before y in the alphabet" is a prerequisite. What makes it hard is that nobody hands you the prerequisites. You must extract them from the words, extract exactly the right ones (not too many, not too few), and spot two different kinds of contradiction: a cycle among letters, and a word list that is broken before any letters are compared.

## Do it by hand first

How does a human compare two dictionary words? Left to right, until the first position where they differ. That position, and only that position, decides the order. Everything after it is irrelevant: "cat" < "dog" says c < d and nothing about a versus o.

So compare neighbours in the list:

```text
 wrt vs wrf :  w=w, r=r, t!=f   ->  t before f
 wrf vs er  :  w!=e             ->  w before e
 er  vs ett :  e=e, r!=t        ->  r before t
 ett vs rftt:  e!=r             ->  e before r
```

Four facts. Chain them: w before e, e before r, r before t, t before f. So `w e r t f`.

```text
 letters as nodes, facts as arrows:

   w ---> e ---> r ---> t ---> f

 stored as:
   adj:   w:{e}  e:{r}  r:{t}  t:{f}  f:{}
   indeg: w:0    e:1    r:1    t:1    f:1
```

Your hand did two separate jobs. First it turned word pairs into arrows. Then it ordered the letters so all arrows point forward, which is exactly what Kahn's queue did in Course Schedule II. The seed is the realisation that the first job produces a graph and the second job is a topological sort of it.

Two questions you should ask while doing it by hand:

1. Why only neighbours, not all pairs? Because sorted order is transitive. If words 0 < 1 and 1 < 2, the fact from comparing 0 with 2 is already implied by the chain of facts from 0-1 and 1-2. Comparing non-neighbours adds nothing new but can never add anything false either; it only wastes time.
2. What if two neighbours never differ? Then one is a prefix of the other. `"ab"` before `"abc"` is fine and gives no fact. `"abc"` before `"ab"` is impossible in any alphabet, because a prefix always sorts first. That input is broken, so the answer is `""`.

## The first honest attempt

A careful candidate extracts the facts as above into a set of pairs `(a, b)`, then builds the alphabet greedily: each round, scan every remaining letter, and for each one scan every remaining fact to see whether some fact still has it on the right-hand side. Pick a letter that is on no right-hand side, emit it, delete the facts it starts, and repeat. If a round finds no free letter while letters remain, the facts are contradictory.

With U letters and C facts, each of the U rounds rescans all C facts: O(U · C), plus the scan of the words.

```text
 facts: (t,f) (w,e) (r,t) (e,r)

 round 1: scan 4 facts -> blocked {f,e,t,r}  free {w}  emit w
 round 2: scan 3 facts -> blocked {f,t,r}    free {e}  emit e
 round 3: scan 2 facts -> blocked {f,t}      free {r}  emit r
 round 4: scan 1 fact  -> blocked {f}        free {t}  emit t
          ^ (t,f) was read in every single round
```

The waste is the same waste as in Course Schedule II: emitting w can only change the status of the letters w points to (just e), yet every fact is reread to recompute every letter's status.

## The turning point

**Claim: each adjacent pair of words contributes at most one arrow, at the first differing position; once those arrows are collected, any topological order of the letters is a valid alphabet, and Kahn's algorithm finds one in linear time or proves none exists.**

The first half is the extraction rule from the hand solution. Make it airtight:

- For each neighbour pair `(w1, w2)`, walk both words together. At the first index j where `w1[j] != w2[j]`, add the arrow `w1[j] -> w2[j]` and stop.
- If the walk ends without a difference and `len(w1) > len(w2)`, return `""` immediately: a longer word sits before its own prefix.
- Every letter that appears anywhere is a node, even if it is in no arrow. In `["ab", "adc"]` the only fact is `b -> d`; the letters `a` and `c` take part in no fact at all and must still be in the output.

The second half reuses Kahn. A letter with in-degree 0 has no letter that must precede it, so it can go next. Emitting it lowers the in-degree of the letters it points to. If the queue empties while letters remain, those letters form a cycle of facts, such as `z < x` and `x < z` from `["z", "x", "z"]`, and the answer is `""`.

One detail decides whether the counters are right: **do not count the same arrow twice**. If two different word pairs both give `t -> f`, and you add it twice, `indeg[f]` becomes 2, but popping t decrements it only once if your adjacency is a set, or twice if it is a list. Mixing the two is the classic bug: a set for adjacency with a raw `+= 1` per fact leaves f stuck at 1 forever, and a valid dictionary is reported as contradictory. The fix is simple and local: increment `indeg[b]` only when `b` is newly added to `adj[a]`.

```text
 duplicate fact, done wrong:

   adj[t] = {f}        indeg[f] = 2   (counted twice)
   pop t  -> indeg[f] = 1             (one arrow in the set)
   f never reaches 0  -> "" returned for a valid input
```

So the whole algorithm is: build nodes for every letter; extract at most one deduplicated arrow per neighbour pair, failing early on a bad prefix; run Kahn; return the joined order if it has every letter, else `""`.

## Watch it work

Example `["wrt", "wrf", "er", "ett", "rftt"]`. State: the arrow set, `indeg` per letter, the queue (front on the left), and the output.

**Frame 1.** Initialise every letter at in-degree 0. Compare `wrt` and `wrf`: first difference at index 2, so add `t -> f`.

```text
 wrt
 wrf
   ^ j=2: t != f        arrows: t->f
 indeg: w0 r0 t0 f1 e0
```

**Frame 2.** `wrf` vs `er`: they differ immediately. Add `w -> e`.

```text
 wrf
 er
 ^ j=0: w != e          arrows: t->f  w->e
 indeg: w0 r0 t0 f1 e1
```

The `r` at index 1 of both words is ignored; after the first difference nothing counts.

**Frame 3.** `er` vs `ett` gives `r -> t`; `ett` vs `rftt` gives `e -> r`. Extraction done.

```text
 arrows: t->f  w->e  r->t  e->r
 indeg:  w0 r1 t1 f1 e1

   w ---> e ---> r ---> t ---> f
 queue: [w]
```

Only w has nothing pointing at it.

**Frame 4.** Pop w, emit it. Its arrow lowers e to 0; e is enqueued.

```text
 indeg:  w- r1 t1 f1 e0
 queue:  [e]
 output: w
```

**Frame 5.** Pop e. Lowers r to 0.

```text
 indeg:  w- r0 t1 f1 e-
 queue:  [r]
 output: w e
```

**Frame 6.** Pop r (t drops to 0), then pop t (f drops to 0), then pop f.

```text
 indeg:  w- r- t- f- e-
 queue:  []
 output: w e r t f      5 letters == 5 distinct letters
```

Return `"wertf"`.

Across frames, the in-degree of each letter equalled the number of distinct letters that must precede it and had not been emitted yet. The queue never held more than one letter here, which tells you something extra: this alphabet is the only valid one for this input.

And the failing case, `["z", "x", "z"]`: the pairs give `z -> x` and `x -> z`. Both letters start at in-degree 1, the queue starts empty, the output is empty and shorter than 2 letters, so return `""`.

## Why it is correct

Soundness of the facts. If the list is sorted under the true alphabet, the first difference of two neighbours decides their order, so every extracted arrow is a true statement about that alphabet. The prefix check catches the one situation with no differing position that is still impossible.

Sufficiency of the facts. Take any order that respects all extracted arrows, and any neighbour pair. If it was a prefix pair in the allowed direction, it is sorted under any alphabet. Otherwise the two words agree up to j and the order puts `w1[j]` before `w2[j]`, so w1 sorts first. Every neighbour pair is in order, and sortedness of neighbours implies sortedness of the whole list. So any topological order is a correct answer, and Kahn's correctness from Course Schedule II says it outputs one exactly when the arrows contain no cycle.

Contradiction. If the arrows contain a cycle, no order can put every letter on the cycle before the next one, so no alphabet exists and `""` is right. Kahn signals that by emitting fewer letters than exist.

## Cost

- Time O(S + U + C): S is the total number of characters (each neighbour comparison stops at the first difference, so the scan reads each character at most twice), U letters and C arrows for Kahn. With a fixed 26-letter alphabet, U and C are tiny and S dominates.
- Space O(U + C): the letter graph and counters.
- The rescanning brute force was O(S + U · C).

## Variations you will meet

- **Verifying an Alien Dictionary (LeetCode 953).** You are given the alphabet and asked whether the words are sorted. No graph: map letters to ranks and compare neighbours. It is the extraction step without the sort.
- **Return the smallest valid alphabet.** Use a min-heap in Kahn instead of a FIFO queue.
- **Is the alphabet unique?** It is unique iff the queue never holds two letters at once, which in turn means the arrows chain every letter.
- **DFS instead of Kahn.** Run three-colour DFS over letters, append a letter when it finishes, reverse the list; a grey-to-grey arrow means `""`. Equivalent cost, and you must still deduplicate and handle the prefix case.

## What to carry forward

When order constraints are hidden in data, first mine them into arrows (one per adjacent pair, at the first difference, no duplicates), then topologically sort; the graph is the bridge between "sorted list" and "alphabet". The next problem, Parallel Courses III, keeps Kahn's queue but carries a number along each arrow: not just "may I go now" but "when is the earliest I can finish".
