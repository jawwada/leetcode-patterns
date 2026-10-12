"""
Design Underground System - Open Trips and Route Totals in Two Maps

Track a metro: check_in(card_id, station, t), check_out(card_id, station, t)
and get_average_time(start, end), the mean time of the finished trips from
start to end: Leyton-to-Waterloo trips from 3 to 15 and 10 to 20 -> 11.0.
"""


# --- algorithm ---
class UndergroundSystem:
    """Map card -> open trip, map (start, end) -> [total_time, count].
    Every call O(1)."""

    def __init__(self):
        self.open_trips = {}        # card_id -> (start station, start time)
        self.routes = {}            # (start, end) -> [total_time, count]

    def check_in(self, card_id, station, t):
        """Remember where and when the card entered. O(1)."""
        self.open_trips[card_id] = (station, t)

    def check_out(self, card_id, station, t):
        """Close the card's trip and add it to its route's totals. O(1)."""
        start, start_time = self.open_trips[card_id]
        del self.open_trips[card_id]        # the trip is over
        route = (start, station)            # direction matters
        if route not in self.routes:
            self.routes[route] = [0, 0]     # [total_time, count]
        self.routes[route][0] += t - start_time     # aggregate on write
        self.routes[route][1] += 1

    def get_average_time(self, start, end):
        """Divide the route's total time by its trip count. O(1)."""
        total_time, count = self.routes[(start, end)]
        return total_time / count


# --- try it ---
metro = UndergroundSystem()
metro.check_in(45, "Leyton", 3)
metro.check_in(32, "Paradise", 8)
metro.check_in(27, "Leyton", 10)
metro.check_out(45, "Waterloo", 15)     # 12 minutes
metro.check_out(27, "Waterloo", 20)     # 10 minutes
metro.check_out(32, "Cambridge", 22)    # 14 minutes
print(metro.get_average_time("Paradise", "Cambridge"))  # -> 14.0
print(metro.get_average_time("Leyton", "Waterloo"))     # -> 11.0
metro.check_in(10, "Leyton", 24)        # an open trip changes no average
print(metro.get_average_time("Leyton", "Waterloo"))     # -> 11.0
metro.check_out(10, "Waterloo", 38)     # 14 minutes
print(metro.get_average_time("Leyton", "Waterloo"))     # -> 12.0
print(metro.routes[("Leyton", "Waterloo")], metro.open_trips)   # -> [36, 3] {}
