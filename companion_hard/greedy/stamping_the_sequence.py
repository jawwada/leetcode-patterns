"""
Stamping The Sequence (LeetCode 936) - Hard
Chapter: greedy
Pattern: Reverse greedy (undo the last move first)

Starting from a string of len(target) '?' characters, repeatedly place stamp anywhere,
overwriting the characters beneath it. Return any sequence of at most 10 * len(target) stamp
positions that produces target, or [] if impossible.
Example: stamp = "abc", target = "ababc" -> [0, 2] (stamp at 0 gives "abc??", at 2 gives "ababc").
"""
from collections import deque   # popleft is O(1)


# --- helpers ---
def apply_moves(stamp, moves, n):
    """Start from n '?' and stamp at each position in order: shows what a move list produces."""
    current = ["?"] * n
    for i in moves:
        for k in range(len(stamp)):
            current[i + k] = stamp[k]
    return "".join(current)


# --- brute force ---
def brute_force(stamp, target):
    """Forward BFS over partial strings from '???...', stamping at every position. Exponential."""
    m = len(stamp)
    n = len(target)
    start = "?" * n
    previous = {start: None}                      # string -> (string before it, stamp position)
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current == target:
            return path_back(previous, current)
        for i in range(n - m + 1):
            stamped = current[:i] + stamp + current[i + m:]
            if stamped not in previous:
                previous[stamped] = (current, i)
                queue.append(stamped)
    return []


def path_back(previous, current):
    """Follow the breadcrumbs from the target back to the start; reverse for the forward order."""
    path = []
    while previous[current] is not None:
        current, position = previous[current]
        path.append(position)
    return path[::-1]


# --- optimal ---
def stamping_the_sequence(stamp, target):
    """Work backwards: erase any window matching the stamp ("?" matches all), reverse. O(n^2 m)."""
    m = len(stamp)
    n = len(target)
    letters = list(target)
    done = [False] * (n - m + 1)                  # window fully erased: never look at it again
    moves = []
    erased_total = 0
    while erased_total < n:
        progressed = False
        for i in range(n - m + 1):
            if done[i]:
                continue
            erased = unstamp(stamp, letters, i)
            if erased > 0:                        # this window was the last stamp laid here
                erased_total += erased
                moves.append(i)
                done[i] = True
                progressed = True
        if not progressed:
            return []                             # letters remain but no window matches
    return moves[::-1]                            # peeled last-first, so stamp first-last


def unstamp(stamp, letters, i):
    """If every real letter under window i matches the stamp, turn them into "?"; count them."""
    live = []
    for k in range(i, i + len(stamp)):
        if letters[k] != "?":
            if letters[k] != stamp[k - i]:
                return 0
            live.append(k)
    for k in live:
        letters[k] = "?"
    return len(live)


# --- try the brute force ---
# several move lists are valid, so the demos print the string the moves produce
print(apply_moves("abc", brute_force("abc", "ababc"), 5))        # -> ababc
print(apply_moves("abca", brute_force("abca", "aabcaca"), 7))    # -> aabcaca
print(brute_force("abc", "abd"))                                 # -> []
print(apply_moves("a", brute_force("a", "aaa"), 3))              # -> aaa


# --- try the optimal ---
# several move lists are valid, so the demos print the string the moves produce
print(apply_moves("abc", stamping_the_sequence("abc", "ababc"), 5))        # -> ababc
print(apply_moves("abca", stamping_the_sequence("abca", "aabcaca"), 7))    # -> aabcaca
print(stamping_the_sequence("abc", "abd"))                                 # -> []
print(apply_moves("a", stamping_the_sequence("a", "aaa"), 3))              # -> aaa
