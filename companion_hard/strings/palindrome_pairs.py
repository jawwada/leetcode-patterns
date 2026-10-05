"""
Palindrome Pairs (LeetCode 336) - Hard
Chapter: strings
Pattern: Hash map of reversed words + palindrome split

Given distinct words, return every index pair [i, j] with i != j such that
words[i] + words[j] is a palindrome, in any order.
Example: ["abcd","dcba","lls","s","sssll"] -> [[0,1],[1,0],[3,2],[2,4]]
("abcddcba", "dcbaabcd", "slls", "llssssll"); ["a",""] -> [[0,1],[1,0]].
"""


# --- helpers ---
def is_palindrome(text):
    """True when text reads the same backwards."""
    return text == text[::-1]


# --- brute force ---
def brute_force(words):
    """Glue every ordered pair and test it. O(n^2 * L) time, O(1) extra space."""
    pairs = []
    n = len(words)
    for i in range(n):
        for j in range(n):
            if i != j and is_palindrome(words[i] + words[j]):
                pairs.append([i, j])
    return pairs


# --- optimal ---
def palindrome_pairs(words):
    """Split each word; the partner is the reverse of one half, found in a map. O(n * L^2)."""
    where = {}                                     # reversed word -> its index
    for i in range(len(words)):
        where[words[i][::-1]] = i
    pairs = []
    for i in range(len(words)):
        word = words[i]
        for cut in range(len(word) + 1):           # word = front + back
            front = word[:cut]
            back = word[cut:]
            if is_palindrome(front) and back in where and where[back] != i:
                pairs.append([where[back], i])     # reverse(back) + front + back is a palindrome
            if cut < len(word) and is_palindrome(back) and front in where and where[front] != i:
                pairs.append([i, where[front]])    # front + back + reverse(front)
    return pairs


# --- try the brute force ---
words = ["abcd", "dcba", "lls", "s", "sssll"]
print(sorted(brute_force(words)))                  # -> [[0, 1], [1, 0], [2, 4], [3, 2]]
print(sorted(brute_force(["bat", "tab", "cat"])))                   # -> [[0, 1], [1, 0]]
print(sorted(brute_force(["a", ""])))                               # -> [[0, 1], [1, 0]]
print(sorted(brute_force(["abc"])))                                 # -> []


# --- try the optimal ---
words = ["abcd", "dcba", "lls", "s", "sssll"]
print(sorted(palindrome_pairs(words)))             # -> [[0, 1], [1, 0], [2, 4], [3, 2]]
print(sorted(palindrome_pairs(["bat", "tab", "cat"])))                   # -> [[0, 1], [1, 0]]
print(sorted(palindrome_pairs(["a", ""])))                               # -> [[0, 1], [1, 0]]
print(sorted(palindrome_pairs(["abc"])))                                 # -> []
