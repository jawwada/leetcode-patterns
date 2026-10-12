# Q023. Design a large-scale vector index

## Scope and success

Search millions of embeddings under tenant filters, updates, and bounded latency. Define dimensions, distance metric, recall target, freshness, and index memory budget. Success is useful candidate retrieval at scale; nearest-neighbor similarity does not establish answer truth.

## Architecture and request path

An ingestion pipeline produces versioned embeddings. A search tier partitions vectors using tenant/corpus boundaries and an approximate-nearest-neighbor strategy appropriate to the workload. Query services generate a compatible query embedding, apply supported metadata filtering, search bounded shards, merge results, and return candidates to the retrieval webhook used by CX.

Maintain an active index generation and a build/update path. Separate index construction resources from latency-sensitive serving. Use replicas for read capacity and recovery where the selected engine supports them.

## Data and contracts

Vectors reference chunk IDs, model/configuration version, document version, and access metadata. The query specifies trusted tenant, filters, candidate count, and deadline. Results include IDs, distances, and index generation. Keep source text in an authoritative artifact store to avoid losing lineage during rebuild.

## Failure, security, and scale

Apply admission control and monitor memory, fanout, and hot tenants. Filter semantics must be verified; postfiltering can reduce permitted recall dramatically. A partial shard response is a degraded result, not complete coverage. Deletions and tombstones prevent obsolete or unauthorized vectors from reappearing.

## Trade-off and validation

Approximation lowers latency and memory cost with recall loss. Compression trades precision for footprint. Tune against exact search on a representative sample, then evaluate downstream task quality. Measure filtered recall, update lag, p95 latency, and capacity during rebuild.

## Interview follow-up answered

**One tenant has a hundred times more vectors.** Give it an appropriate partition/serving tier and independent resource budget. Avoid forcing every small tenant query across its shards. Rebalance using versioned routing and validate query/index compatibility during movement.
