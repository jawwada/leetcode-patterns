"""
My Calendar I and II - Bookings Without Double or Triple Overlaps

Book half-open events [start, end). MyCalendar rejects an event that overlaps
any booking; MyCalendarTwo allows a double booking but rejects a triple one.
MyCalendar: book(10, 20), book(15, 25), book(20, 30) -> True, False, True.
"""


# --- algorithm ---
class MyCalendar:
    """Bookings sorted by start; only the two neighbors of the insertion slot
    can overlap a new event. O(log n) search, O(n) list insert."""

    def __init__(self):
        self.starts = []                # starts of the bookings, sorted
        self.ends = []                  # ends[i] goes with starts[i]

    def book(self, start, end):
        """Find the slot by binary search, check both neighbors. O(n)."""
        left = 0
        right = len(self.starts)
        while left < right:             # first booking with a start >= start
            mid = (left + right) // 2
            if self.starts[mid] < start:
                left = mid + 1
            else:
                right = mid
        if left < len(self.starts) and self.starts[left] < end:
            return False                # the next booking starts too soon
        if left > 0 and self.ends[left - 1] > start:
            return False                # the previous booking ends too late
        self.starts.insert(left, start)
        self.ends.insert(left, end)
        return True


class MyCalendarTwo:
    """Every booking plus the overlaps already booked twice; an event that
    meets an overlap would make a triple booking. O(n) per book."""

    def __init__(self):
        self.bookings = []              # every accepted (start, end)
        self.overlaps = []              # the parts that are booked twice

    def book(self, start, end):
        """Reject if the event meets an overlap; else record the overlaps it
        creates with the bookings. O(n)."""
        for overlap_start, overlap_end in self.overlaps:
            if overlap_start < end and start < overlap_end:
                return False            # that time would be booked 3 times
        for booked_start, booked_end in self.bookings:
            if booked_start < end and start < booked_end:
                low = max(start, booked_start)
                high = min(end, booked_end)
                self.overlaps.append((low, high))   # now booked twice
        self.bookings.append((start, end))
        return True


# --- try it ---
calendar = MyCalendar()
print(calendar.book(10, 20), calendar.book(15, 25))     # -> True False
print(calendar.book(20, 30), calendar.book(5, 10))      # -> True True
print(calendar.book(0, 6), calendar.starts)             # -> False [5, 10, 20]
two = MyCalendarTwo()
print(two.book(10, 20), two.book(50, 60))               # -> True True
print(two.book(10, 40), two.book(5, 15))                # -> True False
print(two.book(5, 10), two.book(25, 55))                # -> True True
print(two.overlaps)             # -> [(10, 20), (50, 55), (25, 40)]
