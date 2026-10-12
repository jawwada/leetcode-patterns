---
rank: 148
slug: quadtree
---

A quadtree stores points in the plane so that a box query reads only the part of the map the box covers, the query behind "find the drivers near this rider". `insert(x, y)` adds a point and `range_query(left, bottom, right, top)` returns the points inside the box, edges included. With nine drivers in a 16 by 16 square of city blocks, the box from `(2, 2)` to `(6, 6)` around a rider at `(4, 4)` returns `(3, 5)`, `(5, 6)` and `(6, 3)`.

Scanning every driver costs `O(n)` per query, and a busy city can send thousands of queries a second. A quadtree cuts the square into four equal quarters and keeps cutting wherever points crowd. Each node covers a square, given by its lower-left corner and its side, and a leaf holds up to 4 points. Inserting into a full leaf splits it into four children of half the side, south-west, south-east, north-west and north-east, and its points move down into the children whose squares hold them. Busy downtown blocks end up deep inside small squares while an empty suburb stays one big leaf, so the tree follows the density of the data.

A query walks down from the root and asks each node one question: does its square overlap the box? If not, the whole square is skipped and every point beneath it goes unread. If so, a leaf tests its few points and an inner node asks its four children. A square owns its left and bottom edges but not its right and top ones, so each point lives in exactly one leaf. A leaf whose side has shrunk to `MIN_SIZE` keeps every point it receives, so a pile of identical points cannot split forever.

```text
insert (1, 2) (3, 5) (6, 1) (2, 7): they fill the root, a leaf of 4
insert (5, 6): the root splits, all 4 points fall into SW, and SW splits too
insert (12, 3) (10, 12) (14, 9) (6, 3)

root  [0,16)×[0,16)
├── SW  [0,8)×[0,8)
│   ├── SW  [0,4)×[0,4)      (1, 2)
│   ├── SE  [4,8)×[0,4)      (6, 1) (6, 3)
│   ├── NW  [0,4)×[4,8)      (3, 5) (2, 7)
│   └── NE  [4,8)×[4,8)      (5, 6)
├── SE  [8,16)×[0,8)         (12, 3)
├── NW  [0,8)×[8,16)         empty
└── NE  [8,16)×[8,16)        (10, 12) (14, 9)

range_query(2, 2, 6, 6), the box around a rider at (4, 4):
  it overlaps root, SW and all four children of SW, which hold 6 points
  (1, 2) ✗   (6, 1) ✗   (6, 3) ✓   (3, 5) ✓   (2, 7) ✗   (5, 6) ✓
  SE, NW and NE miss the box: skipped, their 3 points never read
  → sorted: [(3, 5), (5, 6), (6, 3)]
```

```pseudo
CAPACITY ← 4                            // points a leaf holds before it splits
MIN_SIZE ← 1                            // a leaf this small never splits

CLASS QuadTree
    FUNCTION Init(x, y, size)
        self.x ← x                      // lower-left corner
        self.y ← y
        self.size ← size
        self.points ← empty list        // only leaves hold points
        self.children ← null            // SW, SE, NW, NE once split

    FUNCTION Contains(px, py)           // left and bottom edges included
        inside_x ← self.x ≤ px AND px < self.x + self.size
        inside_y ← self.y ≤ py AND py < self.y + self.size
        RETURN inside_x AND inside_y

    FUNCTION Insert(px, py)
        IF NOT self.Contains(px, py)
            RETURN false                // not in this square
        IF self.children = null
            IF len(self.points) < CAPACITY OR self.size ≤ MIN_SIZE
                self.points.append((px, py))
                RETURN true
            self.Split()                // a full leaf becomes four leaves
        FOR EACH child IN self.children
            IF child.Insert(px, py)     // exactly one child holds it
                RETURN true
        RETURN false

    FUNCTION Split()
        half ← self.size / 2
        self.children ← empty list      // SW, SE, NW, NE
        FOR EACH (dx, dy) IN [(0, 0), (half, 0), (0, half), (half, half)]
            self.children.append(QuadTree(self.x + dx, self.y + dy, half))
        old_points ← self.points
        self.points ← empty list
        FOR EACH (px, py) IN old_points
            self.Insert(px, py)         // now lands in a child

    FUNCTION RangeQuery(left, bottom, right, top)
        found ← empty list
        IF left ≥ self.x + self.size OR right < self.x
            RETURN found                // no overlap in x: prune
        IF bottom ≥ self.y + self.size OR top < self.y
            RETURN found                // no overlap in y: prune
        FOR EACH (px, py) IN self.points
            IF left ≤ px AND px ≤ right AND bottom ≤ py AND py ≤ top
                found.append((px, py))
        IF self.children ≠ null
            FOR EACH child IN self.children
                found.extend(child.RangeQuery(left, bottom, right, top))
        RETURN found
```

An insert walks one path down from the root, `O(depth)`, and for evenly spread points the depth is `O(log n)`. A query costs the nodes it visits plus the points it reads: a box about the size of a leaf touches a few leaves and their ancestors, roughly `O(log n + k)` for k answers, and a radius query is a box query plus a distance check. The signals are points in the plane and questions about what is near: the drivers around a rider, the restaurants within a mile, the pins in a map's visible window. A geohash writes the same picture as a string: interleaved bits of longitude and latitude pick a half, then a half of that, so nearby points share a prefix, though a query must also read the 8 neighboring cells, since a point just across an edge can get a different prefix. Google's S2 library numbers quadtree cells on the faces of a cube along a Hilbert curve. A k-d tree splits at the median instead, alternating x and y, and stays balanced for points known in advance. The classic mistake is pruning by corners, asking whether a corner of either shape lies inside the other: a thin box that crosses a square from edge to edge has no such corner, so the square is skipped and the points in its middle are lost.

*Practice:* LC 427 Construct Quad Tree · LC 558 Logical OR of Two Binary Grids Represented as Quad-Trees · LC 973 K Closest Points to Origin
