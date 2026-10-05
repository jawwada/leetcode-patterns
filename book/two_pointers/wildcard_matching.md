# Wildcard Matching
*LeetCode 44 · Hard · Pattern: Greedy two pointers with last-star backtrack · Reading time ~12 min*

## The problem

Given a string s and a pattern p where '?' matches any single character and '*' matches any sequence of characters
including the empty one, decide whether p matches all of s.

```text
Example: s = "adceb", p = "*a*b" -> True ("" a "dce" b). s =
  "acdcb", p = "a*c?b" -> False.
```

## What the problem is really asking

You get a text `s` and a pattern `p`. In the pattern, `?` matches exactly one character of any kind, and `*` matches any sequence of characters, including the empty one. Every other pattern character matches only itself. Does the pattern match the **whole** text?

The answer is a boolean. Without stars this would be trivial: walk both strings in lockstep and compare. Every `*` adds a choice, "how many characters do I swallow?", and with k stars the choices multiply. The challenge is to show that most of those choices never need to be revisited.

```text
s = "adceb"       p = "*a*b"

  s:   a  d  c  e  b
       |  \_____/  |
  p: * a     *     b
     ^ "" (empty)
                         match: True

s = "acdcb"       p = "a*c?b"   -> False
```

## Do it by hand first

Take `s = "abcabd"` and `p = "a*bd"`. Read the pattern piece by piece. `a` must match `s[0]`, fine. Then `*`: you do not decide how much it eats yet; you just remember "a star started at text position 1". Next, try to match `bd` right away: `b` matches `s[1]`, but `d` does not match `s[2] = c`. So the star must eat more. Let it eat `b`, and retry `bd` from text position 2: `c` is not `b`. Eat `bc`, retry from 3: `a` is not `b`. Eat `bca`, retry from 4: `b` matches, `d` matches, end of both. True.

```text
s:  a  b  c  a  b  d
p:  a  *  b  d
    |  |
    |  star eats: ""   -> "bd" vs "bc"  fail
    |             "b"  -> "bd" vs "ca"  fail
    |             "bc" -> "bd" vs "ab"  fail
    |             "bca"-> "bd" vs "bd"  ok
```

What did you keep track of? Your place in the text, your place in the pattern, and one bookmark: "where the last star is, and how much it has eaten". You never once went back to rethink an earlier star, and you will see why that is safe.

## The first honest attempt

Recursion. Compare the first characters; if the pattern starts with `*`, try both "star eats nothing" (drop the star) and "star eats one character" (drop a text character, keep the star). Return True if either branch does.

```text
match(s, p):
  p empty         -> s empty?
  p[0] == '*'     -> match(s, p[1:]) or match(s[1:], p)
  p[0] fits s[0]  -> match(s[1:], p[1:])
  else            -> False
```

It is correct and exponential. With k stars, the stars can split the text in O(n^k) ways, and the recursion explores them. The repeated work is visible on a tiny failing case: `s = "aab"`, `p = "*a*c"`. The recursion makes 18 calls, and the subproblem "match `b` against `*c`" is solved twice, once for each way the first star split the text.

```text
              (aab, *a*c)
             /           \
     (aab, a*c)         (ab, *a*c)    first star
         |               /      \     eats "" / "a"
     (ab, *c)      (ab, a*c)   (b, *a*c)
      /     \          |
 (ab, c)  [b, *c]   [b, *c]   <- same subproblem,
             |          |        solved again
          (b, c) ...  (b, c) ...
```

**Level 1** is memoising this recursion on `(i, j)`, the 2D dynamic programming table. O(n * m) time and space. It is a correct answer, and many interviewers accept it. But it fills a whole table, and the question underneath is: why remember every split of every star, when you only needed one bookmark by hand?

## The turning point

**Claim: when a mismatch happens after one or more stars, only the most recent star ever needs to eat more. Earlier stars can stay exactly as the greedy left them.**

Here is the argument, built in two steps.

**Step 1: the greedy places every star at its earliest possible text position.** Split the pattern at its stars into star-free segments: `p = seg0 * seg1 * seg2 ...`. `seg0` has no choice; it must match the start of the text exactly. After a star, the greedy tries to match the next segment at text position `match`, then `match + 1`, then `match + 2`, and so on, taking the first position where the whole segment fits before the next star. Trying positions in increasing order means the next star is reached at the **leftmost** text position any matching could reach it.

**Step 2: leftmost is never worse.** Suppose some full matching places the last star's start at text position `m'`, and the greedy placed it at `m <= m'`. In that matching, the star eats `s[m'..q-1]` and the rest of the pattern matches `s[q..]`. In the greedy's configuration the same star can simply eat `s[m..q-1]`, a longer stretch, and the rest of the pattern still matches `s[q..]` unchanged. So whatever an alternative choice for earlier stars could achieve, the most recent star can achieve from the greedy's position by eating more. Re-deciding an earlier star is never needed. Earlier stars are **dominated** by the latest one.

```text
alternative:  [ earlier stuff ]*[eats.....][rest]
                               m'          q
greedy:       [ earlier ]*[eats............][rest]
                         m                  q
same [rest] at q; the greedy's star just eats more
```

That collapses the recursion into two pointers and one bookmark:

- `i` walks the text, `j` walks the pattern.
- `star` is the index of the last `*` in `p` (or -1 if none yet).
- `match` is the text index where that star's swallowed stretch ends, i.e. where the pattern after the star is currently being tried.

The rules, in order:

1. `p[j]` is `s[i]` or `?`: advance both.
2. `p[j]` is `*`: record `star = j`, `match = i`, advance `j` only (the star eats nothing for now).
3. Mismatch and a star exists: the star eats one more character. `match += 1`, `i = match`, `j = star + 1`.
4. Mismatch and no star: return False.

When the text is used up, any remaining pattern must be all stars (they eat nothing). Return True if `j` reaches the end after skipping them.

The bookmark `match` only moves right, and it is the key to the cost bound below. It is also why this belongs in a two-pointer chapter: like every problem before it, each failed attempt permanently discards a candidate (one more starting position for the post-star segment), and a dominance fact guarantees nothing discarded could have helped.

## Watch it work

`s = "abcabd"`, `p = "a*bd"`. Top rail is the text with `i` and the bookmark `m` (match); bottom rail is the pattern with `j` and `S` (star).

Frame 1. `p[0] = 'a'` equals `s[0]`. Advance both: `i = 1`, `j = 1`.

```text
 s:  a  b  c  a  b  d
        i
 p:  a  *  b  d
        j            star=-1
```

Frame 2. `p[1] = '*'`. Record `star = 1`, `match = 1`; advance `j` to 2. The star eats nothing so far.

```text
 s:  a  b  c  a  b  d
        i
        m
 p:  a  *  b  d
        S  j         star=1 match=1
```

Frame 3. `p[2] = 'b'` equals `s[1]`. Advance both: `i = 2`, `j = 3`.

```text
 s:  a  b  c  a  b  d
        m  i
 p:  a  *  b  d
        S     j      star=1 match=1
```

Frame 4. `p[3] = 'd'` vs `s[2] = 'c'`: mismatch. Backtrack to the star: `match = 2`, `i = 2`, `j = 2`. The star now eats `"b"`.

```text
 s:  a  b  c  a  b  d
           i
           m         star eats "b"
 p:  a  *  b  d
        S  j         star=1 match=2
```

Frame 5. `p[2] = 'b'` vs `s[2] = 'c'`: mismatch. Star eats one more: `match = 3`, `i = 3`, `j = 2`.

```text
 s:  a  b  c  a  b  d
              i
              m      star eats "bc"
 p:  a  *  b  d
        S  j         star=1 match=3
```

Frame 6. `p[2] = 'b'` vs `s[3] = 'a'`: mismatch. `match = 4`, `i = 4`, `j = 2`.

```text
 s:  a  b  c  a  b  d
                 i
                 m   star eats "bca"
 p:  a  *  b  d
        S  j         star=1 match=4
```

Frame 7. `p[2] = 'b'` equals `s[4]`, then `p[3] = 'd'` equals `s[5]`. `i = 6` (end of text), `j = 4` (end of pattern). No trailing stars to skip; `j == len(p)`: True.

```text
 s:  a  b  c  a  b  d
                 m     i (end)
 p:  a  *  b  d
        S        j (end)
 result: True
```

Across the frames, `match` moved only rightward (1, 2, 3, 4), and every backtrack returned `j` to exactly `star + 1`, never to the star itself and never to an earlier part of the pattern.

## Why it is correct

**If it returns True, the match is real.** Every advance either pairs a pattern character with a text character it legally matches, or assigns a stretch of text to a star. When the loop ends, the text is consumed and the pattern's leftovers are stars eating nothing. That is a valid assignment.

**If a match exists, it returns True.** Consider the segments between stars. By Step 1 the greedy reaches each star at the leftmost possible text position, because it tries post-star positions in increasing order and stops at the first that fits the whole next segment. By Step 2 a leftmost placement never rules out a match that a later placement allows. So if a valid matching exists, the greedy reaches the last star no later than that matching does, and from there trying `match`, `match + 1`, ... eventually hits the matching's choice.

**It always terminates.** Every loop iteration either advances `i`, advances `j` past a star, or advances `match`. `match` never exceeds the text length, and between two backtracks `i` and `j` only move forward. So the loop ends, and by the first point it can only answer True when a real match exists.

A tempting bug is resetting `j` to `star` instead of `star + 1`. That re-reads the `*`, which sets `match = i` again, and the bookmark stops advancing: an infinite loop.

## Cost

- Recursion: exponential time in the number of stars, O(n + m) stack.
- Level 1, DP over `(i, j)`: O(n * m) time and O(n * m) space (O(m) with a rolling row).
- Level 2, greedy two pointers: O(n * m) time in the worst case, O(1) space. Each backtrack moves `match` right by one (at most n times) and then rescans at most the pattern segment after the star (at most m characters). On typical inputs it is close to O(n + m).

## Variations you will meet

- **Regular Expression Matching (LeetCode 10)**: `*` repeats the **previous** element, and `.` is the single-character wildcard. The dominance argument fails, because `a*` can only eat `a`s, so a later star cannot always imitate an earlier one. Use DP over `(i, j)`.
- **Glob with character classes (`[abc]`)**: rule 1 becomes "does `s[i]` belong to the class". The star logic is unchanged.
- **Count matches, or return the star assignments**: the greedy finds one assignment, the leftmost. Counting all of them needs the DP table.
- **Many patterns against one text**: build an automaton (or a trie of patterns) instead of running the greedy per pattern.

## What to carry forward

When backtracking only ever needs the latest choice point, because the latest choice dominates every earlier one, a whole recursion tree collapses into two pointers and one bookmark that only moves forward. That is the chapter's argument in its most general form: each step discards a candidate for good, and a monotone or dominance fact proves nothing discarded could have mattered.
