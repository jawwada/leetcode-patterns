# Letter Combinations of a Phone Number

*LeetCode 17 · Medium · Pattern: Backtracking over a fixed-depth choice tree (Cartesian product) · Reading time ~6 min*

## The problem

Given a string of digits 2-9, return all letter strings the digits could represent on a phone keypad (2=abc, 3=def,
..., 7=pqrs, 9=wxyz), in any order; empty input gives [].

```text
Example: "23" -> ["ad","ae","af","bd","be","bf","cd","ce","cf"].
```

## What the problem is really asking

Old phone keypads put three or four letters on each digit from 2 to 9. Given a string of digits, list every letter string you could have meant by pressing them: one letter per digit, in order.

```text
 +-------+-------+-------+
 |   1   | 2 abc | 3 def |
 +-------+-------+-------+
 | 4 ghi | 5 jkl | 6 mno |
 +-------+-------+-------+
 |7 pqrs | 8 tuv |9 wxyz |
 +-------+-------+-------+

 digits = "23"
   slot 0 from "abc", slot 1 from "def"
   -> ad ae af bd be bf cd ce cf     (3 x 3 = 9)
```

The answer is a list of strings, all of length n = number of digits. Its size is the product of the alphabet sizes: 3 for most digits, 4 for 7 and 9. That is the Cartesian product of n small alphabets. Every combination is valid, nothing is pruned, and empty input returns `[]`, not `[""]`.

So what is hard? Only one thing: **n is not known when you write the code**. For "23" you would write two nested loops; for "2345" four. You cannot write a variable number of nested loops directly. That is what recursion is for.

## Do it by hand first

With "23" on paper you would write the first letter of 2, then run through 3's letters, then move to the next letter of 2.

```text
 a + d   a + e   a + f       (a fixed, cycle d e f)
 b + d   b + e   b + f       (b fixed, cycle d e f)
 c + d   c + e   c + f       (c fixed, cycle d e f)
```

That is exactly two nested loops, the outer for digit 0, the inner for digit 1. What did your hand keep? The **current prefix** (`a`, then `ad`, back to `a`, then `ae`) and **which digit's letters you are cycling through now**. For three digits you would add a third, innermost cycle. Each digit owns one loop, and the loops are stacked.

## The first honest attempt

A good first answer, and honestly a fine one in Python, builds the answer level by level:

```text
 level = [""]
 digit 2:  ["a", "b", "c"]
 digit 3:  ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

For each digit, replace the list with every existing string extended by every letter. Time O(n · 4^n), space O(4^n). The output itself is 4^n strings of length n, so time cannot improve.

Where is the waste? In memory and copying. Every intermediate level is a full list of separate string objects: 3, then 9, then 27, then 81... each built by copying its whole prefix. When processing the last digit, the entire previous level sits in memory alongside the new one.

```text
 digits "2345", intermediate levels held in memory
 after 2:  3 strings   a b c
 after 3:  9 strings  ad ae af bd ...  prefix "a" copied 3x
 after 4: 27 strings  adg adh adi ... prefix "ad" copied 3x
 after 5: 81 strings   (output)
           ^ the 27 prefixes all exist at once just to be
             extended and discarded
```

This also has no place to stand if a rule arrives ("no two equal adjacent letters", "must be a dictionary word prefix"): you would build the whole level, then filter.

## The turning point

**Claim: the combinations are the leaves of a tree of fixed depth n where level i branches into the letters of `digits[i]`; a depth-first walk needs only the single root-to-leaf prefix in memory, extended and shortened by one letter at a time.**

This is recursion as a variable-depth nested loop. Each call `dfs(i)` *is* the loop for digit i:

```text
 dfs(0): for ch in "abc":          <- outer loop
           path.append(ch)
           dfs(1): for ch in "def":   <- inner loop
                     path.append(ch)
                     dfs(2): record "".join(path)
                     path.pop()
           path.pop()
```

The call stack is the stack of loops. Depth n means n loops. The `path` list is the tuple of current loop variables.

```text
 tree for "23": depth 2, fan-out 3 then 3
                         []
          /              |              \
        a                b                c
     /  |  \          /  |  \          /  |  \
   ad   ae  af      bd   be  bf      cd   ce  cf
```

Compared with the earlier templates: this is pick-from-set where the "set" at level i is not "unused elements" but "letters of digit i". There is no `start` and no `used`, because levels are independent: picking `a` places no restriction on slot 1. And there are no `x` marks anywhere: every branch is a valid answer, so pruning has nothing to cut. Notice that the tree is the same shape for every prefix at a level; that uniformity is what "Cartesian product" means.

The leaf test is `i == len(digits)`; that is where you join the path into a string. Joining costs O(n) per leaf, and building with a list plus `join` avoids allocating a new string at every internal node.

One edge case belongs to the problem, not the technique: with empty digits, the tree is a lone root, which is a leaf, and the walk would return `[""]`. The problem says `[]`, so check for empty input first.

## Watch it work

Example `digits = "23"`. Legend: `*` current path, `<-` current node, `?` not visited. There is no `x` in this problem: no branch is ever invalid.

**Frame 1.** `dfs(0)` picks `a`, `dfs(1)` picks `d`, `dfs(2)` is a leaf: record "ad".

```text
                        *[]
          /              |              \
        *a               ?               ?
     /   |   \
   *ad   ?    ?
    <-
 path=[a,d]  i=2  depth 3   result=["ad"]
```

**Frame 2.** Pop `d`, pick `e`, record; pop `e`, pick `f`, record. Digit 3's loop is done.

```text
                        *[]
          /              |              \
        *a               ?               ?
     /   |   \
   ad    ae  *af
              <-
 path=[a,f]  i=2  depth 3   result=["ad","ae","af"]
```

Digit 1's loop cycled d, e, f under a fixed `a`, exactly like an inner loop.

**Frame 3.** Pop `f`, return to `dfs(0)`, pop `a`, pick `b`. Its subtree records bd, be, bf.

```text
                        *[]
          /              |              \
        a               *b               ?
     /  |  \          /  |  \
   ad   ae  af      bd   be  *bf
                              <-
 path=[b,f]  depth 3   result=[ad,ae,af,bd,be,bf]
```

**Frame 4.** Pop back to the root, pick `c`, record cd, ce, cf. The root's loop ends.

```text
                         []
          /              |              \
        a                b                c
     /  |  \          /  |  \          /  |  \
   ad   ae  af      bd   be  bf      cd   ce  cf
 path=[]  stack empty
 result=[ad,ae,af,bd,be,bf,cd,ce,cf]
```

Nine leaves, in the solution's output order. Throughout, `len(path)` equalled the current call's i, the stack never held more than three frames, and at most one prefix existed in memory at a time.

## Why it is correct

*Invariant.* When `dfs(i)` starts, `path` holds one letter for each of `digits[0..i-1]`, in order. The loop appends a letter of `digits[i]` (now i + 1 letters), calls `dfs(i+1)`, and pops (back to i letters). So the invariant holds at every call and is restored on return.

*Every combination appears.* For any choice of letters `l0 l1 ... l(n-1)` with each `lk` on key `digits[k]`, the loop at depth k tries `lk`, so the path reaches exactly that sequence at depth n, where it is recorded.

*No combination appears twice.* Two different leaves first differ at some depth k, where different letters of the same key were chosen, so their strings differ at position k.

## Cost

- **Time: O(n · 4^n).** At most 4^n leaves, each joined in O(n); internal nodes are fewer than leaves, since every node branches at least 3 ways.
- **Space: O(n)** beyond the output: the path and n + 1 stack frames. The level-by-level version uses O(4^n) for the previous level.

## Variations you will meet

- **Iterative with a queue or itertools.** `["".join(p) for p in product(*(keypad[d] for d in digits))]` is a valid one-liner, and interviewers accept it; be ready to write the recursion if asked "without libraries".
- **Letter Case Permutation (LeetCode 784).** Each letter has two options (lower, upper), digits have one. Same fixed-depth tree with per-position alphabets.
- **Restricted keypad words.** "Only return strings that are dictionary words": put the dictionary in a trie and prune any prefix that is not a trie node. Now the `x` marks appear, and the tree shrinks dramatically.
- **Count only.** The product of alphabet sizes, no walk needed.

## What to carry forward

Recursion is how you write n nested loops when n is a variable: each level owns one position and iterates its own alphabet, and the path is the tuple of loop variables. The next problem keeps a two-letter alphabet, "(" and ")", but each letter is only allowed when two counters say so, so pruning comes back with zero dead ends.
