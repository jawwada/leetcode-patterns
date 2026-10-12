---
rank: 98
slug: my_calendar
---

Build a calendar that accepts or refuses events one at a time. An event is the half-open interval `[start, end)`, so `[10, 20)` and `[20, 30)` only touch. `MyCalendar.book(start, end)` adds the event and returns `true` unless it overlaps a booking, in which case it returns `false` and changes nothing. `MyCalendarTwo.book` lets two events overlap but refuses one that would put any instant under three. The first calendar accepts `[10, 20)`, refuses `[15, 25)` and accepts `[20, 30)`. The second accepts `[10, 20)`, `[50, 60)` and `[10, 40)`, then refuses `[5, 15)`, because the time from 10 to 15 would be booked three times.

The brute force compares a new event with every booking, `O(n)` comparisons per call. Two half-open intervals overlap exactly when each starts before the other ends. In My Calendar I the accepted bookings never overlap, so sorted by start they are also sorted by end, and they lie on the time line like disjoint tiles. Binary search finds the slot where the new event would go, the first booking whose start is at least the new start (the lower bound of #14). Only the two tiles beside that slot can collide with the event: the next one if it starts before the new end, the previous one if it ends after the new start. Every tile further left ends no later than the previous one starts, and every tile further right starts after the next one does. If both neighbors are clear, the event is inserted at the slot and the tiles stay sorted.

My Calendar II cannot use tiles, because its bookings may overlap. It keeps two lists instead: all the bookings, and the overlaps, the stretches of time already booked twice. A new event that meets any overlap would create a triple booking, so it is refused before anything changes. Otherwise each intersection of the event with an existing booking, from the later start to the earlier end, is now booked twice and joins the overlaps, and the event joins the bookings.

```text
MyCalendar: the slot is the first booking whose start is ≥ the new start
book       slot   previous   next       verdict
[10, 20)    0     none       none       ✓
[15, 25)    1     [10, 20)   none       ✗  the previous ends at 20 > 15
[20, 30)    1     [10, 20)   none       ✓  20 > 20 is false: touching is fine
[5, 10)     0     none       [10, 20)   ✓  10 < 10 is false
[0, 6)      0     none       [5, 10)    ✗  the next starts at 5 < 6
time   0    5    10   15   20   25   30
            ├────┼─────────┼─────────┤   starts [5, 10, 20], ends [10, 20, 30]

MyCalendarTwo: the overlaps hold the time already booked twice
book       meets an overlap?    new overlaps         verdict
[10, 20)   no                   none                 ✓
[50, 60)   no                   none                 ✓
[10, 40)   no                   [10, 20)             ✓
[5, 15)    yes, [10, 20)        none                 ✗  10 to 15 would be triple
[5, 10)    no, it only touches  none                 ✓
[25, 55)   no                   [50, 55), [25, 40)   ✓
```

```pseudo
CLASS MyCalendar
    FUNCTION Init()
        self.starts ← empty list               // starts of the bookings, sorted
        self.ends ← empty list                 // ends[i] goes with starts[i]

    FUNCTION Book(start, end)
        left ← 0
        right ← len(self.starts)
        WHILE left < right                     // first booking starting ≥ start
            mid ← floor((left + right) / 2)
            IF self.starts[mid] < start
                left ← mid + 1
            ELSE
                right ← mid
        IF left < len(self.starts) AND self.starts[left] < end
            RETURN false                       // the next starts too soon
        IF left > 0 AND self.ends[left - 1] > start
            RETURN false                       // the previous ends too late
        self.starts.insert(left, start)
        self.ends.insert(left, end)
        RETURN true

CLASS MyCalendarTwo
    FUNCTION Init()
        self.bookings ← empty list             // every accepted (start, end)
        self.overlaps ← empty list             // the parts booked twice

    FUNCTION Book(start, end)
        FOR EACH (overlap_start, overlap_end) IN self.overlaps
            IF overlap_start < end AND start < overlap_end
                RETURN false                   // it would be booked 3 times
        FOR EACH (booked_start, booked_end) IN self.bookings
            IF booked_start < end AND start < booked_end
                low ← max(start, booked_start)
                high ← min(end, booked_end)
                self.overlaps.append((low, high))   // now booked twice
        self.bookings.append((start, end))
        RETURN true
```

My Calendar I spends only `O(log n)` comparisons on the search, but inserting into the middle of an array shifts every later entry, so a booking costs `O(n)`; a balanced search tree, such as Java's `TreeMap` with `floorKey` and `ceilingKey`, brings it to `O(log n)`. My Calendar II costs `O(n)` per booking, and because no instant is ever booked three times there are always fewer overlaps than bookings. My Calendar III asks for the largest number of events sharing an instant: a map of +1 at every start and -1 at every end, walked in time order, counts the open events at each moment, the sweep line that also solves Meeting Rooms II (#27). The signals are requests accepted or refused one at a time under a cap on how many events may share an instant. The classic mistakes are treating the intervals as closed, which refuses `[20, 30)` after `[10, 20)`, and, in the second calendar, counting how many bookings a new event meets: `[15, 25)` meets both `[10, 20)` and `[20, 30)`, yet no instant would be booked three times.

*Practice:* LC 729 My Calendar I · LC 731 My Calendar II · LC 732 My Calendar III
