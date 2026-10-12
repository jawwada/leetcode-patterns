# Q018. Design a multi-tenant conversational platform

## Scope and success

Host agents for multiple customers with isolated identity, data, configuration, and budgets. Decide which customers require dedicated infrastructure. Success combines correct isolation, predictable performance, and independently releasable tenant behavior.

## Architecture and request path

An authenticated channel resolves tenant from trusted routing and identity. A control plane maps tenant to CX agent/environment, backend configuration, search corpus, secrets, and region. The gateway attaches authoritative tenant context to every request. Domain, retrieval, and memory services enforce it independently.

Keep onboarding/configuration outside the turn path. Publish validated tenant configurations atomically and retain versions. Separate runtime callers from tenant administrators and platform deployment principals.

## Data and contracts

Use tenant in every relevant key and uniqueness constraint. Store release manifests, quotas, policy, data residency, source connections, and lifecycle status. Encryption keys and logs can be partitioned when required. Cache keys include tenant and authorization context; filenames and embedding indices also need isolation.

## Failure, security, and scale

Apply tenant-specific rate, concurrency, and token budgets. A noisy customer's ingest or agent loop must not starve others. Protect shared database connection capacity. Test cross-tenant identifiers, misrouted channels, background workers, cache reuse, and administrative access.

## Trade-off and validation

Shared infrastructure lowers cost and simplifies management but increases blast radius. Dedicated projects or deployments can meet stricter isolation and residency at greater operational cost. Offer explicit tiers based on customer requirements rather than one universal topology. Measure both isolation and per-tenant SLOs.

## Interview follow-up answered

**One customer requires complete operational separation.** Provision a dedicated project/deployment with separate identities, storage, search, telemetry, and quotas. Reuse release tooling and contracts while removing shared runtime dependencies where required. Document whether platform administrators still have access and how that access is audited.
