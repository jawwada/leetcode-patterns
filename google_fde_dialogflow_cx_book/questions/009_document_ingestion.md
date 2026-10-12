# Q009. Design document ingestion for policy Q&A

## Scope and success

Ingest approved policy sources into a searchable corpus with permissions, effective dates, citations, and deletions. Clarify update frequency, file formats, maximum size, and freshness targets. Success means serving retrieves the intended current evidence and can explain its lineage.

## Architecture and request path

Connectors emit source-change events. A durable queue triggers fetch, malware/format checks, parsing, normalization, metadata extraction, chunking, and embedding. Workers write versioned artifacts and build an index generation. Publication occurs after completeness and quality checks, then serving switches the active pointer.

CX does not parse documents during the customer's turn. It calls the serving system, which reads a published generation. Keep rejected documents in an operator-visible error queue with safe diagnostics.

## Data and contracts

Use source ID plus source version and parser configuration as an ingestion key. Store raw-object reference, normalized text, chunk hashes, ACL version, effective period, and embedding version. A manifest records every expected artifact. Tombstones represent deletion and invalidate retrieval and caches.

## Failure, security, and scale

Workers are idempotent under repeated events. Large documents can be partitioned with bounded memory and reassembled by manifest. Parsing treats documents as untrusted input. Encrypt artifacts, isolate tenants, and quarantine malicious files. Partial failures must not publish an apparently complete index.

## Trade-off and validation

Full rebuilds are operationally simple but expensive and slow; incremental processing lowers freshness lag but complicates dependency tracking. Start with generation-based rebuilds and add incremental changes where requirements justify them. Evaluate table extraction, exceptions, citation fidelity, deletion latency, and end-to-end update lag.

## Interview follow-up answered

**The embedding model changes.** Build a compatible new corpus and query-embedding path, evaluate it, then switch generation pointers together. Mixing embeddings from incompatible models in one search space makes similarity unreliable. Preserve the old generation long enough for rollback and audit.
