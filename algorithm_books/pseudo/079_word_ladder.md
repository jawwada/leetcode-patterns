---
rank: 79
slug: word_ladder
---

Turn `begin_word` into `end_word` by changing one letter at a time, where every word after the first must come from `word_list`. Return the number of words in the shortest such ladder, or `0` if there is none. From `hit` to `cog` with the list `hot, dot, dog, lot, log, cog`, one shortest ladder is `hit → hot → dot → dog → cog`, so the answer is `5`.

The words are the nodes of a graph that is never written down: two words are joined when they differ in exactly one letter, and the question is a shortest path in that graph, which is BFS (#39). Building the graph by comparing every pair of words costs `O(n² · L)` for `n` words of length `L`. Generating neighbors on demand is cheaper for a large dictionary: change each of the `L` positions to each of the 26 letters and keep the candidates that are unvisited dictionary words. The set of unvisited words does double duty. It is the dictionary, so a string that is not a word never becomes a neighbor, and it is the visited mark, because a word is removed the moment it is enqueued and can never enter the queue twice. Each queue entry carries the length of the ladder that reached it, and the first time `end_word` leaves the queue, that length is the answer.

Picture BFS rings around `hit`, one ring per changed letter. The pattern beside each step names the position that changed: `hot` and `dot` and `lot` all match `*ot`, which is why they sit one step apart. Grouping the dictionary by such patterns ahead of time, `*ot → [hot, dot, lot]`, is the other standard way to find neighbors.

```text
  hit ── hot ─┬─ dot ── dog ── cog      cog is end_word
              └─ lot ── log
   1      2       3      4      5       words in the ladder

pop (hit, 1)   h*t → hot          queue (hot, 2)
pop (hot, 2)   *ot → dot, lot     queue (dot, 3) (lot, 3)
pop (dot, 3)   do* → dog          queue (lot, 3) (dog, 4)
pop (lot, 3)   lo* → log          queue (dog, 4) (log, 4)
pop (dog, 4)   *og → cog          queue (log, 4) (cog, 5)
pop (log, 4)   nothing new        queue (cog, 5)
pop (cog, 5)   it is end_word: return 5
```

```pseudo
FUNCTION LadderLength(begin_word, end_word, word_list)
    unvisited ← set(word_list)             // dictionary words not reached yet
    IF end_word NOT IN unvisited
        RETURN 0
    IF begin_word IN unvisited
        unvisited.remove(begin_word)       // the start counts as reached
    queue ← empty queue
    queue.enqueue((begin_word, 1))         // (word, words in the ladder)
    WHILE queue is not empty
        (word, length) ← queue.dequeue()
        IF word = end_word
            RETURN length
        FOR i FROM 0 TO len(word) - 1
            FOR EACH letter IN "abcdefghijklmnopqrstuvwxyz"
                candidate ← word with position i replaced by letter
                IF candidate IN unvisited          // a word not reached yet
                    unvisited.remove(candidate)    // mark when enqueued
                    queue.enqueue((candidate, length + 1))
    RETURN 0
```

Each word is enqueued at most once and tries `26 · L` candidates that each cost `O(L)` to build and look up, so the search takes `O(n · 26 · L²)` time and `O(n · L)` space. Reach for BFS on an implicit graph whenever the states are strings, lock combinations or board positions and one move changes a state a little: Open the Lock turns one wheel per move, and Minimum Genetic Mutation changes one gene letter. Bidirectional BFS grows one frontier from each end, always expanding the smaller, and stops when they touch; with `b` neighbors per word and a ladder of `d` steps it explores about `2 · b^(d/2)` words instead of `b^d`. Word Ladder II wants every shortest ladder, so it records each word's parents from the previous layer and walks them back from `end_word`. The classic mistake is counting changes instead of words: starting the length at 0 answers 4.

*Practice:* LC 127 Word Ladder · LC 126 Word Ladder II · LC 752 Open the Lock · LC 433 Minimum Genetic Mutation
