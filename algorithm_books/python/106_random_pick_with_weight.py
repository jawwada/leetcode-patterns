"""
Random Pick with Weight - Prefix Sums + Binary Search

Given positive weights w, pick_index returns index i with probability
w[i] / sum(w): w = [1, 3, 2] -> index 0, 1, 2 with chances 1/6, 3/6, 2/6.
"""
import random                       # randint(a, b) includes both ends


# --- algorithm ---
class WeightedPicker:
    """Prefix sums of the weights; a pick binary-searches a uniform target."""

    def __init__(self, w):
        self.prefix = []            # prefix[i] = w[0] + ... + w[i]
        running = 0
        for weight in w:
            running += weight
            self.prefix.append(running)
        self.total = running

    def lower_bound(self, target):
        """First index i with prefix[i] >= target: the owner of target.
        O(log n)."""
        lo = 0
        hi = len(self.prefix)       # half-open [lo, hi)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.prefix[mid] < target:
                lo = mid + 1        # mid's whole range lies below target
            else:
                hi = mid            # mid's range reaches target: keep it
        return lo

    def pick_index(self):
        """Draw a target uniformly from 1..total, return its owner. O(log n)."""
        target = random.randint(1, self.total)
        return self.lower_bound(target)


def is_fair(w, draws):
    """Index i should win about draws * w[i] / total picks. O(draws log n)."""
    picker = WeightedPicker(w)
    counts = [0] * len(w)
    for trial in range(draws):
        i = picker.pick_index()
        counts[i] += 1
    for i in range(len(w)):
        expected = draws * w[i] / picker.total
        if abs(counts[i] - expected) > 0.05 * expected:
            return False            # more than 5 percent off
    return True


# --- try it ---
picker = WeightedPicker([1, 3, 2])
print(picker.prefix, picker.total)          # -> [1, 4, 6] 6
owners = []
for target in range(1, 7):
    owners.append(picker.lower_bound(target))
print(owners)                               # -> [0, 1, 1, 1, 2, 2]
random.seed(7)
print(is_fair([1, 3, 2], 60000))            # -> True
print(is_fair([5, 1, 1, 10, 3], 60000))     # -> True
print(WeightedPicker([42]).pick_index())    # -> 0
