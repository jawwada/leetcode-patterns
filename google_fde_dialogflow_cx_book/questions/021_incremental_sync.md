# Q021. Design incremental document synchronization

## Scope and success

Keep a retrieval corpus synchronized with source edits, permissions, and deletions. Define allowed lag and whether a source provides change cursors, webhooks, or only polling. Success means every eligible source change eventually reaches the published corpus without older work overwriting newer state.

## Architecture and request path

Connectors capture changes into a durable log. Workers fetch the referenced source version, normalize it, regenerate affected chunks, and update search artifacts. A checkpoint advances only after required records are durable. Periodic reconciliation compares source inventory against the index to catch missed events.

CX reads the current published generation and can return an explicit freshness timestamp. It does not participate in synchronization. Batch rebuilds provide a repair path when a source cursor becomes invalid.

## Data and contracts

Track source instance, cursor, document ID, source version, event sequence, content hash, ACL version, and indexed status. Events are idempotent by source identity/version. Use conditional writes or monotonic versions so delayed old events cannot resurrect deleted content. Tombstones persist long enough to defeat late arrivals.

## Failure, security, and scale

Retry transient fetches with source-specific limits. Dead-letter malformed changes while exposing freshness degradation to operators. Apply access revocation separately if its deadline is shorter than ordinary indexing lag. Bound concurrent embedding jobs and use backpressure rather than exhausting source quotas.

## Trade-off and validation

Incremental updates are faster and cheaper but require careful ordering and repair. Full snapshots are simpler to compare but slower. Combine incremental processing with periodic authoritative reconciliation. Test out-of-order events, duplicate delivery, cursor reset, deletion/recreation, and permission-only changes.

## Interview follow-up answered

**The source webhook drops events for an hour.** Resume from an authoritative change cursor if available, otherwise run a bounded reconciliation or snapshot. Mark the affected source freshness state and avoid claiming current answers. Webhooks accelerate detection; they should not be the only mechanism establishing corpus completeness.
