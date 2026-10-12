# Q017. Design enterprise SaaS connectors

## Scope and success

Connect approved customer systems such as document stores, CRM, and issue trackers. Clarify read versus write capabilities, identity mapping, source rate limits, freshness, and deletion semantics. A connector succeeds when it preserves source meaning and access while exposing a stable application contract.

## Architecture and request path

A connector control plane manages tenant configurations and protected credential references. Ingestion workers fetch changes with cursors and publish normalized records. Interactive adapters expose narrow read/action APIs through the CX gateway. Keep batch synchronization separate from customer-turn traffic.

Use source-specific adapters for pagination, permission representation, webhook verification, and error translation. An integration contract defines which fields are authoritative and how unknown or unavailable data is represented.

## Data and contracts

Store tenant, source instance, connection version, scopes, cursor, last successful sync, and source IDs. Preserve source versions and ACL lineage. Mutation operations retain an idempotency reference and external object ID. Credential rotation should update references without copying secrets into CX examples or logs.

## Failure, security, and scale

Handle expired tokens, revoked scopes, cursor invalidation, throttling, and partial pages. Rate-limit by source tenant and back off with bounded retries. Dead-letter malformed records with safe diagnostics. A service-level credential must not accidentally grant users all documents it can read.

## Trade-off and validation

Managed connectors shorten delivery when their identity and action semantics fit. Custom adapters offer control but increase maintenance. Verify actual capabilities with representative data, permission changes, schema updates, and source outages. Monitor freshness lag and contract conformance.

## Interview follow-up answered

**The source changes its API unexpectedly.** Freeze unsafe mutations, keep compatible read paths where possible, alert operators, and version the adapter. Replay captured sandbox fixtures against the new contract. Resume only after the scope and permission behavior are verified; a successful HTTP response alone is insufficient.
