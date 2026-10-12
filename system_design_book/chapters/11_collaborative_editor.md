---
rank: 11
slug: collaborative_editor
---

A collaborative editor lets several people work in one document at once and see each other's keystrokes a moment after they are typed. In Google Docs, Alice rewrites a sentence while Bob types a paragraph under it and Carol's coloured cursor moves through the table below; nobody presses save, nobody waits for a lock, and all three end with the same text. The text itself is small; the hard part is that each editor applies its own keystrokes at once and everyone else's a little later, in a different order on every screen. Three questions decide the design: how concurrent edits merge so that every copy converges and keeps each person's intent, where a document's live state lives so that one place orders its edits, and how the edit stream is stored so that loading, history and offline catch-up all come from one log.

### Requirements

Users create documents and share them with editors, commenters or viewers. Everyone in a document edits rich text at once and sees the others' edits as they type, with their coloured cursors and a list of who is present. Every change is kept: users browse the revision history, see who wrote what, name a version and restore any earlier one. Comments stay attached to their passage as the text around it changes, and editing continues offline and merges on reconnect.

A user's own keystroke must appear instantly, and a collaborator's edit must reach everyone else within 200 ms at the 99th percentile on the same continent. All copies must converge on identical text once the typing stops, and an acknowledged edit must never be lost. Assume 100 M daily users, 10 M clients connected at peak, documents of up to a million characters and at most 100 people in one document, close to the limits Google publishes for Docs. A server failure may pause editing for seconds but must never lose or fork a document. Spreadsheets, slides, suggestion mode, spelling, export and search are out of scope.

### Estimates

```text
connections  10 M clients at peak / 50 k WebSockets per gateway = 200 gateways
sessions     10 M clients / 1.4 per open document ≈ 7 M live documents
edits        10 M × 1 in 10 typing × 3 ops/s = 3 M ops/s peak, 1 M/s average
fan-out      each op goes to ~2 other clients → 6 M messages/s out
one room     100 editors × 5 ops/s = 500 ops/s in, × 99 peers ≈ 50 k msgs/s
session tier 3 M ops/s / 10 k ops/s per server ≈ 300 session servers
live state   7 M docs × (50 KB text + 1,000 recent ops × 100 B) ≈ 1 TB RAM
op log       1 M ops/s × 86,400 s × 100 B ≈ 8.6 TB/day raw ≈ 3 PB/year
snapshots    5 B docs × 50 KB ≈ 250 TB latest, + 4.3 TB/day at 1 per 1,000 ops
```

One document's traffic is tiny: even a full room typing flat out sends 500 operations a second, which one server orders and broadcasts with ease. The total is large but splits perfectly by document, so each live document gets one owner among a few hundred session servers. Ten million mostly idle WebSockets are a separate dimension with a tier of their own. The op log and its snapshots fill the disks, which is why old history is compacted. And every open document's live state fits in a terabyte of memory across the fleet, so the hot path writes to storage but never reads from it.

### API

```text
POST /v1/docs                               {"title": "Q3 plan"}
     201 {"doc_id": "d7Kp2", "rev": 0}
GET  /v1/docs/{doc_id}?rev=4812             no rev: the head
     200 {"rev": 4812, "content": {...}, "role": "editor"}
     403 no access        404 unknown document
GET  /v1/docs/{doc_id}/versions?before=4812&limit=50
     200 {"versions": [{"rev": 4790, "authors": ["u9"]}], "next": "4790"}
POST /v1/docs/{doc_id}/restore              {"rev": 3100}
     200 {"rev": 4813}                      a restore adds a revision
PUT  /v1/docs/{doc_id}/acl/{user_id}        {"role": "commenter"}

GET  /v1/docs/{doc_id}/live?rev=4812        Upgrade: websocket → 101
  →  {"t": "op", "client": "c42", "seq": 17, "base": 4812,
      "op": {"ins": 120, "text": "x"}}
  ←  {"t": "ack", "seq": 17, "rev": 4813}
  ←  {"t": "op", "rev": 4814, "author": "u9", "op": {"del": 300, "len": 4}}
  →  {"t": "comment", "base": 4814, "range": [120, 134], "text": "source?"}
  ↔  {"t": "cursor", "user": "u3", "rev": 4814, "pos": 121}
  ←  {"t": "presence", "here": ["u3", "u9"]}
```

The live channel is a WebSocket because both directions carry a steady stream of small messages; everything else is plain HTTPS. Each operation names its base, the revision it was typed against, which tells the session server what to transform it against, plus the client's id and a sequence number. That pair makes resending safe: the server remembers the last sequence number it committed for each client and answers a duplicate with the original acknowledgement. Revisions are consecutive, so a client that receives 4816 after 4814 asks for the one it missed. The upgrade carries the user's cookie or OAuth token, and the role is checked on every message: a viewer's operations are refused, and a commenter may add comment anchors but no text.

### Data Model

```text
docs       doc_id PK | owner_id | title | head_rev | owner_epoch | region
acl        (doc_id, user_id) PK | role: owner, editor, commenter, viewer
op_log     (doc_id, rev) PK | author | client_id | client_seq | at | op
           a document's rows contiguous and sorted by rev; split by doc_id
snapshots  (doc_id, rev) PK | text, style runs, anchor marks, or a blob ref
versions   (doc_id, rev) PK | authors | started_at | name      history list
comments   (doc_id, comment_id) PK | anchor_id | author | thread | resolved
sessions   doc_id → session server, lease expiry        coordination store
presence   doc_id → {user → cursor, selection, colour}          memory only
```

The op log is the source of truth, and its access patterns, an append at the head and an in-order scan of one document's revisions, choose the store: one with sorted keys and transactions, such as Spanner, keeping each document's rows together and spreading documents by doc_id. Every append is a compare-and-set that succeeds only if head_rev and owner_epoch still hold the values the writer expects, so no revision number is ever issued twice and a former owner can never write again. Snapshots share the key, so the newest one at or before revision r is a single reverse seek. ACLs sit in a strongly consistent database, because a revoked permission must bite at once. A comment's thread has its own table, but its anchor lives inside the document as two zero-width marks that move with the text through the same transformation as every character. Session ownership lives in a coordination store such as etcd or ZooKeeper, and presence is never written down: a cursor from ten seconds ago is worthless.

### Architecture

```dot
rankdir=TB;
alice  [label="Alice's editor", class=client];
bob    [label="Bob's editor", class=client];
api    [label="docs API", class=service];
gw     [label="WebSocket\ngateway", class=edge];
dir    [label="session directory\ndoc → lease", class=store];
sess   [label="session server\nOT, presence", class=service];
meta   [label="docs, ACLs,\ncomments", class=store];
snaps  [label="snapshots,\nversions", class=store];
oplog  [label="op log\n(doc_id, rev)", class=store];
snapw  [label="snapshot worker\nevery 1,000 revs", class=worker];
feed   [label="change stream", class=queue];
alice -> api [label=" open, history"];
alice -> gw [label=" ops, cursors", dir=both];
bob -> gw [dir=both];
gw -> dir [label=" 1. owner?"];
gw -> sess [label=" 2. forward", dir=both];
sess -> oplog [label=" 3. append\n if head = N"];
sess -> meta [label=" roles,\n comments"];
sess -> snaps [label=" load"];
api -> meta [label=" check role"];
api -> snaps [label=" snapshot"];
api -> oplog [label=" ops after it"];
api -> sess [label=" ACL change", style=dashed];
oplog -> feed [style=dashed, label=" committed ops"];
snapw -> feed [style=dashed, dir=back];
snapw -> snaps [constraint=false];
{rank=same; alice; bob}
{rank=same; api; gw}
{rank=same; sess; dir}
{rank=same; meta; snaps; oplog}
{rank=same; snapw; feed}
alice -> bob [style=invis];
api -> gw [style=invis];
sess -> dir [style=invis];
meta -> snaps -> oplog [style=invis];
```

Opening a document starts at the docs API, which checks Alice's role, reads the newest snapshot and the operations after it from the op log, and returns the document at its head, revision 4812. Her editor then opens a WebSocket to a gateway, a tier like Chapter 6's, which authenticates it and asks the session directory who owns the document. If nobody does, the directory picks a session server by consistent hashing over the live servers (#139) and grants it a lease. That server loads the snapshot and tail and holds the text as a rope, a balanced tree of chunks, because edits land in many places at once; a single-user editor gets away with the gap buffer of #144, which is cheap only while edits stay at one cursor.

Alice types an x. Her editor shows it at once and sends it with base 4812. The session server transforms it against anything committed since, appends it to the op log as revision 4813 with the compare-and-set, and only then acknowledges it to Alice and broadcasts it through the gateways to Bob, whose editor transforms it against his own unacknowledged edits and applies it. Presence uses the same connections but skips the log: the session server keeps cursors in memory and rebroadcasts them, at most ten a second per user and coalesced to the latest position. When a WebSocket closes or its heartbeats stop, the gateway tells the session server, which removes that cursor.

Off the hot path, committed operations flow from the op log into a change stream, and the snapshot worker writes a snapshot of each document every 1,000 revisions and groups operations by author and pause into the versions the history shows. The session server reads joining users' roles from the docs, ACLs and comments store and writes comment threads there; when an owner changes a permission, the docs API tells the live session server, which refuses the downgraded user's next edit.

### Deep Dives

#### Merging concurrent edits with operational transformation

The naive design sends each edit as a position and some text and applies it everywhere as it arrives. But a position is relative to the text its sender saw, which may have changed by the time the edit lands. In the figure, two concurrent inserts leave Alice and Bob with different texts that never heal. Locking paragraphs would make people wait on each other across an ocean, and last-writer-wins would silently drop keystrokes.

```text
rev 7, both see   "ABC"
Alice             ins(1, "x") → "AxBC"     reaches the server first: rev 8
Bob, meanwhile    ins(2, "y") → "AByC"     typed against rev 7
no transform      Alice applies ins(2, "y") → "AxyBC"
                  Bob applies   ins(1, "x") → "AxByC"          ✗ diverged
server            rev 8 inserted 1 char before position 2, so
                  T(ins(2, "y"), ins(1, "x")) = ins(3, "y") → rev 9
                  Alice applies ins(3, "y") → "AxByC"
Bob's editor      T(ins(1, "x"), ins(2, "y")) = ins(1, "x"): y lies after it
                  Bob applies   ins(1, "x") → "AxByC"          ✓ converged
rule              T(ins(p, s), ins(q, t)) = ins(p + len(t), s) if q < p,
                  or if q = p and t was ordered first; else ins(p, s)
```

Operational transformation fixes the positions instead of the order. T(a, b) rewrites operation a so that, applied after b, it still does what its author meant: an insert after another insert moves right by that insert's length, one before it stays put, positions after a delete move left, and overlapping deletes shrink to what is left. A tie at one position needs a rule both sides apply identically, here that the operation the server ordered first goes first. Cursors are positions too, so editors pass remote cursors through the same function.

Peer to peer, transformation alone breaks down: concurrent operations meet in different orders at different sites, and the functions must also satisfy TP2, which says that transforming an operation along two paths through the same concurrent edits gives the same result. Such functions are notoriously hard to get right, and several published ones were later shown to violate it. A central server sidesteps TP2 by imposing one order. This is the client-server design of the Jupiter system from Xerox PARC, which Google Wave built on, and Google Docs too sends every change through its servers. Wave adds a rule this design keeps: a client has at most one operation in flight and composes everything typed meanwhile into one pending operation, sent when the acknowledgement arrives. The server then keeps one linear history rather than one per client.

The costs are real: every pair of operation types needs its own transformation, so a rich-text model with styles, lists, tables and anchors grows its transformation code with the square of the type count, and that is where the bugs hide. An operation typed against an old revision must be transformed against everything since, cheap half a second behind and expensive after a day offline. And every edit needs the document's one server.

#### CRDTs: unique position ids instead of a central order

A conflict-free replicated data type, or CRDT, takes the opposite route: it makes concurrent edits commute, so replicas can apply them in any order and still converge. For text, the trick is to stop naming characters by offset, which shifts with every edit before them, and give each one a unique, immutable position id. In Logoot-style CRDTs the ids come from a dense ordered space: replicas keep characters sorted by id, an insert invents an id between its neighbours', and a delete names the id it removes. RGA, and YATA behind the Yjs library, instead have each character record the one it was typed next to, leave tombstones for deletions, and order concurrent inserts at one spot by id.

```text
ids, kept sorted    A 0.2         B 0.4         C 0.6
Alice: x after A    x gets (0.3, alice), between 0.2 and 0.4
Bob:   y after B    y gets (0.5, bob), between 0.4 and 0.6
any arrival order   sort by id: A 0.2, x 0.3, B 0.4, y 0.5, C 0.6 → "AxByC"
same gap twice      (0.3, alice) < (0.3, bob): the site id breaks the tie
no room left        between 0.3 and 0.31 lies 0.305: ids are digit lists
delete y            remove id (0.5, bob) on every replica, whatever the order
```

The price is metadata. Every character carries an id several times its own size; tombstones can be dropped only after every replica has seen the deletion, which one laptop in a drawer can delay for months; and dense ids lengthen as people keep typing at one spot. Logoot and LSEQ can also interleave two words typed concurrently at the same place. Yjs merges a run of characters typed in sequence into one item, which cuts the overhead sharply, but the document stays bigger than plain text plus a window of recent operations.

A CRDT wins wherever no server can sit in the middle and transform the edits: an offline-first app that edits for a week and merges by exchanging the operations each side lacks, peers collaborating directly, or an end-to-end encrypted editor whose server relays ciphertext it cannot read, let alone transform. Google Docs' clients are nearly always online and every edit already passes through a server, so the order comes free and OT's smaller, simpler document wins, at the price of a weaker offline story.

#### Snapshots, the operation log and revision history

The naive store overwrites the document on every change: 3 M operations a second against 50 KB documents is 150 GB of writes a second to save a few bytes each, with no history. The opposite extreme keeps only operations, perfect history and terrible loading, since a document edited for five years would replay millions of them on every open. Google described the Docs of 2010 as storing each document as a revision log of three kinds of change: inserting text, deleting text and applying a style to a range. This design keeps that log as the source of truth and treats snapshots as a cache of it.

```text
snapshots of d7Kp2   0     1000     2000     3000     4000         head 4812
show rev 3417        newest snapshot ≤ 3417 is 3000 (binary search)
                     then replay ops 3001…3417 from the op log
restore rev 3417     diff(text at 4812 → text at 3417), committed as 4813
```

With a snapshot every 1,000 revisions, an open costs one snapshot plus about a thousand small operations at most. Showing revision r is the same lookup: binary-search the snapshot revisions for the newest one at or before r, exactly as in Snapshot Array (#47), and replay the operations after it up to r. A restore never rewrites history: the server diffs the head against the old text and commits the difference as a new revision, which can itself be undone, and a named version is a label on a revision.

Offline editing is the same machinery over a longer gap. The editor keeps its unacknowledged operations and their base in local storage such as IndexedDB and, on reconnect, composes them into one. Transforming n pending operations one by one against m missed ones costs n × m steps; transforming the composed operation against the composition of the missed ones takes a single pass. If the base predates the raw history still in the log, the editor offers its offline text as a separate copy, like the conflicted copies of Chapter 10, rather than guess; this is where a CRDT does better.

History is where the storage goes. After 30 days the worker composes each run of consecutive operations by one author into a single operation per few minutes, about twenty times fewer rows, and thins snapshots to one per 20,000 revisions, so log and snapshots grow by about 240 TB a year instead of almost 5 PB.

### Scaling and Bottlenecks

Every tier scales out because documents are independent. A new session server takes only the documents consistent hashing hands it, each pausing for the second its new owner needs to load it. Gateways scale with connections and the op log with doc_id partitions. The session server batches appends: while one write for a document is in flight, arriving operations are transformed and queued, then committed together as consecutive revisions. Without this group commit a document could never beat one operation per write latency, 200 a second at 5 ms, below the 500 of a full room.

The first real bottleneck is a crowded document, whose owner is one server by design. A full room means 50,000 messages a second out, so the session server sends each operation once per gateway and lets the gateway copy it to its connections. Google Docs itself supports up to 100 people working in a file at once, lets only the owner and some editors edit beyond that, and suggests publishing to the web for bigger audiences. Presence comes next, since cursor updates can match operations in volume; they are throttled, coalesced and dropped first under load, because a stale cursor fixes itself and a dropped operation never would.

Across regions, each session lives where most of its editors are. A user on another continent reaches it through a nearby gateway, so their own typing stays instant and only acknowledgements and others' edits cross the ocean; when the crowd moves from London to Sydney, the session follows by the same lease handover as a failover.

### Failure Modes

When a session server dies, its leases expire within seconds and the session directory gives its documents to other servers, which rebuild each from its snapshot and the op log. Nothing acknowledged is lost, because acknowledgement follows the commit. The WebSockets end at the gateways and stay up; the gateways route to the new owners, and each editor resends its in-flight operation, which the new owner either finds in the log, if only the acknowledgement was lost, or applies. Users see a short pause, never a lost edit.

The dangerous case is a server that is slow rather than dead: its lease expires, a new owner takes over, and for a moment two servers think they own the document. The new owner's first act is to bump owner_epoch, the fencing token of Chapter 39, and since every append checks the epoch as well as head_rev, the old owner's next write fails, which tells it to drop the document. A lease alone cannot promise this, since a paused process can wake up still believing it holds one.

After a gateway crash, editors reconnect elsewhere with exponential backoff and jitter, so that clients do not all return at once, and resume from their last revision with pending operations intact. If the op log is unavailable, the session server stops acknowledging while editors keep typing and show the document as saving. A lagging snapshot worker makes opens slower, never wrong. The quiet failure is a bug that lets one client's text drift, so the session server periodically sends a checksum of the document at a revision, and an editor whose own checksum differs reloads.

### Trade-offs and Alternatives

The central trade is OT against a CRDT, and the product decides it: OT for a server-centred editor whose users are nearly always online, where the live document is plain text and history a clean sequence of revisions, and a CRDT for an offline-first, peer-to-peer or end-to-end encrypted editor, paid for in metadata. Figma shows where character-level merging is not worth it: its server is the authority and merges objects property by property with last-writer-wins, so one client turning a text value B into AB while another turns it into BC ends with AB or BC, never ABC. That suits a canvas of shapes and would fail a document.

One owner per document keeps ordering simple but ties every edit to one server and region; letting any region accept edits needs a CRDT or an op log committed through multi-region consensus, which adds a cross-region round trip to every acknowledgement.

### What Interviewers Probe

The conversation starts with the merge. Walk me through two people typing at the same spot: show the insert/insert transform and the tie rule, and say who orders the operations. Why a central server? One order means clients transform only against the server's history, so TP2 never arises. OT or CRDT? OT for an online, server-centred product, a CRDT for offline-first, peer-to-peer or encrypted ones, with the metadata cost named. What if the document's server dies? Acknowledged edits are in the log, a new owner rebuilds from snapshot and tail, clients resend with their sequence numbers, and the compare-and-set stops a slow old owner from forking the document. How does undo work? It undoes only your own edits: each operation pushes its inverse, a delete recording the text it removed just as the undo log of #50 records before-values, and undo transforms that inverse past every later operation and submits it as a new edit, so Bob's later sentence survives Alice's undo. Last Tuesday's version? The nearest snapshot at or before it, plus a replay.

Strong candidates raise four points unprompted: group commit, without which a full room outruns the log; permissions checked on every operation; comment anchors stored inside the text; and checksums that catch a drifting client before its user does. Interviewers care less about which algorithm you name than about whether you can show that every replica ends with the same text.

*Algorithms:* #47 Snapshot Array · #50 Key-Value Store with Transactions · #144 Design a Text Editor · #139 Consistent Hashing
