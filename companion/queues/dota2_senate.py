"""
Dota2 Senate (LeetCode 649) - Medium
Chapter: queues
Pattern: Round-robin queues (re-enqueue with index + n)

Senators 'R' (Radiant) and 'D' (Dire) sit in a string and act in order, round after round.
On its turn a senator still in the game bans one opposing senator, who loses all future
turns. When only one party is left it wins; return "Radiant" or "Dire".
Example: "RDD" -> "Dire" (R bans the first D, then the second D bans R).
"""
from collections import deque   # deque: popleft is O(1)


# --- brute force ---
def brute_force(senate):
    """Simulate round by round; each live senator scans for the next live opponent. O(n^2)."""
    n = len(senate)
    banned = [False] * n
    while True:
        for i in range(n):
            if banned[i]:
                continue
            j = (i + 1) % n                         # scan forward, wrapping, for an opponent
            while j != i and (banned[j] or senate[j] == senate[i]):
                j = (j + 1) % n
            if j == i:                              # no opponent left: senator i's party wins
                if senate[i] == "R":
                    return "Radiant"
                return "Dire"
            banned[j] = True


# --- optimal ---
def predict_party_victory(senate):
    """Two queues of turn indices; the earlier front bans the other and rejoins as i + n. O(n)."""
    n = len(senate)
    radiant = deque()
    dire = deque()
    for i in range(n):
        if senate[i] == "R":
            radiant.append(i)
        else:
            dire.append(i)
    while len(radiant) > 0 and len(dire) > 0:
        r = radiant.popleft()                       # the two senators who act soonest face off
        d = dire.popleft()
        if r < d:
            radiant.append(r + n)                   # r acts first: bans d, votes again next round
        else:
            dire.append(d + n)
    if len(radiant) > 0:
        return "Radiant"
    return "Dire"


# --- try the brute force ---
print(brute_force("RD"))                 # -> Radiant
print(brute_force("RDD"))                # -> Dire
print(brute_force("DDRRR"))              # -> Dire
print(brute_force("DRRDRDRDRDDRDRDR"))   # -> Radiant


# --- try the optimal ---
print(predict_party_victory("RD"))                 # -> Radiant
print(predict_party_victory("RDD"))                # -> Dire
print(predict_party_victory("DDRRR"))              # -> Dire
print(predict_party_victory("DRRDRDRDRDDRDRDR"))   # -> Radiant
