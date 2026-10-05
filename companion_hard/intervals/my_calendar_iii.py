"""
My Calendar III (LeetCode 732) - Hard
Chapter: intervals
Pattern: Difference array / prefix-sum sweep

Implement MyCalendarThree. book(start, end) adds the half-open event [start, end) and returns
the largest k such that some instant is covered by k events after this booking.
Example: book(10, 20) -> 1; book(50, 60) -> 1; book(10, 40) -> 2; book(5, 15) -> 3
"""


# --- brute force ---
class BruteForce:
    """Store every event; after each booking count the overlap at every start. O(n^2) per book."""

    def __init__(self):
        self.events = []

    def book(self, start, end):
        self.events.append((start, end))
        best = 0
        for point, _ in self.events:          # the max overlap happens at some start
            covering = 0
            for other_start, other_end in self.events:
                if other_start <= point < other_end:
                    covering += 1
            best = max(best, covering)
        return best


# --- optimal ---
class MyCalendarThree:
    """+1 at each start, -1 at each end; a sweep in time order sums them. O(n log n) per book."""

    def __init__(self):
        self.change = {}                      # time -> net change in open events there

    def book(self, start, end):
        self.change[start] = self.change.get(start, 0) + 1
        self.change[end] = self.change.get(end, 0) - 1
        best = 0
        open_events = 0
        for time in sorted(self.change):      # running total = events open at this time
            open_events += self.change[time]
            best = max(best, open_events)
        return best


# --- try the brute force ---
cal = BruteForce()
print(cal.book(10, 20))   # -> 1
print(cal.book(50, 60))   # -> 1
print(cal.book(10, 40))   # -> 2
print(cal.book(5, 15))    # -> 3
print(cal.book(5, 10))    # -> 3
print(cal.book(25, 55))   # -> 3


# --- try the optimal ---
cal = MyCalendarThree()
print(cal.book(10, 20))   # -> 1
print(cal.book(50, 60))   # -> 1
print(cal.book(10, 40))   # -> 2
print(cal.book(5, 15))    # -> 3
print(cal.book(5, 10))    # -> 3
print(cal.book(25, 55))   # -> 3
