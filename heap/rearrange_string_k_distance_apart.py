"""
Rearrange String k Distance Apart (LeetCode 358)  — Hard
Pattern: Greedy max-heap by remaining count + fixed-length cooldown queue

Problem
-------
Rearrange string s so that identical characters are at least k positions apart. Return any
valid rearrangement, or "" if none exists (k = 0 means no constraint).
Example: s="aabbcc", k=3 -> "abcabc". s="aaabc", k=3 -> "". s="aaadbbcc", k=2 -> "abacabcd"
(one of several valid answers).

Brute force
-----------
Backtracking: fill positions left to right; at each position try every character that still
has remaining count and does not appear in the previous k-1 positions. Exponential, O(26^n)
in the worst case, O(n) space for the recursion. The waste: the search explores orderings
that are doomed early -- whenever a frequent character is postponed, it later needs more
slots than remain -- and it retries equivalent prefixes that differ only in the order of
characters with identical counts.

From brute force to optimal
---------------------------
The redundancy is searching over which character to place when one choice is provably safe:
the eligible character with the MOST remaining copies. If some other eligible character were
placed first, swapping it with the next placement of the most-frequent one never creates a
violation (exchange argument), so a greedy sequence of choices is optimal. Two structures make
"most frequent eligible character" O(log 26): a max-heap keyed by remaining count for the
eligible characters, and a FIFO cooldown queue of length k holding the characters placed in
the last k slots. After placing a character it goes to the back of the queue; once the queue
holds k entries its front has waited k slots and (if it still has copies) returns to the heap.
If the heap is ever empty before the string is complete, no arrangement exists. O(n log 26).

Intuition
---------
Think of the characters as workers who need a k-slot rest after each shift. Always schedule
the worker with the most shifts left among those who are rested -- postponing them only
piles up their shifts into fewer remaining slots. The rest bench is a queue: whoever sat down
first stands up first, exactly k slots later. An empty pool of rested workers while slots
remain means someone must break the rest rule, so the answer is "".

Geometric view
--------------
A conveyor belt of empty slots moving left. Above it a triangle (max-heap) of rested letters
with the biggest count at the apex; beside it a short tube of length k (the cooldown queue).
Each tick the apex letter drops onto the belt and slides into the back of the tube, pushing
the letter at the tube's front out and back up into the triangle. The tube's length is
precisely the gap the problem demands.

Steps
-----
1. If k <= 1 return s. Count characters; heap = max-heap of (-count, ch).
2. cooldown = deque(); result = [].
3. For each of n positions: if the heap is empty, return "". Pop (-cnt, ch); append ch;
   push (-(cnt-1), ch) onto cooldown (even if cnt-1 == 0, so positions line up).
4. If len(cooldown) == k: pop its front; if its count > 0, push it back onto the heap.
5. Return "".join(result).

Complexity: O(n log A) time (A = alphabet size, 26), O(A) space — each placement is one heap
pop/push; the heap and queue hold at most 26 and k entries.
Pitfalls: Releasing a character after k-1 slots instead of k; skipping the cooldown queue for
characters whose count hit zero (then the queue length no longer measures distance); not
handling k <= 1 (every string is valid).
"""
import heapq
from collections import Counter, deque
from typing import List


class Solution:
    def rearrangeString(self, s: str, k: int) -> str:
        if k <= 1:
            return s
        heap = [(-cnt, ch) for ch, cnt in Counter(s).items()]   # max-heap by remaining count
        heapq.heapify(heap)
        cooldown = deque()                                      # chars placed in the last k slots
        out = []
        for _ in range(len(s)):
            if not heap:                                        # nobody is rested: impossible
                return ""
            neg, ch = heapq.heappop(heap)
            out.append(ch)
            cooldown.append((neg + 1, ch))                      # one fewer copy left
            if len(cooldown) == k:                              # front has waited k slots
                neg, ch = cooldown.popleft()
                if neg < 0:
                    heapq.heappush(heap, (neg, ch))
        return "".join(out)


def brute_force(s: str, k: int) -> str:
    # Exponential backtracking: at each slot try every char not used in the previous k-1 slots.
    counts = Counter(s)
    out: List[str] = []

    def place() -> bool:
        if len(out) == len(s):
            return True
        recent = set(out[-(k - 1):]) if k > 1 else set()
        for ch in sorted(counts):
            if counts[ch] and ch not in recent:
                counts[ch] -= 1
                out.append(ch)
                if place():
                    return True
                out.pop()
                counts[ch] += 1
        return False

    return "".join(out) if place() else ""


def is_valid(s: str, k: int, t: str) -> bool:
    if sorted(s) != sorted(t):
        return False
    last = {}
    for i, ch in enumerate(t):
        if ch in last and i - last[ch] < k:
            return False
        last[ch] = i
    return True


if __name__ == "__main__":
    s = Solution()
    assert s.rearrangeString("aabbcc", 3) == "abcabc"
    assert s.rearrangeString("aaabc", 3) == "" == brute_force("aaabc", 3)
    assert is_valid("aaadbbcc", 2, s.rearrangeString("aaadbbcc", 2))
    assert s.rearrangeString("abc", 0) == "abc"                 # k = 0: no constraint
    assert s.rearrangeString("a", 5) == "a"                     # single char
    assert s.rearrangeString("aa", 2) == ""
    import random
    random.seed(358)
    for _ in range(200):
        n = random.randint(1, 8)
        t = "".join(random.choice("abcd") for _ in range(n))
        k = random.randint(0, 4)
        mine, ref = s.rearrangeString(t, k), brute_force(t, k)
        assert (mine == "") == (ref == ""), (t, k, mine, ref)   # same feasibility
        assert mine == "" or is_valid(t, k, mine), (t, k, mine)
    print("ok")
