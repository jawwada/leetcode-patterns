"""
Unique ID Generator - Snowflake: Time, Machine and Sequence Bits

Hand out 64-bit ids, unique across machines and roughly sorted by time, with
no coordination: 41 bits of milliseconds since a custom epoch, 10 bits of
machine id, 12 bits of sequence. Machine 5, two ids in millisecond 1000 after
the epoch, one in 1001 -> 4194324480, 4194324481, 4198518784.
"""


# --- algorithm ---
SEQUENCE_BITS = 12                          # 4096 ids per millisecond
MACHINE_BITS = 10                           # 1024 machines
TIME_SHIFT = SEQUENCE_BITS + MACHINE_BITS   # time starts at bit 22
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1     # 4095: twelve 1 bits
MAX_MACHINE = (1 << MACHINE_BITS) - 1       # 1023: ten 1 bits


class SnowflakeGenerator:
    """Time | machine | sequence packed into one integer. O(1) per id."""

    def __init__(self, machine_id, epoch_ms):
        self.machine_id = machine_id    # 0..1023, different on every machine
        self.epoch_ms = epoch_ms        # custom epoch: time 0 for these ids
        self.last_clock = -1            # the latest time a caller passed
        self.last_ms = -1               # the millisecond in the latest id
        self.sequence = 0               # the latest id's number in last_ms

    def next_id(self, now_ms):
        """New millisecond: sequence 0; same one: sequence + 1, borrowing
        the next millisecond after 4096 ids. O(1)."""
        if now_ms < self.last_clock:
            raise ValueError("clock moved backwards")
        self.last_clock = now_ms
        if now_ms > self.last_ms:
            self.last_ms = now_ms       # a new millisecond: restart at 0
            self.sequence = 0
        else:
            self.sequence += 1          # the same millisecond: next number
            if self.sequence > MAX_SEQUENCE:
                self.last_ms += 1       # 4096 ids used: move to the next ms
                self.sequence = 0
        elapsed = self.last_ms - self.epoch_ms
        time_part = elapsed << TIME_SHIFT                   # bits 22..62
        machine_part = self.machine_id << SEQUENCE_BITS     # bits 12..21
        return time_part | machine_part | self.sequence     # bits 0..11


def decode_id(snowflake_id):
    """Shift and mask the three fields back out: [ms since the epoch,
    machine, sequence]. O(1)."""
    sequence = snowflake_id & MAX_SEQUENCE                  # low 12 bits
    machine_id = (snowflake_id >> SEQUENCE_BITS) & MAX_MACHINE
    elapsed = snowflake_id >> TIME_SHIFT                    # the rest
    return [elapsed, machine_id, sequence]


# --- try it ---
EPOCH_MS = 1700000000000            # 2023-11-14 22:13:20 UTC
gen = SnowflakeGenerator(5, EPOCH_MS)
first = gen.next_id(EPOCH_MS + 1000)
second = gen.next_id(EPOCH_MS + 1000)       # same millisecond: sequence 1
third = gen.next_id(EPOCH_MS + 1001)        # new millisecond: sequence 0
print(first, second, third)         # -> 4194324480 4194324481 4198518784
print(decode_id(second), decode_id(third))  # -> [1000, 5, 1] [1001, 5, 0]
burst = SnowflakeGenerator(7, EPOCH_MS)
for i in range(4097):               # one more id than a millisecond holds
    last = burst.next_id(EPOCH_MS + 50)
print(decode_id(last))              # -> [51, 7, 0]
try:
    gen.next_id(EPOCH_MS + 999)     # earlier than the last call
except ValueError as error:
    print(error)                    # -> clock moved backwards
