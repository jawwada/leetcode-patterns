---
rank: 7
slug: messenger
---

Messenger is chat that follows one person across many devices. A conversation started on the phone continues on the laptop, a message read on the laptop stops the phone from buzzing, a green dot shows who is online, and a search for "passport" finds a message from three years ago. The design builds on the chat core of Chapter 6, and three questions decide it: how each device learns exactly what it missed, how to tell a billion people who is online without drowning in presence traffic, and how to search years of one person's messages in a fraction of a second.

### Requirements

A user is logged in on up to five devices, all showing the same conversations, the same messages in the same order, and the same edits and read state; reading a conversation on one marks it read on all. A newly linked device shows recent conversations within seconds and can scroll back through all of history. Users see whether contacts are online or when they were last active, unless a contact hides it, see who is typing, and can search the full text of their own history. Conversations are one-to-one, groups of up to 250 members, or channels with millions of followers in which only admins post.

Assume 1 billion daily active users with two devices each. A message reaches the recipient's online devices within 500 ms at the 99th percentile, and a device offline for a day catches up in about a second. No device may lose a message, show one twice or order a conversation differently from the user's other devices. Presence may lag by seconds and typing is best effort; neither touches the message store. Search answers within 500 ms and may miss the last few minutes. History is kept until deleted, and sending and syncing are 99.99% available. Unlike in Chapter 6, the servers can read message text, as server-side history and search require. Calls (Chapter 36), stories and payments are out of scope.

### Estimates

```text
devices      1 B daily users × 2 devices = 2 B devices
messages     40 sent/user/day = 40 B/day ≈ 460,000/s (peak ×2: 930,000/s)
log appends  a copy into every member's log, the sender's too: ~3 per message
             120 B/day ≈ 1.4 M appends/s (peak 2.8 M/s)
connections  30% of devices online at peak = 600 M / 250 K each ≈ 2,400 gateways
heartbeats   600 M connections / 30 s = 20 M/s, all absorbed at the gateways
history      120 B copies/day × 250 B = 30 TB/day ≈ 11 PB/year before replicas
sync log     ~150 events/user/day (120 messages + reads, receipts, edits)
             × 30 days × 250 B ≈ 1.1 MB/user ≈ 1.1 PB
presence     1 B × 20 sessions/day × 2 changes = 40 B/day ≈ 460,000 changes/s
             to all 200 friends: 93 M pushes/s; to ~5 watchers: 2.3 M/s
search index 120 copies/day × 15 words × 3 B ≈ 5 KB/user/day ≈ 2 MB/user/year
typing       ~2 events per message ≈ 930,000/s, never stored
```

Four numbers shape the design. Copying each message into every member's log means nearly three million small appends a second at peak, all keyed by user, the workload LSM-based wide-column stores are built for. Twenty million heartbeats a second must stop at the gateways. Pushing every presence change to every friend would cost two hundred times the message rate, so a change goes only to the few devices showing that person. And a year of one user's messages is about 11 MB of history and 2 MB of index, so any search runs over one user's data on one machine.

### API

```text
WSS  /v1/connect?device_id=d7       one per device; the same frames over MQTT
     → sync    {cursor: 1041}
     ← events  {from: 1042, to: 1541, items: [...], more: true}
     → ack     {upto: 1541}
     → send    {cid: "c-88f1", conv: "g42", body: "..."}
     ← sent    {cid: "c-88f1", msg_id: <64-bit id>, conv_seq: 58}
     → read    {conv: "g42", read_upto: 58}
     → typing  {conv: "g42"}                       no ack, never stored
     → watch   {user_ids: [...]}      ← presence {changes: [...]}, batched

GET  /v1/sync?cursor=1041&limit=500             a phone woken for a moment
     200 {events: [...], next: 1541, more: false}
     410 cursor older than the log: rebuild from a snapshot
GET  /v1/threads?limit=50                       snapshot for a new device
     200 {threads: [{conv, last_messages, read_upto}], head: 1541}
GET  /v1/threads/{conv}/messages?before=58&limit=50
     200 {messages: [...]}              403 not a member
GET  /v1/search?q=concert+tickets&limit=20&page=<token>
     200 {hits: [{conv, msg_id, snippet}], next: <token>}
```

Every frame is safe to repeat. A `send` carries a `cid`, so a retry is deduplicated as in Chapter 6 and returns the same `msg_id`; a `sync` names the last log position the device applied, never a time; and a `read` names a position in the conversation, so one frame marks everything up to 58 as read. Where Chapter 6 acks each conversation separately, a device here acks a single number, its position in the log. A phone woken in the background syncs over HTTPS with the same cursor. A cursor older than the log's retention gets 410 Gone, the convention Google's Calendar API uses for an expired sync token, and the device rebuilds from the thread snapshot, whose `head` says where to resume. `typing` and `watch` are fire-and-forget.

### Data Model

```text
user_log  (user_id, seq) PK → type | conv | conv_seq | msg_id | payload
          every event of one user in order; seq gapless; TTL 30 days
messages  (user_id, conv, conv_seq ↓) PK → msg_id | sender | sent_at | body
          the user's own copy, newest first, kept until deleted
threads   (user_id, conv) PK → members | last_seq | read_upto | muted
recent    (user_id, last_active ↓) PK → conv       order of the thread list
devices   (user_id, device_id) PK → acked_seq | push_token | last_sync
profile   user_id PK → last_seen | shows_presence | settings
          all of the above keyed by hash(user_id) first, 3 replicas
channels  ((channel_id, 10-day bucket), conv_seq ↓) PK → msg_id | sender | body
follows   (user_id, channel_id) PK → read_upto | muted
index     (user_id, segment_id) PK → immutable segment, plus deleted msg_ids
presence  user_id → gateways | last_active | watchers         in memory only
```

Every access pattern is a range scan inside one user's keys: the log from a cursor, a conversation newest first, the thread list by recency. Nothing joins, so the store is a wide-column one with strongly consistent single-row operations, such as HBase or Bigtable, with every key led by a hash of the user id so that one user's rows sit together and users spread evenly. Facebook built its Messages system on HBase in 2010, finding Cassandra's eventual consistency hard to reconcile with messaging, and moved Messenger's storage to MyRocks in 2018. Unlike Chapter 6, every member keeps a copy of each message, three on average, so a user's history, deletions and search index live on that user's own rows. Channels are the exception: a post is stored once, keyed by channel and a ten-day bucket, the layout Discord adopted on Cassandra to keep partitions bounded. Presence lives only in memory; only `last_seen` is written down, into `profile`.

### Architecture

```dot
rankdir=TB;
phone   [label="phone\nMQTT", class=client];
laptop  [label="laptop\nWebSocket", class=client];
gw      [label="connection gateways", class=edge];
chat    [label="chat service\n(Chapter 6)", class=service];
pres    [label="presence service\nin memory", class=cache];
search  [label="search service", class=service];
mbox    [label="mailbox service\nper-user log", class=service];
reg     [label="session registry", class=cache];
chan    [label="channel log", class=store];
store   [label="mailbox store\nrows by user", class=store];
apns    [label="APNs / FCM", class=external];
cdc     [label="mailbox changes", class=queue];
indexer [label="indexer", class=worker];
index   [label="search index\nper-user segments", class=store];
phone -> gw;
laptop -> gw;
gw -> chat [label=" send, typing", dir=both];
gw -> mbox [label=" sync / events", dir=both];
gw -> pres [label=" presence", dir=both, style=dashed];
gw -> search [label=" query"];
chat -> mbox [label=" append per member"];
chat -> chan [label=" channel posts"];
chat -> reg [label=" typing", style=dashed];
mbox -> store [label=" conditional put"];
mbox -> reg [label=" devices?"];
mbox -> apns [label=" offline"];
store -> cdc [style=dashed];
cdc -> indexer [style=dashed];
indexer -> index;
search -> index;
search -> store [label=" fetch hits"];
pres -> store [label=" last seen", style=dashed];
{rank=same; phone; laptop}
{rank=same; cdc; indexer; index}
```

The write path starts on Alice's phone, whose MQTT connection ends at one of the connection gateways; browsers use WebSocket. The gateway hands the message to the chat service of Chapter 6, which checks membership, drops a retried `cid`, stamps a 64-bit time-ordered id (#145) and the conversation's next sequence number, and asks the mailbox service to append the message to every member's log, Alice's included. The mailbox service, partitioned by user id, writes each event at the next position of that user's log with a conditional put into the mailbox store, and `sent` goes back once every append is durable. It then pushes the event to each member's devices, found in the session registry, through their gateways, or asks APNs or FCM to notify a member with none connected, so Alice's laptop receives her message exactly as Bob's phone does.

A connecting device sends its cursor, and the mailbox service streams the missing events and then keeps the connection live; acked positions, kept in `devices`, drive delivered receipts. Gateways report connects, disconnects and watch lists to the presence service and receive batched changes back, and the presence service writes only `last_seen` to the store. Typing goes from the gateway to the chat service, which finds the members' devices in the session registry and hands the event back to their gateways. Off the hot path, the mailbox changes stream feeds the indexer, which writes the search index; the search service answers queries arriving through the gateways from that index and fetches the hits from the mailbox store. A post to a channel is written once, to the channel log.

### Deep Dives

#### One log per user, one cursor per device

Giving each device its own queue makes every message a write per device, starts a new device empty, and lets one missed copy of an edit or a read marker leave a device permanently out of step. Syncing by time fails more quietly: a device that asks for everything since 18:42:07.120 misses an event stamped 18:42:07.118 by a server whose clock runs slightly behind, and never learns that it did. Asking each conversation what changed costs four hundred mostly empty queries on every reconnect for a busy user.

Instead each user has one totally ordered log of everything that changes their view: messages, edits, reactions, receipts, read markers and membership changes, each at the next integer position. A device keeps one cursor, the last position it applied, saved in the same local transaction as the events so that a crash never leaves it ahead of the data, and catching up is one range read from the cursor to the head. Facebook rebuilt Messenger's sync this way in 2014: its Iris service was a totally ordered queue of messaging updates with a pointer for each device and one for the storage tier.

```text
alice's log  1040    1041    1042    1043    1044    1045        head = 1045
             msg g42 read c9 msg c9  edit    receipt msg g42
phone        cursor 1045    live, nothing to fetch
laptop       cursor 1041    sync(1041) → 1042..1045, then live
tablet       cursor 612     already expired → 410, snapshot, resume at head
```

Positions are gapless because each log has one writer, the mailbox shard that owns the user, which appends in order with a conditional put that succeeds only if the position is free. A shard that takes over a user continues from the highest written position, and the conditional put stops a deposed owner from writing the same position twice. A device at 1043 that is pushed event 1045 knows that 1044 is missing and fetches it: a push is a hint, and the log is the truth.

Read state is one more event. The thread row's `read_upto` only moves forward, to the larger of its value and the reported one, so a slow laptop reporting 55 after the phone reported 58 changes nothing. A read event in the reader's own log makes the laptop clear its badge and the phone withdraw its notification, and a receipt goes to the other members. Delivered receipts come from acks: when any of Bob's devices first acks a position at or past Alice's message, her log gains a delivered event. A new device, or one whose cursor has expired, records the head, loads the snapshot and syncs from that head; events it sees twice are harmless, because each is keyed by message id and version. The cost is one append per member for every message.

#### Presence and typing without a storm

When Facebook launched Chat in 2008, its engineers wrote that the most resource-intensive operation in a chat system is not sending messages but keeping each online user aware of the online, idle and offline states of their friends. The naive cost grows with friend-list size times peak users times churn, which here is 93 million pushes a second, and mobile makes it worse, because a phone drops its connection in every lift.

The fix has four parts. First, liveness stays at the edge. The device heartbeats every 30 seconds, MQTT's keep-alive ping, since TCP alone may not notice a vanished phone for hours. The gateway files each connection under its deadline, a minute after the last heartbeat, in a ring of one-second buckets, the ring of the hit counter (#45) holding connection ids instead of counts, and each second it sweeps one bucket and closes the connections still due. The gateway reports only transitions, a user's first device connected or last one gone, and renews one lease for all of its connections, so a gateway that dies silently takes its users offline when the lease lapses.

Second, going offline is debounced: when a user's last connection closes, the entry gets a 30-second TTL (#94), a reconnection cancels it without publishing anything, and only expiry publishes offline, with `last_seen`. Third, changes go only to watchers: a device sends the list of users it is displaying, and the presence service, sharded by user id with consistent hashing (#139), pushes each change, unless the user hides presence, to about five watching devices instead of two hundred friends. Fourth, changes are batched per destination gateway and flushed once a second, keeping only a user's latest state, so the number of messages a second is bounded by shards times gateways, whatever the churn. A user with a huge audience is never pushed; viewers fetch the status when they open the conversation.

Typing indicators are more ephemeral still: sent at most every three seconds while the user types, forwarded by the chat service to connected devices only, never stored, retried or pushed, and shown for six seconds unless refreshed, so a lost "stopped typing" cannot leave one stuck. Groups above fifty members send none. The price of the whole scheme is honesty measured in seconds: a phone that dies in a tunnel looks online for up to 90 seconds.

#### Searching years of one person's messages

Scanning fails first. A user's history grows by about 11 MB a year, so a search over five years reads 55 MB, and gigabytes for a heavy user, on every keystroke of search-as-you-type. One global index, the web-search design of Chapter 22, fails the other way. Partitioned by term, the postings for "ok" span hundreds of billions of messages and each query filters them down to one person; partitioned by document, every query visits every shard.

The index is therefore partitioned the way the queries are: one inverted index per user (#150), keyed by user id, so a query reaches one shard. Every few minutes the indexer turns the mailbox changes into a small immutable segment for each active user, a sorted dictionary of terms with each term's message ids. Message ids are time-ordered and postings run newest first, so the two-pointer intersection of "concert" and "tickets" yields the latest matches first and stops at twenty. A query merges each term's postings across the user's few segments with the heap of #20, and compaction merges small segments into larger ones with the same k-way merge, as Lucene does. The word still being typed matches as a prefix by binary search in each dictionary, and Chinese and Japanese text is indexed as overlapping character bigrams, as Lucene's CJK analyzer does.

A deletion adds the message id to the user's list of deleted ids, which queries subtract and compaction purges, and hits are fetched from the mailbox store before they are shown, so a deleted message never resurfaces. The cost is about 2 MB of index per user per year, 2 PB a year in all. The newest minutes are not yet in any segment, so the client also searches its local database and merges those matches in.

### Scaling and Bottlenecks

The mailbox store comes first. Its 2.8 million appends a second at peak are small writes that an LSM tree turns into sequential flushes, and storage, 33 PB a year with replicas, sizes the cluster long before the write rate does. Large groups come next, because the per-user log is fan-out on write: a 250-member group costs 250 appends per message, and a channel with a million followers would cost a million. Channels therefore use fan-out on read, the celebrity hybrid of Chapter 5: one copy in the channel log, a cursor per channel on each device, each live post sent once to every gateway with a follower online as in Chapter 32, one `read_upto` per follower, read receipts shown as counts, and no presence or typing. The chat service caches a hot channel's last page and coalesces concurrent reads of it into one, as Discord's data services do.

Restarting a gateway reconnects a quarter of a million devices, so clients reconnect with jittered backoff, and because each device resumes from its cursor, a reconnect costs one range read. Presence needs about 300 GB of memory, a billion 100-byte entries plus 600 million devices watching 20 users each at 16 bytes a watch. History grows by 11 PB a year, so old history moves to cheaper disks and loads when a user scrolls back.

### Failure Modes

A crashed gateway loses nothing: undelivered events live in the log, its devices reconnect elsewhere and sync from their cursors, and when its lease lapses only the users who fail to reconnect within the TTL appear offline. A failed mailbox shard's users move to another node, which resumes from each log's highest position. A send that was never acknowledged is retried with the same `cid`, and the mailbox service remembers each user's recent message ids, so a repeated append is dropped. A lost presence shard is rebuilt within seconds from the gateways, which report their connected users again, and from watch renewals. An APNs or FCM outage or an indexer backlog only delays notifications or search; the messages wait in the log.

The log is replicated synchronously across three zones of each user's home region and asynchronously to a second region. Promoting that region could lose the last seconds of appends and hand out positions that devices have already seen, so promotion starts a new log epoch and the affected users' devices rebuild from a snapshot, the same path a device offline past the 30-day retention takes on its own.

### Trade-offs and Alternatives

The central choice is a log per user against storage per conversation. Chapter 6's single copy per conversation is cheaper to write and store, but its inbox keeps one watermark per user and conversation; with five devices it would need one per device and conversation, and a returning device would scan them all to learn what changed. The per-user log pays three appends and three copies per message and buys one cursor per device and one range read per sync. Cassandra would keep accepting writes through replica failures, but the gapless conditional put would need its Paxos-based lightweight transactions, several round trips for every append.

Building an index lazily, on a user's first search, saves much of the 2 PB a year if most users rarely search, at the cost of a slow first query. End-to-end encryption changes the most. Each device has its own keys and the sender encrypts one copy per device, which WhatsApp calls client-fanout. A new device gets its history from an existing device, as on WhatsApp, or from encrypted server storage that only the user's devices can open, the Labyrinth protocol Messenger built when it began making encryption the default for personal chats in December 2023. Search can then run only on the device.

### What Interviewers Probe

Expect six questions. How does a device know it has everything? Positions are gapless, so a cursor and one range read are complete, and a push that skips a number triggers a fetch. Why not sync by timestamp? Skewed clocks and late commits slip behind a device's watermark unnoticed. How do read state and badges agree across devices? A forward-only `read_upto` and a read event in the user's own log. How does presence scale? Heartbeats end at the gateways, offline is debounced with a TTL, and changes go only to watchers, in batches. How does search work? An inverted index per user, because every query concerns one user. What changes for a channel with a million followers? Fan-out on read: one stored copy, a cursor per channel, receipts as counts, and no presence or typing.

Strong candidates raise three points unprompted: the line between durable state (the log and history) and soft state (presence and typing, rebuilt from connections and never stored); the snapshot path for new devices and for those offline past the retention; and end-to-end encryption, which moves history and search onto the devices. Interviewers care less about the brand of wide-column store than about whether you can explain, position by position, how a laptop that slept all weekend catches up without missing or repeating a message.

*Algorithms:* #150 Inverted Index · #145 Unique ID Generator · #45 Design Hit Counter · #94 Cache with Expiring Keys · #139 Consistent Hashing · #20 Merge K Sorted Arrays
