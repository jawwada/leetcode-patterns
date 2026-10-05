"""
Text Justification (LeetCode 68) - Hard
Chapter: strings
Pattern: Greedy line packing

Pack words greedily into lines of exactly max_width characters. Fully justify each line, with
the extra spaces spread as evenly as possible (leftover spaces go to the leftmost gaps); the
last line, and any line with a single word, is left-justified and padded on the right.
Example: ["This","is","an","example","of","text","justification."], 16
-> ["This    is    an", "example  of text", "justification.  "].
"""


# --- helpers ---
def left_justify(line, max_width):
    """Join the words with single spaces and pad the right with spaces up to max_width."""
    text = " ".join(line)
    return text + " " * (max_width - len(text))


# --- brute force ---
def spread_one_at_a_time(line, max_width):
    """Start every gap at one space; add a space to the next gap (cycling) until the line fits."""
    gaps = [" "] * (len(line) - 1)
    k = 0
    while len("".join(line) + "".join(gaps)) < max_width:   # re-measure after every single space
        gaps[k % len(gaps)] += " "
        k += 1
    text = ""
    for i in range(len(gaps)):
        text += line[i] + gaps[i]
    return text + line[-1]


def brute_force(words, max_width):
    """Pack greedily; hand out the extra spaces one at a time. O(width) re-measures per line."""
    lines = []
    line = []
    for word in words:
        if line != [] and len(" ".join(line + [word])) > max_width:
            if len(line) == 1:
                lines.append(left_justify(line, max_width))
            else:
                lines.append(spread_one_at_a_time(line, max_width))
            line = []                              # the word that did not fit starts a new line
        line.append(word)
    lines.append(left_justify(line, max_width))    # the last line is always left-justified
    return lines


# --- optimal ---
def spread_evenly(line, max_width):
    """Every gap gets spaces // gaps; the leftmost spaces % gaps gaps get one more."""
    gaps = len(line) - 1
    letters = 0
    for word in line:
        letters += len(word)
    spaces = max_width - letters
    each = spaces // gaps
    extra = spaces % gaps                          # one divmod replaces the one-at-a-time loop
    text = ""
    for k in range(gaps):
        text += line[k] + " " * each
        if k < extra:
            text += " "
    return text + line[-1]


def text_justification(words, max_width):
    """Two indices pack each line greedily; arithmetic spreads the spaces. O(total characters)."""
    lines = []
    i = 0
    while i < len(words):
        j = i
        width = len(words[i])
        while j + 1 < len(words) and width + 1 + len(words[j + 1]) <= max_width:
            j += 1                                 # words[j] still fits after one space
            width += 1 + len(words[j])
        line = words[i:j + 1]
        if len(line) == 1 or j == len(words) - 1:  # single word or the last line
            lines.append(left_justify(line, max_width))
        else:
            lines.append(spread_evenly(line, max_width))
        i = j + 1
    return lines


# --- try the brute force ---
words = ["This", "is", "an", "example", "of", "text", "justification."]
print(brute_force(words, 16))
# -> ['This    is    an', 'example  of text', 'justification.  ']
words = ["What", "must", "be", "acknowledgment", "shall", "be"]
print(brute_force(words, 16))
# -> ['What   must   be', 'acknowledgment  ', 'shall be        ']
print(brute_force(["a"], 1))                       # -> ['a']
print(brute_force(["ab", "cd", "ef"], 2))          # -> ['ab', 'cd', 'ef']


# --- try the optimal ---
words = ["This", "is", "an", "example", "of", "text", "justification."]
print(text_justification(words, 16))
# -> ['This    is    an', 'example  of text', 'justification.  ']
words = ["What", "must", "be", "acknowledgment", "shall", "be"]
print(text_justification(words, 16))
# -> ['What   must   be', 'acknowledgment  ', 'shall be        ']
print(text_justification(["a"], 1))                       # -> ['a']
print(text_justification(["ab", "cd", "ef"], 2))          # -> ['ab', 'cd', 'ef']
