"""
Quadtree - Points in Squares, Split When Full

Store points so that a box query reads only the part of the map it covers,
as when an app looks for the drivers near a rider: 9 drivers in a 16 x 16
square, box from (2, 2) to (6, 6) -> [(3, 5), (5, 6), (6, 3)].
"""


# --- algorithm ---
CAPACITY = 4                        # points a leaf holds before it splits
MIN_SIZE = 1                        # a leaf this small never splits


class QuadTree:
    """A square [x, x + size) by [y, y + size); a leaf holds up to CAPACITY
    points and a full leaf splits into four half-size squares."""

    def __init__(self, x, y, size):
        self.x = x                  # lower-left corner
        self.y = y
        self.size = size
        self.points = []            # only leaves hold points
        self.children = None        # SW, SE, NW, NE once split

    def contains(self, px, py):
        """Left and bottom edges belong to the square, right and top do not."""
        inside_x = self.x <= px < self.x + self.size
        inside_y = self.y <= py < self.y + self.size
        return inside_x and inside_y

    def insert(self, px, py):
        """Put the point in the leaf whose square holds it. O(depth)."""
        if not self.contains(px, py):
            return False                    # not in this square
        if self.children is None:
            if len(self.points) < CAPACITY or self.size <= MIN_SIZE:
                self.points.append((px, py))
                return True
            self.split()                    # a full leaf becomes four leaves
        for child in self.children:
            if child.insert(px, py):        # exactly one child holds it
                return True
        return False

    def split(self):
        """Make four half-size children and pass this leaf's points down."""
        half = self.size / 2
        self.children = []                  # SW, SE, NW, NE
        for dx, dy in [(0, 0), (half, 0), (0, half), (half, half)]:
            self.children.append(QuadTree(self.x + dx, self.y + dy, half))
        old_points = self.points
        self.points = []
        for px, py in old_points:
            self.insert(px, py)                 # now lands in a child

    def range_query(self, left, bottom, right, top):
        """Points with left <= x <= right and bottom <= y <= top; a square that
        misses the box is skipped whole. O(nodes visited + points read)."""
        found = []
        if left >= self.x + self.size or right < self.x:
            return found                    # no overlap in x: prune
        if bottom >= self.y + self.size or top < self.y:
            return found                    # no overlap in y: prune
        for px, py in self.points:
            if left <= px <= right and bottom <= py <= top:
                found.append((px, py))
        if self.children is not None:
            for child in self.children:
                found.extend(child.range_query(left, bottom, right, top))
        return found


# --- try it ---
tree = QuadTree(0, 0, 16)                   # a 16 x 16 square of city blocks
drivers = [(1, 2), (3, 5), (6, 1), (2, 7), (5, 6), (12, 3), (10, 12), (14, 9),
           (6, 3)]
for point in drivers:
    tree.insert(point[0], point[1])
print(sorted(tree.range_query(2, 2, 6, 6)))     # -> [(3, 5), (5, 6), (6, 3)]
print(sorted(tree.range_query(9, 8, 16, 16)))   # -> [(10, 12), (14, 9)]
print(tree.children[0].children[2].points)      # -> [(3, 5), (2, 7)]
print(tree.range_query(7, 13, 9, 15), tree.insert(16, 4))   # -> [] False
