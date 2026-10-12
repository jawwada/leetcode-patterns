# Q026. Design GraphRAG for connected enterprise knowledge

## Scope and success

Answer relationship questions such as which services depend on a deprecated library and which team owns them. Assume both documents and structured relationships. Success requires a supported path through current permitted entities, not simply semantically similar passages.

## Architecture and request path

Ingestion extracts or imports entities and relationships with provenance. A graph store retains verified structured facts; a text index retains explanatory documents. CX collects ambiguous entities, then a retrieval backend combines bounded graph traversal with text retrieval. Generation explains the resulting evidence and cites the underlying sources.

Use schema-driven traversals for known questions before introducing broad model-generated queries. Every traversal is bounded by depth, fanout, and authorization. Keep inferred edges distinguishable from authoritative imported relationships.

## Data and contracts

Nodes have tenant, entity type, canonical ID, aliases, access policy, and validity period. Edges carry relation type, source/version, confidence provenance, and effective dates. Retrieval returns paths, source passages, and uncertainty. Entity resolution preserves ambiguous candidates rather than merging by name alone.

## Failure, security, and scale

Apply access checks to nodes, edges, and supporting documents. Hidden intermediate relationships can leak restricted facts even if the endpoints are public. Limit graph expansion and cache only under compatible access/version context. Rebuild or invalidate derived edges when source documents change.

## Trade-off and validation

Graph structure improves multi-hop relationship tasks but adds extraction, maintenance, and identity-resolution costs. Plain hybrid retrieval may be better for ordinary FAQs. Evaluate against both baselines using path correctness, source support, freshness, latency, and access isolation.

## Interview follow-up answered

**Two sources disagree about ownership.** Store both assertions with provenance and effective dates, prefer an agreed authoritative source where policy specifies it, and disclose unresolved conflict. A graph must not collapse contradictory evidence into one silently chosen edge because traversal expects a single answer.
