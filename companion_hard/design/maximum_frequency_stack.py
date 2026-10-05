"""
Maximum Frequency Stack (LeetCode 895) - Hard
Chapter: design
Pattern: Frequency buckets as stacks + max pointer

Design FreqStack with push(val) and pop(): pop removes and returns the most frequent element; on a
tie, the one pushed most recently among the tied values.
Example: push 5,7,5,7,4,5 then pop -> 5 (frequency 3), pop -> 7 (5 and 7 tie at 2, 7 is more
recent), pop -> 5, pop -> 4.
"""


# --- brute force ---
class BruteForce:
    """Plain list in push order; pop recounts everything and scans from the top. O(n) pop."""

    def __init__(self):
        self.items = []

    def push(self, val):
        self.items.append(val)

    def pop(self):
        counts = {}                           # rebuilt from scratch on every pop
        for val in self.items:
            counts[val] = counts.get(val, 0) + 1
        top = 0
        for val in counts:
            top = max(top, counts[val])
        i = len(self.items) - 1
        while i >= 0:
            if counts[self.items[i]] == top:  # rightmost among the most frequent
                return self.items.pop(i)
            i -= 1


# --- optimal ---
class FreqStack:
    """One stack per frequency: group[f] holds values in the order they reached f. O(1) per op."""

    def __init__(self):
        self.freq = {}                        # val -> current frequency
        self.group = {}                       # frequency -> stack of vals that reached it
        self.maxfreq = 0

    def push(self, val):
        self.freq[val] = self.freq.get(val, 0) + 1
        f = self.freq[val]
        if f not in self.group:
            self.group[f] = []
        self.group[f].append(val)             # val is now the newest value at frequency f
        self.maxfreq = max(self.maxfreq, f)

    def pop(self):
        val = self.group[self.maxfreq].pop()  # most recent among the most frequent
        if len(self.group[self.maxfreq]) == 0:
            self.maxfreq -= 1                 # counts grow one at a time: that row is non-empty
        self.freq[val] -= 1
        return val


# --- try the brute force ---
fs = BruteForce()
for v in (5, 7, 5, 7, 4, 5):
    fs.push(v)
print(fs.pop())      # -> 5
print(fs.pop())      # -> 7
print(fs.pop())      # -> 5
print(fs.pop())      # -> 4
fs.push(7)           # 7 still has frequency 1 from the earlier push
print(fs.pop())      # -> 7
print(fs.pop())      # -> 7
fs = BruteForce()
fs.push(1)
print(fs.pop())      # -> 1
fs.push(2)
print(fs.pop())      # -> 2


# --- try the optimal ---
fs = FreqStack()
for v in (5, 7, 5, 7, 4, 5):
    fs.push(v)
print(fs.pop())      # -> 5
print(fs.pop())      # -> 7
print(fs.pop())      # -> 5
print(fs.pop())      # -> 4
fs.push(7)           # 7 still has frequency 1 from the earlier push
print(fs.pop())      # -> 7
print(fs.pop())      # -> 7
fs = FreqStack()
fs.push(1)
print(fs.pop())      # -> 1
fs.push(2)
print(fs.pop())      # -> 2
