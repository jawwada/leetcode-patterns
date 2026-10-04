"""
Dota2 Senate (LeetCode 649)  — Medium
Pattern: Round-robin queues (re-enqueue with index + n)

Problem
-------
A string of senators, 'R' (Radiant) or 'D' (Dire), vote in order, round after round. On its
turn a senator still in the game may ban one opposing senator (who loses all future turns).
When only one party remains, it wins. Return "Radiant" or "Dire".
Example: "RDD" -> "Dire": R bans the first D, the second D bans R.

Brute force
-----------
Simulate literally: walk the string round by round with a banned[] array; when senator i acts,
scan forward circularly for the next un-banned opponent and ban them. Each ban costs an O(n)
scan and there can be up to n rounds over n senators, so O(n^2) time, O(n) space. The wasted
work is the scan: the simulation keeps re-walking banned senators and same-party senators to
find "the next opponent in turn order".

From brute force to optimal
---------------------------
Greedy first: the best ban is always the NEXT opponent in turn order (they'd act soonest).
Then notice we only ever need "who acts next on each side", so keep two queues of turn
indices, one per party, each sorted by when that senator next acts. Compare the two fronts:
the smaller index acts first, bans the other front (pop it, gone for good), and goes to the
back of its own queue as index + n, meaning "same seat, next round". Adding n keeps both
queues ordered by actual turn time across rounds. Each comparison removes one senator, so
there are at most n comparisons in total.

Intuition
---------
The two queue fronts are the two senators about to act. Whoever is earlier wins the duel,
eliminates the other front and rejoins the line one full round later. Banned senators are
simply never re-enqueued, so no scanning past them is ever needed.

Geometric view
--------------
Picture the senate as a timeline that repeats every n ticks. Each party's queue is its
remaining senators laid out on that timeline in order. The earlier front jumps forward by
exactly n ticks (to the same seat in the next lap) while the later front is erased.
The lines shrink by one per duel until one is empty.

Steps
-----
1. n = len(senate); r = deque of i where senate[i] == 'R'; d = deque of i where 'D'.
2. While both are non-empty: a = r.popleft(), b = d.popleft().
3. If a < b: r.append(a + n) (R acts first and bans b), else d.append(b + n).
4. Return "Radiant" if r else "Dire".

Complexity: O(n) time, O(n) space — each loop iteration permanently removes one senator.
Pitfalls: banning the first opponent in the string instead of the next one in turn order;
          re-enqueueing with i instead of i + n (breaks ordering across rounds);
          stopping after one pass over the string.
"""
import random
from collections import deque


class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)
        r = deque(i for i, c in enumerate(senate) if c == "R")
        d = deque(i for i, c in enumerate(senate) if c == "D")
        while r and d:
            a, b = r.popleft(), d.popleft()
            if a < b:
                r.append(a + n)     # R acts first, bans b, waits for next round
            else:
                d.append(b + n)
        return "Radiant" if r else "Dire"


def brute_force(senate: str) -> str:
    n = len(senate)
    banned = [False] * n
    while True:
        for i in range(n):
            if banned[i]:
                continue
            j = (i + 1) % n                     # scan for the next live opponent
            while j != i and (banned[j] or senate[j] == senate[i]):
                j = (j + 1) % n
            if j == i:                          # no opponent left
                return "Radiant" if senate[i] == "R" else "Dire"
            banned[j] = True


if __name__ == "__main__":
    s = Solution()
    assert s.predictPartyVictory("RD") == "Radiant"
    assert s.predictPartyVictory("RDD") == "Dire"
    assert s.predictPartyVictory("DDRRR") == "Dire"
    assert s.predictPartyVictory("R") == "Radiant"     # edge: one senator
    for case in ("RD", "RDD", "DDRRR", "R", "DRRDRDRDRDDRDRDR"):
        assert brute_force(case) == s.predictPartyVictory(case)

    random.seed(649)
    for _ in range(500):
        senate = "".join(random.choice("RD") for _ in range(random.randint(1, 30)))
        assert brute_force(senate) == s.predictPartyVictory(senate)
    print("ok")
