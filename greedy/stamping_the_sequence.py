"""
Stamping The Sequence (LeetCode 936)  — Hard
Pattern: Reverse greedy (undo the last move first)

Problem
-------
You have a stamp string and a target string. Start from "????..." (len(target) '?'s) and repeatedly
place the stamp anywhere, overwriting the characters beneath it. Return any sequence of stamp
positions (at most 10 * len(target)) that produces target, or [] if it is impossible.
Example: stamp = "abc", target = "ababc" -> [0, 2] (stamp at 0: "abc??", stamp at 2: "ababc");
[1, 0, 2] is also accepted.

Brute force
-----------
Forward BFS over partial strings: start at "????", from each string stamp at every one of the
n - m + 1 positions, stop when the target appears. Each cell can hold any letter or '?', so the
state space is exponential in n, and even one BFS level costs O(n * m). The wasted work: forwards
you never know which stamps will later be overwritten, so you must explore every order; most of
those orders are equivalent up to overwriting.

From brute force to optimal
---------------------------
Reverse the process. The LAST stamp applied is visible in target intact: some window of target
equals stamp exactly. Peel it off by replacing that window with '?'s (wildcards that match any
stamp letter, because whatever was underneath was overwritten anyway). Now the second-to-last
stamp is an exact match on the remaining letters, with '?' allowed to stand for anything, and so
on. The greedy is safe because un-stamping any matching window never hurts a later un-stamp:
turning letters into '?' only makes other windows easier to match. So: scan positions, un-stamp
every window that matches (letters agree, '?' free) and that still contains at least one real
letter, repeat until the whole string is '?' or a full pass makes no progress (-> impossible).
Reverse the recorded positions to get a forward order. Each pass is O((n - m) * m) and every
productive pass erases >= 1 character, so the worst case is O(n * (n - m) * m) with O(n) space;
a `done` flag per window keeps fully erased windows from being rechecked.

Intuition
---------
Working backwards turns an unknowable question ("what will be covered later?") into a visible one
("which window looks exactly like the stamp right now?"). Erased cells become wildcards, so the
set of matchable windows only grows as you peel, which is why any order of peeling works.

Geometric view
--------------
Picture the target as a strip of tiles. Slide the stamp along it; wherever every tile under the
stamp either matches or is already blank, lift those tiles off (blank them) and write down the
position. Keep sliding and lifting until the strip is blank. The lifting order, read backwards,
is the stamping order.

Steps
-----
1. t = list(target); stars = 0; moves = []; done[i] = window i fully erased.
2. unstamp(i): collect positions in window i that are not '?'; if none, nothing to do; if any
   of them differs from stamp, fail; else set them to '?', stars += count, return True.
3. Loop: for every i not done: if unstamp(i) succeeds, append i, set done[i], note progress.
4. If a full pass makes no progress and stars < n: return [].
5. When stars == n: return reversed(moves).

Complexity: O(n * (n - m) * m) time worst case, O(n) space —
            at most n productive passes, each scanning every window against the stamp.
Pitfalls: counting a window that is already all '?' as progress (infinite loop); forgetting to
          reverse the recorded positions; stopping after one left-to-right pass (windows that
          only match after a neighbour is erased need another pass).
"""
from collections import deque
from typing import List


class Solution:
    def movesToStamp(self, stamp: str, target: str) -> List[int]:
        m, n = len(stamp), len(target)
        t = list(target)
        done = [False] * (n - m + 1)        # window fully erased: never look again
        moves: List[int] = []
        stars = 0

        def unstamp(i: int) -> int:
            """Erase window i if every live letter matches the stamp; return letters erased."""
            live = [k for k in range(i, i + m) if t[k] != "?"]
            if any(t[k] != stamp[k - i] for k in live):
                return 0
            for k in live:
                t[k] = "?"
            return len(live)

        while stars < n:
            progressed = False
            for i in range(n - m + 1):
                if done[i]:
                    continue
                erased = unstamp(i)
                if erased:                   # this window was the latest surviving stamp here
                    stars += erased
                    moves.append(i)
                    done[i] = True
                    progressed = True
            if not progressed:
                return []                    # letters remain but no window matches
        return moves[::-1]                   # peeled last-first -> stamp first-last


def brute_force(stamp: str, target: str) -> List[int]:
    """Forward BFS over partial strings from '???...'; exponential state space."""
    m, n = len(stamp), len(target)
    start = "?" * n
    prev = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == target:
            path = []
            while prev[cur] is not None:
                cur, pos = prev[cur]
                path.append(pos)
            return path[::-1]
        for i in range(n - m + 1):
            nxt = cur[:i] + stamp + cur[i + m:]
            if nxt not in prev:
                prev[nxt] = (cur, i)
                queue.append(nxt)
    return []


def apply_moves(stamp: str, moves: List[int], n: int) -> str:
    cur = ["?"] * n
    for i in moves:
        cur[i:i + len(stamp)] = stamp
    return "".join(cur)


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ("abc", "ababc", True),
        ("abca", "aabcaca", True),
        ("abc", "abd", False),         # edge: impossible
        ("a", "aaa", True),
        ("ab", "ba", False),           # edge: never matches
    ]
    for stamp, target, feasible in cases:
        got = s.movesToStamp(stamp, target)
        assert bool(got) is feasible, (stamp, target, got)
        assert bool(brute_force(stamp, target)) is feasible, (stamp, target)
        if feasible:
            assert len(got) <= 10 * len(target)
            assert apply_moves(stamp, got, len(target)) == target, (stamp, target, got)

    random.seed(936)
    for _ in range(150):
        stamp = "".join(random.choice("ab") for _ in range(random.randint(1, 3)))
        target = "".join(random.choice("ab") for _ in range(random.randint(1, 6)))
        if len(target) < len(stamp):
            continue
        got = s.movesToStamp(stamp, target)
        assert bool(got) == bool(brute_force(stamp, target)), (stamp, target)
        if got:
            assert apply_moves(stamp, got, len(target)) == target, (stamp, target, got)
    print("ok")
