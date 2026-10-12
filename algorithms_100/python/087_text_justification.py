"""
Text Justification - Greedy Line Packing, Then Spread the Spaces

Pack words greedily into lines of exactly max_width characters, spreading the
spaces evenly with the extras in the leftmost gaps; the last line and one-word
lines are left-justified: ["What", "must", "be", "acknowledgment"], 16 ->
["What   must   be", "acknowledgment  "].
"""


# --- algorithm ---
def full_justify(words, max_width):
    """Take words while they fit, then justify the line.
    O(n + L * max_width) for n words and L lines."""
    lines = []
    i = 0
    while i < len(words):
        j = i + 1                       # the line is words[i..j-1]
        width = len(words[i])           # its letters plus one space per gap
        while j < len(words) and width + 1 + len(words[j]) <= max_width:
            width = width + 1 + len(words[j])
            j += 1
        is_last = (j == len(words))
        lines.append(justify_line(words, i, j, max_width, is_last))
        i = j
    return lines


def justify_line(words, i, j, max_width, is_last):
    """Lay words[i..j-1] into exactly max_width characters. O(max_width)."""
    if is_last or j - i == 1:           # left-justify, pad on the right
        line = " ".join(words[i:j])
        return line + " " * (max_width - len(line))
    letters = 0
    for k in range(i, j):
        letters += len(words[k])
    gaps = j - i - 1
    spaces = max_width - letters        # blanks to place in the gaps
    each = spaces // gaps
    extra = spaces % gaps               # leftmost gaps get one more
    pieces = [words[i]]
    for k in range(i + 1, j):
        gap = each
        if k - i <= extra:              # gap number k - i, from 1
            gap += 1
        pieces.append(" " * gap)
        pieces.append(words[k])
    return "".join(pieces)


# --- try it ---
words = ["This", "is", "an", "example", "of", "text", "justification."]
lines = full_justify(words, 16)
print("|" + lines[0] + "|")             # -> |This    is    an|
print("|" + lines[1] + "|")             # -> |example  of text|
print("|" + lines[2] + "|")             # -> |justification.  |
lines = full_justify(["What", "must", "be", "acknowledgment", "shall"], 16)
print("|" + lines[1] + "|")             # -> |acknowledgment  |
