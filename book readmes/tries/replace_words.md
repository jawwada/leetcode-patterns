# Replace Words
*LeetCode 648 · Medium · Pattern: Trie (prefix tree) · Reading time ~6 min*

## The problem

Given a dictionary of roots and a sentence, replace every word that starts with a root by its shortest such root.

```text
Example: dictionary=[cat,bat,rat], sentence="the cattle was
  rattled by the battery" -> "the cat was rat by the bat".
```

## What the problem is really asking

You get a dictionary of short "roots" and a sentence. Every word in the sentence that begins with some root must be replaced by that root; if several roots fit, use the shortest one. Words that begin with no root stay as they are. The answer is the rewritten sentence, one output word per input word.

So for each sentence word, the question is: *among all roots, which is the shortest one that is a prefix of this word?* That is a prefix question asked in the opposite direction from Implement Trie. There we asked "does any stored word start with this query?"; here we ask "does this query start with any stored root?".

```text
 roots: cat, ca, bat
 sentence:  cattle   bat   bark
              |       |      |
 roots fit:  ca,cat  bat   (none)
 shortest:   ca      bat    bark   (kept)
 answer:  "ca bat bark"
```

What makes it hard is scale: thousands of roots and a long sentence. Testing each word against each root multiplies the two.

## Do it by hand first

Take `cattle`. With the roots written down, you would read `cattle` from the left and keep asking "have I just spelled a root?".

```text
 read:   c      ca      cat     catt
 root?   no     YES     (yes)   ...
                 ^
                 stop: first hit is the shortest
```

Two things your hand did deserve names. First, you read the word once, left to right, and checked all roots *at the same time* — you did not try `cat` and then separately try `ca`. Second, the first time you saw a complete root, you stopped, because every later hit would be longer. And for `bark` you could stop even sooner: after `bar`, no root starts with `bar`, so nothing further can match.

The thing you kept track of was "which roots still agree with what I have read so far, and has one of them just ended?". That is exactly a position in a trie of roots.

## The first honest attempt

For each sentence word, loop over every root, test `word.startswith(root)`, and keep the shortest match.

Cost: O(W · D · L) for W sentence words, D roots, L the maximum length. The repeated work shows up as soon as roots share letters:

```text
 word "cattle" against roots
   cat : c=c a=a t=t      match
   ca  : c=c a=a          match   <- re-reads "c","a"
   bat : b?c              fail
 word "cattlex" next ... same three tests again
```

The letters `c`, `a` of `cattle` are compared once per root that starts with `ca`. Roots that start with a different letter are still visited, just to fail on their first character. The answer depends on the word's prefixes, not on each root separately.

## The turning point

**Claim: put the roots in a trie; walking the word down it tests the word against every root simultaneously, and the first end marker on the walk is the shortest root.**

Why it is true. The node reached after reading `word[:i]` exists iff some root begins with `word[:i]` (the trie invariant). So at every step the walk represents exactly the roots still in play. If that node carries a marker, then `word[:i]` is itself a root — and it is a prefix of the word, because we spelled it from the word. Since we read i = 1, 2, 3, ... in increasing order, the first marked node we meet is the shortest such root. If the walk falls off (the next letter has no edge), no root extends the current prefix, so no longer root can match either: keep the word.

```text
 trie of roots cat, ca, bat
       (root)
       /    \
      c      b
      |      |
      a*     a
      |      |
      t*     t*
```

The algorithm per word is therefore three outcomes, checked in this order at each letter:

1. next letter has no edge: return the word unchanged;
2. step down; if the new node has `"$"`: return `word[:i+1]`;
3. otherwise continue; if the word runs out without a marker, return it unchanged.

The order inside step 2 matters: descend first, *then* look for the marker. Checking `"$"` at the root before reading anything would match an empty root, which does not exist but is an easy off-by-one to write.

A neat consequence: the root `cat` is never even reached for `cattle`, because `ca` stops the walk first. Longer roots behind a shorter one are dead weight, and the walk ignores them for free.

## Watch it work

Roots `cat`, `ca`, `bat`; sentence `cattle bat bark`. Running the solution gives `ca bat bark`.

**Frame 1** — the trie after inserting the roots. `ca` marks the middle of the `cat` path.

```text
 {"c":{"a":{"$":T,"t":{"$":T}}},
  "b":{"a":{"t":{"$":T}}}}
       (root)
       /    \
      c      b
      a*     a
      t*     t*
```

**Frame 2** — word `cattle`: read `c` (no marker), read `a`: the node has `"$"`. Return `word[:2]` = `ca`.

```text
 cattle
 ^^          node: root>c>a*   marker -> "ca"
 i=1         letters t,t,l,e never read
```

**Frame 3** — word `bat`: `b` no marker, `a` no marker, `t` marker. Return `bat`.

```text
 bat
 ^^^         node: root>b>a>t*  -> "bat"
 i=2
```

**Frame 4** — word `bark`: `b`, `a` fine; `r` is not a child of `ba`. The walk falls off; keep `bark`.

```text
 bark
 ^^x         node: root>b>a, no edge "r"
             -> keep "bark"
 output so far: "ca bat bark"
```

At every frame the current node stood for exactly the roots that agreed with the letters read; a marker meant one of them had just been completed, and falling off meant none could.

## Why it is correct

Invariant along a walk: after i letters, the current node exists iff some root begins with `word[:i]`, and it is marked iff `word[:i]` is a root. The walk visits i = 1, 2, ... in increasing order and stops at the first marked node, so the root it returns is a prefix of the word and no shorter root exists (a shorter one would have been marked earlier and stopped the walk). If it falls off at length i, no root begins with `word[:i]`, so no root of length i or more is a prefix of the word, and none shorter was marked — keeping the word is correct. If the word ends without a marker, every root that is a prefix of the word would have been seen; there were none.

## Cost

- **Time:** O(total root characters + total sentence characters) — building inserts each root letter once; each word walks at most its own length (often far less, since it stops at the first marker).
- **Space:** O(total root characters) for the trie, plus the output string.

The brute force was O(W · D · L); the trie removes the factor D entirely.

## Variations you will meet

- **Longest root instead of shortest.** Do not stop at the first marker; remember the last marked depth and keep walking until you fall off or the word ends.
- **Prune the dictionary during build.** When inserting `cat` after `ca` exists, you can stop as soon as you pass a marked node, since `cat` can never be chosen. A small speed-up, same answer.
- **Hash-set alternative.** Put roots in a set and test `word[:1]`, `word[:2]`, ... in order. Correct and short, but each slice costs O(i), so a word costs O(L²); the trie makes it O(L).
- **Longest word in dictionary (LeetCode 720).** Same "walk and look at markers" idea: a word counts only if every prefix along its path is marked.

## What to carry forward

Walking one string down a trie compares it against every stored string at once, and "first marker on the path" means "shortest stored prefix". The next problem keeps the walk but lets the query contain wildcards, so the single path becomes a branching search.
