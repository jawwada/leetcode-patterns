# Copy List with Random Pointer
*LeetCode 138 · Medium · Pattern: Interleaved clone (hash map original -> copy, embedded in the list) · Reading time ~9 min*

## What the problem is really asking

Each node has a value, a `next` pointer, and a `random` pointer that may point to any node in the list or to None. Build a deep copy: a brand-new set of nodes with the same values, where every copied `next` and `random` points to a *copied* node, never back into the original. The original must be left exactly as it was.

The answer is the head of a new list. What makes it hard is the random pointers: when you create the copy of a node, its random target may not have been copied yet, and even if it has, you need a way to get from "original node X" to "the copy of X".

```text
  A, B, C are original nodes; arrows below are random
     A(1) ---> B(2) ---> C(3) ---> None     (next)
     A.random = C
     B.random = A
     C.random = None

  answer: A'(1) -> B'(2) -> C'(3), A'.random = C',
          B'.random = A', C'.random = None
```

## Do it by hand first

On paper you would copy the nodes left to right, writing a new box under each old one. To fill in A'.random, you look at A.random, which is C, and then look *straight down* from C to find C'.

```text
  original:   A      B      C
              |      |      |    "the copy is right below"
  copies:     A'     B'     C'
```

Your hand relied on a translation: given an original node, find its copy. On paper, position does the translating ("right below"). In memory, nodes have no "below". We need a translator, and the whole problem is about where to keep it.

## The first honest attempt

Copy the list using `next` only. Then, for each original node X with a random target T, find T's position by walking the original from the head and counting steps, then walk the copy the same number of steps to find T'. O(n^2) time, O(1) extra space.

```text
  set A'.random: walk A, B, C   -> index 2; walk A', B', C'
  set B'.random: walk A         -> index 0; walk A'
  ...
  every random costs two walks from the head
```

The repeated work is the translation. "Which copy corresponds to this original?" is answered from scratch, by linear search, once per node. But that correspondence never changes after the clones exist.

## The turning point

**Claim: the original-to-copy correspondence is a fixed function, so compute it once and look it up in O(1); and you can store it inside the list itself by placing each copy immediately after its original.**

The first half of the claim gives the hash-map solution. Pass 1: create a clone for every node and store `copy[X] = X'`. Pass 2: for every X, set `X'.next = copy[X.next]` and `X'.random = copy[X.random]`, with `copy[None] = None`. O(n) time and O(n) space. That is a perfectly good interview answer.

The second half removes the map. Where can we put "the copy of X" so that, given X, it is found in O(1) without a dictionary? Right after X. Weave the copies in:

```text
  A -> A' -> B -> B' -> C -> C' -> None

  copy of X  ==  X.next          (the map, embedded)
```

Now the translation is a pointer hop. To set the random of A', look at A.random (which is C) and take one step: C.next is C'. In one line:

```text
  X.next.random = X.random.next     (if X.random is not None)
  ^ X'               ^ copy of X's random target
```

Finally, unweave: walk the woven list two nodes at a time, sending each original's `next` to the next original and each copy's `next` to the next copy. This restores the original list exactly and leaves the copies as their own list.

Three passes, each a simple walk. The order matters: all copies must exist before any random is set (the target's copy has to be there to hop to), and all randoms must be set before unweaving (once unwoven, `X.next` is no longer the copy).

## Watch it work

Original `A(1) -> B(2) -> C(3)` with `A.random = C`, `B.random = A`, `C.random = None`.

Frame 1 — the original.

```text
  next:    A(1) -> B(2) -> C(3) -> None
  random:  A ~> C     B ~> A     C ~> None
```

Nothing copied yet; `~>` marks a random pointer.

Frame 2 — weave.

```text
  A -> A' -> B -> B' -> C -> C' -> None
       1          2          3
  A'.random, B'.random, C'.random = None (not set yet)
```

Each clone was created with its original's value and its original's old next, then the original was pointed at it.

Frame 3 — set randoms.

```text
  X = A: A.random = C   -> A'.random = C.next = C'
  X = B: B.random = A   -> B'.random = A.next = A'
  X = C: C.random = None -> skip

  A -> A' -> B -> B' -> C -> C' -> None
       A' ~> C'   B' ~> A'   C' ~> None
```

Each copy's random was found by one hop past its original's random target.

Frame 4 — unweave.

```text
  node = A: A.next = A'.next = B ; A'.next = B.next = B'
  node = B: B.next = B'.next = C ; B'.next = C.next = C'
  node = C: C.next = C'.next = None ; C'.next is None

  originals: A -> B -> C -> None
  copies:    A' -> B' -> C' -> None
```

The two lists are separated; the original's links are exactly what they were in Frame 1.

Frame 5 — result.

```text
  return A'
  A'(1) -> B'(2) -> C'(3) -> None
  A' ~> C'    B' ~> A'    C' ~> None
```

Same shape as the original, no shared nodes.

Across Frames 2 to 4 one fact held throughout the weaving phase: for every original X, `X.next` was X's copy. That embedded map is what made every random assignment a single hop.

## Why it is correct

After the weave, for every original X, X.next is a new node X' with X's value, and X'.next is the next original (or None). That is the invariant "X.next is copy(X)".

In the random pass, for each X with random target T, we set X'.random = T.next. By the invariant T.next = copy(T) = T', which is exactly the deep-copy requirement. If T is None we leave None. Because we step `X = X.next.next`, we visit each original once and never treat a copy as an original.

In the unweave pass, at original X: X.next becomes X'.next, which is the next original, restoring the original link; X'.next becomes the next original's next, which is the next copy. Each original and each copy gets its `next` fixed exactly once, so both lists come out intact and disjoint, and the copies' random pointers, set in the previous pass, all point at copies.

## Cost

- **Time: O(n).** Three linear passes: weave, randoms, unweave.
- **Space: O(1) extra.** Apart from the n new nodes, which are the output, only a few pointers.
- The hash-map version is O(n) time and O(n) extra space for the map; the brute force is O(n^2) time.

## Variations you will meet

- **Clone Graph (LeetCode 133).** The same translator problem on a general graph. There is no list to weave into, so you use the hash map, filled during BFS or DFS; the map doubles as the visited set.
- **Copy a binary tree with random pointers (LeetCode 1485).** Hash map from original to clone during a traversal, then wire randoms in a second pass, or lazily on first sight.
- **"Do it in one pass."** With a map, create clones on demand: when you need copy[T] and it does not exist yet, create it then. Each node is created once, whoever asks first.
- **Interviewer forbids modifying the input even temporarily.** The weave touches the original's links, so fall back to the hash map.

## What to carry forward

A deep copy is a translation from old pointers to new ones; keep the translator in a map, or weave it into the structure so the copy of X is X.next. The last problem, Reverse Nodes in k-Group, brings back the very first trick of the chapter, reversal, and asks you to perform it many times in a row while stitching the reversed pieces together.
