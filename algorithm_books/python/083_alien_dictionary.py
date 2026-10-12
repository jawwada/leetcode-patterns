"""
Alien Dictionary - Letter Edges from Adjacent Words, Then Topological Sort

A list of words is sorted in an unknown alphabet. Return the letters that
appear in an order that sorts the list, or '' if no alphabet can:
["wrt", "wrf", "er", "ett", "rftt"] -> "wertf".
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def alien_order(words):
    """Collect the letters, add one edge per adjacent pair of words, then
    sort the letters topologically. O(C) time for C letters in all."""
    graph = {}                          # letter -> letters that come after it
    indegree = {}                       # letter -> letters still before it
    for word in words:
        for letter in word:
            if letter not in graph:
                graph[letter] = []
                indegree[letter] = 0
    for i in range(len(words) - 1):
        if not add_edge(words[i], words[i + 1], graph, indegree):
            return ""                   # a word came before its own prefix
    return topological_order(graph, indegree)


def add_edge(first, second, graph, indegree):
    """The first letters that differ give the edge before -> after; False
    if second is a proper prefix of first, which no alphabet allows."""
    for j in range(min(len(first), len(second))):
        before = first[j]
        after = second[j]
        if before != after:
            if after not in graph[before]:  # count each edge once
                graph[before].append(after)
                indegree[after] += 1
            return True                 # later letters say nothing
    return len(first) <= len(second)    # "abc" before "ab" is impossible


def topological_order(graph, indegree):
    """Kahn's algorithm: place a letter once nothing must come before it.
    O(V + E); '' if a cycle leaves letters unplaced."""
    queue = deque()
    for letter in sorted(indegree):     # sorted start: a repeatable answer
        if indegree[letter] == 0:
            queue.append(letter)
    order = []
    while queue:
        letter = queue.popleft()
        order.append(letter)
        for after in graph[letter]:
            indegree[after] -= 1        # one fewer before it
            if indegree[after] == 0:
                queue.append(after)
    if len(order) < len(indegree):
        return ""                       # the rest sit on a cycle
    return "".join(order)


# --- try it ---
print(repr(alien_order(["wrt", "wrf", "er", "ett", "rftt"])))   # -> 'wertf'
print(repr(alien_order(["ab", "ac", "d"])))         # -> 'abdc'
print(repr(alien_order(["z", "x", "z"])))           # -> ''
print(repr(alien_order(["abc", "ab"])))             # -> ''
print(repr(alien_order(["z", "z"])))                # -> 'z'
