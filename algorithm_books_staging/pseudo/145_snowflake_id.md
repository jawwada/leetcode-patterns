---
rank: 145
slug: snowflake_id
---

Design a generator of unique 64-bit ids for many machines that create records independently, with ids that sort roughly by creation time. Twitter's Snowflake packs three fields into one integer: 41 bits of milliseconds since a custom epoch, 10 bits of machine id and 12 bits of sequence number within the millisecond, with the sign bit left at 0. `next_id(now_ms)` takes the time as an argument, which keeps it deterministic and testable. On machine 5, two ids requested in millisecond 1000 after the epoch and one in millisecond 1001 are `4194324480`, `4194324481` and `4198518784`.

The obvious designs either coordinate or sprawl. A single database counter makes every id a round trip to one point of failure; a random 128-bit UUID needs no coordination but is twice as wide and scattered in time, so new rows land all over a database index instead of at its end. Snowflake removes the coordination by splitting the id space. The machine field gives each machine a private slice, so two machines never produce the same id, and within one machine the pair (millisecond, sequence) only has to never repeat, which takes nothing but local state. With the time in the highest bits, every id from a later millisecond is larger than every id from an earlier one, so sorting ids sorts them by time across the fleet, roughly: machine clocks drift apart by a few milliseconds, and inside one millisecond the machine id, not the true order, decides.

The generator remembers the millisecond of its latest id and that id's sequence number. A call in a new millisecond restarts the sequence at 0, and a call in the same millisecond takes the next number. After 4096 ids in one millisecond the 12 bits would overflow; the real generator spins until the clock ticks, and with the time passed in, it moves its stamp to the next millisecond itself, borrowing it from the future. Since the stamp can then run ahead of the clock, the generator keeps the latest clock reading separately: a call whose time is not past the stamp continues the sequence there, and only a time earlier than the previous call means the clock ran backwards, which the generator refuses rather than stamp ids with a time it cannot trust. Packing is two shifts and two ORs; decoding reverses them with shifts and masks, and AND-ing with `MAX_SEQUENCE = 4095`, twelve 1 bits, keeps exactly the low field.

```text
machine 5, epoch E = 1700000000000 (2023-11-14 22:13:20 UTC)
now - E   last_ms - E   sequence   id
1000      1000          0          4194324480    a new millisecond
1000      1000          1          4194324481    the same millisecond
1001      1001          0          4198518784    a new millisecond
999       clock moved backwards: 999 < 1001, no id

the second id, 4194324481, as 64 bits from bit 63 down to bit 0:
0 00000000000000000000000000000001111101000 0000000101 000000000001
│ └─── 41 bits: 1000 ms since the epoch ──┘ └── 5 ───┘ └──── 1 ───┘
sign                                        machine    sequence
decode: id >> 22 = 1000, (id >> 12) & 1023 = 5, id & 4095 = 1

machine 7, 4097 calls at now - E = 50: calls 1 to 4096 get
[50, 7, 0] to [50, 7, 4095]; call 4097 moves to the next ms: [51, 7, 0]
```

```pseudo
SEQUENCE_BITS ← 12                          // 4096 ids per millisecond
MACHINE_BITS ← 10                           // 1024 machines
TIME_SHIFT ← SEQUENCE_BITS + MACHINE_BITS   // time starts at bit 22
MAX_SEQUENCE ← (1 << SEQUENCE_BITS) - 1     // 4095: twelve 1 bits
MAX_MACHINE ← (1 << MACHINE_BITS) - 1       // 1023: ten 1 bits

CLASS SnowflakeGenerator
    FUNCTION Init(machine_id, epoch_ms)
        self.machine_id ← machine_id    // 0..1023, different on every machine
        self.epoch_ms ← epoch_ms        // custom epoch: time 0 for these ids
        self.last_clock ← -1            // the latest time a caller passed
        self.last_ms ← -1               // the millisecond in the latest id
        self.sequence ← 0               // the latest id's number in last_ms

    FUNCTION NextId(now_ms)
        IF now_ms < self.last_clock
            RAISE "clock moved backwards"
        self.last_clock ← now_ms
        IF now_ms > self.last_ms
            self.last_ms ← now_ms       // a new millisecond: restart at 0
            self.sequence ← 0
        ELSE
            self.sequence ← self.sequence + 1   // the same millisecond
            IF self.sequence > MAX_SEQUENCE
                self.last_ms ← self.last_ms + 1 // 4096 ids used: next ms
                self.sequence ← 0
        elapsed ← self.last_ms - self.epoch_ms
        time_part ← elapsed << TIME_SHIFT                   // bits 22..62
        machine_part ← self.machine_id << SEQUENCE_BITS     // bits 12..21
        RETURN time_part | machine_part | self.sequence     // bits 0..11

FUNCTION DecodeId(snowflake_id)
    sequence ← snowflake_id & MAX_SEQUENCE                  // low 12 bits
    machine_id ← (snowflake_id >> SEQUENCE_BITS) & MAX_MACHINE
    elapsed ← snowflake_id >> TIME_SHIFT                    // the rest
    RETURN [elapsed, machine_id, sequence]
```

Each id costs `O(1)` time and a handful of numbers of state. The field widths set the capacity: 41 bits of milliseconds last about 69.7 years, so counting from the Unix epoch would run out in 2039, while the epoch above lasts until 2093; 10 bits allow 1024 machines, and 12 bits allow 4096 ids per millisecond per machine, about four million a second. Machine ids are the only coordination, assigned once at deployment from configuration or a service such as ZooKeeper; Twitter split the field into 5 bits of data center and 5 of worker. Reach for this layout when ids must be unique across servers without a central counter, ordered by time and small enough for a 64-bit column; the URL shortener of #100 can encode such ids in base 62. The classic mistake is wrapping the sequence with `(sequence + 1) & 4095` and carrying on, so the 4097th id of a millisecond repeats the first. Another is a wrong shift: moving the time by 12 instead of 22 lands its low bits on the machine field, and two machines can mint the same id.

*Practice:* LC 535 Encode and Decode TinyURL · LC 190 Reverse Bits · LC 191 Number of 1 Bits
