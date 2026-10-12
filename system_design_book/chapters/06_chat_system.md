---
rank: 6
slug: chat_system
---

A chat system such as WhatsApp carries short messages between phones, one to one and in small groups, and shows the sender what became of each: one tick when the server has it, two when the recipient's phone has it, blue ticks once it is read. Alice's "running late" reaches Bob's phone a moment later, or as soon as it is back online. Three questions decide the design: how a message finds the one server, among more than a thousand, that holds the recipient's connection; how to deliver every message once and in order over networks that keep dropping connections; and what to keep for an offline recipient when the server cannot read a word of it.

### Requirements

A user sends text, photos, videos, voice notes and files to another user or to a group of up to 1,024 members, WhatsApp's own limit. Messages appear in the same order on every phone and never twice. The sender sees sent, delivered and read receipts, and in a group a message counts as delivered or read only once every member has received or read it. An offline recipient gets everything on reconnecting, woken by a push notification. Content is end-to-end encrypted, so the servers handle only ciphertext.

Assume 2 billion users, a billion active each day and 300 million connected at the peak, sending 100 billion messages a day. A message to an online recipient arrives within 500 ms at the 99th percentile, an acknowledged message is never lost, and availability is 99.99%. The server is a relay, not an archive: phones keep the history, and the server deletes each message once every recipient has it, or after 30 days undelivered, as WhatsApp's published policy does. Multi-device sync, presence, typing indicators and search belong to Chapter 7 and calls to Chapter 36; registration, backups and broadcast channels are out of scope.

### Estimates

```text
users        2 B registered, 1 B active a day, 300 M connected at peak
messages     100 B a day / 86,400 s ≈ 1.2 M/s (peak ×2: 2.3 M/s)
recipients   80% one-to-one (1) + 20% to groups of ~10 (9) ≈ 2.6 a message
deliveries   2.3 M/s × 2.6 ≈ 6 M/s at peak, and up to 2 receipts for each
gateways     300 M connections / 250,000 per host ≈ 1,200 hosts (+ spares)
memory       250,000 connections × ~20 KB of TLS and buffers ≈ 5 GB a host
heartbeats   300 M phones × one ping a minute = 5 M pings/s
registry     300 M sessions × ~100 B ≈ 30 GB, in memory
message      ~300 B of ciphertext and envelope × 100 B a day ≈ 30 TB/day
relay        at most 30 days × 30 TB = 900 TB; most rows live for seconds
archive      keeping all history instead: 30 TB × 365 ≈ 11 PB a year
writes       counter + dedup + message + 2.6 inbox ≈ 5.6 × 2.3 M/s ≈ 13 M/s
media        5% of messages × 100 KB ≈ 500 TB/day in, × 2.6 ≈ 1.3 PB/day out
```

The gateway fleet is sized by memory, not traffic: each host holds a quarter of a million mostly idle connections but forwards only about 5,000 deliveries a second, and its 4,000 heartbeats a second must end there. Heartbeats outnumber messages and receipts can outnumber deliveries, which is why acknowledgements are cumulative. The store is sized by its write rate, 13 million writes a second at peak plus one per ack, against under a petabyte of data, the load log-structured wide-column stores are built for. Media is over fifteen times the bytes of the messages, so it bypasses the chat path. Peak is only twice the average because users span every time zone.

### API

```text
GET  wss://chat.example.com/v1/connect      Authorization: Bearer <token>
     101 Switching Protocols, then binary frames      401 bad token

phone → server
  send     {cid, conv, ciphertext}          cid: a random 128-bit id
  ack      {conv, delivered_upto: 4812}     cumulative, like a TCP ack
  read     {conv, read_upto: 4812}
  fetch    {conv, after: 4809}              resend everything after 4809
  group    {conv, add: [user], remove: [user]}      group admins only
server → phone
  sent     {cid, conv, seq: 4813, ts}       the first tick
  msg      {conv, seq: 4813, from, cid, ciphertext}
  receipt  {conv, by: user | all, delivered_upto | read_upto}  ✓✓, blue
ping and pong once a minute keep the connection alive

POST /v1/media        200 {media_id, upload_url}         pre-signed PUT
GET  /v1/keys/{user}  200 {identity_key, signed_prekey, one_time_prekey}
```

After the handshake the phone exchanges small binary frames with no per-message headers or authentication. The cid makes sending idempotent: a phone that loses its connection before it sees `sent` resends with the same cid and gets the original sequence number back, not a second copy. Acks and read marks are watermarks, so one frame covers a burst, and `fetch` fills a hole in the sequence. A `group` frame without a conversation id creates a group. Media never crosses this connection: the phone uploads the encrypted file through a pre-signed URL and sends a message whose ciphertext carries the file's id, key and hash.

### Data Model

```text
messages  (conv, seq) PK | cid | sender | sent_at | ciphertext
          partitioned by hash(conv), sorted by seq; deleted once every
          recipient has it, or after 30 days
convs     conv PK | kind | members | last_seq | fanned_out_upto
dedup     (conv, cid) PK → seq                               TTL one day
inbox     (user, conv) PK | last_seq | delivered_upto | read_upto
          partitioned by hash(user); pending where last_seq > delivered_upto
sessions  user → (gateway, conn_id)          Redis, sharded by hash(user)
keys      user PK | identity_key | signed_prekey | one_time_prekeys
devices   user PK | platform | push_token
blobs     media_id → encrypted file      object store, deleted after 30 d
```

The first four tables live in one wide-column store with single-row atomic operations, such as Bigtable or HBase: the load is millions of small writes a second, every read stays inside one partition and nothing joins. Partitioning messages by conversation keeps each backlog contiguous and sorted, so delivering it is one range scan, and stores a group message once, not once per member. The inbox is partitioned by user because reconnecting asks which of one user's conversations have messages past the watermark; each message bumps one small inbox row per recipient, a fan-out on write as in Chapter 5 but of a number rather than a post. A one-to-one conversation's id is derived from the two user ids, so it needs no setup; a group's id is a Snowflake id (#145), unique without a central counter. Sessions live in Redis because the gateways can rebuild them, keys and push tokens in a replicated key-value store, media in object storage behind a CDN.

### Architecture

```dot
rankdir=TB;
alice    [label="Alice's phone", class=client];
lb       [label="L4 load balancer", class=edge];
api      [label="media and\nkey API"];
gw1      [label="gateway 1"];
keys     [label="key directory", class=store];
blobs    [label="object store", class=store];
chat     [label="chat service\nconversation owners"];
registry [label="session\nregistry", class=cache];
msgs     [label="message store\nby conversation", class=store];
inbox    [label="inbox\nby user", class=store];
push     [label="push worker", class=worker];
gw2      [label="gateway 2"];
cdn      [label="CDN", class=edge];
apns     [label="APNs / FCM", class=external];
bob      [label="Bob's phone", class=client];
alice -> lb [label=" WebSocket"];
lb -> gw1;
gw1 -> chat [label=" send"];
chat -> msgs [label=" 1. append"];
chat -> inbox [label=" 2. bump"];
chat -> registry [label=" 3. where is Bob?"];
chat -> gw2 [label=" 4. deliver"];
gw2 -> bob;
gw1 -> registry [style=dashed, label=" register", constraint=false];
gw2 -> registry [style=dashed, constraint=false];
chat -> push [style=dashed, label=" if offline"];
push -> apns;
apns -> bob [style=dashed, label=" wake"];
alice -> api [label=" upload URL"];
api -> keys [label=" prekeys"];
alice -> blobs [label=" PUT ciphertext"];
blobs -> cdn;
cdn -> bob [label=" GET"];
{rank=same; lb; api}
{rank=same; gw1; keys; blobs}
{rank=same; chat; registry}
{rank=same; msgs; inbox; push; gw2; cdn}
{rank=same; apns; bob}
```

The send path starts at Alice's phone, whose WebSocket runs through an L4 load balancer to gateway 1. Each gateway terminates TLS, records in the session registry which users it holds and forwards their frames to the chat-service instance that owns the conversation, found by consistent hashing (#139) on the conversation id. The owner checks the cid against the dedup table, takes the next sequence number and appends the message to the message store; once that write is durable it answers `sent`, Alice's first tick. Then it bumps each recipient's inbox row, asks the registry where Bob is connected and hands the message to gateway 2, which writes it down Bob's connection.

Bob's phone answers with a cumulative `ack` that returns through gateway 2 to the owner, which advances Bob's watermark and sends Alice her second tick through gateway 1; a `read` frame turns the ticks blue the same way. If the registry has no entry for Bob, or gateway 2 says his connection is gone, the owner hands a job to the push worker, which sends a notification with no readable content through APNs or FCM; Bob's app wakes, connects and receives every conversation whose inbox row shows messages past its watermark.

Media takes its own road: Alice's phone encrypts the photo under a fresh key and PUTs the ciphertext into the object store through a pre-signed URL from the media and key API, and Bob's phone downloads it through the CDN. The same API fronts the key directory, where phones publish the public keys others need to open an encrypted session with them.

### Deep Dives

#### Finding the recipient's connection

A server can only push to a phone that keeps a connection open, since a phone behind a carrier's NAT accepts no incoming connections. Polling inverts the cost: 300 million phones asking every five seconds make 60 million requests a second, nearly all empty, and messages still wait up to five seconds. A persistent connection pushes the moment a message exists. WebSocket is the usual one: it starts as an ordinary HTTPS request on port 443, which gets it through most proxies and firewalls, and becomes a full-duplex stream when the server answers 101.

That makes the gateways stateful, and Bob's connection lives on exactly one of 1,200. Rather than broadcast every message to all of them, each gateway writes `user → (gateway, conn_id)` to the registry on connect and the owner looks recipients up. Entries change only on connect and disconnect, never on the 5 million heartbeats a second. A newer connection overwrites the entry, and a disconnect deletes it only if conn_id still matches, so the late cleanup of an old connection cannot erase a new one. Instead of expiring entries one by one, each gateway renews a lease of its own in the registry every few seconds, and entries naming a gateway whose lease has lapsed count as absent.

The registry is only a hint. A stale entry sends the message to a gateway that answers "not here", the owner falls back to a push, and the message waits in the inbox either way, so the registry can live in memory and be rebuilt by asking the gateways to republish. Gateways also defend against slow readers: each connection's outgoing frames sit in a fixed-size ring buffer (#110), and a phone that stops reading fills it and is disconnected, to resync later from its inbox. A ping every minute catches connections that died without a FIN, which TCP alone would not notice for hours.

#### Ordering, retries and receipts

Timestamps cannot order a conversation. Phone clocks can be minutes wrong, so a reply could sort above the message it answers; server clocks agree only to milliseconds; and no timestamp reveals that something is missing. Order needs one point of decision per conversation, which ownership provides. The owner handles a conversation's messages one at a time, cheap because even a lively group sends at most tens a second, and numbers each from `last_seq` in the conversation row with a conditional write, 4813 only if it is still 4812, so two instances that briefly both believe they own the conversation never give one number to two messages. A crash between taking a number and storing the message leaves a gap, never a reuse.

Retries create duplicates, so delivery is at least once and idempotent at both ends: the owner remembers each cid with its number for a day, and the recipient's phone drops any cid it has already shown, so each message appears exactly once.

Dense numbers buy two more things. The phone acknowledges cumulatively, as TCP does: `delivered_upto: 4812` means "I hold everything through 4812", so a burst of two hundred messages costs one ack. And holes show: a phone holding 4812 that receives 4815 sends `fetch` after 4812, and the owner answers from the message store, marking any number lost to a crash as skipped.

Receipts are the same watermarks. Alice's message 4813 shows two ticks once Bob's delivered_upto reaches 4813 and turns blue once his read_upto does. In a group it shows two ticks when the lowest delivered_upto among the other members reaches 4813, and its info screen lists the members whose read_upto has passed it. The owner keeps these watermarks in memory, so an ack costs a row write and a comparison, and Alice hears only when a minimum moves; once every recipient is past a message, the owner deletes it.

#### The offline inbox, group fan-out and encryption

The obvious offline store is a queue of message copies per recipient, deleted as they are delivered. It fails twice: a message to a full group becomes 1,023 copies, and a queue in a log-structured store leaves a tombstone for every delete that later reads must step over until compaction. The inbox holds no messages, only one row per conversation per user with the latest number and the user's watermarks, so five hundred messages in a busy group cost an offline member one row. Reconnecting reads the user's partition, a few hundred rows, and range-scans each conversation whose last_seq exceeds delivered_upto from the watermark on. A phone with no session gets one push per conversation per burst through APNs or FCM, a pipeline Chapter 20 covers.

Small groups fan out on write: the owner walks the member list, bumps each inbox row and delivers to the members online, having acknowledged the sender as soon as the message was stored. `fanned_out_upto`, written along with the counter, records how far it got, so a new owner can finish the job after a crash, and because membership changes are applied in sequence with messages, who receives message 4813 has an exact answer.

The server's part in encryption is small. Phones run the Signal protocol. To reach Bob for the first time, Alice's phone fetches his identity key and signed prekey, plus a one-time prekey that the key directory never hands out again, and builds a session while Bob is offline; later messages use keys that ratchet forward. In a group, a member's first message hands its sender key to every other member over their pairwise sessions; after that it encrypts each message once and the server fans out that single ciphertext, which is what lets a group message be stored once. When a member leaves, everyone discards their sender keys and starts over. The server sees who talks to whom, when and how much, never what is said.

### Scaling and Bottlenecks

Gateways scale out and are bound by memory; WhatsApp ran more than two million connections on one FreeBSD server in 2012, so a quarter of a million per host leaves room. In front of them, a packet-level load balancer such as Google's Maglev forwards packets without terminating connections and uses consistent hashing so that every balancer sends a connection to the same gateway; a terminating proxy would hold a second socket per phone. The chat service spreads conversations over a consistent-hash ring, so a new instance takes over only a slice, and keeps its active conversations' counters, members and watermarks in an LRU cache (#44).

The first real bottleneck is a burst of fan-out: a 1,024-member family group answering at midnight on New Year's Eve may send fifty messages a second, fifty thousand inbox writes from one owner, which batches them per store node while the senders already have their first ticks. Across regions, phones connect to the nearest one, each conversation is owned in the region of one of its members and every region holds a replica of the registry, so a one-to-one message crosses at most one inter-region link, the minimum any design pays, and a stale replica costs only a push.

### Failure Modes

A crashed gateway drops 250,000 phones at once. They reconnect elsewhere with jittered exponential backoff, the registry ignores the dead gateway once its lease lapses, and anything in flight to those phones is still in their inboxes. Deploys drain a gateway a few connections at a time with WebSocket close code 1001, "going away". The dangerous case is the reconnect storm after a regional outage, a hundred million phones returning together; admission control at the gateways, a rate limiter (#138) on resync and syncing the newest conversations first keep it from becoming a second outage.

If a chat-service instance dies, its conversations move to the next instances on the ring; the new owner reads last_seq and finishes any fan-out past fanned_out_upto, and phones resend unacknowledged messages under their original cids, so nothing is lost or doubled. Losing a registry shard costs pushes, not messages; a failed store node is covered by its replicas; and a slow APNs or FCM only delays wake-ups. A phone that stays off for more than 30 days loses its undelivered messages by design, and the sender's tick never turns double.

### Trade-offs and Alternatives

The connection protocol is the smallest decision. WebSocket crosses most networks and works in browsers; a native app can run its own framing over TCP, as Facebook Messenger did with MQTT in 2011 to save battery; and long polling is the fallback where upgrades are blocked. WhatsApp layers its client connections inside Noise Pipes, from the Noise Protocol Framework, for very fast connection setup and resume.

The relay model is the large decision. Keeping history on the server, the design of Chapter 7, lets new devices download old conversations and the server search them, at 11 petabytes a year and the cost of holding everyone's messages; partitions then need a time bucket in the key, as Discord's do. Per-conversation sequence numbers trade a single owner for gap detection, cumulative acks and receipt watermarks; Snowflake ids need no owner but leave holes invisible. Fan-out on write suits groups capped at 1,024, but a channel with a million followers would turn each post into a million inbox writes, so channels switch to fan-out on read, like the celebrity timelines of Chapter 5.

### What Interviewers Probe

Expect five questions. How does a message find Bob? A session registry maps him to a gateway, and it is only a hint backed by the inbox and a push. How do you keep order? A per-conversation sequence number from the conversation's single owner, guarded by a conditional write, never timestamps. What happens on a retry? The cid makes sends idempotent, and recipients deduplicate by cid too. How do group receipts work? Cumulative watermarks per member, with two ticks once the lowest passes the message. What if Bob is offline for a week? His inbox rows name the conversations with news, a push wakes his phone, and he syncs from his watermarks.

Strong candidates add three points unprompted: heartbeats outnumber messages and must never touch shared state; reconnect storms, not steady traffic, set the capacity plan; and end-to-end encryption makes the server a relay of ciphertext, with Sender Keys the reason a group message is still stored once. Underneath every answer, the interviewer is listening for one property: an acknowledged message survives any single crash.

*Algorithms:* #139 Consistent Hashing · #145 Unique ID Generator · #110 Circular Queue · #44 LRU Cache · #138 Rate Limiter
