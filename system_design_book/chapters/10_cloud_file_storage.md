---
rank: 10
slug: cloud_file_storage
---

A cloud file store keeps a folder identical on every device its owner uses and on the devices of everyone it is shared with. Save a file on a laptop and seconds later it is on the phone and on a colleague's desktop; insert one line near the top of a 1 GB CSV and only a megabyte or two should cross the network. Three questions decide the design: how to cut files so that an edit moves only the bytes it changed, how every device learns what changed without polling, and what happens when two devices change the same file while apart.

### Requirements

A user uploads and downloads files of up to 50 GB, organises them in folders and runs a client on each device that keeps a chosen folder in sync, offline edits included. Every change creates a version, and any version from the last 30 days, deleted files included, can be restored. Folders can be shared with other users as viewers or editors, and files or folders through links that can expire.

Durability comes first: eleven nines for stored bytes, and no acknowledged commit ever rolled back. Assume 500 million accounts, 100 million active daily with about three devices each. A change should reach the user's other online devices within seconds plus transfer time, and an edit to a large file should upload roughly the bytes it changed. Metadata is strongly consistent within a folder tree: no device sees a file whose chunks are missing, and concurrent commits to one file are ordered, never silently merged. Sync stays available 99.99% of the time; a commit may wait out a failover of a few seconds. Co-editing (Chapter 11), search, previews and the block store's internals (Chapter 33) are out of scope.

### Estimates

```text
users        500 M accounts, 100 M daily active, ~3 devices each
stored       500 M × 10 GB = 5 EB logical; 2,000 files each → 10^12 files
unique       assume dedup saves 30% → 3.5 EB of distinct chunks
raw disk     3.5 EB × 1.5 (6 + 3 erasure code) ≈ 5 EB; 3 copies, no dedup: 15 EB
uploads      100 M × 30 MB of new chunks a day = 3 PB/day ≈ 35 GB/s
             peak ×3 ≈ 100 GB/s ≈ 0.8 Tbps; growth ≈ 1.1 EB a year
downloads    other devices and collaborators ≈ 2 × uploads ≈ 70 GB/s
commits      100 M × 20 changes a day = 2 B/day ≈ 23,000/s (peak ×3: 70,000/s)
chunk puts   3 PB/day / 1 MB average chunk = 3 B/day ≈ 35,000/s
metadata     10^12 files × 500 B (tree row + current version) ≈ 500 TB
             + 5 × 10^12 owned-chunk rows × 40 B ≈ 200 TB
             ≈ 0.7 PB → ~350 shards of 2 TB, each with 3 replicas
block index  3.5 × 10^12 chunks × 64 B ≈ 220 TB, keyed by hash
collisions   n = 3.5 × 10^12 SHA-256 names: n² / 2^257 ≈ 5 × 10^-53
connections  ~100 M desktop clients online / 100,000 per server ≈ 1,000
idle polls   100 M / 90 s long-poll timeout ≈ 1.1 M empty requests/s
fan-out      70,000 commits/s × ~3 other devices ≈ 210,000 hints/s
```

The numbers split the system in two. The chunks are exabytes of immutable bytes, written once and read often, which belong in a cheap erasure-coded blob store; dedup and erasure coding together cut 15 EB of naive storage to about 5 EB. The metadata is under a petabyte of small rows that each commit updates in a transaction, so it needs a sharded database sized by bytes, not load: 280,000 commits and change reads a second over 350 shards are under a thousand per shard. And a hundred million idle connections are a fleet of their own.

### API

```text
POST /v2/files/commit                          Idempotency-Key: <uuid>
     {"ns": 42, "file_id": "f81…", "base_rev": 6, "parent_id": "d17…",
      "name": "q3.csv", "size": 1073741824, "blocklist": ["9f2c…", …]}
     200 {"rev": 7, "seq": 1047}
     422 {"need": ["a71e…", "0b3d…"]}     upload these chunks, commit again
     409 {"latest_rev": 8}                 another device committed first
PUT  /v2/blocks/{sha256}?ns=42            body: the chunk, compressed
     201 stored (same reply if the bytes already existed)   400 hash mismatch
GET  /v2/blocks/{sha256}?ns=42            200 bytes    403 no read access
POST /v2/changes   {"cursor": "<opaque: ns 42 at 1046, ns 77 at 310>"}
     200 {"entries": [{"file_id": "f81…", "rev": 7, "op": "edit", …}],
          "cursor": "…", "has_more": false}
     410 cursor older than the journal keeps → list the tree again
GET  /v2/notify    WebSocket; the server sends {"ns": 42, "seq": 1047}
POST /v2/files/{file_id}/restore   {"rev": 5}    200 {"rev": 8, "seq": 1052}
POST /v2/shares    {"folder_id": "d17…", "user": "ana@…", "role": "editor"}
     201 {"ns": 77}
POST /v2/links     {"file_id": "f81…", "role": "viewer", "expires_at": "…"}
     201 {"url": "https://…/s/<128-bit random token>"}
```

The commit carries the blocklist, never the bytes: when the namespace already owns every chunk, as for a rename, a copy or a restore, it succeeds at once, and otherwise it fails with 422 and the hashes to upload first, the protocol Dropbox has described for its desktop client. `base_rev` makes the commit a compare-and-set; a new file omits it and gets its id in the reply. The idempotency key matters because a commit whose response was lost would otherwise return as a conflict with itself. Chunk PUTs need no key, since a chunk is named by its hash, and chunks are served only to callers who can read a namespace that owns them.

### Data Model

```text
namespaces  ns_id PK | owner_id | head_seq       a user's root or a shared
            folder; all rows of a namespace live on that namespace's shard
mounts      (user_id, ns_id) PK | path | role    + index (ns_id, user_id)
files       (ns_id, file_id) PK | parent_id | name | rev | seq | deleted
            unique (ns_id, parent_id, folded name)          the current tree
journal     (ns_id, seq) PK | file_id | rev | op | parent_id | name | size |
            blocklist | device | time          append-only, a row per change
            index (ns_id, file_id, seq)          → a file's version history
chunk_refs  (ns_id, sha256) PK                 chunks this namespace owns
links       token PK | ns_id | file_id | role | expires_at
blocks      sha256 PK | location | size | ns_count       the block index
```

Everything hangs on the namespace, a root directory with its own journal: each user has one, and every shared folder is one, mounted into each member's tree, which is how Dropbox organises its metadata. A namespace's rows share a shard, so a commit is a single-shard transaction, the journal numbers changes densely, and access is checked once per namespace through `mounts`. The `files` table is the directory trie of #143 flattened into rows: each row points at its parent, and the unique key on a case-folded, normalised name plays the trie's child map, which also refuses `report.txt` beside `Report.txt`, a pair the default Mac and Windows file systems cannot hold. Files carry 64-bit Snowflake-style ids (#145), minted by any metadata server without coordination, so moving a folder of a million files is one updated row.

The journal is append-only, like Dropbox's server file journal, and its second index makes it each file's history, a snapshot array (#47): the version current at sequence number S is the last row at or before S, one binary search away. Very long blocklists are stored as chunks themselves. Transactions and unique keys call for a sharded relational database, MySQL behind a sharding layer or Spanner; the block index is one huge hash-to-location map for a key-value store such as Bigtable, spread evenly because hashes are uniform. Share links use 128-bit random tokens, not Chapter 1's short codes, because they must be unguessable.

### Architecture

```dot
rankdir=TB;
other    [label="other devices", class=client];
desk     [label="desktop client\nchunker", class=client];
notify   [label="notification\nservers", class=service];
meta     [label="metadata\nservice", class=service];
blocks   [label="block\nservice", class=service];
mcache   [label="metadata\ncache", class=cache];
mdb      [label="metadata DB\nby namespace", class=store];
bindex   [label="block index\nby hash", class=store];
bstore   [label="block\nstore", class=store];
events   [label="change\nevents", class=queue];
fanout   [label="fan-out\nworkers", class=worker];
registry [label="connection\nregistry", class=cache];
gc       [label="GC jobs", class=worker];
desk -> meta [label=" commit"];
desk -> blocks [label=" put chunks"];
other -> meta [label=" changes"];
other -> blocks [label=" get chunks"];
other -> notify [dir=back, style=dashed, label=" hint"];
meta -> mcache [label=" roles, heads"];
meta -> mdb [label=" txn"];
blocks -> mdb [label=" owner"];
blocks -> bindex [label=" lookup"];
blocks -> bstore [label=" new bytes"];
meta -> events [style=dashed, label=" ns, seq"];
events -> fanout [style=dashed];
fanout -> registry [label=" subscribers"];
notify -> fanout [dir=back, style=dashed, label=" hint"];
mdb -> gc [dir=back, label=" sweep"];
bindex -> gc [dir=back];
bstore -> gc [dir=back, label=" delete"];
{rank=same; other; desk}
{rank=same; notify; meta; blocks}
{rank=same; mcache; mdb; bindex; bstore}
{rank=same; events; fanout; registry; gc}
```

Every device runs the same client; the diagram follows one upload. The desktop client watches the synced folder, chunks and hashes each changed file and commits its blocklist to the metadata service, which checks the caller's role in the metadata cache, compares the blocklist with the chunks the namespace owns and answers 422 with the missing ones. The client puts those to the block service, which verifies each SHA-256, looks the chunk up in the block index, writes the bytes to the erasure-coded block store only if they are new to the whole system, and records in the metadata DB that the namespace owns the chunk. The second commit is one transaction on the namespace's shard: check `base_rev`, update the `files` row, raise `head_seq`, append the journal row, and only then answer 200.

The sync path begins there. The metadata service publishes the namespace and its new sequence number to the change events topic; fan-out workers ask the connection registry which notification servers hold a device that mounts the namespace and send each a hint, which goes down those devices' WebSockets. Each other device calls changes with its cursor, fetches from the block service only the chunks it lacks, verifies their hashes and moves the finished file into place with one rename, so nobody opens half a file. Off the request path, GC jobs sweep ownership rows no retained version needs, lower counts in the block index and delete unowned chunks from the block store.

### Deep Dives

#### Cutting files so that an edit moves only what changed

Uploading the whole file on every save fails at once: one line inserted into a 1 GB CSV costs a 1 GB upload, and an upload that drops at 9 GB of 10 starts over. Fixed 4 MB blocks, hashed and sent only when changed, cure appends, overwrites and restarts, but not insertions: one byte added near the start moves every later byte, so every later block gets new contents and a new hash.

```text
fixed 4 MB blocks      |  A  |  B  |  C  |  D  |
insert 10 bytes in A   |  A' |  B' |  C' |  D' |E'|    every later block moved
content-defined cuts   |  A    | B  |    C    | D |
insert 10 bytes in A   |  A'    | B  |    C    | D |   only A changed
```

The cure is to let the content choose the cuts. The client slides a 48-byte window over the file and keeps a rolling hash of it, the trick of Rabin-Karp (#120), so each one-byte step costs constant time. Once a chunk is 512 KB long, the chunker cuts wherever the low 19 bits of the hash match a fixed nonzero pattern, which on random-looking data happens once in 2^19 positions, so chunks average 512 KB plus 512 KB, or 1 MB; a 4 MB cap covers inputs, such as runs of zeros, that never cut. A cut depends on the bytes in the window, not on its offset, so an insertion changes the chunk it lands in and perhaps a neighbour, while every later cut falls on the same bytes as before. The LBFS research file system chunked this way in 2001, and backup tools such as restic still do.

Each chunk is named by its SHA-256, and with collisions out of reach, equal hashes count as equal bytes, whereas Rabin-Karp must confirm each hit character by character. The name deduplicates, since successive versions share all but a chunk or two; it guards integrity, since the block service, the client and a background scrubber all rehash what they handle; and it makes uploads resumable without session state, since a reconnecting client simply commits again. Chunks travel compressed, with a modified Brotli at Dropbox, but the hash covers the uncompressed bytes.

Naming by content has two costs. Deletion becomes garbage collection: the GC jobs mark the chunks each namespace's retained versions reference, sweep the other `chunk_refs` rows, lower `ns_count`, and delete bytes once the count is zero and a grace period has passed. And global dedup leaks. A server that skipped chunks any user had stored would reveal whether someone holds a given file, and if a hash alone could claim a chunk, the hash would be a key to its contents; in 2011 a tool called Dropship used Dropbox's deduplication to transfer files between accounts given only their block hashes. So bandwidth is deduplicated only within a namespace and storage globally, behind the block service, where claiming a new chunk takes its bytes and the reply never says whether they were new.

#### The journal, cursors and push hints

Listing the whole tree every 30 seconds is absurd for a hundred million devices, and asking for changes since a timestamp fails quietly: server clocks differ, and a transaction that takes its timestamp first can commit last, so a device whose cursor has passed that time never sees the change.

The journal fixes the order. Every commit takes the next sequence number from `head_seq` inside its transaction, and since commits to a namespace serialise on that row, the numbers are dense, increasing and visible in order: once a device has read up to 1046, no change at or below 1046 can appear. A cursor holds the last number applied in each mounted namespace; the changes call returns the rows after each, page by page, reading only journals whose heads in the metadata cache have moved, and since rows carry their `rev`, applying one twice is harmless. A new device lists the tree as of some number and follows the journal from there, and a device that was away longer than the 30 days of history the journal keeps gets 410 and lists again.

Telling a device to look is a separate, deliberately weak channel. A notification carries only a hint, "namespace 42 is at 1047", so a lost one costs seconds, never a change: the next hint, or the safety poll each client runs every few minutes, catches up from the cursor, and the channel needs neither persistence nor acknowledgements. Dropbox's clients hold a long poll to a notification server; a WebSocket carries the same hint without the re-polls, over a million empty requests a second at a 90-second timeout, so this design prefers WebSockets and falls back to long polling, while a phone in the background simply catches up when the app opens. Bursts are coalesced: 5,000 photos dropped into a shared folder make 5,000 commits, but each notification server forwards at most one hint per namespace per device each second.

#### Conflicts and conflicted copies

Last writer wins by timestamp is the naive answer and the worst: it silently destroys an edit and trusts device clocks, which drift, and the timestamps of a laptop that was offline all day. Locking prevents conflicts, but a lock needs the server, and the devices that conflict are mostly the ones that could not reach it.

The server decides by commit order. A commit names its `base_rev`, and the shard transaction accepts it only if the file is still at that revision, so the first commit wins and the second gets 409. The losing client keeps both: it renames its file to `q3 (Ana's conflicted copy 2026-10-12).csv`, commits that as a new file and downloads the winner under the original name, so no edit is lost and a person merges the two. Dropbox's conflicted copies follow the same rule, naming the editor and the date, with the version saved last becoming the copy. The server cannot merge opaque bytes; merging edits as they happen, with OT or CRDTs, is for an editor that owns its format (Chapter 11).

The client must also know which side changed. Dropbox's sync engine, Nucleus, keeps three trees: the remote tree read from the journal, the local tree on disk, and the synced tree, the last state both agreed on, which serves as a merge base.

```text
local vs synced   remote vs synced   action
unchanged         unchanged          nothing
unchanged         changed            download the remote version
changed           unchanged          upload, with base_rev = the synced rev
changed           changed            same hash: nothing; else conflicted copy
```

Without the merge base, a laptop back from a week offline could not tell its own edits from everyone else's. The remaining cases get rules: an edit beats a delete, because losing work is worse than restoring a file; a rename and an edit touch different fields of one id, so the client that gets 409 simply recommits on top; two files created with the same name collide on the unique key, and the second becomes a conflicted copy; and of two concurrent moves, A into B and B into A, the server rejects whichever would make a folder its own ancestor, found by walking parent pointers up from the destination.

### Scaling and Bottlenecks

The metadata tier strains first, from hot namespaces rather than total load. Commits to one namespace serialise on its head row, roughly a thousand a second at a millisecond each, so bulk operations commit hundreds of files per transaction and a company-wide folder works better as many shared folders. Namespaces map to shards through a directory, not a hash, so one that outgrows its neighbours can move alone. Hot reads are the other half: a commit to a folder shared with 20,000 employees sets off 20,000 changes calls for the same rows within a second, which the metadata cache absorbs by holding each namespace's head and journal tail.

Block servers are stateless and bandwidth-bound, and the block store is the object store of Chapter 33; its one hot spot, a viral public link, suits a CDN, since immutable chunks never go stale. The notification fleet grows with connected devices, and its danger is the reconnect storm after a server or region drops, which jittered exponential backoff spreads over minutes. Each namespace has a home region for commits, and chunks are copied to a second region in the background.

### Failure Modes

A dropped upload resumes by committing again. A commit whose response was lost is answered from its idempotency key rather than failing with 409 against its own revision, and chunks uploaded for a commit that never happened are swept as unreferenced.

The journal sets the strictest rule: a sequence number, once read, must never be reissued. A shard that failed over to an asynchronous standby missing the last commits would hand out 1047 again for a different change, and every device that had read the lost 1047 would skip the new one forever. So shards replicate through a consensus protocol and acknowledge a commit only once a majority of replicas hold it, and a failover pauses commits for seconds and loses none. A dead notification server's devices reconnect elsewhere and pull with their cursors, and a corrupted chunk, caught by its hash, is rebuilt from its erasure-coded fragments.

The most damaging failure is the client doing its job: ransomware that encrypts a laptop, or a mistaken mass deletion, produces valid commits that sync everywhere. Version history is the defence. Rewinding a namespace to before sequence number S is the snapshot-array lookup for every file, committed as new versions with no bytes moved, and a device that rewrites thousands of files in minutes trips an alarm that pauses its sync.

### Trade-offs and Alternatives

The chunker is the first dial. Dropbox uses fixed, aligned 4 MB blocks, which need no rolling hash and lose only when bytes are inserted or removed mid-file; appends and in-place overwrites, the way logs, databases and disk images change, leave the other blocks alone. Neither scheme helps with compressed formats: change one cell of a spreadsheet stored as a zip archive and most of the compressed bytes after it change. Smaller chunks find more duplicates, but 64 KB chunks would make the block index sixteen times larger; an rsync-style binary delta of a changed chunk against its predecessor is the cheaper refinement.

Dedup scope is the second dial: global client-side dedup saves the most bandwidth and leaks, per-namespace dedup leaks nothing, and end-to-end encryption with per-user keys gives up dedup across users. Conflicted copies never lose an edit, locks suit teams that are always online, and co-editing suits formats the service owns. Mirroring every file on every device costs disk and bandwidth, and Google Drive for desktop lets users choose between mirroring files and streaming them on open. A sharded MySQL store makes a move between namespaces a two-phase commit; Spanner (Chapter 38) makes it an ordinary transaction.

### What Interviewers Probe

Expect these questions. Why chunk at all? For resumable, parallel uploads, versions that share storage and edits that send only what changed. How big, and fixed or content-defined? About a megabyte, cut by content so that an insertion does not shift every later chunk; sketch the rolling hash. How does a second device learn of a change, and what if the notification is lost? A hint, then a pull from the journal by cursor, so a lost hint only delays the pull. What if two people edit one file offline? The first commit wins on its base revision and the second becomes a conflicted copy. How is a shared chunk deleted? Ownership per namespace, a count per chunk, a sweep and a grace period. Where does the metadata store break? On hot namespaces.

Strong candidates raise more unprompted: global dedup leaks whether a file exists, so a hash must never stand in for the bytes; journal numbers must never be reissued, which rules out asynchronous metadata replication; ids rather than paths make moves single operations, with names compared case-insensitively on the server; version history is the defence against ransomware; and quotas count logical bytes, or they would leak dedup too.

*Algorithms:* #120 Rabin-Karp · #47 Snapshot Array · #145 Unique ID Generator · #143 In-Memory File System
