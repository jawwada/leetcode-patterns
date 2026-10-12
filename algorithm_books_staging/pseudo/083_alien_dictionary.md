---
rank: 83
slug: alien_dictionary
---

A list of words is sorted by the rules of an unknown alphabet. Return the letters that appear in the words, arranged in an alphabet order that sorts the list, or the empty string if no alphabet can. From `["wrt", "wrf", "er", "ett", "rftt"]` the only possible order is `"wertf"`.

The brute force tries every arrangement of the letters and checks whether it sorts the list, `U!` arrangements for `U` distinct letters. Everything the list says about the alphabet sits between neighbors. Two adjacent words agree up to some position, and the first letters that differ are in alphabet order: `wrt` before `wrf` says only that `t` comes before `f`. The letters after that position say nothing, and words further apart add nothing the adjacent pairs do not already imply, because sorted order is transitive. So each adjacent pair yields at most one edge `before → after` between two letters, and the alphabet is a topological order of that letter graph, which Kahn's algorithm (#40) produces by repeatedly placing a letter that has nothing left in front of it.

Two kinds of input have no answer. A cycle among the letters, as in `["z", "x", "z"]`, leaves letters whose indegree never reaches zero, so fewer letters come out than went in. A word followed by its own proper prefix, `abc` before `ab`, breaks the rule that a prefix sorts first, and since no edge can express that, the pair check rejects it directly. When the queue holds several letters at once, any of them may go next, so many alphabets can be right: `["ab", "ac", "d"]` only says that `b` precedes `c` and `a` precedes `d`, and six orders satisfy both. Starting the queue from the letters in sorted order makes the answer repeatable.

```text
adjacent pair   first difference    edge
wrt   wrf       index 2: t ≠ f      t → f
wrf   er        index 0: w ≠ e      w → e
er    ett       index 1: r ≠ t      r → t
ett   rftt      index 0: e ≠ r      e → r

graph  w → e → r → t → f       indegree  w 0, r 1, t 1, f 1, e 1

pop   order    queue after
 -    ""       [w]          only w has nothing in front of it
 w    w        [e]
 e    we       [r]
 r    wer      [t]
 t    wert     [f]
 f    wertf    []           all 5 letters placed: no cycle
```

```pseudo
FUNCTION AlienOrder(words)
    graph ← empty map                      // letter → letters after it
    indegree ← empty map                   // letter → letters still before it
    FOR EACH word IN words
        FOR EACH letter IN word
            IF letter NOT IN graph
                graph[letter] ← empty list
                indegree[letter] ← 0
    FOR i FROM 0 TO len(words) - 2
        IF NOT AddEdge(words[i], words[i + 1], graph, indegree)
            RETURN ""                      // a word came before its own prefix
    RETURN TopologicalOrder(graph, indegree)

FUNCTION AddEdge(first, second, graph, indegree)
    FOR j FROM 0 TO min(len(first), len(second)) - 1
        before ← first[j]
        after ← second[j]
        IF before ≠ after
            IF after NOT IN graph[before]  // count each edge once
                graph[before].append(after)
                indegree[after] ← indegree[after] + 1
            RETURN true                    // later letters say nothing
    RETURN len(first) ≤ len(second)        // "abc" before "ab" is impossible

FUNCTION TopologicalOrder(graph, indegree)
    queue ← empty queue
    FOR EACH letter IN sorted(keys of indegree)    // a repeatable answer
        IF indegree[letter] = 0
            queue.enqueue(letter)
    order ← empty list
    WHILE queue is not empty
        letter ← queue.dequeue()
        order.append(letter)
        FOR EACH after IN graph[letter]
            indegree[after] ← indegree[after] - 1  // one fewer before it
            IF indegree[after] = 0
                queue.enqueue(after)
    IF len(order) < len(indegree)
        RETURN ""                          // the rest sit on a cycle
    RETURN join(order, "")
```

Comparing neighbors reads each letter of the input at most twice, and the graph holds at most 26 letters, so the whole run is `O(C)` for `C` letters in all the words. Reach for this whenever a sorted list must reveal the order that sorted it, or whenever "comes before" facts must be assembled into one sequence. Checking a proposed alphabet is the easy half, LC 953, which compares each adjacent pair by letter ranks. The classic mistake is reading past the first difference: it turns `["ab", "ba"]` into the false cycle `a → b → a` and reports no alphabet, when `ab` is the answer. Forgetting the prefix rule is the other one, and it returns `abc` for `["abc", "ab"]` instead of the empty string.

*Practice:* LC 269 Alien Dictionary · LC 953 Verifying an Alien Dictionary · LC 210 Course Schedule II · LC 444 Sequence Reconstruction
