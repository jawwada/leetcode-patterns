"""
Design Movie Rental System (LeetCode 1912) - Hard
Chapter: design
Pattern: Heaps with lazy deletion by version stamp

There are n shops, and entries[i] = [shop, movie, price] means shop has one copy of movie at that
price. search(movie) returns up to 5 shops with an unrented copy, cheapest first, ties broken by
shop id. rent(shop, movie) and drop(shop, movie) rent and return that copy. report() returns up to
5 rented copies as [shop, movie], cheapest first, ties broken by shop then movie.
Example: entries [[0,1,5],[0,2,6],[0,3,7],[1,1,4],[1,2,7],[2,1,5]]: search(1) -> [1,0,2];
rent(0,1); rent(1,2); report() -> [[0,1],[1,2]]; drop(1,2); search(2) -> [0,1].
"""
import heapq                                  # heappush / heappop keep the smallest at index 0


# --- brute force ---
class BruteForce:
    """Dict (shop, movie) -> [price, rented]; each query sorts every copy. O(E log E) per query."""

    def __init__(self, n, entries):
        self.items = {}
        for entry in entries:
            shop, movie, price = entry[0], entry[1], entry[2]
            self.items[(shop, movie)] = [price, False]

    def search(self, movie):
        candidates = []
        for (shop, other_movie) in self.items:    # every copy in the system, every query
            price, rented = self.items[(shop, other_movie)]
            if other_movie == movie and not rented:
                candidates.append((price, shop))
        candidates.sort()
        shops = []
        for price, shop in candidates[:5]:
            shops.append(shop)
        return shops

    def rent(self, shop, movie):
        self.items[(shop, movie)][1] = True

    def drop(self, shop, movie):
        self.items[(shop, movie)][1] = False

    def report(self):
        candidates = []
        for (shop, movie) in self.items:
            price, rented = self.items[(shop, movie)]
            if rented:
                candidates.append((price, shop, movie))
        candidates.sort()
        result = []
        for price, shop, movie in candidates[:5]:
            result.append([shop, movie])
        return result


# --- optimal ---
class MovieRentingSystem:
    """Two heaps; a stale entry is one whose stamp is no longer current. O(log E) per operation."""

    def __init__(self, n, entries):
        self.price = {}                       # (shop, movie) -> price
        self.version = {}                     # (shop, movie) -> stamp, bumped on every rent / drop
        self.available = {}                   # movie -> heap of (price, shop, movie, stamp)
        self.rented = []                      # heap of (price, shop, movie, stamp)
        for entry in entries:
            shop, movie, price = entry[0], entry[1], entry[2]
            self.price[(shop, movie)] = price
            self.version[(shop, movie)] = 0
            if movie not in self.available:
                self.available[movie] = []
            heapq.heappush(self.available[movie], (price, shop, movie, 0))

    def is_alive(self, item):
        price, shop, movie, stamp = item
        return self.version[(shop, movie)] == stamp   # an old stamp means the copy moved heaps

    def top5(self, heap):
        kept = []
        while len(heap) > 0 and len(kept) < 5:
            item = heapq.heappop(heap)
            if self.is_alive(item):
                kept.append(item)             # stale entries fall out here, for good
        for item in kept:
            heapq.heappush(heap, item)        # put the live ones back
        return kept

    def search(self, movie):
        if movie not in self.available:
            return []
        shops = []
        for price, shop, other_movie, stamp in self.top5(self.available[movie]):
            shops.append(shop)
        return shops

    def rent(self, shop, movie):
        self.version[(shop, movie)] += 1      # the copy sitting in available is now stale
        stamp = self.version[(shop, movie)]
        heapq.heappush(self.rented, (self.price[(shop, movie)], shop, movie, stamp))

    def drop(self, shop, movie):
        self.version[(shop, movie)] += 1      # the copy sitting in rented is now stale
        stamp = self.version[(shop, movie)]
        heapq.heappush(self.available[movie], (self.price[(shop, movie)], shop, movie, stamp))

    def report(self):
        result = []
        for price, shop, movie, stamp in self.top5(self.rented):
            result.append([shop, movie])
        return result


# --- try the brute force ---
mrs = BruteForce(3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]])
print(mrs.search(1))     # -> [1, 0, 2]
mrs.rent(0, 1)
mrs.rent(1, 2)
print(mrs.report())      # -> [[0, 1], [1, 2]]
mrs.drop(1, 2)
print(mrs.search(2))     # -> [0, 1]
print(mrs.search(9))     # -> []
mrs.drop(0, 1)
print(mrs.report())      # -> []
print(mrs.search(1))     # -> [1, 0, 2]


# --- try the optimal ---
mrs = MovieRentingSystem(3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]])
print(mrs.search(1))     # -> [1, 0, 2]
mrs.rent(0, 1)
mrs.rent(1, 2)
print(mrs.report())      # -> [[0, 1], [1, 2]]
mrs.drop(1, 2)
print(mrs.search(2))     # -> [0, 1]
print(mrs.search(9))     # -> []
mrs.drop(0, 1)
print(mrs.report())      # -> []
print(mrs.search(1))     # -> [1, 0, 2]
