"""
Design Movie Rental System (LeetCode 1912)  — Hard
Pattern: Heaps with lazy deletion by version stamp

Problem
-------
n shops; entries[i] = [shop, movie, price] says shop has one copy of movie at that price.
search(movie): up to 5 shops with an UNRENTED copy, cheapest first, ties by shop id.
rent(shop, movie) / drop(shop, movie): rent or return that copy.
report(): up to 5 RENTED copies as [shop, movie], cheapest first, ties by shop then movie.
Example: entries [[0,1,5],[0,2,6],[0,3,7],[1,1,4],[1,2,7],[2,1,5]]: search(1) -> [1,0,2];
rent(0,1); rent(1,2); report() -> [[0,1],[1,2]]; drop(1,2); search(2) -> [0,1].

Brute force
-----------
Store (shop, movie) -> [price, rented]. rent/drop flip a flag in O(1); search filters and sorts
every entry of that movie, report filters and sorts every rented entry: O(E log E) per query for
E entries, O(E) space. The wasted work is re-sorting the whole collection on every query to read
only its first five elements, when a rent or drop changes exactly one element.

From brute force to optimal
---------------------------
The redundancy is re-sorting an almost-unchanged collection. A sorted container that supports
insert, delete and "first 5" would fix it, but Python has none built in. Heaps give insert and
top in O(log n); the missing piece is deletion of an arbitrary element, which we make lazy: leave
the entry in the heap and recognise it as dead when it reaches the top. The classic "check a
rented set" test fails here because a copy rented and then dropped would exist twice in the
available heap and be reported twice. So stamp every entry with a version number: ver[(shop,
movie)] is bumped on every rent and drop, each state change pushes exactly one entry carrying the
new stamp into the heap it now belongs in, and an entry is alive iff its stamp is current. Dead
entries are discarded the moment they surface; alive ones popped for a top-5 are pushed back.
Each entry is pushed once and popped dead at most once, so every operation is amortised O(log E)
plus 5 log E for the answer.

Intuition
---------
Think of a copy as a token that moves between two sorted shelves, "available" and "rented". We
never physically move it; we lay a fresh token on the destination shelf and leave the old one
behind with an outdated serial number. Whoever picks up a token checks the serial against the
register and throws away stale tokens. Because every state change issues exactly one new token,
the live tokens are always a perfect copy of the true state.

Geometric view
--------------
Two priority heaps drawn as triangles: one per movie ordered by (price, shop), and one global
ordered by (price, shop, movie). Each rent/drop drops a new node into one triangle and greys out
a node in the other. A query skims the top of a triangle, brushing grey nodes aside, lifts the
first five live nodes out, reads them, and drops them back in.

Steps
-----
1. price[(shop, movie)]; ver[(shop, movie)] = 0; avail[movie] heap of (price, shop, stamp);
   out heap of (price, shop, movie, stamp).
2. rent: ver += 1; push (price, shop, movie, ver) into out. The copy in avail is now stale.
3. drop: ver += 1; push (price, shop, ver) into avail[movie]. The copy in out is now stale.
4. top5(heap, alive): pop until 5 alive entries are collected, discarding stale ones; push the
   alive ones back; return them.
5. search(movie) -> shops of top5(avail[movie]); report() -> [shop, movie] of top5(out).

Complexity: O(log E) amortised per rent/drop, O(log E) per query (5 pops and 5 pushes plus
            stale pops paid for by their earlier push); O(E + ops) space.
Pitfalls: lazy deletion by flag alone (duplicates after rent -> drop); forgetting to push alive
          entries back after reading them; wrong tie order (report breaks ties by shop, then
          movie); defaultdict for ver is required because entries never rented have no stamp.
"""
import random
from collections import defaultdict
from heapq import heappop, heappush
from typing import Callable, List


class MovieRentingSystem:
    def __init__(self, n: int, entries: List[List[int]]):
        self.price = {}                          # (shop, movie) -> price
        self.ver = defaultdict(int)              # (shop, movie) -> stamp, bumped on rent/drop
        self.avail = defaultdict(list)           # movie -> heap of (price, shop, stamp)
        self.out = []                            # heap of (price, shop, movie, stamp)
        for shop, movie, p in entries:
            self.price[(shop, movie)] = p
            heappush(self.avail[movie], (p, shop, 0))

    def _top5(self, heap: list, alive: Callable[[tuple], bool]) -> list:
        kept = []
        while heap and len(kept) < 5:
            item = heappop(heap)
            if alive(item):                      # stale entries fall out here, for good
                kept.append(item)
        for item in kept:
            heappush(heap, item)                 # put the live ones back
        return kept

    def search(self, movie: int) -> List[int]:
        def alive(e: tuple) -> bool:
            return self.ver[(e[1], movie)] == e[2]
        return [shop for _, shop, _ in self._top5(self.avail[movie], alive)]

    def rent(self, shop: int, movie: int) -> None:
        self.ver[(shop, movie)] += 1             # the copy sitting in avail is now stale
        heappush(self.out, (self.price[(shop, movie)], shop, movie, self.ver[(shop, movie)]))

    def drop(self, shop: int, movie: int) -> None:
        self.ver[(shop, movie)] += 1             # the copy sitting in out is now stale
        heappush(self.avail[movie], (self.price[(shop, movie)], shop, self.ver[(shop, movie)]))

    def report(self) -> List[List[int]]:
        def alive(e: tuple) -> bool:
            return self.ver[(e[1], e[2])] == e[3]
        return [[shop, movie] for _, shop, movie, _ in self._top5(self.out, alive)]


class BruteForce:
    """Flat dict (shop, movie) -> [price, rented]; every query filters and sorts everything."""

    def __init__(self, n: int, entries: List[List[int]]):
        self.items = {(s, m): [p, False] for s, m, p in entries}

    def search(self, movie: int) -> List[int]:
        cands = sorted((p, s) for (s, m), (p, r) in self.items.items() if m == movie and not r)
        return [s for _, s in cands[:5]]

    def rent(self, shop: int, movie: int) -> None:
        self.items[(shop, movie)][1] = True

    def drop(self, shop: int, movie: int) -> None:
        self.items[(shop, movie)][1] = False

    def report(self) -> List[List[int]]:
        cands = sorted((p, s, m) for (s, m), (p, r) in self.items.items() if r)
        return [[s, m] for _, s, m in cands[:5]]


if __name__ == "__main__":
    mrs = MovieRentingSystem(3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]])
    assert mrs.search(1) == [1, 0, 2]
    mrs.rent(0, 1)
    mrs.rent(1, 2)
    assert mrs.report() == [[0, 1], [1, 2]]
    mrs.drop(1, 2)
    assert mrs.search(2) == [0, 1]
    assert mrs.search(9) == []                                    # unknown movie
    mrs.drop(0, 1)
    assert mrs.report() == []
    assert mrs.search(1) == [1, 0, 2]                             # no duplicate shop 0

    random.seed(4)
    for _ in range(30):
        pairs = random.sample([(s, m) for s in range(4) for m in range(4)], 9)
        entries = [[s, m, random.randint(1, 6)] for s, m in pairs]
        fast, slow = MovieRentingSystem(4, entries), BruteForce(4, entries)
        rented = set()
        for _ in range(120):
            op = random.random()
            if op < 0.3:
                m = random.randint(0, 4)
                assert fast.search(m) == slow.search(m)
            elif op < 0.55 and len(rented) < len(pairs):
                s, m = random.choice([p for p in pairs if p not in rented])
                rented.add((s, m))
                fast.rent(s, m)
                slow.rent(s, m)
            elif op < 0.8 and rented:
                s, m = random.choice(sorted(rented))
                rented.remove((s, m))
                fast.drop(s, m)
                slow.drop(s, m)
            else:
                assert fast.report() == slow.report()
    print("ok")
