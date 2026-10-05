"""
Design Search Autocomplete System (LeetCode 642) - Hard
Chapter: tries
Pattern: Trie with per-node frequency map + cursor that follows keystrokes

AutocompleteSystem(sentences, times) seeds a history in which sentences[i] was typed
times[i] times. input(c) receives one character. If c is '#', the typed sentence is saved
with +1 count and [] is returned. Otherwise it returns up to 3 historical sentences that
start with everything typed so far, ordered by count descending and then ASCII.
Example: history {"i love you": 5, "island": 3, "ironman": 2, "i love leetcode": 2},
input('i') -> ["i love you", "island", "i love leetcode"].
"""


# --- helpers ---
def top_three(counts):
    """The 3 sentences of a sentence -> count dict with the highest count, ties by ASCII order."""
    pairs = []
    for sentence in counts:
        pairs.append((-counts[sentence], sentence))    # negative count: bigger counts sort first
    pairs.sort()
    best = []
    for neg_count, sentence in pairs[:3]:
        best.append(sentence)
    return best


# --- brute force ---
class BruteForce:
    """Flat dict sentence -> count; every keystroke rescans every sentence. O(S * L + S log S)."""

    def __init__(self, sentences, times):
        self.counts = {}
        for i in range(len(sentences)):
            self.counts[sentences[i]] = times[i]
        self.typed = ""

    def input(self, c):
        if c == "#":
            self.counts[self.typed] = self.counts.get(self.typed, 0) + 1
            self.typed = ""
            return []
        self.typed += c
        matches = {}
        for sentence in self.counts:                    # full rescan on every keystroke
            if sentence.startswith(self.typed):
                matches[sentence] = self.counts[sentence]
        return top_three(matches)


# --- optimal ---
class AutocompleteSystem:
    """Trie whose nodes hold sentence -> count; a cursor steps one edge per keystroke."""

    def __init__(self, sentences, times):
        self.root = {"$": {}}               # letter -> child node; "$" -> sentence -> count
        for i in range(len(sentences)):
            self.add(sentences[i], times[i])
        self.cursor = self.root             # trie node of the prefix typed so far; None = dead end
        self.typed = ""

    def add(self, sentence, count):
        node = self.root
        for letter in sentence:
            if letter not in node:
                node[letter] = {"$": {}}
            node = node[letter]
            node["$"][sentence] = node["$"].get(sentence, 0) + count   # each prefix node records it

    def input(self, c):
        if c == "#":
            self.add(self.typed, 1)
            self.cursor = self.root
            self.typed = ""
            return []
        self.typed += c
        if self.cursor is not None:
            if c in self.cursor:
                self.cursor = self.cursor[c]        # one pointer step instead of a rescan
            else:
                self.cursor = None                  # no sentence has this prefix: dead until '#'
        if self.cursor is None:
            return []
        return top_three(self.cursor["$"])


# --- try the brute force ---
ac = BruteForce(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2])
print(ac.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(ac.input(" "))    # -> ['i love you', 'i love leetcode']
print(ac.input("a"))    # -> []
print(ac.input("#"))    # -> []
print(ac.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(ac.input(" "))    # -> ['i love you', 'i love leetcode', 'i a']
print(ac.input("a"))    # -> ['i a']
print(ac.input("#"))    # -> []
print(ac.input("z"))    # -> []
print(ac.input("i"))    # -> []
print(ac.input("#"))    # -> []
print(ac.input("i"))    # -> ['i love you', 'island', 'i a']


# --- try the optimal ---
ac = AutocompleteSystem(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2])
print(ac.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(ac.input(" "))    # -> ['i love you', 'i love leetcode']
print(ac.input("a"))    # -> []
print(ac.input("#"))    # -> []
print(ac.input("i"))    # -> ['i love you', 'island', 'i love leetcode']
print(ac.input(" "))    # -> ['i love you', 'i love leetcode', 'i a']
print(ac.input("a"))    # -> ['i a']
print(ac.input("#"))    # -> []
print(ac.input("z"))    # -> []
print(ac.input("i"))    # -> []
print(ac.input("#"))    # -> []
print(ac.input("i"))    # -> ['i love you', 'island', 'i a']
