"""
Reorganize String (LeetCode 767)  — Medium
Pattern: Greedy most-frequent-first with a max-heap

Problem
-------
Rearrange the characters of s so that no two adjacent characters are equal. Return any valid
arrangement, or "" if impossible.
Example: "aab" -> "aba".  "aaab" -> "".

Brute force
-----------
Try every permutation of s and return the first one with no equal neighbours.
O(n! * n) time, O(n) space. The waste: permutations that differ only in the order of identical
letters are tried separately, and a permutation is rejected only after being fully built even
when its first two characters already clash.

From brute force to optimal
---------------------------
The redundancy is exploring arrangements blindly when the constraint is purely about counts.
Observation 1: an arrangement exists iff the most frequent letter occurs at most (n+1)//2 times
(otherwise two copies must touch). Observation 2: the greedy rule "always place the most frequent
letter that is not the one just placed" never gets stuck when that condition holds, because
placing the majority letter as early as possible spreads it out maximally. We need the letter
with the highest remaining count, excluding one letter, repeatedly: a max-heap of counts gives
that in O(log 26), and we simply hold the just-used letter out of the heap for one round.

Intuition
---------
Spend your most dangerous (most frequent) letter first at every step so it never piles up;
hold the letter you just placed out for exactly one turn so it cannot repeat.

Geometric view
--------------
A triangle (max-heap) of letter counts with the biggest at the apex, and a single "parking spot"
beside it for the letter placed last. Each tick: pop the apex, write it to the output, move the
parked letter back into the triangle, park the one just written. If the feasibility check up
front guarantees the parking spot is empty when the triangle runs dry.

Steps
-----
1. Count letters. If max count > (n + 1) // 2 return "" early.
2. Build a max-heap of (-count, char).
3. Loop: pop the top, append its char, decrement. Push the previously held letter back (if it
   still has copies), then hold the current one.
4. When the heap is empty the held letter has no copies left (guaranteed by step 1), so return
   the joined output.

Complexity: O(n log 26) = O(n) time, O(26) space — the heap holds at most 26 distinct letters.
Pitfalls: Pushing the just-used letter back before popping the next one (it would be chosen
again); forgetting the early feasibility check; mis-computing the bound as n // 2 for odd n.
"""
import heapq
from collections import Counter
from itertools import permutations


class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        if max(counts.values()) > (len(s) + 1) // 2:
            return ""                                   # majority letter cannot be spread out
        heap = [(-c, ch) for ch, c in counts.items()]   # max-heap on remaining count
        heapq.heapify(heap)
        out = []
        held = None                                     # (negcount, char) just placed, kept out
        while heap:
            neg, ch = heapq.heappop(heap)
            out.append(ch)
            if held and held[0] < 0:                    # previous letter is allowed back now
                heapq.heappush(heap, held)
            held = (neg + 1, ch)                        # one copy spent; park it for a turn
        return "".join(out)


def brute_force(s: str) -> str:
    for perm in permutations(s):                        # n! candidates, checked only when complete
        if all(perm[i] != perm[i + 1] for i in range(len(perm) - 1)):
            return "".join(perm)
    return ""


def valid(original: str, out: str) -> bool:
    return sorted(out) == sorted(original) and all(out[i] != out[i + 1] for i in range(len(out) - 1))


if __name__ == "__main__":
    s = Solution()
    assert valid("aab", s.reorganizeString("aab"))
    assert s.reorganizeString("aaab") == ""
    assert valid("vvvlo", s.reorganizeString("vvvlo"))
    assert s.reorganizeString("a") == "a"                     # single char
    assert valid("abab", s.reorganizeString("abab"))          # even length, exactly n/2 copies
    for case in ["aab", "aaab", "vvvlo", "a", "abab", "aaabbc", "aaaabbc"]:
        mine, theirs = s.reorganizeString(case), brute_force(case)
        assert (mine == "") == (theirs == ""), case             # agree on feasibility
        assert mine == "" or valid(case, mine), case
    print("ok")
