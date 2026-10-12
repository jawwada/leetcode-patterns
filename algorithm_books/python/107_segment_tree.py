"""
Segment Tree - Range Sums with Point Updates

Keep an array under two operations, update(index, value), which sets one
element, and query(left, right), which sums nums[left..right], both O(log n):
[5, 8, 6, 3, 2, 7, 2, 6], query(2, 6) -> 20, then update(4, 9), query -> 27.
"""


# --- algorithm ---
class SegmentTree:
    """Node 1 owns the whole array, and node i hands the two halves of its
    segment to nodes 2i and 2i + 1; every node stores its segment's sum."""

    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)      # 4n slots always suffice
        if self.n > 0:
            self.build(nums, 1, 0, self.n - 1)

    def build(self, nums, node, lo, hi):
        """Fill the sums of node's subtree, which owns nums[lo..hi]. O(n)."""
        if lo == hi:
            self.tree[node] = nums[lo]      # a leaf owns one element
            return
        mid = (lo + hi) // 2
        self.build(nums, 2 * node, lo, mid)
        self.build(nums, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, index, value):
        """Set nums[index] to value. O(log n)."""
        self.update_at(1, 0, self.n - 1, index, value)

    def update_at(self, node, lo, hi, index, value):
        """Walk down to the leaf of index, then redo the sums on the way up."""
        if lo == hi:
            self.tree[node] = value
            return
        mid = (lo + hi) // 2
        if index <= mid:                    # index lies in the left half
            self.update_at(2 * node, lo, mid, index, value)
        else:
            self.update_at(2 * node + 1, mid + 1, hi, index, value)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left, right):
        """Sum of nums[left..right], both ends included. O(log n)."""
        return self.query_at(1, 0, self.n - 1, left, right)

    def query_at(self, node, lo, hi, left, right):
        """Sum of the part of node's segment nums[lo..hi] inside left..right."""
        if right < lo or hi < left:
            return 0                        # no overlap
        if left <= lo and hi <= right:
            return self.tree[node]          # full overlap: the stored sum
        mid = (lo + hi) // 2                # partial overlap: both halves
        left_sum = self.query_at(2 * node, lo, mid, left, right)
        right_sum = self.query_at(2 * node + 1, mid + 1, hi, left, right)
        return left_sum + right_sum


# --- try it ---
tree = SegmentTree([5, 8, 6, 3, 2, 7, 2, 6])
print(tree.query(2, 6))                     # -> 20
tree.update(4, 9)                           # nums[4] becomes 9
print(tree.query(2, 6))                     # -> 27
print(tree.query(0, 7), tree.query(3, 3))   # -> 46 3
mixed = SegmentTree([-2, 0, 3, -5, 2, -1])
mixed.update(3, 4)
print(mixed.query(0, 2), mixed.query(2, 5))     # -> 1 8
