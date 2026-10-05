"""
Number of Valid Words for Each Puzzle (LeetCode 1178) - Hard
Chapter: bit_manipulation
Pattern: Bitmask counting + submask enumeration

A word is valid for a puzzle if it contains the puzzle's first letter and every letter of
the word appears in the puzzle. Each puzzle has exactly 7 distinct letters. Return, for each
puzzle, how many words are valid for it.
Example: words = ["aaaa", "asas", "able", "ability", "actt", "actor", "access"],
         puzzles = ["aboveyz", "abrodyz", "abslute", "absoryz", "actresz", "gaswxyz"]
         -> [1, 1, 3, 2, 4, 0].
"""


# --- brute force ---
def word_fits(word, puzzle):
    """True if the word uses the puzzle's first letter and only puzzle letters."""
    if puzzle[0] not in word:
        return False
    for letter in word:
        if letter not in puzzle:
            return False
    return True


def brute_force(words, puzzles):
    """Check every word against every puzzle. O(P * W * L) time, O(1) space."""
    answer = []
    for puzzle in puzzles:
        count = 0
        for word in words:  # every word is rescanned for every puzzle
            if word_fits(word, puzzle):
                count += 1
        answer.append(count)
    return answer


# --- optimal ---
def letter_mask(text):
    """26-bit mask with bit (letter - 'a') set for every letter in text."""
    mask = 0
    for letter in text:
        mask |= 1 << (ord(letter) - ord("a"))
    return mask


def find_num_of_valid_words(words, puzzles):
    """Count words per letter mask, then sum the 128 submasks of each puzzle. O(W L + 128 P)."""
    counts = {}  # letter mask -> how many words have exactly that letter set
    for word in words:
        mask = letter_mask(word)
        counts[mask] = counts.get(mask, 0) + 1
    answer = []
    for puzzle in puzzles:
        full = letter_mask(puzzle)
        first = 1 << (ord(puzzle[0]) - ord("a"))
        total = 0
        sub = full
        while True:  # visit every submask of full, from full down to 0
            if sub & first:  # the word must contain the first letter
                total += counts.get(sub, 0)
            if sub == 0:
                break
            sub = (sub - 1) & full  # the next smaller submask of full
        answer.append(total)
    return answer


# --- try the brute force ---
words = ["aaaa", "asas", "able", "ability", "actt", "actor", "access"]
puzzles = ["aboveyz", "abrodyz", "abslute", "absoryz", "actresz", "gaswxyz"]
print(brute_force(words, puzzles))   # -> [1, 1, 3, 2, 4, 0]
print(brute_force(["apple", "pleas", "please"], ["aelwxyz", "aelpxyz", "aelpsxy", "saelpxy"]))
# -> [0, 1, 3, 2]
print(brute_force(["a"], ["abcdefg"]))   # -> [1]
print(brute_force(["b"], ["abcdefg"]))   # -> [0]


# --- try the optimal ---
words = ["aaaa", "asas", "able", "ability", "actt", "actor", "access"]
puzzles = ["aboveyz", "abrodyz", "abslute", "absoryz", "actresz", "gaswxyz"]
print(find_num_of_valid_words(words, puzzles))   # -> [1, 1, 3, 2, 4, 0]
print(find_num_of_valid_words(["apple", "pleas", "please"],
                              ["aelwxyz", "aelpxyz", "aelpsxy", "saelpxy"]))
# -> [0, 1, 3, 2]
print(find_num_of_valid_words(["a"], ["abcdefg"]))   # -> [1]
print(find_num_of_valid_words(["b"], ["abcdefg"]))   # -> [0]
