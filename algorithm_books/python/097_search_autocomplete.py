"""
Design Search Autocomplete System - Walk a Trie, Rank the Top 3

Seed past sentences with counts; input(c) takes one keystroke and returns the
3 hottest past sentences that start with everything typed so far (count first,
ties in ASCII order), and '#' records the sentence. With i love you 5, island 3,
iroman 2, i love leetcode 2: input("i") -> i love you, island, i love leetcode.
"""


# --- helpers ---
class TrieNode:
    def __init__(self):
        self.children = {}              # character -> TrieNode
        self.sentence = None            # the whole sentence, if one ends here


# --- algorithm ---
class AutocompleteSystem:
    """A trie of past sentences, their counts, and a cursor that follows the
    typing: one step per keystroke, then rank the m sentences below it."""

    def __init__(self, sentences, times):
        self.root = TrieNode()
        self.counts = {}                # sentence -> how often it was typed
        for i in range(len(sentences)):
            self.record(sentences[i], times[i])
        self.typed = ""                 # the sentence typed so far
        self.node = self.root           # trie node of typed; None: dead end

    def record(self, sentence, times):
        """Walk the sentence into the trie and add to its count. O(L)."""
        node = self.root
        for ch in sentence:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.sentence = sentence        # mark where the sentence ends
        self.counts[sentence] = self.counts.get(sentence, 0) + times

    def input(self, c):
        """Step the cursor one child down and rank what lies below it; '#'
        records the typed sentence and resets. O(1) step, then top_three."""
        if c == "#":
            self.record(self.typed, 1)  # it was typed once more
            self.typed = ""
            self.node = self.root
            return []
        self.typed = self.typed + c
        if self.node is None or c not in self.node.children:
            self.node = None            # dead end: stays dead until '#'
            return []
        self.node = self.node.children[c]   # one step down, no rescan
        return self.top_three(self.node)

    def collect(self, node, found):
        """Append every sentence in the subtree of node. O(subtree size)."""
        if node.sentence is not None:
            found.append(node.sentence)
        for ch in node.children:
            self.collect(node.children[ch], found)

    def top_three(self, node):
        """Collect the sentences below node, sort them by (-count, sentence)
        and keep the first 3. O(k + m log m) for k nodes, m sentences."""
        found = []
        self.collect(node, found)
        ranked = []
        for sentence in found:
            ranked.append((-self.counts[sentence], sentence))
        ranked.sort()                   # highest count first, ties by ASCII
        best = []
        for i in range(min(3, len(ranked))):
            best.append(ranked[i][1])
        return best


# --- try it ---
sentences = ["i love you", "island", "iroman", "i love leetcode"]
system = AutocompleteSystem(sentences, [5, 3, 2, 2])
print(system.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(system.input(" "))    # -> ['i love you', 'i love leetcode']
print(system.input("a"))    # -> []
print(system.input("#"))    # -> []
print(system.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(system.input(" "))    # -> ['i love you', 'i love leetcode', 'i a']
print(system.input("a"))    # -> ['i a']
print(system.input("#"), system.counts["i a"])     # -> [] 2
