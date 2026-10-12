# Q010. Design permission-aware retrieval

## Scope and success

Search enterprise content while honoring tenant, user, group, and document permissions. Establish whether revocation must be immediate and whether source systems support authoritative checks. The invariant is that no inaccessible evidence enters generation or reaches the customer.

## Architecture and request path

The channel verifies identity and the webhook resolves trusted tenant/group context. The retrieval service applies supported ACL filters during candidate search. It checks candidate permissions again when source freshness requires it, reranks only permitted evidence, and validates citation access before responding through CX.

Permission synchronization runs independently. Membership and document ACL changes update versioned access metadata and invalidate relevant caches. Search results cannot rely on an LLM to decide whether the user deserves access.

## Data and contracts

Store document ACL references, tenant boundaries, membership versions, revocation markers, and evidence provenance. Cache keys include an authorization fingerprint and corpus generation. Retrieval outputs contain approved source IDs rather than broad raw records. Denial responses should not reveal restricted document titles.

## Failure, security, and scale

Fail closed when required authorization cannot be verified. Post-filtering alone can miss all relevant permitted results after top-k unauthorized candidates occupy the search window; use prefiltering where supported and bounded overfetch only as an explicit quality strategy. Never remove ACL filters to improve recall.

## Trade-off and validation

Per-request source checks improve revocation semantics but add latency and source load. Versioned local policy can be faster when the customer accepts bounded synchronization lag. Test tenant separation, group removal, nested groups, cache reuse, revoked citations, and denied-source existence leakage.

## Interview follow-up answered

**The user belongs to thousands of groups.** Normalize policy into indexed access sets or a dedicated authorization service, cache trusted membership with versioning, and benchmark filter limits. Keep tenant isolation mandatory. If the search engine cannot express the policy efficiently, partition the corpus or change the retrieval design rather than truncating the user's permissions arbitrarily.
