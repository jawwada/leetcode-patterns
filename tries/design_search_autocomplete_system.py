"""
Design Search Autocomplete System (LeetCode 642)  — Hard
Pattern: Trie with per-node frequency map + cursor that follows keystrokes

Problem
-------
AutocompleteSystem(sentences, times) seeds a history where sentences[i]
was typed times[i] times. input(c) receives one character of the sentence
being typed: if c is "#" the sentence is complete, its count goes up by
one and [] is returned; otherwise return up to 3 historical sentences
that start with everything typed so far, ordered by count descending,
ties broken by ASCII order.
Example: history {"i love you":5, "island":3, "ironman":2, "i love
leetcode":2}; input("i") -> ["i love you","island","i love leetcode"];
input(" ") -> ["i love you","i love leetcode"]; input("a") -> [];
input("#") -> [] and "i a" is now in the history with count 1.

Brute force
-----------
Keep a dict sentence -> count and the string typed so far. On every
keystroke scan all S sentences, keep those that startswith the prefix,
sort by (-count, sentence) and return 3. O(S * L + S log S) per keystroke,
O(S * L) space. The wasted work is the full scan: typing "i love y"
rescans every sentence 8 times, although after the first letter only the
sentences under the prefix "i" could ever match again, and each
keystroke merely narrows the previous keystroke's candidate set.

From brute force to optimal
---------------------------
Prefix narrowing is exactly what a trie models: the node for prefix p has
the node for p + c as a child, so the system can keep a CURSOR into the
trie that moves one edge per keystroke instead of rescanning. To avoid
walking the subtree below the cursor on each query, store at every node a
small map sentence -> count for all sentences passing through it; a
query is then "take the top 3 of the map at the cursor" (heapq.nsmallest
on (-count, sentence) is O(m log 3) for m sentences under the prefix).
Inserting a finished sentence bumps the count in every node along its
path, O(L). Once a keystroke leaves the trie the cursor becomes None and
stays dead until "#" resets it. Space grows to O(S * L^2) in the worst
case (each sentence appears in the map of each of its L prefix nodes),
which is the trade for O(L) per-keystroke work.

Intuition
---------
Autocomplete is a conversation with a prefix that only ever grows until
the user hits "#". A trie is the one structure where "grow the prefix by
one letter" is a single pointer step, and caching the ranked candidates
at each node means the step also delivers the answer.

Geometric view
--------------
Draw the trie as a branching diagram with the cursor as a marker that
slides down one edge per keystroke. Every node is annotated with the
sentences that flow through it and their counts; the three heaviest
annotations at the marker are the suggestions. Pressing "#" walks the
typed path once more, incrementing counts, then lifts the marker back to
the root.

Steps
-----
1. _add(sentence, t): walk/create the trie path; at each node do
   node["$"][sentence] += t.
2. __init__: _add every seeded sentence; cursor = root; typed = [].
3. input(c) with c == "#": _add("".join(typed), 1); reset cursor and
   typed; return [].
4. Otherwise append c to typed; cursor = cursor.get(c) (None if dead).
5. If cursor is None return []; else return the 3 smallest items of
   cursor["$"] by key (-count, sentence).

Complexity: O(L + m log 3) per keystroke, O(S * L^2) space — one pointer
step plus a top-3 selection over the m sentences under the prefix;
every sentence is recorded in each of its L prefix nodes.
Pitfalls: sorting by count only (ties must be ASCII ascending); not
resetting the cursor after "#"; continuing to walk from a dead cursor;
treating the typed-so-far string as a sentence before "#" arrives.
"""
import heapq
from typing import Dict, List


class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.root: Dict = {"$": {}}               # child chars -> node; "$" -> {sentence: count}
        for sentence, count in zip(sentences, times):
            self._add(sentence, count)
        self.cursor: Dict = self.root             # trie node for the prefix typed so far (None = dead)
        self.typed: List[str] = []

    def _add(self, sentence: str, count: int) -> None:
        node = self.root
        for ch in sentence:
            node = node.setdefault(ch, {"$": {}})
            node["$"][sentence] = node["$"].get(sentence, 0) + count   # every prefix node records it

    def input(self, c: str) -> List[str]:
        if c == "#":
            self._add("".join(self.typed), 1)
            self.cursor, self.typed = self.root, []
            return []
        self.typed.append(c)
        if self.cursor is not None:
            self.cursor = self.cursor.get(c)      # one pointer step per keystroke
        if self.cursor is None:
            return []
        top = heapq.nsmallest(3, self.cursor["$"].items(), key=lambda kv: (-kv[1], kv[0]))
        return [sentence for sentence, _ in top]


class BruteForce:
    """Flat dict sentence -> count; every keystroke rescans and re-sorts all sentences: O(S*L + S log S)."""

    def __init__(self, sentences: List[str], times: List[int]):
        self.counts = dict(zip(sentences, times))
        self.typed = ""

    def input(self, c: str) -> List[str]:
        if c == "#":
            self.counts[self.typed] = self.counts.get(self.typed, 0) + 1
            self.typed = ""
            return []
        self.typed += c
        matches = [s for s in self.counts if s.startswith(self.typed)]   # full rescan per keystroke
        matches.sort(key=lambda s: (-self.counts[s], s))
        return matches[:3]


if __name__ == "__main__":
    import random

    sentences = ["i love you", "island", "iroman", "i love leetcode"]
    times = [5, 3, 2, 2]
    ac = AutocompleteSystem(sentences, times)
    assert ac.input("i") == ["i love you", "island", "i love leetcode"]
    assert ac.input(" ") == ["i love you", "i love leetcode"]
    assert ac.input("a") == []
    assert ac.input("#") == []
    assert ac.input("i") == ["i love you", "island", "i love leetcode"]   # "i a" (count 1) not yet in top 3
    assert ac.input(" ") == ["i love you", "i love leetcode", "i a"]
    assert ac.input("a") == ["i a"]
    assert ac.input("#") == []                                       # "i a" now has count 2
    assert ac.input("z") == []                                       # dead prefix stays dead until '#'
    assert ac.input("i") == []
    assert ac.input("#") == []
    assert ac.input("i") == ["i love you", "island", "i a"]          # reset after '#'; "i a" wins the tie at 2 by ASCII

    rng = random.Random(642)
    alphabet = "ab "
    pool = ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4))) for _ in range(6)]
    pool = list(dict.fromkeys(pool))                                 # distinct seed sentences
    seeds = [rng.randint(1, 4) for _ in pool]
    fast, slow = AutocompleteSystem(pool, seeds), BruteForce(pool, seeds)
    for _ in range(600):
        c = "#" if rng.random() < 0.25 else rng.choice(alphabet)
        assert fast.input(c) == slow.input(c), c
    print("ok")
