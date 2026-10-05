"""
Logger Rate Limiter (LeetCode 359) - Easy
Chapter: design
Pattern: Hash map of next-allowed timestamps

Implement Logger.should_print_message(timestamp, message) -> bool: a message may be printed only
if the same message was not printed in the previous 10 seconds (printed at t means it is next
allowed at t + 10). Timestamps arrive in non-decreasing order.
Example: (1,"foo") True, (2,"bar") True, (3,"foo") False, (8,"bar") False, (11,"foo") True.
"""


# --- brute force ---
class BruteForce:
    """Keep every printed (timestamp, message); scan the whole log on each call. O(n) per call."""

    def __init__(self):
        self.printed = []

    def should_print_message(self, timestamp, message):
        for old_time, old_message in self.printed:
            if old_message == message and timestamp - old_time < 10:
                return False              # the same message was printed less than 10 s ago
        self.printed.append((timestamp, message))
        return True


# --- optimal ---
class Logger:
    """Dict message -> the earliest timestamp it may print again. O(1) per call."""

    def __init__(self):
        self.next_ok = {}

    def should_print_message(self, timestamp, message):
        allowed_at = self.next_ok.get(message, 0)     # never seen: allowed from time 0
        if timestamp < allowed_at:
            return False
        self.next_ok[message] = timestamp + 10        # blocked for the next 10 seconds
        return True


# --- try the brute force ---
lg = BruteForce()
print(lg.should_print_message(1, "foo"))    # -> True
print(lg.should_print_message(2, "bar"))    # -> True
print(lg.should_print_message(3, "foo"))    # -> False
print(lg.should_print_message(8, "bar"))    # -> False
print(lg.should_print_message(10, "foo"))   # -> False
print(lg.should_print_message(11, "foo"))   # -> True


# --- try the optimal ---
lg = Logger()
print(lg.should_print_message(1, "foo"))    # -> True
print(lg.should_print_message(2, "bar"))    # -> True
print(lg.should_print_message(3, "foo"))    # -> False
print(lg.should_print_message(8, "bar"))    # -> False
print(lg.should_print_message(10, "foo"))   # -> False
print(lg.should_print_message(11, "foo"))   # -> True
