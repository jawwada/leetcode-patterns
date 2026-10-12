# Q013. Design conversation sessions and durable memory

## Scope and success

Maintain coherent CX interactions and optionally remember approved preferences across visits. Separate temporary workflow state, durable operations, and user-consented memory. Success includes correct resumption without sharing another user's context or reviving an invalid action.

## Architecture and request path

The channel issues a random session and binds it to verified identity. CX stores current page and conversational parameters. Domain services persist proposals and operations. A memory service stores approved facts such as language preference, with provenance and expiry. On a new conversation, the backend loads only permitted relevant memory.

A resumption flow looks up pending operations or saved tasks, rechecks identity and eligibility, and presents a clear choice. Avoid reconstructing authority from a generated conversation summary. Keep turn processing ordered for each CX session.

## Data and contracts

Memory records contain subject, tenant, fact type, value, source, consent basis, confidence/provenance, expiry, and deletion status. Task records contain state version and authoritative references. A session binding contains principal, authentication expiry, and channel. Treat inferred preferences as distinguishable from explicit user statements.

## Failure, security, and scale

When memory is unavailable, continue without personalization where possible. When authentication expires, reverify before protected work. Deletion must cover derived memories and caches. Avoid storing secrets or full histories by default. Partition durable records by tenant and subject, with bounded retrieval.

## Trade-off and validation

More memory can improve continuity but creates stale assumptions and privacy costs. Prefer narrow typed preferences over unrestricted summaries. Test expired sessions, account switching, shared devices, contradictory preferences, deletion, and simultaneous conversations.

## Interview follow-up answered

**The customer returns a week later to finish a return.** Load the durable task after verification, check whether the proposal or policy has changed, and reconfirm a new proposal if needed. CX session continuity is convenient but is not required for a durable business journey to survive.
