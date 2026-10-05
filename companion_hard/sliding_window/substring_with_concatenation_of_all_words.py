"""
Substring with Concatenation of All Words (LeetCode 30) - Hard
Chapter: sliding_window
Pattern: Fixed-size sliding window with counts

Given a string s and a list words of equal-length strings (duplicates allowed), return the
start indices of every substring of s that is a concatenation of all the words in some
order, each used exactly once.
Example: s = "barfoothefoobarman", words = ["foo", "bar"] -> [0, 9] ("barfoo" and "foobar").
"""


# --- helpers ---
def count_items(items):
    """How many times each item appears, as a dict."""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


# --- brute force ---
def brute_force(s, words):
    """Cut m chunks at every start and compare their counts with words. O(n * m * L) time."""
    word_len = len(words[0])
    m = len(words)
    need = count_items(words)
    result = []
    for start in range(len(s) - m * word_len + 1):
        chunks = []
        for j in range(start, start + m * word_len, word_len):   # rebuilt for every start
            chunks.append(s[j:j + word_len])
        if count_items(chunks) == need:         # same words, same multiplicities
            result.append(start)
    return result


# --- optimal ---
def find_substring(s, words):
    """One counting window per chunk offset; each chunk enters and leaves once. O(n * L) time."""
    word_len = len(words[0])
    m = len(words)
    need = count_items(words)
    result = []
    for offset in range(word_len):              # starts with the same chunk grid
        have = {}
        left = offset
        count = 0                               # chunks inside the window
        for right in range(offset, len(s) - word_len + 1, word_len):
            chunk = s[right:right + word_len]
            if chunk not in need:               # a wall: no valid window crosses it
                have = {}
                count = 0
                left = right + word_len
                continue
            have[chunk] = have.get(chunk, 0) + 1
            count += 1
            while have[chunk] > need[chunk]:    # too many copies: drop chunks from the left
                have[s[left:left + word_len]] -= 1
                count -= 1
                left += word_len
            if count == m:                      # exactly m chunks: a match starts at left
                result.append(left)
                have[s[left:left + word_len]] -= 1
                count -= 1
                left += word_len
    return result


# --- try the brute force ---
print(brute_force("barfoothefoobarman", ["foo", "bar"]))                          # -> [0, 9]
print(brute_force("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]))  # -> []
print(sorted(brute_force("barfoofoobarthefoobarman", ["bar", "foo", "the"])))     # -> [6, 9, 12]
print(sorted(brute_force("aaaaaa", ["aa", "aa"])))                                # -> [0, 1, 2]


# --- try the optimal ---
print(find_substring("barfoothefoobarman", ["foo", "bar"]))                          # -> [0, 9]
print(find_substring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]))  # -> []
print(sorted(find_substring("barfoofoobarthefoobarman", ["bar", "foo", "the"])))     # -> [6, 9, 12]
print(sorted(find_substring("aaaaaa", ["aa", "aa"])))                                # -> [0, 1, 2]
